"""Measure the orthogonal top-view product photo (easyelecmodule 3-26.png) of the blue PN5180 board.

usage: e_measure.py IMAGE OUT_DEBUG_PNG
Outputs (source px): board edge lines (sub-pixel), corners, edge lengths, angles; header pad
centres; mounting-hole ring centres/diameters and bore diameters.
"""
import sys
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

src, dbg = sys.argv[1], sys.argv[2]
full = Image.open(src).convert("RGB")
A = np.asarray(full).astype(np.float32) / 255.0
r, g, b = A[..., 0], A[..., 1], A[..., 2]
mx = A.max(axis=2); mn = A.min(axis=2)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
lum = A.mean(axis=2)
blueness = b - 0.5 * (r + g)

# --- board silhouette: everything that is not near-white background, in the board window ---
WIN = (20, 220, 1560, 1130)  # x0,y0,x1,y1 containing the board only
x0, y0, x1, y1 = WIN
sub_blue = blueness[y0:y1, x0:x1]
board = sub_blue > 0.10
lab, n = ndi.label(board)
sizes = ndi.sum(board, lab, index=np.arange(1, n + 1))
board = lab == (1 + int(np.argmax(sizes)))
sil = ndi.binary_fill_holes(board)
ys, xs = np.nonzero(sil)
print("silhouette bbox px: x[%d,%d] y[%d,%d]" % (xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0))
bx0, bx1, by0, by1 = xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0


def subpix_edge(profile, coords, level=None):
    """position where a monotone-ish profile crosses the half level between its two plateaus."""
    p = np.asarray(profile, float)
    lo, hi = np.percentile(p, 10), np.percentile(p, 90)
    lvl = 0.5 * (lo + hi) if level is None else level
    s = p - lvl
    idx = np.nonzero(np.sign(s[:-1]) != np.sign(s[1:]))[0]
    if len(idx) == 0:
        return np.nan
    # take crossing with the steepest slope
    k = idx[np.argmax(np.abs(p[idx + 1] - p[idx]))]
    t = s[k] / (s[k] - s[k + 1])
    return coords[k] + t * (coords[k + 1] - coords[k])


def edge_points(side, nsamp=60, half=14, margin=0.07):
    pts = []
    if side in ("top", "bottom"):
        yc = by0 if side == "top" else by1
        xa, xb = bx0 + margin * (bx1 - bx0), bx1 - margin * (bx1 - bx0)
        for x in np.linspace(xa, xb, nsamp):
            xi = int(round(x))
            ycoords = np.arange(yc - half, yc + half + 1)
            prof = blueness[ycoords, xi - 3:xi + 4].mean(axis=1)
            e = subpix_edge(prof, ycoords.astype(float))
            if np.isfinite(e):
                pts.append((x, e))
    else:
        xc = bx0 if side == "left" else bx1
        ya, yb = by0 + margin * (by1 - by0), by1 - margin * (by1 - by0)
        for y in np.linspace(ya, yb, nsamp):
            yi = int(round(y))
            xcoords = np.arange(xc - half, xc + half + 1)
            prof = blueness[yi - 3:yi + 4, xcoords].mean(axis=0)
            e = subpix_edge(prof, xcoords.astype(float))
            if np.isfinite(e):
                pts.append((e, y))
    return np.array(pts)


def fit_line(pts):
    for _ in range(5):
        c = pts.mean(axis=0)
        _, _, vt = np.linalg.svd(pts - c)
        d = vt[0]
        nrm = np.array([-d[1], d[0]])
        res = (pts - c) @ nrm
        keep = np.abs(res) < max(0.6, 2.5 * res.std())
        if keep.all():
            break
        pts = pts[keep]
    return c, d, float(np.sqrt(np.mean(res ** 2))), len(pts)


def intersect(l1, l2):
    (c1, d1), (c2, d2) = l1, l2
    t = np.linalg.solve(np.array([d1, -d2]).T, c2 - c1)
    return c1 + t[0] * d1


lines = {}
for side in ("top", "bottom", "left", "right"):
    pts = edge_points(side)
    c, d, rms, npts = fit_line(pts)
    if d[0] < 0 and side in ("top", "bottom"):
        d = -d
    if d[1] < 0 and side in ("left", "right"):
        d = -d
    lines[side] = (c, d)
    ang = np.degrees(np.arctan2(d[1], d[0]))
    print(f"edge {side:6s}: through ({c[0]:8.2f},{c[1]:8.2f}) angle {ang:8.3f} deg rms {rms:.2f}px n={npts}")

TL = intersect(lines["top"], lines["left"]); TR = intersect(lines["top"], lines["right"])
BL = intersect(lines["bottom"], lines["left"]); BR = intersect(lines["bottom"], lines["right"])
corners = {"TL": TL, "TR": TR, "BL": BL, "BR": BR}
for k, v in corners.items():
    print(f"corner {k}: ({v[0]:8.2f},{v[1]:8.2f})")
