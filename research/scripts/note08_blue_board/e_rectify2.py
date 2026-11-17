"""Metric rectification of the top-view product photo, v2.

Plane orientation comes from the vanishing line of the board outline (assumed rectangle).
The camera is a pinhole with square pixels; focal length f and principal point pp are NOT known,
so results are reported over a plausible range and the residual corner angle is shown as a check.
Absolute scale: the 2.54 mm header pitch, measured from the soldermask gaps between round pads.

Board frame: x = distance from the header-end short edge, y = distance from the long edge next
to pin 1 (+5V).  usage: e_rectify2.py IMAGE [f ppx ppy]
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src = sys.argv[1]
A = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255.0
blueness = A[..., 2] - 0.5 * (A[..., 0] + A[..., 1])

TL = np.array([71.87, 282.01]); TR = np.array([1467.87, 281.49])
BL = np.array([74.79, 1051.57]); BR = np.array([1459.64, 1065.08])
# pad column: soldermask gaps between round pads 13|12 ... 3|2 (distance t along P0->P1), from e_pitch.py
P0 = np.array([1414.2, 340.0]); P1 = np.array([1406.4, 1012.0])
GAPS_T = np.array([52.26, 104.26, 156.0, 208.28, 258.91, 310.43, 362.71, 413.69, 466.04, 516.84, 568.25])
# pad land centres (circle fits), pin 13 first ... pin 1 last, from e_pads.py
PADS_LAND = [(1413.81, 366.6), (1414.01, 418.15), (1413.14, 470.05), (1412.82, 522.19), (1408.08, 572.15),
             (1411.39, 627.55), (1411.26, 676.99), (1410.48, 728.37), (1409.92, 779.88), (1408.62, 833.13),
             (1409.37, 885.49), (1408.35, 936.31), (1406.76, 984.81)]
HOLE_SEEDS = {"mid_pin13side": (943, 331), "mid_pin1side": (940, 1016), "ant_pin13side": (207, 421), "ant_pin1side": (209, 920)}


def hom(p):
    return np.array([p[0], p[1], 1.0])


def line(p, q):
    return np.cross(hom(p), hom(q))


def ring_boundary(ax, ay, h=60):
    w = blueness[ay - h:ay + h, ax - h:ax + h] < 0.08
    w = ndi.binary_opening(w, structure=np.ones((5, 5), bool))
    lab, n = ndi.label(w)
    comp = ndi.binary_fill_holes(lab == lab[h, h])
    bd = comp & ~ndi.binary_erosion(comp)
    yy, xx = np.nonzero(bd)
    return np.c_[xx + ax - h, yy + ay - h].astype(float)


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
    return np.array([cen[0] + xm, cen[1] + ym]), ax[order]


RINGS = {k: ring_boundary(*v) for k, v in HOLE_SEEDS.items()}
V1 = np.cross(line(TL, TR), line(BL, BR))
V2 = np.cross(line(TL, BL), line(TR, BR))
VL = np.cross(V1, V2)  # vanishing line of the board plane
VL = VL / np.linalg.norm(VL[:2])


class Rect:
    def __init__(self, f, pp):
        self.f, self.pp = f, np.array(pp, float)
        K = np.array([[f, 0, pp[0]], [0, f, pp[1]], [0, 0, 1.0]])
        self.Kinv = np.linalg.inv(K)
        n = K.T @ VL
        self.n = n / np.linalg.norm(n)
        self.tilt = np.degrees(np.arccos(abs(self.n[2])))
        # plane basis
        X_BR, X_BL = self.back(BR), self.back(BL)
        e1 = X_BL - X_BR; e1 /= np.linalg.norm(e1)       # +x: header end -> antenna end, along the pin-1 long edge
        e2 = np.cross(self.n, e1); e2 /= np.linalg.norm(e2)
        if np.dot(self.back(TR) - X_BR, e2) < 0:
            e2 = -e2
        self.e1, self.e2, self.O = e1, e2, X_BR
        # scale from the gap positions along the pad column
        g = np.array([self.raw(P0 + t * (P1 - P0) / np.linalg.norm(P1 - P0)) for t in GAPS_T])
        s = np.r_[0, np.cumsum(np.hypot(*np.diff(g, axis=0).T))]
        k = np.arange(len(s))
        self.scale = 2.54 / np.polyfit(k, s, 1)[0]

    def back(self, p):
        d = self.Kinv @ hom(p)
        return d / np.dot(self.n, d)  # point on plane n.X = 1

    def raw(self, p):
        X = self.back(p) - self.O
        return np.array([np.dot(X, self.e1), np.dot(X, self.e2)])

    def mm(self, p):
        return self.raw(p) * self.scale


def report(f, pp, verbose=True):
    R = Rect(f, pp)
    c = {k: R.mm(v) for k, v in (("BR", BR), ("BL", BL), ("TR", TR), ("TL", TL))}
    Lb, Lt = np.linalg.norm(c["BL"] - c["BR"]), np.linalg.norm(c["TL"] - c["TR"])
    Wh, Wa = np.linalg.norm(c["TR"] - c["BR"]), np.linalg.norm(c["TL"] - c["BL"])
    v1 = c["BL"] - c["BR"]; v2 = c["TR"] - c["BR"]
    ang = np.degrees(np.arccos(np.dot(v1, v2) / np.linalg.norm(v1) / np.linalg.norm(v2)))
    # board frame with the outline as axes (remove tiny shear): x along BR->BL, y measured perpendicular
    L, W = 0.5 * (Lb + Lt), 0.5 * (Wh + Wa)
    pads = np.array([R.mm(p) for p in PADS_LAND])
    holes = {}
    for k, pts in RINGS.items():
        q = np.array([R.mm(p) for p in pts[::2]])
        cen, axes = fit_ellipse(q[:, 0], q[:, 1])
        holes[k] = (cen, axes)
    out = dict(R=R, L=L, W=W, Lb=Lb, Lt=Lt, Wh=Wh, Wa=Wa, ang=ang, pads=pads, holes=holes, corners=c)
    if verbose:
        print(f"f={f:.0f}px pp=({pp[0]:.0f},{pp[1]:.0f}) tilt {R.tilt:.2f} deg; scale {1/R.scale:.3f} px-units/mm; corner angle at header/pin1 corner {ang:.3f} deg")
        print(f"  LENGTH {L:.3f} mm (pin-1 edge {Lb:.3f}, pin-13 edge {Lt:.3f});  WIDTH {W:.3f} mm (header end {Wh:.3f}, antenna end {Wa:.3f})")
        print(f"  pad row: x = {pads[:,0].mean():.3f} (pin13 {pads[0,0]:.3f} ... pin1 {pads[-1,0]:.3f}); pin1 y = {pads[-1,1]:.3f}; pin13 y = {pads[0,1]:.3f} (to far edge {Wh - pads[0,1]:.3f}); span {np.linalg.norm(pads[0]-pads[-1]):.3f}")
        for k, (cen, axes) in holes.items():
            print(f"  hole {k:14s}: x={cen[0]:7.3f} y={cen[1]:7.3f} ring outer dia {2*axes[0]:.3f} x {2*axes[1]:.3f} (ratio {axes[0]/axes[1]:.4f})")
        hm1, hm13 = holes["mid_pin1side"][0], holes["mid_pin13side"][0]
        ha1, ha13 = holes["ant_pin1side"][0], holes["ant_pin13side"][0]
        xm, xa = 0.5 * (hm1[0] + hm13[0]), 0.5 * (ha1[0] + ha13[0])
        print(f"  mid pair spacing {np.linalg.norm(hm13 - hm1):.3f}; antenna pair spacing {np.linalg.norm(ha13 - ha1):.3f}; pair distance {xa - xm:.3f}")
        print(f"  mid pair x {xm:.3f}; antenna pair x {xa:.3f} (to antenna-end edge {L - xa:.3f})")
        print(f"  mid holes to long edges: pin1 {hm1[1]:.3f} / pin13 {W - hm13[1]:.3f}; antenna holes: pin1 {ha1[1]:.3f} / pin13 {W - ha13[1]:.3f}")
    return out


if len(sys.argv) > 4:
    report(float(sys.argv[2]), (float(sys.argv[3]), float(sys.argv[4])))
    sys.exit(0)

print("vanishing points: x-dir", (V1[:2] / V1[2]).round(0), "y-dir", (V2[:2] / V2[2]).round(0))
print()
base = report(3000, (1024, 1024))
print()
print("  f     ppx   ppy   tilt  angle     L        W      L/W    pairdist  midsp  antsp  ring-ratio")
for f in (2000, 3000, 4000, 5000, 7000):
    for pp in ((1024, 1024), (1024, 1500), (1024, 700), (700, 1024), (1300, 1024)):
        o = report(f, pp, verbose=False)
        h = o["holes"]
        hm1, hm13, ha1, ha13 = h["mid_pin1side"][0], h["mid_pin13side"][0], h["ant_pin1side"][0], h["ant_pin13side"][0]
        pd = 0.5 * (ha1[0] + ha13[0]) - 0.5 * (hm1[0] + hm13[0])
        rr = np.mean([v[1][0] / v[1][1] for v in h.values()])
        print(f"{f:5d} {pp[0]:5d} {pp[1]:5d} {o['R'].tilt:6.2f} {o['ang']:7.3f} {o['L']:8.3f} {o['W']:8.3f} {o['L']/o['W']:7.4f} {pd:8.3f} {np.linalg.norm(hm13-hm1):6.3f} {np.linalg.norm(ha13-ha1):6.3f} {rr:8.4f}")
