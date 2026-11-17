"""Measure a Pokémon Tonie standing on a Toniebox 2 (official 'auf Toniebox' pictures).

Usage: python -I measure_onbox.py IMG OVERLAY_OUT.png RING_OUTER_MM RING_INNER_MM [--ring-rows y0 y1] [--verbose]

Method
  * The light ring on the box top is a circle; in the picture it is an ellipse. Its outer and inner
    edges are located on horizontal scan lines (left flank) and vertical scan lines (front flank) and
    wherever else they are visible, then fitted with an axis-aligned ellipse.
  * The black puck base of the figure stands inside the ring, on the same plane. Its silhouette width
    (leftmost to rightmost dark pixel of the puck) is the puck diameter at the scale of the ring centre.
  * base diameter [mm] = ring diameter [mm] * puck width [px] / (2 * ring semi-major axis [px]).
The ring diameters in mm come from the top view (measure_topview.py).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from PIL import ImageDraw

import mcommon as mc


def arg(name, default=None):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    if default is None:
        raise SystemExit(f"missing {name}")
    return default


def main():
    path, out = sys.argv[1], sys.argv[2]
    ring_outer_mm, ring_inner_mm = float(sys.argv[3]), float(sys.argv[4])
    verbose = "--verbose" in sys.argv
    a = mc.load_rgba(path)
    r, g, b, al, sat, lum = mc.channels(a)
    h, w = al.shape
    solid = al > 200

    # ---------- puck (black base): run of dark/grey pixels through a seed column, per row
    from rowruns import run_extent

    seed = int(arg("--seed"))
    y0p, y1p = (int(v) for v in arg("--puck-rows").split(":"))
    rows = []
    for y in range(y0p, y1p + 1):
        e = run_extent(lum, sat, al, y, seed)
        if e is not None:
            rows.append((y, e[0], e[1]))
    rows = np.array(rows)
    widths = rows[:, 2] - rows[:, 1]
    # the silhouette of an upright cylinder has (nearly) constant width between the centre rows of its
    # top and bottom ellipses: take the median of the rows within 1 px of the maximum width
    wmax = np.max(widths)
    sel = widths > wmax - 1.0
    puck_w = float(np.median(widths[sel]))
    xl_sub = float(np.median(rows[sel, 1]))
    xr_sub = float(np.median(rows[sel, 2]))
    puck_cx = (xl_sub + xr_sub) / 2
    y_l = y_r = float(np.median(rows[sel, 0]))
    puck_top, puck_bottom = float(y0p), float(y1p)
    # bottom of the puck: lowest dark pixel in the seed column below the measured rows
    yb = y1p
    while yb < h - 1 and al[yb + 1, seed] > 200 and sat[yb + 1, seed] < 0.2 and lum[yb + 1, seed] < 170:
        yb += 1
    puck_bottom_front = float(yb)

    # ---------- light ring: saturated, fairly bright pixels on the white panel (not the red/yellow shell)
    # the shell colour is very saturated (sat > 0.75); the ring is pastel (0.12 .. 0.7) and bright
    ringmask = solid & (sat > 0.10) & (sat < 0.72) & (lum > 150)
    # restrict to the neighbourhood of the puck: |x - cx| < 1.1 * puck_w, y between puck top and well below
    yy, xx = np.mgrid[0:h, 0:w]
    ringmask &= (np.abs(xx - puck_cx) < 1.15 * puck_w) & (yy > puck_top - 0.10 * puck_w) & (yy < puck_bottom_front + 0.30 * puck_w)
    # remove pixels adjacent to the grey ears / yellow feet by requiring white on at least one side in the row
    outer_pts, inner_pts = [], []
    white = solid & (sat < 0.08) & (lum > 200)
    # horizontal scans: left flank (outer = first ring pixel coming from the left, preceded by white)
    for y in range(int(puck_top - 0.10 * puck_w), int(min(puck_bottom_front + 0.30 * puck_w, h - 1))):
        xs = np.nonzero(ringmask[y, : int(puck_cx)])[0]
        if len(xs) >= 3:
            runs = np.split(xs, np.nonzero(np.diff(xs) > 2)[0] + 1)
            run = runs[0]
            x0, x1 = run[0], run[-1]
            if x0 > 8 and white[y, x0 - 6 : x0 - 1].all():
                outer_pts.append((x0 - 0.5, y, "L"))
            if x1 + 7 < w and white[y, x1 + 2 : x1 + 7].all() and len(run) >= 3:
                inner_pts.append((x1 + 0.5, y, "L"))
        xs = np.nonzero(ringmask[y, int(puck_cx) :])[0]
        if len(xs) >= 3:
            xs = xs + int(puck_cx)
            runs = np.split(xs, np.nonzero(np.diff(xs) > 2)[0] + 1)
            run = runs[-1]
            x0, x1 = run[0], run[-1]
            if x1 + 8 < w and white[y, x1 + 2 : x1 + 7].all():
                outer_pts.append((x1 + 0.5, y, "R"))
            if x0 > 8 and white[y, x0 - 6 : x0 - 1].all() and len(run) >= 3:
                inner_pts.append((x0 - 0.5, y, "R"))
    # vertical scans: front flank (outer = last ring pixel going down, followed by white)
    for x in range(int(puck_cx - 1.1 * puck_w), int(puck_cx + 1.1 * puck_w)):
        if x < 0 or x >= w:
            continue
        ys_ = np.nonzero(ringmask[:, x])[0]
        ys_ = ys_[ys_ > puck_top]
        if len(ys_) >= 2:
            runs = np.split(ys_, np.nonzero(np.diff(ys_) > 2)[0] + 1)
            run = runs[-1]
            y0_, y1_ = run[0], run[-1]
            if y1_ + 7 < h and white[y1_ + 2 : y1_ + 7, x].all():
                outer_pts.append((x, y1_ + 0.5, "F"))
            if y0_ > 8 and white[y0_ - 6 : y0_ - 1, x].all():
                inner_pts.append((x, y0_ - 0.5, "F"))

    def fit(pts):
        if len(pts) < 12:
            return None
        x = np.array([p[0] for p in pts], float)
        y = np.array([p[1] for p in pts], float)
        return mc.fit_ellipse_robust(x, y, iters=6, k=2.2)

    fo = fit(outer_pts)
    if fo:
        cx, cy, ea, eb = fo[:4]
        keep = [p for p in outer_pts if abs(np.hypot((p[0] - cx) / ea, (p[1] - cy) / eb) - 1) < 0.03]
        outer_pts = keep
        fo = fit(outer_pts)
        cx, cy, ea, eb = fo[:4]
        # inner edge candidates must lie just inside the outer ellipse
        inner_pts = [p for p in inner_pts if 0.80 < np.hypot((p[0] - cx) / ea, (p[1] - cy) / eb) < 0.985]
    fi = fit(inner_pts)
    if fi:
        cx2, cy2, ea2, eb2 = fi[:4]
        inner_pts = [p for p in inner_pts if abs(np.hypot((p[0] - cx2) / ea2, (p[1] - cy2) / eb2) - 1) < 0.03]
        fi = fit(inner_pts)

    res = {
        "image": os.path.basename(path),
        "puck_left_px": round(float(xl_sub), 2),
        "puck_right_px": round(float(xr_sub), 2),
        "puck_width_px": round(float(puck_w), 2),
        "puck_rows_used_y": [puck_top, puck_bottom],
        "puck_front_bottom_y": puck_bottom_front,
        "puck_centre_x": round(float(puck_cx), 2),
        "n_outer_pts": len(outer_pts),
        "n_inner_pts": len(inner_pts),
    }
    if fo:
        cx, cy, ea, eb, rms, n = fo
        res["ring_outer_ellipse_cx_cy_a_b"] = [round(float(v), 2) for v in (cx, cy, ea, eb)]
        res["ring_outer_fit_rms_rel"] = round(float(rms), 5)
        res["ring_outer_fit_n"] = n
        res["view_elevation_deg_from_outer"] = round(float(np.degrees(np.arcsin(eb / ea))), 2)
        res["puck_diameter_mm_from_outer"] = round(ring_outer_mm * puck_w / (2 * ea), 2)
        res["puck_centre_minus_ring_centre_px"] = round(float(puck_cx - cx), 2)
    if fi:
        cx, cy, ea, eb, rms, n = fi
        res["ring_inner_ellipse_cx_cy_a_b"] = [round(float(v), 2) for v in (cx, cy, ea, eb)]
        res["ring_inner_fit_rms_rel"] = round(float(rms), 5)
        res["ring_inner_fit_n"] = n
        res["view_elevation_deg_from_inner"] = round(float(np.degrees(np.arcsin(eb / ea))), 2)
        res["puck_diameter_mm_from_inner"] = round(ring_inner_mm * puck_w / (2 * ea), 2)
    print(json.dumps(res, indent=1))

    im = mc.overlay_base(a)
    d = ImageDraw.Draw(im)
    for x, y, tag in outer_pts:
        d.point((x, y), fill=(255, 255, 0))
    for x, y, tag in inner_pts:
        d.point((x, y), fill=(0, 255, 255))
    if fo:
        mc.draw_ellipse(d, fo[0], fo[1], fo[2], fo[3], (255, 200, 0), 1)
    if fi:
        mc.draw_ellipse(d, fi[0], fi[1], fi[2], fi[3], (0, 200, 255), 1)
    d.line([(xl_sub, y_l - 25), (xl_sub, y_l + 25)], fill=(255, 0, 255), width=2)
    d.line([(xr_sub, y_r - 25), (xr_sub, y_r + 25)], fill=(255, 0, 255), width=2)
    d.line([(xl_sub, y_l), (xr_sub, y_r)], fill=(255, 0, 255), width=1)
    im.save(out)
    if verbose:
        for p in outer_pts[:: max(len(outer_pts) // 40, 1)]:
            print("outer", p)


if __name__ == "__main__":
    main()
