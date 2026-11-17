"""Lower and upper silhouette of the puck base in a front view, and ellipse fits restricted to the flanks.

Usage: python -I puck_profile.py IMG SEED_X Y0:Y1 [U_MIN U_MAX]
The puck silhouette is taken as the opaque dark region connected to the puck rows. For each column the
lowest and highest dark pixel are found. Outside the nameplate (|u| = |x-cx|/a between U_MIN and U_MAX)
the lower silhouette is the front arc of the footprint circle:  y = yc + b*sqrt(1-u^2), b = a*sin(elev).
Prints the fit and the deviation of the lower silhouette from that ellipse across the whole width
(positive = silhouette lower than the circle = something protrudes towards the camera).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import mcommon as mc
from rowruns import run_extent

path, seed = sys.argv[1], int(sys.argv[2])
y0, y1 = (int(v) for v in sys.argv[3].split(":"))
umin = float(sys.argv[4]) if len(sys.argv) > 4 else 0.74
umax = float(sys.argv[5]) if len(sys.argv) > 5 else 0.97
a = mc.load_rgba(path)
r, g, b, al, sat, lum = mc.channels(a)
val = np.maximum(np.maximum(r, g), b)
rows = []
for y in range(y0, y1 + 1):
    e = run_extent(lum, sat, al, y, seed, level=170.0, maxsat=0.25)
    if e is not None:
        rows.append((y, e[0], e[1]))
rows = np.array(rows)
wd = rows[:, 2] - rows[:, 1]
sel = wd > wd.max() - 1.0
xl, xr = float(np.median(rows[sel, 1])), float(np.median(rows[sel, 2]))
cx, aa = 0.5 * (xl + xr), 0.5 * (xr - xl)
dark = (al >= 250) & (val < 125) & (sat < 0.35)
low, up = {}, {}
for x in range(int(xl) + 1, int(xr)):
    col = np.nonzero(dark[:, x])[0]
    col = col[(col > y0 - 1.2 * aa) & (col < y1 + 1.2 * aa)]
    if len(col) < 5:
        continue
    yb = col[-1]
    # sub-pixel lower edge from the alpha ramp just below
    frac = al[yb + 1, x] / 255.0 if yb + 1 < al.shape[0] else 0.0
    low[x] = yb + 0.5 + frac
    # highest pixel of the contiguous dark run ending at yb
    s = set(col.tolist()); yt = yb
    while yt - 1 in s:
        yt -= 1
    up[x] = yt - 0.5
xs = np.array(sorted(low))
u = (xs - cx) / aa
ylow = np.array([low[x] for x in xs])
m = (np.abs(u) > umin) & (np.abs(u) < umax)
A = np.column_stack([np.ones(m.sum()), np.sqrt(1 - u[m] ** 2)])
(yc, bb), *_ = np.linalg.lstsq(A, ylow[m], rcond=None)
res = ylow[m] - A @ np.array([yc, bb])
elev = np.degrees(np.arcsin(bb / aa))
print(f"{os.path.basename(path)}: puck x {xl:.1f}..{xr:.1f} a={aa:.2f}px | flank fit |u| in [{umin},{umax}]: yc={yc:.2f} b={bb:.2f} "
      f"-> elevation {elev:.2f} deg (rms {np.sqrt(np.mean(res ** 2)):.2f} px, n={m.sum()})")
dev = ylow - (yc + bb * np.sqrt(np.clip(1 - u ** 2, 0, 1)))
print("  lower silhouette minus footprint ellipse [px] at u = ", " ".join(f"{uu:+.2f}:{np.median(dev[np.abs(u - uu) < 0.03]):+.1f}" for uu in np.arange(-0.9, 0.91, 0.1)))
s_px = 2 * aa / 45.0
print(f"  -> as a forward protrusion in mm (dev / (sin(elev) * px_per_mm), D=45): ", " ".join(
    f"{uu:+.2f}:{np.median(dev[np.abs(u - uu) < 0.03]) / (np.sin(np.radians(elev)) * s_px):+.1f}" for uu in np.arange(-0.7, 0.71, 0.1)))
# vertical side: rows where the left edge is within 0.6 px of xl
side = rows[np.abs(rows[:, 1] - xl) < 0.8]
print(f"  left side straight from y={side[:, 0].min():.0f} to y={side[:, 0].max():.0f}; footprint centre row from fit yc={yc:.1f}; "
      f"height of the straight side = {(yc - side[:, 0].min()) / (np.cos(np.radians(elev)) * s_px):.2f} mm (below the top fillet)")
