"""Renders every picture of the building manual and writes docs/building_manual.md.

Everything is generated from the CAD assembly, so pictures, part numbers and
the bill of materials cannot drift apart from the model.
"""

from __future__ import annotations

import math
from pathlib import Path

import cadquery as cq

from . import assembly as A
from . import geom as g
from . import params as P
from . import parts_base as B
from . import parts_core as K
from . import parts_shell as S
from . import render as R
from .manual_text import BOM_NOTES, STEPS, manual_markdown

SIZE = (1600, 1200)


# --------------------------------------------------------------------------
# scene helpers
# --------------------------------------------------------------------------
def numbers(items: list[A.Item]) -> dict[str, int]:
    """BOM position of every item (stable: order of assembly.build())."""
    return {it.key: i + 1 for i, it in enumerate(items) if it.key != "tonie"}


def centre(item: A.Item, offset=(0.0, 0.0, 0.0)) -> tuple[float, float, float]:
    bb = item.shape().BoundingBox()
    return ((bb.xmin + bb.xmax) / 2 + offset[0], (bb.ymin + bb.ymax) / 2 + offset[1], (bb.zmin + bb.zmax) / 2 + offset[2])


def scene(items, keys=None, lift=None, ghost=(), keep=None, hide=()) -> tuple[R.Scene, dict[str, tuple[float, float, float]]]:
    """Build a render scene.  ``lift`` maps keys to displacement vectors;
    ``ghost`` keys are drawn translucent; ``keep`` clips everything (section)."""
    lift = lift or {}
    sc = R.Scene()
    anchors = {}
    for it in items:
        if (keys is not None and it.key not in keys) or it.key in hide:
            continue
        off = lift.get(it.key, (0.0, 0.0, 0.0))
        bodies = it.bodies
        if any(off):
            bodies = [(g.move(s, *off), c) for s, c in bodies]
        if keep is not None:
            bodies = R.clip(bodies, keep)
            if not bodies:
                continue
        if it.key in ghost:
            sc.add(bodies, opacity=0.16, edges=False)
        else:
            sc.add(bodies)
        anchors[it.key] = centre(it, off)
    return sc, anchors


def shot(path: Path, sc: R.Scene, cam: R.Camera, anchors=None, nums=None, size=SIZE) -> None:
    px = R.render(sc, path, cam, size=size, anchors=anchors if nums else None)
    if nums:
        R.callouts(path, px, {k: v for k, v in nums.items() if k in px})


# --------------------------------------------------------------------------
# pictures
# --------------------------------------------------------------------------
def render_overview(img: Path) -> list[Path]:
    out = []
    items = A.build()
    sc, _ = scene(items)
    p = img / "hero_closed.png"
    shot(p, sc, R.Camera(azimuth=28, elevation=14, zoom=1.0))
    out.append(p)
    p = img / "back_closed.png"
    shot(p, sc, R.Camera(azimuth=197, elevation=5, zoom=1.0))
    out.append(p)
    sc, _ = scene(A.build(with_tonie=True))
    p = img / "hero_tonie.png"
    shot(p, sc, R.Camera(azimuth=24, elevation=14, zoom=1.0))
    out.append(p)

    opened = A.build(lid_deg=P.LID_OPEN_DEG, pawl_deg=P.PAWL_RELEASE_DEG, horn_deg=P.HORN_RELEASE_DEG)
    sc, _ = scene(opened)
    p = img / "hero_open.png"
    shot(p, sc, R.Camera(azimuth=32, elevation=28, zoom=1.0))
    out.append(p)

    # longitudinal section through the centre plane, seen from the right side
    keep = g.box(-200, 200, 0.0, 200, -200, 200)
    nums = numbers(items)
    sc, anchors = scene(items, keep=keep)
    for k in ("mcu", "amp", "charger", "boost", "contacts", "inserts", "stack_screws", "servo_screws", "clamp_screws", "pawl_spring", "pawl_screw", "sleeve", "hinge_pin", "turf_screws"):
        anchors.pop(k, None)
    for k in list(anchors):
        x, y, z = anchors[k]
        anchors[k] = (x, 0.0, z)
    anchors["lid"] = (-20.0, 0, 45.0)
    anchors["bowl"] = (-25.0, 0, -42.0)
    anchors["stage"] = (20.0, 0, 27.0)
    anchors["chassis"] = (-24.0, 0, -27.5)
    anchors["band"] = (-48.0, 0, -1.5)
    anchors["cell"] = (P.CELL_AXIS[0], 0, P.CELL_AXIS[1])
    anchors["spring"] = (P.HINGE_X + 1, 0, P.HINGE_Z)
    anchors["grass_base"] = (P.X_TIP - 4.0, 0, (P.Z_SOLE + P.Z_RAIL) / 2)
    anchors["grass_top"] = (50.0, 0, P.Z_TURF - 0.5)
    anchors["reader"] = (B.BLUE_X0 + 30.0, 0, (P.Z_PCB_TOP + P.Z_PCB_BOT) / 2)
    anchors["harness"] = (22.0, 0, -38.0)
    anchors["base_screws"] = (B.base_screw_xy()[0][0], 0, P.Z_SOLE + 3.0)
    p = img / "section.png"
    shot(p, sc, R.Camera(azimuth=-90, elevation=0, zoom=1.0), anchors, nums)
    out.append(p)
    return out


