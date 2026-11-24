"""Printed parts that are visible from outside when the ball is closed.

bowl   white lower half with the flat foot and the seat for the grass tongue
band   black equatorial ring (carries the lid seat and the hinge pocket)
lid    red upper half with hinge ribs and latch hook
bezel  black ring around the button with the sound slits
lens   translucent flat rim + button, lit by the RGB LED
cone   white light funnel that also carries the LED

All parts are returned in assembly coordinates (see geom.py).
"""

from __future__ import annotations

import math
from functools import lru_cache

import cadquery as cq

from . import geom as g
from . import params as P
from . import parts_base as B

HINGE = (P.HINGE_X, 0.0, P.HINGE_Z)


def open_lid(shape: cq.Shape, deg: float) -> cq.Shape:
    """Rotate a lid-fixed shape about the hinge axis by the opening angle."""
    return g.rot(shape, "y", -deg, HINGE) if deg else shape


def _bezel_cut(extra: float = 0.0) -> cq.Shape:
    """The cylinder all shells are notched with to let the bezel tube pass."""
    return g.cyl_x(P.BEZEL_R + extra, 20.0, 70.0)


# --------------------------------------------------------------------------
# bowl
# --------------------------------------------------------------------------
@lru_cache(maxsize=None)
def bowl() -> cq.Shape:
    outer = g.inter(g.sphere(P.R), g.slab(P.Z_FLAT, P.Z_BOWL_RIM))
    cavity = g.inter(g.sphere(P.RI_BOWL), g.slab(P.Z_FLOOR, 10.0))
    body = outer.cut(cavity)

    skin = g.sphere(P.R - 0.6)
    z0, z1 = P.Z_BOWL_RIM - P.BOSS_DEPTH, P.Z_BOWL_RIM
    for az in P.SCREW_AZ:
        bx, by = g.polar(P.SCREW_R, az)
        boss = g.cyl_z(P.BOSS_R, z0, z1, bx, by)
        web = g.rot(g.box(P.SCREW_R, P.R, -P.BOSS_R, P.BOSS_R, z0, z1), "z", az)
        body = body.fuse(g.inter(boss.fuse(web), skin))
    for az in P.SCREW_AZ:
        bx, by = g.polar(P.SCREW_R, az)
        body = body.cut(g.cyl_z(P.M3_INSERT_HOLE / 2, z1 - P.M3_INSERT_DEPTH, z1 + 1, bx, by))
        body = body.cut(g.cyl_z(1.6, z0 + 1.0, z1, bx, by))          # screw tip relief

    body = body.cut(_bezel_cut(P.CL))
    # the grass tongue is screwed on from below: four bosses with heat-set inserts
    for bx, by in B.base_screw_xy():
        body = body.fuse(g.inter(g.cyl_z(P.BASE_BOSS_R, P.Z_FLOOR, P.Z_BASE_BOSS, bx, by), skin))
    for bx, by in B.base_screw_xy():
        body = body.cut(g.cyl_z(P.M3_INSERT_HOLE / 2, P.Z_BASE_BOSS - P.BASE_INSERT_DEPTH, P.Z_BASE_BOSS + 1, bx, by))
        body = body.cut(g.cyl_z(P.M3_CLEAR / 2, P.Z_FLAT - 1, P.Z_BASE_BOSS, bx, by))
    # the reader harness enters through a window in the wall that the tongue hides
    body = body.cut(B.cable_window())
    # the charger PCB reaches under the band: relieve the inside of the rim for its corners
    z_pcb = P.USB_Z - P.USB_H / 2 - 1.0
    r_pcb_end = P.TP_TIP_R - 1.2
    body = body.cut(g.rot(g.box(44.0, r_pcb_end + 0.15, -P.TP_W / 2 - 0.7, P.TP_W / 2 + 0.7, z_pcb - 0.3, P.Z_BOWL_RIM + 1), "z", P.USB_AZ))
    # ... and outside, a shallow scoop in the rim lets the body of the USB-C plug reach the socket
    scoop = g.box(P.R_BAND - 0.1, P.R + 5, -P.USB_PLUG_W / 2 - 0.5, P.USB_PLUG_W / 2 + 0.5, P.USB_Z - P.USB_PLUG_H / 2 - 0.3, P.Z_BOWL_RIM + 1)
    body = body.cut(g.rot(scoop, "z", P.USB_AZ))
    return g.clean(body)


