"""Inspect a STEP file (untrusted data; geometry is parsed only, nothing is executed).

usage: step_info.py FILE.step [--planes] [--minr R] [--maxr R]
Prints solids with bounding boxes, cylindrical faces (radius, axis, extent) and optionally
axis-aligned planar faces (position + bbox).
"""
import sys
import math
import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane

path = sys.argv[1]
show_planes = "--planes" in sys.argv
minr = float(sys.argv[sys.argv.index("--minr") + 1]) if "--minr" in sys.argv else 0.0
maxr = float(sys.argv[sys.argv.index("--maxr") + 1]) if "--maxr" in sys.argv else 1e9

wp = cq.importers.importStep(path)
solids = wp.solids().vals()
print("file", path)
print("solids:", len(solids))
for i, s in enumerate(solids):
    bb = s.BoundingBox()
    print(f" solid {i}: x[{bb.xmin:.3f},{bb.xmax:.3f}] y[{bb.ymin:.3f},{bb.ymax:.3f}] z[{bb.zmin:.3f},{bb.zmax:.3f}] "
          f"size {bb.xlen:.3f} x {bb.ylen:.3f} x {bb.zlen:.3f} vol {s.Volume():.1f}")

for si, s in enumerate(solids):
    cyls = []
    planes = []
    for f in s.Faces():
        ad = BRepAdaptor_Surface(f.wrapped)
        t = ad.GetType()
        bb = f.BoundingBox()
        if t == GeomAbs_Cylinder:
            c = ad.Cylinder()
            ax = c.Axis()
            loc, d = ax.Location(), ax.Direction()
            cyls.append((round(c.Radius(), 4), round(loc.X(), 3), round(loc.Y(), 3), round(loc.Z(), 3),
                         round(d.X(), 3), round(d.Y(), 3), round(d.Z(), 3),
                         round(bb.xmin, 3), round(bb.xmax, 3), round(bb.ymin, 3), round(bb.ymax, 3),
                         round(bb.zmin, 3), round(bb.zmax, 3), f.wrapped.Orientation().name))
        elif t == GeomAbs_Plane and show_planes:
            p = ad.Plane()
            n = p.Axis().Direction()
            planes.append((round(n.X(), 3), round(n.Y(), 3), round(n.Z(), 3),
                           round(bb.xmin, 3), round(bb.xmax, 3), round(bb.ymin, 3), round(bb.ymax, 3),
                           round(bb.zmin, 3), round(bb.zmax, 3), round(f.Area(), 2)))
    print(f"--- solid {si}: {len(cyls)} cylindrical faces")
    seen = set()
    for c in sorted(cyls):
        if not (minr <= c[0] <= maxr):
            continue
        key = c[:13]
        if key in seen:
            continue
        seen.add(key)
        r, lx, ly, lz, dx, dy, dz, x0, x1, y0, y1, z0, z1, ori = c
        print(f"  cyl r={r:7.3f} (d={2*r:7.3f}) axis@({lx:8.3f},{ly:8.3f},{lz:8.3f}) dir({dx:5.2f},{dy:5.2f},{dz:5.2f}) "
              f"bbox x[{x0:8.3f},{x1:8.3f}] y[{y0:8.3f},{y1:8.3f}] z[{z0:7.3f},{z1:7.3f}] {ori}")
    if show_planes:
        print(f"--- solid {si}: {len(planes)} planar faces")
        for p in sorted(planes, key=lambda t: (t[0], t[1], t[2], t[7], t[3], t[5])):
            nx, ny, nz, x0, x1, y0, y1, z0, z1, area = p
            print(f"  plane n({nx:5.2f},{ny:5.2f},{nz:5.2f}) x[{x0:8.3f},{x1:8.3f}] y[{y0:8.3f},{y1:8.3f}] z[{z0:7.3f},{z1:7.3f}] area {area}")
