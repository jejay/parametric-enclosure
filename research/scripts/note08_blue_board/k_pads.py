"""Header pad centres in the oblique photo via distance-transform maxima and
weighted centroids of the inscribed core.

usage: k_pads.py UPRIGHT_PNG
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

A = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32) / 255.0
X0, Y0, X1, Y1 = 250, 2150, 960, 2860
a = A[Y0:Y1, X0:X1]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mx = a.max(axis=2); mn = a.min(axis=2)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
blue = (b > r * 1.25) & (b > g * 1.08) & (sat > 0.30) & (b > 0.10)
m = ~blue
m = ndi.binary_fill_holes(m)
dt = ndi.distance_transform_edt(m)
dts = ndi.gaussian_filter(dt, 2.0)
mxf = ndi.maximum_filter(dts, size=41)
peaks = np.argwhere((dts == mxf) & (dts > 14))
rows = []
for py, px in peaks:
    # refine: centroid of the region where dt >= 0.6*peak within the same connected core
    core = dt >= 0.6 * dt[py, px]
    lab, n = ndi.label(core)
    li = lab[py, px]
    cy, cx = ndi.center_of_mass(lab == li)
    rows.append((px + X0, py + Y0, cx + X0, cy + Y0, dt[py, px]))
rows.sort(key=lambda t: t[1])
for px, py, cx, cy, d in rows:
    print(f"peak ({px:4d},{py:4d}) core-centroid ({cx:7.1f},{cy:7.1f}) inscribed radius {d:5.1f}px")
