"""Segment the oblique board photo into soldermask-blue / other and report blobs.

usage: k_segment.py IN_PNG OUT_MASK_PNG x0 y0 x1 y1
Writes a mask image (white = not blue) for the given window and prints connected
components (non-blue blobs fully inside the blue area) with centroid + bbox in source px.
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = (int(v) for v in sys.argv[3:7])
im = Image.open(src).convert("RGB").crop((x0, y0, x1, y1))
a = np.asarray(im).astype(np.float32) / 255.0
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mx = a.max(axis=2)
mn = a.min(axis=2)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
# soldermask: blue clearly dominant
blue = (b > r * 1.25) & (b > g * 1.08) & (sat > 0.30) & (b > 0.10)
nonblue = ~blue
Image.fromarray((nonblue * 255).astype(np.uint8)).save(dst)

lab, n = ndi.label(nonblue)
print("components", n)
objs = ndi.find_objects(lab)
H, W = nonblue.shape
rows = []
for i, sl in enumerate(objs, start=1):
    ys, xs = sl
    area = int((lab[sl] == i).sum())
    if area < 150:
        continue
    touches = ys.start == 0 or xs.start == 0 or ys.stop == H or xs.stop == W
    cy, cx = ndi.center_of_mass(lab == i)
    rows.append((area, cx + x0, cy + y0, xs.start + x0, xs.stop + x0, ys.start + y0, ys.stop + y0, touches))
rows.sort(key=lambda t: -t[0])
for area, cx, cy, xa, xb, ya, yb, t in rows[:80]:
    print(f"area {area:7d} centroid ({cx:8.1f},{cy:8.1f}) bbox x[{xa},{xb}] y[{ya},{yb}] size {xb-xa}x{yb-ya} edge={t}")
