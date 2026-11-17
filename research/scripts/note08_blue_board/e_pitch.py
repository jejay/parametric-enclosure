"""Header pitch in px from the soldermask gaps between adjacent round pads (top-surface features).
usage: e_pitch.py IMAGE
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

A = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32) / 255.0
blueness = A[..., 2] - 0.5 * (A[..., 0] + A[..., 1])

P0 = np.array([1414.2, 340.0]); P1 = np.array([1406.4, 1012.0])  # along the pad column (slightly tilted)
L = np.linalg.norm(P1 - P0)
d = (P1 - P0) / L
n = np.array([-d[1], d[0]])
ts = np.arange(0, L, 0.25)
for halfw in (3, 6, 9):
    offs = np.arange(-halfw, halfw + 0.1, 1.0)
    T, O = np.meshgrid(ts, offs)
    X = P0[0] + T * d[0] + O * n[0]
    Y = P0[1] + T * d[1] + O * n[1]
    prof = ndi.map_coordinates(blueness, [Y, X], order=1).mean(axis=0)
    sm = ndi.gaussian_filter1d(prof, 2.0)
    # gaps = local maxima of blueness above threshold
    thr = 0.5 * (np.percentile(sm, 95) + np.percentile(sm, 5))
    above = sm > thr
    lab, k = ndi.label(above)
    gaps = []
    for i in range(1, k + 1):
        idx = np.nonzero(lab == i)[0]
        w = sm[idx] - thr
        gaps.append((float((ts[idx] * w).sum() / w.sum()), float(ts[idx[-1]] - ts[idx[0]])))
    pos = np.array([g[0] for g in gaps])
    print(f"half-width {halfw}: {len(gaps)} blue segments along the column")
    print("   positions:", np.round(pos, 2).tolist())
    print("   widths   :", [round(g[1], 1) for g in gaps])
    if len(pos) >= 3:
        dd = np.diff(pos)
        print("   spacings :", np.round(dd, 2).tolist())
