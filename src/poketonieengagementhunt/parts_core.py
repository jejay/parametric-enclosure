"""Printed parts inside the ball.

stage         black inner dome: ring deck with the slot of the ring, hinge towers, the pivots of the two pawls,
              lid collar
chassis       bucket carrying battery, servo, boards and the speaker baffle
pawl          latch pawl released by the servo
ring_pawl     pawl that locks the ring in its slot; its knob stands up through the deck
sleeve        mandrel of the torsion spring; the two hinge pins are pressed into its ends
spk_clamp     ring that clamps the speaker against the baffle

All parts are returned in assembly coordinates.
"""

from __future__ import annotations

import math
from functools import lru_cache

import cadquery as cq

from . import geom as g
from . import params as P
from . import parts_shell as S

HX, HZ = P.HINGE_X, P.HINGE_Z
TOWER_Y0 = P.SPRING_SLOT / 2 + P.LID_RIB_T + P.TOWER_GAP   # inner face of a hinge tower
TOWER_Y1 = TOWER_Y0 + P.TOWER_T                        # outer face of a hinge tower
FOOT_Y0 = TOWER_Y0 - P.YOKE_FOOT_PAD                   # inner face of a tower's foot, which is thicker than the tower
SLEEVE_HALF = P.SPRING_SLOT / 2 - P.SLEEVE_PLAY        # half the length of the spring sleeve
YOKE_SEAT_Z = HZ - (P.SPRING_OD - P.SPRING_WIRE) / 2 - P.SPRING_WIRE / 2   # the spring's forward leg lies on this height
YOKE_PIN_Z = YOKE_SEAT_Z - P.YOKE_PIN_D / 2                                # axis of the pin under that leg
PAWL_SPRING_Z = P.PAWL_Z0 + 1.0                                            # axis of the pawl's return spring
PAWL_SPRING_X = P.PAWL_PIVOT[0] - P.PAWL_TAIL_X + 1.75                     # ... and where its seat under the deck lies
DECK_BOTTOM = P.Z_DECK - P.DECK_T
# the ring pawl and the slot of the ring
RPX, RPY = P.RPAWL_PIVOT
RPAWL_Z1 = DECK_BOTTOM - P.RPAWL_PLAY                  # top of the ring pawl where it lies by itself: on its washer
RPAWL_Z0 = RPAWL_Z1 - P.RPAWL_T                        # its underside there, which is also the end of its pivot boss
RPAWL_SPRING_Z = RPAWL_Z0 + P.RPAWL_T / 2              # axis of its return spring
RING_SLOT_Z = P.Z_DECK - P.RING_SLOT_DEPTH             # bottom of the slot of the ring, in its middle
RING_UNDER_TIP = RPAWL_Z0 - RING_SLOT_Z                # room under the finger of the ring pawl, for the band of the ring
RING_SLOT_ZC = RING_SLOT_Z + P.RING_SLOT_D / 2         # axis of its round bottom
RING_SLOT_X0, RING_SLOT_X1 = P.RING_X - P.RING_SLOT_W / 2, P.RING_X + P.RING_SLOT_W / 2
RPAWL_R = math.hypot(P.RING_X - RPX, RPY)              # radius of the middle line of the finger: it crosses the middle of
                                                       # the slot (y = 0)


def _sector(profile, az: float, half_deg: float) -> cq.Shape:
    """Revolve an (r, z) profile into a sector centred on azimuth ``az``."""
    return g.rot(g.revolve_z(profile, 2 * half_deg), "z", az - half_deg)


def band_lug(az: float, grow: float = 0.0) -> cq.Shape:
    """One band lug (same profile as in parts_shell.band), optionally grown."""
    c = grow
    profile = [
        (P.RI_BAND + 1.0, -c),
        (P.LUG_R_IN - c, -c),
        (P.LUG_R_IN - c, P.LUG_T + c),
        (P.LUG_R_IN + (P.HB - P.LUG_T) - c, P.HB + c),
        (P.RI_BAND + 1.0, P.HB + c),
    ]
    return _sector(profile, az, P.LUG_HALF_DEG + (0.6 if c else 0.0))


def hook_slot() -> cq.Shape:
    """What is cut out of the stage for the hook of the lid.

    The ring sector about the hinge axis that the hook sweeps while the lid opens, with room round it: little
    beside the stem, more beside the tooth.  At the top of the deck the slot widens to a funnel on both sides,
    for a hook that comes down beside its place.  Under the deck its edge beside the tooth is sloped, for a
    tooth that comes up beside its place: a square edge would catch it there."""
    grow = P.CL_MOVE + 0.1
    r0 = math.hypot(P.HOOK_X0 - HX, P.PAWL_Z0 - 4.0 - HZ) - grow - 0.3
    r1 = math.hypot(P.HOOK_X1 - HX, 40.0 - HZ) + grow
    a0 = math.degrees(math.atan2(P.PAWL_Z0 - 5.5 - HZ, P.HOOK_X1 - HX))
    pts = []
    n = 24
    for i in range(n + 1):
        a = math.radians(a0 + (40.0 * i) / n)
        pts.append((HX + r1 * math.cos(a), HZ + r1 * math.sin(a)))
    for i in range(n, -1, -1):
        a = math.radians(a0 + (40.0 * i) / n)
        pts.append((HX + r0 * math.cos(a), HZ + r0 * math.sin(a)))
    y0, y1 = hook_slot_y()
    slot = g.prism_xz(pts, y0, y1)
    xa = HX + math.sqrt(r0**2 - (P.Z_DECK - HZ) ** 2) - 0.2        # rear end of the slot at the top of the deck
    xb = P.R_STAGE
    top = P.Z_DECK + 0.1

    def lead(y_wall: float, sgn: int, size: float) -> cq.Shape:
        """Slope at 45 degrees on the top edge of the slot: ``size`` wide at the top of the deck and as deep."""
        return g.prism_yz([(y_wall - sgn * 0.01, P.Z_DECK - size), (y_wall - sgn * 0.01, top), (y_wall + sgn * (size + 0.1), top)], xa, xb)

    funnel = lead(y1, 1, P.HOOK_SLOT_LEAD_STEM).fuse(lead(y0, -1, P.HOOK_SLOT_LEAD))
    uw, uh = P.HOOK_SLOT_UNDER
    under = g.prism_yz([(y0 + 0.01, DECK_BOTTOM + uh), (y0 + 0.01, DECK_BOTTOM - 0.1), (y0 - uw * (uh + 0.1) / uh, DECK_BOTTOM - 0.1)], xa, xb)
    # room for the front end of the tooth beside the slot, below the deck: only as far out as the tooth reaches,
    # so that the dome stays closed outside
    r_front = math.hypot(P.HOOK_X1 - HX, P.TOOTH_TOP_Z - HZ) + grow + 0.2
    arc = [(HX + r_front * math.cos(math.radians(a0 + 40.0 * i / n)), HZ + r_front * math.sin(math.radians(a0 + 40.0 * i / n))) for i in range(n + 1)]
    room = g.prism_xz(arc + pts[n + 1 :], y0 - P.HOOK_SLOT_ROOM, y0 + 0.01)
    room = g.inter(room, g.box(0.0, 60.0, y0 - P.HOOK_SLOT_ROOM - 1.0, y0 + 1.0, 0.0, DECK_BOTTOM + 0.01))
    return slot.fuse(funnel).fuse(under).fuse(room)


def hook_slot_y() -> tuple[float, float]:
    """The two walls of the hook's slot: beside the tip of the tooth and beside the stem."""
    return (P.HOOK_Y - P.HOOK_W / 2 - P.TOOTH_REACH - P.HOOK_SLOT_TOOTH, P.HOOK_Y + P.HOOK_W / 2 + P.HOOK_SLOT_STEM)


def hook_guide() -> cq.Shape:
    """Rib under the deck beside the stem of the hook.  It makes the deck thick enough there for a deep funnel
    and, below the funnel, an upright wall that guides the stem.  The slot is cut out of it afterwards."""
    _, y1 = hook_slot_y()
    rib = g.box(P.HOOK_GUIDE_X, P.R_STAGE, y1 - 1.0, y1 + P.HOOK_SLOT_LEAD_STEM + 0.8, DECK_BOTTOM - P.HOOK_GUIDE_T, DECK_BOTTOM + 0.01)
    return g.inter(rib, g.sphere(P.R_STAGE - 0.01))


