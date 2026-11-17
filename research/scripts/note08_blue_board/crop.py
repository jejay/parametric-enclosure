"""Crop a region of an image and save an (optionally upscaled) PNG with a pixel grid.

usage: crop.py IN OUT x0 y0 x1 y1 [scale] [grid_step_px]
Coordinates are in source pixels. Grid lines are labelled with source pixel coordinates.
"""
import sys
from PIL import Image, ImageDraw

src, dst = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = (int(float(v)) for v in sys.argv[3:7])
scale = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
grid = int(sys.argv[8]) if len(sys.argv) > 8 else 0

im = Image.open(src).convert("RGB")
W, H = im.size
x0 = max(0, x0); y0 = max(0, y0); x1 = min(W, x1); y1 = min(H, y1)
c = im.crop((x0, y0, x1, y1))
if scale != 1.0:
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
if grid:
    d = ImageDraw.Draw(c)
    gx = (x0 // grid + 1) * grid
    while gx < x1:
        px = (gx - x0) * scale
        d.line([(px, 0), (px, c.height)], fill=(255, 255, 0), width=1)
        d.text((px + 2, 2), str(gx), fill=(255, 255, 0))
        gx += grid
    gy = (y0 // grid + 1) * grid
    while gy < y1:
        py = (gy - y0) * scale
        d.line([(0, py), (c.width, py)], fill=(0, 255, 255), width=1)
        d.text((2, py + 2), str(gy), fill=(0, 255, 255))
        gy += grid
c.save(dst)
print("saved", dst, c.size, "from", (x0, y0, x1, y1), "of", (W, H))
