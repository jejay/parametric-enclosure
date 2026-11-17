"""Rectify the oblique kosla photo into the board frame using the 4 mounting-hole centres
(raster 34/25/37 mm) and save a 20 px/mm image compatible with ant_edges.py / hole_radial.py.

Board frame as in the top views: x from the header-end edge (mid pair at x=25.9), y from the
pin-1 long edge (raster centre line at y=19.3). usage: k_rectify.py UPRIGHT_PNG OUT_PREFIX
"""
import sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

src, outp = sys.argv[1], sys.argv[2]
A = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255.0
XM, YC = 25.9, 19.3
holes_img = [(773.8, 1934.6), (1353.0, 2445.5), (1418.3, 1655.1), (1829.8, 1947.5)]
holes_brd = [(XM, YC - 17.0), (XM, YC + 17.0), (XM + 37.0, YC - 12.5), (XM + 37.0, YC + 12.5)]


def homography(srcp, dstp):
    M = []
    for (x, y), (u, v) in zip(srcp, dstp):
        M.append([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])
        M.append([0, 0, 0, x, y, 1, -v * x, -v * y, -v])
    _, _, vt = np.linalg.svd(np.array(M, float))
    return vt[-1].reshape(3, 3)


H = homography(holes_brd, holes_img)  # board mm -> image px
PPM, MARG = 20.0, 2.0
L, W = 69.7, 38.6
xs = np.arange(-MARG, L + MARG, 1 / PPM); ys = np.arange(-MARG, W + MARG, 1 / PPM)
XX, YY = np.meshgrid(xs, ys)
P = np.stack([XX, YY, np.ones_like(XX)], axis=-1) @ H.T
U, V = P[..., 0] / P[..., 2], P[..., 1] / P[..., 2]
rect = np.stack([ndi.map_coordinates(A[..., c], [V, U], order=1, mode="constant", cval=0.0) for c in range(3)], axis=-1)
np.save(outp + "_rect.npy", rect.astype(np.float32))
im = Image.fromarray((np.clip(rect, 0, 1) * 255).astype(np.uint8))
d = ImageDraw.Draw(im)
for gx in range(0, int(L) + 1, 5):
    px = (gx + MARG) * PPM
    d.line([(px, 0), (px, im.height)], fill=(255, 255, 0), width=1)
    d.text((px + 2, 2), str(gx), fill=(255, 255, 0))
for gy in range(0, int(W) + 1, 5):
    py = (gy + MARG) * PPM
    d.line([(0, py), (im.width, py)], fill=(0, 255, 255), width=1)
    d.text((2, py + 2), str(gy), fill=(0, 255, 255))
im.save(outp + "_rect.png")
print("saved", outp + "_rect.png", im.size)
