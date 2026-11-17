"""Homography analysis of the oblique PN5180 photo.

Reference A: the 4 mounting-hole ring centres with the raster taken from the lhm0 holder STL
             (34.0 mm pair and 25.0 mm pair, 37.0 mm apart, both centred on the same axis).
Check 1: header pads must come out collinear, perpendicular to the long axis, 2.54 mm pitch.
Check 2: the board outline must come out as a rectangle; its size is then an independent
         estimate of length x width, and gives the hole -> edge distances.

usage: k_homography.py [pair_distance_mm]
"""
import sys
import numpy as np

DX = float(sys.argv[1]) if len(sys.argv) > 1 else 37.0

# --- image measurements (source px of the upright photo) ---
holes_img = {
    "mid_far": (773.8, 1934.6),
    "mid_near": (1353.0, 2445.5),
    "ant_far": (1418.3, 1655.1),
    "ant_near": (1829.8, 1947.5),
}
holes_brd = {
    "mid_far": (0.0, -17.0),
    "mid_near": (0.0, 17.0),
    "ant_far": (DX, -12.5),
    "ant_near": (DX, 12.5),
}
pads_img = [
    (331.1, 2223.7), (370.4, 2263.9), (409.4, 2306.7), (451.6, 2348.6), (491.6, 2392.4),
    (533.7, 2437.4), (576.2, 2482.4), (620.1, 2529.0), (664.2, 2577.8), (709.5, 2624.0),
    (755.7, 2673.4), (804.0, 2724.0), (851.5, 2776.5),
]
# edge lines from k_measure.py (corner intersections of fitted silhouette lines) with the
# per-edge inward corrections found by edge_profile.py (px, towards board interior)
corners_fit = {"L": (215.0, 2186.2), "B": (872.7, 2899.3), "R": (2039.5, 1971.7), "T": (1407.6, 1529.1)}
edge_shift = {("L", "B"): 2.5, ("B", "R"): 3.0, ("R", "T"): 0.25, ("T", "L"): 1.0}


def homography(src, dst):
    A = []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y, -v])
    _, _, vt = np.linalg.svd(np.array(A, float))
    return vt[-1].reshape(3, 3)


def apply(H, pts):
    p = np.c_[np.array(pts, float), np.ones(len(pts))] @ H.T
    return p[:, :2] / p[:, 2:3]


names = list(holes_img)
H_img2brd = homography([holes_img[n] for n in names], [holes_brd[n] for n in names])

pads = apply(H_img2brd, pads_img)
print(f"== reference: hole raster 34/25/{DX} (lhm0 STL) ==")
print("pads in hole frame (u along board length from mid-hole pair, v across):")
for i, p in enumerate(pads, 1):
    print(f"  pad {i:2d}: u={p[0]:8.3f} v={p[1]:8.3f}")
d = np.diff(pads, axis=0)
pitch = np.hypot(d[:, 0], d[:, 1])
print("pitches:", np.round(pitch, 3).tolist())
print(f"mean pitch {pitch.mean():.4f} mm (expected 2.540); span 1..13 = {np.hypot(*(pads[-1]-pads[0])):.3f} (expected 30.480)")
# line fit u = a + b v
b, a = np.polyfit(pads[:, 1], pads[:, 0], 1)
print(f"pad row: u = {a:.3f} + {b:.5f} v  (tilt {np.degrees(np.arctan(b)):.3f} deg); row centre v = {pads[:,1].mean():.3f}")


def line_through(p, q):
    p = np.array(p, float); q = np.array(q, float)
    d = (q - p) / np.linalg.norm(q - p)
    return p, d


def shifted_edge(pk, qk, shift, interior_pt):
    p, d = line_through(corners_fit[pk], corners_fit[qk])
    n = np.array([-d[1], d[0]])
    if (np.array(interior_pt) - p) @ n < 0:
        n = -n
    return p + shift * n, d


def intersect(l1, l2):
    (c1, d1), (c2, d2) = l1, l2
    t = np.linalg.solve(np.array([d1, -d2]).T, c2 - c1)
    return c1 + t[0] * d1