# --------------------------------------------------------------------------
# stage
# --------------------------------------------------------------------------
COLLAR_R_TOP = 45.4                                    # the slopes above collar and base ring end on this radius
COLLAR_Z0 = 0.4                                        # the base ring steps in to the collar this far below the seam, so
                                                       # that its corner does not lie beside the lip of the lid


def _stage_shell() -> cq.Shape:
    """Dome, deck and the base ring inside the band; the collar comes on top (see stage)."""
    r_deck = math.sqrt(P.R_STAGE**2 - P.Z_DECK**2)
    dome = g.ball_zone(P.R_STAGE, P.RI_STAGE, P.HB, P.Z_DECK)
    deck = g.cyl_z(r_deck, DECK_BOTTOM, P.Z_DECK)
    r_top = COLLAR_R_TOP
    z0 = P.HB - COLLAR_Z0
    ring_back = g.revolve_z(
        [(44.4, 0.0), (P.R_CORE, 0.0), (P.R_CORE, z0 - (P.R_CORE - P.R_COLLAR)), (P.R_COLLAR, z0), (r_top, z0 + (P.R_COLLAR - r_top)), (44.4, z0 + (P.R_COLLAR - r_top))]
    )
    return dome.fuse(deck).fuse(ring_back)


def _collar() -> cq.Shape:
    """The collar that centres the lid: an upright wall inside the lip of the lid, with a slope above it that
    leads a lid in which comes down beside its place."""
    z_ch = P.HB + P.COLLAR_H
    r_top = COLLAR_R_TOP
    z0 = P.HB - COLLAR_Z0
    return _sector(
        [(44.4, 0.0), (P.R_CORE, 0.0), (P.R_CORE, z0 - (P.R_CORE - P.R_COLLAR)), (P.R_COLLAR, z0), (P.R_COLLAR, z_ch), (r_top, z_ch + (P.R_COLLAR - r_top)), (44.4, z_ch + (P.R_COLLAR - r_top))],
        0.0,
        P.COLLAR_AZ,
    )


def _screw_pads() -> cq.Shape:
    out = None
    for az in P.SCREW_AZ:
        pad = _sector(
            [(P.LUG_R_IN, P.LUG_T), (P.LUG_R_IN + (P.HB - P.LUG_T), P.HB), (46.2, P.HB), (46.2, 12.5), (44.9, 12.5), (P.LUG_R_IN, 12.5 - (44.9 - P.LUG_R_IN))],
            az,
            P.LUG_HALF_DEG + 1.0,
        )
        bx, by = g.polar(P.SCREW_R, az)
        well = g.cyl_z(P.M3_HEAD_D / 2 + 1.3, P.HB, P.Z_DECK - 0.5, bx, by)
        pad = pad.fuse(well)
        out = pad if out is None else out.fuse(pad)
    return g.inter(out, g.sphere(P.R_STAGE - 0.01))


def tower_knuckle(y0: float, y1: float) -> cq.Shape:
    """Knuckle of a hinge tower, without its bore: a closed ring round the hinge pin.

    The hinge axis lies almost on the sphere of the stage's dome, so half of the ring stands out of the dome,
    into the room that the thinned wall of the lid leaves behind the hinge.  The ring is a solid of revolution
    about the hinge axis: its distance from the lid's wall is the same at every opening angle.

    The stage is printed upside down.  The quarter of the ring that lies behind and above the pin would then
    hang in the air; a roof at 45 degrees, from the ring up to the tower, carries it instead."""
    r = P.TOWER_KNUCKLE_R
    c = r * math.sqrt(0.5)
    reach = 2.0                                  # the roof ends this far in front of the axis, inside the tower
    ring = g.cyl_y(r, y0, y1, HX, HZ)
    roof = g.prism_xz([(HX - c, HZ + c), (HX + reach, HZ + c + (reach + c)), (HX + reach, HZ), (HX, HZ)], y0, y1)
    return ring.fuse(roof)


def _hinge_towers() -> cq.Shape:
    out = None
    inside = g.inter(g.sphere(P.R_STAGE - 0.01), g.slab(0, P.Z_DECK - 0.01))
    fx0, fx1 = P.YOKE_FOOT_X
    for sy in (1, -1):
        y0, y1 = (TOWER_Y0, TOWER_Y1) if sy > 0 else (-TOWER_Y1, -TOWER_Y0)
        arm = g.box(HX, HX + fx1, y0, y1, HZ - P.TOWER_KNUCKLE_R, P.Z_DECK)      # the foot is flush with its front
        # the pin on which the spring's forward leg rests passes through a foot under each tower
        foot = g.box(HX + fx0, HX + fx1, y0, y1, P.YOKE_FOOT_Z, HZ)
        # round the hole the foot is thicker than the tower, towards the middle of the hinge.  The stage is
        # printed upside down: the slope at the upper end of the added thickness carries it there
        ya, yb = sy * (TOWER_Y0 + 0.01), sy * FOOT_Y0
        foot = foot.fuse(g.prism_yz([(ya, P.YOKE_FOOT_Z), (yb, P.YOKE_FOOT_Z), (yb, P.YOKE_FOOT_PAD_Z), (ya, P.YOKE_FOOT_PAD_Z + P.YOKE_FOOT_PAD + 0.01)], HX + fx0, HX + fx1))
        # a buttress on the outside ties the thin tower to the deck.  It begins in front of the hinge axis, so
        # that the room beside the knuckle, where the pins wait and the tools come in, stays free
        brace = g.prism_yz([(sy * TOWER_Y1, HZ + 1.0), (sy * (TOWER_Y1 + P.TOWER_BRACE_W), P.Z_DECK), (sy * TOWER_Y1, P.Z_DECK)], HX + P.TOWER_BRACE_X, HX + fx1)
        # arm, foot and buttress end at the dome of the stage; the knuckle does not: it has to enclose the pin
        tower = g.inter(arm.fuse(foot).fuse(brace), inside).fuse(tower_knuckle(y0, y1))
        out = tower if out is None else out.fuse(tower)
    # end stop: the lid's stop tabs land on this beam at LID_OPEN_DEG
    a_open = math.radians(P.LID_TAB_DEG + P.LID_OPEN_DEG)
    ux, uz = math.cos(a_open), math.sin(a_open)          # tab direction when open
    nx, nz = -uz, ux                                      # normal on its leading face
    p1 = (HX + 4.5 * ux + 1.5 * nx, HZ + 4.5 * uz + 1.5 * nz)
    p2 = (HX + (P.LID_TAB_LEN + 0.5) * ux + 1.5 * nx, HZ + (P.LID_TAB_LEN + 0.5) * uz + 1.5 * nz)
    stop = g.prism_xz([p1, p2, (p2[0], p2[1] + 1.2), (HX + 1.0, p2[1] + 1.2), (HX + 1.0, p1[1] + 0.7)], -TOWER_Y0, TOWER_Y0)
    return out.fuse(stop)


def yoke_pin() -> cq.Shape:
    """The steel pin on which the spring's forward leg rests."""
    return g.cyl_y(P.YOKE_PIN_D / 2, -P.YOKE_PIN_L / 2, P.YOKE_PIN_L / 2, HX + P.YOKE_X, YOKE_PIN_Z)


def stop_contact_ok() -> float:
    """Height of the stop beam's lower corner above the hinge axis (for reports)."""
    a_open = math.radians(P.LID_TAB_DEG + P.LID_OPEN_DEG)
    return 4.5 * math.sin(a_open) + 1.5 * math.cos(a_open)


def rp_point(r: float, az: float) -> tuple[float, float]:
    """The point at distance ``r`` from the pivot of the ring pawl in the direction ``az`` (degrees from +X)."""
    return (RPX + r * math.cos(math.radians(az)), RPY + r * math.sin(math.radians(az)))


def rp_az(x: float) -> float:
    """Direction, seen from the pivot of the ring pawl, in which the middle line of its finger crosses the
    plane ``x``.  The finger lies on the -Y side of the pivot, so the angle is negative."""
    return -math.degrees(math.acos((x - RPX) / RPAWL_R))