# --------------------------------------------------------------------------
# lid
# --------------------------------------------------------------------------
def _hook(c: float = 0.0) -> cq.Shape:
    ys0, ys1 = P.HOOK_Y - P.HOOK_W / 2 - c, P.HOOK_Y + P.HOOK_W / 2 + c
    z_top = P.TOOTH_TOP_Z + c
    stem_bottom = z_top - 1.0 - P.TOOTH_REACH - 2 * c
    stem = g.box(P.HOOK_X0 - c, P.HOOK_X1 + c, ys0, ys1, stem_bottom, P.R)
    tooth = g.prism_yz(
        [
            (ys0 + 0.01, z_top),
            (ys0 - P.TOOTH_REACH - c, z_top),
            (ys0 - P.TOOTH_REACH - c, z_top - 1.0 - 2 * c),
            (ys0 + 0.01, stem_bottom),
        ],
        P.HOOK_X0 - c,
        P.HOOK_X1 + c,
    )
    return g.inter(stem.fuse(tooth), g.sphere(P.RI_LID + 0.4))


def _ribs(c: float = 0.0, bores: bool = True) -> cq.Shape:
    hx, hz, kr = P.HINGE_X, P.HINGE_Z, P.KNUCKLE_R + c
    out = None
    for sy in (1, -1):
        ya = P.SPRING_SLOT / 2 - c
        yb = P.SPRING_SLOT / 2 + P.LID_RIB_T + c
        y0, y1 = (ya, yb) if sy > 0 else (-yb, -ya)
        knuckle = g.cyl_y(kr, y0, y1, hx, hz)
        web = g.prism_xz(
            [(hx, hz + kr), (-P.R, hz + kr), (-P.R, hz - kr - 6.9), (hx - 0.6, hz - kr)], y0, y1
        )
        tab = g.box(hx, hx + P.LID_TAB_LEN + c, y0, y1, hz - 1.5 - c, hz + 1.5 + c)
        tab = g.rot(tab, "y", -P.LID_TAB_DEG, HINGE)
        rib = knuckle.fuse(web).fuse(tab)
        out = rib if out is None else out.fuse(rib)
    out = g.inter(out, g.sphere(P.R - 0.25))
    out = g.inter(out, g.slab(P.HB - c, 100.0))
    if bores:
        out = out.cut(g.cyl_y(P.HINGE_BORE / 2, -30, 30, hx, hz))      # the ribs turn on the two hinge pins
    return out


@lru_cache(maxsize=None)
def lid(fat: float = 0.0) -> cq.Shape:
    """The red lid.  ``fat`` > 0 grows every surface by that amount; the fat
    lid is only used as a cutting tool to create clearance for the motion."""
    c = fat
    shell = g.ball_zone(P.R + c, P.RI_LID - c, P.HB - c, P.R + 10.0)
    lip = g.revolve_z(
        [
            (P.LID_LIP_R - c, P.HB - c),
            (P.RI_LID + 0.05, P.HB - c),
            (P.RI_LID + 0.05, P.HB + P.LID_LIP_H + (P.RI_LID - P.LID_LIP_R) + c),
            (P.LID_LIP_R - c, P.HB + P.LID_LIP_H + c),
        ]
    )
    body = shell.fuse(g.inter(lip, g.sphere(P.R - 0.3 + c)))
    # the wall is thinned from inside where the hinge knuckles sit
    patch = g.inter(
        g.sphere(P.R - P.LID_WALL_AT_HINGE - c),
        g.box(-70, -30, -11.5 + c, 11.5 - c, P.HB - 5, P.HINGE_Z + 4.0 - c),
    )
    body = body.cut(patch)
    # ... and relieved beside them: the two hinge pins stand out of their towers while the lid is put on
    for sgn in (1, -1):
        ya, yb = sorted((sgn * 11.4, sgn * (P.HINGE_RECESS_Y - c)))
        relief = g.inter(
            g.sphere(P.R - P.HINGE_RECESS_WALL - c),
            g.box(-70, -30, ya, yb, P.HB - 5, P.HINGE_Z + P.HINGE_RECESS_TOP - c),
        )
        body = body.cut(relief)
    body = body.fuse(_ribs(c, bores=(c == 0.0)))
    body = body.fuse(_hook(c))
    body = body.cut(_bezel_cut(P.SEAM_GAP - c))
    return g.clean(body)