def render_exploded(img: Path) -> list[Path]:
    items = A.build()
    nums = numbers(items)
    lift = {it.key: it.explode for it in items}
    sc, anchors = scene(items, lift=lift)
    p = img / "exploded.png"
    shot(p, sc, R.Camera(azimuth=32, elevation=12, zoom=1.62), anchors, nums, size=(1900, 3600))
    return [p]


def render_steps(img: Path) -> list[Path]:
    out = []
    items = A.build()
    nums = numbers(items)
    opened = A.build(lid_deg=P.LID_OPEN_DEG, pawl_deg=P.PAWL_RELEASE_DEG, horn_deg=P.HORN_RELEASE_DEG)
    unlocked = A.build(lid_deg=P.LID_OPEN_DEG, pawl_deg=P.PAWL_RELEASE_DEG, horn_deg=P.HORN_RELEASE_DEG, locked=False)
    pools = {"closed": items, "open": opened, "unlocked": unlocked}
    for st in STEPS:
        for view in st["views"]:
            pool = pools[view.get("pose", "closed")]
            keys = set(view["show"])
            new = [k for k in view.get("new", [])]
            lift = dict(view.get("lift", {}))
            sc, anchors = scene(pool, keys=keys | set(new), lift=lift, ghost=view.get("ghost", ()))
            cam = R.Camera(azimuth=view["az"], elevation=view["el"], zoom=view.get("zoom", 1.0))
            p = img / view["file"]
            labelled = view.get("label", new)
            shot(p, sc, cam, anchors, {k: nums[k] for k in labelled if k in nums})
            out.append(p)
    return out


def _zoomed(sc: R.Scene, p: Path, az: float, el: float, zoom: float, size=(1400, 1050)) -> None:
    R.render(sc, p, R.Camera(azimuth=az, elevation=el, zoom=zoom), size=size)


