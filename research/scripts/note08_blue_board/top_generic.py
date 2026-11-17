"""Generic measurement of a near-orthogonal top-view photo of the blue PN5180 board.

usage: top_generic.py IMAGE CONFIG [f ppx ppy]
CONFIG is one of the built-in names below (window, orientation and feature seeds per photo).
Board frame: x from the header-end short edge, y from the long edge next to pin 1 (+5V).
Scale: 2.54 mm header pitch from the soldermask gaps between the round pads.
"""
import sys
import json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

CONFIGS = {
    # easyelecmodule 3-26.png: header on the right, pin 1 at the bottom
    "e326": dict(win=(20, 220, 1560, 1130), roles=dict(HP1="BR", HP13="TR", AP1="BL", AP13="TL"),
                 padcol=dict(axis="y", lo=335, hi=1015, c0=1370, c1=1455),
                 holes=dict(mid_p13=(943, 331), mid_p1=(940, 1016), ant_p13=(207, 421), ant_p1=(209, 920)),
                 blue_thr=0.10, hole_half=60),
    # easyelecmodule 1-50.png: header on the left, pin 1 at the top
    "e150": dict(win=(5, 120, 1195, 815), roles=dict(HP1="TL", HP13="BL", AP1="TR", AP13="BR"),
                 padcol=dict(axis="y", lo=165, hi=745, c0=30, c1=100),
                 holes=dict(mid_p1=(450, 179), mid_p13=(449, 742), ant_p1=(1068, 258), ant_p13=(1066, 675)),
                 blue_thr=0.10, hole_half=50),
}

src, cfgname = sys.argv[1], sys.argv[2]
cfg = CONFIGS[cfgname]
A = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255.0
Himg, Wimg = A.shape[:2]
blueness = A[..., 2] - 0.5 * (A[..., 0] + A[..., 1])
lum = A.mean(axis=2)


def hom(p):
    return np.array([p[0], p[1], 1.0])


def line(p, q):
    return np.cross(hom(p), hom(q))


def disc(rad):
    yy, xx = np.mgrid[-rad:rad + 1, -rad:rad + 1]
    return (xx * xx + yy * yy) <= rad * rad


# ---------- outline ----------
x0, y0, x1, y1 = cfg["win"]
board = blueness[y0:y1, x0:x1] > cfg["blue_thr"]
lab, n = ndi.label(board)
sizes = ndi.sum(board, lab, index=np.arange(1, n + 1))
sil = ndi.binary_fill_holes(lab == (1 + int(np.argmax(sizes))))
ys, xs = np.nonzero(sil)
bx0, bx1, by0, by1 = xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0


def subpix_edge(profile, coords):
    p = np.asarray(profile, float)
    lo, hi = np.percentile(p, 10), np.percentile(p, 90)
    s = p - 0.5 * (lo + hi)
    idx = np.nonzero(np.sign(s[:-1]) != np.sign(s[1:]))[0]
    if len(idx) == 0:
        return np.nan
    k = idx[np.argmax(np.abs(p[idx + 1] - p[idx]))]
    t = s[k] / (s[k] - s[k + 1])
    return coords[k] + t * (coords[k + 1] - coords[k])


def edge_points(side, nsamp=70, half=12, margin=0.06):
    pts = []
    if side in ("top", "bottom"):
        yc = by0 if side == "top" else by1
        for x in np.linspace(bx0 + margin * (bx1 - bx0), bx1 - margin * (bx1 - bx0), nsamp):
            xi = int(round(x))
            yc_ = np.arange(max(1, yc - half), min(Himg - 1, yc + half + 1))
            e = subpix_edge(blueness[yc_, xi - 3:xi + 4].mean(axis=1), yc_.astype(float))
            if np.isfinite(e):
                pts.append((x, e))
    else:
        xc = bx0 if side == "left" else bx1
        for y in np.linspace(by0 + margin * (by1 - by0), by1 - margin * (by1 - by0), nsamp):
            yi = int(round(y))
            xc_ = np.arange(max(1, xc - half), min(Wimg - 1, xc + half + 1))
            e = subpix_edge(blueness[yi - 3:yi + 4, xc_].mean(axis=0), xc_.astype(float))
            if np.isfinite(e):
                pts.append((e, y))
    return np.array(pts)


