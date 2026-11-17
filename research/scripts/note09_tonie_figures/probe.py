"""Exploration helper for measuring pictures (untrusted images, decoded with Pillow only).

Usage:
  python -I probe.py row  IMG y [x0 x1 step]      # print RGBA + saturation along a row
  python -I probe.py col  IMG x [y0 y1 step]      # same along a column
  python -I probe.py crop IMG x0 y0 x1 y1 OUT.png [scale]   # save an enlarged crop (to the scratchpad)
  python -I probe.py bbox IMG kind                # bounding box of a pixel class: dark | sat | notbg
"""
import sys

from PIL import Image

Image.MAX_IMAGE_PIXELS = 80_000_000


def load(p):
    im = Image.open(p)
    im.load()
    return im.convert("RGBA")


def sat(r, g, b):
    mx, mn = max(r, g, b), min(r, g, b)
    return 0 if mx == 0 else (mx - mn) / mx


def main():
    cmd, path = sys.argv[1], sys.argv[2]
    im = load(path)
    w, h = im.size
    px = im.load()
    if cmd == "row":
        y = int(sys.argv[3])
        x0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        x1 = int(sys.argv[5]) if len(sys.argv) > 5 else w
        st = int(sys.argv[6]) if len(sys.argv) > 6 else 4
        for x in range(x0, min(x1, w), st):
            r, g, b, a = px[x, y]
            print(f"x={x:5d} rgba=({r:3d},{g:3d},{b:3d},{a:3d}) sat={sat(r, g, b):.2f} lum={(r + g + b) / 3:.0f}")
    elif cmd == "col":
        x = int(sys.argv[3])
        y0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        y1 = int(sys.argv[5]) if len(sys.argv) > 5 else h
        st = int(sys.argv[6]) if len(sys.argv) > 6 else 4
        for y in range(y0, min(y1, h), st):
            r, g, b, a = px[x, y]
            print(f"y={y:5d} rgba=({r:3d},{g:3d},{b:3d},{a:3d}) sat={sat(r, g, b):.2f} lum={(r + g + b) / 3:.0f}")
    elif cmd == "crop":
        x0, y0, x1, y1 = (int(v) for v in sys.argv[3:7])
        out = sys.argv[7]
        sc = float(sys.argv[8]) if len(sys.argv) > 8 else 1.0
        c = im.crop((x0, y0, x1, y1))
        bg = Image.new("RGBA", c.size, (200, 200, 200, 255))
        bg.alpha_composite(c)
        c = bg.convert("RGB")
        if sc != 1.0:
            c = c.resize((int(c.size[0] * sc), int(c.size[1] * sc)), Image.LANCZOS)
        c.save(out)
        print("saved", out, c.size)
    elif cmd == "bbox":
        kind = sys.argv[3]
        xs, ys = [], []
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a < 128:
                    continue
                s = sat(r, g, b)
                lum = (r + g + b) / 3
                ok = (
                    (kind == "dark" and lum < 60)
                    or (kind == "sat" and s > 0.35 and lum > 90)
                    or (kind == "notbg" and a > 128)
                )
                if ok:
                    xs.append(x)
                    ys.append(y)
        if xs:
            print(kind, "x", min(xs), max(xs), "y", min(ys), max(ys), "n", len(xs))
        else:
            print(kind, "none")


if __name__ == "__main__":
    main()
