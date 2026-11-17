"""Measure one Pokémon Tonie standing on the Toniebox 2 in a video frame (weak-perspective estimate).

Usage: python -I video_measure.py FRAME.jpg --left x0,x1,y0,y1 --right x0,x1,y0,y1 --bottom x0,x1,y0,y1
           --topbox x0,y0,x1,y1 --hue yellow|teal|orange|blue|dark --elev DEG [--base-mm 45]
           [--ring-px A_OUTER --ring-mm 76.04]

  left/right/bottom : boxes for the puck silhouette edges (as in puck3d.py)
  topbox + hue      : where to look for the highest pixel of the figure and how to recognise it
  elev              : view elevation in degrees (from the ring ellipse of the empty-box frame)
Prints the puck width in px, the height of the figure in units of the puck diameter and in mm,
and - if the ring's semi-major axis in px is given - the puck diameter from the ring ratio.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import mcommon as mc


def arg(name, default=None):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


def main():
    path = sys.argv[1]
    a = mc.load_rgba(path)
    r, g, b, al, sat, lum = mc.channels(a)
    val = np.maximum(np.maximum(r, g), b)
    level, bright = float(arg("--level", "120")), float(arg("--bright", "160"))

    def rows(bx, from_left):
        x0, x1, y0, y1 = (int(v) for v in bx.split(","))
        out = []
        for y in range(y0, y1 + 1):
            prof = val[y, x0:x1 + 1]
            if not from_left:
                prof = prof[::-1]
            idx = np.nonzero(prof < level)[0]
            if len(idx) == 0 or idx[0] < 3:
                continue
            i = idx[0]
            if prof[max(i - 6, 0):i - 1].mean() < bright:
                continue
            tt = (i - 1) + (prof[i - 1] - level) / (prof[i - 1] - prof[i])
            out.append(x0 + tt if from_left else x1 - tt)
        return np.array(out)

    def cols(bx):
        x0, x1, y0, y1 = (int(v) for v in bx.split(","))
        out = []
        for x in range(x0, x1 + 1):
            prof = val[y0:y1 + 1, x][::-1]
            idx = np.nonzero(prof < level)[0]
            if len(idx) == 0 or idx[0] < 3:
                continue
            i = idx[0]
            if prof[max(i - 6, 0):i - 1].mean() < bright:
                continue
            tt = (i - 1) + (prof[i - 1] - level) / (prof[i - 1] - prof[i])
            out.append(y1 - tt)
        return np.array(out)

    L = rows(arg("--left"), True)
    R = rows(arg("--right"), False)
    B = cols(arg("--bottom"))
    xl, xr = float(np.median(L)), float(np.median(R))
    W = xr - xl
    ybot = float(np.max(B))                      # front point of the footprint (lowest point of the arc)
    x0, y0, x1, y1 = (int(v) for v in arg("--topbox").split(","))
    hue = arg("--hue")
    sub = (slice(y0, y1), slice(x0, x1))
    if hue == "yellow":
        m = (r[sub] > 170) & (g[sub] > 140) & (b[sub] < 110)
    elif hue == "dark":
        m = val[sub] < 70
    elif hue == "teal":
        m = (g[sub] > r[sub] + 25) & (g[sub] > 110)
    elif hue == "orange":
        m = (r[sub] > 170) & (g[sub] > 70) & (g[sub] < 150) & (b[sub] < 90)
    else:  # blue
        m = (b[sub] > r[sub] + 40) & (b[sub] > 150) & (g[sub] > 120)
    rowsum = m.sum(axis=1)
    ys = np.nonzero(rowsum >= 3)[0]
    ytop = float(y0 + ys.min())
    xtop = float(x0 + np.mean(np.nonzero(m[ys.min()])[0]))
    e = np.radians(float(arg("--elev")))
    D = float(arg("--base-mm", "45"))
    s = W / D
    T = ybot - ytop
    H = (T / s - (D / 2) * np.sin(e)) / np.cos(e)
    msg = (f"{os.path.basename(path)}: puck x {xl:.1f}..{xr:.1f} W={W:.1f} px (n={len(L)}/{len(R)}), footprint front y={ybot:.1f}, "
           f"top y={ytop:.0f} at x={xtop:.0f} (axis x={(xl + xr) / 2:.0f}), T={T:.1f} px | H/D={H / D:.3f} -> H={H:.1f} mm for D={D:.0f}")
    if arg("--ring-px"):
        a_px = float(arg("--ring-px"))
        ring_mm = float(arg("--ring-mm", "76.04"))
        msg += f" | D from ring ratio = {ring_mm * W / (2 * a_px):.2f} mm"
    print(msg)


if __name__ == "__main__":
    main()
