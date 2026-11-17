"""Printed parts of the grass tongue (revision 3).

grass_base    dark green tray: a tongue in front of the ball whose rear end
              lies under the ball's belly; it holds the reader board
grass_top     dark green turf plate that closes the tray; its top is the
              plain surface on which a Tonie stands
grass_blades  the tufts of grass, in a brighter green, printed onto the turf
grass_spot    the marker of the standing spot: a disc in the same brighter
              green, printed flush into the turf

Turf, blades and spot are one print job; they are kept as three bodies so
that a multi-colour slicer can give each its filament.

All parts are returned in assembly coordinates (see geom.py).  The underside
of the tongue lies in the plane of the ball's flat: ball and tongue stand on
the table together.  Nothing of the tongue reaches round the ball.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from functools import lru_cache

import cadquery as cq

from . import geom as g
from . import params as P

BLUE_X0 = P.SPOT_X - P.BLUE_ANT_X            # x of the reader board's header-end edge
BLUE_X1 = BLUE_X0 + P.BLUE_L                 # x of its antenna-end edge
POCKET = (BLUE_X0 - P.BLUE_CL_X, BLUE_X1 + P.BLUE_CL_X, P.BLUE_W / 2 + P.BLUE_CL_Y)   # x0, x1, half width
HALL_SEAT_Z = P.Z_TRAY_FLOOR                 # the hall switch lies on the floor of the pocket
RHO_TURF = math.sqrt((P.R + P.CUP_GAP) ** 2 - P.Z_TURF**2)   # where the turf surface meets the ball
GRASS_EDGE = P.EDGE_CHAMFER + 0.3            # grass keeps this far from the rim of the turf


# --------------------------------------------------------------------------
# plan outline and fasteners
# --------------------------------------------------------------------------
def plan(z0: float, z1: float) -> cq.Shape:
    """Prism of the tongue's outline: straight sides, round tip, rear corners cut off at 45 degrees."""
    w, xs, x0, c = P.TONGUE_W, P.SPOT_X, P.X_REAR, P.REAR_CHAMFER
    body = g.prism_xy([(x0, -w + c), (x0 + c, -w), (xs, -w), (xs, w), (x0 + c, w), (x0, w - c)], z0, z1)
    return g.clean(body.fuse(g.cyl_z(w, z0, z1, xs, 0.0)))


def in_plan(x: float, y: float, margin: float = 0.0) -> bool:
    """Inside the tongue's outline, ``margin`` away from its edge."""
    w = P.TONGUE_W
    if x >= P.SPOT_X:
        return math.hypot(x - P.SPOT_X, y) <= w - margin
    if x < P.X_REAR + margin or abs(y) > w - margin:
        return False
    return ((x - P.X_REAR) + (w - abs(y)) - P.REAR_CHAMFER) / math.sqrt(2.0) >= margin      # the cut-off rear corner


def _chamfered(shape: cq.Shape, selector: str) -> cq.Shape:
    try:
        out = cq.Workplane(obj=shape).edges(selector).chamfer(P.EDGE_CHAMFER).val()
        return out if out.isValid() else shape
    except Exception:
        return shape


def base_screw_xy() -> list[tuple[float, float]]:
    """The four M3 screws that hold the tongue under the lower front of the bowl."""
    return [g.polar(P.BASE_SCREW_RHO, az) for az in P.BASE_SCREW_AZ]


def turf_screw_xy() -> list[tuple[float, float]]:
    """The small screws that hold the turf on the tray.  Each one ends in the
    root of a grass tuft, so nothing shows on top."""
    return list(P.TURF_SCREW_XY)


def cable_window() -> cq.Shape:
    """Annular sector cut through the bowl wall for the reader harness."""
    half = P.WINDOW_HALF_DEG
    sector = g.revolve_z(
        [(P.WINDOW_R0, P.Z_FLAT - 1.0), (P.WINDOW_R1, P.Z_FLAT - 1.0), (P.WINDOW_R1, -30.0), (P.WINDOW_R0, -30.0)], 2 * half
    )
    return g.rot(sector, "z", -half)


# --------------------------------------------------------------------------
# grass: tufts scattered at random
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class Blade:
    x: float
    y: float
    h: float           # height above the turf
    w: float           # root width (along the fan of its tuft)
    t: float           # root thickness
    yaw: float         # direction of the blade's local +Y (the side it leans to), deg from +X
    lean: float        # lean towards local +Y, deg
    tilt: float = 0.0  # sideways tilt along local +X, deg (the fan of a tuft)
    sway: float = 0.0  # extra sideways curl of the tip, mm
    slim: float = 0.0  # 0 = broad leaf, 1 = narrow leaf
    hub: bool = False  # its root takes a turf screw


