"""Fit an axis-aligned ellipse to the lit light ring of a Toniebox 2 in a frame (green/mint glow).

Usage: python -I ring_ellipse.py IMG "x0,y0,x1,y1" OVERLAY.png [GREEN_MIN]
Reports the ellipse through the glow centroid (ring mid-line) and through the outer edge.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from PIL import ImageDraw

import mcommon as mc


def main():
    path = sys.argv[1]
    x0, y0, x1, y1 = (int(v) for v in sys.argv[2].split(","))
    out = sys.argv[3]
    gmin = float(sys.argv[4]) if len(sys.argv) > 4 else 12.0
    a = mc.load_rgba(path)
    r, g, b, al, sat, lum = mc.channels(a)
    green = g - np.maximum(r, b)
    m = np.zeros(green.shape, bool)
    m[y0:y1, x0:x1] = (green[y0:y1, x0:x1] > gmin) & (lum[y0:y1, x0:x1] > 150)
    ys, xs = np.nonzero(m)
    # rough ellipse from the mask extents
    cx, cy = 0.5 * (xs.min() + xs.max()), 0.5 * (ys.min() + ys.max())
    ax, by = 0.5 * (xs.max() - xs.min()), 0.5 * (ys.max() - ys.min())
    mid, outer = [], []
    for it in range(3):
        mid, outer = [], []
        for t in np.radians(np.arange(0, 360, 1.0)):
            # ray in ellipse-normalised coordinates
            ca, sa = np.cos(t), np.sin(t)
            rr = np.linspace(0.75, 1.25, 201)
            px = cx + rr * ax * ca
            py = cy + rr * by * sa
            ix = np.clip(np.round(px).astype(int), 0, green.shape[1] - 1)
            iy = np.clip(np.round(py).astype(int), 0, green.shape[0] - 1)
            gv = np.where(lum[iy, ix] > 150, green[iy, ix], 0.0)
            if gv.max() < gmin + 4:
                continue
            w = np.clip(gv - gmin, 0, None)
            # reject rays where a dark object (ear) interrupts the profile near the maximum
            k = int(np.argmax(gv))
            if lum[iy, ix][max(k - 12, 0):k + 12].min() < 110:
                continue
            rc = float((w * rr).sum() / w.sum())
            mid.append((cx + rc * ax * ca, cy + rc * by * sa))
            idx = np.nonzero(gv > gmin)[0]
            ro = rr[idx[-1]]
            outer.append((cx + ro * ax * ca, cy + ro * by * sa))
        mid_a = np.array(mid)
        fm = mc.fit_ellipse_robust(mid_a[:, 0], mid_a[:, 1], iters=5, k=2.5)
        cx, cy, ax, by = fm[:4]
    out_a = np.array(outer)
    fo = mc.fit_ellipse_robust(out_a[:, 0], out_a[:, 1], iters=5, k=2.5)
    print(f"{os.path.basename(path)}: mid-line ellipse cx={fm[0]:.1f} cy={fm[1]:.1f} a={fm[2]:.2f} b={fm[3]:.2f} "
          f"(elev {np.degrees(np.arcsin(fm[3] / fm[2])):.2f} deg, n={fm[5]}, rms={fm[4]:.4f}) | "
          f"outer-edge ellipse a={fo[2]:.2f} b={fo[3]:.2f} (elev {np.degrees(np.arcsin(fo[3] / fo[2])):.2f} deg, n={fo[5]})")
    im = mc.overlay_base(a)
    d = ImageDraw.Draw(im)
    mc.draw_ellipse(d, fm[0], fm[1], fm[2], fm[3], (255, 0, 255), 1)
    mc.draw_ellipse(d, fo[0], fo[1], fo[2], fo[3], (255, 255, 0), 1)
    for x, y in mid:
        d.point((x, y), fill=(0, 0, 255))
    im.crop((x0 - 20, y0 - 20, x1 + 20, y1 + 20)).save(out)


if __name__ == "__main__":
    main()