def fit_line(pts):
    for _ in range(6):
        c = pts.mean(axis=0)
        _, _, vt = np.linalg.svd(pts - c)
        d = vt[0]
        res = (pts - c) @ np.array([-d[1], d[0]])
        keep = np.abs(res) < max(0.5, 2.5 * res.std())
        if keep.all():
            break
        pts = pts[keep]
    return c, d, float(np.sqrt(np.mean(res ** 2))), len(pts)


def intersect(l1, l2):
    (c1, d1), (c2, d2) = l1, l2
    t = np.linalg.solve(np.array([d1, -d2]).T, c2 - c1)
    return c1 + t[0] * d1


L_ = {}
for side in ("top", "bottom", "left", "right"):
    c, d, rms, npts = fit_line(edge_points(side))
    if (side in ("top", "bottom") and d[0] < 0) or (side in ("left", "right") and d[1] < 0):
        d = -d
    L_[side] = (c, d)
    print(f"edge {side:6s}: angle {np.degrees(np.arctan2(d[1], d[0])):8.3f} deg rms {rms:.2f}px n={npts}")
C = {"TL": intersect(L_["top"], L_["left"]), "TR": intersect(L_["top"], L_["right"]),
     "BL": intersect(L_["bottom"], L_["left"]), "BR": intersect(L_["bottom"], L_["right"])}
print("corners px:", {k: v.round(2).tolist() for k, v in C.items()})
R = {role: C[name] for role, name in cfg["roles"].items()}

