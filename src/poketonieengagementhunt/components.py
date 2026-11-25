"""Dummy CAD models of every purchased component.

They are deliberately simple but recognisable (connector, coil, horn ...), so
that each part can be identified in the exploded view and the building
manual, and their *envelopes* are dimensionally faithful to the sources in
``research/`` so that the interference checks mean something.

Every function returns a list of ``(shape, colour_name)`` bodies in the
component's own local frame, described in its docstring.
"""

from __future__ import annotations

import math

import cadquery as cq

from . import geom as g
from . import params as P

Bodies = list[tuple[cq.Shape, str]]


def _board(length: float, width: float, t: float, colour: str, r: float = 1.0) -> cq.Shape:
    return g.rbox(-length / 2, length / 2, -width / 2, width / 2, 0, t, r)


# --------------------------------------------------------------------------
# electronics
# --------------------------------------------------------------------------
def pn5180_blue() -> Bodies:
    """Common blue "PN5180-NFC" reader board (70 x 39 mm, silkscreen R1.1-170710).

    Local frame, as the board lies in the grass tongue: x runs from the
    header-end edge (x = 0) to the antenna end (x = BLUE_L); y is centred.
    The plain side is on top at z = 0 and faces the Tonie; the PCB occupies
    z = -BLUE_T .. 0 and the components hang below it.  The antenna is a
    rectangular spiral in the far half of the board; its centre is BLUE_ANT_X
    from the header edge.
    """
    L, W, T = P.BLUE_L, P.BLUE_W, P.BLUE_T
    pcb = g.rbox(0.0, L, -W / 2, W / 2, -T, 0.0, 1.0)
    for hx, hy in P.BLUE_HOLES:
        pcb = pcb.cut(g.cyl_z(P.BLUE_HOLE_D / 2, -T - 1, 1, hx, hy - W / 2))
    pins = [(P.BLUE_HDR_X, P.BLUE_PIN1_Y - W / 2 + 2.54 * i) for i in range(13)]
    for px, py in pins:
        pcb = pcb.cut(g.cyl_z(0.5, -T - 1, 1, px, py))
    ax0, ax1, ay0, ay1 = P.BLUE_ANT
    # the antenna is drawn as an inlay that is flush with the component side
    outer = g.rbox(ax0, ax1, ay0 - W / 2, ay1 - W / 2, -T, -T + 0.12, 2.0)
    inner = g.rbox(ax0 + 3.3, ax1 - 3.3, ay0 - W / 2 + 3.2, ay1 - W / 2 - 3.2, -T - 0.3, -T + 0.4, 1.2)
    loop = outer.cut(inner)
    for hx, hy in P.BLUE_HOLES:
        loop = loop.cut(g.cyl_z(P.BLUE_HOLE_D / 2 + 0.5, -T - 1, 1, hx, hy - W / 2))
    pcb = pcb.cut(loop)
    chip = g.box(10.1, 16.1, -4.2, 1.8, -T - 0.85, -T)                    # PN5180 HVQFN40 6 x 6
    xtal = g.box(5.2, 8.0, -3.6, -0.4, -T - 0.7, -T)                       # 27.12 MHz crystal
    match = g.box(19.0, P.BLUE_COMP_X[1], -7.5, 9.0, -T - P.BLUE_COMP_H, -T)   # EMC filter and matching (envelope)
    decap = g.box(6.5, 15.5, 9.5, 17.5, -T - 0.8, -T)
    joints = g.compound([g.cyl_z(0.9, 0.0, 0.5, px, py) for px, py in pins])   # solder joints of the 11 wires
    return [(pcb, "pcb_blue"), (loop, "copper"), (chip, "ic"), (xtal, "metal"), (match, "ic"), (decap, "ic"), (joints, "metal")]