def rp_az_end() -> float:
    """Direction of the end of the finger when the pawl is locked."""
    return rp_az(RING_SLOT_X1 + P.RPAWL_FINGER_BEYOND)


def _rp_sector(profile, az0: float, az1: float) -> cq.Shape:
    """Revolve an (r, z) profile about the pivot of the ring pawl, from direction ``az0`` to ``az1``."""
    return g.move(_sector(profile, (az0 + az1) / 2, (az1 - az0) / 2), RPX, RPY, 0.0)


def ring_finger_window() -> cq.Shape:
    """What is cut out of the two walls of the slot for the finger of the ring pawl: the band that the finger
    sweeps about its pivot, with RPAWL_CL of room on each side and below it.  Above, the windows end at the
    deck, against which the finger is pressed when someone pulls at a locked ring."""
    cl = P.RPAWL_CL
    r0, r1 = RPAWL_R - P.RPAWL_FINGER_W / 2 - cl, RPAWL_R + P.RPAWL_FINGER_W / 2 + cl
    x0, x1 = RING_SLOT_X0 - P.RING_SLOT_WALL - 0.5, RING_SLOT_X1 + P.RING_SLOT_WALL + 0.5
    return _rp_sector([(r0, RPAWL_Z0 - cl), (r1, RPAWL_Z0 - cl), (r1, DECK_BOTTOM + 0.02), (r0, DECK_BOTTOM + 0.02)], rp_az(x0) - 2.0, rp_az(x1) + 2.0)


def ring_slot_void() -> cq.Shape:
    """What is cut out of the stage for the ring: a slot of RING_SLOT_W with a round bottom of RING_SLOT_D;
    where it is deeper than its radius, its ends stand upright above the round."""
    r = P.RING_SLOT_D / 2
    void = g.cyl_x(r, RING_SLOT_X0, RING_SLOT_X1, 0.0, RING_SLOT_ZC)
    return void.fuse(g.box(RING_SLOT_X0, RING_SLOT_X1, -r, r, RING_SLOT_ZC, P.Z_DECK + 1.0))


def _ring_slot_walls() -> cq.Shape:
    """What hangs under the deck round the slot of the ring: a wall before it, a wall behind it and a floor
    under it, together a segment of a disc, with the two windows for the finger of the ring pawl.  The slot
    itself is cut afterwards, through the deck as well.  The stage is printed upside down: the segment then
    stands on the deck and closes like a dome, and the bottom of the slot is a bridge of RING_SLOT_W."""
    x0, x1 = RING_SLOT_X0 - P.RING_SLOT_WALL, RING_SLOT_X1 + P.RING_SLOT_WALL
    r = P.RING_SLOT_D / 2 + P.RING_SLOT_FLOOR
    solid = g.cyl_x(r, x0, x1, 0.0, RING_SLOT_ZC).fuse(g.box(x0, x1, -r, r, RING_SLOT_ZC, P.Z_DECK))
    walls = g.inter(solid, g.box(x0 - 1.0, x1 + 1.0, -40.0, 40.0, 0.0, DECK_BOTTOM + 0.01))
    return walls.cut(ring_finger_window())


def rp_turned(x: float, y: float, deg: float) -> tuple[float, float]:
    """The point (x, y) of the ring pawl when the pawl has turned ``deg`` towards release (clockwise from above)."""
    a = math.radians(-deg)
    dx, dy = x - RPX, y - RPY
    return (RPX + dx * math.cos(a) - dy * math.sin(a), RPY + dx * math.sin(a) + dy * math.cos(a))


def ring_knob_at() -> tuple[float, float]:
    """Axis of the knob of the locked ring pawl."""
    return rp_point(P.RPAWL_KNOB_R, P.RPAWL_TAIL_DEG)


def ring_pin_at() -> tuple[float, float]:
    """Axis of the counterweight pin of the locked ring pawl."""
    return (RPX + P.RPAWL_PIN_AT[0], RPY + P.RPAWL_PIN_AT[1])


def ring_knob_slit() -> cq.Shape:
    """The curved slit in the deck through which the knob of the ring pawl stands up: the band that the knob
    sweeps about the pivot from locked to RPAWL_MOUNT_DEG, with RPAWL_CL of room all round."""
    rk = P.RPAWL_KNOB_D / 2 + P.RPAWL_CL
    r0, r1 = P.RPAWL_KNOB_R - rk, P.RPAWL_KNOB_R + rk
    z0, z1 = DECK_BOTTOM - 1.0, P.Z_DECK + 1.0
    a0, a1 = P.RPAWL_TAIL_DEG - P.RPAWL_MOUNT_DEG, P.RPAWL_TAIL_DEG
    slit = _rp_sector([(r0, z0), (r1, z0), (r1, z1), (r0, z1)], a0, a1)
    for a in (a0, a1):
        x, y = rp_point(P.RPAWL_KNOB_R, a)
        slit = slit.fuse(g.cyl_z(rk, z0, z1, x, y))
    return slit


def ring_pawl_stop() -> cq.Shape:
    """The stop of the locked ring pawl: a pad on the rear wall of the slot, beside the window, against which
    the arm of the pawl lies when the spring has turned the finger home."""
    hw = P.RPAWL_ARM_W / 2
    return g.box(P.RPAWL_ARM_X + hw, RING_SLOT_X0 - P.RING_SLOT_WALL + 0.01, 7.5, 11.5, RPAWL_Z0 - 0.5, DECK_BOTTOM + 0.01)


def ring_spring_nub(deg: float = 0.0) -> tuple[float, float]:
    """The point of the tail on which the return spring bears: on the round about the knob, on the side to
    which the tail goes when the ring is freed.  ``deg``: the pawl turned that far towards release."""
    kx, ky = ring_knob_at()
    a = math.radians(P.RPAWL_TAIL_DEG)
    x, y = kx + P.RPAWL_TAIL_END_R * math.sin(a), ky - P.RPAWL_TAIL_END_R * math.cos(a)
    return rp_turned(x, y, deg) if deg else (x, y)


def ring_spring_axis() -> tuple[float, float]:
    """Direction of the return spring, from the tail to the floor of its cup: along the way that the point on
    which it bears goes from locked to released.  The spring then stays straight while it is pressed."""
    (x0, y0), (x1, y1) = ring_spring_nub(), ring_spring_nub(P.RPAWL_RELEASE_DEG)
    d = math.hypot(x1 - x0, y1 - y0)
    return ((x1 - x0) / d, (y1 - y0) / d)


def ring_spring_seat() -> tuple[float, float, float]:
    """Middle of the floor of the cup of the ring pawl's return spring."""
    (x0, y0), (ux, uy) = ring_spring_nub(), ring_spring_axis()
    return (x0 + P.RPAWL_SPRING_REST * ux, y0 + P.RPAWL_SPRING_REST * uy, RPAWL_SPRING_Z)


def ring_spring_cup() -> cq.Shape:
    """Seat of the return spring of the ring pawl under the deck: a cup like that of the latch, turned so that
    it opens along the way of the tail.  In the print it stands on the deck and its floor is a short bridge."""
    gx, gy, z = ring_spring_seat()
    ux, uy = ring_spring_axis()
    depth, r, wall = 3.0, 2.6, 1.0                     # how far the spring reaches into the cup; room for a spring of up to 4.6 mm
    outer = g.box(-depth, 2.0, -r - wall, r + wall, z - r - wall, DECK_BOTTOM + 0.01)
    inner = g.box(-depth - 0.01, 0.0, -r, r, z - r, DECK_BOTTOM + 0.02)
    cup = g.rot(outer.cut(inner), "z", math.degrees(math.atan2(uy, ux)))
    return g.move(cup, gx, gy, 0.0)


def ring_pilot_end() -> float:
    """Height at which the pilot hole of the ring pawl's pivot screw ends: 0.3 mm above the end of the screw
    under the thinnest washer."""
    return RPAWL_Z0 - P.M2_WASHER_T + P.RPAWL_SCREW_L + 0.3


