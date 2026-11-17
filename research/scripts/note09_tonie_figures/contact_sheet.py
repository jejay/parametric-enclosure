"""Make a contact sheet from the images in a directory.

Usage: python -I contact_sheet.py DIR OUT.jpg [COLS] [THUMB_W]
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = 80_000_000


def main():
    d, out = sys.argv[1], sys.argv[2]
    cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    tw = int(sys.argv[4]) if len(sys.argv) > 4 else 480
    files = sorted(glob.glob(os.path.join(d, "*.jpg")) + glob.glob(os.path.join(d, "*.png")))
    thumbs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        th = int(im.size[1] * tw / im.size[0])
        im = im.resize((tw, th), Image.LANCZOS)
        ImageDraw.Draw(im).text((6, 4), os.path.basename(f), fill=(255, 0, 0))
        thumbs.append(im)
    if not thumbs:
        raise SystemExit("no images")
    th = max(t.size[1] for t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (40, 40, 40))
    for i, t in enumerate(thumbs):
        sheet.paste(t, ((i % cols) * tw, (i // cols) * th))
    sheet.save(out, quality=88)
    print("saved", out, sheet.size, len(thumbs))


if __name__ == "__main__":
    main()