def harness() -> Bodies:
    """Reader harness, modelled in ASSEMBLY coordinates because its path is
    the point: a flat bundle of wires from the reader's header pads, along
    the channel of the tongue, level through the window in the bowl wall,
    and two mated 6-pin plug pairs (1.25 mm pitch) parked above the floor of the bowl.
    """
    w, t = P.HARNESS_W / 2, P.HARNESS_T
    x_pad = P.SPOT_X - P.BLUE_ANT_X + P.BLUE_HDR_X
    x_plug = 2.0                                               # near end of the parked plug pairs
    z0 = -38.6
    ribbon = g.box(x_plug - 0.5, x_pad + 1.5, -w, w, z0, z0 + t)
    plugs = [
        g.rbox(x_plug - P.PLUG_L, x_plug, s * 5.6 - P.PLUG_W / 2, s * 5.6 + P.PLUG_W / 2, z0 - 0.3, z0 - 0.3 + P.PLUG_H, 0.8, "x")
        for s in (1, -1)
    ]
    return [(ribbon, "cable"), (plugs[0], "connector"), (plugs[1], "connector")]


def xiao_s3_plus() -> Bodies:
    """Seeed XIAO ESP32-S3 Plus.

    Local frame: PCB centre at origin, z = 0 underside, USB-C at the +X short
    edge (overhanging 1.6 mm), U.FL antenna connector at -X.
    """
    L, W = P.XIAO_L, P.XIAO_W
    pcb = _board(L, W, 1.2, "pcb_black", 1.9)
    usb = g.rbox(L / 2 - 5.7, L / 2 + 1.6, -P.USB_W / 2, P.USB_W / 2, 1.2, 1.2 + P.USB_H, 1.2, "x")
    shield = g.box(-L / 2 + 1.5, -L / 2 + 13.0, -6.0, 6.0, 1.2, 3.4)       # RF can
    ufl = g.cyl_z(1.0, 1.2, 2.4, -L / 2 + 1.2, 6.5)
    pads = []
    for i in range(7):
        x = -L / 2 + 2.95 + i * 2.54
        for sy in (-1, 1):
            pads.append(g.box(x - 0.8, x + 0.8, sy * (W / 2) - 1.0 if sy > 0 else -W / 2, sy * (W / 2) if sy > 0 else -W / 2 + 1.0, 1.2, 1.3))
    return [(pcb, "pcb_black"), (usb, "metal"), (shield, "metal"), (ufl, "gold"), (g.compound(pads), "gold")]


def max98357() -> Bodies:
    """MAX98357A I2S amplifier breakout (Adafruit #3006 footprint).

    Local frame: PCB centre at origin; long edge (19.05) along X; the 7-pin
    header row is at -X, the speaker pads at +X.
    """
    L, W = P.AMP_L, P.AMP_W
    pcb = _board(L, W, 1.6, "pcb_purple", 2.0)
    for sy in (-1, 1):
        pcb = pcb.cut(g.cyl_z(1.25, -1, 3, L / 2 - 2.54, sy * 6.35))
    chip = g.box(-1.6, 1.6, -1.6, 1.6, 1.6, 2.4)
    pads = g.box(-L / 2 + 1.6, -L / 2 + 3.4, -7.9, 7.9, 1.6, 1.75)
    out = g.box(L / 2 - 5.2, L / 2 - 3.6, -2.6, 2.6, 1.6, 1.75)
    return [(pcb, "pcb_purple"), (chip, "ic"), (pads, "gold"), (out, "gold")]


def tp4056() -> Bodies:
    """TP4056 USB-C charger module with DW01A protection.

    Local frame: PCB centre at origin, z = 0 underside; the USB-C receptacle
    is on the top side at the -X short edge and overhangs the edge by 1.2 mm.
    Battery / output pads at +X.
    """
    L, W = P.TP_L, P.TP_W
    pcb = _board(L, W, 1.0, "pcb_blue", 0.8)
    usb = g.rbox(-L / 2 - 1.2, -L / 2 + 6.1, -P.USB_W / 2, P.USB_W / 2, 1.0, 1.0 + P.USB_H, 1.2, "x")
    chip = g.box(-2.5, 2.5, -2.0, 2.0, 1.0, 2.6)                 # TP4056 SOP-8
    prot = g.box(6.0, 9.0, -1.5, 1.5, 1.0, 2.1)                   # DW01A + FS8205A
    pads = []
    for y in (-6.5, -3.9, 3.9, 6.5):
        pads.append(g.box(L / 2 - 2.6, L / 2 - 0.4, y - 1.0, y + 1.0, 1.0, 1.12))
    leds = g.box(-L / 2 + 7.5, -L / 2 + 9.0, 5.0, 7.5, 1.0, 1.6)
    return [(pcb, "pcb_blue"), (usb, "metal"), (chip, "ic"), (prot, "ic"), (g.compound(pads), "gold"), (leds, "led_red")]