# ---------- pad column ----------
pc = cfg["padcol"]
sub = blueness[pc["lo"]:pc["hi"], pc["c0"]:pc["c1"]] < 0.08
sub = ndi.binary_fill_holes(sub)
sub_o = ndi.binary_opening(sub, structure=disc(max(8, int(0.27 * (pc["hi"] - pc["lo"]) / 13 / 1.0) // 2)))
labp, npad = ndi.label(sub_o)
lands = []
for i in range(1, npad + 1):
    m = labp == i
    if m.sum() < 300:
        continue
    bd = m & ~ndi.binary_erosion(m)
    yy, xx = np.nonzero(bd)
    Am = np.c_[2 * xx, 2 * yy, np.ones_like(xx)].astype(float)
    sol, *_ = np.linalg.lstsq(Am, (xx * xx + yy * yy).astype(float), rcond=None)
    lands.append((sol[0] + pc["c0"], sol[1] + pc["lo"], np.sqrt(sol[2] + sol[0] ** 2 + sol[1] ** 2)))
lands.sort(key=lambda t: t[1])
print(f"pad lands found: {len(lands)}")
for i, (cx, cy, rr) in enumerate(lands):
    print(f"   land {i:2d}: ({cx:8.2f},{cy:8.2f}) r={rr:5.2f}")
lands_xy = np.array([(a, b) for a, b, _ in lands])
# column line through first and last land
Pa, Pb = lands_xy[0], lands_xy[-1]
dcol = (Pb - Pa) / np.linalg.norm(Pb - Pa)
P0 = Pa - 30 * dcol
Lcol = np.linalg.norm(Pb - Pa) + 60
ncol = np.array([-dcol[1], dcol[0]])
ts = np.arange(0, Lcol, 0.25)
offs = np.arange(-5, 5.1, 1.0)
T, O = np.meshgrid(ts, offs)
prof = ndi.map_coordinates(blueness, [P0[1] + T * dcol[1] + O * ncol[1], P0[0] + T * dcol[0] + O * ncol[0]], order=1).mean(axis=0)
sm = ndi.gaussian_filter1d(prof, 2.0)
thr = 0.5 * (np.percentile(sm, 95) + np.percentile(sm, 5))
labg, kg = ndi.label(sm > thr)
gaps = []
for i in range(1, kg + 1):
    idx = np.nonzero(labg == i)[0]
    w = sm[idx] - thr
    gaps.append(((ts[idx] * w).sum() / w.sum(), ts[idx[-1]] - ts[idx[0]]))
gaps = np.array(gaps)
print("blue gaps along the pad column (t, width):", np.round(gaps, 2).tolist())

# ---------- hole rings ----------
def ring_boundary(ax, ay, h):
    w = blueness[ay - h:ay + h, ax - h:ax + h] < 0.08
    w = ndi.binary_opening(w, structure=np.ones((5, 5), bool))
    lab_, _ = ndi.label(w)
    comp = ndi.binary_fill_holes(lab_ == lab_[h, h])
    bd = comp & ~ndi.binary_erosion(comp)
    yy, xx = np.nonzero(bd)
    return np.c_[xx + ax - h, yy + ay - h].astype(float)


def fit_ellipse(x, y):
    xm, ym = x.mean(), y.mean()
    xs_, ys_ = x - xm, y - ym
    D = np.stack([xs_ * xs_, xs_ * ys_, ys_ * ys_, xs_, ys_, np.ones_like(xs_)], axis=1)
    _, _, vt = np.linalg.svd(D, full_matrices=False)
    a, b_, c, d, e, f = vt[-1]
    M = np.array([[a, b_ / 2], [b_ / 2, c]])
    cen = -np.linalg.solve(2 * M, np.array([d, e]))
    val = f + 0.5 * (d * cen[0] + e * cen[1])
    w, v = np.linalg.eigh(M)
    ax = np.sqrt(np.abs(-val / w))
    return np.array([cen[0] + xm, cen[1] + ym]), np.sort(ax)[::-1]


RINGS = {k: ring_boundary(v[0], v[1], cfg["hole_half"]) for k, v in cfg["holes"].items()}

# ---------- rectification ----------
V1 = np.cross(line(C["TL"], C["TR"]), line(C["BL"], C["BR"]))
V2 = np.cross(line(C["TL"], C["BL"]), line(C["TR"], C["BR"]))
VL = np.cross(V1, V2); VL = VL / np.linalg.norm(VL[:2])
print("vanishing points:", (V1[:2] / V1[2]).round(0).tolist(), (V2[:2] / V2[2]).round(0).tolist())


class Rect:
    def __init__(self, f, pp, gap_sel):
        K = np.array([[f, 0, pp[0]], [0, f, pp[1]], [0, 0, 1.0]])
        self.Kinv = np.linalg.inv(K)
        nrm = K.T @ VL
        self.n = nrm / np.linalg.norm(nrm)
        self.tilt = np.degrees(np.arccos(abs(self.n[2])))
        O = self.back(R["HP1"]); Xa = self.back(R["AP1"])
        e1 = Xa - O; e1 /= np.linalg.norm(e1)
        e2 = np.cross(self.n, e1); e2 /= np.linalg.norm(e2)
        if np.dot(self.back(R["HP13"]) - O, e2) < 0:
            e2 = -e2
        self.O, self.e1, self.e2 = O, e1, e2
        g = np.array([self.raw(P0 + t * dcol) for t in gap_sel])
        s = np.r_[0, np.cumsum(np.hypot(*np.diff(g, axis=0).T))]
        self.scale = 2.54 / np.polyfit(np.arange(len(s)), s, 1)[0]

    def back(self, p):
        d = self.Kinv @ hom(p)
        return d / np.dot(self.n, d)

    def raw(self, p):
        X = self.back(p) - self.O
        return np.array([np.dot(X, self.e1), np.dot(X, self.e2)])

    def mm(self, p):
        return self.raw(p) * self.scale


# gaps between round pads only: drop the first/last blue segments (board margin) and the gap next to the square pad 1
g_all = gaps[:, 0]
sp = np.diff(g_all)
med = np.median(sp)
runs = [i for i in range(len(sp)) if abs(sp[i] - med) < 0.08 * med]
sel = sorted(set(runs) | {i + 1 for i in runs})
gap_sel = g_all[sel]
print(f"using {len(gap_sel)} gaps, median spacing {med:.2f}px, regression pitch {np.polyfit(np.arange(len(gap_sel)), gap_sel, 1)[0]:.3f}px")


def report(f, pp, verbose=True):
    Rr = Rect(f, pp, gap_sel)
    c = {k: Rr.mm(v) for k, v in R.items()}
    Lp1 = np.linalg.norm(c["AP1"] - c["HP1"]); Lp13 = np.linalg.norm(c["AP13"] - c["HP13"])
    Wh = np.linalg.norm(c["HP13"] - c["HP1"]); Wa = np.linalg.norm(c["AP13"] - c["AP1"])
    v1 = c["AP1"] - c["HP1"]; v2 = c["HP13"] - c["HP1"]
    ang = np.degrees(np.arccos(np.dot(v1, v2) / np.linalg.norm(v1) / np.linalg.norm(v2)))
    L, W = 0.5 * (Lp1 + Lp13), 0.5 * (Wh + Wa)
    pads = np.array([Rr.mm(p) for p in lands_xy])
    if pads[0, 1] > pads[-1, 1]:
        pads = pads[::-1]  # pin 1 first
    holes = {}
    for k, pts in RINGS.items():
        q = np.array([Rr.mm(p) for p in pts[::2]])
        holes[k] = fit_ellipse(q[:, 0], q[:, 1])
    hm1, hm13, ha1, ha13 = holes["mid_p1"][0], holes["mid_p13"][0], holes["ant_p1"][0], holes["ant_p13"][0]
    xm, xa = 0.5 * (hm1[0] + hm13[0]), 0.5 * (ha1[0] + ha13[0])
    o = dict(L=L, W=W, ang=ang, tilt=Rr.tilt, pads=pads, holes=holes, xm=xm, xa=xa,
             midsp=np.linalg.norm(hm13 - hm1), antsp=np.linalg.norm(ha13 - ha1), Rr=Rr)
    if verbose:
        print(f"f={f:.0f} pp=({pp[0]:.0f},{pp[1]:.0f}) tilt {Rr.tilt:.2f} deg, corner angle {ang:.3f} deg, {1/Rr.scale*1:.4f} plane-units/mm")
        print(f"  LENGTH {L:.3f} (pin-1 edge {Lp1:.3f}, pin-13 edge {Lp13:.3f})  WIDTH {W:.3f} (header end {Wh:.3f}, antenna end {Wa:.3f})  L/W {L/W:.4f}")
        print(f"  pad row x: mean {pads[:,0].mean():.3f} (pin1 {pads[0,0]:.3f}, pin13 {pads[-1,0]:.3f}); pin1 y {pads[0,1]:.3f}; pin13 y {pads[-1,1]:.3f} -> to pin-13 edge {W - pads[-1,1]:.3f}; span {np.linalg.norm(pads[-1]-pads[0]):.3f}; n={len(pads)}")
        for k, (cen, axes) in holes.items():
            print(f"  hole {k:8s}: x={cen[0]:7.3f} y={cen[1]:7.3f}  ring outer dia {2*axes[0]:.3f} x {2*axes[1]:.3f}")
        print(f"  mid pair: x {xm:.3f}, spacing {o['midsp']:.3f}, to edges p1 {hm1[1]:.3f} / p13 {W - hm13[1]:.3f}")
        print(f"  ant pair: x {xa:.3f} (to antenna-end edge {L - xa:.3f}), spacing {o['antsp']:.3f}, to edges p1 {ha1[1]:.3f} / p13 {W - ha13[1]:.3f}")
        print(f"  pair distance {xa - xm:.3f};  L/pairdist {L/(xa-xm):.4f};  W/midspacing {W/o['midsp']:.4f}")
    return o


if len(sys.argv) > 5:
    report(float(sys.argv[3]), (float(sys.argv[4]), float(sys.argv[5])))
else:
    report(3000 * Wimg / 2048, (Wimg / 2, Himg / 2))
    print("  f      pp            tilt   angle     L       W      pairdist")
    for fm in (2000, 3000, 5000):
        f = fm * Wimg / 2048
        for pp in ((0.5, 0.5), (0.5, 0.2), (0.5, 0.8), (0.2, 0.5), (0.8, 0.5)):
            p = (pp[0] * Wimg, pp[1] * Himg)
            o = report(f, p, verbose=False)
            print(f"{f:6.0f} ({p[0]:5.0f},{p[1]:5.0f}) {o['tilt']:6.2f} {o['ang']:8.3f} {o['L']:8.3f} {o['W']:7.3f} {o['xa']-o['xm']:8.3f}")
