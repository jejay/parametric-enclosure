"""Save an EXIF-orientation-corrected PNG copy of an image. usage: exif_fix.py IN OUT"""
import sys
from PIL import Image, ImageOps

im = Image.open(sys.argv[1])
print("orig size", im.size, "exif orientation", im.getexif().get(274))
im2 = ImageOps.exif_transpose(im).convert("RGB")
im2.save(sys.argv[2])
print("saved", sys.argv[2], im2.size)
