"""Build a metric model of the Toniebox 2 top face from the official top view.

Usage: python -I topmodel.py TOPVIEW.png OUT_MODEL.json
The model (mm, origin = centre of the white panel, +y towards the ears) contains
  * the outline of the white panel as radius over angle,
  * the centre and the inner / outer radius of the light ring,
  * the outer width of the box used for the scale (130 mm, tonies.com product data).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import mcommon as mc


def main():
    path, out = sys.argv[1], sys.argv[2]
    a = mc.load_rgba(path)
    r, g, b, al, sat, lum = mc.channels(a)
    h, w = al.shape
    solid = al > 128
    # scale from the outer width (median of the central rows)
    widths, centres = [], []
    for y in range(int(h * 0.42), int(h * 0.58)):
        xs = np.nonzero(solid[y])[0]
        xl = mc.subpixel_cross(al[y], max(xs[0] - 3, 0), xs[0] + 3, 128, True)
        xr = mc.subpixel_cross(al[y], min(xs[-1] + 3, w - 1), xs[-1] - 3, 128, True)
        widths.append(xr - xl)
        centres.append((xl + xr) / 2)
    box_w = float(np.median(widths))
    mm = 130.0 / box_w

    # white panel: unsaturated bright pixels; its boundary against the coloured rim
    white = solid & (sat < 0.10) & (lum > 200)
    ys, xs = np.nonzero(white)
    cx0, cy0 = xs.mean(), ys.mean()
    # refine the centre as the midpoint of the panel extents through the rough centre
    row = np.nonzero(white[int(cy0)])[0]
    col = np.nonzero(white[:, int(cx0)])[0]
    pcx = (row[0] + row[-1]) / 2.0
    pcy = (col[0] + col[-1]) / 2.0
    angles = np.radians(np.arange(0, 360, 0.5))
    radii = []
    colour = solid & (sat > 0.25)
    for ang in angles:
        ca, sa = np.cos(ang), np.sin(ang)
        rr = np.arange(46.0 / mm, 0.56 * box_w, 0.2)  # start outside the light ring (max 44.5 mm from the centre)
        px = np.clip(np.round(pcx + rr * ca).astype(int), 0, w - 1)
        py = np.clip(np.round(pcy + rr * sa).astype(int), 0, h - 1)
        s = sat[py, px]
        # first sample where saturation exceeds 0.2 and stays (the rim), interpolated
        idx = np.nonzero(s > 0.20)[0]
        if len(idx) == 0:
            radii.append(np.nan)
            continue
        i = idx[0]
        if i == 0:
            radii.append(rr[0])
            continue
        t = (0.20 - s[i - 1]) / (s[i] - s[i - 1]) if s[i] != s[i - 1] else 0.0
        radii.append(rr[i - 1] + t * (rr[i] - rr[i - 1]))
    radii = np.array(radii)

    # light ring (two-pass as in measure_topview.py)
    yy, xx = np.mgrid[0:h, 0:w]
    rad = np.hypot(xx - pcx, yy - pcy)
    ring = solid & (sat > 0.18) & (rad < 0.36 * box_w)
    inner = []
    for ang in np.radians(np.arange(0, 360, 1.0)):
        ca, sa = np.cos(ang), np.sin(ang)
        rr = np.arange(0.12 * box_w, 0.36 * box_w, 0.25)
        px = np.clip(np.round(pcx + rr * ca).astype(int), 0, w - 1)
        py = np.clip(np.round(pcy + rr * sa).astype(int), 0, h - 1)
        idx = np.nonzero(ring[py, px])[0]
        if len(idx) >= 8:
            inner.append((pcx + rr[idx[0]] * ca, pcy + rr[idx[0]] * sa))
    inner = np.array(inner)
    icx, icy, irad = mc.fit_circle(inner[:, 0], inner[:, 1])
    outer = []
    for ang in np.radians(np.arange(0, 360, 1.0)):
        ca, sa = np.cos(ang), np.sin(ang)
        rr = np.arange(irad - 6, irad + 45, 0.25)
        px = np.clip(np.round(icx + rr * ca).astype(int), 0, w - 1)
        py = np.clip(np.round(icy + rr * sa).astype(int), 0, h - 1)
        m = (sat[py, px] > 0.18) & solid[py, px]
        idx = np.nonzero(m)[0]
        if len(idx) < 8:
            continue
        run_end = idx[0]
        for k in idx[1:]:
            if k - run_end > 3:
                break
            run_end = k
        outer.append((icx + rr[run_end] * ca, icy + rr[run_end] * sa))
    outer = np.array(outer)
    ocx, ocy, orad = mc.fit_circle(outer[:, 0], outer[:, 1])

    model = {
        "source": os.path.basename(path),
        "scale_mm_per_px": mm,
        "box_outer_width_mm": 130.0,
        "panel_centre_px": [pcx, pcy],
        "panel_angles_deg": [float(v) for v in np.degrees(angles)],
        "panel_radius_mm": [None if np.isnan(v) else float(v * mm) for v in radii],
        "panel_width_mm": float((row[-1] - row[0] + 1) * mm),
        "panel_height_mm": float((col[-1] - col[0] + 1) * mm),
        "ring_centre_mm": [float((icx - pcx) * mm), float((icy - pcy) * mm)],
        "ring_inner_radius_mm": float(irad * mm),
        "ring_outer_radius_mm": float(orad * mm),
        "ring_outer_centre_mm": [float((ocx - pcx) * mm), float((ocy - pcy) * mm)],
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(model, f)
    rr_ = np.array([v for v in model["panel_radius_mm"] if v is not None])
    print("scale mm/px", round(mm, 5), "panel w,h mm", round(model["panel_width_mm"], 2), round(model["panel_height_mm"], 2))
    print("panel radius mm: min", round(rr_.min(), 2), "max", round(rr_.max(), 2), "at 0/90/180/270 deg:",
          [round(model["panel_radius_mm"][i], 2) for i in (0, 180, 360, 540)],
          "diagonals:", [round(model["panel_radius_mm"][i], 2) for i in (90, 270, 450, 630)])
    print("ring centre mm", [round(v, 2) for v in model["ring_centre_mm"]], "inner R", round(model["ring_inner_radius_mm"], 2),
          "outer R", round(model["ring_outer_radius_mm"], 2))


if __name__ == "__main__":
    main()
