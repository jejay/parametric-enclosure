"""Printed parts inside the ball.

stage         black inner dome: ring deck, hinge towers, latch pivot, lid collar
chassis       bucket carrying battery, servo, boards and the speaker baffle
pawl          latch pawl released by the servo
cradle        ring seat (exchangeable, fitted to the actual ring)
slider        knob of the ring lock pin
sleeve        mandrel sleeve between hinge pin and torsion spring
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
TOWER_Y0 = P.SPRING_SLOT / 2 + P.LID_RIB_T + 0.2      # inner face of a hinge tower
TOWER_Y1 = P.HINGE_W / 2                               # outer face of a hinge tower
DECK_BOTTOM = P.Z_DECK - P.DECK_T


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


def hook_sweep(grow: float) -> cq.Shape:
    """Ring sector about the hinge axis swept by the lid hook while opening."""
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
    y0 = P.HOOK_Y - P.HOOK_W / 2 - P.TOOTH_REACH - grow
    y1 = P.HOOK_Y + P.HOOK_W / 2 + grow
    return g.prism_xz(pts, y0, y1)


# --------------------------------------------------------------------------
# stage
# --------------------------------------------------------------------------
def _stage_shell() -> cq.Shape:
    r_deck = math.sqrt(P.R_STAGE**2 - P.Z_DECK**2)
    dome = g.ball_zone(P.R_STAGE, P.RI_STAGE, P.HB, P.Z_DECK)
    deck = g.cyl_z(r_deck, DECK_BOTTOM, P.Z_DECK)
    z_ch = P.HB + P.COLLAR_H
    r_top = 45.4
    ring_back = g.revolve_z(
        [(44.4, 0.0), (P.R_CORE, 0.0), (P.R_CORE, P.HB), (r_top, P.HB + (P.R_CORE - r_top)), (44.4, P.HB + (P.R_CORE - r_top))]
    )
    collar = _sector(
        [(44.4, 0.0), (P.R_CORE, 0.0), (P.R_CORE, P.HB), (P.R_COLLAR, P.HB), (P.R_COLLAR, z_ch), (r_top, z_ch + (P.R_COLLAR - r_top)), (44.4, z_ch + (P.R_COLLAR - r_top))],
        0.0,
        P.COLLAR_AZ,
    )
    return dome.fuse(deck).fuse(ring_back).fuse(collar)


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


def _hinge_towers() -> cq.Shape:
    out = None
    inside = g.inter(g.sphere(P.R_STAGE - 0.01), g.slab(0, P.Z_DECK - 0.01))
    for sy in (1, -1):
        y0, y1 = (TOWER_Y0, TOWER_Y1) if sy > 0 else (-TOWER_Y1, -TOWER_Y0)
        knuckle = g.cyl_y(P.KNUCKLE_R, y0, y1, HX, HZ)
        arm = g.box(HX, HX + 13.5, y0, y1, HZ - P.KNUCKLE_R, P.Z_DECK)
        # the spring's body leg rests on a yoke between the towers; each tower
        # carries one end of it
        foot = g.box(HX + 10.6, HX + 13.5, y0, y1, 4.4, HZ)
        tower = g.inter(knuckle.fuse(arm).fuse(foot), inside)
        out = tower if out is None else out.fuse(tower)
    rm = (P.SPRING_OD - P.SPRING_WIRE) / 2
    seat_z = HZ - rm - P.SPRING_WIRE / 2
    yoke = g.box(HX + 10.6, HX + 13.5, -TOWER_Y0, TOWER_Y0, 4.4, seat_z)
    # end stop: the lid's stop tabs land on this beam at LID_OPEN_DEG
    a_open = math.radians(P.LID_TAB_DEG + P.LID_OPEN_DEG)
    ux, uz = math.cos(a_open), math.sin(a_open)          # tab direction when open
    nx, nz = -uz, ux                                      # normal on its leading face
    p1 = (HX + 4.5 * ux + 1.5 * nx, HZ + 4.5 * uz + 1.5 * nz)
    p2 = (HX + (P.LID_TAB_LEN + 0.5) * ux + 1.5 * nx, HZ + (P.LID_TAB_LEN + 0.5) * uz + 1.5 * nz)
    stop = g.prism_xz([p1, p2, (p2[0], p2[1] + 1.2), (HX + 1.0, p2[1] + 1.2), (HX + 1.0, p1[1] + 0.7)], -TOWER_Y0, TOWER_Y0)
    return out.fuse(yoke).fuse(stop)


def stop_contact_ok() -> float:
    """Height of the stop beam's lower corner above the hinge axis (for reports)."""
    a_open = math.radians(P.LID_TAB_DEG + P.LID_OPEN_DEG)
    return 4.5 * math.sin(a_open) + 1.5 * math.cos(a_open)


