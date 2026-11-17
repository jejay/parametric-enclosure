"""Save a contrast-stretched crop of an image, to see faint edges.

Usage: python -I enhance.py IMG x0 y0 x1 y1 OUT.png [scale] [lo hi]
Luminance range lo..hi (default 200..255) is stretched to 0..255 per channel.
"""
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = 80_000_000


def main():
    p = sys.argv[1]
    x0, y0, x1, y1 = (int(v) for v in sys.argv[2:6])
    out = sys.argv[6]
    sc = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
    lo = float(sys.argv[8]) if len(sys.argv) > 8 else 200.0
    hi = float(sys.argv[9]) if len(sys.argv) > 9 else 255.0
    im = Image.open(p)
    im.load()
    a = np.asarray(im.convert("RGB"), dtype=np.float64)[y0:y1, x0:x1]
    a = np.clip((a - lo) / (hi - lo), 0, 1) * 255
    o = Image.fromarray(a.astype(np.uint8), "RGB")
    if sc != 1.0:
        o = o.resize((int(o.size[0] * sc), int(o.size[1] * sc)), Image.LANCZOS)
    o.save(out)
    print("saved", out, o.size)


if __name__ == "__main__":
    main()
