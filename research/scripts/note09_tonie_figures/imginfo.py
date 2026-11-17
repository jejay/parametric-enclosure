"""Print size/mode of images and optionally write downscaled previews.

Usage: python -I imginfo.py OUT_PREVIEW_DIR MAXSIDE IMG [IMG ...]
Images are untrusted: they are only decoded with Pillow.
"""
import os
import sys

from PIL import Image

Image.MAX_IMAGE_PIXELS = 80_000_000


def main():
    out, maxside = sys.argv[1], int(sys.argv[2])
    os.makedirs(out, exist_ok=True)
    for p in sys.argv[3:]:
        try:
            im = Image.open(p)
            im.load()
        except Exception as e:  # noqa: BLE001
            print(p, "ERROR", e)
            continue
        name = os.path.splitext(os.path.basename(p))[0]
        print(f"{os.path.basename(p)}: {im.size[0]}x{im.size[1]} mode={im.mode} format={im.format}")
        prev = im
        if prev.mode in ("RGBA", "LA", "P"):
            prev = prev.convert("RGBA")
            bg = Image.new("RGBA", prev.size, (200, 200, 200, 255))
            bg.alpha_composite(prev)
            prev = bg.convert("RGB")
        else:
            prev = prev.convert("RGB")
        prev.thumbnail((maxside, maxside), Image.LANCZOS)
        prev.save(os.path.join(out, name + "_prev.jpg"), quality=88)


if __name__ == "__main__":
    main()
