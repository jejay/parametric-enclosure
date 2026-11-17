"""Compare the x-extent of a coloured figure with the x-extent of its black puck inside a box.

Usage: python -I bbox_overhang.py IMG NAME "x0,y0,x1,y1" [BASE_MM] [--no-yellow]
Puck = opaque pixels darker than 80 (max channel); figure = opaque pixels with saturation > 0.3
(or bright unsaturated ones), optionally without yellow. Positive overhang = figure beyond puck edge.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import mcommon as mc

path, name = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = (int(v) for v in sys.argv[3].split(","))
base = float(sys.argv[4]) if len(sys.argv) > 4 and not sys.argv[4].startswith("--") else 45.0
a = mc.load_rgba(path)
r, g, b, al, sat, lum = mc.channels(a)
val = np.maximum(np.maximum(r, g), b)
sub = np.zeros(al.shape, bool); sub[y0:y1, x0:x1] = True
opaque = al >= 250
dark = sub & opaque & (val < 80)
# keep only rows where the dark run is long (puck body), to drop pupils / claws
rowlen = dark.sum(axis=1)
rows = np.nonzero(rowlen > 0.5 * rowlen.max())[0]
pm = np.zeros_like(dark); pm[rows.min():rows.max() + 1] = dark[rows.min():rows.max() + 1]
ys, xs = np.nonzero(pm)
pl, pr = xs.min(), xs.max() + 1
fig = sub & opaque & ((sat > 0.30) & (val > 90))
if "--hue" in sys.argv:
    hue = sys.argv[sys.argv.index("--hue") + 1]
    if hue == "blue":
        fig = sub & opaque & (b > r + 25) & (val > 90)
    elif hue == "teal":
        fig = sub & opaque & (g > r + 20) & (b > r + 5) & (val > 90)
    elif hue == "orange":
        fig = sub & opaque & (r > 200) & (g > 90) & (g < 175) & (b < 90)
if "--no-yellow" in sys.argv:
    fig &= ~((r > 170) & (g > 140) & (b < 120))
fig[rows.min():, :] = False          # only what is above the puck's body rows
fy, fx = np.nonzero(fig)
fl, fr = fx.min(), fx.max() + 1
s = (pr - pl) / base
print(f"{os.path.basename(path)} {name}: puck x {pl}..{pr} ({pr - pl} px, {s:.2f} px/mm) figure x {fl}..{fr} top y {fy.min()} | "
      f"left beyond {(pl - fl) / s:+.1f} mm, right beyond {(fr - pr) / s:+.1f} mm, figure width {(fr - fl) / s:.1f} mm")
