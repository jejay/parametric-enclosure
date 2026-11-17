"""Header pad centres in the top-view photo: two independent estimators per pad.
 (a) bore = white see-through hole -> circle fit to its boundary
 (b) pad  = outer boundary of the silver land (non-blue blob, silkscreen removed by opening) -> circle fit
usage: e_pads.py IMAGE OUT_MASK_PNG
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

A = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32) / 255.0
r, g, b = A[..., 0], A[..., 1], A[..., 2]
lum = A.mean(axis=2)
mx = A.max(axis=2); mn = A.min(axis=2)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
blueness = b - 0.5 * (r + g)


def disc(rad):
    yy, xx = np.mgrid[-rad:rad + 1, -rad:rad + 1]
    return (xx * xx + yy * yy) <= rad * rad


def circle_fit(x, y):
    Am = np.c_[2 * x, 2 * y, np.ones_like(x)]
    sol, *_ = np.linalg.lstsq(Am, x * x + y * y, rcond=None)
    cx, cy = sol[0], sol[1]
    rad = np.sqrt(sol[2] + cx * cx + cy * cy)
    res = np.hypot(x - cx, y - cy) - rad
    return cx, cy, rad, float(np.sqrt(np.mean(res ** 2)))


X0, X1, Y0, Y1 = 1370, 1455, 335, 1015
sub_l = lum[Y0:Y1, X0:X1]; sub_s = sat[Y0:Y1, X0:X1]; sub_b = blueness[Y0:Y1, X0:X1]
bore = (sub_l > 0.80) & (sub_s < 0.10)
bore = ndi.binary_opening(bore, structure=disc(4))
land = sub_b < 0.08
land = ndi.binary_fill_holes(land)
land_o = ndi.binary_opening(land, structure=disc(14))
Image.fromarray(np.concatenate([bore, land, land_o], axis=1).astype(np.uint8) * 255).save(sys.argv[2])

# seeds: 13 pads between y=366 and y=983 (found earlier), x about 1410
seeds = [(1413.5 - 7.0 * k / 12, 366.2 + (982.0 - 366.2) * k / 12) for k in range(13)]
labb, _ = ndi.label(bore)
labl, _ = ndi.label(land_o)
print("idx  seed_y   bore(cx,cy,r,rms)                 land(cx,cy,r,rms)")
rows = []
for k, (sx, sy) in enumerate(seeds):
    ix, iy = int(round(sx - X0)), int(round(sy - Y0))
    out = []
    for lab in (labb, labl):
        li = lab[iy, ix]
        if li == 0:
            w = lab[max(0, iy - 8):iy + 9, max(0, ix - 8):ix + 9]
            vals = w[w > 0]
            li = np.bincount(vals).argmax() if len(vals) else 0
        if li == 0:
            out.append((np.nan,) * 4)
            continue
        comp = lab == li
        bd = comp & ~ndi.binary_erosion(comp)
        yy, xx = np.nonzero(bd)
        cx, cy, rad, rms = circle_fit(xx.astype(float), yy.astype(float))
        out.append((cx + X0, cy + Y0, rad, rms))
    rows.append(out)
    (bx, by, br, brms), (lx, ly, lr, lrms) = out
    print(f"{k:2d}  {sy:7.1f}  ({bx:8.2f},{by:8.2f}) r={br:5.2f} rms={brms:4.2f}   ({lx:8.2f},{ly:8.2f}) r={lr:5.2f} rms={lrms:4.2f}")
bys = np.array([r_[0][1] for r_ in rows]); lys = np.array([r_[1][1] for r_ in rows])
print("bore pitches:", np.round(np.diff(bys), 2).tolist(), "mean", round(float(np.diff(bys).mean()), 3))
print("land pitches:", np.round(np.diff(lys), 2).tolist(), "mean", round(float(np.diff(lys).mean()), 3))
print("PADS_BORE =", [(round(float(r_[0][0]), 2), round(float(r_[0][1]), 2)) for r_ in rows])
print("PADS_LAND =", [(round(float(r_[1][0]), 2), round(float(r_[1][1]), 2)) for r_ in rows])