def miniboost() -> Bodies:
    """Adafruit MiniBoost 5V (TPS61023).  PCB centre at origin, z = 0 underside."""
    L, W = P.BOOST_L, P.BOOST_W
    pcb = _board(L, W, 1.6, "pcb_black", 1.2)
    inductor = g.rbox(-2.2, 2.2, -2.2, 2.2, 1.6, 4.0, 0.6)
    chip = g.box(-6.0, -4.0, -1.0, 1.0, 1.6, 2.4)
    pads = g.box(L / 2 - 2.2, L / 2 - 0.4, -4.6, 4.6, 1.6, 1.75)
    return [(pcb, "pcb_black"), (inductor, "ic"), (chip, "ic"), (pads, "gold")]


def hall_sensor() -> Bodies:
    """DRV5032FB in TO-92: body lying flat, sensing face = -Z, leads towards +X."""
    body = g.box(-P.HALL_H / 2, P.HALL_H / 2, -P.HALL_W / 2, P.HALL_W / 2, 0, P.HALL_T)
    leads = g.compound(
        [g.box(P.HALL_H / 2, P.HALL_H / 2 + 6.0, y - 0.2, y + 0.2, 0.5, 0.9) for y in (-1.27, 0.0, 1.27)]
    )
    return [(body, "ic"), (leads, "metal")]


def led_pcb() -> Bodies:
    """Single WS2812B / SK6812 on a Ø10 mm round PCB.

    Local frame: emitting face normal = +X; PCB occupies x in [-LED_PCB_T, -1.6],
    the LED body x in [-1.6, 0]; centred on the X axis.
    """
    pcb = g.cyl_x(P.LED_PCB_D / 2, -P.LED_PCB_T, -1.6)
    led = g.box(-1.6, 0.0, -2.5, 2.5, -2.5, 2.5)
    window = g.cyl_x(1.9, -0.05, 0.05)
    return [(pcb, "pcb_black"), (led, "white"), (window, "led_glow")]


def speaker_k40() -> Bodies:
    """Visaton K 40 (8 Ohm, Ø40 x 4.3 mm).

    Local frame: axis = X, sound leaves towards +X.  The front rim face is at
    x = 0; the speaker extends to x = -SPK_DEPTH.
    """
    rim = g.cyl_x(P.SPK_D / 2, -P.SPK_RIM_T, 0.0).cut(g.cyl_x(P.SPK_BASKET_D / 2 - 1.5, -P.SPK_RIM_T - 1, 1))
    basket = g.cyl_x(P.SPK_BASKET_D / 2, -3.0, -P.SPK_RIM_T)
    cone = g.cone_x(6.0, P.SPK_BASKET_D / 2 - 1.5, -P.SPK_RIM_T, -0.2)
    cup = g.cyl_x(P.SPK_CUP_D / 2, -P.SPK_DEPTH, -3.0)
    tags = g.box(-3.6, -3.0, 13.0, 17.0, -2.0, 2.0)
    return [(rim, "metal"), (basket, "metal_dark"), (cone, "speaker_cone"), (cup, "metal"), (tags, "gold")]