def pawl_spring_cup() -> cq.Shape:
    """Seat of the pawl's return spring under the deck: a cup that holds the end of the spring on all sides.
    The stage is printed upside down; the cup then stands on the deck and its floor is a short bridge."""
    x, z, y0 = PAWL_SPRING_X, PAWL_SPRING_Z, P.PAWL_SPRING_SEAT_Y
    depth, r, wall = 3.0, 2.6, 1.0                     # how far the spring reaches into the cup; room for a spring of up to 4.6 mm
    outer = g.box(x - r - wall, x + r + wall, y0 - depth, y0 + 2.0, z - r - wall, DECK_BOTTOM + 0.01)
    inner = g.box(x - r, x + r, y0 - depth - 0.01, y0, z - r, DECK_BOTTOM + 0.02)
    return outer.cut(inner)


@lru_cache(maxsize=None)
def stage() -> cq.Shape:
    body = _stage_shell()
    body = body.fuse(_screw_pads())
    # Room for the rim of the lid at the back, which swings forwards about the hinge before it rises: round the
    # hinge a cylinder, and beside it whatever the lip of the lid sweeps, for a lid that stands as far to one
    # side as the play of its hinge lets it
    relief = g.cyl_y(P.BACK_RELIEF_R, -P.BACK_RELIEF_Y, P.BACK_RELIEF_Y, HX, HZ)
    relief = relief.fuse(S.lip_swing_tool(P.LIP_SWING_CL, P.LID_SIDE_PLAY, P.R_CORE + 0.1))
    behind = g.box(-60, HX, -P.BACK_RELIEF_Y, P.BACK_RELIEF_Y, -1, HZ)
    # under that cylinder the base ring would be left as two thin blades that run out to nothing: they go as well
    blades = g.box(-60, HX + P.BACK_RELIEF_R + 1.5, -P.BACK_RELIEF_Y, P.BACK_RELIEF_Y, -1, P.HB + 0.1)
    body = body.cut(relief).cut(behind).cut(blades)
    # the collar is not relieved: it is the guide.  It ends where the lip begins to swing inwards
    body = body.fuse(_collar())
    body = body.fuse(hook_guide())
    body = body.fuse(_hinge_towers())
    body = body.cut(g.cyl_y(P.HINGE_SLIDE / 2, -30, 30, HX, HZ))    # the two hinge pins slide in the towers
    y_w = TOWER_Y1 + 1.0
    body = body.cut(g.cyl_y(P.YOKE_HOLE / 2, -y_w, y_w, HX + P.YOKE_X, YOKE_PIN_Z))    # the pin under the spring's leg
    # ... which the feet hold in the thickness of the towers only: in what the feet are thicker, the hole is wider
    body = body.cut(g.cyl_y(P.YOKE_FREE / 2, -TOWER_Y0, TOWER_Y0, HX + P.YOKE_X, YOKE_PIN_Z))

    # The slot of the ring is cut into the stage itself: through the deck, and below it between two walls and a
    # floor that hang under the deck.  Its bottom is round
    body = body.fuse(_ring_slot_walls())
    body = body.cut(ring_slot_void())
    # the ring pawl: the slit for its knob through the deck, and under the deck its pivot boss, the pad on
    # which its arm rests when it is locked, and the cup of its return spring
    body = body.cut(ring_knob_slit())
    body = body.fuse(g.cyl_z(P.PAWL_BOSS_D / 2, RPAWL_Z0, DECK_BOTTOM + 0.01, RPX, RPY))
    body = body.fuse(ring_pawl_stop()).fuse(ring_spring_cup())
    # its pivot screw forms its own thread in the boss, like that of the latch pawl
    body = body.cut(g.cyl_z(P.M2_PILOT_FLAT / 2, RPAWL_Z0 - 1, ring_pilot_end(), RPX, RPY))
    body = body.cut(g.cone_z(P.M2_PILOT_FLAT / 2 + P.M2_LEAD, P.M2_PILOT_FLAT / 2, RPAWL_Z0 - 0.001, RPAWL_Z0 + P.M2_LEAD, RPX, RPY))

    # latch: pivot boss, stop pin and the seat of the return spring hang from the deck underside
    px, py = P.PAWL_PIVOT
    z_cap = P.PAWL_Z0 - P.PAWL_PLAY                    # end of the boss; the washer under the pawl lies against it
    boss = g.cyl_z(P.PAWL_BOSS_D / 2, z_cap, DECK_BOTTOM + 0.01, px, py)
    tail_x = px - P.PAWL_TAIL_X
    stop_pin = g.cyl_z(1.5, z_cap, DECK_BOTTOM + 0.01, tail_x, -4.1)
    body = body.fuse(boss).fuse(stop_pin).fuse(pawl_spring_cup())
    # the pivot screw forms its own thread in the boss; the mouth of the hole is at the top of the print
    body = body.cut(g.cyl_z(P.M2_PILOT_FLAT / 2, z_cap - 1, DECK_BOTTOM + 1.2, px, py))
    body = body.cut(g.cone_z(P.M2_PILOT_FLAT / 2 + P.M2_LEAD, P.M2_PILOT_FLAT / 2, z_cap - 0.001, z_cap + P.M2_LEAD, px, py))

    # openings: screws, lid hook, bezel tube, band lugs
    for az in P.SCREW_AZ:
        bx, by = g.polar(P.SCREW_R, az)
        body = body.cut(g.cyl_z(P.M3_HEAD_D / 2, P.STAGE_PAD_Z, 60, bx, by))
        body = body.cut(g.cyl_z(P.M3_CLEAR / 2, -1, 60, bx, by))
        body = body.cut(band_lug(az, 0.15))
    body = body.cut(hook_slot())
    body = body.cut(S._bezel_cut(P.CL))
    return g.clean(body)


# --------------------------------------------------------------------------
# chassis
# --------------------------------------------------------------------------
def _usb_frame(shape: cq.Shape) -> cq.Shape:
    """Move a shape built along +X (radial, outwards) to the USB azimuth."""
    return g.rot(shape, "z", P.USB_AZ)


def tp4056_centre_r() -> float:
    return P.TP_TIP_R - 1.2 - P.TP_L / 2


def tp4056_z() -> float:
    """Underside of the TP4056 PCB."""
    return P.USB_Z - P.USB_H / 2 - 1.0


def _cradle_solid() -> cq.Shape:
    cx, cz = P.CELL_AXIS
    half = P.CELL_L / 2 + P.CELL_CONTACT + P.CRADLE_WALL
    ro = P.CELL_BORE / 2 + P.CRADLE_WALL
    low = g.box(cx - ro, cx + ro, -half, half, P.Z_PLATE_TOP - 0.01, cz)
    snap = g.box(cx - ro, cx + ro, -15.0, 15.0, cz, cz + P.CELL_SNAP)
    ends = None
    for sy in (1, -1):
        y0 = sy * (half - P.CRADLE_WALL) if sy > 0 else -half
        y1 = half if sy > 0 else -(half - P.CRADLE_WALL)
        end = g.cyl_y(ro, y0, y1, cx, cz).fuse(g.box(cx - ro, cx + ro, y0, y1, P.Z_PLATE_TOP, cz))
        ends = end if ends is None else ends.fuse(end)
    return low.fuse(snap).fuse(ends)


def _cradle_cuts() -> cq.Shape:
    cx, cz = P.CELL_AXIS
    inner = P.CELL_L / 2 + P.CELL_CONTACT
    bore = g.cyl_y(P.CELL_BORE / 2, -inner, inner, cx, cz)
    top = g.box(cx - 8.2, cx + 8.2, -inner, inner, cz, cz + 30)       # insertion opening
    relief = g.box(cx - 30, cx + 30, 15.0, inner, cz + 0.01, cz + 30).fuse(g.box(cx - 30, cx + 30, -inner, -15.0, cz + 0.01, cz + 30))
    cuts = bore.fuse(top).fuse(relief)
    for sy in (1, -1):
        # slot for the contact plate and a window for its solder tab
        y0 = sy * inner if sy > 0 else -inner - 0.6
        cuts = cuts.fuse(g.box(cx - 5.3, cx + 5.3, y0, y0 + 0.6, cz - 5.3, cz + 30))
        yw0 = sy * inner if sy > 0 else -inner - P.CRADLE_WALL - 1
        cuts = cuts.fuse(g.box(cx - 2.0, cx + 2.0, yw0, yw0 + P.CRADLE_WALL + 1, cz + 3.0, cz + 30))
    return cuts


