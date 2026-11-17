"""Geometry verification: watertightness, fit, clearances and motion.

Run ``uv run poketonieengagementhunt check``.  Results are printed and
written to ``docs/verification.md`` and ``docs/verification.json``.
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path

import cadquery as cq
import numpy as np
import trimesh

from . import assembly as A
from . import geom as g
from . import params as P
from . import parts_base as B
from . import parts_core as K
from . import parts_shell as S

# Pairs that overlap ON PURPOSE (threads cut by screws, press fits).  The value
# is the largest overlap volume in mm^3 that is still considered intended.
INTENDED_OVERLAP: dict[frozenset[str], tuple[float, str]] = {
    frozenset(("inserts", "bowl")): (220.0, "heat-set inserts melt into Ø4.0 holes"),
    frozenset(("stack_screws", "inserts")): (60.0, "M3 thread in the inserts"),
    frozenset(("base_screws", "inserts")): (70.0, "M3 thread in the inserts"),
    frozenset(("turf_screws", "grass_top")): (45.0, "self-tapping 2.2 in Ø1.8 pilot"),
    frozenset(("servo_screws", "chassis")): (25.0, "servo screws in Ø1.6 pilot"),
    frozenset(("clamp_screws", "chassis")): (20.0, "self-tapping 2.2 in Ø1.8 pilot"),
    frozenset(("pawl_screw", "stage")): (12.0, "self-tapping 2.2 in Ø1.8 pilot"),
    frozenset(("hinge_pin", "lid")): (2.0, "Ø2 pin pressed into Ø1.95 bores"),
    frozenset(("lock_pin", "slider")): (4.0, "Ø3 pin pressed into Ø2.9 bore"),
}
TOL_VOLUME = 0.05      # mm^3: anything below is numerical noise / touching faces


@dataclass
class Result:
    name: str
    ok: bool
    detail: str
    data: dict = field(default_factory=dict)


# --------------------------------------------------------------------------
# meshes
# --------------------------------------------------------------------------
def to_mesh(shape: cq.Shape, tol: float = 0.01, ang: float = 0.1) -> trimesh.Trimesh:
    verts, tris = shape.tessellate(tol, ang)
    v = np.array([(p.x, p.y, p.z) for p in verts], dtype=float)
    f = np.array(tris, dtype=np.int64)
    mesh = trimesh.Trimesh(vertices=v, faces=f, process=False)
    mesh.merge_vertices(digits_vertex=5)
    mesh.update_faces(mesh.nondegenerate_faces())
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    return mesh


def check_watertight() -> list[Result]:
    out = []
    for key, (shape, _filament, _note) in A.printed_parts().items():
        solids = g.solids(shape)
        mesh = to_mesh(shape, *A.MESH.get(key, (0.01, 0.1)))
        vol_cad = g.volume(shape)
        ok = (
            shape.isValid()
            and (len(solids) == 1 or key in A.MULTI_BODY)
            and mesh.is_watertight
            and mesh.is_winding_consistent
            and mesh.volume > 0
            and abs(mesh.volume - vol_cad) / vol_cad < A.MESH_VOLUME_TOL.get(key, 0.015)
        )
        bb = shape.BoundingBox()
        out.append(
            Result(
                f"watertight:{key}",
                ok,
                f"solids={len(solids)} valid={shape.isValid()} watertight={mesh.is_watertight} "
                f"winding={mesh.is_winding_consistent} V_cad={vol_cad:.0f} V_mesh={mesh.volume:.0f} mm3 "
                f"tris={len(mesh.faces)}",
                {
                    "volume_mm3": vol_cad,
                    "mass_g_petg": vol_cad * 1.27e-3,
                    "bbox": [bb.xlen, bb.ylen, bb.zlen],
                    "triangles": int(len(mesh.faces)),
                },
            )
        )
    return out


# --------------------------------------------------------------------------
# static fit
# --------------------------------------------------------------------------
def interference(items: list[A.Item], only_groups: tuple[set[str], set[str]] | None = None) -> list[tuple[str, str, float]]:
    """Common volume of every pair of items (bounding boxes pre-filter)."""
    todo = [it for it in items if it.check]
    shapes = {it.key: it.shape() for it in todo}
    hits = []
    for i, a in enumerate(todo):
        for b in todo[i + 1 :]:
            if only_groups is not None:
                ga, gb = only_groups
                if not ((a.group in ga and b.group in gb) or (a.group in gb and b.group in ga)):
                    continue
            if not g.bbox_overlap(shapes[a.key], shapes[b.key]):
                continue
            v = 0.0
            for sa, _ in a.bodies:
                for sb, _ in b.bodies:
                    if g.bbox_overlap(sa, sb):
                        v += g.common_volume(sa, sb)
            if v > TOL_VOLUME or math.isnan(v):
                hits.append((a.key, b.key, v))
    return hits


def classify(hits: list[tuple[str, str, float]]) -> tuple[list, list]:
    """Split overlaps into intended (threads, press fits) and collisions."""
    intended, collisions = [], []
    for a, b, v in hits:
        rule = INTENDED_OVERLAP.get(frozenset((a, b)))
        if rule and v <= rule[0]:
            intended.append((a, b, v, rule[1]))
        else:
            collisions.append((a, b, v))
    return intended, collisions


def check_static_fit() -> list[Result]:
    items = A.build()
    hits = interference(items)
    intended, collisions = classify(hits)
    res = [
        Result(
            "fit:closed assembly",
            not collisions,
            f"{len(items)} items, {len(collisions)} collisions, {len(intended)} intended overlaps",
            {"collisions": collisions, "intended": intended},
        )
    ]
    return res


# --------------------------------------------------------------------------
# clearances that matter
# --------------------------------------------------------------------------
def check_clearances() -> list[Result]:
    it = A.by_key(A.build())
    out = []

    def need(name: str, a: str, b: str, minimum: float):
        d = g.min_distance(it[a].shape(), it[b].shape())
        out.append(Result(f"clearance:{name}", d >= minimum, f"{d:.2f} mm (need >= {minimum})", {"distance": d}))

    need("lid inner wall - stage dome", "lid", "stage", 0.0)
    need("ring - lid", "ring", "lid", 1.0)
    need("servo horn - stage", "horn", "stage", 0.3)
    need("servo horn - pawl (latched)", "horn", "pawl", 0.2)
    need("cell - charger board", "cell", "charger", 0.8)
    need("speaker - lid hook", "speaker", "lid", 1.0)
    need("base insert bosses - chassis", "inserts", "chassis", 0.0)
    need("reader harness and plugs - chassis", "harness", "chassis", 2.0)
    need("reader harness - bowl (window and wall)", "harness", "bowl", 0.5)
    # torsion spring: coil must run free, legs must sit on their seats
    coil, legs = it["spring"].bodies[0][0], it["spring"].bodies[1][0]
    for name, key in (("spring coil - lid", "lid"), ("spring coil - stage", "stage"), ("spring coil - sleeve", "sleeve")):
        d = g.min_distance(coil, it[key].shape())
        out.append(Result(f"clearance:{name}", d >= 0.2, f"{d:.2f} mm (need >= 0.2)", {"distance": d}))
    d = g.min_distance(legs, it["stage"].shape())
    out.append(Result("clearance:spring body leg on the stage yoke", d <= 0.3, f"{d:.2f} mm gap (seat, need <= 0.3)", {"distance": d}))
    # the lid leg must lie along the lid's back wall: measure at its far end
    import math as _m
    a = _m.radians(180.0 - P.SPRING_DEFL_CLOSED)
    rm = (P.SPRING_OD - P.SPRING_WIRE) / 2
    tip = cq.Vector(P.HINGE_X + rm * _m.cos(a + _m.pi / 2) + (P.SPRING_LEG - 1.0) * _m.cos(a), P.SPRING_BODY / 2 - P.SPRING_WIRE / 2, P.HINGE_Z + rm * _m.sin(a + _m.pi / 2) + (P.SPRING_LEG - 1.0) * _m.sin(a))
    probe = cq.Solid.makeSphere(P.SPRING_WIRE / 2, tip, cq.Vector(0, 0, 1), -90.0, 90.0, 360.0)
    d = g.min_distance(probe, it["lid"].shape())
    v = g.common_volume(legs, it["lid"].shape()) + g.common_volume(legs, it["stage"].shape())
    out.append(Result("clearance:spring lid leg along the lid wall", d <= 1.2 and v < 0.05, f"leg tip is {d:.2f} mm from the lid wall (it bends onto the wall under load); overlap of the legs with lid or stage {v:.2f} mm3", {"distance": d}))
    # battery can be lifted straight out once the stage is removed
    cell = it["cell"].shape()
    blocked = []
    for dz in (3.0, 8.0, 15.0, 25.0, 40.0):
        up = g.move(cell, dz=dz)
        for key in ("charger", "servo", "mcu", "amp", "boost", "contacts", "band", "speaker"):
            if g.common_volume(up, it[key].shape()) > TOL_VOLUME:
                blocked.append((dz, key))
    out.append(Result("clearance:cell lifts straight out of its cradle", not blocked, f"cell lifted 3..40 mm with the stage removed: blocked by {blocked or 'nothing'}", {"blockers": blocked}))
    return out


# --------------------------------------------------------------------------
# motion
# --------------------------------------------------------------------------
def check_lid_motion(step: float = 2.5) -> list[Result]:
    """Open the lid in steps and look for collisions of the lid group."""
    worst: list[tuple[float, str, str, float]] = []
    angles = [round(i * step, 2) for i in range(int(P.LID_OPEN_DEG / step) + 1)]
    if angles[-1] != P.LID_OPEN_DEG:
        angles.append(P.LID_OPEN_DEG)
    for deg in angles:
        # the pawl is retracted as soon as the lid moves; at 0 deg it is engaged
        items = A.build(lid_deg=deg, pawl_deg=(0.0 if deg == 0 else P.PAWL_RELEASE_DEG), horn_deg=(None if deg == 0 else P.HORN_RELEASE_DEG))
        hits = interference(items, only_groups=({"lid"}, {"fixed", "pawl", "horn", "slider"}))
        _, collisions = classify(hits)
        for a, b, v in collisions:
            worst.append((deg, a, b, v))
    ok = not worst
    detail = f"{len(angles)} positions 0..{P.LID_OPEN_DEG:.0f} deg, {len(worst)} collisions"
    res = [Result("motion:lid opening sweep", ok, detail, {"collisions": worst})]
    # the end stop must really stop the lid: 3 deg further has to collide with the stage
    items = A.build(lid_deg=P.LID_OPEN_DEG + 3.0, pawl_deg=P.PAWL_RELEASE_DEG, horn_deg=P.HORN_RELEASE_DEG)
    v = sum(h[2] for h in interference(items, only_groups=({"lid"}, {"fixed"})) if "stage" in h[:2])
    res.append(Result("motion:end stop holds at the open angle", v > 0.5, f"overlap lid/stage at {P.LID_OPEN_DEG + 3:.0f} deg: {v:.2f} mm3 (must be > 0)", {"overlap": v}))
    # the torsion spring coil stays clear of lid and stage over the whole travel
    it0 = A.by_key(A.build())
    coil = it0["spring"].bodies[0][0]
    dmin = 99.0
    for deg in angles[::3] + [P.LID_OPEN_DEG]:
        dmin = min(dmin, g.min_distance(coil, S.open_lid(S.lid(), deg)))
    res.append(Result("motion:spring coil clears the lid", dmin >= 0.2, f"minimum distance coil/lid over the travel: {dmin:.2f} mm", {"distance": dmin}))
    return res


def check_latch() -> list[Result]:
    out = []
    # 1. engaged pawl must block the lid: lifting the lid by 1.5 deg must collide
    items = A.build(lid_deg=1.5, pawl_deg=0.0)
    hit = [h for h in interference(items, only_groups=({"lid"}, {"pawl"}))]
    v = sum(h[2] for h in hit)
    out.append(Result("latch:engaged pawl holds the lid", v > 0.5, f"overlap when lid is forced to 1.5 deg: {v:.2f} mm3 (must be > 0)", {"overlap": v}))
    # 2. released pawl frees the lid over the whole first part of the travel
    free = True
    worst = 0.0
    for deg in (0.0, 0.5, 1.0, 2.0, 4.0, 8.0):
        items = A.build(lid_deg=deg, pawl_deg=P.PAWL_RELEASE_DEG, horn_deg=P.HORN_RELEASE_DEG)
        v = sum(h[2] for h in interference(items, only_groups=({"lid"}, {"pawl"})))
        worst = max(worst, v)
        free = free and v <= TOL_VOLUME
    out.append(Result("latch:released pawl frees the lid", free, f"max overlap lid/pawl with pawl at {P.PAWL_RELEASE_DEG:.0f} deg: {worst:.3f} mm3", {"overlap": worst}))
    # 3. pawl travel is collision free against everything that does not move with it
    bad = []
    for deg in np.linspace(0.0, P.PAWL_RELEASE_DEG + 4.0, 8):
        horn = P.HORN_REST_DEG if deg == 0 else P.HORN_RELEASE_DEG + 4.0
        items = A.build(pawl_deg=float(deg), horn_deg=horn, lid_deg=(0.0 if deg == 0 else 12.0))
        hits = interference(items, only_groups=({"pawl"}, {"fixed", "slider", "lid"}))
        _, col = classify(hits)
        bad += [(float(deg), a, b, v) for a, b, v in col]
    out.append(Result("latch:pawl travel", not bad, f"0..{P.PAWL_RELEASE_DEG + 4:.0f} deg, {len(bad)} collisions", {"collisions": bad}))
    # 4. servo horn sweep: rest -> release (+ over-travel), must only ever touch the pawl post
    bad = []
    for hdeg in np.linspace(P.HORN_REST_DEG - 15.0, P.HORN_RELEASE_DEG + 10.0, 9):
        items = A.build(horn_deg=float(hdeg), pawl_deg=P.PAWL_RELEASE_DEG + 4.0, lid_deg=12.0)
        hits = interference(items, only_groups=({"horn"}, {"fixed", "slider", "lid"}))
        _, col = classify(hits)
        bad += [(float(hdeg), a, b, v) for a, b, v in col]
    out.append(Result("latch:servo horn sweep", not bad, f"{P.HORN_REST_DEG - 15:.0f}..{P.HORN_RELEASE_DEG + 10:.0f} deg, {len(bad)} collisions", {"collisions": bad}))
    # 5. horn reaches the post: at the release angle the horn must have pushed the pawl
    it = A.by_key(A.build(horn_deg=P.HORN_RELEASE_DEG, pawl_deg=P.PAWL_RELEASE_DEG))
    d = g.min_distance(it["horn"].shape(), it["pawl"].shape())
    out.append(Result("latch:horn drives pawl at release angle", d < 0.8, f"gap horn/post with both at release pose: {d:.2f} mm (contact expected, < 0.8)", {"gap": d}))
    # 6. emergency paper clip: straight path from the slit to the pawl lug
    path = S.emergency_channel(1.2, 21.0)
    it = A.by_key(A.build())
    blockers = []
    for key in ("bezel", "lens", "cone", "chassis", "stage", "lid", "band", "speaker", "led", "bowl", "spk_clamp"):
        v = g.common_volume(path, it[key].shape())
        if v > TOL_VOLUME:
            blockers.append((key, v))
    reach = g.min_distance(S.emergency_channel(1.2, 24.0), it["pawl"].shape())
    out.append(Result("latch:emergency clip path is free", not blockers and reach < 0.01, f"blocked by {blockers or 'nothing'}; path reaches the pawl lug: {reach < 0.01}", {"blockers": blockers}))
    return out


def check_ring_lock() -> list[Result]:
    out = []
    # locked: lifting the ring by 2 mm must collide with the pin
    it = A.by_key(A.build(locked=True))
    lifted = g.move(it["ring"].shape(), dz=2.0)
    v = g.common_volume(lifted, it["lock_pin"].shape())
    out.append(Result("ring:locked pin retains the ring", v > 0.5, f"overlap pin/ring when the ring is lifted 2 mm: {v:.2f} mm3 (must be > 0)", {"overlap": v}))
    # released: ring can be lifted out
    it = A.by_key(A.build(locked=False))
    free = True
    for dz in (0.0, 2.0, 5.0, 10.0, 16.0):
        ring = g.move(it["ring"].shape(), dz=dz)
        for key in ("lock_pin", "cradle", "stage", "slider"):
            if g.common_volume(ring, it[key].shape()) > TOL_VOLUME:
                free = False
    out.append(Result("ring:released ring lifts out freely", free, "ring lifted 0..16 mm with the pin retracted", {}))
    # slider travel collision free
    bad = []
    for locked in (True, False):
        items = A.build(locked=locked)
        hits = interference(items, only_groups=({"slider"}, {"fixed", "lid", "pawl", "horn"}))
        _, col = classify(hits)
        bad += col
    out.append(Result("ring:lock slider travel", not bad, f"{len(bad)} collisions in both end positions", {"collisions": bad}))
    # snugness: play of the ring in its seat
    r_out = P.RING_ID / 2 + P.RING_THICK
    play_x = (P.RING_SLOT_W - P.RING_BAND) / 2
    lift = (P.Z_DECK - P.LOCK_PIN_DEPTH - P.LOCK_PIN_D / 2) - (A.ring_centre_z() - P.RING_ID / 2)
    out.append(Result("ring:seat play", lift < 1.5, f"side play {play_x:.2f} mm per side before felt lining; locked lift play {lift:.2f} mm; ring sunk {P.RING_SINK:.1f} of {2 * r_out:.1f} mm", {"lift_play": lift}))
    return out


def check_assembly_paths() -> list[Result]:
    """Can the sub-assemblies be put together in the order of the manual?"""
    out = []
    it = A.by_key(A.build())
    core_keys = ["chassis", "contacts", "mcu", "amp", "charger", "boost", "servo", "horn", "servo_screws", "speaker", "spk_clamp", "clamp_screws", "led", "cone", "lens", "bezel"]
    core = [it[k].shape() for k in core_keys]
    bad = []
    for dz in (2.0, 5.0, 10.0, 20.0, 35.0, 55.0):
        for shape, key in zip(core, core_keys):
            for fixed in ("bowl", "inserts", "harness"):
                v = g.common_volume(g.move(shape, dz=dz), it[fixed].shape())
                if v > TOL_VOLUME:
                    bad.append((dz, key, fixed, v))
    out.append(Result("assembly:core drops into the bowl", not bad, f"core lifted 2..55 mm above its seat, {len(bad)} collisions with bowl, inserts or the parked harness", {"collisions": bad}))
    bad = []
    for dz in (1.0, 3.0, 6.0, 12.0, 25.0):
        band = g.move(it["band"].shape(), dz=dz)
        for key in core_keys + ["bowl", "cell"]:
            v = g.common_volume(band, it[key].shape())
            if v > TOL_VOLUME:
                bad.append((dz, key, v))
    out.append(Result("assembly:band lowers over the core", not bad, f"band lifted 1..25 mm, {len(bad)} collisions", {"collisions": bad}))
    bad = []
    top_keys = ["stage", "pawl", "pawl_screw", "cradle", "lock_pin", "slider", "lid", "hinge_pin", "sleeve"]
    for dz in (1.0, 3.0, 6.0, 12.0, 25.0, 40.0):
        for tk in top_keys:
            moved = g.move(it[tk].shape(), dz=dz)
            for key in core_keys + ["bowl", "band", "cell"]:
                v = g.common_volume(moved, it[key].shape())
                if v > TOL_VOLUME:
                    bad.append((dz, tk, key, v))
    # the stack screws are only reachable with the lid open, so repeat with the lid at its stop
    ito = A.by_key(A.build(lid_deg=P.LID_OPEN_DEG, pawl_deg=P.PAWL_RELEASE_DEG, horn_deg=P.HORN_RELEASE_DEG))
    for dz in (1.0, 3.0, 6.0, 12.0, 25.0, 40.0):
        moved = g.move(ito["lid"].shape(), dz=dz)
        for key in core_keys + ["bowl", "band", "cell"]:
            v = g.common_volume(moved, ito[key].shape())
            if v > TOL_VOLUME:
                bad.append((dz, "lid(open)", key, v))
    out.append(Result("assembly:stage with lid lowers onto the core", not bad, f"stage sub-assembly lifted 1..40 mm, lid closed and open, {len(bad)} collisions", {"collisions": bad}))
    # a USB-C plug body must reach the band at the port
    it2 = A.by_key(A.build())
    plug = g.rot(g.box(P.R_BAND + 0.05, P.R_BAND + 20.0, -P.USB_PLUG_W / 2, P.USB_PLUG_W / 2, P.USB_Z - P.USB_PLUG_H / 2, P.USB_Z + P.USB_PLUG_H / 2), "z", P.USB_AZ)
    blockers = [(k, g.common_volume(plug, it2[k].shape())) for k in ("bowl", "band", "lid")]
    blockers = [(k, v) for k, v in blockers if v > TOL_VOLUME]
    out.append(Result("assembly:USB-C plug body reaches the socket", not blockers, f"plug body {P.USB_PLUG_W} x {P.USB_PLUG_H} mm at the port: blocked by {blockers or 'nothing'}", {"blockers": blockers}))
    return out


# --------------------------------------------------------------------------
# numbers that have to hold
# --------------------------------------------------------------------------
DENSITY = {"printed": 1.27e-3}   # g / mm^3 (PETG)
MASS_G = {
    "reader": 9.0, "mcu": 3.0, "amp": 1.5, "charger": 2.0, "boost": 1.5, "servo": 9.0, "horn": 0.5,
    "speaker": 10.0, "led": 0.4, "cell": 48.0, "contacts": 1.5, "hall": 0.2, "ring": 3.5,
    "spring": 0.4, "hinge_pin": 0.5, "lock_pin": 1.3, "stack_screws": 4.4, "inserts": 2.1,
    "harness": 6.0, "turf_screws": 1.6, "base_screws": 2.0,
}
BASE_KEYS = ("grass_base", "grass_top", "grass_blades", "grass_spot", "reader", "hall", "harness", "turf_screws", "base_screws")
FIGURE_MASS_G = P.TONIE_MASS_G     # a Tonie standing on the spot (research/09)


def mass_table(items: list[A.Item]) -> list[tuple[str, float, tuple[float, float, float]]]:
    rows = []
    for it in items:
        shape = it.shape()
        if it.kind == "printed":
            m = g.volume(shape) * DENSITY["printed"]
        else:
            m = MASS_G.get(it.key, 0.5)
        try:
            c = g.centre_of_mass(shape)
        except Exception:
            bb = shape.BoundingBox()
            c = ((bb.xmin + bb.xmax) / 2, (bb.ymin + bb.ymax) / 2, (bb.zmin + bb.zmax) / 2)
        rows.append((it.key, m, c))
    return rows


def centre_of_gravity(items: list[A.Item]) -> tuple[float, tuple[float, float, float]]:
    rows = mass_table(items)
    m = sum(r[1] for r in rows)
    return m, tuple(sum(r[1] * r[2][i] for r in rows) / m for i in range(3))


def check_physics() -> list[Result]:
    out = []
    closed = A.build()
    opened = A.build(lid_deg=P.LID_OPEN_DEG, pawl_deg=P.PAWL_RELEASE_DEG)
    # the ball without its base: it must still stand by itself (bench, assembly)
    ball_closed = [i for i in closed if i.key not in BASE_KEYS]
    ball_open = [i for i in opened if i.key not in BASE_KEYS]
    mb, cgb = centre_of_gravity(ball_closed)
    out.append(Result("physics:ball alone, mass and centre of gravity", cgb[2] < 0, f"mass {mb:.0f} g, CoG x={cgb[0]:.1f} y={cgb[1]:.1f} z={cgb[2]:.1f} mm (below the ball centre: self-righting)", {"mass": mb, "cg": cgb}))
    _, cgbo = centre_of_gravity(ball_open)
    margin = P.R_FLAT - math.hypot(cgbo[0], cgbo[1])
    out.append(Result("physics:ball alone stands on its flat with the lid open", margin > 2.0, f"CoG with open lid x={cgbo[0]:.1f} y={cgbo[1]:.1f}; flat radius {P.R_FLAT:.1f} mm -> tipping margin {margin:.1f} mm", {"cg_open": cgbo, "margin": margin}))
    # the complete device on the flat of the ball and the underside of the tongue
    hull = _hull(B.sole_outline())
    m, cg = centre_of_gravity(closed)
    m2, cg2 = centre_of_gravity(opened)
    fig = (P.SPOT_X, 0.0)
    cg3 = tuple((m * cg[i] + FIGURE_MASS_G * fig[i]) / (m + FIGURE_MASS_G) for i in range(2))
    margins = {"closed": _margin(hull, cg), "lid open": _margin(hull, cg2), "closed with a figure on the spot": _margin(hull, cg3)}
    out.append(
        Result(
            "physics:device stands on the ball's flat and the tongue",
            min(margins.values()) > 15.0,
            f"mass {m:.0f} g; CoG closed x={cg[0]:.1f}, open x={cg2[0]:.1f}, with a {FIGURE_MASS_G:.0f} g figure x={cg3[0]:.1f} mm; distance of the CoG from the edge of the standing area (flat of the ball and underside of the tongue together): "
            + ", ".join(f"{k} {v:.0f} mm" for k, v in margins.items()),
            {"mass": m, "cg": cg, "cg_open": cg2, "margins": margins},
        )
    )
    # spring versus gravity
    lid_items = [i for i in closed if i.key == "lid"]
    lm, lcg = centre_of_gravity(lid_items)
    arm = lcg[0] - P.HINGE_X
    grav = lm * 9.81e-3 * arm                       # N mm
    rate, mn = 0.288, 41.48                          # Gutekunst T-16324: N mm / deg, Mn
    m_closed = rate * P.SPRING_DEFL_CLOSED
    m_open = rate * (P.SPRING_DEFL_CLOSED - P.LID_OPEN_DEG)
    worst = 0.8 * m_closed - grav
    out.append(
        Result(
            "physics:spring opens the lid",
            worst > 3.0 and m_open > 2.0 and m_closed <= 0.85 * mn,
            f"lid {lm:.0f} g, gravity torque {grav:.1f} N mm; spring {m_closed:.1f} N mm closed ({100 * m_closed / mn:.0f} % of Mn), "
            f"{m_open:.1f} N mm at {P.LID_OPEN_DEG:.0f} deg; net opening torque with a -20 % spring: {worst:.1f} N mm",
            {"lid_mass": lm, "gravity_torque": grav, "spring_closed": m_closed, "spring_open": m_open},
        )
    )
    latch_arm = P.HOOK_X0 - P.HINGE_X
    f_latch = (1.2 * m_closed - grav) / latch_arm
    out.append(Result("physics:latch load", f_latch < 2.0, f"force on the pawl nose with a +20 % spring: {f_latch:.2f} N at {latch_arm:.0f} mm from the hinge", {"latch_force": f_latch}))
    slit_area = 4 * math.radians(P.SLIT_ARC) * P.SLIT_R * P.SLIT_W
    cone_area = math.pi * (P.SPK_BASKET_D / 2 - 1.5) ** 2
    out.append(Result("audio:slit open area", slit_area / cone_area >= 0.10, f"{slit_area:.0f} mm2 of slits = {100 * slit_area / cone_area:.0f} % of the cone area ({cone_area:.0f} mm2)", {"slit_area": slit_area}))
    return out


def _hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Convex hull, counter-clockwise (Andrew's monotone chain)."""
    pts = sorted(set(points))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list[tuple[float, float]] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[tuple[float, float]] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _margin(hull: list[tuple[float, float]], p) -> float:
    """Distance of a point from the nearest edge of a CCW hull (negative outside)."""
    best = 1e9
    for i, a in enumerate(hull):
        b = hull[(i + 1) % len(hull)]
        ex, ey = b[0] - a[0], b[1] - a[1]
        best = min(best, (ex * (p[1] - a[1]) - ey * (p[0] - a[0])) / math.hypot(ex, ey))
    return best


