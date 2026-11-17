"""Antenna trace positions from a metric-rectified board image (20 px/mm, 2 mm margin).

usage: ant_profiles.py RECT_NPY
Prints, for four cuts across the loop, the positions (mm, board frame) of the copper traces
(lighter under soldermask) found as bands above the local mid level, and the silk dot centre.
"""
import sys
import numpy as np
from scipy import ndimage as ndi

rect = np.load(sys.argv[1])
PPM, M = 20.0, 2.0
lum = rect.mean(axis=2)
blue = rect[..., 2] - 0.5 * (rect[..., 0] + rect[..., 1])


def ix(mm):
    return int(round((mm + M) * PPM))


def bands(profile, coords, name, smooth=1.0, minw=0.12):
    p = ndi.gaussian_filter1d(profile, smooth)
    # remove slow illumination trend
    trend = ndi.gaussian_filter1d(p, 40)
    d = p - trend
    thr = 0.0
    lab, k = ndi.label(d > thr + 0.25 * d.std())
    out = []
    for i in range(1, k + 1):
        idx = np.nonzero(lab == i)[0]
        w = coords[idx[-1]] - coords[idx[0]]
        if w >= minw:
            out.append((coords[idx[0]], coords[idx[-1]], w, float(d[idx].mean())))
    print(f"{name}:")
    for a, b, w, amp in out:
        print(f"    light band {a:7.2f} .. {b:7.2f} mm  width {w:5.2f}  contrast {amp:+.3f}")
    return out


H, Wd = lum.shape
Lmm, Wmm = Wd / PPM - 2 * M, H / PPM - 2 * M
print(f"rectified image covers x 0..{Lmm:.2f}, y 0..{Wmm:.2f}")
# horizontal cuts (vary x) averaged over y bands that avoid silk arcs / notch
for (ya, yb) in ((8.0, 11.0), (27.0, 30.0)):
    rows = lum[ix(ya):ix(yb), :].mean(axis=0)
    xs = np.arange(Wd) / PPM - M
    sel = (xs > 26.5) & (xs < 34.5)
    bands(rows[sel], xs[sel], f"cut y={ya}-{yb}, header-side leg of the loop (x 26.5..34.5)")
    sel = (xs > 63.5) & (xs < Lmm + 0.5)
    bands(rows[sel], xs[sel], f"cut y={ya}-{yb}, far-end leg of the loop (x 63.5..end)")
# vertical cuts (vary y) averaged over x bands
for (xa, xb) in ((35.0, 38.0), (57.0, 60.0)):
    cols = lum[:, ix(xa):ix(xb)].mean(axis=1)
    ys = np.arange(H) / PPM - M
    sel = (ys > -0.5) & (ys < 6.0)
    bands(cols[sel], ys[sel], f"cut x={xa}-{xb}, pin-1-side leg (y -0.5..6)")
    sel = (ys > 32.5) & (ys < Wmm + 0.5)
    bands(cols[sel], ys[sel], f"cut x={xa}-{xb}, pin-13-side leg (y 32.5..end)")

# silk dot: small white ring near (48, 19.3)
x0, x1, y0, y1 = 45.0, 51.0, 16.5, 22.0
sub = rect[ix(y0):ix(y1), ix(x0):ix(x1)]
white = (sub.min(axis=2) > 0.75)
lab, k = ndi.label(white)
best = None
for i in range(1, k + 1):
    m = lab == i
    cy, cx = ndi.center_of_mass(ndi.binary_fill_holes(m))
    a = m.sum()
    yy, xx = np.nonzero(m)
    wmm = (xx.max() - xx.min() + 1) / PPM; hmm = (yy.max() - yy.min() + 1) / PPM
    print(f"  white blob: centre x={cx/PPM + x0:.2f} y={cy/PPM + y0:.2f} size {wmm:.2f} x {hmm:.2f} mm area {a}")