def rim_swing_radius(y: float) -> float:
    """Largest distance from the hinge axis of any lid point in the slice ``y``
    that lies behind the hinge: the outer bottom corner of the rim."""
    behind = math.sqrt(max(P.R**2 - y**2 - P.HB**2, 0.0)) + P.HINGE_X      # > 0: behind the axis
    return math.hypot(max(behind, 0.0), P.HINGE_E)


def rim_swing_tool(clearance: float) -> cq.Shape:
    """Solid of revolution about the hinge axis that contains everything the
    rear rim of the lid sweeps while it dips behind the concealed hinge."""
    y_end = math.sqrt(P.R**2 - P.HB**2 - P.HINGE_X**2)       # rim is level with the axis line
    n = 40
    pts = [(P.HINGE_X, -y_end - 1.0)]
    for i in range(n + 1):
        y = -y_end + 2 * y_end * i / n
        pts.append((P.HINGE_X + rim_swing_radius(y) + clearance, y))
    pts.append((P.HINGE_X, y_end + 1.0))
    wp = cq.Workplane("XY").polyline(pts).close().revolve(360.0, (P.HINGE_X, 0, 0), (P.HINGE_X, 1, 0))
    return wp.val().translate(cq.Vector(0, 0, P.HINGE_Z))


def lip_swing_radius(y: float) -> float:
    """Distance from the hinge axis of the inner bottom edge of the lid's lip in the slice ``y``, at the back of
    the lid.  Of everything the lid has in that slice near its rim, this edge lies furthest from the axis: it is
    what swings into the stage when the lid opens."""
    dx = -math.sqrt(max(P.LID_LIP_R**2 - y**2, 0.0)) - P.HINGE_X
    return math.hypot(dx, P.HINGE_E)


def lip_swing_tool(clearance: float, side_play: float, y_max: float) -> cq.Shape:
    """Solid of revolution about the hinge axis that contains everything the lip of the lid sweeps at the back
    of the ball while the lid opens, for a lid that may stand up to ``side_play`` to either side of its place,
    with ``clearance`` round it."""
    y_lip = P.LID_LIP_R - 0.5
    n = 72
    pts = [(P.HINGE_X, -y_max)]
    for i in range(n + 1):
        y = -y_max + 2 * y_max * i / n
        near, far = max(abs(y) - side_play, 0.0), min(abs(y) + side_play, y_lip)
        pts.append((P.HINGE_X + max(lip_swing_radius(near), lip_swing_radius(far)) + clearance, y))
    pts.append((P.HINGE_X, y_max))
    wp = cq.Workplane("XY").polyline(pts).close().revolve(360.0, (P.HINGE_X, 0, 0), (P.HINGE_X, 1, 0))
    return wp.val().translate(cq.Vector(0, 0, P.HINGE_Z))


# --------------------------------------------------------------------------
# band
# --------------------------------------------------------------------------
def usb_dir() -> tuple[float, float]:
    a = math.radians(P.USB_AZ)
    return (math.cos(a), math.sin(a))


