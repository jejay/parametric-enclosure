"""Locate an edge across a straightened strip, numerically.

usage: edge_profile.py IN px py qx qy halfwidth nseg [channel-mode]
For nseg segments along P->Q, average the strip over the segment and print, per offset
(1 px steps, + = towards normal n=(dy,-dx)), mean R,G,B and a 'blueness' b-(r+g)/2.
Then report the offset of the steepest blueness drop (interior -> exterior) per segment.
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src = sys.argv[1]
px, py, qx, qy, hw = (float(v) for v in sys.argv[2:7])
nseg = int(sys.argv[7])
im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
P = np.array([px, py]); Q = np.array([qx, qy])
L = np.linalg.norm(Q - P)
d = (Q - P) / L
n = np.array([d[1], -d[0]])
ts = np.arange(0, L, 1.0)
offs = np.arange(hw, -hw - 1e-6, -0.5)
T, O = np.meshgrid(ts, offs)
X = P[0] + T * d[0] + O * n[0]
Y = P[1] + T * d[1] + O * n[1]
st = np.stack([ndi.map_coordinates(im[..., c], [Y, X], order=1, mode="nearest") for c in range(3)], axis=-1)
bl = st[..., 2] - 0.5 * (st[..., 0] + st[..., 1])
lum = st.mean(axis=-1)
edges_t = np.linspace(0.06 * L, 0.94 * L, nseg + 1)
print(f"length {L:.1f}px; offsets + = interior if n points inward; n={n.round(4).tolist()}")
res = []
for i in range(nseg):
    a, b = int(edges_t[i]), int(edges_t[i + 1])
    pb = np.median(bl[:, a:b], axis=1)
    pl = np.median(lum[:, a:b], axis=1)
    sm = ndi.gaussian_filter1d(pb, 1.5)
    g = np.gradient(sm)  # along decreasing offset (rows go +hw -> -hw)
    k = int(np.argmin(g))  # steepest drop of blueness going outward
    res.append((0.5 * (a + b), offs[k], g[k]))
    prof = " ".join(f"{offs[j]:+.0f}:{pb[j]:.0f}/{pl[j]:.0f}" for j in range(0, len(offs), 4))
    print(f"seg {i} t[{a},{b}] steepest blueness drop at offset {offs[k]:+.1f} (grad {g[k]:.1f})")
    print("   blueness/lum profile:", prof)
tt = np.array([r[0] for r in res]); oo = np.array([r[1] for r in res])
print("offsets per segment:", np.round(oo, 1).tolist())
print(f"median offset {np.median(oo):+.2f}")