def lock_pin_span(locked: bool) -> tuple[float, float]:
    tip = P.LOCK_TIP_X if locked else P.LOCK_TIP_X - P.LOCK_TRAVEL
    return (tip - P.LOCK_PIN_L, tip)


@lru_cache(maxsize=None)
def stage() -> cq.Shape:
    body = _stage_shell()
    body = body.fuse(_screw_pads())
    # room for the lid's rear rim, which swings inwards about the hinge
    relief = g.cyl_y(P.BACK_RELIEF_R, -P.BACK_RELIEF_Y, P.BACK_RELIEF_Y, HX, HZ)
    behind = g.box(-60, HX, -P.BACK_RELIEF_Y, P.BACK_RELIEF_Y, -1, HZ)
    body = body.cut(relief).cut(behind)
    body = body.fuse(_hinge_towers())
    body = body.cut(g.cyl_y(P.HINGE_PRESS / 2, -30, 30, HX, HZ))    # the two hinge pins are pressed into the towers

    # ring cradle pocket and the guide of the lock pin behind it
    guide = g.box(P.LOCK_STEM_X[0] - P.LOCK_TRAVEL - 1.5, P.CRADLE_X0 - 0.2, -4.0, 4.0, P.LOCK_Z - 3.2, DECK_BOTTOM + 0.01)
    body = body.fuse(guide)
    body = body.cut(g.box(P.CRADLE_X0 - 0.2, P.CRADLE_X1 + 0.2, -P.CRADLE_Y - 0.2, P.CRADLE_Y + 0.2, 0, 60))
    # the lock pin is pushed in from behind: its bore runs out through the rear wall of the stage
    body = body.cut(g.cyl_x(P.LOCK_PIN_D / 2 + 0.15, -60, P.CRADLE_X0, 0, P.LOCK_Z))
    stem_slot = g.box(P.LOCK_STEM_X[0] - P.LOCK_TRAVEL - 0.3, P.LOCK_STEM_X[1] + 0.3, -1.7, 1.7, P.LOCK_Z - 2.3, 60)
    body = body.cut(stem_slot)
    # detent dimples for the slider cap (locked / released)
    for dx in (0.0, -P.LOCK_TRAVEL):
        body = body.cut(g.sphere(0.9, (P.LOCK_STEM_X[0] + 2.5 + dx, 4.2, P.Z_DECK + 0.45)))

    # latch: pivot boss, stop pin and spring seat hang from the deck underside
    px, py = P.PAWL_PIVOT
    boss = g.cyl_z(P.PAWL_BOSS_D / 2, P.PAWL_Z0 - 0.3, DECK_BOTTOM + 0.01, px, py)
    tail_x = px - P.PAWL_TAIL_X
    stop_pin = g.cyl_z(1.5, P.PAWL_Z0 - 0.3, DECK_BOTTOM + 0.01, tail_x, -4.1)
    seat = g.box(tail_x - 2.6, tail_x + 2.6, 9.3, 11.6, P.PAWL_Z0 - 0.5, DECK_BOTTOM + 0.01)
    nub = g.cyl_y(1.1, 8.3, 9.4, tail_x, (P.PAWL_Z0 + P.PAWL_Z1) / 2)
    body = body.fuse(boss).fuse(stop_pin).fuse(seat).fuse(nub)
    # the pivot screw forms its own thread in the boss; the mouth of the hole is at the top of the print
    body = body.cut(g.cyl_z(P.M2_PILOT_FLAT / 2, P.PAWL_Z0 - 1, DECK_BOTTOM + 1.2, px, py))
    body = body.cut(g.cone_z(P.M2_PILOT_FLAT / 2 + P.M2_LEAD, P.M2_PILOT_FLAT / 2, P.PAWL_Z0 - 0.301, P.PAWL_Z0 - 0.3 + P.M2_LEAD, px, py))

    # openings: screws, lid hook, bezel tube, band lugs
    for az in P.SCREW_AZ:
        bx, by = g.polar(P.SCREW_R, az)
        body = body.cut(g.cyl_z(P.M3_HEAD_D / 2, P.STAGE_PAD_Z, 60, bx, by))
        body = body.cut(g.cyl_z(P.M3_CLEAR / 2, -1, 60, bx, by))
        body = body.cut(band_lug(az, 0.15))
    body = body.cut(hook_sweep(P.CL_MOVE + 0.1))
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
def pawl_at(deg: float = 0.0) -> cq.Shape:
    """The latch pawl, rotated by ``deg`` towards release (clockwise from above)."""
    shape = pawl()
    px, py = P.PAWL_PIVOT
    return g.rot(shape, "z", -deg, (px, py, 0)) if deg else shape


