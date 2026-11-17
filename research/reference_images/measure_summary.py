"""Combine the measurements into one table, remove camera perspective where it could be fitted, and print statistics.

    uv run python -I research/reference_images/measure_summary.py

Inputs: measurements_front.json (measure_front_views.py), measurements_side.json (measure_side_views.py).
Output: Markdown on stdout + measurements_summary.json.

Perspective removal (photos / renders whose camera distance d could be fitted from the band profile):
    true = apparent * (d - z) / sqrt(d^2 - 1)          (lengths in ball radii)
    z    = height of the feature above the ball centre, times cos(angle between button axis and view axis)
           ring and white disc: plane of the ring's outer edge, sqrt(1 - rho_ring^2)   (flat ring face, see S01)
           button face:         that plane + 0.046 R  (button stands ~2.3 % of D above the collar on the replica)
    band: the fitted true band height is used directly.
"""
from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
front = {r["name"][:3]: r for r in json.loads((HERE / "measurements_front.json").read_text(encoding="utf-8"))}
side = json.loads((HERE / "measurements_side.json").read_text(encoding="utf-8"))


def demag(app, d, z):
    return app * (d - z) / math.sqrt(d * d - 1.0)


def corrected(key, d, button_lift=0.046):
    """Perspective-corrected ring / disc / button for front image `key` with camera distance d (in R)."""
    m = front[key]
    cosg = math.cos(math.radians(m["yaw_deg"])) * math.cos(math.radians(m["tilt_deg"]))
    rho = m["ring_od_over_D"]
    for _ in range(4):
        h = math.sqrt(1.0 - rho * rho)
        ring = demag(m["ring_od_over_D"], d, h * cosg)
        rho = ring
    out = dict(ring=ring, disc=None, button=None)
    if m.get("disc_over_D"):
        out["disc"] = demag(m["disc_over_D"], d, h * cosg)
    if m.get("button_over_D"):
        out["button"] = demag(m["button_over_D"], d, (h + button_lift) * cosg)
    return out


rows = []   # (id, label, group, band, ring, disc, button, grade, note)


def add(i, label, group, band, ring, disc, button, grade, note):
    rows.append(dict(id=i, label=label, group=group, band=band, ring=ring, disc=disc, button=button, grade=grade, note=note))


def app(key):
    m = front[key]
    return m["band_over_D"], m["ring_od_over_D"], m.get("disc_over_D"), m.get("button_over_D")


# --- official 2D art (drawn, no camera) -----------------------------------------------------------
b, r, d_, t = app("F01")
disc_free = front["F01"]["disc_free_fit_over_D"]
add("F01", "Sugimori official artwork", "official 2D art", b, r, round((d_ + disc_free) / 2, 4), t, "A",
    "hand-drawn 3/4 view; outlines removed; disc = mean of sphere-model fit (%.3f) and free ellipse (%.3f)" % (d_, disc_free))
b, r, d_, t = app("F08")
add("F08", "Vector art, official clip-art style", "official-style 2D art", b, r, d_, t, "A",
    "flat vector with CMYK-style swatches; provenance not verified; outline centre lines")
b, r, d_, t = app("F11")
add("F11", "TV anime EP001 frame", "official 2D art", b, r, d_, t, "B", "160 px, blurry; +/-1 px = 6-8 % on small features")

# --- official physical replica, perspective removed ------------------------------------------------
tw = []
for key in ("F04", "F05"):
    cam = side[key]["camera"]
    c = corrected(key, cam["d"])
    tw.append(dict(src=key, d=cam["d"], band=cam["band_true_over_D"], **c))
s01 = side["S01"]
d1 = s01["camera"]["d"]
cosg = s01["collar_axis_ratio"]
rho = s01["ring_major_over_D"]
for _ in range(4):
    h = math.sqrt(1 - rho * rho)
    rho = demag(s01["ring_major_over_D"], d1, h * cosg)
tw.append(dict(src="S01", d=d1, band=s01["camera"]["band_true_over_D"], ring=rho,
               disc=demag(s01["collar_major_over_D"], d1, h * cosg), button=None))
for x in tw:
    add(x["src"] + "c", f"TWC die-cast replica, {x['src']} (camera at {x['d']:.1f} R removed)", "official replica",
        x["band"], round(x["ring"], 4), round(x["disc"], 4), None if x["button"] is None else round(x["button"], 4), "-",
        "component of the TWC mean")
mean = lambda k: round(statistics.mean(x[k] for x in tw if x[k] is not None), 4)
add("TWC", "The Wand Company die-cast replica 75 mm (mean of F04, F05, S01)", "official replica",
    mean("band"), mean("ring"), mean("disc"), mean("button"), "A", "perspective removed; three independent photos")
cam = side["F06"]["camera"]
c = corrected("F06", cam["d"])
add("F06", f"The Wand Company MINI replica 40 mm (render, camera at {cam['d']:.1f} R removed)", "official replica",
    cam["band_true_over_D"], round(c["ring"], 4), round(c["disc"], 4), round(c["button"], 4), "A",
    "single CG render with strong perspective; correction is -15 % on the ring")

# --- official 3D renders, perspective unknown -> apparent values ------------------------------------
for key, label, note in (
        ("F02", "Pokemon GO item sprite", "186 px; apparent (perspective unknown, not removed)"),
        ("F03", "Let's Go in-game model (screenshot)", "212 px JPEG; button glowing; apparent"),
        ("F12", "Smash Bros. Wii U trophy render", "236 px; low-poly; apparent")):
    b, r, d_, t = app(key)
    add(key, label, "official 3D render (apparent)", b, r, d_, t, "C", note)