Lt, Lb = np.linalg.norm(TR - TL), np.linalg.norm(BR - BL)
Wl, Wr = np.linalg.norm(BL - TL), np.linalg.norm(BR - TR)
print(f"length top {Lt:.2f}px bottom {Lb:.2f}px ; width left {Wl:.2f}px right {Wr:.2f}px ; ratio {0.5*(Lt+Lb)/(0.5*(Wl+Wr)):.4f}")

# --- header pads: bright low-saturation blobs in the header column ---
hx0, hx1 = int(bx1 - 110), int(bx1 - 8)
hy0, hy1 = int(by0 + 20), int(by1 - 20)
sub = A[hy0:hy1, hx0:hx1]
sb = blueness[hy0:hy1, hx0:hx1]
notblue = sb < 0.08
notblue = ndi.binary_fill_holes(notblue)
dt = ndi.distance_transform_edt(notblue)
dts = ndi.gaussian_filter(dt, 1.5)
mxf = ndi.maximum_filter(dts, size=35)
peaks = np.argwhere((dts == mxf) & (dts > 12))
pads = []
for py, px in peaks:
    core = dt >= 0.55 * dt[py, px]
    labc, _ = ndi.label(core)
    m = labc == labc[py, px]
    cy, cx = ndi.center_of_mass(m)
    pads.append((cx + hx0, cy + hy0, dt[py, px]))
pads.sort(key=lambda t: t[1])
print("pads found:", len(pads))
for i, (cx, cy, rad) in enumerate(pads):
    print(f"  pad idx {i:2d}: ({cx:8.2f},{cy:8.2f}) inscribed r {rad:.1f}px")

# --- mounting holes: non-blue blobs near the expected places ---
holes = []
nb_full = (blueness < 0.08)
for name, (ax, ay) in {"mid_top": (940, 330), "mid_bottom": (940, 1015), "ant_top": (207, 420), "ant_bottom": (207, 920)}.items():
    h = 75
    w = nb_full[ay - h:ay + h, ax - h:ax + h]
    w = ndi.binary_opening(w, structure=np.ones((5, 5), bool))
    labh, nh = ndi.label(w)
    li = labh[h, h]
    if li == 0:
        # nearest component
        d2 = ndi.distance_transform_edt(labh == 0, return_indices=True)
        iy, ix = d2[1][0][h, h], d2[1][1][h, h]
        li = labh[iy, ix]
    comp = ndi.binary_fill_holes(labh == li)
    area = comp.sum()
    cy, cx = ndi.center_of_mass(comp)
    yy, xx = np.nonzero(comp)
    wpx, hpx = xx.max() - xx.min() + 1, yy.max() - yy.min() + 1
    # bore: bright (near white) region inside
    lw = lum[ay - h:ay + h, ax - h:ax + h]
    sw = sat[ay - h:ay + h, ax - h:ax + h]
    bore = comp & (lw > 0.86) & (sw < 0.10)
    bore = ndi.binary_opening(bore, structure=np.ones((3, 3), bool))
    labb, nb = ndi.label(bore)
    if nb:
        sz = ndi.sum(bore, labb, index=np.arange(1, nb + 1))
        bore = labb == (1 + int(np.argmax(sz)))
    bcy, bcx = ndi.center_of_mass(bore) if bore.any() else (np.nan, np.nan)
    holes.append({"name": name, "cx": cx + ax - h, "cy": cy + ay - h, "ring_d_eq": 2 * np.sqrt(area / np.pi),
                  "ring_w": int(wpx), "ring_h": int(hpx), "bore_d_eq": 2 * np.sqrt(bore.sum() / np.pi),
                  "bore_cx": bcx + ax - h, "bore_cy": bcy + ay - h})
for hinfo in holes:
    print("hole {name:10s}: ring centre ({cx:8.2f},{cy:8.2f}) ring d_eq {ring_d_eq:6.2f}px (bbox {ring_w}x{ring_h}) "
          "bore d_eq {bore_d_eq:6.2f}px centre ({bore_cx:8.2f},{bore_cy:8.2f})".format(**hinfo))

out = {"corners": {k: v.tolist() for k, v in corners.items()},
       "pads": [(float(a), float(b_)) for a, b_, _ in pads],
       "holes": [{k: (float(v) if not isinstance(v, str) else v) for k, v in h.items()} for h in holes]}
print("JSON", json.dumps(out))

ov = full.copy()
d = ImageDraw.Draw(ov)
d.line([tuple(TL), tuple(TR), tuple(BR), tuple(BL), tuple(TL)], fill=(255, 0, 0), width=1)
for cx, cy, _ in pads:
    d.line([cx - 9, cy, cx + 9, cy], fill=(0, 255, 0)); d.line([cx, cy - 9, cx, cy + 9], fill=(0, 255, 0))
for hinfo in holes:
    cx, cy = hinfo["cx"], hinfo["cy"]
    d.line([cx - 12, cy, cx + 12, cy], fill=(255, 0, 255)); d.line([cx, cy - 12, cx, cy + 12], fill=(255, 0, 255))
ov.crop((0, 180, 1700, 1330)).save(dbg)