centre_img = np.mean([corners_fit[k] for k in "LBRT"], axis=0)
E = {k: shifted_edge(k[0], k[1], s, centre_img) for k, s in edge_shift.items()}
C = {
    "L": intersect(E[("T", "L")], E[("L", "B")]),
    "B": intersect(E[("L", "B")], E[("B", "R")]),
    "R": intersect(E[("B", "R")], E[("R", "T")]),
    "T": intersect(E[("R", "T")], E[("T", "L")]),
}
cb = apply(H_img2brd, [C[k] for k in "LBRT"])
cbd = dict(zip("LBRT", cb))
print("corners (image px, top-surface corrected):", {k: np.round(v, 1).tolist() for k, v in C.items()})
print("corners in hole frame:")
for k in "LBRT":
    print(f"  {k}: u={cbd[k][0]:8.3f} v={cbd[k][1]:8.3f}")
len_far = np.hypot(*(cbd["T"] - cbd["L"]))
len_near = np.hypot(*(cbd["R"] - cbd["B"]))
wid_hdr = np.hypot(*(cbd["B"] - cbd["L"]))
wid_ant = np.hypot(*(cbd["R"] - cbd["T"]))
print(f"length: far edge {len_far:.2f}, near edge {len_near:.2f}; width: header end {wid_hdr:.2f}, antenna end {wid_ant:.2f}")
# edges as lines in hole frame
u_hdr = 0.5 * (cbd["L"][0] + cbd["B"][0]); u_ant = 0.5 * (cbd["T"][0] + cbd["R"][0])
v_far = 0.5 * (cbd["L"][1] + cbd["T"][1]); v_near = 0.5 * (cbd["B"][1] + cbd["R"][1])
print(f"header-end edge u = {u_hdr:.2f} (L {cbd['L'][0]:.2f}, B {cbd['B'][0]:.2f}); antenna-end edge u = {u_ant:.2f} (T {cbd['T'][0]:.2f}, R {cbd['R'][0]:.2f})")
print(f"far long edge v = {v_far:.2f} (L {cbd['L'][1]:.2f}, T {cbd['T'][1]:.2f}); near long edge v = {v_near:.2f} (B {cbd['B'][1]:.2f}, R {cbd['R'][1]:.2f})")
print(f"=> board length {u_ant-u_hdr:.2f}, width {v_near-v_far:.2f}")
print(f"=> mid hole pair x from header edge {0-u_hdr:.2f}; antenna pair x from header edge {DX-u_hdr:.2f}; antenna pair to antenna-end edge {u_ant-DX:.2f}")
print(f"=> hole-pattern centre line vs board centre line: {0.5*(v_far+v_near):+.2f} (0 = centred)")
print(f"=> mid holes to long edges: far {-17 - v_far:.2f}, near {v_near - 17:.2f}; antenna holes to long edges: far {-12.5 - v_far:.2f}, near {v_near - 12.5:.2f}")
print(f"=> header row from header-end edge: {a - u_hdr:.2f} (row at u={a:.2f})")
print(f"=> pad1 from far long edge (y of pin 1): {pads[0,1]-v_far:.2f}; pad13 from near long edge: {v_near - pads[-1,1]:.2f}")

# --- alternative reference B: outline 70 x 39 from the 4 corrected corners ---
print()
print("== alternative reference: outline corners = 70.0 x 39.0 ==")
H2 = homography([C[k] for k in "LBRT"], [(0, 0), (0, 39), (70, 39), (70, 0)])
hp = apply(H2, [holes_img[n] for n in names])
for n, p in zip(names, hp):
    print(f"  hole {n:9s}: x={p[0]:7.3f} y={p[1]:7.3f}")
hd = dict(zip(names, hp))
print(f"  mid pair spacing {np.hypot(*(hd['mid_near']-hd['mid_far'])):.2f}; antenna pair spacing {np.hypot(*(hd['ant_near']-hd['ant_far'])):.2f}; "
      f"pair distance {0.5*(hd['ant_far'][0]+hd['ant_near'][0]) - 0.5*(hd['mid_far'][0]+hd['mid_near'][0]):.2f}")
pp = apply(H2, pads_img)
d2 = np.diff(pp, axis=0)
print("  pad pitches:", np.round(np.hypot(d2[:, 0], d2[:, 1]), 3).tolist())
print(f"  mean pitch {np.hypot(d2[:,0], d2[:,1]).mean():.4f}; pad row x mean {pp[:,0].mean():.3f} (min {pp[:,0].min():.3f}, max {pp[:,0].max():.3f}); pad1 y {pp[0,1]:.3f}; pad13 y {pp[-1,1]:.3f}")

np.save(sys.argv[2], H_img2brd) if len(sys.argv) > 2 else None
