"""Lateral overhang of a figure over its puck base in an arbitrary view.

Usage: python -I overhang_view.py IMG "x0,y0,x1,y1" SEED_X PUCK_Y0:PUCK_Y1 [BASE_MM] [--exclude-yellow]

Inside the box, the puck's left/right silhouette is taken from the dark run through SEED_X (constant
band in PUCK rows); the figure is every opaque, clearly coloured or bright pixel above the puck rows.
Reports how far the figure reaches beyond the vertical lines through the puck's silhouette edges
(positive = overhang), in px and in mm (scale = puck width / BASE_MM).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import mcommon as mc
from rowruns import run_extent


def main():
    path = sys.argv[1]
    x0, y0, x1, y1 = (int(v) for v in sys.argv[2].split(","))
    seed = int(sys.argv[3])
    py0, py1 = (int(v) for v in sys.argv[4].split(":"))
    base = float(sys.argv[5]) if len(sys.argv) > 5 and not sys.argv[5].startswith("--") else 45.0
    a = mc.load_rgba(path)
    r, g, b, al, sat, lum = mc.channels(a)
    rows = []
    for y in range(py0, py1 + 1):
        e = run_extent(lum, sat, al, y, seed, level=150.0, maxsat=0.3)
        if e is not None:
            rows.append((y, e[0], e[1]))
    rows = np.array(rows)
    wd = rows[:, 2] - rows[:, 1]
    sel = wd > wd.max() - 1.5
    xl, xr = float(np.median(rows[sel, 1])), float(np.median(rows[sel, 2]))
    W = xr - xl
    s = W / base
    fig = (al >= 250) & ((sat > 0.22) | (lum > 150))
    if "--exclude-yellow" in sys.argv:
        yellow = (r > 180) & (g > 150) & (b < 110)
        fig &= ~yellow
    sub = np.zeros_like(fig)
    sub[y0:py0, x0:x1] = fig[y0:py0, x0:x1]
    ys, xs = np.nonzero(sub)
    fl, fr = float(xs.min()), float(xs.max()) + 1.0
    ytop = int(ys.min())
    print(f"{os.path.basename(path)} box={sys.argv[2]} puck x {xl:.1f}..{xr:.1f} (W={W:.1f} px, {s:.3f} px/mm) "
          f"figure x {fl:.0f}..{fr:.0f} top y {ytop} | left beyond {(xl - fl) / s:+.2f} mm, right beyond {(fr - xr) / s:+.2f} mm, "
          f"figure width {(fr - fl) / s:.1f} mm")


if __name__ == "__main__":
    main()
