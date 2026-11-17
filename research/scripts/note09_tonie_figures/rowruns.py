"""Print, per image row, the sub-pixel extent of the dark/grey run through a seed column.

Usage: python -I rowruns.py IMG SEED_X Y0 Y1 [STEP] [LEVEL]
The run is grown left and right from SEED_X while the pixel is opaque, unsaturated and darker
than LEVEL (default 170); the end points are interpolated on the luminance profile.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import mcommon as mc


def run_extent(lum, sat, al, y, seed, level=170.0, maxsat=0.2):
    w = lum.shape[1]
    ok = (al[y] > 200) & (sat[y] < maxsat) & (lum[y] < level)
    if not ok[seed]:
        return None
    xl = seed
    while xl > 0 and ok[xl - 1]:
        xl -= 1
    xr = seed
    while xr < w - 1 and ok[xr + 1]:
        xr += 1
    # sub-pixel: linear interpolation of the luminance crossing of `level`
    def interp(i_in, i_out):
        a, b = lum[y, i_in], lum[y, i_out]
        if al[y, i_out] <= 200 or sat[y, i_out] >= maxsat:
            return (i_in + i_out) / 2.0  # edge against a coloured / transparent neighbour
        if b == a:
            return float(i_in)
        t = (level - a) / (b - a)
        return i_in + (i_out - i_in) * float(np.clip(t, 0, 1))

    left = interp(xl, xl - 1) if xl > 0 else float(xl)
    right = interp(xr, xr + 1) if xr < w - 1 else float(xr)
    return left, right


def main():
    path = sys.argv[1]
    seed, y0, y1 = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    step = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    level = float(sys.argv[6]) if len(sys.argv) > 6 else 170.0
    a = mc.load_rgba(path)
    r, g, b, al, sat, lum = mc.channels(a)
    for y in range(y0, y1, step):
        e = run_extent(lum, sat, al, y, seed, level)
        if e is None:
            print(f"y={y:4d} seed not dark")
        else:
            print(f"y={y:4d} left={e[0]:8.2f} right={e[1]:8.2f} width={e[1] - e[0]:8.2f} centre={(e[0] + e[1]) / 2:8.2f}")


if __name__ == "__main__":
    main()
