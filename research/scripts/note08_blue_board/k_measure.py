"""Measure the oblique photo of the blue PN5180 board (kosla docs/images/pn5180.jpg, upright copy).

usage: k_measure.py UPRIGHT_PNG OUT_DEBUG_PNG

1. blue soldermask mask -> board silhouette -> 4 edge lines -> 4 corners (top copper plane)
2. blobs (pads / mounting-hole rings) after morphological opening -> centroids
3. prints everything in source pixels; a second script does the homography.
"""
import sys
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

src, dbg = sys.argv[1], sys.argv[2]
X0, Y0, X1, Y1 = 100, 1400, 2200, 3050
im = Image.open(src).convert("RGB").crop((X0, Y0, X1, Y1))
a = np.asarray(im).astype(np.float32) / 255.0
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mx = a.max(axis=2)
mn = a.min(axis=2)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
blue = (b > r * 1.25) & (b > g * 1.08) & (sat > 0.30) & (b > 0.10)

lab, n = ndi.label(blue)
sizes = ndi.sum(blue, lab, index=np.arange(1, n + 1))
board = lab == (1 + int(np.argmax(sizes)))
sil = ndi.binary_fill_holes(board)
# remove small protrusions / speckle
sil = ndi.binary_opening(sil, structure=np.ones((5, 5), bool))
lab2, n2 = ndi.label(sil)
sizes2 = ndi.sum(sil, lab2, index=np.arange(1, n2 + 1))
sil = lab2 == (1 + int(np.argmax(sizes2)))
print("silhouette area px", int(sil.sum()))

# boundary pixels
er = ndi.binary_erosion(sil)
bd = sil & ~er
by, bx = np.nonzero(bd)
bpts = np.stack([bx + X0, by + Y0], axis=1).astype(np.float64)

# approximate corners (source px) picked by eye from zoomed crops
approx = {
    "L": (222.0, 2187.0),   # header end, pin-1 side
    "B": (868.0, 2895.0),   # header end, REQ side
    "R": (2030.0, 1960.0),  # antenna end, near side
    "T": (1400.0, 1535.0),  # antenna end, far side
}
edges = {"LB_header_short": ("L", "B"), "BR_near_long": ("B", "R"),
         "RT_antenna_short": ("R", "T"), "TL_far_long": ("T", "L")}


def fit_line(points):
    """total least squares; returns (point_on_line, unit_direction, rms)."""
    c = points.mean(axis=0)
    u, s, vt = np.linalg.svd(points - c)
    d = vt[0]
    nrm = np.array([-d[1], d[0]])
    res = (points - c) @ nrm
    return c, d, nrm, res


lines = {}
for name, (p, q) in edges.items():
    P, Q = np.array(approx[p]), np.array(approx[q])
    d = (Q - P) / np.linalg.norm(Q - P)
    nrm = np.array([-d[1], d[0]])
    t = (bpts - P) @ d
    off = (bpts - P) @ nrm
    L = np.linalg.norm(Q - P)
    sel = (t > 0.08 * L) & (t < 0.92 * L) & (np.abs(off) < 25)
    pts = bpts[sel]
    for _ in range(6):  # iterative trimming
        c, dd, nn, res = fit_line(pts)
        sd = np.std(res)
        keep = np.abs(res - np.median(res)) < max(1.5, 2.0 * sd)
        if keep.all():
            break
        pts = pts[keep]
    c, dd, nn, res = fit_line(pts)
    lines[name] = (c, dd)
    print(f"edge {name}: n={len(pts)} rms={np.sqrt(np.mean(res**2)):.2f}px dir=({dd[0]:.4f},{dd[1]:.4f})")


def intersect(l1, l2):
    (c1, d1), (c2, d2) = l1, l2
    A = np.array([d1, -d2]).T
    t = np.linalg.solve(A, c2 - c1)
    return c1 + t[0] * d1


corners = {
    "L": intersect(lines["TL_far_long"], lines["LB_header_short"]),
    "B": intersect(lines["LB_header_short"], lines["BR_near_long"]),
    "R": intersect(lines["BR_near_long"], lines["RT_antenna_short"]),
    "T": intersect(lines["RT_antenna_short"], lines["TL_far_long"]),
}
for k, v in corners.items():
    print(f"corner {k}: ({v[0]:.1f}, {v[1]:.1f})")

# blobs inside the silhouette
nonblue = sil & ~board
rad = 7
yy, xx = np.mgrid[-rad:rad + 1, -rad:rad + 1]
disc = (xx * xx + yy * yy) <= rad * rad
opened = ndi.binary_opening(nonblue, structure=disc)
lab3, n3 = ndi.label(opened)
objs = ndi.find_objects(lab3)
blobs = []
for i, sl in enumerate(objs, start=1):
    m = lab3[sl] == i
    area = int(m.sum())
    if area < 900:
        continue
    cy, cx = ndi.center_of_mass(m)
    ys, xs = sl
    blobs.append({
        "area": area,
        "cx": float(cx + xs.start + X0), "cy": float(cy + ys.start + Y0),
        "x0": xs.start + X0, "x1": xs.stop + X0, "y0": ys.start + Y0, "y1": ys.stop + Y0,
    })
blobs.sort(key=lambda t: (t["cx"]))
for bl in blobs:
    print("blob area {area:6d} c=({cx:7.1f},{cy:7.1f}) bbox x[{x0},{x1}] y[{y0},{y1}] size {w}x{h}".format(
        w=bl["x1"] - bl["x0"], h=bl["y1"] - bl["y0"], **bl))

out = {"corners": {k: v.tolist() for k, v in corners.items()}, "blobs": blobs}
print("JSON", json.dumps(out))

# debug overlay
ov = im.copy()
d = ImageDraw.Draw(ov)
for k, v in corners.items():
    x, y = v[0] - X0, v[1] - Y0
    d.ellipse([x - 6, y - 6, x + 6, y + 6], outline=(255, 0, 0), width=2)
order = ["L", "B", "R", "T", "L"]
d.line([(corners[k][0] - X0, corners[k][1] - Y0) for k in order], fill=(255, 0, 0), width=1)
for bl in blobs:
    x, y = bl["cx"] - X0, bl["cy"] - Y0
    d.line([x - 8, y, x + 8, y], fill=(0, 255, 0), width=1)
    d.line([x, y - 8, x, y + 8], fill=(0, 255, 0), width=1)
ov.save(dbg)
print("saved", dbg, "window origin", (X0, Y0))
