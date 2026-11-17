"""Edge list across the antenna legs from a metric-rectified board image (20 px/mm, 2 mm margin).

usage: ant_edges.py RECT_NPY
For each cut the luminance profile (restricted to the board interior) is smoothed and its
significant gradient extrema are listed: '+' = dark->light going outward-to-inward along the
axis direction, '-' = light->dark. Light = copper under soldermask.
"""
import sys
import numpy as np
from scipy import ndimage as ndi

rect = np.load(sys.argv[1])
PPM, M = 20.0, 2.0
lum = rect.mean(axis=2)
H, Wd = lum.shape
Lmm, Wmm = Wd / PPM - 2 * M, H / PPM - 2 * M


def ix(mm):
    return int(round((mm + M) * PPM))


def edges(profile, coords, name, sm=0.8, rel=0.30):
    p = ndi.gaussian_filter1d(profile, sm)
    g = np.gradient(p)
    thr = rel * np.percentile(np.abs(g), 98)
    out = []
    for i in range(1, len(g) - 1):
        if abs(g[i]) > thr and abs(g[i]) >= abs(g[i - 1]) and abs(g[i]) >= abs(g[i + 1]):
            # sub-sample refinement by parabola
            den = (abs(g[i - 1]) - 2 * abs(g[i]) + abs(g[i + 1]))
            off = 0.5 * (abs(g[i - 1]) - abs(g[i + 1])) / den if den != 0 else 0.0
            out.append((coords[i] + off * (coords[1] - coords[0]), "+" if g[i] > 0 else "-", abs(g[i])))
    print(name)
    print("    " + "  ".join(f"{s}{x:.2f}" for x, s, a in out))
    # light bands = '+' edge followed by '-' edge
    bands = []
    for (xa, sa, _), (xb, sb, _) in zip(out[:-1], out[1:]):
        if sa == "+" and sb == "-":
            bands.append((xa, xb))
    print("    light bands: " + ", ".join(f"[{a:.2f},{b:.2f}] w={b-a:.2f}" for a, b in bands))
    return out, bands


xs = np.arange(Wd) / PPM - M
ys = np.arange(H) / PPM - M
print(f"board {Lmm:.2f} x {Wmm:.2f}")
res = {}
for (ya, yb) in ((24.0, 27.0), (27.0, 30.0), (11.0, 13.0)):
    row = lum[ix(ya):ix(yb), :].mean(axis=0)
    sel = (xs > 26.8) & (xs < 33.5)
    res[("hdr", ya)] = edges(row[sel], xs[sel], f"cut y={ya}..{yb}: header-side leg, x 26.8..33.5")
    sel = (xs > 64.0) & (xs < Lmm - 0.25)
    res[("far", ya)] = edges(row[sel], xs[sel], f"cut y={ya}..{yb}: far-end leg, x 64..{Lmm-0.25:.2f}")
for (xa, xb) in ((35.0, 38.0), (41.0, 44.0), (57.0, 60.0)):
    col = lum[:, ix(xa):ix(xb)].mean(axis=1)
    sel = (ys > 0.25) & (ys < 5.5)
    res[("p1", xa)] = edges(col[sel], ys[sel], f"cut x={xa}..{xb}: pin-1-side leg, y 0.25..5.5")
    sel = (ys > 33.0) & (ys < Wmm - 0.25)
    res[("p13", xa)] = edges(col[sel], ys[sel], f"cut x={xa}..{xb}: pin-13-side leg, y 33..{Wmm-0.25:.2f}")