def cell_18650() -> Bodies:
    """Unprotected flat-top 18650.  Axis along Y, centred; positive end at +Y."""
    half = P.CELL_L / 2
    can = g.cyl_y(P.CELL_D / 2, -half, half - 1.2)
    top = g.cyl_y(P.CELL_D / 2 - 0.4, half - 1.2, half - 0.4)
    plus = g.cyl_y(4.0, half - 0.4, half)
    ring = g.cyl_y(P.CELL_D / 2 + 0.01, half - 4.0, half - 2.6).cut(g.cyl_y(P.CELL_D / 2 - 0.5, half - 5, half))
    return [(can, "cell_wrap"), (top, "white"), (plus, "metal"), (ring, "white")]


def cell_contact(spring: bool) -> Bodies:
    """Battery contact plate (10 x 10 x 0.4).  Plate in the X-Z plane at y = 0,
    the spring / dimple points towards +Y."""
    plate = g.box(-5.0, 5.0, -0.4, 0.0, -5.0, 5.0)
    tab = g.box(-1.5, 1.5, -0.4, 0.0, 5.0, 9.0)
    if spring:
        bump = cq.Solid.makeCone(4.0, 2.0, P.CELL_SPRING_LEN, cq.Vector(0, 0, 0), cq.Vector(0, 1, 0))
    else:
        bump = g.cyl_y(2.5, 0.0, 1.0)
    return [(plate.fuse(tab), "metal"), (bump, "metal")]


# --------------------------------------------------------------------------
# servo
# --------------------------------------------------------------------------
def sg90(horn_deg: float = 0.0) -> Bodies:
    """Generic 9 g micro servo (SG90 class) with its stock single-arm horn.

    Local frame (research/05 §8.1): origin on the output-shaft axis at the
    bottom face of the body; +X along the body away from the shaft end, Z up.
    ``horn_deg`` is the direction of the horn arm, measured CCW from local +X
    seen from above.
    """
    x0, x1 = -P.SG90_SHAFT_OFF, P.SG90_L - P.SG90_SHAFT_OFF
    w = P.SG90_W / 2
    body = g.box(x0, x1, -w, w, 0.0, P.SG90_CASE_Z)
    fx = (P.SG90_FLANGE_SPAN - P.SG90_L) / 2
    flange = g.box(x0 - fx, x1 + fx, -w, w, P.SG90_FLANGE_Z, P.SG90_FLANGE_Z + P.SG90_FLANGE_T)
    hole_x0 = (x0 + x1) / 2 - P.SG90_HOLE_PITCH / 2
    for hx in (hole_x0, hole_x0 + P.SG90_HOLE_PITCH):
        flange = flange.cut(g.cyl_z(1.0, 0, 40, hx, 0))
    gear = g.cyl_z(P.SG90_W / 2, P.SG90_CASE_Z, P.SG90_GEAR_Z).fuse(
        g.cyl_z(2.5, P.SG90_CASE_Z, P.SG90_GEAR_Z, 6.4, 0)
    ).fuse(g.box(0, 6.4, -2.5, 2.5, P.SG90_CASE_Z, P.SG90_GEAR_Z))
    spline = g.cyl_z(2.3, P.SG90_GEAR_Z, P.SG90_SPLINE_Z)
    cable = g.box(x0 - 7.0, x0, -1.8, 1.8, 4.5, 5.7)
    hub = g.cyl_z(3.5, P.SG90_ARM_Z0, 31.0)
    a0, a1 = P.SG90_ARM_Z0 + 0.6, P.SG90_ARM_Z0 + 2.1
    L = P.SG90_ARM_LEN - 2.2
    arm = g.prism_xy([(0, -2.8), (L, -2.2), (L, 2.2), (0, 2.8)], a0, a1).fuse(g.cyl_z(2.2, a0, a1, L, 0))
    screw = g.cyl_z(2.0, 31.0, P.SG90_HORN_TOP_Z)
    horn = g.rot(hub.fuse(arm).cut(g.cyl_z(2.3, 0, P.SG90_SPLINE_Z + 0.01)), "z", horn_deg)
    return [
        (body.fuse(flange), "servo_blue"),
        (gear, "servo_clear"),
        (spline, "white"),
        (cable, "cable"),
        (horn, "white"),
        (screw, "metal_dark"),
    ]


