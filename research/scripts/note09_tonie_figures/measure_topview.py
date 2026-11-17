"""Measure the Toniebox 2 top view: outer width, white panel, light ring diameters.

Usage: python -I measure_topview.py IMG OVERLAY_OUT.png
Reference length: the outer width of the box = 130 mm (tonies.com product data).
"""
import json
import os
import sys

# -I drops the script directory from sys.path; add our own (trusted) script directory back.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from PIL import ImageDraw

import mcommon as mc


def main():
    path, out = sys.argv[1], sys.argv[2]
    a = mc.load_rgba(path)
    r, g, b, al, sat, lum = mc.channels(a)
    h, w = al.shape
    solid = al > 128

    # --- outer outline of the box: per row, first/last opaque pixel (alpha crossing at 128)
    rows = {}
    for y in range(h):
        xs = np.nonzero(solid[y])[0]
        if len(xs) > 200:
            xl = mc.subpixel_cross(al[y], max(xs[0] - 3, 0), xs[0] + 3, 128, True)
            xr = mc.subpixel_cross(al[y], min(xs[-1] + 3, w - 1), xs[-1] - 3, 128, True)
            if xl is not None and xr is not None:
                rows[y] = (xl, xr)
    ys = sorted(rows)
    widths = np.array([rows[y][1] - rows[y][0] for y in ys])
    # the label tag sticks out on the right in a few rows: use the median of the widest 40 % band in the middle
    mid = [y for y in ys if ys[0] + 0.3 * (ys[-1] - ys[0]) < y < ys[0] + 0.7 * (ys[-1] - ys[0])]
    wmid = np.array([rows[y][1] - rows[y][0] for y in mid])
    box_w = float(np.median(wmid))
    box_cx = float(np.median([(rows[y][0] + rows[y][1]) / 2 for y in mid]))
    cols = {}
    for x in range(w):
        yy = np.nonzero(solid[:, x])[0]
        if len(yy) > 200:
            cols[x] = (yy[0], yy[-1])
    xs_all = sorted(cols)
    midx = [x for x in xs_all if xs_all[0] + 0.3 * (xs_all[-1] - xs_all[0]) < x < xs_all[0] + 0.7 * (xs_all[-1] - xs_all[0])]
    box_h = float(np.median([cols[x][1] - cols[x][0] + 1 for x in midx]))
    box_cy = float(np.median([(cols[x][1] + cols[x][0]) / 2 for x in midx]))

    # --- white panel: achromatic bright pixels; width along the centre row band
    white = solid & (sat < 0.06) & (lum > 225)
    pw = []
    for y in range(int(box_cy) - 40, int(box_cy) + 40):
        xs = np.nonzero(white[y])[0]
        if len(xs):
            pw.append((xs[0], xs[-1]))
    panel_w = float(np.median([q[1] - q[0] + 1 for q in pw]))

    # --- light ring: saturated pixels well inside the panel
    yy, xx = np.mgrid[0:h, 0:w]
    rad = np.hypot(xx - box_cx, yy - box_cy)
    ring = solid & (sat > 0.18) & (rad < 0.42 * box_w)
    # boundary points along rays from the box centre
    outer, inner = [], []
    for ang in np.radians(np.arange(0, 360, 1.0)):
        ca, sa = np.cos(ang), np.sin(ang)
        rr = np.arange(0.15 * box_w, 0.42 * box_w, 0.25)
        px = np.clip(np.round(box_cx + rr * ca).astype(int), 0, w - 1)
        py = np.clip(np.round(box_cy + rr * sa).astype(int), 0, h - 1)
        m = ring[py, px]
        idx = np.nonzero(m)[0]
        if len(idx) < 8:
            continue
        inner.append((box_cx + rr[idx[0]] * ca, box_cy + rr[idx[0]] * sa))
        outer.append((box_cx + rr[idx[-1]] * ca, box_cy + rr[idx[-1]] * sa))
    inner = np.array(inner)
    icx, icy, irad = mc.fit_circle(inner[:, 0], inner[:, 1])
    ie = mc.fit_ellipse_robust(inner[:, 0], inner[:, 1])
    # second pass for the outer edge: search only a narrow band outside the inner circle,
    # from the ring's own centre (the ring is not centred on the box)
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
        # last pixel of the first contiguous saturated run
        run_end = idx[0]
        for k in idx[1:]:
            if k - run_end > 3:
                break
            run_end = k
        outer.append((icx + rr[run_end] * ca, icy + rr[run_end] * sa))
    outer = np.array(outer)
    ocx, ocy, orad = mc.fit_circle(outer[:, 0], outer[:, 1])
    oe = mc.fit_ellipse_robust(outer[:, 0], outer[:, 1])

    mm_per_px = 130.0 / box_w
    res = {
        "image": path,
        "box_outer_width_px": round(box_w, 2),
        "box_outer_height_px": round(box_h, 2),
        "box_centre_px": [round(box_cx, 2), round(box_cy, 2)],
        "mm_per_px_if_width_130": round(mm_per_px, 5),
        "box_height_mm_if_width_130": round(box_h * mm_per_px, 2),
        "white_panel_width_px": round(panel_w, 2),
        "white_panel_width_mm": round(panel_w * mm_per_px, 2),
        "ring_outer_circle_px": [round(ocx, 2), round(ocy, 2), round(orad, 2)],
        "ring_inner_circle_px": [round(icx, 2), round(icy, 2), round(irad, 2)],
        "ring_outer_ellipse_px_cx_cy_a_b_rms_n": [round(float(v), 3) for v in oe],
        "ring_inner_ellipse_px_cx_cy_a_b_rms_n": [round(float(v), 3) for v in ie],
        "ring_outer_diameter_mm": round(2 * orad * mm_per_px, 2),
        "ring_inner_diameter_mm": round(2 * irad * mm_per_px, 2),
        "ring_centre_offset_from_box_centre_mm": [
            round((icx - box_cx) * mm_per_px, 2),
            round((icy - box_cy) * mm_per_px, 2),
        ],
        "n_ring_rays": int(len(outer)),
    }
    print(json.dumps(res, indent=1))

    im = mc.overlay_base(a)
    d = ImageDraw.Draw(im)
    mc.draw_ellipse(d, ocx, ocy, orad, orad, (255, 255, 0), 2)
    mc.draw_ellipse(d, icx, icy, irad, irad, (0, 255, 255), 2)
    yc = int(box_cy)
    d.line([(box_cx - box_w / 2, yc), (box_cx + box_w / 2, yc)], fill=(255, 0, 255), width=2)
    mc.draw_cross(d, box_cx, box_cy, (255, 0, 255))
    im.save(out)


if __name__ == "__main__":
    main()