@lru_cache(maxsize=None)
def pawl() -> cq.Shape:
    px, py = P.PAWL_PIVOT
    z0, z1 = P.PAWL_Z0, P.PAWL_Z1
    tail_x = px - P.PAWL_TAIL_X
    y_stem = P.HOOK_Y - P.HOOK_W / 2          # -y face of the lid hook stem
    nose_x1 = P.HOOK_X1 - 1.2
    plate = g.prism_xy(
        [
            (tail_x - 2.5, -2.5),
            (tail_x + 2.5, -2.5),
            (px - 2.0, -4.6),
            (P.HOOK_X0 - 0.4, y_stem - P.TOOTH_REACH - 2.4),
            (nose_x1, y_stem - P.TOOTH_REACH - 2.4),
            (nose_x1, y_stem - 0.25),
            (P.HOOK_X0 - 0.4, y_stem - 0.25),
            (px + 3.4, 4.2),
            (px - 3.4, 4.2),
            (tail_x + 2.5, 2.5),
            (tail_x - 2.5, 2.5),
        ],
        z0,
        z1,
    )
    hub = g.cyl_z(P.PAWL_BOSS_D / 2 + 2.0, z0, z1, px, py)
    post = g.cyl_z(P.PAWL_POST_R, P.PAWL_POST_Z0, z0 + 0.01, tail_x, 0.0)
    # lug pushed by the emergency paper clip (on the -y side of the pivot)
    start, direction = S.emergency_axis()
    t = (start.x - (px + 4.6)) / -direction.x
    hit = start + direction * t
    lug = g.box(px + 3.0, px + 6.2, hit.y - 2.2, hit.y + 2.2, hit.z - 1.6, z0 + 0.01)
    body = plate.fuse(hub).fuse(post).fuse(lug)
    body = body.cut(g.cyl_z(P.PAWL_BORE / 2, z0 - 1, z1 + 1, px, py))
    # chamfer on the nose so the closing lid can push the pawl aside
    wedge = g.prism_yz(
        [(y_stem - 0.25 + 0.01, z1 + 0.01), (y_stem - 0.25 + 0.01, z1 - 1.6), (y_stem - 0.25 - 1.6, z1 + 0.01)],
        P.HOOK_X0 - 1.0,
        nose_x1 + 1.0,
    )
    body = body.cut(wedge)
    # seat for the return spring on the +y side of the tail
    body = body.fuse(g.cyl_y(1.1, 2.4, 3.4, tail_x, (z0 + z1) / 2))
    return g.clean(body)


def emergency_hit_point() -> cq.Vector:
    px, _ = P.PAWL_PIVOT
    start, direction = S.emergency_axis()
    t = (start.x - (px + 4.6)) / -direction.x
    return start + direction * t