# --------------------------------------------------------------------------
# hardware
# --------------------------------------------------------------------------
def pin_y(d: float, length: float) -> Bodies:
    """Steel pin along Y, centred at the origin."""
    return [(g.cyl_y(d / 2, -length / 2, length / 2), "metal")]


def pin_x(d: float, length: float) -> Bodies:
    """Steel pin along X from x = 0 to x = length."""
    return [(g.cyl_x(d / 2, 0, length), "metal")]


def washer(d_in: float, d_out: float, t: float) -> Bodies:
    """Flat washer lying in the X-Y plane, from z = 0 to z = t."""
    return [(g.cyl_z(d_out / 2, 0.0, t).cut(g.cyl_z(d_in / 2, -1.0, t + 1.0)), "metal")]


def screw_down(d: float, length: float, head_d: float, head_h: float) -> Bodies:
    """Cap screw pointing down (-Z).  Underside of the head at z = 0."""
    shank = g.cyl_z(d / 2, -length, 0.0)
    head = g.cyl_z(head_d / 2, 0.0, head_h)
    socket = g.cyl_z(d * 0.42, head_h - 0.9 * d / 2 - 0.3, head_h + 0.01)
    return [(shank.fuse(head).cut(socket), "metal_dark")]


def screw_up(d: float, length: float, head_d: float, head_h: float) -> Bodies:
    """Cap screw pointing up (+Z).  Bearing face of the head at z = 0."""
    return [(g.rot(s, "x", 180.0), c) for s, c in screw_down(d, length, head_d, head_h)]


def screw_x(d: float, length: float, head_d: float, head_h: float) -> Bodies:
    """Cap screw pointing along -X (head at +X).  Bearing face at x = 0."""
    return [(g.rot(s, "y", 90.0), c) for s, c in screw_down(d, length, head_d, head_h)]


def screw_csk_up(d: float, length: float, head_d: float, head_h: float) -> Bodies:
    """Countersunk screw pointing up (+Z).  The flat face of the head is at
    z = 0; ``length`` includes the head, as in ISO 10642."""
    head = g.cone_z(head_d / 2, d / 2, 0.0, head_h)
    shank = g.cyl_z(d / 2, head_h - 0.01, length)
    socket = g.cyl_z(d * 0.36, -0.01, head_h * 0.65)
    return [(head.fuse(shank).cut(socket), "metal_dark")]


def insert_m3(length: float, od: float) -> Bodies:
    """M3 heat-set insert, ``od`` over the knurl.  Top face at z = 0, body below."""
    body = g.cyl_z(od / 2, -length, 0.0).cut(g.cyl_z(1.25, -length - 1, 1))
    return [(body, "brass")]


def torsion_spring(leg_lid_deg: float, leg_body_deg: float) -> Bodies:
    """Gutekunst T-16324 class torsion spring on the hinge pin.

    Local frame: coil axis = Y through the origin, coil centred.  Leg
    directions are angles in the X-Z plane measured from +X towards +Z; the
    lid leg leaves the coil at the +Y end, the body leg at the -Y end.
    """
    half = P.SPRING_BODY / 2
    coil = g.cyl_y(P.SPRING_OD / 2, -half, half).cut(g.cyl_y(P.SPRING_ID / 2, -half - 1, half + 1))
    rm = (P.SPRING_OD - P.SPRING_WIRE) / 2

    def leg(deg: float, y: float, side: float) -> cq.Shape:
        a = math.radians(deg)
        # tangent leg: it leaves the coil's mean circle a quarter turn before
        # (side = -1) or after (side = +1) the direction it points in.  With
        # the legs of a relaxed spring in one line, both lie on the same tangent.
        sx, sz = rm * math.cos(a + side * math.pi / 2), rm * math.sin(a + side * math.pi / 2)
        wire = cq.Solid.makeCylinder(
            P.SPRING_WIRE / 2, P.SPRING_LEG, cq.Vector(sx, y, sz), cq.Vector(math.cos(a), 0, math.sin(a))
        )
        return wire

    legs = leg(leg_lid_deg, half - P.SPRING_WIRE / 2, +1.0).fuse(leg(leg_body_deg, -half + P.SPRING_WIRE / 2, -1.0))
    return [(coil, "spring"), (legs, "spring")]


