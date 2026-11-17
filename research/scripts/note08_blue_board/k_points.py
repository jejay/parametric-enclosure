"""Refined feature centres in the oblique board photo: mounting-hole rings and header pads.

usage: k_points.py UPRIGHT_PNG OUT_DEBUG_PNG
For each feature a window is segmented (not-soldermask-blue), opened to drop thin silkscreen,
the component nearest the window centre is filled and an ellipse is fitted to its boundary.
Prints centre (source px), semi-axes and angle.
"""
import sys
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

src, dbg = sys.argv[1], sys.argv[2]
full = Image.open(src).convert("RGB")
A = np.asarray(full).astype(np.float32) / 255.0


def nonblue_mask(win):
    x0, y0, x1, y1 = win
    a = A[y0:y1, x0:x1]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(axis=2); mn = a.min(axis=2)
    sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
    blue = (b > r * 1.25) & (b > g * 1.08) & (sat > 0.30) & (b > 0.10)
    return ~blue


def disc(rad):
    yy, xx = np.mgrid[-rad:rad + 1, -rad:rad + 1]
    return (xx * xx + yy * yy) <= rad * rad


def fit_ellipse(x, y):
    """Direct least squares conic fit; returns centre, semi-axes, angle(deg)."""
    xm, ym = x.mean(), y.mean()
    xs, ys = x - xm, y - ym
    D = np.stack([xs * xs, xs * ys, ys * ys, xs, ys, np.ones_like(xs)], axis=1)
    _, _, vt = np.linalg.svd(D, full_matrices=False)
    a, b, c, d, e, f = vt[-1]
    M = np.array([[a, b / 2], [b / 2, c]])
    cen = -np.linalg.solve(2 * M, np.array([d, e]))
    val = f + 0.5 * (d * cen[0] + e * cen[1])
    w, v = np.linalg.eigh(M)
    ax = np.sqrt(np.abs(-val / w))
    order = np.argsort(-ax)
    ang = np.degrees(np.arctan2(v[1, order[0]], v[0, order[0]]))
    return np.array([cen[0] + xm, cen[1] + ym]), ax[order], ang


def feature(name, cx, cy, half, open_rad):
    win = (int(cx - half), int(cy - half), int(cx + half), int(cy + half))
    m = nonblue_mask(win)
    if open_rad:
        m = ndi.binary_opening(m, structure=disc(open_rad))
    lab, n = ndi.label(m)
    if n == 0:
        print(name, "nothing found")
        return None
    # component containing / nearest to window centre
    best, bestd = None, 1e9
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 300:
            continue
        dmin = np.min((xs - half) ** 2 + (ys - half) ** 2)
        if dmin < bestd:
            best, bestd = i, dmin
    comp = ndi.binary_fill_holes(lab == best)
    touches = comp[0].any() or comp[-1].any() or comp[:, 0].any() or comp[:, -1].any()
    cyc, cxc = ndi.center_of_mass(comp)
    bd = comp & ~ndi.binary_erosion(comp)
    by, bx = np.nonzero(bd)
    cen, ax, ang = fit_ellipse(bx.astype(float), by.astype(float))
    res_c = (cxc + win[0], cyc + win[1])
    res_e = (cen[0] + win[0], cen[1] + win[1])
    print(f"{name:10s} centroid ({res_c[0]:7.1f},{res_c[1]:7.1f}) ellipse c ({res_e[0]:7.1f},{res_e[1]:7.1f}) "
          f"semi-axes {ax[0]:5.1f} x {ax[1]:5.1f} ang {ang:6.1f} area {int(comp.sum())} touches_window={bool(touches)}")
    return {"name": name, "centroid": res_c, "ellipse": res_e, "axes": ax.tolist(), "ang": float(ang),
            "touch": bool(touches), "bd": (bx + win[0], by + win[1])}


feats = []
# mounting holes: approx centres from earlier blob list / zoomed crops
for name, cx, cy, half, orad in [
    ("H_mid_far", 775, 1933, 70, 3),
    ("H_ant_far", 1418, 1655, 60, 3),
    ("H_ant_near", 1830, 1948, 70, 3),
    ("H_mid_near", 1353, 2446, 62, 5),
]:
    feats.append(feature(name, cx, cy, half, orad))

# header pads: start from pads 1 and 8 found earlier and extrapolate, then refine
p1 = np.array([331.5, 2223.5]); p8 = np.array([620.0, 2529.0])
for k in range(13):
    # projective spacing is not uniform; use the earlier blob list for 1..8 and a guess beyond
    guess = p1 + (p8 - p1) * (k / 7.0) * (1 + 0.012 * k)
    feats.append(feature(f"PAD{k+1}", guess[0], guess[1], 46, 9))

ov = full.copy()
d = ImageDraw.Draw(ov)
out = []
for f in feats:
    if not f:
        continue
    bx, by = f["bd"]
    for x, y in zip(bx[::2], by[::2]):
        ov.putpixel((int(x), int(y)), (255, 0, 0))
    x, y = f["ellipse"]
    d.line([x - 10, y, x + 10, y], fill=(0, 255, 0), width=1)
    d.line([x, y - 10, x, y + 10], fill=(0, 255, 0), width=1)
    out.append({k: f[k] for k in ("name", "centroid", "ellipse", "axes", "ang", "touch")})
ov.crop((100, 1400, 2200, 3050)).save(dbg)
print("JSON", json.dumps(out))