def _servo_bay() -> tuple[cq.Shape, cq.Shape]:
    """(material, cuts) of the servo mount.  Servo long axis runs along -Y."""
    sx, sy, bz = P.SERVO_X, P.SERVO_Y, P.SERVO_BASE_Z
    seat = bz + P.SG90_FLANGE_Z                       # underside of the servo flange
    yb0 = sy - (P.SG90_L - P.SG90_SHAFT_OFF) - 0.55   # pocket ends (23.8 long)
    yb1 = sy + P.SG90_SHAFT_OFF + 0.55
    xw = P.SG90_POCKET_W / 2
    post_a = g.box(sx - xw - 1.6, sx + xw + 1.6, yb1, yb1 + 5.0, P.Z_PLATE_TOP - 0.01, seat)
    post_b = g.box(sx - xw - 1.6, sx + xw + 1.6, yb0 - 5.0, yb0, P.Z_PLATE_TOP - 0.01, seat)
    spine = g.box(sx - xw - 1.6, sx - xw, yb0 - 5.0, yb1 + 5.0, P.Z_PLATE_TOP - 0.01, seat - 3.0)
    mat = post_a.fuse(post_b).fuse(spine)
    mid = sy + P.SG90_SHAFT_OFF - P.SG90_L / 2
    cuts = None
    for hy in (mid + P.SG90_HOLE_PITCH / 2, mid - P.SG90_HOLE_PITCH / 2):
        hole = g.cyl_z(0.8, seat - 9.0, seat + 1, sx, hy)
        cuts = hole if cuts is None else cuts.fuse(hole)
    cable = g.box(sx - 2.6, sx + 2.6, yb1 - 0.1, yb1 + 5.1, bz + 2.5, bz + 8.0)
    return mat, cuts.fuse(cable)


def _pocket(cx: float, cy: float, sx: float, sy: float, z0: float, z1: float, wall: float = 1.2) -> tuple[cq.Shape, cq.Shape]:
    """Open-top box (material, cavity) with inner size sx x sy centred at cx, cy."""
    mat = g.box(cx - sx / 2 - wall, cx + sx / 2 + wall, cy - sy / 2 - wall, cy + sy / 2 + wall, P.Z_PLATE_TOP - 0.01, z1)
    cav = g.box(cx - sx / 2, cx + sx / 2, cy - sy / 2, cy + sy / 2, z0, z1 + 5)
    return mat, cav


@lru_cache(maxsize=None)
def chassis() -> cq.Shape:
    zb = P.Z_PLATE_TOP - P.PLATE_T
    wall = P.CHASSIS_WALL
    outer = g.inter(g.inter(g.sphere(P.R_BUCKET), g.cyl_z(P.R_BUCKET_CYL, -60, 10)), g.slab(zb, 0.0))
    inner = g.inter(g.inter(g.sphere(P.R_BUCKET - wall), g.cyl_z(P.R_BUCKET_CYL - wall, -60, 10)), g.slab(P.Z_PLATE_TOP, 10))
    envelope = g.inter(g.inter(g.sphere(P.R_BUCKET - 0.01), g.cyl_z(P.R_BUCKET_CYL - 0.01, -60, 60)), g.slab(zb, 60))
    bucket = outer.cut(inner)
    flange = g.revolve_z(
        [
            (P.R_FLANGE_IN, -P.HB),
            (P.R_BUCKET_CYL - wall + 0.01, -P.HB - (P.R_BUCKET_CYL - wall - P.R_FLANGE_IN)),
            (P.R_BUCKET_CYL - 0.01, -P.HB - (P.R_BUCKET_CYL - wall - P.R_FLANGE_IN)),
            (P.R_BUCKET_CYL - 0.01, 0.0),
            (P.R_FLANGE_IN, 0.0),
        ]
    )
    body = bucket.fuse(flange)
    # the flange is open at the front for the speaker clamp ears and the bezel
    body = body.cut(g.box(28.0, 43.0, -27.0, 27.0, -P.HB - 6.5, 5).cut(g.cyl_z(39.4, -60, 60)))

    # --- material ---------------------------------------------------------
    servo_mat, servo_cut = _servo_bay()
    mx, my, mz = P.MCU_POS
    ax, ay, az_ = P.AMP_POS
    mcu_mat, mcu_cav = _pocket(mx, my, P.XIAO_W + 2.2, P.XIAO_H + 1.2, mz - P.XIAO_L / 2, mz + P.XIAO_L / 2 - 6.0)
    amp_mat, amp_cav = _pocket(ax, ay, P.AMP_W + 2.2, P.AMP_H + 2.0, az_ - P.AMP_L / 2, az_ + P.AMP_L / 2 - 6.0)
    # speaker baffle block with the socket for the bezel tube
    baffle = g.cyl_x(P.BAFFLE_R, P.SPK_X_FRONT, P.BAFFLE_X1, 0, P.SPK_Z)
    foot = g.box(P.SPK_X_FRONT, P.BAFFLE_X1, -15.0, 15.0, P.Z_PLATE_TOP - 0.01, P.SPK_Z)
    socket = g.cyl_x(P.BEZEL_R + 1.3, P.CHAMBER_X1, P.BAFFLE_X1)
    ears = g.cyl_x(3.2, P.SPK_X_FRONT, P.BAFFLE_X1, 22.6, P.SPK_Z).fuse(g.cyl_x(3.2, P.SPK_X_FRONT, P.BAFFLE_X1, -22.6, P.SPK_Z))
    front = baffle.fuse(foot).fuse(socket).fuse(ears)
    # USB charger shelf (built along +X, then turned to the USB azimuth)
    rc, zt = tp4056_centre_r(), tp4056_z()
    shelf = g.box(rc - 2.0, P.R_BUCKET_CYL - wall, -P.TP_W / 2 - 1.4, P.TP_W / 2 + 1.4, zt - 1.6, zt)
    legs = g.box(rc - 2.0, P.R_BUCKET_CYL - wall, -P.TP_W / 2 - 1.4, -P.TP_W / 2 + 0.2, P.Z_PLATE_TOP - 0.01, zt).fuse(
        g.box(rc - 2.0, P.R_BUCKET_CYL - wall, P.TP_W / 2 - 0.2, P.TP_W / 2 + 1.4, P.Z_PLATE_TOP - 0.01, zt)
    )
    lips = g.box(rc - 2.0, P.R_BUCKET_CYL - wall, -P.TP_W / 2 - 1.4, -P.TP_W / 2 - 0.2, zt, zt + 1.4).fuse(
        g.box(rc - 2.0, P.R_BUCKET_CYL - wall, P.TP_W / 2 + 0.2, P.TP_W / 2 + 1.4, zt, zt + 1.4)
    )
    usb_mat = _usb_frame(shelf.fuse(legs).fuse(lips))
    # block behind the inner end of the charger board: takes the push of the USB plug.
    # It stands on the plate behind the battery cradle and never enters the cell's path.
    r_in = rc - P.TP_L / 2
    stop = _usb_frame(g.box(r_in - 6.2, r_in - 0.2, -P.TP_W / 2, P.TP_W / 2, P.Z_PLATE_TOP - 0.01, zt + 1.4))
    behind_cradle = g.box(-60, P.CELL_AXIS[0] - P.CELL_BORE / 2 - P.CRADLE_WALL + 0.05, -60, 60, -60, 60)
    usb_mat = usb_mat.fuse(g.inter(stop, behind_cradle))
    # boost converter shelf
    bx, by, bz = P.BOOST_POS
    boost_mat = g.box(bx - P.BOOST_W / 2 - 1.2, bx + P.BOOST_W / 2 + 1.2, by - P.BOOST_L / 2 - 1.2, by + P.BOOST_L / 2 + 1.2, P.Z_PLATE_TOP - 0.01, bz + 1.5)
    boost_cav = g.box(bx - P.BOOST_W / 2 - 0.2, bx + P.BOOST_W / 2 + 0.2, by - P.BOOST_L / 2 - 0.2, by + P.BOOST_L / 2 + 0.2, bz, bz + 10)
    boost_hollow = g.box(bx - P.BOOST_W / 2 + 1.5, bx + P.BOOST_W / 2 - 1.5, by - P.BOOST_L / 2 + 1.5, by + P.BOOST_L / 2 - 1.5, P.Z_PLATE_TOP, bz - 1.2)

    extra = _cradle_solid().fuse(servo_mat).fuse(mcu_mat).fuse(amp_mat).fuse(front).fuse(usb_mat).fuse(boost_mat)
    body = body.fuse(g.inter(extra, envelope))

    # --- cuts -------------------------------------------------------------
    body = body.cut(_cradle_cuts()).cut(servo_cut).cut(mcu_cav).cut(amp_cav).cut(boost_cav).cut(boost_hollow)
    # servo pocket itself
    sx, sy = P.SERVO_X, P.SERVO_Y
    body = body.cut(
        g.box(sx - P.SG90_POCKET_W / 2, sx + P.SG90_POCKET_W / 2, sy - (P.SG90_L - P.SG90_SHAFT_OFF) - 0.55, sy + P.SG90_SHAFT_OFF + 0.55, P.SERVO_BASE_Z - 0.5, 60)
    )
    # front chamber, bezel socket, emergency clip path, hook clearance
    body = body.cut(g.cyl_x(P.SPK_OPEN_D / 2, P.SPK_X_FRONT - 1, P.CHAMBER_X1, 0, P.SPK_Z))
    body = body.cut(g.cyl_x(P.BEZEL_R + 0.15, P.CHAMBER_X1, 80))
    body = body.cut(g.cyl_x(P.BEZEL_R - P.BEZEL_WALL, P.SPK_X_FRONT - 1, P.CHAMBER_X1 + 1))
    body = body.cut(g.box(P.CHAMBER_X1, P.CHAMBER_X1 + 3.4, -1.7, 1.7, -P.BEZEL_R - 1.5, -P.BEZEL_R + 1))   # bezel key
    body = body.cut(S.emergency_channel(3.0, 30.0))
    body = body.cut(g.box(P.SPK_X_FRONT - 1, P.BAFFLE_X1 + 1, -4.2, 4.2, P.BEZEL_R - 0.5, 60))
    for sgn in (1, -1):
        # the clamp screws form their own thread; these holes lie level in the print
        body = body.cut(g.cyl_x(P.M2_PILOT_SIDE / 2, P.SPK_X_FRONT - 1, P.BAFFLE_X1 + 1, sgn * 22.6, P.SPK_Z))
        body = body.cut(g.cone_x(P.M2_PILOT_SIDE / 2 + P.M2_LEAD, P.M2_PILOT_SIDE / 2, P.SPK_X_FRONT - 0.001, P.SPK_X_FRONT + P.M2_LEAD, sgn * 22.6, P.SPK_Z))
    # USB shelf access through wall and flange
    body = body.cut(_usb_frame(g.box(38.0, 70, -P.TP_W / 2 - 0.2, P.TP_W / 2 + 0.2, zt, 5)))
    # bowl bosses, stack screws
    for az in P.SCREW_AZ:
        bxs, bys = g.polar(P.SCREW_R, az)
        body = body.cut(g.cyl_z(P.BOSS_R + 0.4, -60, -P.HB, bxs, bys))
        web = g.rot(g.box(P.SCREW_R, P.R, -P.BOSS_R - 0.4, P.BOSS_R + 0.4, -60, -P.HB), "z", az)
        body = body.cut(web)
        body = body.cut(g.cyl_z(P.M3_CLEAR / 2, -10, 5, bxs, bys))
    # plate openings: window for the reader harness that comes up from the bowl, cable holes
    body = body.cut(g.box(9.5, 18.0, -11.0, 9.0, zb - 1, P.Z_PLATE_TOP + 0.5))
    body = body.cut(g.cyl_z(3.0, zb - 1, P.Z_PLATE_TOP + 1, 26.0, -18.0))
    body = body.cut(g.cyl_z(3.0, zb - 1, P.Z_PLATE_TOP + 1, -26.0, 14.0))
    return g.clean(body)


