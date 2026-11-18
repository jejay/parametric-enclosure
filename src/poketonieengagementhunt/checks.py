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
    frozenset(("turf_screws", "grass_top")): (3.0, "M2 thread formed in a Ø1.95 pilot"),
    frozenset(("servo_screws", "chassis")): (25.0, "servo screws in Ø1.6 pilot"),
    frozenset(("clamp_screws", "chassis")): (12.0, "M2 thread formed in a Ø1.70 pilot"),
    frozenset(("pawl_screw", "stage")): (3.0, "M2 thread formed in a Ø1.95 pilot"),
    frozenset(("hinge_pin", "stage")): (2.0, "Ø2 pins pressed into Ø1.95 bores"),
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
    shapes = {it.key: g.compound([b for b, _ in it.check_bodies()]) if len(it.check_bodies()) > 1 else it.check_bodies()[0][0] for it in todo}
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
            for sa, _ in a.check_bodies():
                for sb, _ in b.check_bodies():
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
    "spring": 0.4, "hinge_pin": 0.4, "lock_pin": 1.4, "stack_screws": 4.4, "inserts": 2.1,
    "harness": 6.0, "turf_screws": 1.6, "base_screws": 2.0,
}
BASE_KEYS = ("grass_base", "grass_top", "reader", "hall", "harness", "turf_screws", "base_screws")
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
    bowl, tray = it["bowl"].shape(), it["grass_base"].shape()
    turf = B.turf_plate()            # the plate of the grass top; its tufts are measured one by one below
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
    out.append(Result("base:tongue is flush with the ball's flat and stays in front of it", flush and bb.xmin >= -0.05 and bb.ymax < P.R, f"the underside of the tongue and the flat of the ball both lie on the table plane (gaps {gap_t:.3f} and {gap_b:.3f} mm) and nothing reaches below it ({below:.2f} mm3, screw heads included); the tongue begins {P.X_REAR:.0f} mm in front of the ball's axis, under its belly, is {2 * P.TONGUE_W:.0f} mm wide there and {2 * B.half_width(P.SPOT_X):.0f} mm beside a figure, {P.BASE_T:.0f} mm high, and reaches {P.X_TIP - P.R:.1f} mm beyond the ball: nothing of it lies beside or behind the ball", {"x_rear": P.X_REAR, "reach": P.X_TIP - P.R, "width": 2 * P.TONGUE_W, "width_figure": 2 * B.half_width(P.SPOT_X), "below": below}))

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

    # 4. reader pocket, grass top and its frame.  The plate goes in along the slope of the frame
    #    walls: forwards and down.  Lifted straight up it has to collide with the rim at the tip.
    reader, hall = it["reader"].shape(), it["hall"].shape()
    slope = P.TURF_HOOK / P.TURF_T
    bad = []
    for dz in (0.5, 2.0, 5.0, 12.0):
        for key in ("reader", "hall"):
            vv = g.common_volume(g.move(it[key].shape(), dz=dz), tray)
            if vv > TOL_VOLUME:
                bad.append((dz, key, vv))
        out_of_bed = g.move(turf, dx=-slope * dz, dz=dz)
        for fixed in ("grass_base", "reader", "hall"):
            vv = g.common_volume(out_of_bed, it[fixed].shape())
            if vv > TOL_VOLUME:
                bad.append((dz, "grass_top", fixed, vv))
    d_seat, d_roof = g.min_distance(reader, tray), g.min_distance(reader, turf)
    hold = P.BLUE_LEDGE_ANT - 2 * max(P.BLUE_CL_X, P.BLUE_CL_Y)      # ledge left under a board pushed to one side
    out.append(Result("base:reader drops into its pocket, grass top closes it", not bad and d_seat < 0.02 and 0.0 <= d_roof <= 0.3 and hold >= 1.0, f"board on its ledge ({d_seat:.2f} mm), {d_roof:.2f} mm under the turf; pushed to one side of its {2 * P.BLUE_CL_X + P.BLUE_L:.1f} x {2 * P.BLUE_CL_Y + P.BLUE_W:.1f} mm pocket, the antenna half still rests on {hold:.1f} mm of ledge; reader and hall switch lifted 0.5..12 mm and the grass top drawn out of its frame along the slope of the frame walls: {len(bad)} collisions", {"collisions": bad}))
    caught = g.common_volume(g.move(turf, dz=0.4), tray)
    in_frame = g.common_volume(turf, tray)
    d_bed = g.min_distance(turf, tray)
    z_plate, z_rim = turf.BoundingBox().zmax, tray.BoundingBox().zmax
    wall = min(B.edge_distance(B.POCKET[1], B.POCKET[2]), P.X_TIP - B.POCKET[1])     # round a front corner of the reader pocket, and in front of it
    out.append(Result("base:the rim of the tray holds the tip of the grass top", caught > 1.0 and in_frame < TOL_VOLUME and d_bed < 0.02 and abs(z_plate - z_rim) < 0.05 and wall >= 3.0, f"the grass top lies in a frame, {P.RIM_GAP} mm clear all round, level with the rim (step {z_plate - z_rim:+.2f} mm); the frame walls lean forwards by {P.TURF_HOOK} mm over the {P.TURF_T} mm of the plate, so the rim at the tip overhangs it: lifted straight up by 0.4 mm the plate runs into the rim ({caught:.1f} mm3). Four screws hold its rear half, and with the ball in place it cannot slide back out. In front of the reader pocket and round its front corners at least {wall:.1f} mm of wall remain", {"caught": caught, "wall": wall}))
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
    proud = sum(g.common_volume(above, x) for x in grass) + g.common_volume(above, turf) + g.common_volume(above, tray)
    x_front = max(max(x for x, _, _ in B._samples(b, (0.0, 0.5, 1.0))) for b in B.blades())
    r_foot = P.TONIE_BASE_D / 2
    front = P.X_TIP - (P.SPOT_X + r_foot)                                    # from the foot of a centred figure to the front edge
    seam = front - B.PLATE_INSET - P.TURF_HOOK                               # ... and to the joint between grass top and rim (negative: the foot stands on the rim too)
    under = g.cyl_z(r_foot, P.Z_TURF - 0.3, P.Z_TURF, P.SPOT_X, 0.0)
    carried = (g.common_volume(under, turf) + g.common_volume(under, tray)) / g.volume(under)
    side = B.half_width(P.SPOT_X) - r_foot
    out.append(Result("figure:stands free on a plain flat spot", proud < TOL_VOLUME and d_blade >= P.GRASS_GAP and x_front <= P.SPOT_X - r_foot + 12.0 and carried > 0.99 and front >= 1.0, f"where a figure stands nothing rises above the surface ({proud:.2f} mm3 within {r_plain:.1f} mm of its place) and nothing is recessed: no rim to stand in, no pocket, no lock, and no mark. The foot of a centred Ø{P.TONIE_BASE_D:.0f} mm figure is carried on {100 * carried:.1f} % of its area; the rest is the {P.RIM_GAP} mm joint between grass top and rim, which crosses under its front edge, and the two are level. The foot ends {front:.1f} mm short of the front edge of the tongue and leaves {side:.1f} mm of ground on each side: the front end is the cue for putting a figure down. The nearest grass is {d_blade:.1f} mm from that foot and all grass stands behind x = {x_front:.0f} mm, {P.SPOT_X - x_front:.0f} mm behind the centre of the figure: its sides and its front are open", {"blade": d_blade, "x_front": x_front, "seam": seam, "front": front, "side": side, "carried": carried}))
    # the lawn must not be mirrored: compare the tuft positions with their mirror image
    lawn = B.tufts()
    pos = [(t.mound.x, t.mound.y) for t in lawn]
    twin = [min(math.hypot(x - u, -y - w) for j, (u, w) in enumerate(pos) if j != i) for i, (x, y) in enumerate(pos)]   # 0 for every tuft of a mirrored lawn
    sizes = [len(t.blades) for t in lawn]
    heights = [b.h for b in B.blades()]
    left = sum(1 for _, y in pos if y > 0)
    spread = len({int(((t.mound.out_deg - 90.0) % 180.0) // 30.0) for t in lawn})   # how many of six directions occur
    out.append(Result("grass:tufts are scattered, not mirrored", min(twin) >= 3.0 and max(sizes) >= min(sizes) + 2 and max(heights) >= 2.0 * min(heights) and spread >= 4, f"{len(pos)} tufts with {min(sizes)} to {max(sizes)} blades each, blades {min(heights):.0f} to {max(heights):.0f} mm high, tufts turned in {spread} of 6 direction classes; no tuft has a twin on the other side: the nearest mirror image of another tuft is {min(twin):.1f} mm away at least and {sum(twin) / len(twin):.1f} mm on average. Places, sizes, directions and leaf shapes come from a random generator with a fixed seed (LAWN_SEED)", {"tufts": len(pos), "twin_min": min(twin), "sizes": sizes}))
    # the lawn is thin and gathered in the two corners between the ball and the sides of the tongue
    cx, cy = P.LAWN_CORNER
    roots = [(b.x, b.y) for b in B.blades()]
    in_corner = sum(1 for x, y in roots if math.hypot(x - cx, abs(y) - cy) <= 2.0 * P.LAWN_SPREAD) / len(roots)
    middle = sum(1 for x, y in roots if abs(y) < P.LAWN_CENTRE_FREE)
    y_min = min(abs(y) for _, y in pos)
    out.append(Result("grass:thin, and gathered in the two corners beside the ball", in_corner >= 0.75 and middle == 0 and min(left, len(pos) - left) >= 3 and len(pos) <= 16, f"{len(pos)} tufts in all, {left} in the left corner and {len(pos) - left} in the right; {100 * in_corner:.0f} % of the {len(roots)} blades are rooted within {2 * P.LAWN_SPREAD:.0f} mm of the two corner points (x = {cx:.0f}, y = ±{cy:.0f} mm), none within {P.LAWN_CENTRE_FREE:.0f} mm of the centre line in front of the ball (the nearest tuft is rooted {y_min:.0f} mm from it), and none beside or in front of the figure", {"in_corner": in_corner, "left": left, "right": len(pos) - left}))

    # every turf screw ends in the root of a tuft, with solid plastic round and above its pilot hole
    z_hole = P.Z_RAIL + P.TURF_PILOT_DEPTH
    z_tip = P.Z_SOLE + P.TURF_SCREW_CB + P.TURF_SCREW_L
    wall, solid, on_hub = 0.8, [], True
    for (x, y), tuft in zip(B.turf_screw_xy(), lawn):
        hub = tuft.blades[0]
        on_hub = on_hub and hub.hub and math.hypot(hub.x - x, hub.y - y) < 1e-6
        root = g.union(B.mound_solid(tuft.mound), *[B.blade_solid(b) for b in tuft.blades])
        sleeve = g.cyl_z(P.M2_PILOT_FLAT / 2 + wall, P.Z_TURF, z_hole, x, y)
        cap = g.cyl_z(P.M2_PILOT_FLAT / 2, z_hole, z_hole + 1.0, x, y)
        solid.append(min(g.common_volume(sleeve, root) / g.volume(sleeve), g.common_volume(cap, root) / g.volume(cap)))
    out.append(Result("grass:turf screws end inside tuft roots", on_hub and min(solid) > 0.995 and z_tip <= z_hole - 0.25 and z_tip >= P.Z_TURF + 1.0, f"each of the {len(solid)} turf screws stands under the main blade of a tuft and ends {z_tip - P.Z_TURF:.1f} mm above the turf surface inside its root; the pilot hole reaches {z_hole - P.Z_TURF:.1f} mm above the surface and has {wall} mm of solid plastic all round and 1 mm above it ({100 * min(solid):.0f} % of the probed volume at the worst screw): nothing shows on top. The check runs for whatever lawn the seed gives", {"solid": solid}))

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
    x_tip = P.X_TIP
    f_screw = force * x_tip / (2 * max(x for x, _ in screws))
    # bending of the tray where the reader pocket begins: two rails beside the pocket and the floor under it
    wr, hr = B.half_width(B.POCKET[0]) - B.POCKET[2], P.Z_RAIL - P.Z_SOLE
    wf, hf = 2 * B.POCKET[2], P.TRAY_FLOOR
    area = 2 * wr * hr + wf * hf
    zc = (2 * wr * hr * hr / 2 + wf * hf * hf / 2) / area
    inertia = 2 * (wr * hr**3 / 12 + wr * hr * (hr / 2 - zc) ** 2) + wf * hf**3 / 12 + wf * hf * (hf / 2 - zc) ** 2
    sigma = force * (x_tip - B.POCKET[0]) * max(zc, hr - zc) / inertia
    out.append(Result("base:load estimate for a push on the tongue", f_screw < 150.0 and sigma < 10.0, f"{force:.0f} N on the tip with the ball held: at most {f_screw:.0f} N of tension in each front screw (an M3 insert in PETG holds several hundred), about {sigma:.1f} MPa bending stress in the tray where the pocket begins (PETG yields near 45 MPa; revision 2 had 13 MPa); estimate by hand formula, rim and grass top not counted", {"screw": f_screw, "stress": sigma}))
    return out


def _upright_in_print(key: str, axis: str) -> bool:
    """Does a hole along ``axis`` (assembly coordinates) stand upright when the part is printed?"""
    rot = A.PRINT_ORIENT[key]
    v = {"x": cq.Vector(1, 0, 0), "y": cq.Vector(0, 1, 0), "z": cq.Vector(0, 0, 1)}[axis]
    if rot:
        v = cq.Edge.makeLine(cq.Vector(0, 0, 0), v).rotate(cq.Vector(0, 0, 0), {"x": cq.Vector(1, 0, 0), "y": cq.Vector(0, 1, 0), "z": cq.Vector(0, 0, 1)}[rot[0]], rot[1]).endPoint()
    return abs(v.z) > 0.99


def check_fasteners() -> list[Result]:
    """The M2 machine screws that form their own thread in printed pilot holes."""
    out = []
    lug = P.SPK_RIM_T + 2.0                                   # the clamp screw passes through this much of the clamp ring
    cap = P.PAWL_CAP_T + P.PAWL_CAP_HUB_T                     # ... and the pivot screw through the printed washer
    boss = (P.Z_DECK - P.DECK_T) - (P.PAWL_Z0 - 0.3)          # length of the pivot boss
    # joint -> (screw length, length that is not thread in the print, depth of the pilot hole or None for a through hole,
    #           part with the pilot hole, axis of that hole in the assembly, pilot diameter used there)
    joints = {
        "grass top": (P.TURF_SCREW_L, P.TURF_SEAT, P.TURF_PILOT_DEPTH, "grass_top", "z", P.M2_PILOT_FLAT),
        "speaker clamp": (P.CLAMP_SCREW_L, lug, None, "chassis", "x", P.M2_PILOT_SIDE),
        "pawl pivot": (P.PAWL_SCREW_L, cap, boss + 1.2, "stage", "z", P.M2_PILOT_FLAT),
    }
    ok, rows = True, []
    for name, (length, free, depth, key, axis, pilot) in joints.items():
        thread = length - free
        engaged = thread - P.M2_LEAD
        fits = depth is None or depth >= thread + 0.2          # a machine screw has a blunt end: the hole must be deeper
        upright = _upright_in_print(key, axis)
        right_pilot = abs(pilot - (P.M2_PILOT_FLAT if upright else P.M2_PILOT_SIDE)) < 1e-9
        ok = ok and engaged >= P.M2_ENGAGE - 1e-9 and fits and right_pilot
        rows.append(f"{name}: M2 x {length:.0f}, {engaged:.1f} mm of thread beyond the lead-in, pilot Ø{pilot} ({'mouth parallel to the bed' if upright else 'mouth in an upright wall'})" + ("" if depth is None else f", hole {depth - thread:.1f} mm deeper than the screw"))
    through = (P.BAFFLE_X1 - P.SPK_X_FRONT) - (P.CLAMP_SCREW_L - lug)
    skin = P.DECK_T - 1.2
    out.append(Result("screws:M2 screws form enough thread in the print", ok and through >= 0.2 and skin >= 1.0, "; ".join(rows) + f". Needed: {P.M2_ENGAGE} mm (research/06 section 4.2). The clamp screws end {through:.1f} mm inside the front face of the baffle; above the pivot screw's hole {skin:.1f} mm of the ring deck stay closed. Head room everywhere: Ø{P.M2_HEAD_D} x {P.M2_HEAD_H} mm, which takes a cap head (ISO 4762) or a pan head (ISO 7045)", {"rows": rows}))
    lip = (P.PAWL_CAP_D - P.PAWL_BORE) / 2 - (P.M2_CLEAR - 2.0) / 2
    standard = (5.0 - P.PAWL_BORE) / 2
    it = A.by_key(A.build())
    d_pawl = g.min_distance(it["pawl_cap"].shape(), it["pawl"].shape())
    d_horn = min(g.min_distance(A.by_key(A.build(horn_deg=h))["pawl_cap"].shape(), A.by_key(A.build(horn_deg=h))["horn"].shape()) for h in (P.HORN_REST_DEG, P.HORN_RELEASE_DEG))
    out.append(Result("screws:printed washer keeps the pawl on its pivot", lip >= 0.5 and 0.1 <= d_pawl <= 0.6 and d_horn >= 0.3, f"the flange of the printed pivot washer (Ø{P.PAWL_CAP_D}) overlaps the pawl's bore (Ø{P.PAWL_BORE}) by {lip:.2f} mm all round, however the washer sits on its screw; a standard M2 washer (Ø5.0, ISO 7089) would be {-standard:.2f} mm smaller than the bore. The pawl keeps {d_pawl:.2f} mm of play above the washer, and the servo arm passes {d_horn:.2f} mm from it at rest and at release", {"lip": lip, "pawl": d_pawl, "horn": d_horn}))
    # the two speaker clamp screws lie deep in the core: only a hex key reaches them
    key_long, key_short = 45.0, 15.0                         # arms of an ordinary 1.5 mm hex key
    x_head = P.SPK_X_FRONT - lug - P.M2_HEAD_H
    core = [i for i in A.build() if 4 <= i.step <= 6 and i.key != "clamp_screws"]
    blocked, sweeps, straight, tilted = [], [], set(), set()
    for sgn in (1, -1):
        y = sgn * 22.6
        shaft = g.cyl_x(1.0, x_head - key_long, x_head - 0.05, y, P.SPK_Z)
        blocked += [i.key for i in core if g.common_volume(shaft, i.shape()) > TOL_VOLUME]
        free = set()
        for ang in range(0, 360, 10):
            arm = g.move(g.rot(g.box(-0.9, 0.9, 0.0, key_short, -0.9, 0.9), "x", ang, (0, 0, 0)), dx=x_head - key_long + 1.5, dy=y, dz=P.SPK_Z)
            if all(g.common_volume(arm, i.shape()) <= TOL_VOLUME for i in core):
                free.add(ang)
        run = max((next(n for n in range(37) if (a + 10 * n) % 360 not in free) for a in free), default=0) * 10 if len(free) < 36 else 360
        sweeps.append(run)
        # a screwdriver in line with the screw, and one held 20 degrees off its axis (possible only with a ball end)
        inline = g.cyl_x(1.5, x_head - 90.0, x_head - 0.3, y, P.SPK_Z)
        straight |= {i.key for i in core if g.common_volume(inline, i.shape()) > TOL_VOLUME}
        t = math.radians(20.0)
        d = cq.Vector(-math.cos(t), 0.0, math.sin(t))
        o = cq.Vector(x_head - 0.3, y, P.SPK_Z)
        tool = cq.Solid.makeCylinder(1.5, 90.0, o, d).fuse(cq.Solid.makeCylinder(8.0, 60.0, o + d * 60.0, d))
        tilted |= {i.key for i in core if g.common_volume(tool, i.shape()) > TOL_VOLUME}
    out.append(Result("screws:a hex key reaches the speaker clamp screws", not blocked and min(sweeps) >= 90 and not tilted, f"with the core on the bench (steps 4 to 6) the long arm of a 1.5 mm hex key ({key_long:.0f} mm) lies free behind each of the two screws: blocked by {blocked or 'nothing'}; its short arm can swing through {min(sweeps)}° (60° are enough to take a new grip). A screwdriver in line with the screw meets {', '.join(sorted(straight)) or 'nothing'}; held 20° upwards, as a ball-end hex driver allows, it meets {', '.join(sorted(tilted)) or 'nothing'}. A cross-head screw cannot be driven here: these two screws need a hex socket", {"sweeps": sweeps, "blocked": blocked}))
    return out


def check_pins() -> list[Result]:
    """The two hinge pins and the pin of the ring lock: do they hold, and can they be put in?"""
    out = []
    hx, hz = P.HINGE_X, P.HINGE_Z
    y_in, y_out = K.hinge_pin_span()
    w_in, w_out = K.hinge_pin_span(parked=True)
    rib0, rib1 = P.SPRING_SLOT / 2, P.SPRING_SLOT / 2 + P.LID_RIB_T
    half = P.SPRING_SLOT / 2 - 0.15
    in_tower = min(y_out, K.TOWER_Y1) - K.TOWER_Y0
    in_rib = min(y_out, rib1) - max(y_in, rib0)
    in_sleeve = half - y_in
    out.append(Result("pins:two hinge pins carry lid and spring", in_tower >= 2.5 and in_rib >= P.LID_RIB_T - 1e-9 and in_sleeve >= 1.0 and y_out <= K.TOWER_Y1, f"each Ø{P.HINGE_PIN_D:.0f} x {P.HINGE_PIN_L:.0f} pin is pressed into {in_tower:.1f} mm of its hinge tower (bore Ø{P.HINGE_PRESS}), carries one rib of the lid over its full {in_rib:.1f} mm (bore Ø{P.HINGE_BORE}) and reaches {in_sleeve:.2f} mm into the spring sleeve; its outer end lies {K.TOWER_Y1 - y_out:.1f} mm inside the outer face of the tower", {"tower": in_tower, "rib": in_rib, "sleeve": in_sleeve}))

    # one long pin cannot be mounted: the lid's own wall closes the hinge axis
    lid = S.lid()
    axis = g.inter(g.cyl_y(0.05, 0.0, 60.0, hx, hz), lid)
    wall_y = min(sol.BoundingBox().ymin for sol in axis.Solids() if sol.BoundingBox().ymin > rib1 + 0.5)
    room = math.sqrt((P.R - P.T_LID) ** 2 - (math.hypot(hx, hz) + P.HINGE_PIN_D / 2) ** 2) - K.TOWER_Y1
    out.append(Result("pins:why the hinge has two pins", wall_y < K.TOWER_Y1 + 2 * P.HINGE_PIN_L and w_out - K.TOWER_Y1 < wall_y - K.TOWER_Y1, f"the hinge axis lies inside the lid and meets its wall {wall_y:.1f} mm from the middle; beside a hinge tower a Ø{P.HINGE_PIN_D:.0f} pin has {room:.1f} mm of room before it touches the wall. A pin that goes through both ribs cannot be put in, at any length. A waiting pin stands {w_out - K.TOWER_Y1:.1f} mm out of its tower", {"wall_y": wall_y, "room": room}))

    # the pins wait in the towers while the lid is put on
    asm = P.HINGE_MOUNT_DEG                                   # the lid is held about this far open
    parked = A.by_key(A.build(lid_deg=asm, hinge_parked=True))
    lid_a, pins, stage = parked["lid"].shape(), parked["hinge_pin"].shape(), parked["stage"].shape()
    gap = g.min_distance(pins, lid_a)
    shell = g.inter(g.ball_zone(P.R, P.R - P.HINGE_RECESS_WALL + 0.02, P.HB, hz + 6.0), g.box(-70, -30, 11.6, P.HINGE_RECESS_Y + 2.0, 0, 30))
    kept = g.common_volume(shell, lid) / g.volume(shell)
    out.append(Result("pins:waiting pins clear the lid", gap >= 0.15 and kept > 0.999 and P.HINGE_RECESS_WALL >= 1.2, f"with the pins waiting in the towers (flush with the towers' inner faces) the lid keeps {gap:.2f} mm from them; the relief inside the lid wall that makes this room leaves {P.HINGE_RECESS_WALL} mm of wall (measured: {kept * 100:.1f} % of that shell is solid), so nothing shows outside. The wall behind the knuckles is {P.LID_WALL_AT_HINGE} mm as before", {"gap": gap, "kept": kept}))
    bad = []
    steps = (0.6, 1.2, 2.0, 3.0, 4.5, 6.5, 9.0, 12.0, 16.0)
    for ang in (180.0, 190.0, 200.0):
        ux, uz = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        for d in steps:
            moved = g.move(lid_a, dx=d * ux, dz=d * uz)
            v_s, v_p = g.common_volume(moved, stage), g.common_volume(moved, pins)
            if v_s > TOL_VOLUME or v_p > TOL_VOLUME:
                bad.append((ang, d, round(v_s, 2), round(v_p, 2)))
    out.append(Result("pins:lid slides onto the hinge from behind", not bad, f"lid held {asm:.0f}° open and brought forwards from {steps[-1]:.0f} mm behind its seat, level and up to 20° from below: {len(bad)} collisions with the stage or the waiting pins", {"collisions": bad}))
    # long-nose pliers press both pins in at once: one jaw on each pin end
    jaw_t, jaw_w = 1.5, 2.5
    reach = {}
    for deg in (asm, 90.0):
        lid_j = A.by_key(A.build(lid_deg=deg, hinge_parked=True))["lid"].shape()
        free = []
        for ang in range(0, 360, 15):
            ok = True
            for sgn in (1, -1):
                ya, yb = sorted((sgn * (K.TOWER_Y1 + 0.05), sgn * (w_out + jaw_t)))
                bar = g.move(g.rot(g.box(-0.6, 40.0, ya, yb, -jaw_w / 2, jaw_w / 2), "y", -ang, (0, 0, 0)), dx=hx, dz=hz)
                if g.common_volume(bar, lid_j) > TOL_VOLUME or g.common_volume(bar, stage) > TOL_VOLUME:
                    ok = False
                    break
            if ok:
                free.append(ang)
        reach[deg] = free
    above = {deg: [a for a in fr if 45 <= a <= 135] for deg, fr in reach.items()}
    out.append(Result("pins:pliers reach the waiting pins", all(above.values()) and len(above[90.0]) >= 2, "two jaws of " + f"{jaw_w} x {jaw_t} mm reach the ends of both waiting pins and can follow them to the towers, coming from above: " + "; ".join(f"lid {deg:.0f}° open from {', '.join(str(a) for a in fr)}°" for deg, fr in above.items()) + " (directions round the hinge, 90° is straight from above, tried in steps of 15°). The jaws stop on the faces of the towers, which sets the depth", {"directions": {str(k): v for k, v in reach.items()}}))

    # ring lock
    stem = P.LOCK_STEM_X[1] - max(P.LOCK_STEM_X[0], P.LOCK_TIP_X - P.LOCK_PIN_L)
    behind = P.LOCK_STEM_X[0] - (P.LOCK_TIP_X - P.LOCK_PIN_L)
    guide_x = P.LOCK_STEM_X[0] - P.LOCK_TRAVEL - 1.5
    proud = guide_x - (P.LOCK_TIP_X - P.LOCK_TRAVEL - P.LOCK_PIN_L)
    it = A.by_key(A.build())
    path = g.cyl_x(P.LOCK_PIN_D / 2, -80.0, P.LOCK_TIP_X, 0, P.LOCK_Z)
    v_stage, v_cradle = g.common_volume(path, it["stage"].shape()), g.common_volume(path, it["cradle"].shape())
    out.append(Result("pins:lock pin goes in from behind", stem >= 5.0 - 1e-9 and 0.0 <= behind <= 3.0 and v_stage <= TOL_VOLUME and v_cradle <= TOL_VOLUME and 0.0 <= proud <= 2.0, f"lock pin Ø{P.LOCK_PIN_D:.0f} x {P.LOCK_PIN_L:.0f}: {stem:.1f} mm in the stem of the slider, {behind:.1f} mm standing out behind it; its straight path from behind the stage to the locked position is free (stage {v_stage:.2f}, cradle {v_cradle:.2f} mm3). With the slider drawn back it stands {proud:.1f} mm out of the back of its guide", {"stem": stem, "path": v_stage + v_cradle}))
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
        ("Small screws", check_fasteners),
        ("Pins", check_pins),
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