@dataclass(frozen=True)
class Mound:
    """Low solid hump from which the blades of one tuft grow."""

    x: float
    y: float
    out_deg: float     # the long axis points 90 deg clockwise from this direction
    a: float           # half length
    b: float           # half width


@dataclass(frozen=True)
class Tuft:
    mound: Mound
    blades: tuple[Blade, ...]


# (height fraction, width factor, thickness factor, narrowing of a slim leaf):
# a broad, lance-shaped leaf, widest in its lower third, blunt tip (research/10 A)
_PROFILE = ((0.0, 0.80, 1.0, 0.0), (0.25, 1.0, 0.86, 0.15), (0.52, 0.88, 0.68, 0.30), (0.80, 0.54, 0.48, 0.35), (1.0, 0.0, 0.0, 0.0))
_TIP_A, _TIP_B = P.BLADE_TIP


def _axes(yaw_deg: float) -> tuple[tuple[float, float], tuple[float, float]]:
    yaw = math.radians(yaw_deg)
    return (math.sin(yaw), -math.cos(yaw)), (math.cos(yaw), math.sin(yaw))     # local X and Y in plan


def _section(b: Blade, s: float) -> tuple[float, float, float, float, float]:
    """Half width, half thickness, offsets along local X and Y, and height of a blade section."""
    fw = ft = 0.0
    for (s0, w0, t0, k0), (s1, w1, t1, k1) in zip(_PROFILE, _PROFILE[1:]):
        if s0 <= s <= s1:
            f = (s - s0) / (s1 - s0)
            fw = (w0 + f * (w1 - w0)) * (1.0 - b.slim * (k0 + f * (k1 - k0)))
            ft = t0 + f * (t1 - t0)
            break
    z = s * b.h
    dx = math.tan(math.radians(b.tilt)) * z + b.sway * s * s
    dy = math.tan(math.radians(b.lean)) * z
    return max(b.w / 2 * fw, _TIP_A), max(b.t / 2 * ft, _TIP_B), dx, dy, z


def _samples(b: Blade, heights: tuple[float, ...]) -> list[tuple[float, float, float]]:
    """Points on the centre line and on both edges of a blade at the given height fractions."""
    ex, ey = _axes(b.yaw)
    pts = []
    for s in heights:
        a, _, dx, dy, z = _section(b, s)
        cx, cy = b.x + ex[0] * dx + ey[0] * dy, b.y + ex[1] * dx + ey[1] * dy
        pts += [(cx + ex[0] * u, cy + ex[1] * u, z) for u in (-a, 0.0, a)]
    return pts


def _root_points(b: Blade) -> list[tuple[float, float]]:
    ex, ey = _axes(b.yaw)
    a, th = 0.8 * b.w / 2, b.t / 2
    return [(b.x + ex[0] * u + ey[0] * v, b.y + ex[1] * u + ey[1] * v) for u, v in ((0, 0), (a, 0), (-a, 0), (0, th), (0, -th))]


def blade_ball_gap(b: Blade) -> float:
    """Least distance between a blade and the ball (analytic estimate used
    while laying the blades out; the verification measures the real solids)."""
    ex, ey = _axes(b.yaw)
    worst = 1e9
    for i in range(21):
        a, th, dx, dy, z = _section(b, i / 20)
        cx, cy = b.x + ex[0] * dx + ey[0] * dy, b.y + ex[1] * dx + ey[1] * dy
        rho = math.hypot(cx, cy)
        if rho < 1e-6:
            return -P.R
        ux, uy = -cx / rho, -cy / rho                                            # towards the ball's axis
        extent = math.hypot(a * (ux * ex[0] + uy * ex[1]), th * (ux * ey[0] + uy * ey[1]))
        worst = min(worst, math.hypot(rho - extent, P.Z_TURF + z) - P.R)
    return worst


def _with_height(b: Blade, h: float) -> Blade:
    return Blade(b.x, b.y, h, b.w, b.t, b.yaw, b.lean, b.tilt, b.sway, b.slim, b.hub)


