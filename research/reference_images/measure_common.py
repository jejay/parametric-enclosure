"""Shared helpers for the Poke Ball reference-image measurements.

Only numpy + Pillow.  Every image in this folder is a download from the web and
is treated as untrusted data: it is only ever decoded by Pillow, never executed.
Run the scripts from the repo root with the interpreter in isolated mode, e.g.

    uv run python -I research/reference_images/measure_front_views.py

Conventions
-----------
* Pixel coordinates are (x, y) with y pointing DOWN, origin at the top-left
  pixel centre (so a pixel covers [x-0.5, x+0.5]).
* An "edge" is located at the extremum of the first derivative of a smoothed
  1-D profile sampled along a line segment (sub-pixel via parabola fit).  For an
  anti-aliased or slightly blurred step this is the 50 % point of the step.
* Circles seen obliquely project to ellipses.  Under (near-)orthographic
  projection the MAJOR axis of that ellipse equals the true diameter, so all
  ring/disc/button diameters are reported from the major axis.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
OVERLAYS = HERE / "overlays"


# --------------------------------------------------------------------------- IO
def load(path, bg=(255, 255, 255)):
    """Return (rgb float64 HxWx3 in 0..255 composited on bg, alpha HxW 0..1 or None)."""
    im = Image.open(path)
    if im.mode in ("P", "LA", "PA"):
        im = im.convert("RGBA")
    if im.mode == "RGBA":
        a = np.asarray(im, dtype=np.float64)
        alpha = a[..., 3] / 255.0
        rgb = a[..., :3] * alpha[..., None] + np.array(bg, float)[None, None, :] * (1 - alpha[..., None])
        return rgb, alpha
    return np.asarray(im.convert("RGB"), dtype=np.float64), None


def metric(rgb, alpha, name, bg=(255, 255, 255)):
    """Scalar field used for edge finding."""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    if name == "lum":
        return 0.299 * r + 0.587 * g + 0.114 * b
    if name == "val":  # HSV value: black is the only low region (red and white are high)
        return np.max(rgb, axis=2)
    if name == "min":  # low for saturated red AND black, high only for white/grey
        return np.min(rgb, axis=2)
    if name == "R":
        return r
    if name == "G":
        return g
    if name == "B":
        return b
    if name == "r-g":
        return r - g
    if name == "red":  # redness
        return r - 0.5 * (g + b)
    if name == "alpha":
        if alpha is None:
            raise ValueError("image has no alpha")
        return alpha * 255.0
    if name == "bgdist":
        return np.sqrt(((rgb - np.array(bg, float)[None, None, :]) ** 2).sum(axis=2))
    raise ValueError(name)


def bilinear(field, xs, ys):
    h, w = field.shape
    xs = np.clip(np.asarray(xs, float), 0, w - 1.001)
    ys = np.clip(np.asarray(ys, float), 0, h - 1.001)
    x0 = np.floor(xs).astype(int)
    y0 = np.floor(ys).astype(int)
    fx = xs - x0
    fy = ys - y0
    return (field[y0, x0] * (1 - fx) * (1 - fy) + field[y0, x0 + 1] * fx * (1 - fy)
            + field[y0 + 1, x0] * (1 - fx) * fy + field[y0 + 1, x0 + 1] * fx * fy)


# ------------------------------------------------------------------------ edges
def _gauss_kernel(sigma_samples):
    n = max(1, int(math.ceil(3 * sigma_samples)))
    x = np.arange(-n, n + 1)
    k = np.exp(-0.5 * (x / sigma_samples) ** 2)
    return k / k.sum()


def profile(field, p0, p1, step=0.25, sigma=1.0):
    """Smoothed profile along p0->p1.  Returns (dist, values)."""
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    length = float(np.hypot(*(p1 - p0)))
    n = max(8, int(length / step) + 1)
    t = np.linspace(0.0, 1.0, n)
    v = bilinear(field, p0[0] + t * (p1[0] - p0[0]), p0[1] + t * (p1[1] - p0[1]))
    if sigma > 0:
        k = _gauss_kernel(sigma / (length / (n - 1)))
        pad = len(k) // 2
        v = np.convolve(np.pad(v, pad, mode="edge"), k, mode="valid")
    return t * length, v


def find_edge(field, p0, p1, polarity, step=0.25, sigma=1.0, min_strength=0.0):
    """Strongest edge of the given polarity (+1 rising, -1 falling along p0->p1).

    Returns (point_xy, distance_from_p0, strength) or None.
    Strength is the derivative magnitude in metric units per pixel.
    """
    d, v = profile(field, p0, p1, step, sigma)
    g = np.gradient(v, d) * polarity
    m = len(k_trim := g[2:-2])
    if m < 3:
        return None
    i = int(np.argmax(k_trim)) + 2
    s = float(g[i])
    if s <= min_strength:
        return None
    # parabola through (i-1, i, i+1)
    y0, y1, y2 = g[i - 1], g[i], g[i + 1]
    den = y0 - 2 * y1 + y2
    off = 0.5 * (y0 - y2) / den if abs(den) > 1e-12 else 0.0
    off = max(-1.0, min(1.0, off))
    dist = d[i] + off * (d[1] - d[0])
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    u = (p1 - p0) / np.hypot(*(p1 - p0))
    return p0 + dist * u, float(dist), s


def find_line(field, p0, p1, polarity, step=0.25, sigma=1.0, min_strength=0.0):
    """Centre of the darkest (polarity -1) or brightest (+1) thin line crossing p0->p1.

    Used for drawn outlines and for the shadow groove between two parts.
    Strength is the contrast against the mean of the two profile ends.
    """
    d, v = profile(field, p0, p1, step, sigma)
    w = v * polarity
    i = int(np.argmax(w[2:-2])) + 2
    s = float(w[i] - 0.5 * (w[:4].mean() + w[-4:].mean()))
    if s <= min_strength:
        return None
    y0, y1, y2 = w[i - 1], w[i], w[i + 1]
    den = y0 - 2 * y1 + y2
    off = 0.5 * (y0 - y2) / den if abs(den) > 1e-12 else 0.0
    off = max(-1.0, min(1.0, off))
    dist = d[i] + off * (d[1] - d[0])
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    u = (p1 - p0) / np.hypot(*(p1 - p0))
    return p0 + dist * u, float(dist), s


def first_crossing(field, p_out, p_in, thr, step=0.25, sigma=1.0):
    """Walking from p_out (background) towards p_in: first point where field exceeds thr.

    For silhouettes against a plain background when the object has soft inner
    rim highlights that would attract the strongest-gradient search.
    Returns point_xy or None.
    """
    d, v = profile(field, p_out, p_in, step, sigma)
    idx = np.nonzero(v > thr)[0]
    if len(idx) == 0 or idx[0] == 0:
        return None
    i = int(idx[0])
    t = (thr - v[i - 1]) / (v[i] - v[i - 1])
    dist = d[i - 1] + t * (d[i] - d[i - 1])
    p_out = np.asarray(p_out, float)
    p_in = np.asarray(p_in, float)
    u = (p_in - p_out) / np.hypot(*(p_in - p_out))
    return p_out + dist * u


def ray_crossings(field, centre, angles_deg, r_in, r_out, thr, **kw):
    """first_crossing() on rays through centre, walking inwards from r_out to r_in."""
    pts = []
    c = np.asarray(centre, float)
    for a in angles_deg:
        u = np.array([math.cos(math.radians(a)), -math.sin(math.radians(a))])
        res = first_crossing(field, c + r_out * u, c + r_in * u, thr, **kw)
        if res is not None:
            pts.append(res)
    return np.array(pts)


def ray_edges(field, centre, angles_deg, r0, r1, polarity, kind="edge", **kw):
    """Edge (or line) points along rays from centre.  Angle 0 = +x (right), 90 = UP on screen."""
    pts = []
    fn = find_edge if kind == "edge" else find_line
    for a in angles_deg:
        u = np.array([math.cos(math.radians(a)), -math.sin(math.radians(a))])
        c = np.asarray(centre, float)
        res = fn(field, c + r0 * u, c + r1 * u, polarity, **kw)
        if res is not None:
            pts.append(res[0])
    return np.array(pts)


def arange_deg(*ranges, step=5.0):
    out = []
    for a0, a1 in ranges:
        n = int(round((a1 - a0) / step))
        out.extend(a0 + i * step for i in range(n + 1))
    return out


# -------------------------------------------------------------------- geometry
def fit_circle(pts, iters=20):
    """Geometric least-squares circle.  Returns (cx, cy, r, rms)."""
    pts = np.asarray(pts, float)
    x, y = pts[:, 0], pts[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones_like(x)]
    sol, *_ = np.linalg.lstsq(A, x * x + y * y, rcond=None)
    cx, cy = sol[0], sol[1]
    r = math.sqrt(max(sol[2] + cx * cx + cy * cy, 1e-9))
    for _ in range(iters):  # Gauss-Newton on geometric distance
        dx, dy = x - cx, y - cy
        d = np.hypot(dx, dy)
        J = np.c_[-dx / d, -dy / d, -np.ones_like(d)]
        delta, *_ = np.linalg.lstsq(J, -(d - r), rcond=None)
        cx, cy, r = cx + delta[0], cy + delta[1], r + delta[2]
    rms = float(np.sqrt(np.mean((np.hypot(x - cx, y - cy) - r) ** 2)))
    return float(cx), float(cy), float(r), rms


def robust_circle(pts, k=2.5, rounds=3):
    """fit_circle with iterative rejection of points > k*rms (min 1 px)."""
    pts = np.asarray(pts, float)
    keep = np.ones(len(pts), bool)
    for _ in range(rounds):
        cx, cy, r, rms = fit_circle(pts[keep])
        res = np.abs(np.hypot(pts[:, 0] - cx, pts[:, 1] - cy) - r)
        new = res <= max(k * rms, 1.0)
        if new.sum() < 6 or (new == keep).all():
            break
        keep = new
    cx, cy, r, rms = fit_circle(pts[keep])
    return cx, cy, r, rms, keep


def fit_ellipse(pts):
    """Direct least-squares ellipse (Halir & Flusser).

    Returns dict(cx, cy, a, b, theta_deg, rms) with a >= b semi-axes and theta
    the direction of the major axis (screen coords, y down).
    """
    pts = np.asarray(pts, float)
    mx, my = pts[:, 0].mean(), pts[:, 1].mean()
    sc = max(pts[:, 0].std(), pts[:, 1].std(), 1e-9)
    x = (pts[:, 0] - mx) / sc
    y = (pts[:, 1] - my) / sc
    D1 = np.c_[x * x, x * y, y * y]
    D2 = np.c_[x, y, np.ones_like(x)]
    S1, S2, S3 = D1.T @ D1, D1.T @ D2, D2.T @ D2
    T = -np.linalg.solve(S3, S2.T)
    M = S1 + S2 @ T
    M = np.array([M[2] / 2.0, -M[1], M[0] / 2.0])
    w, v = np.linalg.eig(M)
    v = np.real(v)
    cond = 4 * v[0] * v[2] - v[1] ** 2
    a1 = v[:, np.argmax(cond)]
    A, B, C = a1
    Dc, E, F = T @ a1
    # conic A x^2 + B xy + C y^2 + D x + E y + F = 0 (normalised coords)
    den = B * B - 4 * A * C
    x0 = (2 * C * Dc - B * E) / den
    y0 = (2 * A * E - B * Dc) / den
    num = 2 * (A * E * E + C * Dc * Dc - B * Dc * E + den * F)
    root = math.sqrt((A - C) ** 2 + B * B)
    ax1 = -math.sqrt(max(num * (A + C + root), 0.0)) / den
    ax2 = -math.sqrt(max(num * (A + C - root), 0.0)) / den
    if abs(B) < 1e-12:
        th = 0.0 if A < C else math.pi / 2
    else:
        th = math.atan2(C - A - root, B)
    # ax1 belongs to direction th
    if ax1 >= ax2:
        a, b, theta = ax1, ax2, th
    else:
        a, b, theta = ax2, ax1, th + math.pi / 2
    cx, cy = x0 * sc + mx, y0 * sc + my
    a, b = abs(a) * sc, abs(b) * sc
    # residual: approximate geometric distance via radial scaling
    ct, st = math.cos(theta), math.sin(theta)
    dx, dy = pts[:, 0] - cx, pts[:, 1] - cy
    u = dx * ct + dy * st
    vv = -dx * st + dy * ct
    rho = np.sqrt((u / a) ** 2 + (vv / b) ** 2)
    res = (rho - 1.0) * np.hypot(u, vv) / np.maximum(rho, 1e-9)
    return dict(cx=float(cx), cy=float(cy), a=float(a), b=float(b),
                theta_deg=float(math.degrees(theta) % 180.0), rms=float(np.sqrt(np.mean(res ** 2))))


def ellipse_points(e, n=180):
    t = np.linspace(0, 2 * math.pi, n)
    ct, st = math.cos(math.radians(e["theta_deg"])), math.sin(math.radians(e["theta_deg"]))
    u, v = e["a"] * np.cos(t), e["b"] * np.sin(t)
    return np.c_[e["cx"] + u * ct - v * st, e["cy"] + u * st + v * ct]


def circle_as_ellipse(cx, cy, r, rms=0.0):
    return dict(cx=cx, cy=cy, a=r, b=r, theta_deg=0.0, rms=rms)


# -------------------------------------------------------------------- overlays
class Overlay:
    """Draws what was measured on top of the image so it can be eyeballed."""

    def __init__(self, rgb, crop=None, scale=1.0):
        h, w, _ = rgb.shape
        self.crop = crop or (0, 0, w, h)
        x0, y0, x1, y1 = [int(round(v)) for v in self.crop]
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(w, x1), min(h, y1)
        self.crop = (x0, y0, x1, y1)
        self.scale = scale
        im = Image.fromarray(np.clip(rgb[y0:y1, x0:x1], 0, 255).astype(np.uint8))
        self.im = im.resize((max(1, int((x1 - x0) * scale)), max(1, int((y1 - y0) * scale))),
                            Image.LANCZOS if scale < 1 else Image.NEAREST)
        self.d = ImageDraw.Draw(self.im)

    def _t(self, p):
        return ((p[0] - self.crop[0] + 0.5) * self.scale, (p[1] - self.crop[1] + 0.5) * self.scale)

    def poly(self, pts, colour, width=1, closed=True):
        q = [self._t(p) for p in pts]
        if closed:
            q.append(q[0])
        self.d.line(q, fill=colour, width=width)

    def ellipse(self, e, colour, width=1):
        self.poly(ellipse_points(e), colour, width)

    def dots(self, pts, colour, r=2):
        for p in pts:
            x, y = self._t(p)
            self.d.ellipse([x - r, y - r, x + r, y + r], outline=colour)

    def tick(self, p, colour, half=6, horizontal=True):
        x, y = self._t(p)
        if horizontal:
            self.d.line([x - half, y, x + half, y], fill=colour, width=1)
        else:
            self.d.line([x, y - half, x, y + half], fill=colour, width=1)

    def save(self, name, max_w=1100):
        OVERLAYS.mkdir(exist_ok=True)
        im = self.im
        if im.size[0] > max_w:
            im = im.resize((max_w, int(im.size[1] * max_w / im.size[0])), Image.LANCZOS)
        out = OVERLAYS / name
        im.save(out)
        return out


def view_angles(ball_c, ball_r, button_c, roll_deg=0.0):
    """Yaw (about the ball's vertical axis) and tilt (camera elevation) of the button, orthographic model.

    roll_deg: in-plane rotation of the ball on screen (positive = right end of the band raised).
    yaw > 0  : button right of the ball centre (after de-rolling).
    tilt > 0 : button below the ball centre, i.e. the camera looks down on the ball.
    """
    dx = (button_c[0] - ball_c[0]) / ball_r
    dy = (button_c[1] - ball_c[1]) / ball_r
    th = math.radians(roll_deg)
    dx, dy = dx * math.cos(th) - dy * math.sin(th), dx * math.sin(th) + dy * math.cos(th)
    dx = max(-0.999, min(0.999, dx))
    yaw = math.asin(dx)
    s = dy / max(math.cos(yaw), 1e-6)
    s = max(-0.999, min(0.999, s))
    tilt = math.asin(s)
    return math.degrees(yaw), math.degrees(tilt)
