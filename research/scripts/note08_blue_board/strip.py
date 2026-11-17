"""Straighten a strip of an image along the segment P->Q.

usage: strip.py IN OUT px py qx qy halfwidth [yscale] [xstep]
Output: x axis = position along P->Q (one column per xstep source px), y axis = signed
offset perpendicular to the segment, scaled by yscale. The top row is offset +halfwidth
along the normal n = (dy, -dx) (i.e. to the LEFT of the travel direction as seen in the
image with y pointing down), the bottom row is offset -halfwidth.
Tick marks every 100 source px along the segment; a cyan ruler shows offsets.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
px, py, qx, qy, hw = (float(v) for v in sys.argv[3:8])
yscale = float(sys.argv[8]) if len(sys.argv) > 8 else 4.0
xstep = float(sys.argv[9]) if len(sys.argv) > 9 else 1.0

im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
P = np.array([px, py])
Q = np.array([qx, qy])
L = np.linalg.norm(Q - P)
d = (Q - P) / L
n = np.array([d[1], -d[0]])
ts = np.arange(0, L, xstep)
offs = np.arange(hw, -hw - 1e-6, -1.0 / yscale)  # top row = +hw
T, O = np.meshgrid(ts, offs)
X = P[0] + T * d[0] + O * n[0]
Y = P[1] + T * d[1] + O * n[1]
out = np.zeros(X.shape + (3,), np.float32)
for c in range(3):
    out[..., c] = ndi.map_coordinates(im[..., c], [Y, X], order=1, mode="nearest")
img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
dr = ImageDraw.Draw(img)
for k in range(0, int(L), 100):
    x = k / xstep
    dr.line([(x, 0), (x, 8)], fill=(255, 255, 0), width=1)
    dr.text((x + 2, 8), str(k), fill=(255, 255, 0))
for o in range(-int(hw), int(hw) + 1, 5):
    y = (hw - o) * yscale
    dr.line([(0, y), (5 if o % 10 else 10, y)], fill=(0, 255, 255), width=1)
    if o % 10 == 0:
        dr.text((12, y - 5), str(o), fill=(0, 255, 255))
img.save(dst)
print("saved", dst, img.size, "length px", round(L, 1), "dir", d.round(4).tolist(), "normal(top)", n.round(4).tolist())
