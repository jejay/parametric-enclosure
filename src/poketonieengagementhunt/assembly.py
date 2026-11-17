"""The complete device: every printed part and purchased component in place.

``build()`` returns a list of :class:`Item`.  The pose of the moving parts
(lid, latch pawl, servo horn, ring lock) is a parameter, so the same function
serves the static fit check, the motion simulation and every rendering.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import cadquery as cq

from . import components as C
from . import geom as g
from . import params as P
from . import parts_base as B
from . import parts_core as K
from . import parts_shell as S

Bodies = list[tuple[cq.Shape, str]]


@dataclass
class Item:
    key: str                 # unique id
    label: str               # name used in manual and BOM
    kind: str                # 'printed' | 'purchased' | 'hardware'
    bodies: Bodies
    group: str = "fixed"     # motion group: fixed | lid | pawl | horn | slider
    step: int = 0            # assembly step in the building manual
    explode: tuple[float, float, float] = (0.0, 0.0, 0.0)
    qty: int = 1             # quantity represented by this item (for the BOM)
    note: str = ""
    material: str = ""       # filament for printed parts
    check: bool = True       # take part in the interference checks
    proxy: Bodies | None = None   # simpler bodies that stand in for the item in those checks

    def shape(self) -> cq.Shape:
        if len(self.bodies) == 1:
            return self.bodies[0][0]
        return g.compound([b for b, _ in self.bodies])

    def check_bodies(self) -> Bodies:
        return self.proxy if self.proxy is not None else self.bodies

    def moved(self, dx: float, dy: float, dz: float) -> "Item":
        proxy = None if self.proxy is None else [(g.move(s, dx, dy, dz), c) for s, c in self.proxy]
        return Item(self.key, self.label, self.kind, [(g.move(s, dx, dy, dz), c) for s, c in self.bodies], self.group, self.step, self.explode, self.qty, self.note, self.material, self.check, proxy)


def _place(bodies: Bodies, *ops) -> Bodies:
    """Apply a sequence of ('rot', axis, deg) / ('move', x, y, z) operations."""
    out = bodies
    for op in ops:
        if op[0] == "rot":
            out = [(g.rot(s, op[1], op[2]), c) for s, c in out]
        else:
            out = [(g.move(s, op[1], op[2], op[3]), c) for s, c in out]
    return out


def _col(shape: cq.Shape, colour: str) -> Bodies:
    return [(shape, colour)]


def screw_positions() -> list[tuple[float, float]]:
    return [g.polar(P.SCREW_R, az) for az in P.SCREW_AZ]


def ring_centre_z() -> float:
    return P.Z_DECK - P.RING_SINK + P.RING_ID / 2 + P.RING_THICK


def build(
    lid_deg: float = 0.0,
    pawl_deg: float = 0.0,
    horn_deg: float | None = None,
    locked: bool = True,
    with_ring: bool = True,
    with_tonie: bool = False,
) -> list[Item]:
    horn = P.HORN_REST_DEG if horn_deg is None else horn_deg
    items: list[Item] = []
    add = items.append

    # ---------------------------------------------------------------- step 1
    add(Item("bowl", "Bowl (white lower half)", "printed", _col(S.bowl(), "white"), step=1, explode=(0, 0, -118), material="PETG white"))
    ins: Bodies = []
    for x, y in screw_positions():
        ins += _place(C.insert_m3(), ("move", x, y, -P.HB))
    for x, y in B.base_screw_xy():
        ins += _place(C.insert_m3(), ("move", x, y, P.Z_BASE_BOSS))
    add(Item("inserts", "Heat-set insert M3 x 5.7", "hardware", ins, step=1, explode=(0, 0, -92), qty=8))

    # ----------------------------------------------- step 2: the grass tongue
    add(Item("grass_base", "Grass tongue (tray)", "printed", _col(B.grass_base(), "grass"), step=2, explode=(0, 0, -218), material="PETG light green"))
    add(Item("reader", "PN5180 NFC reader (blue board, 70 x 39 mm)", "purchased", _place(C.pn5180_blue(), ("move", B.BLUE_X0, 0, P.Z_PCB_TOP)), step=2, explode=(0, 0, -188)))
    add(Item("hall", "Hall switch DRV5032FB (TO-92)", "purchased", _place(C.hall_sensor(), ("rot", "y", 180.0), ("move", P.SPOT_X, 0, B.HALL_SEAT_Z + P.HALL_T)), step=2, explode=(0, 0, -203)))
    add(Item("harness", "Reader harness: 6-pin plug-and-socket pair with wires", "purchased", C.harness(), step=2, explode=(0, 0, -168), qty=2))
    # one print: turf plate and tufts.  In the generic interference test the plate alone stands in for it;
    # the tufts are checked against ball and figure by check_grass_base
    add(Item("grass_top", "Grass top (turf plate with its tufts)", "printed", _col(B.grass_top(), "grass"), step=2, explode=(0, 0, -142), material="PETG light green", proxy=_col(B.turf_plate(), "grass")))
    ts: Bodies = []
    for x, y in B.turf_screw_xy():
        ts += _place(C.screw_up(2.2, P.TURF_SCREW_L, P.TURF_SCREW_HEAD_D, P.TURF_SCREW_HEAD_H), ("move", x, y, P.Z_SOLE + P.TURF_SCREW_CB))   # head deep in its counterbore, 2.9 mm of tray under it
    add(Item("turf_screws", "Screw 2.2 x 6 self-tapping (grass top to tray)", "hardware", ts, step=2, explode=(0, 0, -240), qty=len(B.turf_screw_xy())))

    # ----------------------------------- step 3: the tongue goes under the bowl
    bs: Bodies = []
    for x, y in B.base_screw_xy():
        bs += _place(C.screw_csk_up(3.0, P.BASE_SCREW_L, P.CSK_D, P.CSK_H), ("move", x, y, P.Z_SOLE + P.CSK_RECESS))
    add(Item("base_screws", "Screw M3 x 16 countersunk ISO 10642 (tongue to bowl)", "hardware", bs, step=3, explode=(0, 0, -256), qty=4))

    # ---------------------------------------------------------------- step 4
    add(Item("chassis", "Chassis", "printed", _col(K.chassis(), "chassis"), step=4, explode=(0, 0, -44), material="PETG any colour"))
    cx, cz = P.CELL_AXIS
    inner = P.CELL_L / 2 + P.CELL_CONTACT
    cont = _place(C.cell_contact(False), ("rot", "z", 180.0), ("move", cx, inner, cz)) + _place(C.cell_contact(True), ("move", cx, -inner, cz))
    add(Item("contacts", "18650 contact plates (+ dimple, - spring)", "purchased", cont, step=4, explode=(0, 0, 14), qty=2))
    mx, my, mz = P.MCU_POS
    add(Item("mcu", "Seeed XIAO ESP32-S3 Plus", "purchased", _place(C.xiao_s3_plus(), ("rot", "y", -90.0), ("rot", "z", 90.0), ("move", mx, my + 0.6, mz)), step=4, explode=(6, -34, 6)))
    ax, ay, az = P.AMP_POS
    add(Item("amp", "MAX98357A I2S amplifier", "purchased", _place(C.max98357(), ("rot", "y", 90.0), ("rot", "z", 90.0), ("move", ax, ay - 0.8, az)), step=4, explode=(6, 34, 6)))
    u = S.usb_dir()
    rc = K.tp4056_centre_r()
    add(Item("charger", "TP4056 USB-C charger with protection", "purchased", _place(C.tp4056(), ("rot", "z", P.USB_AZ - 180.0), ("move", rc * u[0], rc * u[1], K.tp4056_z())), step=4, explode=(-34, 12, 10)))
    bx, by, bz = P.BOOST_POS
    add(Item("boost", "5 V boost converter (Adafruit MiniBoost TPS61023)", "purchased", _place(C.miniboost(), ("rot", "z", 90.0), ("move", bx, by, bz)), step=4, explode=(-30, -16, 16)))

    # ---------------------------------------------------------------- step 5
    servo = _place(C.sg90(horn + 90.0), ("rot", "z", -90.0), ("move", P.SERVO_X, P.SERVO_Y, P.SERVO_BASE_Z))
    add(Item("servo", "9 g micro servo (SG90 class)", "purchased", servo[:4], step=5, explode=(0, 0, 4)))
    add(Item("horn", "Servo horn (stock single arm) + screw", "purchased", servo[4:], group="horn", step=5, explode=(0, 0, 14)))
    mid = P.SERVO_Y + P.SG90_SHAFT_OFF - P.SG90_L / 2
    ss: Bodies = []
    for hy in (mid + P.SG90_HOLE_PITCH / 2, mid - P.SG90_HOLE_PITCH / 2):
        ss += _place(C.screw_down(2.0, 8.0, 3.8, 1.5), ("move", P.SERVO_X, hy, P.SERVO_BASE_Z + P.SG90_FLANGE_Z + P.SG90_FLANGE_T))
    add(Item("servo_screws", "Servo mounting screw 2 x 8 (supplied with servo)", "hardware", ss, step=5, explode=(0, 0, 24), qty=2))

    # ---------------------------------------------------------------- step 6
    add(Item("speaker", "Speaker Visaton K 40 (8 ohm)", "purchased", _place(C.speaker_k40(), ("move", P.SPK_X_FRONT, 0, P.SPK_Z)), step=6, explode=(24, 0, 0)))
    add(Item("spk_clamp", "Speaker clamp ring", "printed", _col(K.spk_clamp(), "clamp"), step=6, explode=(10, 0, 0), material="PETG any colour"))
    x_clamp = P.SPK_X_FRONT - P.SPK_RIM_T - 2.0
    cs: Bodies = []
    for sgn in (1, -1):
        cs += _place(C.screw_x(2.2, 8.0, 3.8, 1.6), ("rot", "z", 180.0), ("move", x_clamp, sgn * 22.6, P.SPK_Z))
    add(Item("clamp_screws", "Screw 2.2 x 8 self-tapping (speaker clamp)", "hardware", cs, step=6, explode=(0, 0, 0), qty=2))
    add(Item("led", "RGB LED WS2812B on 10 mm PCB", "purchased", _place(C.led_pcb(), ("move", P.LED_X, 0, 0)), step=6, explode=(40, 0, 0)))
    add(Item("cone", "Light cone", "printed", _col(S.cone(), "white"), step=6, explode=(50, 0, 0), material="PETG white"))
    add(Item("lens", "Button lens", "printed", _col(S.lens(), "clear"), step=6, explode=(66, 0, 0), material="PETG natural / clear"))
    add(Item("bezel", "Button bezel (black ring with sound slits)", "printed", _col(S.bezel(), "black"), step=6, explode=(86, 0, 0), material="PETG black"))

    # ---------------------------------------------------------------- step 7
    add(Item("cell", "18650 Li-ion cell (unprotected flat top)", "purchased", _place(C.cell_18650(), ("move", cx, P.CELL_Y, cz)), step=7, explode=(0, 0, 22)))

    # ---------------------------------------------------------------- step 8
    add(Item("band", "Band (black equator ring)", "printed", _col(S.band(), "black"), step=8, explode=(0, 0, 40), material="PETG black"))

    # ---------------------------------------------------------------- step 9
    add(Item("stage", "Stage (inner dome with ring deck)", "printed", _col(K.stage(), "stage"), step=9, explode=(0, 0, 84), material="PETG black"))
    add(Item("pawl", "Latch pawl", "printed", _col(K.pawl_at(pawl_deg), "pawl"), group="pawl", step=9, explode=(0, 0, 62), material="PETG any colour"))
    px, py = P.PAWL_PIVOT
    pv = _place(C.screw_up(2.2, 6.0, 3.8, 1.6), ("move", px, py, P.PAWL_Z0 - 0.8)) + _col(g.cyl_z(3.5, P.PAWL_Z0 - 0.8, P.PAWL_Z0 - 0.3, px, py).cut(g.cyl_z(1.2, 0, 60, px, py)), "metal")
    add(Item("pawl_screw", "Screw 2.2 x 6 self-tapping + washer M2 (pawl pivot)", "hardware", pv, step=9, explode=(0, 0, 50)))
    tail_x = px - P.PAWL_TAIL_X
    tail_shift = P.PAWL_TAIL_X * math.sin(math.radians(pawl_deg))
    y_a, y_b = 3.4 + tail_shift, 9.3
    sp = _place(C.compression_spring(3.5, max(y_b - y_a, 1.0)), ("rot", "z", 90.0), ("move", tail_x, y_a, (P.PAWL_Z0 + P.PAWL_Z1) / 2))
    add(Item("pawl_spring", "Compression spring 3.5 x 8 (pawl return)", "hardware", sp, step=9, explode=(0, 10, 62), check=False))
    add(Item("cradle", "Ring cradle", "printed", _col(K.cradle(), "cradle"), step=9, explode=(0, 0, 112), material="PETG red or black"))
    span = K.lock_pin_span(locked)
    add(Item("lock_pin", "Dowel pin 3 x 24 (ring lock)", "hardware", _place(C.pin_x(P.LOCK_PIN_D, P.LOCK_PIN_L), ("move", span[0], 0, P.LOCK_Z)), group="slider", step=9, explode=(-30, 0, 112)))
    add(Item("slider", "Ring lock slider", "printed", _col(K.slider_at(locked), "slider"), group="slider", step=9, explode=(-6, 0, 124), material="PETG any colour"))

    # --------------------------------------------------------------- step 10
    lid_shape = S.open_lid(S.lid(), lid_deg)
    add(Item("lid", "Lid (red upper half)", "printed", _col(lid_shape, "red"), group="lid", step=10, explode=(0, 0, 164), material="PETG red"))
    add(Item("hinge_pin", "Hinge pin 2 x 20 (stainless)", "hardware", _place(C.pin_y(P.HINGE_PIN_D, P.HINGE_PIN_L), ("move", P.HINGE_X, 0, P.HINGE_Z)), step=10, explode=(0, 38, 122)))
    add(Item("sleeve", "Spring sleeve", "printed", _col(K.sleeve(), "sleeve"), step=10, explode=(-14, 0, 136), material="PETG any colour"))
    lid_leg = 180.0 - P.SPRING_DEFL_CLOSED + lid_deg
    spring = _place(C.torsion_spring(lid_leg, 0.0), ("move", P.HINGE_X, 0, P.HINGE_Z))
    add(Item("spring", "Torsion spring Gutekunst T-16324 (0.7 x 6.7, 7 coils)", "purchased", spring, step=10, explode=(-26, 0, 136), check=False))

    # --------------------------------------------------------------- step 11
    st: Bodies = []
    for x, y in screw_positions():
        st += _place(C.screw_down(3.0, P.STACK_SCREW_L, 5.5, P.M3_HEAD_H), ("move", x, y, P.STAGE_PAD_Z))
    add(Item("stack_screws", "Screw M3 x 16 ISO 4762 (stack)", "hardware", st, step=11, explode=(0, 0, 128), qty=4))

    # --------------------------------------------------------------- step 12
    if with_ring:
        add(Item("ring", "Engagement ring (EU 49)", "purchased", _place(C.ring(), ("move", P.RING_X, 0, ring_centre_z())), step=12, explode=(0, 0, 190)))
    if with_tonie:
        add(Item("tonie", "Tonie figurine", "purchased", _place(C.tonie(), ("move", P.SPOT_X, 0, P.Z_TURF)), step=13, check=False))
    return items


def by_key(items: list[Item]) -> dict[str, Item]:
    return {it.key: it for it in items}


# rotation that brings each printed part from assembly orientation into its
# print orientation (None = print as assembled)
PRINT_ORIENT: dict[str, tuple[str, float] | None] = {
    "bowl": ("x", 180.0), "band": ("x", 180.0), "lid": None, "bezel": ("y", 90.0), "lens": ("y", -90.0),
    "cone": ("y", 90.0), "stage": ("x", 180.0), "chassis": None, "pawl": ("x", 180.0),
    "cradle": None, "slider": ("x", 180.0), "sleeve": ("x", 90.0), "spk_clamp": ("y", 90.0),
    "grass_base": None, "grass_top": None,
}
# tessellation (linear, angular tolerance) for parts whose default mesh would be needlessly heavy
MESH: dict[str, tuple[float, float]] = {"grass_top": (0.015, 0.2)}
# parts that are printed with another part in the same job share its placement
PRINT_WITH: dict[str, str] = {}
# parts that consist of several separate bodies on purpose
MULTI_BODY: set[str] = set()
# allowed relative difference between CAD and mesh volume (thin curved parts lose more to facets)
MESH_VOLUME_TOL: dict[str, float] = {"grass_top": 0.03}


def print_oriented(key: str) -> cq.Shape:
    """The printed part turned into print orientation and set down on z = 0."""
    shape = printed_parts()[key][0]
    rot = PRINT_ORIENT[key]
    s = g.rot(shape, rot[0], rot[1]) if rot else shape
    host = PRINT_WITH.get(key)
    if host:
        hrot = PRINT_ORIENT[host]
        hs = printed_parts()[host][0]
        bb = (g.rot(hs, hrot[0], hrot[1]) if hrot else hs).BoundingBox()
    else:
        bb = s.BoundingBox()
    return g.move(s, -(bb.xmin + bb.xmax) / 2, -(bb.ymin + bb.ymax) / 2, -bb.zmin)


def printed_parts() -> dict[str, tuple[cq.Shape, str, str]]:
    """key -> (shape, filament, print orientation note) for every printed part."""
    return {
        "bowl": (S.bowl(), "PETG white", "rim on the bed (dome up), tree supports inside only"),
        "band": (S.band(), "PETG black", "upside down: lid seat on the bed, no supports"),
        "lid": (S.lid(), "PETG red", "rim on the bed (dome up), supports inside only (hook, pole)"),
        "bezel": (S.bezel(), "PETG black", "face down on the bed, no supports"),
        "lens": (S.lens(), "PETG natural / clear", "flange on the bed, button up, 100 % infill"),
        "cone": (S.cone(), "PETG white", "large end on the bed"),
        "stage": (K.stage(), "PETG black", "upside down: deck on the bed, supports for the hinge yoke only"),
        "chassis": (K.chassis(), "PETG any colour", "plate on the bed, supports under the baffle disc and shelf"),
        "pawl": (K.pawl(), "PETG any colour", "upside down: top face on the bed"),
        "cradle": (K.cradle(), "PETG red or black", "as assembled, no supports"),
        "slider": (K.slider(), "PETG any colour", "cap on the bed (upside down)"),
        "sleeve": (K.sleeve(), "PETG any colour", "standing on one end"),
        "spk_clamp": (K.spk_clamp(), "PETG any colour", "flat on the bed"),
        "grass_base": (B.grass_base(), "PETG light green", "sole on the bed, no supports"),
        "grass_top": (B.grass_top(), "PETG light green", "underside on the bed, tufts up, no supports"),
    }