@lru_cache(maxsize=None)
def band() -> cq.Shape:
    wall = g.inter(g.sphere(P.R_BAND), g.slab(-P.HB, P.HB)).cut(g.cyl_z(P.RI_BAND, -10, 10))
    # spigot: drops inside the bowl rim and is tied to the wall by a 45 deg fillet
    # (the band is printed upside down, so the fillet needs no support)
    spigot = g.revolve_z(
        [
            (P.RI_BAND + 0.05, -P.HB + 2.5),
            (P.R_SPIGOT_IN, -P.HB + 2.5 - (P.RI_BAND - P.R_SPIGOT_IN)),
            (P.R_SPIGOT_IN, -P.HB - P.SPIGOT_H),
            (P.R_SPIGOT_OUT, -P.HB - P.SPIGOT_H),
            (P.R_SPIGOT_OUT, -P.HB),
            (P.RI_BAND + 0.05, -P.HB),
        ]
    )
    body = wall.fuse(spigot)
    lug_profile = [
        (P.RI_BAND + 0.2, 0.0),
        (P.LUG_R_IN, 0.0),
        (P.LUG_R_IN, P.LUG_T),
        (P.LUG_R_IN + (P.HB - P.LUG_T), P.HB),
        (P.RI_BAND + 0.2, P.HB),
    ]
    for az in P.SCREW_AZ:
        lug = g.revolve_z(lug_profile, 2 * P.LUG_HALF_DEG)
        lug = g.rot(lug, "z", az - P.LUG_HALF_DEG)
        body = body.fuse(lug)
    for az in P.SCREW_AZ:
        bx, by = g.polar(P.SCREW_R, az)
        body = body.cut(g.cyl_z(P.M3_CLEAR / 2, -1, 10, bx, by))
        body = body.cut(g.cyl_z(P.BOSS_R + 0.35, -20, -P.HB, bx, by))   # spigot clears the bosses
        body = body.cut(g.rot(g.box(P.SCREW_R, P.R, -P.BOSS_R - 0.35, P.BOSS_R + 0.35, -20, -P.HB), "z", az))
    # straight-sided gap: the band is lowered over the bezel from above
    body = body.cut(g.box(20.0, 70.0, -P.BEZEL_R - P.CL, P.BEZEL_R + P.CL, -20, 20))
    # USB-C notch, open towards the bowl so the band can be lowered over the port
    notch = g.box(30, 60, -P.USB_OPEN_W / 2, P.USB_OPEN_W / 2, -20, P.USB_Z + P.USB_H / 2 + 0.2)
    body = body.cut(g.rot(notch, "z", P.USB_AZ))
    # ... and the charger PCB below it needs the spigot and the lower wall edge relieved
    z_pcb_top = P.USB_Z - P.USB_H / 2
    body = body.cut(g.rot(g.box(40.0, 48.2, -P.TP_W / 2 - 0.7, P.TP_W / 2 + 0.7, -20, z_pcb_top + 0.1), "z", P.USB_AZ))
    # pocket for the lid rim, which dips behind the concealed hinge while opening
    body = body.cut(rim_swing_tool(P.BAND_POCKET_CL))
    return g.clean(body)


# --------------------------------------------------------------------------
# bezel, lens, light cone
# --------------------------------------------------------------------------
def _slit_arcs(x0: float, x1: float) -> cq.Shape:
    """Four arc slits (centred on the diagonals) as one cutting tool."""
    r0, r1 = P.SLIT_R - P.SLIT_W / 2, P.SLIT_R + P.SLIT_W / 2
    ring = g.cyl_x(r1, x0, x1).cut(g.cyl_x(r0, x0 - 1, x1 + 1))
    out = None
    for k in range(4):
        mid = 45.0 + 90.0 * k
        a0, a1 = math.radians(mid - P.SLIT_ARC / 2), math.radians(mid + P.SLIT_ARC / 2)
        big = 60.0
        wedge = g.prism_yz(
            [(0, 0), (big * math.cos(a0), big * math.sin(a0)), (big * math.cos((a0 + a1) / 2), big * math.sin((a0 + a1) / 2)), (big * math.cos(a1), big * math.sin(a1))],
            x0 - 1,
            x1 + 1,
        )
        arc = g.inter(ring, wedge)
        out = arc if out is None else out.fuse(arc)
    return out


def emergency_axis() -> tuple[cq.Vector, cq.Vector]:
    """Start point (on the bezel face) and unit direction of the paper-clip path."""
    y, z = P.EMERGENCY_YZ
    a = math.radians(P.EMERGENCY_SLOPE_DEG)
    return cq.Vector(P.BEZEL_X_FACE, y, z), cq.Vector(-math.cos(a), 0.0, math.sin(a))


def emergency_channel(d: float, length: float = 30.0) -> cq.Shape:
    """Cylinder along the paper-clip path, starting 2 mm in front of the bezel face."""
    start, direction = emergency_axis()
    return cq.Solid.makeCylinder(d / 2, length + 2.0, start - direction * 2.0, direction)