# --------------------------------------------------------------------------
# small parts
# --------------------------------------------------------------------------
def pawl_at(deg: float = 0.0, down: bool = False) -> cq.Shape:
    """The latch pawl, rotated by ``deg`` towards release (clockwise from above).  ``down``: lying on its
    washer, where it rests when nothing lifts it, instead of pushed up against the deck."""
    shape = pawl()
    px, py = P.PAWL_PIVOT
    if deg:
        shape = g.rot(shape, "z", -deg, (px, py, 0))
    return g.move(shape, dz=-P.PAWL_PLAY) if down else shape


def pawl_nose() -> tuple[float, float, float, float]:
    """The nose of the pawl in plan: its rear and front end (x), the tip of the tooth it lies over (y) and its
    edge that faces the stem of the hook (y)."""
    y_stem = P.HOOK_Y - P.HOOK_W / 2
    return (P.HOOK_X0 - 0.6, P.HOOK_X1 - 0.5, y_stem - P.TOOTH_REACH, y_stem - P.PAWL_NOSE_GAP)


@lru_cache(maxsize=None)
def pawl() -> cq.Shape:
    """Latch pawl, drawn pushed up against the deck.

    Its nose lies over the tooth of the lid hook.  The underside of the nose is the latch face: it is cut back
    so far that it clears the tooth by LATCH_GAP when the lid is seated, and still clears it when the pawl has
    dropped onto its washer.  The top of the nose slopes down towards the stem, so that a hook that comes down
    beside its place pushes the nose aside instead of landing on it."""
    px, py = P.PAWL_PIVOT
    z0, z1 = P.PAWL_Z0, P.PAWL_Z1
    tail_x = px - P.PAWL_TAIL_X
    nx0, nx1, y_tip, y_edge = pawl_nose()
    # While the lid closes, the hook comes down in an arc: when its lower end passes the pawl it stands up to
    # 1.5 mm further back than when the lid is shut.  The edge of the nose, with its slope, therefore runs on
    # behind the nose, and the flank behind it keeps out of the way of the stem at every angle of the pawl
    x_flank = nx0 - 1.4
    plate = g.prism_xy(
        [
            (tail_x - 2.5, -2.5),
            (tail_x + 2.5, -2.5),
            (px - 2.0, -4.6),
            (nx1 - 1.8, y_tip - 2.2),
            (nx1, y_tip - 0.5),
            (nx1, y_edge),
            (x_flank, y_edge),
            (px + 2.8, 4.0),
            (px - 3.4, 4.2),
            (tail_x + 2.5, 2.5),
            (tail_x - 2.5, 2.5),
        ],
        z0,
        z1,
    )
    hub = g.cyl_z(P.PAWL_BOSS_D / 2 + 2.0, z0, z1, px, py)
    post = g.cyl_z(P.PAWL_POST_R, P.PAWL_POST_Z0, z0 + 0.01, tail_x, 0.0)
    # lug pushed by the emergency paper clip (on the -y side of the pivot).  It is as high as the pawl, so that
    # it stands on the bed when the pawl is printed upside down
    start, direction = S.emergency_axis()
    t = (start.x - (px + 4.6)) / -direction.x
    hit = start + direction * t
    lug = g.box(px + 3.0, px + 5.2, hit.y - 2.2, hit.y + 2.2, hit.z - 1.6, z1)       # it ends behind the path of the tooth
    body = plate.fuse(hub).fuse(post)
    body = body.cut(g.cyl_z(P.PAWL_BORE / 2, z0 - 1, z1 + 1, px, py))
    # the latch face: the underside of the nose
    body = body.cut(g.box(x_flank - 0.2, nx1 + 1.0, y_tip - 4.0, y_edge + 1.0, P.PAWL_POST_Z0 - 1.0, P.PAWL_NOSE_Z0))
    # slope on top of the nose
    ch = P.PAWL_NOSE_CHAMFER
    body = body.cut(g.prism_yz([(y_edge + 0.01, z1 + 0.01), (y_edge + 0.01, z1 - ch), (y_edge - ch, z1 + 0.01)], x_flank - 1.0, nx1 + 1.0))
    # ... and a smaller one under its edge
    ld, zn = P.PAWL_NOSE_LEAD, P.PAWL_NOSE_Z0
    body = body.cut(g.prism_yz([(y_edge + 0.01, zn - 0.01), (y_edge + 0.01, zn + ld), (y_edge - ld, zn - 0.01)], x_flank - 1.0, nx1 + 1.0))
    # ... and on its front, where it passes under the dome of the stage
    body = body.cut(g.prism_xz([(nx1 + 0.01, z1 + 0.01), (nx1 + 0.01, z1 - 1.0), (nx1 - 1.0, z1 + 0.01)], y_tip - 4.0, y_edge + 1.0))
    # the lug comes on after the latch face has been cut: that cut must not take its front away
    body = body.fuse(lug)
    # nub for the return spring on the +y side of the tail
    body = body.fuse(g.cyl_y(1.1, 2.4, 4.0, tail_x, PAWL_SPRING_Z))
    return g.clean(body)