# --- fan made ---------------------------------------------------------------------------------------
for key, label in (("F09", "Fan 3D model (Sketchfab, JMGameDev)"), ("F10", "Fan 3D print (Printables, Gonz Heredia)")):
    b, r, d_, t = app(key)
    add(key, label + " - apparent", "fan (apparent)", b, r, d_, t, "C", "strong perspective, not removed")
    cam = side[key]["camera"]
    c = corrected(key, cam["d"], button_lift=0.06)
    add(key + "c", label + f" - camera at {cam['d']:.1f} R removed", "fan", cam["band_true_over_D"], round(c["ring"], 4),
        None if c["disc"] is None else round(c["disc"], 4), None if c["button"] is None else round(c["button"], 4), "C",
        "camera distance fit is biased low by the deeply recessed band -> treat as lower bound")

# Fan vectors: numbers read straight from the SVG path data (see comments), D taken at the outline centre line.
# F07 'Poke Ball.svg': shell arcs r = 127.279 * 2.5786 = 328.20 (stroke 18.31); band rect 54.335 + stroke 18.308 =
#   72.64 black; white disc r = 20.536 * 4.18 = 85.84 with an 18.10 stroke (= the whole black ring); grey button
#   r = 20.536 * 2.2516 = 46.24.
D07 = 2 * 328.20
add("F07", "Fan vector (Commons 'Poke Ball.svg', used on Wikipedia)", "fan", round(72.64 / D07, 4),
    round(2 * (85.84 + 9.05) / D07, 4), round(2 * (85.84 - 9.05) / D07, 4), round(2 * 46.24 / D07, 4), "A",
    "exact vector numbers; the black ring is only a thick stroke")
# F13 'Poke Ball icon.svg': black disc r = 255.7 with coloured halves inset to r = 215.5 (-> centre line 235.6);
#   band = gap 279.7 .. 314.3; ring outer r = 83.9 (hypot(82.1, 17.3)); white centre r = 49.4; no button.
D13 = 2 * 235.6
add("F13", "Fan icon (Commons 'Poke Ball icon.svg')", "fan", round(34.6 / D13, 4), round(2 * 83.9 / D13, 4),
    round(2 * 49.4 / D13, 4), None, "B", "stylised icon with uniform thick strokes")


def fmt(v):
    return "-" if v is None else f"{v:.3f}"


print("| id | source | group | band/D | ring OD/D | white disc/D | button/D | grade |")
print("|---|---|---|---|---|---|---|---|")
for r in rows:
    print(f"| {r['id']} | {r['label']} | {r['group']} | {fmt(r['band'])} | {fmt(r['ring'])} | {fmt(r['disc'])} | {fmt(r['button'])} | {r['grade']} |")

SETS = {
    "geometry-grade (2D art + perspective-corrected replicas + exact vectors): F01 F08 F11 TWC F06 F07 F13":
        ["F01", "F08", "F11", "TWC", "F06", "F07", "F13"],
    "official only, geometry-grade: F01 F08 F11 TWC F06": ["F01", "F08", "F11", "TWC", "F06"],
    "all independent sources (apparent values where perspective unknown): + F02 F03 F12 F09 F10":
        ["F01", "F08", "F11", "TWC", "F06", "F07", "F13", "F02", "F03", "F12", "F09", "F10"],
}
byid = {r["id"]: r for r in rows}
stats = {}
print()
for name, ids in SETS.items():
    print(f"**{name}**")
    print()
    print("| quantity | n | mean | median | min | max |")
    print("|---|---|---|---|---|---|")
    stats[name] = {}
    for q, lab in (("band", "band/D"), ("ring", "ring OD/D"), ("disc", "white disc/D"), ("button", "button/D")):
        vals = [byid[i][q] for i in ids if byid[i][q] is not None]
        st = dict(n=len(vals), mean=round(statistics.mean(vals), 4), median=round(statistics.median(vals), 4),
                  min=min(vals), max=max(vals))
        stats[name][q] = st
        print(f"| {lab} | {st['n']} | {st['mean']:.3f} | {st['median']:.3f} | {st['min']:.3f} | {st['max']:.3f} |")
    print()

REC = dict(band=0.070, ring=0.340, disc=0.225, button=0.140, band_recess=0.012, button_above_collar=0.023)
REC["ring_width"] = round((REC["ring"] - REC["disc"]) / 2, 4)
REC["collar_plane_below_apex"] = round(0.5 * (1 - math.sqrt(1 - REC["ring"] ** 2)), 4)   # flat ring face at the chord plane
print("| quantity | ratio of D | D = 90 mm | D = 100 mm | D = 110 mm |")
print("|---|---|---|---|---|")
for k, lab in (("band", "black band height"), ("ring", "black ring outer diameter"), ("disc", "white disc diameter (= ring inner diameter)"),
               ("ring_width", "radial width of the black ring"), ("button", "button diameter"),
               ("band_recess", "band recess below the shell surface"),
               ("collar_plane_below_apex", "flat ring/collar plane below the sphere apex (if the ring face is flat)"),
               ("button_above_collar", "button face above the white collar")):
    print(f"| {lab} | {REC[k]:.4f} | {REC[k] * 90:.1f} | {REC[k] * 100:.1f} | {REC[k] * 110:.1f} |")

(HERE / "measurements_summary.json").write_text(json.dumps(dict(rows=rows, stats=stats, recommended=REC), indent=1), encoding="utf-8")