@lru_cache(maxsize=None)
def cradle() -> cq.Shape:
    """Exchangeable ring seat.  Reprint with the measured ring dimensions."""
    x0, x1, yh = P.CRADLE_X0, P.CRADLE_X1, P.CRADLE_Y
    z1 = P.Z_DECK
    z0 = z1 - P.CRADLE_DEPTH
    body = g.rbox(x0, x1, -yh, yh, z0, z1, 1.5)
    r_out = P.RING_ID / 2 + P.RING_THICK
    zc = P.Z_DECK - P.RING_SINK + r_out               # ring centre height
    slot = g.cyl_x(r_out + 0.6, P.RING_X - P.RING_SLOT_W / 2, P.RING_X + P.RING_SLOT_W / 2, 0, zc)
    slot = slot.fuse(g.box(P.RING_X - P.RING_SLOT_W / 2, P.RING_X + P.RING_SLOT_W / 2, -r_out - 0.6, r_out + 0.6, zc, z1 + 5))
    body = body.cut(slot)
    body = body.cut(g.cyl_x(P.LOCK_PIN_D / 2 + 0.15, x0 - 1, P.LOCK_TIP_X + 0.6, 0, P.LOCK_Z))
    # cushion look: a shallow valley towards the ring
    valley = g.prism_xz([(x0 + 1.2, z1 + 1), (P.RING_X, z1 - 1.3), (x1 - 1.2, z1 + 1)], -yh + 1.5, yh - 1.5)
    body = body.cut(valley)
    lip = g.rbox(x0 - 1.2, x1 + 1.2, -yh - 1.2, yh + 1.2, z1, z1 + 0.8, 2.0).cut(g.box(x0 + 1.0, x1 - 1.0, -yh + 1.0, yh - 1.0, z1 - 1, z1 + 2))
    return g.clean(body.fuse(lip))


def slider_at(locked: bool = True) -> cq.Shape:
    return slider() if locked else g.move(slider(), dx=-P.LOCK_TRAVEL)


@lru_cache(maxsize=None)
def slider() -> cq.Shape:
    """Knob of the ring lock; the Ø3 steel pin is pressed into its stem."""
    xs0, xs1 = P.LOCK_STEM_X
    stem = g.box(xs0, xs1, -1.5, 1.5, P.LOCK_Z - 2.0, P.Z_DECK + 0.3)
    cap = g.rbox(xs0 - 1.5, xs1 + 1.5, -5.5, 5.5, P.Z_DECK + 0.3, P.Z_DECK + 2.6, 1.6)
    grip = None
    for i in range(3):
        rib = g.box(xs0 + 0.2 + i * 2.0, xs0 + 1.0 + i * 2.0, -4.5, 4.5, P.Z_DECK + 2.6, P.Z_DECK + 3.3)
        grip = rib if grip is None else grip.fuse(rib)
    bump = g.sphere(0.8, (xs0 + 2.5, 4.2, P.Z_DECK + 0.45))
    body = stem.fuse(cap).fuse(grip).fuse(bump)
    body = body.cut(g.cyl_x(P.LOCK_PIN_D / 2 - 0.05, xs0 - 5, xs1 + 5, 0, P.LOCK_Z))
    return g.clean(body)


@lru_cache(maxsize=None)
def sleeve() -> cq.Shape:
    half = P.SPRING_SLOT / 2 - 0.15
    body = g.cyl_y(P.SLEEVE_OD / 2, -half, half, HX, HZ).cut(g.cyl_y(P.HINGE_BORE / 2, -10, 10, HX, HZ))
    # each end catches the tip of one hinge pin: a funnel leads it in
    r, lead = P.HINGE_BORE / 2, 0.4
    body = body.cut(g.cone_y(r + lead, r, -half - 0.001, -half + lead, HX, HZ))
    body = body.cut(g.cone_y(r, r + lead, half - lead, half + 0.001, HX, HZ))
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
    z1 = P.PAWL_Z0 - 0.3                         # end of the pivot boss
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