def emergency_hit_point() -> cq.Vector:
    px, _ = P.PAWL_PIVOT
    start, direction = S.emergency_axis()
    t = (start.x - (px + 4.6)) / -direction.x
    return start + direction * t


def ring_pawl_at(deg: float = 0.0, up: bool = False) -> cq.Shape:
    """The ring pawl, turned by ``deg`` towards release (clockwise from above).  ``up``: pushed up against the
    deck, as when someone pulls at a locked ring, instead of lying on its washer."""
    shape = ring_pawl()
    if deg:
        shape = g.rot(shape, "z", -deg, (RPX, RPY, 0))
    return g.move(shape, dz=P.RPAWL_PLAY) if up else shape


def _hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Convex hull of points in the plane, counter-clockwise."""
    pts = sorted(set((round(x, 6), round(y, 6)) for x, y in points))

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and (out[-1][0] - out[-2][0]) * (p[1] - out[-2][1]) - (out[-1][1] - out[-2][1]) * (p[0] - out[-2][0]) <= 0:
                out.pop()
            out.append(p)
        return out[:-1]

    return half(pts) + half(reversed(pts))


def _round(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(0, 360, 6)]


def _ring_tail_outline() -> list[tuple[float, float]]:
    """The tail of the ring pawl in plan: a bar from the hub to the round about the knob, with a flat for the
    end of the spring."""
    fx, fy = ring_spring_nub()
    ux, uy = ring_spring_axis()
    flat = [(fx - uy * s, fy + ux * s) for s in (-2.4, 2.4)]                 # square to the spring
    return _hull(flat + _round(RPX, RPY, P.PAWL_BOSS_D / 2 + 2.0) + _round(*ring_knob_at(), P.RPAWL_TAIL_END_R))


def _ring_pin_outline() -> list[tuple[float, float]]:
    """The round beside the hub that holds the counterweight pin, in plan."""
    return _hull(_round(RPX, RPY, P.PAWL_BOSS_D / 2 + 2.0) + _round(*ring_pin_at(), P.RPAWL_PIN_BOSS_R))


@lru_cache(maxsize=None)
def ring_pawl() -> cq.Shape:
    """The ring pawl, locked and lying on its washer.

    Its pivot lies in the plane of the ring, beyond the end of the slot.  The arm leaves the hub towards the
    back, runs behind the rear wall of the slot to its middle and there carries the finger: a piece of a ring
    about the pivot, which therefore slides in its own track and crosses the slot square.  Locked, the finger
    passes through the window of the rear wall, across the slot and through the ring, and into the window of
    the front wall.  Its lower edges are sloped, because the inside of a ring is round, and its end is
    tapered, so that it finds a window again that it has left.

    The tail lies on the other side of the pivot: a bar that carries the knob, a post that stands up through
    the slit in the deck, and the flat and the nub on which the return spring bears.  A round beside the hub
    holds the counterweight pin, which is placed so that the whole pawl balances about its pivot.

    Everything on its underside lies in one plane: it is printed as it lies, knob up."""
    z0, z1 = RPAWL_Z0, RPAWL_Z1
    hw = P.RPAWL_ARM_W / 2
    r0, r1 = RPAWL_R - P.RPAWL_FINGER_W / 2, RPAWL_R + P.RPAWL_FINGER_W / 2
    c = P.RPAWL_FINGER_CHAMFER
    az_end = rp_az_end()
    xb = P.RPAWL_ARM_X
    hub = g.cyl_z(P.PAWL_BOSS_D / 2 + 2.0, z0, z1, RPX, RPY)
    # the arm: from the hub towards the back, then along the rear wall of the slot to its middle
    y_south = RPY - math.sqrt(r1**2 - (xb + hw - RPX) ** 2) - 0.4          # it ends just beyond the root of the finger
    neck = g.box(xb - hw, RPX, RPY - hw, RPY + hw, z0, z1)
    bar = g.box(xb - hw, xb + hw, y_south, RPY + hw, z0, z1)
    finger = _rp_sector([(r0, z0 + c), (r0 + c, z0), (r1 - c, z0), (r1, z0 + c), (r1, z1), (r0, z1)], rp_az(xb - hw + 0.5), az_end)
    tail = g.prism_xy(_ring_tail_outline(), z0, z1)
    body = hub.fuse(neck).fuse(bar).fuse(finger).fuse(tail)
    if P.RPAWL_PIN:
        body = body.fuse(g.prism_xy(_ring_pin_outline(), z0, z1))
    # taper of the finger's end, in plan: over its last 2 mm it narrows to 2 mm
    back = math.degrees(2.0 / RPAWL_R)
    side = (P.RPAWL_FINGER_W - 2.0) / 2
    for r_edge, sgn in ((r0, 1.0), (r1, -1.0)):
        wedge = [rp_point(r_edge - sgn * 0.2, az_end + 1.0), rp_point(r_edge - sgn * 0.2, az_end - back), rp_point(r_edge + sgn * side, az_end + 1.0)]
        body = body.cut(g.prism_xy(wedge, z0 - 1.0, z1 + 1.0))
    # the knob
    kx, ky = ring_knob_at()
    rk, zk = P.RPAWL_KNOB_D / 2, P.Z_DECK + P.RPAWL_KNOB_H
    body = body.fuse(g.cyl_z(rk, z1 - 0.01, zk - 0.6, kx, ky)).fuse(g.cone_z(rk, rk - 0.6, zk - 0.601, zk, kx, ky))
    # nub for the return spring, in line with the spring
    fx, fy = ring_spring_nub()
    ux, uy = ring_spring_axis()
    nub = g.rot(g.cyl_x(1.1, -0.3, 1.6, 0.0, RPAWL_SPRING_Z), "z", math.degrees(math.atan2(uy, ux)))
    body = body.fuse(g.move(nub, fx, fy, 0.0))
    body = body.cut(g.cyl_z(P.PAWL_BORE / 2, z0 - 1, z1 + 1, RPX, RPY))
    if P.RPAWL_PIN:                                   # the hole of the counterweight pin
        nx, ny = ring_pin_at()
        body = body.cut(g.cyl_z(P.RPAWL_PIN_HOLE / 2, z0 - 1, z1 + 1, nx, ny))
    return g.clean(body)


def ring_pawl_pin(deg: float = 0.0, up: bool = False) -> cq.Shape:
    """The counterweight pin in the tail of the ring pawl: its top flush with the top of the pawl."""
    nx, ny = rp_turned(*ring_pin_at(), deg)
    top = RPAWL_Z1 + (P.RPAWL_PLAY if up else 0.0)
    return g.cyl_z(P.RPAWL_PIN_D / 2, top - P.RPAWL_PIN_L, top, nx, ny)


def ring_spring_span(deg: float = 0.0) -> float:
    """Length of the return spring of the ring pawl, from the tail to the floor of its cup, with the pawl
    turned by ``deg`` towards release."""
    (x, y), (gx, gy, _) = ring_spring_nub(deg), ring_spring_seat()
    return math.hypot(gx - x, gy - y)


@lru_cache(maxsize=None)
def sleeve(od: float = P.SLEEVE_OD, press: float = P.HINGE_PRESS) -> cq.Shape:
    """Mandrel of the torsion spring, and what keeps the two hinge pins: each pin is pressed into a blind hole
    at one end and stands on its floor.  The sleeve is as long as the gap between the ribs of the lid lets it
    be, so it cannot leave that gap and the pins cannot leave the hinge.  A funnel leads each pin in."""
    half, r = SLEEVE_HALF, press / 2                  # ``press``: another diameter for the two blind holes than the model's
    body = g.cyl_y(od / 2, -half, half, HX, HZ)
    body = body.cut(g.cyl_y(r, half - P.SLEEVE_BLIND, half + 1.0, HX, HZ)).cut(g.cyl_y(r, -half - 1.0, -half + P.SLEEVE_BLIND, HX, HZ))
    body = body.cut(g.cone_y(r + P.SLEEVE_LEAD_R, r, -half - 0.001, -half + P.SLEEVE_LEAD, HX, HZ))
    body = body.cut(g.cone_y(r, r + P.SLEEVE_LEAD_R, half - P.SLEEVE_LEAD, half + 0.001, HX, HZ))
    return g.clean(body)


def hinge_pin_span(parked: bool = False) -> tuple[float, float]:
    """Distance from the middle of the hinge to the inner and the outer end of a hinge pin.  ``parked``: as it
    waits in its tower while the lid is put on, flush with the tower's inner face."""
    if parked:
        return (TOWER_Y0, TOWER_Y0 + P.HINGE_PIN_L)
    return (P.HINGE_PIN_Y0, P.HINGE_PIN_Y1)