def check_grass_base() -> list[Result]:
    """The grass tongue: joint to the ball, reader pocket, cable path, standing spot."""
    out = []
    it = A.by_key(A.build(with_tonie=True))
    bowl, tray, turf = it["bowl"].shape(), it["grass_base"].shape(), it["grass_top"].shape()
    ball_keys = ("bowl", "band", "lid", "bezel", "lens")
    screws = B.base_screw_xy()

    # 1. joint: the ball touches the seat pads and nothing else; the tongue is flush and stays in front
    d_pad, d_turf = g.min_distance(bowl, tray), g.min_distance(bowl, turf)
    v = g.common_volume(bowl, tray) + g.common_volume(bowl, turf)
    out.append(Result("base:ball bears on the seat pads only", d_pad < 0.02 and d_turf >= P.CUP_GAP - 0.05 and v < TOL_VOLUME, f"bowl to the {len(screws)} pads {d_pad:.2f} mm (contact), bowl to turf {d_turf:.2f} mm, overlap {v:.2f} mm3; elsewhere the tongue keeps {P.CUP_GAP} mm from the ball", {"pad": d_pad, "turf": d_turf}))
    # flush: ball and tongue both touch the table plane and nothing reaches below it
    table = g.box(-200.0, 300.0, -200.0, 200.0, P.Z_FLAT - 5.0, P.Z_FLAT)
    below = sum(g.common_volume(it[k].shape(), table) for k in ("bowl", "grass_base", "grass_top", "base_screws", "turf_screws"))
    gap_t, gap_b = g.min_distance(tray, table), g.min_distance(bowl, table)
    bb = tray.BoundingBox()
    flush = below < TOL_VOLUME and gap_t < 1e-4 and gap_b < 1e-4
    out.append(Result("base:tongue is flush with the ball's flat and stays in front of it", flush and bb.xmin >= -0.05 and bb.ymax < P.R, f"the underside of the tongue and the flat of the ball both lie on the table plane (gaps {gap_t:.3f} and {gap_b:.3f} mm) and nothing reaches below it ({below:.2f} mm3, screw heads included); the tongue begins {P.X_REAR:.0f} mm in front of the ball's axis, under its belly, is {2 * P.TONGUE_W:.0f} mm wide and {P.BASE_T:.0f} mm high and reaches {P.SPOT_X + P.TONGUE_W - P.R:.0f} mm beyond the ball: nothing of it lies beside or behind the ball", {"x_rear": P.X_REAR, "reach": P.SPOT_X + P.TONGUE_W - P.R, "width": 2 * P.TONGUE_W, "below": below}))

    # 2. grass keeps clear of the ball.  Every outer part of the ball lies inside the sphere of
    #    radius R (the front is even flattened), so the distance to that sphere is the safe measure.
    #    The one exception is the rim of the button's ring, which stands BEZEL_PROUD out of it: the
    #    blades near it are measured against the ring itself.
    shell = g.sphere(P.R + 40.0).cut(g.sphere(P.R + P.BEZEL_PROUD + 0.02))
    proud = sum(g.common_volume(it[k].shape(), shell) for k in ball_keys)
    sphere = g.inter(g.sphere(P.R), g.slab(P.Z_FLAT, P.Z_BOWL_RIM))
    grass = [B.blade_solid(b) for b in B.blades()] + [B.mound_solid(m) for m in B.mounds()]
    worst = min(g.min_distance(x, sphere) for x in grass)
    bezel = it["bezel"].shape()
    near = [x for x in grass if g.bbox_overlap(x, bezel, 4.0)]
    d_bezel = min((g.min_distance(x, bezel) for x in near), default=99.0)
    z_grass = max(x.BoundingBox().zmax for x in grass)
    out.append(Result("base:grass blades clear the ball", min(worst, d_bezel) >= P.BLADE_GAP - 0.2 and proud < TOL_VOLUME and z_grass < P.Z_BOWL_RIM, f"{len(B.blades())} blades in {len(B.mounds())} tufts, nearest is {worst:.2f} mm from the ball's sphere (need >= {P.BLADE_GAP - 0.2:.1f}); no part of the ball stands more than {P.BEZEL_PROUD} mm outside that sphere ({proud:.2f} mm3), and the ring round the button, which does stand out by that much, has {'no blade within 4 mm' if not near else f'its nearest blade at {d_bezel:.2f} mm'}; the tallest blade ends {P.Z_BOWL_RIM - z_grass:.0f} mm below the rim of the bowl", {"distance": worst, "bezel": d_bezel}))

    # 3. the ball can be lowered onto the tongue, and the screws reach their inserts.  Below its
    #    equator the ball narrows downwards, so blades that clear it in place clear it all the way down.
    bad = []
    for dz in (0.5, 2.0, 5.0, 12.0, 30.0):
        for key in ball_keys:
            moved = g.move(it[key].shape(), dz=dz)
            for name, fixed in (("grass_base", tray), ("grass_top", turf), ("turf_screws", it["turf_screws"].shape())):
                vv = g.common_volume(moved, fixed)
                if vv > TOL_VOLUME:
                    bad.append((dz, key, name, vv))
        lifted = g.move(sphere, dz=dz)
        if min(g.min_distance(x, lifted) for x in grass) < 0.3:
            bad.append((dz, "bowl", "blades", 0.0))
    out.append(Result("base:ball lowers onto the tongue", not bad, f"ball lifted 0.5..30 mm, {len(bad)} collisions with tray, turf, turf screws or blades", {"collisions": bad}))
    tip = P.Z_SOLE + P.CSK_RECESS + P.BASE_SCREW_L
    grip = tip - (P.Z_BASE_BOSS - 5.7)
    wedge = min(-math.sqrt((P.R + P.CUP_GAP) ** 2 - P.BASE_SCREW_RHO**2) - P.Z_SOLE for _ in screws)
    out.append(Result("base:screws engage the inserts", 3.0 <= grip <= 5.7 and tip <= P.Z_BASE_BOSS + 0.01 and wedge >= 5.0, f"{len(screws)} x M3 x {P.BASE_SCREW_L:.0f} countersunk through {wedge:.1f} mm of tongue: {grip:.1f} mm of thread in the 5.7 mm insert, tip {P.Z_BASE_BOSS - tip:.1f} mm below the top of the boss", {"grip": grip}))

    # 4. reader pocket and turf
    reader, hall = it["reader"].shape(), it["hall"].shape()
    bad = []
    for dz in (0.5, 2.0, 5.0, 12.0):
        for key in ("reader", "hall"):
            vv = g.common_volume(g.move(it[key].shape(), dz=dz), tray)
            if vv > TOL_VOLUME:
                bad.append((dz, key, vv))
        for fixed in ("grass_base", "reader", "hall"):
            vv = g.common_volume(g.move(turf, dz=dz), it[fixed].shape())
            if vv > TOL_VOLUME:
                bad.append((dz, "grass_top", fixed, vv))
    d_seat, d_roof = g.min_distance(reader, tray), g.min_distance(reader, turf)
    hold = P.BLUE_LEDGE_ANT - 2 * max(P.BLUE_CL_X, P.BLUE_CL_Y)      # ledge left under a board pushed to one side
    out.append(Result("base:reader drops into its pocket, turf closes it", not bad and d_seat < 0.02 and 0.0 <= d_roof <= 0.3 and hold >= 1.0, f"board on its ledge ({d_seat:.2f} mm), {d_roof:.2f} mm under the turf; pushed to one side of its {2 * P.BLUE_CL_X + P.BLUE_L:.1f} x {2 * P.BLUE_CL_Y + P.BLUE_W:.1f} mm pocket, the antenna half still rests on {hold:.1f} mm of ledge; reader, hall switch and turf lifted 0.5..12 mm: {len(bad)} collisions", {"collisions": bad}))
    gap_under = P.Z_PCB_BOT - P.Z_TRAY_FLOOR
    d_hall = g.min_distance(hall, reader)
    out.append(Result("base:room under the reader board", gap_under >= P.BLUE_COMP_H + 0.8 and d_hall >= 0.1, f"{gap_under:.1f} mm between tray floor and board for components ({P.BLUE_COMP_H} mm) and wires; the hall switch lies on the floor of the pocket, its face {d_hall:.2f} mm below the board", {"gap": gap_under}))

    # 5. cable path: a plug must pass the window; the window must stay hidden
    r0, r1 = P.WINDOW_R0, P.WINDOW_R1
    half = math.radians(P.WINDOW_HALF_DEG)
    fits = None
    pw, ph = P.PLUG_PASS
    xc = r0 + ph / 2
    while xc + ph / 2 <= r1:
        if math.hypot(xc + ph / 2, pw / 2) <= r1 and math.atan2(pw / 2, xc - ph / 2) <= half:
            fits = xc
            break
        xc += 0.05
    blocked = 1.0
    if fits is not None:
        probe = g.box(fits - ph / 2 + 0.02, fits + ph / 2 - 0.02, -pw / 2 + 0.02, pw / 2 - 0.02, P.Z_FLAT - 3, -31.0)
        blocked = g.common_volume(probe, bowl)
    hidden = P.Z_TURF + math.sqrt(P.R**2 - r1**2)
    out.append(Result("base:plug passes the cable window, window is hidden", fits is not None and blocked < TOL_VOLUME and hidden >= 0.5 and P.PLUG_W <= pw and P.PLUG_H <= ph, f"the {r1 - r0:.0f} mm wide window lets a section of {pw} x {ph} mm pass ({'at r = %.1f mm' % fits if fits is not None else 'NO position'}); the chosen 6-pin pair measures {P.PLUG_W} x {P.PLUG_H} mm; the window's upper edge lies {hidden:.1f} mm below the turf surface, behind the tongue", {"hidden": hidden}))

    # 6. the figure stands free on a plain flat spot
    figure = it["tonie"].shape()
    env = B.figure_envelope()
    ball = [it[k].shape() for k in ball_keys]
    d_fig = min(g.min_distance(figure, x) for x in ball)
    d_env = min(g.min_distance(env, x) for x in ball)
    out.append(Result("figure:clear of the ball", d_env >= 2.0, f"dummy figure {d_fig:.1f} mm, envelope of all four Pokémon figures (Ø{P.TONIE_ENVELOPE_D:.0f} x {P.TONIE_ENVELOPE_H:.0f} mm) {d_env:.1f} mm from the ball", {"figure": d_fig, "envelope": d_env}))
    foot = g.cyl_z(P.TONIE_BASE_D / 2, P.Z_TURF, P.Z_TURF + 20.0, P.SPOT_X, 0.0)
    d_blade = min(g.min_distance(x, foot) for x in grass)
    r_plain = P.SPOT_CLEAR_R - 0.5
    above = g.cyl_z(r_plain, P.Z_TURF + 0.01, P.Z_TURF + 40.0, P.SPOT_X, 0.0)
    below = g.cyl_z(r_plain, P.Z_TURF - 0.3, P.Z_TURF, P.SPOT_X, 0.0)
    proud = sum(g.common_volume(above, x) for x in grass) + g.common_volume(above, turf) + g.common_volume(above, it["grass_spot"].shape())
    filled = (g.common_volume(below, turf) + g.common_volume(below, it["grass_spot"].shape())) / g.volume(below)
    ahead = [math.degrees(math.atan2(abs(b.y), b.x - P.SPOT_X)) for b in B.blades() if math.hypot(b.x - P.SPOT_X, b.y) < P.TONGUE_W + 3.0]
    out.append(Result("figure:stands free on a plain flat spot", proud < TOL_VOLUME and filled > 0.999 and d_blade >= P.GRASS_GAP - 1.5 and min(ahead) >= P.FRONT_OPEN_DEG, f"within {r_plain:.1f} mm of the spot centre nothing stands above the surface ({proud:.2f} mm3) and nothing is recessed (surface {100 * filled:.1f} % filled): no rim, no pocket, no lock; nearest grass {d_blade:.1f} mm from a Ø{P.TONIE_BASE_D:.0f} mm foot, so a figure may stand {d_blade - 1.0:.0f} mm off centre before it touches grass; no grass within {min(ahead):.0f}° of straight ahead", {"blade": d_blade, "front_deg": min(ahead)}))
    # the lawn must not be mirrored: compare the tuft positions with their mirror image
    lawn = B.tufts()
    pos = [(t.mound.x, t.mound.y) for t in lawn]
    twin = [min(math.hypot(x - u, -y - w) for j, (u, w) in enumerate(pos) if j != i) for i, (x, y) in enumerate(pos)]   # 0 for every tuft of a mirrored lawn
    sizes = [len(t.blades) for t in lawn]
    heights = [b.h for b in B.blades()]
    left = sum(1 for _, y in pos if y > 0)
    spread = len({int(((t.mound.out_deg - 90.0) % 180.0) // 30.0) for t in lawn})   # how many of six directions occur
    out.append(Result("grass:tufts are scattered, not mirrored", min(twin) >= 3.0 and max(sizes) >= min(sizes) + 3 and max(heights) >= 2.5 * min(heights) and spread >= 5, f"{len(pos)} tufts ({left} left of the centre line, {len(pos) - left} right) with {min(sizes)} to {max(sizes)} blades each, blades {min(heights):.0f} to {max(heights):.0f} mm high, tufts turned in {spread} of 6 direction classes; no tuft has a twin on the other side: the nearest mirror image of another tuft is {min(twin):.1f} mm away at least and {sum(twin) / len(twin):.1f} mm on average. Places, sizes, directions and leaf shapes come from a random generator with a fixed seed (LAWN_SEED)", {"tufts": len(pos), "twin_min": min(twin), "sizes": sizes}))

    # 7. reading geometry
    d_far, d_near = P.Z_TURF - P.Z_PCB_BOT, P.Z_TURF - P.Z_PCB_TOP
    out.append(Result("rfid:antenna to the figure's foot", d_far <= 4.0, f"antenna copper {d_near:.1f} to {d_far:.2f} mm below the standing surface (plain side to component side of the board); revision 1 had 10.6 mm", {"distance": d_far}))
    h_table = P.Z_PCB_BOT - P.Z_SOLE
    out.append(Result("rfid:antenna above the table", h_table >= 10.0, f"antenna copper {h_table:.1f} mm above whatever the tongue stands on; 10 mm is the spacing to metal that TI recommends (research/02 section 3.2); revision 2 had 3.2 mm", {"distance": h_table}))
    d_mag = P.Z_TURF - (B.HALL_SEAT_Z + P.HALL_T)
    z_near, z_far = d_mag + 0.5 + 1.0, d_mag + 0.5 + 2.0        # element 0.5 mm inside the package, pole face 1-2 mm inside the foot

    def on_axis(z: float, br: float = 1.25) -> float:
        """Field in mT on the axis of an ideal magnet of TONIE_MAGNET_D x TONIE_MAGNET_H, z below its pole face."""
        rm, lm = P.TONIE_MAGNET_D / 2, P.TONIE_MAGNET_H
        return 1000 * br / 2 * ((z + lm) / math.hypot(z + lm, rm) - z / math.hypot(z, rm))

    out.append(Result("rfid:hall switch below the standing spot", 7.5 <= z_near and z_far <= 10.0 and on_axis(z_far) >= 3 * 4.8, f"top of the hall switch {d_mag:.1f} mm below the standing surface, on the axis of the spot: its element lies {z_near:.1f} to {z_far:.1f} mm below the pole face of a magnet of a classic Tonie (Ø{P.TONIE_MAGNET_D:.0f} x {P.TONIE_MAGNET_H:.0f} mm, set 1-2 mm into the foot). An ideal magnet on the axis gives {on_axis(z_far):.0f} to {on_axis(z_near):.0f} mT there; by the table of research/09 section 7 a magnet 8 mm off the axis still gives about 6 mT, and two magnets 20 mm apart with like poles down about 6.5 mT. The switch needs 4.8 mT at most. Not covered: two magnets with unlike poles down, which cancel on the axis; the reader's IRQ line is wired as the second way to wake", {"distance": d_mag, "element_to_pole": (z_near, z_far), "on_axis_mT": (on_axis(z_far), on_axis(z_near))}))
    loop = it["reader"].bodies[1][0]
    near = {}
    for key in ("turf_screws", "base_screws", "inserts", "speaker", "cell", "servo", "harness"):
        near[key] = g.min_distance(loop, it[key].bodies[1][0] if key == "harness" else it[key].shape())
    worst_key = min((k for k in near if k != "harness"), key=lambda k: near[k])
    out.append(Result("rfid:metal keeps away from the antenna", near[worst_key] >= 6.0, "distance from the antenna loop: " + ", ".join(f"{k} {x:.0f} mm" for k, x in near.items()) + " (harness = its plugs)", {"near": near}))

    # 8. estimate: a hand pressing on the tip of the tongue while the ball is held
    # The seat is part of a sphere, so its pressure passes through the ball's centre and carries no
    # moment about it: the screws have to.  Upper bound: the front pair alone, in tension.
    force = 20.0
    x_tip = P.SPOT_X + P.TONGUE_W
    f_screw = force * x_tip / (2 * max(x for x, _ in screws))
    # bending of the tray where the reader pocket begins: two rails beside the pocket and the floor under it
    wr, hr = P.TONGUE_W - B.POCKET[2], P.Z_RAIL - P.Z_SOLE
    wf, hf = 2 * B.POCKET[2], P.TRAY_FLOOR
    area = 2 * wr * hr + wf * hf
    zc = (2 * wr * hr * hr / 2 + wf * hf * hf / 2) / area
    inertia = 2 * (wr * hr**3 / 12 + wr * hr * (hr / 2 - zc) ** 2) + wf * hf**3 / 12 + wf * hf * (hf / 2 - zc) ** 2
    sigma = force * (x_tip - B.POCKET[0]) * max(zc, hr - zc) / inertia
    out.append(Result("base:load estimate for a push on the tongue", f_screw < 150.0 and sigma < 10.0, f"{force:.0f} N on the tip with the ball held: at most {f_screw:.0f} N of tension in each front screw (an M3 insert in PETG holds several hundred), about {sigma:.1f} MPa bending stress in the tray where the pocket begins (PETG yields near 45 MPa; revision 2 had 13 MPa); estimate by hand formula, turf not counted", {"screw": f_screw, "stress": sigma}))
    return out


def check_printability() -> list[Result]:
    """Bed fit and a coarse estimate of the area that needs support."""
    out = []
    for key, (shape, filament, note) in A.printed_parts().items():
        s = A.print_oriented(key)
        mesh = to_mesh(s, 0.08, 0.3)
        zmin = mesh.bounds[0][2]
        n = mesh.face_normals
        centres = mesh.triangles_center
        down = (n[:, 2] < -math.cos(math.radians(40.0))) & (centres[:, 2] > zmin + 0.3)
        area = float(mesh.area_faces[down].sum())
        ext = mesh.extents
        fits = max(ext[0], ext[1]) <= 180.0 and ext[2] <= 180.0
        out.append(Result(f"print:{key}", fits, f"{ext[0]:.0f} x {ext[1]:.0f} x {ext[2]:.0f} mm, {filament}; overhang area needing support ~{area:.0f} mm2; {note}", {"extents": [float(e) for e in ext], "support_area": area}))
    return out


# --------------------------------------------------------------------------
def run_all(verbose: bool = True) -> list[Result]:
    sections = [
        ("Watertight printable solids", check_watertight),
        ("Static fit (closed)", check_static_fit),
        ("Clearances", check_clearances),
        ("Lid motion", check_lid_motion),
        ("Latch", check_latch),
        ("Ring lock", check_ring_lock),
        ("Assembly paths", check_assembly_paths),
        ("Grass tongue and figure", check_grass_base),
        ("Physics and function", check_physics),
        ("Printability", check_printability),
    ]
    results: list[Result] = []
    for title, fn in sections:
        t0 = time.time()
        res = fn()
        if verbose:
            print(f"\n== {title} ({time.time() - t0:.1f} s)")
            for r in res:
                print(f"  [{'PASS' if r.ok else 'FAIL'}] {r.name}: {r.detail}")
                for key in ("collisions", "blockers"):
                    for row in r.data.get(key, [])[:12]:
                        print(f"         {key[:-1]}: {row}")
        for r in res:
            r.data["section"] = title
        results += res
    return results


def write_report(results: list[Result], docs: Path) -> None:
    docs.mkdir(parents=True, exist_ok=True)

    def clean(o):
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, (np.floating, np.integer)):
            return float(o)
        return o

    (docs / "verification.json").write_text(json.dumps([{"name": r.name, "ok": bool(r.ok), "detail": r.detail, "data": clean(r.data)} for r in results], indent=1), encoding="utf-8")
    lines = [
        "# Verification report",
        "",
        "Generated by `uv run poketonieengagementhunt check` from the CAD model in `src/poketonieengagementhunt/`.",
        "It verifies geometry only: a passing report is evidence, not proof, that the printed device works.",
        "",
        f"**{sum(r.ok for r in results)} of {len(results)} checks pass.**",
        "",
    ]
    section = None
    for r in results:
        if r.data.get("section") != section:
            section = r.data.get("section")
            lines += ["", f"## {section}", "", "| Check | Result | Detail |", "| --- | --- | --- |"]
        lines.append(f"| {r.name.split(':', 1)[1]} | {'PASS' if r.ok else '**FAIL**'} | {r.detail} |")
    intended = [x for r in results for x in r.data.get("intended", [])]
    if intended:
        lines += ["", "## Intended overlaps (threads and press fits)", "", "| Pair | Overlap mm3 | Reason |", "| --- | --- | --- |"]
        for a, b, v, why in intended:
            lines.append(f"| {a} / {b} | {v:.1f} | {why} |")
    (docs / "verification.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
