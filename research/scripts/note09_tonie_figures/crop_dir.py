"""Crop every image of a directory to a box and write the crops to another directory.

Usage: python -I crop_dir.py INDIR OUTDIR x0 y0 x1 y1 [scale]
"""
import glob, os, sys
from PIL import Image
ind, outd = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = (int(v) for v in sys.argv[3:7])
sc = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
os.makedirs(outd, exist_ok=True)
for f in sorted(glob.glob(os.path.join(ind, "*.jpg"))):
    im = Image.open(f).convert("RGB").crop((x0, y0, x1, y1))
    if sc != 1.0:
        im = im.resize((int(im.size[0] * sc), int(im.size[1] * sc)), Image.LANCZOS)
    im.save(os.path.join(outd, os.path.basename(f)), quality=90)
print("done")