def _fit(b: Blade) -> Blade:
    """Shorten a blade until it keeps BLADE_GAP to the ball."""
    h = b.h
    while h > 2.5 and blade_ball_gap(_with_height(b, h)) < P.BLADE_GAP + 0.3:
        h -= 0.25
    return _with_height(b, h)


def front_angle(x: float, y: float) -> float:
    """Angle between straight ahead and the direction from the spot centre to a point, deg."""
    return math.degrees(math.atan2(abs(y), x - P.SPOT_X))


def grass_free(x: float, y: float, edge: float, zone: float, ball: float) -> bool:
    """Grass may be here: on the turf (``edge`` inside its rim, ``ball`` away
    from the ball), ``zone`` outside the bare ground round the standing spot,
    and not in the open front."""
    if math.hypot(x - P.SPOT_X, y) < P.SPOT_CLEAR_R + zone:
        return False
    if front_angle(x, y) < P.FRONT_OPEN_DEG + 1.0:
        return False
    return in_plan(x, y, edge) and math.hypot(x, y) >= RHO_TURF + ball


def _mound_frame(m: Mound, x: float, y: float) -> tuple[float, float]:
    ang = math.radians(m.out_deg - 90.0)
    dx, dy = x - m.x, y - m.y
    return dx * math.cos(ang) + dy * math.sin(ang), -dx * math.sin(ang) + dy * math.cos(ang)


def _in_mound(m: Mound, x: float, y: float, grow: float = 0.0) -> bool:
    u, v = _mound_frame(m, x, y)
    return (u / (m.a + grow)) ** 2 + (v / (m.b + grow)) ** 2 < 1.0


def mound_outline(m: Mound, n: int = 24, grow: float = 0.0) -> list[tuple[float, float]]:
    ang = math.radians(m.out_deg - 90.0)
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    for i in range(n):
        u, v = (m.a + grow) * math.cos(2 * math.pi * i / n), (m.b + grow) * math.sin(2 * math.pi * i / n)
        pts.append((m.x + u * ca - v * sa, m.y + u * sa + v * ca))
    return pts


def _mound_ok(m: Mound, lawn: list[Tuft]) -> bool:
    """The whole mound stands on free turf and does not run into another mound."""
    if not all(grass_free(x, y, GRASS_EDGE, 0.2, 3.0) for x, y in mound_outline(m)):
        return False
    for other in lawn:
        o = other.mound
        if math.hypot(m.x - o.x, m.y - o.y) > m.a + o.a + 1.5:
            continue
        if any(_in_mound(o, x, y, 0.8) for x, y in mound_outline(m) + [(m.x, m.y)]):
            return False
        if any(_in_mound(m, x, y, 0.8) for x, y in mound_outline(o) + [(o.x, o.y)]):
            return False
    return True


def _blade_ok(b: Blade, lawn: list[Tuft]) -> bool:
    """Root on free turf; the leaf stays over the tongue, out of the bare
    ground and the open front, and clear of the leaves of other tufts."""
    if b.h < 4.5 or blade_ball_gap(b) < P.BLADE_GAP + 0.3:
        return False
    if not all(grass_free(x, y, GRASS_EDGE, 0.2, 2.0) for x, y in _root_points(b)):
        return False
    upper = _samples(b, (0.3, 0.55, 0.8, 1.0))
    for x, y, _ in upper:
        if not in_plan(x, y) or math.hypot(x - P.SPOT_X, y) < P.SPOT_CLEAR_R + 0.3 or front_angle(x, y) < P.FRONT_OPEN_DEG + 1.0:
            return False
    for other in lawn:
        if math.hypot(b.x - other.mound.x, b.y - other.mound.y) > 30.0:
            continue
        for ob in other.blades:
            for x, y, _ in _samples(ob, (0.55, 0.8, 1.0)):
                if any(math.hypot(x - u, y - v) < 2.2 for u, v, _ in upper[3:]):
                    return False
    return True


def _draw_size(rnd: random.Random, hub: bool) -> tuple[float, int]:
    """Height of the main leaf and number of leaves; tall tufts tend to have more leaves."""
    h = rnd.triangular(P.BLADE_H[0], P.BLADE_H[1], P.BLADE_H[2])
    n = max(2, min(7, round(h / 3.4 + rnd.uniform(-1.3, 1.3))))
    return (max(h, 9.0), max(n, 3)) if hub else (h, n)


