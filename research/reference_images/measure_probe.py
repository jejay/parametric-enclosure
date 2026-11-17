"""Exploration helper: print the edges found along a line, or write a zoomed crop with a pixel grid.

Used to choose the search windows hard-coded in measure_front_views.py and to
check visually that an edge sits where the script says it does.

    uv run python -I research/reference_images/measure_probe.py line  IMG metric x0 y0 x1 y1 [min_strength] [sigma]
    uv run python -I research/reference_images/measure_probe.py crop  IMG x0 y0 x1 y1 scale OUT.png [grid]
    uv run python -I research/reference_images/measure_probe.py info  IMG
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

_spec = importlib.util.spec_from_file_location("measure_common", Path(__file__).resolve().parent / "measure_common.py")
mc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mc)


def cmd_line(a):
    img, name = a[0], a[1]
    x0, y0, x1, y1 = map(float, a[2:6])
    thr = float(a[6]) if len(a) > 6 else 8.0
    sigma = float(a[7]) if len(a) > 7 else 1.0
    rgb, alpha = mc.load(img)
    f = mc.metric(rgb, alpha, name)
    d, v = mc.profile(f, (x0, y0), (x1, y1), 0.25, sigma)
    g = np.gradient(v, d)
    ux, uy = (x1 - x0) / d[-1], (y1 - y0) / d[-1]
    print(f"{name} along ({x0},{y0})->({x1},{y1}) len {d[-1]:.1f}px; start {v[0]:.0f} end {v[-1]:.0f}")
    for i in range(2, len(g) - 2):
        if abs(g[i]) >= thr and abs(g[i]) >= abs(g[i - 1]) and abs(g[i]) > abs(g[i + 1]):
            lo = v[max(0, i - 16)]
            hi = v[min(len(v) - 1, i + 16)]
            print(f"  d={d[i]:8.2f}  x={x0 + ux * d[i]:8.2f} y={y0 + uy * d[i]:8.2f}  "
                  f"{'rise' if g[i] > 0 else 'FALL'} {g[i]:+7.1f}/px   {lo:5.0f} -> {hi:5.0f}")


def cmd_crop(a):
    img = a[0]
    x0, y0, x1, y1 = map(int, a[1:5])
    scale = float(a[5])
    out = a[6]
    grid = int(a[7]) if len(a) > 7 else 0
    rgb, _ = mc.load(img, bg=(255, 0, 255))
    h, w, _ = rgb.shape
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(w, x1), min(h, y1)
    im = Image.fromarray(np.clip(rgb[y0:y1, x0:x1], 0, 255).astype(np.uint8))
    im = im.resize((int((x1 - x0) * scale), int((y1 - y0) * scale)), Image.NEAREST if scale >= 1 else Image.LANCZOS)
    if grid:
        d = ImageDraw.Draw(im)
        gx = (x0 // grid + 1) * grid
        while gx < x1:
            X = (gx - x0) * scale
            d.line([X, 0, X, im.size[1]], fill=(0, 255, 255), width=1)
            d.text((X + 2, 2), str(gx), fill=(0, 255, 255))
            gx += grid
        gy = (y0 // grid + 1) * grid
        while gy < y1:
            Y = (gy - y0) * scale
            d.line([0, Y, im.size[0], Y], fill=(255, 255, 0), width=1)
            d.text((2, Y + 2), str(gy), fill=(255, 255, 0))
            gy += grid
    im.save(out)
    print("wrote", out, im.size)


def cmd_info(a):
    rgb, alpha = mc.load(a[0])
    print(a[0], rgb.shape, "alpha" if alpha is not None else "no alpha")
    if alpha is not None:
        ys, xs = np.nonzero(alpha > 0.5)
        print("  alpha>0.5 bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max())


if __name__ == "__main__":
    {"line": cmd_line, "crop": cmd_crop, "info": cmd_info}[sys.argv[1]](sys.argv[2:])
