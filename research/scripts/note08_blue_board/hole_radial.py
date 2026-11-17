"""Radial profiles of the mounting holes and header pads in a metric-rectified board image.

usage: hole_radial.py RECT_NPY cx cy [cx cy ...]   (mm, board frame)
For each centre the centre is refined (centroid of the non-blue blob), then the luminance,
saturation and blueness are averaged on rings of radius r. Prints the radius where
blueness crosses half level (outer edge of the plated ring / land) and the radius where the
bright bore ends (luminance drops below the bore plateau by 40% of the bore-to-ring step).
"""
import sys
import numpy as np
from scipy import ndimage as ndi

rect = np.load(sys.argv[1])
PPM, M = 20.0, 2.0
vals = [float(v) for v in sys.argv[2:]]
lum = rect.mean(axis=2)
blue = rect[..., 2] - 0.5 * (rect[..., 0] + rect[..., 1])
mx = rect.max(axis=2); mn = rect.min(axis=2)
sat = (mx - mn) / np.maximum(mx, 1e-6)
H, W = lum.shape
YY, XX = np.mgrid[0:H, 0:W]
for cx, cy in zip(vals[0::2], vals[1::2]):
    px, py = (cx + M) * PPM, (cy + M) * PPM
    h = 55
    x0, y0 = int(px) - h, int(py) - h
    w = blue[y0:y0 + 2 * h, x0:x0 + 2 * h] < 0.08
    w = ndi.binary_opening(w, structure=np.ones((3, 3), bool))
    lab, n = ndi.label(w)
    comp = ndi.binary_fill_holes(lab == lab[h, h])
    c = ndi.center_of_mass(comp)
    px, py = c[1] + x0, c[0] + y0
    rr = np.hypot(XX - px, YY - py)
    out = []
    radii = np.arange(0.0, 2.6 * PPM, 1.0)
    for r in radii:
        m = (rr >= r - 0.5) & (rr < r + 0.5)
        out.append((r / PPM, lum[m].mean(), sat[m].mean(), blue[m].mean(), lum[m].std()))
    out = np.array(out)
    r_mm, l_, s_, b_, sd = out.T
    # outer edge of metal: blueness half level
    blv = 0.5 * (b_[:10].mean() + b_[-6:].mean())
    k = np.nonzero((b_[:-1] < blv) & (b_[1:] >= blv))[0]
    r_out = r_mm[k[0]] + (blv - b_[k[0]]) / (b_[k[0] + 1] - b_[k[0]]) / PPM if len(k) else np.nan
    print(f"centre ({px/PPM - M:.3f},{py/PPM - M:.3f}) mm: metal outer radius {r_out:.3f} -> diameter {2*r_out:.3f} mm")
    print("    r(mm):lum/sat/blue  " + "  ".join(f"{a:.2f}:{b:.2f}/{c_:.2f}/{d:+.2f}" for a, b, c_, d, e in out[::2]))
