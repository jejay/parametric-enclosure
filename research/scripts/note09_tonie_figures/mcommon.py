"""Shared helpers for measuring the Tonie reference pictures.

Images are untrusted downloads: they are only decoded with Pillow.
Run the callers with `python -I` and pass every path as an argument.
"""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = 80_000_000


def load_rgba(path: str) -> np.ndarray:
    im = Image.open(path)
    im.load()
    return np.asarray(im.convert("RGBA"), dtype=np.float64)


def channels(a: np.ndarray):
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0.0)
    lum = (r + g + b) / 3.0
    return r, g, b, al, sat, lum


def fit_ellipse_axis_aligned(x, y):
    """Least-squares ellipse with axes parallel to the image axes.

    Solves A x^2 + C y^2 + D x + E y = 1 and returns (cx, cy, a, b).
    """
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    m = np.column_stack([x * x, y * y, x, y])
    coef, *_ = np.linalg.lstsq(m, np.ones_like(x), rcond=None)
    A, C, D, E = coef
    cx = -D / (2 * A)
    cy = -E / (2 * C)
    rhs = 1 + A * cx * cx + C * cy * cy
    a = np.sqrt(rhs / A)
    b = np.sqrt(rhs / C)
    return cx, cy, a, b


def fit_ellipse_robust(x, y, iters=4, k=2.5):
    """Axis-aligned ellipse fit with outlier rejection on the radial residual."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    keep = np.ones(len(x), bool)
    res = None
    for _ in range(iters):
        cx, cy, a, b = fit_ellipse_axis_aligned(x[keep], y[keep])
        rr = np.sqrt(((x - cx) / a) ** 2 + ((y - cy) / b) ** 2) - 1.0
        s = np.std(rr[keep]) + 1e-9
        new = np.abs(rr) < max(k * s, 0.004)
        res = (cx, cy, a, b, float(np.std(rr[new]) if new.any() else np.nan), int(new.sum()))
        if new.sum() < 6 or (new == keep).all():
            break
        keep = new
    return res


def fit_circle(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    m = np.column_stack([2 * x, 2 * y, np.ones_like(x)])
    rhs = x * x + y * y
    (cx, cy, c), *_ = np.linalg.lstsq(m, rhs, rcond=None)
    r = np.sqrt(c + cx * cx + cy * cy)
    return cx, cy, r


def subpixel_cross(profile: np.ndarray, idx0: int, idx1: int, level: float, rising: bool):
    """First index in [idx0, idx1) where the profile crosses `level` (linear interpolation)."""
    step = 1 if idx1 >= idx0 else -1
    prev = profile[idx0]
    for i in range(idx0 + step, idx1, step):
        cur = profile[i]
        if rising and prev < level <= cur or (not rising) and prev > level >= cur:
            t = (level - prev) / (cur - prev) if cur != prev else 0.0
            return (i - step) + step * t
        prev = cur
    return None


def overlay_base(a: np.ndarray) -> Image.Image:
    rgb = a[..., :3].copy()
    al = a[..., 3:4] / 255.0
    bg = np.full_like(rgb, 205.0)
    out = rgb * al + bg * (1 - al)
    return Image.fromarray(out.astype(np.uint8), "RGB")


def draw_ellipse(draw: ImageDraw.ImageDraw, cx, cy, a, b, color, width=2, t0=0.0, t1=360.0):
    pts = []
    for t in np.linspace(np.radians(t0), np.radians(t1), 361):
        pts.append((cx + a * np.cos(t), cy + b * np.sin(t)))
    draw.line(pts, fill=color, width=width)


def draw_cross(draw, x, y, color, s=6, width=2):
    draw.line([(x - s, y), (x + s, y)], fill=color, width=width)
    draw.line([(x, y - s), (x, y + s)], fill=color, width=width)
