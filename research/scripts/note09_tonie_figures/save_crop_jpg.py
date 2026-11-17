"""Save a crop of an image as JPEG. Usage: python -I save_crop_jpg.py IN OUT.jpg [x0 y0 x1 y1] [scale]"""
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = 80_000_000
im = Image.open(sys.argv[1]).convert("RGB")
if len(sys.argv) >= 7:
    im = im.crop(tuple(int(v) for v in sys.argv[3:7]))
if len(sys.argv) >= 8:
    sc = float(sys.argv[7]); im = im.resize((int(im.size[0] * sc), int(im.size[1] * sc)), Image.LANCZOS)
im.save(sys.argv[2], quality=90)
print(sys.argv[2], im.size)
