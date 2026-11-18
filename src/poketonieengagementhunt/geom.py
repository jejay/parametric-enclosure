"""Small geometry helpers on top of CadQuery/OCP.

Conventions used in the whole package
-------------------------------------
* Units are millimetres.
* The ball centre is the origin.  +X is the FRONT (button), -X the BACK
  (hinge), +Z is UP (red half), +Y is the ball's left side.
* All helpers return ``cq.Shape`` objects (not Workplanes) so that parts can
  be combined, moved and measured uniformly.
"""

from __future__ import annotations

import math
from typing import Iterable, Sequence

import cadquery as cq
from OCP.BRepExtrema import BRepExtrema_DistShapeShape

Shape = cq.Shape


# --------------------------------------------------------------------------
# construction primitives
# --------------------------------------------------------------------------
def _val(obj) -> Shape:
    if isinstance(obj, cq.Workplane):
        vals = obj.vals()
        if len(vals) == 1:
            return vals[0]
        return cq.Compound.makeCompound(vals)
    return obj


def box(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> Shape:
    """Axis-aligned box given by its extents."""
    return cq.Solid.makeBox(
        x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0), cq.Vector(0, 0, 1)
    )


def rbox(x0, x1, y0, y1, z0, z1, r: float, axis: str = "z") -> Shape:
    """Box with the four edges parallel to ``axis`` rounded with radius r."""
    b = cq.Workplane(obj=box(x0, x1, y0, y1, z0, z1))
    sel = {"z": "|Z", "x": "|X", "y": "|Y"}[axis]
    r = min(r, 0.49 * min(d for d, a in (((x1 - x0), "x"), ((y1 - y0), "y"), ((z1 - z0), "z")) if a != axis))
    return _val(b.edges(sel).fillet(r))


def cyl_z(r: float, z0: float, z1: float, x: float = 0.0, y: float = 0.0) -> Shape:
    return cq.Solid.makeCylinder(r, z1 - z0, cq.Vector(x, y, z0), cq.Vector(0, 0, 1))


def cyl_x(r: float, x0: float, x1: float, y: float = 0.0, z: float = 0.0) -> Shape:
    return cq.Solid.makeCylinder(r, x1 - x0, cq.Vector(x0, y, z), cq.Vector(1, 0, 0))


def cyl_y(r: float, y0: float, y1: float, x: float = 0.0, z: float = 0.0) -> Shape:
    return cq.Solid.makeCylinder(r, y1 - y0, cq.Vector(x, y0, z), cq.Vector(0, 1, 0))


def cone_x(r0: float, r1: float, x0: float, x1: float, y: float = 0.0, z: float = 0.0) -> Shape:
    """Frustum along +X with radius r0 at x0 and r1 at x1."""
    return cq.Solid.makeCone(r0, r1, x1 - x0, cq.Vector(x0, y, z), cq.Vector(1, 0, 0))


def cone_y(r0: float, r1: float, y0: float, y1: float, x: float = 0.0, z: float = 0.0) -> Shape:
    """Frustum along +Y with radius r0 at y0 and r1 at y1."""
    return cq.Solid.makeCone(r0, r1, y1 - y0, cq.Vector(x, y0, z), cq.Vector(0, 1, 0))


def cone_z(r0: float, r1: float, z0: float, z1: float, x: float = 0.0, y: float = 0.0) -> Shape:
    return cq.Solid.makeCone(r0, r1, z1 - z0, cq.Vector(x, y, z0), cq.Vector(0, 0, 1))


def sphere(r: float, centre: Sequence[float] = (0, 0, 0)) -> Shape:
    # NB: CadQuery's default latitude range is 0..90 deg (a hemisphere); a full
    # ball needs the explicit -90..90 range.
    s = cq.Solid.makeSphere(r, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), -90.0, 90.0, 360.0)
    return s.translate(cq.Vector(*centre)) if any(centre) else s


def slab(z0: float, z1: float, r: float = 500.0) -> Shape:
    """A very wide disc between two heights, used to clip by Z."""
    return cyl_z(r, z0, z1)


def ball_zone(r_out: float, r_in: float, z0: float, z1: float) -> Shape:
    """Spherical shell between two radii, clipped to z0..z1."""
    shell = sphere(r_out)
    if r_in > 0:
        shell = shell.cut(sphere(r_in))
    return shell.intersect(slab(z0, z1))