def render_details(img: Path) -> list[Path]:
    out = []
    # --- latch, seen from above with the deck removed ---------------------------
    for name, pose in (("latch_locked.png", dict()), ("latch_released.png", dict(pawl_deg=P.PAWL_RELEASE_DEG, horn_deg=P.HORN_RELEASE_DEG))):
        items = A.build(**pose)
        it = A.by_key(items)
        sc = R.Scene()
        region = g.box(0, 44, -24, 24, P.SERVO_BASE_Z + 14, P.Z_DECK - P.DECK_T - 0.2)
        for key in ("servo", "horn", "pawl", "pawl_spring", "pawl_screw"):
            sc.add(it[key].bodies)
        sc.add(R.clip(it["stage"].bodies, region), opacity=0.35)
        sc.add(R.clip(it["lid"].bodies, g.box(30, 40, -6, 6, 14, P.Z_DECK - P.DECK_T - 0.2)))
        sc.add(R.clip(it["chassis"].bodies, g.box(0, 44, -24, 24, P.SERVO_BASE_Z + 10, 30)), opacity=0.5)
        p = img / name
        _zoomed(sc, p, -90, 78, 1.0)
        out.append(p)
    # --- emergency opening: section along the paper-clip path -----------------
    items = A.build()
    it = A.by_key(items)
    y0 = P.EMERGENCY_YZ[0]
    keep = g.box(18, 60, y0, 60, 4, 40)
    sc = R.Scene()
    for key in ("bezel", "lens", "cone", "led", "chassis", "stage", "lid", "pawl", "speaker", "spk_clamp", "band"):
        sc.add(R.clip(it[key].bodies, keep))
    start, direction = S.emergency_axis()
    clip_wire = cq.Solid.makeCylinder(0.55, 34.0, start - direction * 12.0, direction)
    sc.add([(clip_wire, "highlight")])
    p = img / "emergency.png"
    _zoomed(sc, p, -90, 0, 1.0)
    out.append(p)
    # --- ring lock, locked and released --------------------------------------
    for name, locked in (("ring_locked.png", True), ("ring_released.png", False)):
        items = A.build(lid_deg=P.LID_OPEN_DEG, pawl_deg=P.PAWL_RELEASE_DEG, locked=locked)
        it = A.by_key(items)
        keep = g.box(-34, 12, 0.0, 30, 12, 60)
        sc = R.Scene()
        for key in ("stage", "cradle", "ring", "lock_pin", "slider"):
            sc.add(R.clip(it[key].bodies, keep))
        p = img / name
        _zoomed(sc, p, -90, 12, 1.0)
        out.append(p)
    # --- hinge, closed and open ---------------------------------------------------
    for name, deg in (("hinge_closed.png", 0.0), ("hinge_open.png", P.LID_OPEN_DEG)):
        items = A.build(lid_deg=deg, pawl_deg=P.PAWL_RELEASE_DEG if deg else 0.0)
        it = A.by_key(items)
        keep = g.box(-75, -22, 0.0, 30, -12, 34)
        sc = R.Scene()
        for key in ("stage", "lid", "band", "bowl", "chassis", "hinge_pin", "sleeve", "spring", "charger", "boost"):
            sc.add(R.clip(it[key].bodies, keep))
        p = img / name
        _zoomed(sc, p, -90, 0, 1.0)
        out.append(p)
    # --- a Tonie on the grass ---------------------------------------------------
    items = A.build(with_tonie=True)
    sc, _ = scene(items)
    p = img / "grass.png"
    R.render(sc, p, R.Camera(azimuth=-30, elevation=24, zoom=1.0), size=(1400, 1050))
    out.append(p)
    keep = g.box(-60, 140, 0.0, 200, -60, 8.0)
    sc = R.Scene()
    for item in items:
        if item.key in ("lid", "stage", "cradle", "ring", "slider", "lock_pin", "pawl", "pawl_screw", "pawl_spring", "stack_screws", "spring", "sleeve", "hinge_pin"):
            continue
        sc.add(R.clip(item.bodies, keep))
    p = img / "grass_section.png"
    _zoomed(sc, p, -90, 0, 1.0)
    out.append(p)
    return out


def render_print_plate(img: Path) -> list[Path]:
    """All printed parts in print orientation, laid out on a virtual bed."""
    colours = {"bowl": "white", "band": "black", "lid": "red", "bezel": "black", "lens": "clear", "cone": "white", "stage": "stage", "chassis": "chassis", "pawl": "pawl", "cradle": "cradle", "slider": "slider", "sleeve": "sleeve", "spk_clamp": "clamp", "grass_base": "grass", "grass_top": "grass"}
    layout = {
        "bowl": (-110, 60), "lid": (0, 60), "stage": (110, 60), "chassis": (-110, -55), "band": (0, -55), "cradle": (95, -30),
        "spk_clamp": (95, -75), "bezel": (150, -35), "lens": (150, -75), "cone": (150, -105), "pawl": (95, -110), "slider": (120, -110), "sleeve": (60, -110),
        "grass_base": (-85, -185), "grass_top": (90, -185),
    }
    sc = R.Scene()
    bed = g.box(-175, 180, -240, 120, -1.0, -0.2)
    sc.add([(bed, "ghost")], opacity=0.5, edges=True)
    for key, (x, y) in layout.items():
        sc.add([(g.move(A.print_oriented(key), x, y, 0), colours[key])])
    p = img / "print_orientation.png"
    R.render(sc, p, R.Camera(azimuth=-60, elevation=38, zoom=1.0), size=(1800, 1400))
    return [p]


# --------------------------------------------------------------------------
def build_manual(root: Path) -> list[Path]:
    docs = root / "docs"
    img = docs / "img"
    img.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    files += render_overview(img)
    files += render_exploded(img)
    files += render_steps(img)
    files += render_details(img)
    files += render_print_plate(img)
    items = A.build()
    nums = numbers(items)
    md = manual_markdown(items, nums, A.printed_parts())
    p = docs / "building_manual.md"
    p.write_text(md, encoding="utf-8")
    files.append(p)
    return files