def compression_spring(d_out: float, length: float) -> Bodies:
    """Small compression spring drawn as a tube, axis X from 0 to length."""
    tube = g.cyl_x(d_out / 2, 0, length).cut(g.cyl_x(d_out / 2 - 0.4, -1, length + 1))
    return [(tube, "spring")]


# --------------------------------------------------------------------------
# the ring and a Tonie
# --------------------------------------------------------------------------
def ring() -> Bodies:
    """Engagement ring, EU size 49.

    Local frame: ring centre at the origin, ring plane = Y-Z (the finger axis
    is X), setting and stone on top (+Z).
    """
    ri = P.RING_ID / 2
    ro = ri + P.RING_THICK
    hw = P.RING_BAND / 2
    band = g.cyl_x(ro, -hw, hw).cut(g.cyl_x(ri, -hw - 1, hw + 1))
    band = cq.Workplane(obj=band).edges().fillet(0.35).val()
    z0 = ro - 0.3
    basket = cq.Solid.makeCone(1.4, P.RING_STONE_D / 2 + 0.3, P.RING_HEAD_H - 2.6, cq.Vector(0, 0, z0), cq.Vector(0, 0, 1))
    zg = z0 + P.RING_HEAD_H - 2.6
    pavilion = cq.Solid.makeCone(0.3, P.RING_STONE_D / 2, 1.4, cq.Vector(0, 0, zg - 0.6), cq.Vector(0, 0, 1))
    crown = cq.Solid.makeCone(P.RING_STONE_D / 2, P.RING_STONE_D / 2 * 0.58, 1.0, cq.Vector(0, 0, zg + 0.8), cq.Vector(0, 0, 1))
    stone = pavilion.fuse(crown)
    return [(band.fuse(basket.cut(g.cyl_z(P.RING_STONE_D / 2 - 0.2, zg - 0.4, zg + 5))), "gold"), (stone, "diamond")]


def tonie() -> Bodies:
    """Tonie figure dummy, after the 2026 Pokémon figures: a dark round foot
    with a small figure standing on it (research/09).

    Local frame: the underside of the foot, where the RFID inlay and the
    magnet sit, is at z = 0; the figure looks towards +X.
    """
    rb, hb = P.TONIE_BASE_D / 2, P.TONIE_BASE_H
    foot = cq.Workplane(obj=g.cyl_z(rb, 0.0, hb)).edges(">Z").fillet(min(3.0, 0.3 * hb)).val()
    k = (P.TONIE_H - hb) / 50.0                       # the figure is drawn 50 units tall
    body = g.sphere(11.0 * k, (0.0, 0.0, hb + 10.0 * k))
    head = g.sphere(11.5 * k, (1.0 * k, 0.0, hb + 27.0 * k))
    ears = [
        cq.Solid.makeCone(3.6 * k, 0.9 * k, 16.0 * k, cq.Vector(0.0, sy * 6.0 * k, hb + 34.0 * k), cq.Vector(-0.15, sy * 0.45, 1.0))
        for sy in (-1, 1)
    ]
    # magnet and tag as in classic Tonies; where they sit in a Pokémon figure is not known
    magnet = g.cyl_z(P.TONIE_MAGNET_D / 2, 1.5, 1.5 + P.TONIE_MAGNET_H)
    tag = g.cyl_z(2.0, hb + 6.0 * k, hb + 6.0 * k + 10.0)          # upright ferrite-rod transponder
    foot = foot.cut(magnet)
    return [
        (foot, "tonie_base"),
        (body.fuse(head).cut(tag), "tonie_body"),
        (g.compound(ears), "tonie_body"),
        (magnet, "metal"),
        (tag, "copper"),
    ]