@lru_cache(maxsize=None)
def bezel() -> cq.Shape:
    xf, xb = P.BEZEL_X_FACE, P.BEZEL_X_BACK
    tube = g.cyl_x(P.BEZEL_R, xb, xf).cut(g.cyl_x(P.BEZEL_R - P.BEZEL_WALL, xb - 1, xf - P.BEZEL_FACE_T))
    # Band, stage and lid come down over the tube from above.  From the rim of the bowl upwards it is therefore
    # smaller: the notch of the lid keeps BEZEL_LID_GAP from it, and band and stage have as much room.  The bowl
    # below and the socket in the chassis behind hold the tube at its full size.  (This is cut from the plain tube
    # on purpose: cut from the finished bezel, the kernel returned the body unchanged, without an error.)
    x_r = P.BAFFLE_X1 + 0.3
    skin = g.cyl_x(P.BEZEL_R + 1.0, x_r, xf + 1.0).cut(g.cyl_x(P.BEZEL_R - (P.BEZEL_LID_GAP - P.SEAM_GAP), x_r - 1.0, xf + 2.0))
    tube = tube.cut(g.inter(skin, g.box(x_r - 1.0, xf + 2.0, -30.0, 30.0, P.Z_BOWL_RIM + 0.2, 30.0)))
    # lens opening, flange seat and the seat tube that also holds the light cone
    seat_tube = g.cyl_x(P.SEAT_R1, xf - 6.0, xf - P.BEZEL_FACE_T + 0.01).cut(g.cyl_x(P.SEAT_R0, xf - 7, xf))
    body = tube.fuse(seat_tube)
    body = body.cut(g.cyl_x(P.LENS_R, xf - 5, xf + 1))
    body = body.cut(g.cyl_x(P.SEAT_R0, xf - 7, P.LENS_SEAT_X))
    body = body.cut(_slit_arcs(xf - P.BEZEL_FACE_T - 0.5, xf + 1))
    # slot in the tube wall through which the emergency paper clip leaves the bezel
    start, direction = emergency_axis()
    body = body.cut(cq.Solid.makeCylinder(0.95, 7.0, start - direction * 1.5, direction))   # entry through the face
    for i in range(7):
        body = body.cut(cq.Solid.makeCylinder(1.15, 14.0, start + direction * 1.5 + cq.Vector(-0.25 * i, 0, 0), direction))
    # key on the underside so the bezel can only be glued in one orientation
    key = g.box(xb, xb + 3.0, -1.5, 1.5, -P.BEZEL_R - 1.2, -P.BEZEL_R + 0.3)
    return g.clean(body.fuse(key))


@lru_cache(maxsize=None)
def lens() -> cq.Shape:
    xf = P.BEZEL_X_FACE
    disc = g.cyl_x(P.LENS_R - 0.15, P.LENS_SEAT_X, xf)
    flange = g.cyl_x(P.LENS_FLANGE_R, P.LENS_SEAT_X - 1.2, P.LENS_SEAT_X)
    button = g.cyl_x(P.BTN_R, xf, xf + P.BTN_PROUD)
    button = cq.Workplane(obj=button).edges(">X").fillet(0.8).val()
    body = disc.fuse(flange).fuse(button)
    hollow = g.cyl_x(P.LENS_R - 1.6, P.LENS_SEAT_X - 2, xf - P.LENS_T)
    return g.clean(body.cut(hollow))


@lru_cache(maxsize=None)
def cone() -> cq.Shape:
    x_led = P.LED_X - 1.6                  # front face of the LED PCB = cone ledge
    x_pcb = P.LED_X - P.LED_PCB_T          # back face of the LED PCB
    x_front = P.LENS_SEAT_X - 1.2          # the cone pushes the lens flange forward
    x_rim = x_front - 2.4
    r_front = P.SEAT_R0 - 0.1
    r_cup = P.LED_PCB_D / 2 + 0.15
    outer = (
        g.cyl_x(r_front, x_rim, x_front)
        .fuse(g.cone_x(r_cup + 1.0, r_front, x_led, x_rim))
        .fuse(g.cyl_x(r_cup + 1.0, x_pcb, x_led))
    )
    inner = (
        g.cone_x(3.8, r_front - 1.2, x_led, x_front + 0.01)
        .fuse(g.cyl_x(r_cup, x_pcb - 1, x_led))
    )
    body = outer.cut(inner)
    body = body.cut(g.box(x_pcb - 1, x_pcb + 1.2, -1.6, 1.6, -r_cup - 2, 0))   # wire exit
    return g.clean(body)