def _grow(rnd: random.Random, x: float, y: float, h: float, n: int, hub: bool, lawn: list[Tuft]) -> Tuft | None:
    """Try one tuft of the given size at (x, y); direction, spread and leaf
    shape are drawn at random."""
    fan = rnd.uniform(0.0, 180.0)                      # direction along which the tuft spreads
    ax, ay = math.cos(math.radians(fan)), math.sin(math.radians(fan))
    w0 = min(8.6, max(5.2, 0.46 * h)) * rnd.uniform(0.88, 1.12)
    step = 0.34 * w0                                   # the roots overlap: one clump, not a row
    stagger = rnd.uniform(0.9, 1.4) if n >= 5 else rnd.uniform(0.2, 0.7)
    a = (n // 2) * step + 0.42 * w0 + 0.6
    b = stagger + rnd.uniform(2.3, 2.6)
    mound = Mound(x, y, fan + 90.0, a, b)
    if not _mound_ok(mound, lawn):
        return None
    slim0 = rnd.uniform(0.0, 0.7)                      # tufts differ in leaf shape, the leaves of one tuft are alike
    blades: list[Blade] = []
    for i in range(n):
        first = i == 0
        sgn, k = (1 if i % 2 else -1), (i + 1) // 2
        side = 1 if (i // 2) % 2 else -1
        for _ in range(10):
            w = w0 if first else max(4.2, w0 * rnd.uniform(0.7, 1.0))
            da = 0.0 if first else sgn * k * step * rnd.uniform(0.85, 1.1)
            do = 0.0 if first else side * stagger * rnd.uniform(0.6, 1.0)
            fh = 1.0 if first else rnd.uniform(0.6, 0.95) * (1.0 - 0.07 * k)
            tilt = rnd.uniform(-6.0, 6.0) if first else sgn * min(32.0, (7.0 + 7.0 * k) * rnd.uniform(0.7, 1.3))
            core = hub and first                                               # this leaf takes the screw
            want = max(5.0, h * fh)
            cand = _fit(
                Blade(
                    x + ax * da - ay * do, y + ay * da + ax * do, want, w, 4.6 if core else rnd.uniform(2.6, 3.0),
                    fan + 90.0 + (0.0 if core else rnd.uniform(-28.0, 28.0)), (0.0 if first else side * 6.0) + rnd.uniform(-8.0, 8.0), tilt,
                    0.0 if first else sgn * rnd.uniform(0.0, 2.0), min(1.0, max(0.0, slim0 + rnd.uniform(-0.2, 0.2))), core,
                )
            )
            # a tall tuft keeps its height: it does not go where the ball's belly would crop it
            if not hub and h >= 12.0 and cand.h < 0.85 * want:
                continue
            if _blade_ok(cand, lawn):
                blades.append(cand)
                break
        else:
            if first:
                return None
    if len(blades) < (3 if hub else min(n, 3) if h >= 12.0 else 2):
        return None
    return Tuft(mound, tuple(blades))


@lru_cache(maxsize=None)
def tufts() -> tuple[Tuft, ...]:
    """The lawn.  One tuft stands on each turf screw; the others are thrown at
    random over the rest of the turf, the largest first so that they still
    find room.  Deterministic: the same seed gives the same lawn, another seed
    another."""
    rnd = random.Random(P.LAWN_SEED)
    lawn: list[Tuft] = []
    for x, y in turf_screw_xy():
        made = None
        for _ in range(600):
            h, n = _draw_size(rnd, True)
            for _ in range(30):
                made = _grow(rnd, x, y, h, n, True, lawn)
                if made:
                    break
            if made:
                break
        if made is None:
            raise ValueError(f"no tuft fits on the turf screw at {x}, {y}")
        lawn.append(made)
    for h, n in sorted((_draw_size(rnd, False) for _ in range(P.LAWN_TUFTS)), reverse=True):
        for _ in range(6000):
            x, y = rnd.uniform(P.X_REAR, P.SPOT_X + P.TONGUE_W), rnd.uniform(-P.TONGUE_W, P.TONGUE_W)
            if not grass_free(x, y, 3.0, 2.6, 5.4):
                continue
            if any(math.hypot(x - t.mound.x, y + t.mound.y) < 5.0 for t in lawn):
                continue                               # no twin of a tuft on the other side
            made = _grow(rnd, x, y, h, n, False, lawn)
            if made:
                lawn.append(made)
                break
    return tuple(lawn)


def blades() -> tuple[Blade, ...]:
    return tuple(b for t in tufts() for b in t.blades)


def mounds() -> tuple[Mound, ...]:
    return tuple(t.mound for t in tufts())


def mound_solid(m: Mound) -> cq.Shape:
    wires = [
        cq.Wire.makeEllipse(m.a * f, m.b * f, cq.Vector(0, 0, z), cq.Vector(0, 0, 1), cq.Vector(1, 0, 0))
        for z, f in ((-P.BLADE_ROOT_SINK, 1.0), (0.45 * P.MOUND_H, 0.93), (P.MOUND_H, 0.66))
    ]
    return g.move(g.rot(cq.Solid.makeLoft(wires), "z", m.out_deg - 90.0), m.x, m.y, P.Z_TURF)


@lru_cache(maxsize=None)
def blade_solid(b: Blade) -> cq.Shape:
    """Loft one blade and put it in place; its root is sunk into the turf."""
    wires = []
    for s, *_ in _PROFILE:
        a, th, dx, dy, z = _section(b, s)
        wires.append(cq.Wire.makeEllipse(a, th, cq.Vector(dx, dy, z if s > 0 else -P.BLADE_ROOT_SINK), cq.Vector(0, 0, 1), cq.Vector(1, 0, 0)))
    return g.move(g.rot(cq.Solid.makeLoft(wires), "z", b.yaw - 90.0), b.x, b.y, P.Z_TURF)


# --------------------------------------------------------------------------
# tray
# --------------------------------------------------------------------------
def _cable_trench() -> cq.Shape:
    """Channel from the reader pocket to the cable window in the bowl, open at the top."""
    x_well = POCKET[0] + P.BLUE_LEDGE
    z0 = P.Z_TRAY_FLOOR
    straight = g.box(P.WINDOW_R0, x_well + 0.02, -P.CHANNEL_W, P.CHANNEL_W, z0, P.Z_TURF + 1.0)
    # the channel widens to the width of the header row; the taper is long, so that no thin fin is left beside the ball
    wide, x1, x2 = 16.5, x_well - 2.0, x_well - 9.0
    mouth = g.prism_xy([(x_well + 0.02, wide), (x1, wide), (x2, P.CHANNEL_W), (x2, -P.CHANNEL_W), (x1, -wide), (x_well + 0.02, -wide)], z0, P.Z_TURF + 1.0)
    return straight.fuse(mouth)


def _hall_seat() -> cq.Shape:
    """Three low walls on the floor of the pocket that hold the hall switch under the antenna centre."""
    sx, zf = P.SPOT_X, P.Z_TRAY_FLOOR
    hx, hy = P.HALL_H / 2, P.HALL_W / 2
    outer = g.box(sx - hx - 0.2, sx + hx + 1.3, -hy - 1.2, hy + 1.2, zf - 0.01, zf + 1.2)
    inner = g.box(sx - hx - 1.0, sx + hx + 0.15, -hy - 0.15, hy + 0.15, zf - 0.02, zf + 2.0)
    return outer.cut(inner)


@lru_cache(maxsize=None)
def grass_base() -> cq.Shape:
    zs, zr, zt, zf = P.Z_SOLE, P.Z_RAIL, P.Z_TURF, P.Z_TRAY_FLOOR
    block = plan(zs, zr)
    cup = g.sphere(P.R + P.CUP_GAP)
    body = _chamfered(block, "<Z").cut(cup).cut(g.cyl_z(P.R_CUP_HOLE, zs - 1, zt + 1))
    # seat pads round the screws carry the joint; everywhere else the cup keeps CUP_GAP
    for x, y in base_screw_xy():
        pad = g.inter(g.inter(g.cyl_z(P.BASE_PAD_R, zs, zr, x, y), cup).cut(g.sphere(P.R)), block)
        body = body.fuse(pad)

    # reader pocket: the board lies on a ledge, component side down, with a well below it
    x0, x1, yh = POCKET
    led, wide = P.BLUE_LEDGE, P.BLUE_LEDGE_ANT
    x_ant = BLUE_X0 + P.BLUE_COMP_X[1] + 1.5              # from here on the board carries no parts
    body = body.cut(g.box(x0, x1, -yh, yh, P.Z_PCB_BOT, zt + 1))
    body = body.cut(g.box(x0 + led, x_ant + 0.01, -yh + led, yh - led, zf, P.Z_PCB_BOT + 0.01))
    body = body.cut(g.box(x_ant, x1 - wide, -yh + wide, yh - wide, zf, P.Z_PCB_BOT + 0.01))
    body = body.cut(_cable_trench())
    body = body.fuse(_hall_seat())

    # fasteners
    for x, y in base_screw_xy():
        r_head = P.CSK_D / 2 + 0.3
        body = body.cut(g.cyl_z(P.M3_CLEAR / 2, zs - 1, zt + 1, x, y))
        body = body.cut(g.cyl_z(r_head, zs - 1, zs + P.CSK_RECESS, x, y))
        body = body.cut(g.cone_z(r_head, P.M3_CLEAR / 2, zs + P.CSK_RECESS, zs + P.CSK_RECESS + (r_head - P.M3_CLEAR / 2), x, y))
    for x, y in turf_screw_xy():
        body = body.cut(g.cyl_z(P.M2_CLEAR / 2, zs - 1, zr + 1, x, y))
        body = body.cut(g.cyl_z(P.TURF_SCREW_HEAD_D / 2 + 0.4, zs - 1, zs + P.TURF_SCREW_CB, x, y))
    return g.clean(body)


# --------------------------------------------------------------------------
# turf
# --------------------------------------------------------------------------
def spot_disc(z0: float, z1: float) -> cq.Shape:
    return g.cyl_z(P.SPOT_R, z0, z1, P.SPOT_X, 0.0)


@lru_cache(maxsize=None)
def turf_plate() -> cq.Shape:
    """The turf without blades and screw holes."""
    zr, zt = P.Z_RAIL, P.Z_TURF
    plate = _chamfered(plan(zr, zt), ">Z").cut(g.sphere(P.R + P.CUP_GAP))
    # underside: flat, except for a shallow relief above the solder joints of the header row
    plate = plate.cut(g.box(POCKET[0], BLUE_X0 + P.BLUE_HDR_X + 3.0, -17.5, 17.5, zr - 1, zr + P.SOLDER_RELIEF))
    # top: pocket for the flush marker disc
    plate = plate.cut(spot_disc(zt - P.SPOT_INLAY, zt + 1))
    return g.clean(plate)


@lru_cache(maxsize=None)
def grass_top() -> cq.Shape:
    """The turf plate with the pilot holes of its screws."""
    body = turf_plate()
    for x, y in turf_screw_xy():
        body = body.cut(g.cyl_z(P.M2_PILOT / 2, P.Z_RAIL - 1, P.Z_TURF + 1, x, y))
    return body


@lru_cache(maxsize=None)
def lawn_fused() -> cq.Shape:
    """Turf, mounds and blades as one solid, as they come off the printer."""
    zr = P.Z_RAIL
    body = turf_plate().fuse(*[mound_solid(m) for m in mounds()], *[blade_solid(b) for b in blades()])
    for x, y in turf_screw_xy():
        body = body.cut(g.cyl_z(P.M2_PILOT / 2, zr - 1, zr + P.TURF_PILOT_DEPTH, x, y))
    return body


@lru_cache(maxsize=None)
def grass_blades() -> cq.Shape:
    """Everything that stands on the turf surface: the tufts with their mounds."""
    return lawn_fused().intersect(g.slab(P.Z_TURF, P.Z_TURF + 60.0))


@lru_cache(maxsize=None)
def grass_spot() -> cq.Shape:
    return spot_disc(P.Z_TURF - P.SPOT_INLAY, P.Z_TURF)


# --------------------------------------------------------------------------
# helpers for checks and pictures
# --------------------------------------------------------------------------
def figure_envelope() -> cq.Shape:
    """Cylinder that contains each of the four Pokémon Tonies standing on the spot."""
    return g.cyl_z(P.TONIE_ENVELOPE_D / 2, P.Z_TURF, P.Z_TURF + P.TONIE_ENVELOPE_H, P.SPOT_X, 0.0)


def sole_outline(n: int = 180) -> list[tuple[float, float]]:
    """Points on what stands on the table: the flat of the ball and the sole of the tongue."""
    w, c = P.TONGUE_W, P.REAR_CHAMFER
    pts = [g.polar(P.R_FLAT, 360.0 * i / n) for i in range(n)]
    for s in (1, -1):
        pts += [(P.X_REAR, s * (w - c)), (P.X_REAR + c, s * w)]
    pts += [(P.SPOT_X + w * math.cos(a), w * math.sin(a)) for a in (math.pi * (i / n - 0.5) for i in range(n + 1))]
    return pts
