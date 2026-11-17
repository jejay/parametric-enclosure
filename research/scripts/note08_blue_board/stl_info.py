"""Inspect an STL (untrusted data, parsed only): bounds, z-levels, horizontal slices.

usage: stl_info.py FILE.stl [z1 z2 ...]
For each z a horizontal section is taken and its closed loops are listed with
bounding box, centroid, area and an equivalent circle diameter.
"""
import sys
import numpy as np
import trimesh

path = sys.argv[1]
zs = [float(v) for v in sys.argv[2:]]
m = trimesh.load(path, force="mesh", process=True)
print("file", path)
print("vertices", len(m.vertices), "faces", len(m.faces), "watertight", m.is_watertight)
print("bounds", np.round(m.bounds, 4).tolist())
print("extents", np.round(m.extents, 4).tolist())
try:
    print("volume", round(float(m.volume), 3))
except Exception as e:  # noqa: BLE001
    print("volume err", e)

# distinct z levels of vertices (flat features)
zv = np.round(m.vertices[:, 2], 3)
vals, counts = np.unique(zv, return_counts=True)
print("distinct z levels (z: vertex count), top 40 by count:")
order = np.argsort(-counts)[:40]
for i in sorted(order, key=lambda k: vals[k]):
    print(f"  z={vals[i]:9.3f}  n={counts[i]}")

for axis, name in ((0, "x"), (1, "y")):
    v = np.round(m.vertices[:, axis], 3)
    vals, counts = np.unique(v, return_counts=True)
    order = np.argsort(-counts)[:30]
    print(f"distinct {name} levels, top 30 by count:")
    for i in sorted(order, key=lambda k: vals[k]):
        print(f"  {name}={vals[i]:9.3f}  n={counts[i]}")

for z in zs:
    print(f"--- section at z={z}")
    sec = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if sec is None:
        print("  (no section)")
        continue
    for k, ent in enumerate(sec.entities):
        pts = sec.vertices[ent.points][:, :2]
        closed = bool(ent.closed)
        mn, mx = pts.min(axis=0), pts.max(axis=0)
        # polygon area + centroid (shoelace)
        x, y = pts[:, 0], pts[:, 1]
        a = 0.5 * np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])
        if abs(a) > 1e-9:
            cx = np.sum((x[:-1] + x[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1])) / (6 * a)
            cy = np.sum((y[:-1] + y[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1])) / (6 * a)
        else:
            cx, cy = pts.mean(axis=0)
        deq = 2 * np.sqrt(abs(a) / np.pi)
        print(
            f"  loop {k:2d} closed={closed} n={len(pts):4d} "
            f"bbox x[{mn[0]:8.3f},{mx[0]:8.3f}] y[{mn[1]:8.3f},{mx[1]:8.3f}] "
            f"size {mx[0]-mn[0]:7.3f} x {mx[1]-mn[1]:7.3f} "
            f"centroid ({cx:8.3f},{cy:8.3f}) area {abs(a):9.3f} d_eq {deq:6.3f}"
        )