@lru_cache(maxsize=None)
def spk_clamp() -> cq.Shape:
    x1 = P.SPK_X_FRONT - P.SPK_RIM_T
    x0 = x1 - 2.0
    ring = g.cyl_x(P.BAFFLE_R, x0, x1, 0, P.SPK_Z).cut(g.cyl_x(P.SPK_BASKET_D / 2 + 0.5, x0 - 1, x1 + 1, 0, P.SPK_Z))
    rim = g.cyl_x(P.BAFFLE_R, x1, P.SPK_X_FRONT, 0, P.SPK_Z).cut(g.cyl_x(P.SPK_D / 2 + 0.25, x0, P.SPK_X_FRONT + 1, 0, P.SPK_Z))
    body = ring.fuse(rim)
    for sgn in (1, -1):
        body = body.fuse(g.cyl_x(3.2, x0, P.SPK_X_FRONT, sgn * 22.6, P.SPK_Z))
    for sgn in (1, -1):
        body = body.cut(g.cyl_x(P.M2_CLEAR / 2, x0 - 1, P.SPK_X_FRONT + 1, sgn * 22.6, P.SPK_Z))
    body = body.cut(g.cyl_x(P.SPK_D / 2 + 0.25, x1, P.SPK_X_FRONT + 1, 0, P.SPK_Z))
    body = body.cut(g.cyl_x(P.SPK_BASKET_D / 2 + 0.5, x0 - 1, x1 + 1, 0, P.SPK_Z))
    body = body.cut(g.box(x0 - 1, P.SPK_X_FRONT + 1, 11.0, 19.5, P.SPK_Z - 3.0, P.SPK_Z + 3.0))   # solder tags
    return g.clean(body)


@lru_cache(maxsize=None)
def pawl_cap() -> cq.Shape:
    """Printed washer of the pawl pivot.  Its flange lies against the end of
    the pivot boss and keeps the pawl on it; a standard M2 washer is only 5 mm
    across and would slip through the pawl's bore.  Its hub fills the rest of
    the length of an M2 x 6 screw."""
    px, py = P.PAWL_PIVOT
    z1 = P.PAWL_Z0 - P.PAWL_PLAY                 # end of the pivot boss
    z0 = z1 - P.PAWL_CAP_T
    body = g.cyl_z(P.PAWL_CAP_D / 2, z0, z1, px, py).fuse(g.cyl_z(P.PAWL_CAP_HUB_D / 2, z0 - P.PAWL_CAP_HUB_T, z0 + 0.01, px, py))
    return g.clean(body.cut(g.cyl_z(P.M2_CLEAR / 2, z0 - P.PAWL_CAP_HUB_T - 1, z1 + 1, px, py)))


M2_COUPON_STEP = 0.1                              # the test holes differ by this much


@lru_cache(maxsize=None)
def m2_coupon() -> cq.Shape:
    """Test piece for the M2 pilot holes, in its own coordinates and print
    orientation.  Three holes from the top (mouth parallel to the bed) and
    three through its side (mouth in an upright wall), each the model's value
    and one step either side.  The smallest of each three is nearest to the
    cut-off corner."""
    body = g.box(0.0, 37.0, 0.0, 12.0, 0.0, 8.0)
    body = body.cut(g.prism_xy([(-1.0, -1.0), (3.5, -1.0), (-1.0, 3.5)], -1.0, 9.0))
    for i, x in enumerate((5.0, 11.0, 17.0)):
        d = P.M2_PILOT_FLAT + (i - 1) * M2_COUPON_STEP
        body = body.cut(g.cyl_z(d / 2, 2.0, 9.0, x, 6.0))
        body = body.cut(g.cone_z(d / 2, d / 2 + P.M2_LEAD, 8.0 - P.M2_LEAD, 8.001, x, 6.0))
    for i, x in enumerate((23.0, 28.0, 33.0)):
        d = P.M2_PILOT_SIDE + (i - 1) * M2_COUPON_STEP
        body = body.cut(g.cyl_y(d / 2, -1.0, 13.0, x, 4.0))
    return g.clean(body)


PIN_COUPON_PRESS = (-0.05, 0.0, 0.05, 0.10)       # the upright test holes, as differences from HINGE_PRESS
PIN_COUPON_SLIDE = (-0.10, 0.0, 0.10)             # the level test holes, as differences from HINGE_SLIDE


@lru_cache(maxsize=None)
def pin_coupon() -> cq.Shape:
    """Test piece for the two fits of the Ø2 hinge pins, in its own coordinates and print orientation.

    Four posts as thick as the spring sleeve, each with a blind hole from the top like those of the sleeve
    (upright in the print, with the same funnel and depth): the press fit.  One wall as thick as a hinge
    tower with three holes through it (level in the print, as in the stage): the sliding fit.  The holes grow
    from the cut-off corner onwards; the second post and the middle hole of the wall have the model's values."""
    plate = 1.6
    body = g.box(0.0, 42.0, 0.0, 13.0, 0.0, plate)
    body = body.cut(g.prism_xy([(-1.0, -1.0), (3.5, -1.0), (-1.0, 3.5)], -1.0, 20.0))
    top = plate + 4.4
    for i, dd in enumerate(PIN_COUPON_PRESS):
        x, r = 5.5 + 5.5 * i, (P.HINGE_PRESS + dd) / 2
        body = body.fuse(g.cyl_z(P.SLEEVE_OD / 2, plate - 0.01, top, x, 4.5))
        body = body.cut(g.cyl_z(r, top - P.SLEEVE_BLIND, top + 1.0, x, 4.5))
        body = body.cut(g.cone_z(r, r + P.SLEEVE_LEAD_R, top - P.SLEEVE_LEAD, top + 0.001, x, 4.5))
    z_hole = plate + 4.0
    y0 = 8.5
    body = body.fuse(g.box(26.5, 41.0, y0, y0 + P.TOWER_T, plate - 0.01, z_hole + 3.0))
    for i, dd in enumerate(PIN_COUPON_SLIDE):
        x = 29.5 + 4.25 * i
        body = body.cut(g.cyl_y((P.HINGE_SLIDE + dd) / 2, y0 - 1.0, y0 + P.TOWER_T + 1.0, x, z_hole))
    return g.clean(body)


@lru_cache(maxsize=None)
def insert_test() -> cq.Shape:
    """Test piece for the heat-set inserts, in its own coordinates and print
    orientation: one boss as at the rim of the bowl and one as low on its
    front wall, each with the hole of the bowl, on a small plate."""
    body = g.box(0.0, 24.0, 0.0, 12.0, 0.0, 1.2)
    for x, depth in ((6.5, P.M3_INSERT_DEPTH), (17.5, P.BASE_INSERT_DEPTH)):
        top = 1.2 + depth + 1.0
        body = body.fuse(g.cyl_z(P.BOSS_R, 0.0, top, x, 6.0))
        body = body.cut(g.cyl_z(P.M3_INSERT_HOLE / 2, top - depth, top + 1.0, x, 6.0))
    return g.clean(body)
