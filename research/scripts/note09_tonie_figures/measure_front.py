"""Measure a Pokémon Tonie front view ('Vorderansicht', transparent background with soft shadow).

Usage: python -I measure_front.py IMG OVERLAY.png --seed X --puck-rows Y0:Y1 [--base-mm 45] [--elev-deg auto]

Everything is expressed in units of the puck (base) diameter D and, with --base-mm, in mm.
  * puck width W: constant-width band of the dark run through the seed column (rowruns.run_extent)
  * view elevation e: from the ellipse fitted to the lower silhouette of the puck (footprint front arc),
    semi-minor / semi-major = sin e; or given with --elev-deg
  * figure top: first fully opaque row; total height H from
        (y_bottom_front - y_top) = s * (H cos e + (D/2) sin e),  s = W / D
    (assumes the highest point sits roughly above the puck axis)
  * puck height h from the vertical distance between the front point of the top rim and the front
    point of the footprint:  dy = s * h cos e
  * lateral extent of the figure (everything above the puck) relative to the puck edges
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from PIL import ImageDraw

import mcommon as mc
from rowruns import run_extent


def arg(name, default=None):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


def main():
    path, out = sys.argv[1], sys.argv[2]
    a = mc.load_rgba(path)
    r, g, b, al, sat, lum = mc.channels(a)
    h, w = al.shape
    val = np.maximum(np.maximum(r, g), b)
    seed = int(arg("--seed"))
    y0p, y1p = (int(v) for v in arg("--puck-rows").split(":"))
    D = float(arg("--base-mm", "45"))

    # object mask: fully opaque pixels (the cast shadow is semi-transparent)
    obj = al >= 250
    ys, xs = np.nonzero(obj)
    y_top = int(ys.min())
    x_top = float(np.mean(xs[ys == y_top]))

    # puck width
    rows = []
    for y in range(y0p, y1p + 1):
        e = run_extent(lum, sat, al, y, seed, level=170.0, maxsat=0.25)
        if e is not None:
            rows.append((y, e[0], e[1]))
    rows = np.array(rows)
    widths = rows[:, 2] - rows[:, 1]
    sel = widths > widths.max() - 1.0
    W = float(np.median(widths[sel]))
    xl = float(np.median(rows[sel, 1]))
    xr = float(np.median(rows[sel, 2]))
    cx = 0.5 * (xl + xr)
    s = W / D                                   # px per mm

    # lower silhouette of the puck: per column, last opaque dark pixel (footprint front arc)
    dark = obj & (val < 120)
    bot = []
    for x in range(int(xl) + 2, int(xr) - 1):
        col = np.nonzero(dark[:, x])[0]
        col = col[col > y0p]
        if len(col):
            # sub-pixel using the alpha / value transition below the last dark pixel
            yb = col[-1]
            bot.append((x, float(yb) + 0.5))
    bot = np.array(bot)
    # ellipse with known centre x and semi-major axis W/2: y = yc + b*sqrt(1-((x-cx)/a)^2)
    aa = W / 2.0
    u = np.sqrt(np.clip(1 - ((bot[:, 0] - cx) / aa) ** 2, 0, 1))
    # use the central 85 % (the ends are steep and dominated by the fillet at the lower edge)
    m = np.abs(bot[:, 0] - cx) < 0.85 * aa
    A = np.column_stack([np.ones(m.sum()), u[m]])
    (yc, bb), *_ = np.linalg.lstsq(A, bot[m, 1], rcond=None)
    res_fit = bot[m, 1] - (yc + bb * u[m])
    e_fit = float(np.degrees(np.arcsin(np.clip(bb / aa, 0, 1))))
    e_arg = arg("--elev-deg", "auto")
    e = e_fit if e_arg == "auto" else float(e_arg)
    er = np.radians(e)
    y_bot = float(yc + bb)                       # front point of the footprint

    # top rim of the puck at the front: first dark pixel in the columns next to the centre where the
    # figure does not cover it is not generally available, so use the left/right flanks instead:
    # at the flank (x = cx +- 0.9a .. 0.97a) the top-rim ellipse and the footprint ellipse differ by h cos e
    top = []
    for x in list(range(int(cx - 0.97 * aa), int(cx - 0.80 * aa))) + list(range(int(cx + 0.80 * aa), int(cx + 0.97 * aa))):
        col = np.nonzero(dark[:, x])[0]
        col = col[(col > y0p - 0.8 * aa) & (col <= y1p + 0.9 * aa)]
        if len(col) < 5:
            continue
        # contiguous dark run ending at the footprint
        yb = col[-1]
        yt = yb
        while yt - 1 in set(col.tolist()):
            yt -= 1
        uu = np.sqrt(max(1 - ((x - cx) / aa) ** 2, 0))
        # silhouette top at this column = back arc of the top rim: y = yc - h' - bb*uu ; bottom = yc + bb*uu
        top.append((x, yt - 0.5, yb + 0.5, uu))
    top = np.array(top)
    hprime = float(np.median((top[:, 2] - top[:, 1]) - 2 * bb * top[:, 3])) if len(top) else float("nan")
    h_puck = hprime / (s * np.cos(er))

    T = y_bot - y_top
    H = (T / s - (D / 2.0) * np.sin(er)) / np.cos(er)

    # lateral extent of the figure above the puck: opaque, non-dark-puck pixels above the puck's top rim
    y_rim_back = yc - hprime - bb                 # highest point of the puck silhouette (back of the top rim)
    fig = obj.copy()
    fig[int(y_rim_back) + 1:, :] = False
    fy, fx = np.nonzero(fig)
    fig_l, fig_r = float(fx.min()), float(fx.max()) + 1.0
    y_at_l = float(np.median(fy[fx == fx.min()]))
    y_at_r = float(np.median(fy[fx == fx.max()]))
    # overall silhouette (figure + puck)
    allx = np.nonzero(obj.any(axis=0))[0]
    sil_l, sil_r = float(allx.min()), float(allx.max()) + 1.0

    res = {
        "image": os.path.basename(path),
        "puck_width_px": round(W, 2),
        "px_per_mm_if_base_is_%.1f_mm" % D: round(s, 4),
        "view_elevation_deg_fitted": round(e_fit, 2),
        "view_elevation_deg_used": round(e, 2),
        "footprint_fit_rms_px": round(float(np.sqrt(np.mean(res_fit ** 2))), 3),
        "total_height_over_D": round(H / D, 4),
        "total_height_mm": round(H, 2),
        "puck_height_over_D": round(h_puck / D, 4),
        "puck_height_mm": round(h_puck, 2),
        "figure_only_height_mm": round(H - h_puck, 2),
        "top_point_offset_from_axis_mm": round((x_top - cx) / s, 2),
        "figure_left_beyond_puck_mm": round((xl - fig_l) / s, 2),
        "figure_right_beyond_puck_mm": round((fig_r - xr) / s, 2),
        "figure_lateral_width_mm": round((fig_r - fig_l) / s, 2),
        "silhouette_total_width_mm": round((sil_r - sil_l) / s, 2),
        "height_of_left_extreme_above_base_mm": round(((y_bot - y_at_l) / s - (D / 2) * np.sin(er)) / np.cos(er), 1),
        "height_of_right_extreme_above_base_mm": round(((y_bot - y_at_r) / s - (D / 2) * np.sin(er)) / np.cos(er), 1),
    }
    print(json.dumps(res, indent=1))

    im = mc.overlay_base(a)
    d = ImageDraw.Draw(im)
    d.line([(xl, rows[sel, 0].min()), (xl, rows[sel, 0].max())], fill=(255, 0, 255), width=2)
    d.line([(xr, rows[sel, 0].min()), (xr, rows[sel, 0].max())], fill=(255, 0, 255), width=2)
    mc.draw_ellipse(d, cx, yc, aa, bb, (0, 255, 255), 1)
    mc.draw_ellipse(d, cx, yc - hprime, aa, bb, (255, 255, 0), 1)
    d.line([(cx - 40, y_top), (cx + 40, y_top)], fill=(255, 0, 0), width=1)
    d.line([(fig_l, y_top), (fig_l, y_rim_back)], fill=(0, 255, 0), width=1)
    d.line([(fig_r, y_top), (fig_r, y_rim_back)], fill=(0, 255, 0), width=1)
    d.line([(cx - 40, y_bot), (cx + 40, y_bot)], fill=(255, 0, 0), width=1)
    im.save(out)


if __name__ == "__main__":
    main()
