"""Metric rectification of the top-view product photo using the board outline (assumed to be a
rectangle) + a pinhole camera with square pixels; absolute scale from the 2.54 mm header pitch.

usage: e_rectify.py IMAGE [ppx ppy]
Prints board size, pad row, hole centres in board coordinates (mm):
  x = distance from the header-end short edge, y = distance from the long edge next to pin 1 (+5V).
Also reports sensitivity to the assumed principal point and independent shape checks
(mounting-hole rings must be circles, the QFN body must be 6.0 x 6.0 mm).
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src = sys.argv[1]
A = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255.0
Himg, Wimg = A.shape[:2]
r, g, b = A[..., 0], A[..., 1], A[..., 2]
lum = A.mean(axis=2)
mx = A.max(axis=2); mn = A.min(axis=2)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
blueness = b - 0.5 * (r + g)

# corners from e_measure.py (sub-pixel edge fits)
TL = np.array([71.87, 282.01]); TR = np.array([1467.87, 281.49])
BL = np.array([74.79, 1051.57]); BR = np.array([1459.64, 1065.08])


def hom(p):
    return np.array([p[0], p[1], 1.0])


def line(p, q):
    return np.cross(hom(p), hom(q))


def bore_centroids():
    """white see-through bores of the 13 header pads."""
    x0, x1, y0, y1 = 1380, 1445, 330, 1020
    w = (lum[y0:y1, x0:x1] > 0.80) & (sat[y0:y1, x0:x1] < 0.12)
    w = ndi.binary_opening(w, structure=np.ones((3, 3), bool))
    lab, n = ndi.label(w)
    out = []
    for i in range(1, n + 1):
        m = lab == i
        a = m.sum()
        if 150 < a < 900:
            cy, cx = ndi.center_of_mass(m)
            out.append((cx + x0, cy + y0, a))
    out.sort(key=lambda t: t[1])
    return out


def ring_ellipse(ax, ay, h=60):
    """outer boundary of the plated ring of a mounting hole -> ellipse fit (centre, axes)."""
    w = blueness[ay - h:ay + h, ax - h:ax + h] < 0.08
    w = ndi.binary_opening(w, structure=np.ones((5, 5), bool))
    lab, n = ndi.label(w)
    li = lab[h, h]
    comp = ndi.binary_fill_holes(lab == li)
    bd = comp & ~ndi.binary_erosion(comp)
    yy, xx = np.nonzero(bd)
    return xx + ax - h, yy + ay - h


def fit_ellipse(x, y):
    xm, ym = x.mean(), y.mean()
    xs, ys = x - xm, y - ym
    D = np.stack([xs * xs, xs * ys, ys * ys, xs, ys, np.ones_like(xs)], axis=1)
    _, _, vt = np.linalg.svd(D, full_matrices=False)
    a, b_, c, d, e, f = vt[-1]
    M = np.array([[a, b_ / 2], [b_ / 2, c]])
    cen = -np.linalg.solve(2 * M, np.array([d, e]))
    val = f + 0.5 * (d * cen[0] + e * cen[1])
    w, v = np.linalg.eigh(M)
    ax = np.sqrt(np.abs(-val / w))
    order = np.argsort(-ax)
    ang = np.degrees(np.arctan2(v[1, order[0]], v[0, order[0]]))
    return np.array([cen[0] + xm, cen[1] + ym]), ax[order], ang


pads_px = bore_centroids()
hole_seeds = {"mid_pin13side": (943, 331), "mid_pin1side": (940, 1016), "ant_pin13side": (207, 421), "ant_pin1side": (209, 920)}
ring_pts = {k: ring_ellipse(*v) for k, v in hole_seeds.items()}


def analyse(pp, verbose=True):
    c = np.array(pp, float)
    V1 = np.cross(line(TL, TR), line(BL, BR))  # vanishing point of the long (x) direction
    V2 = np.cross(line(TL, BL), line(TR, BR))  # vanishing point of the short (y) direction
    v1 = V1[:2] / V1[2]; v2 = V2[:2] / V2[2]
    f2 = -np.dot(v1 - c, v2 - c)
    if f2 <= 0:
        return None
    f = np.sqrt(f2)
    Kinv = np.array([[1 / f, 0, -c[0] / f], [0, 1 / f, -c[1] / f], [0, 0, 1]])
    r1 = Kinv @ V1; r1 /= np.linalg.norm(r1)
    r2 = Kinv @ V2; r2 /= np.linalg.norm(r2)
    # orient: r1 from the header end (right) towards the antenna end (left); r2 from pin1 edge (bottom) to pin13 edge (top)
    X0 = Kinv @ hom(BR)  # origin: header-end / pin-1 corner (bottom right in the image)

    def plane(p):
        d = Kinv @ hom(p)
        M = np.stack([d, -r1, -r2], axis=1)
        s, a_, b_ = np.linalg.solve(M, X0)
        return np.array([a_, b_])

    # fix signs so that BL has +x and TR has +y
    sx = np.sign(plane(BL)[0]); sy = np.sign(plane(TR)[1])

    def brd(p):
        q = plane(p)
        return np.array([sx * q[0], sy * q[1]])

    pads = np.array([brd(p[:2]) for p in pads_px])
    pitch_raw = np.hypot(*np.diff(pads, axis=0).T)
    scale = 2.54 * (len(pads) - 1) / np.hypot(*(pads[-1] - pads[0]))  # mm per unit
    S = lambda p: brd(p) * scale
    cTL, cTR, cBL, cBR = S(TL), S(TR), S(BL), S(BR)
    L = 0.5 * (np.linalg.norm(cBL - cBR) + np.linalg.norm(cTL - cTR))
    W = 0.5 * (np.linalg.norm(cTR - cBR) + np.linalg.norm(cTL - cBL))
    res = {"f": f, "L": L, "W": W, "scale": scale}
    padsmm = pads * scale
    res["pads"] = padsmm
    res["pitch"] = pitch_raw * scale
    holes = {}
    for k, (xx, yy) in ring_pts.items():
        pts = np.array([S((x, y)) for x, y in zip(xx[::3], yy[::3])])
        cen, axes, ang = fit_ellipse(pts[:, 0], pts[:, 1])
        holes[k] = (cen, axes, ang)
    res["holes"] = holes
    if verbose:
        print(f"principal point {tuple(pp)}: focal length {f:.0f}px; vanishing points x-dir ({v1[0]:.0f},{v1[1]:.0f}), y-dir ({v2[0]:.0f},{v2[1]:.0f})")
        print(f"  board length {L:.3f} mm (pin1-side edge {np.linalg.norm(cBL - cBR):.3f}, pin13-side edge {np.linalg.norm(cTL - cTR):.3f})")
        print(f"  board width  {W:.3f} mm (header end {np.linalg.norm(cTR - cBR):.3f}, antenna end {np.linalg.norm(cTL - cBL):.3f})")
        print(f"  corners: BR {cBR.round(3)}, BL {cBL.round(3)}, TR {cTR.round(3)}, TL {cTL.round(3)}")
        print("  pads (x from header edge, y from pin-1 long edge), pin 1 first:")
        for i, p in enumerate(padsmm[::-1], 1):
            print(f"    pin {i:2d}: x={p[0]:6.3f} y={p[1]:7.3f}")
        print("  pitches:", np.round(res["pitch"][::-1], 3).tolist())
        print(f"  pad row x mean {padsmm[:,0].mean():.3f} (min {padsmm[:,0].min():.3f} max {padsmm[:,0].max():.3f}); pin1 y {padsmm[-1,1]:.3f}; pin13 y {padsmm[0,1]:.3f}; pin13 to far edge {W - padsmm[0,1]:.3f}; row centre y {padsmm[:,1].mean():.3f} (board centre {W/2:.3f})")
        for k, (cen, axes, ang) in holes.items():
            print(f"  hole {k:14s}: x={cen[0]:7.3f} y={cen[1]:7.3f}  ring outer d {2*axes[0]:.3f} x {2*axes[1]:.3f} mm (axis ratio {axes[0]/axes[1]:.4f}, major axis angle {ang:.0f} deg)")
        hm1, hm13 = holes["mid_pin1side"][0], holes["mid_pin13side"][0]
        ha1, ha13 = holes["ant_pin1side"][0], holes["ant_pin13side"][0]
        print(f"  mid pair spacing {np.linalg.norm(hm13 - hm1):.3f}; antenna pair spacing {np.linalg.norm(ha13 - ha1):.3f}; pair distance (x) {0.5*(ha1[0]+ha13[0]) - 0.5*(hm1[0]+hm13[0]):.3f}")
        print(f"  mid pair x {0.5*(hm1[0]+hm13[0]):.3f} (pin1 {hm1[0]:.3f}, pin13 {hm13[0]:.3f}); antenna pair x {0.5*(ha1[0]+ha13[0]):.3f} (pin1 {ha1[0]:.3f}, pin13 {ha13[0]:.3f}); antenna pair to antenna-end edge {L - 0.5*(ha1[0]+ha13[0]):.3f}")
        print(f"  mid holes to long edges: pin1 side {hm1[1]:.3f}, pin13 side {W - hm13[1]:.3f}; antenna holes: pin1 side {ha1[1]:.3f}, pin13 side {W - ha13[1]:.3f}")
        print(f"  hole pattern centre line y: mid {0.5*(hm1[1]+hm13[1]):.3f}, antenna {0.5*(ha1[1]+ha13[1]):.3f} (board centre {W/2:.3f})")
    res["S"] = S
    return res


pp0 = (Wimg / 2, Himg / 2)
if len(sys.argv) > 3:
    pp0 = (float(sys.argv[2]), float(sys.argv[3]))
print("pads (bore centroids, px):", [(round(x, 1), round(y, 1), int(a)) for x, y, a in pads_px])
base = analyse(pp0)
print()
print("sensitivity to the assumed principal point (L, W, mean ring axis ratio):")
for dx in (-400, -200, 0, 200, 400):
    for dy in (-400, 0, 400):
        rr = analyse((pp0[0] + dx, pp0[1] + dy), verbose=False)
        if rr is None:
            print(f"  pp offset ({dx:+5d},{dy:+5d}): no real focal length")
            continue
        ar = np.mean([h[1][0] / h[1][1] for h in rr["holes"].values()])
        print(f"  pp offset ({dx:+5d},{dy:+5d}): f={rr['f']:7.0f}  L={rr['L']:.3f}  W={rr['W']:.3f}  ring axis ratio {ar:.4f}")