def torus_x(r_major: float, r_minor: float, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Shape:
    """Torus whose axis is the X direction."""
    return cq.Solid.makeTorus(r_major, r_minor, cq.Vector(x, y, z), cq.Vector(1, 0, 0))


def torus_y(r_major: float, r_minor: float, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Shape:
    return cq.Solid.makeTorus(r_major, r_minor, cq.Vector(x, y, z), cq.Vector(0, 1, 0))


def prism_xz(points: Sequence[tuple[float, float]], y0: float, y1: float) -> Shape:
    """Extrude a closed (x, z) polygon along Y from y0 to y1."""
    wp = cq.Workplane("XZ").polyline(list(points)).close().extrude(-(y1 - y0))
    return _val(wp).translate(cq.Vector(0, y0, 0))


def prism_xy(points: Sequence[tuple[float, float]], z0: float, z1: float) -> Shape:
    """Extrude a closed (x, y) polygon along Z from z0 to z1."""
    wp = cq.Workplane("XY").polyline(list(points)).close().extrude(z1 - z0)
    return _val(wp).translate(cq.Vector(0, 0, z0))


def prism_yz(points: Sequence[tuple[float, float]], x0: float, x1: float) -> Shape:
    """Extrude a closed (y, z) polygon along X from x0 to x1."""
    wp = cq.Workplane("YZ").polyline(list(points)).close().extrude(x1 - x0)
    return _val(wp).translate(cq.Vector(x0, 0, 0))


def revolve_z(points: Sequence[tuple[float, float]], angle: float = 360.0) -> Shape:
    """Revolve a closed (r, z) polygon about the Z axis."""
    wp = cq.Workplane("XZ").polyline(list(points)).close().revolve(angle, (0, 0, 0), (0, 1, 0))
    return _val(wp)


# --------------------------------------------------------------------------
# boolean helpers
# --------------------------------------------------------------------------
def clean(shape: Shape) -> Shape:
    """Merge coplanar / co-cylindrical faces.  OCC's face unifier occasionally
    fails on valid input; the un-merged shape is then returned unchanged."""
    try:
        out = shape.clean()
        return out if out.isValid() else shape
    except Exception:
        return shape


def union(*shapes: Shape | None) -> Shape:
    items = [s for s in shapes if s is not None]
    out = items[0]
    for s in items[1:]:
        out = out.fuse(s)
    return clean(out)


def cut(base: Shape, *tools: Shape | None) -> Shape:
    out = base
    for t in tools:
        if t is not None:
            out = out.cut(t)
    return clean(out)


def inter(a: Shape, b: Shape) -> Shape:
    return clean(a.intersect(b))


def compound(shapes: Iterable[Shape]) -> Shape:
    return cq.Compound.makeCompound(list(shapes))


# --------------------------------------------------------------------------
# placement helpers
# --------------------------------------------------------------------------
def move(shape: Shape, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0) -> Shape:
    return shape.translate(cq.Vector(dx, dy, dz))


def rot(shape: Shape, axis: str, deg: float, centre: Sequence[float] = (0, 0, 0)) -> Shape:
    """Rotate about a line through ``centre`` parallel to a coordinate axis.

    Positive angles follow the right-hand rule about the positive axis.
    """
    c = cq.Vector(*centre)
    d = {"x": cq.Vector(1, 0, 0), "y": cq.Vector(0, 1, 0), "z": cq.Vector(0, 0, 1)}[axis]
    return shape.rotate(c, c + d, deg)


def mirror_y(shape: Shape) -> Shape:
    return shape.mirror("XZ")


# --------------------------------------------------------------------------
# measurements
# --------------------------------------------------------------------------
def volume(shape: Shape | None) -> float:
    if shape is None:
        return 0.0
    try:
        return float(shape.Volume())
    except Exception:
        return 0.0


def solids(shape: Shape) -> list[Shape]:
    return list(shape.Solids())


def bbox(shape: Shape):
    return shape.BoundingBox()


def bbox_overlap(a: Shape, b: Shape, margin: float = 0.0) -> bool:
    A, B = a.BoundingBox(), b.BoundingBox()
    return not (
        A.xmax + margin < B.xmin
        or B.xmax + margin < A.xmin
        or A.ymax + margin < B.ymin
        or B.ymax + margin < A.ymin
        or A.zmax + margin < B.zmin
        or B.zmax + margin < A.zmin
    )


def common_volume(a: Shape, b: Shape) -> float:
    """Volume shared by two shapes (0 when they only touch)."""
    if not bbox_overlap(a, b):
        return 0.0
    try:
        c = a.intersect(b)
    except Exception:
        return float("nan")
    return sum(volume(s) for s in c.Solids())


def min_distance(a: Shape, b: Shape) -> float:
    d = BRepExtrema_DistShapeShape(a.wrapped, b.wrapped)
    d.Perform()
    return float(d.Value())


def centre_of_mass(shape: Shape) -> tuple[float, float, float]:
    c = cq.Shape.centerOfMass(shape)
    return (c.x, c.y, c.z)


def polar(r: float, deg: float) -> tuple[float, float]:
    return (r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))
