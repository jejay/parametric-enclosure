"""Measure Poke Ball proportions (as fractions of the outer diameter D) in the F* reference images.

    uv run python -I research/reference_images/measure_front_views.py            # all images
    uv run python -I research/reference_images/measure_front_views.py F04 F05    # selected

Per image the script fits
  * the silhouette circle                       -> D
  * the outer edge of the black ring            -> ring OD   (ellipse major axis)
  * the inner edge of the black ring            -> white-disc diameter
  * the edge of the innermost button            -> button diameter
  * the black band thickness on lines perpendicular to the band at
    centre +/- f*R  (f = 0.5 is "25 % / 75 % of the width"; a different f is
    used where the button ring or an occluder covers that spot - see labels)
and writes an overlay PNG to overlays/ so the fits can be checked by eye.
All search windows below were chosen by looking at zoomed crops (measure_probe.py).

Corrections applied here (and only these):
  * tilt:     band thickness / cos(tilt), tilt from the button-centre offset
              (orthographic model, see measure_common.view_angles)
  * outlines: drawn artwork has black outlines that are not part of the object.
              Object edges are taken at the outline CENTRE line.  Where the
              script can only find the edge of a dark (fill + outline) region
              the measured outline width is added/subtracted (see `corr`).
NOT applied here: camera perspective of photos/renders (front features look up
to ~10 % too big relative to the silhouette).  That is estimated separately in
measure_side_views.py and applied in the report.

Results go to stdout and to measurements_front.json.
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("measure_common", HERE / "measure_common.py")
mc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mc)

CYAN, YELLOW, GREEN, MAGENTA, BLUE = (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 255), (40, 90, 255)
A = mc.arange_deg


# ------------------------------------------------------------------ primitives
def ring_fit(field, c0, r0, r1, angles, polarity, kind="edge", shape="ellipse", sigma=1.0, k=2.5):
    """Fit a circle/ellipse to edge points found on rays from c0 between radii r0..r1."""
    pts = mc.ray_edges(field, c0, angles, r0, r1, polarity, kind=kind, sigma=sigma)
    if shape == "circle":
        cx, cy, r, rms, keep = mc.robust_circle(pts, k=k)
        return mc.circle_as_ellipse(cx, cy, r, rms), pts[keep]
    keep = np.ones(len(pts), bool)
    e = mc.fit_ellipse(pts)
    for _ in range(3):
        ct, st = math.cos(math.radians(e["theta_deg"])), math.sin(math.radians(e["theta_deg"]))
        dx, dy = pts[:, 0] - e["cx"], pts[:, 1] - e["cy"]
        u, v = dx * ct + dy * st, -dx * st + dy * ct
        rho = np.sqrt((u / e["a"]) ** 2 + (v / e["b"]) ** 2)
        res = np.abs((rho - 1.0) * np.hypot(u, v) / np.maximum(rho, 1e-9))
        new = res <= max(k * e["rms"], 1.0)
        if new.sum() < 8 or (new == keep).all():
            break
        keep = new
        e = mc.fit_ellipse(pts[keep])
    return e, pts[keep]


def model_fit(field, ball, c0, r0, r1, angles, polarity, kind="edge", sigma=1.0, k=2.5, lift=0.0):
    """Ellipse fit constrained by the sphere geometry (3 free parameters: centre + size).

    A circle lying on (or parallel to) the sphere surface, whose centre is seen
    at distance `off` from the ball centre, projects orthographically to an
    ellipse whose MINOR axis points along the radius through the ball centre and
    whose axis ratio is cos(gamma), sin(gamma) = off / h, h = distance of the
    circle's plane from the ball centre = sqrt(R^2 - a^2) (+ lift for a raised
    button face).  Only centre and semi-major axis a are fitted, which keeps the
    result stable where part of the outline is hidden (ring merged with the band).
    Returns (ellipse dict incl. the free-fit major axis for comparison, kept points).
    """
    pts = mc.ray_edges(field, c0, angles, r0, r1, polarity, kind=kind, sigma=sigma)
    R = ball["a"]
    cx, cy = float(c0[0]), float(c0[1])
    a = 0.5 * (r0 + r1)
    keep = np.ones(len(pts), bool)
    q = 1.0
    phi = 0.0
    rms = 0.0
    for it in range(8):
        ox, oy = cx - ball["cx"], cy - ball["cy"]
        off = math.hypot(ox, oy)
        h = math.sqrt(max(R * R - a * a, (0.3 * R) ** 2)) + lift * R
        sing = min(off / h, 0.95)
        q = math.sqrt(1.0 - sing * sing)
        phi = math.atan2(oy, ox) if off > 1e-6 else 0.0
        cp, sp = math.cos(phi), math.sin(phi)
        dx, dy = pts[:, 0] - cx, pts[:, 1] - cy
        u = (dx * cp + dy * sp) / q
        v = -dx * sp + dy * cp
        ucx, vcy, r, rms = mc.fit_circle(np.c_[u[keep], v[keep]])
        if it >= 2:
            res = np.abs(np.hypot(u - ucx, v - vcy) - r)
            new = res <= max(k * rms, 1.0)
            if new.sum() >= 6:
                keep = new
        cx, cy = cx + ucx * q * cp - vcy * sp, cy + ucx * q * sp + vcy * cp
        a = r
    e = dict(cx=float(cx), cy=float(cy), a=float(a), b=float(a * q), theta_deg=float((math.degrees(phi) + 90.0) % 180.0),
             rms=float(rms), model_axis_ratio=round(q, 4))
    if keep.sum() >= 8:
        free = mc.fit_ellipse(pts[keep])
        e["free_major"] = 2 * free["a"]
        e["free_axis_ratio"] = round(free["b"] / free["a"], 4)
    return e, pts[keep]


def multi_circle(parts, k=2.5):
    """Silhouette circle from several (field, c0, r0, r1, angles, polarity, kind, sigma) ray sets."""
    pts = [mc.ray_edges(f, c0, ang, r0, r1, pol, kind=kind, sigma=sig) for f, c0, r0, r1, ang, pol, kind, sig in parts]
    pts = np.vstack([p for p in pts if len(p)])
    cx, cy, r, rms, keep = mc.robust_circle(pts, k=k)
    return mc.circle_as_ellipse(cx, cy, r, rms), pts[keep]


def band_perp(field, ball, f, s0, s1, roll_deg=0.0, pol=(-1, +1), kind=("edge", "edge"), sigma=1.0, min_gap=2.0,
              s_mid=None):
    """Band thickness on a line perpendicular to the band.

    The line starts at  centre + f*R*e + s0*n  and ends at  ... + s1*n  where e is
    the band direction on screen (rolled by roll_deg, positive = right end up)
    and n the screen-down normal to it.  The upper edge is searched on the whole
    line (or on s0..s_mid if s_mid is given), the lower edge below the upper one
    (or on s_mid..s1).  Returns dict(p0, p1, t).
    """
    th = math.radians(roll_deg)
    e = np.array([math.cos(th), -math.sin(th)])
    n = np.array([math.sin(th), math.cos(th)])
    base = np.array([ball["cx"], ball["cy"]]) + f * ball["a"] * e
    fn0 = mc.find_edge if kind[0] == "edge" else mc.find_line
    fn1 = mc.find_edge if kind[1] == "edge" else mc.find_line
    a = fn0(field, base + s0 * n, base + (s1 if s_mid is None else s_mid) * n, pol[0], sigma=sigma)
    if a is None:
        raise RuntimeError("band top edge not found")
    b = fn1(field, (a[0] + min_gap * n) if s_mid is None else (base + s_mid * n), base + s1 * n, pol[1], sigma=sigma)
    if b is None:
        raise RuntimeError("band bottom edge not found")
    return dict(p0=a[0], p1=b[0], t=float(np.hypot(*(b[0] - a[0]))))


def summarise(name, src, ball, ring, disc, button, band, notes, roll_deg=0.0, corr=None, tilt_correct=True):
    """Turn raw pixel fits into ratios of D.  `corr` holds additive pixel corrections (outlines)."""
    corr = corr or {}
    D_raw = 2 * ball["a"]
    D = D_raw + corr.get("D", 0.0)
    yaw = tilt = None
    ref = ring or disc
    if ref is not None:
        yaw, tilt = mc.view_angles((ball["cx"], ball["cy"]), ball["a"], (ref["cx"], ref["cy"]), roll_deg)
    out = dict(name=name, source=src, D_px=round(D, 2), D_raw_px=round(D_raw, 2),
               ball_centre=[round(ball["cx"], 2), round(ball["cy"], 2)], ball_fit_rms_px=round(ball["rms"], 2),
               roll_deg=roll_deg, yaw_deg=None if yaw is None else round(yaw, 1),
               tilt_deg=None if tilt is None else round(tilt, 1), corr_px=corr, notes=notes)
    for key, e in (("ring_od", ring), ("disc", disc), ("button", button)):
        if e is None:
            out[key + "_over_D"] = None
            continue
        major = 2 * e["a"] + corr.get(key, 0.0)
        out[key + "_px"] = round(major, 2)
        out[key + "_minor_px"] = round(2 * e["b"] + corr.get(key, 0.0), 2)
        out[key + "_fit_rms_px"] = round(e["rms"], 2)
        out[key + "_over_D"] = round(major / D, 4)
        if "free_major" in e:  # unconstrained ellipse, for comparison only
            out[key + "_free_fit_over_D"] = round((e["free_major"] + corr.get(key, 0.0)) / D, 4)
            out[key + "_axis_ratio_model_vs_free"] = [e["model_axis_ratio"], e["free_axis_ratio"]]
    if band:
        scale = 1.0 / math.cos(math.radians(tilt)) if (tilt_correct and tilt is not None) else 1.0
        out["band_tilt_scale"] = round(scale, 4)
        th, cen = [], []
        for lab, b in band.items():
            t = b["t"] * scale + corr.get("band", 0.0)
            th.append(t)
            mid = (np.asarray(b["p0"]) + np.asarray(b["p1"])) / 2
            thr = math.radians(roll_deg)
            n = np.array([math.sin(thr), math.cos(thr)])
            cen.append(float(np.dot(mid - np.array([ball["cx"], ball["cy"]]), n)) / D)
            out[f"band_{lab}_px"] = round(t, 2)
            out[f"band_{lab}_over_D"] = round(t / D, 4)
        out["band_over_D"] = round(float(np.mean(th)) / D, 4)
        # signed distance of the band mid-line below the ball centre, as seen (not tilt-corrected)
        out["band_centre_offset_over_D"] = round(float(np.mean(cen)), 4)
    else:
        out["band_over_D"] = None
    return out


def draw(rgb, name, ball, ellipses, pts, band, crop=None, scale=1.0):
    ov = mc.Overlay(rgb, crop, scale)
    w = 2 if scale < 1 else 1
    ov.ellipse(ball, CYAN, w)
    for e, col in zip(ellipses, (YELLOW, GREEN, MAGENTA)):
        if e is not None:
            ov.ellipse(e, col, w)
    for p, col in pts:
        ov.dots(p, col, r=2)
    for lab, b in (band or {}).items():
        ov.poly([b["p0"], b["p1"]], BLUE, 3, closed=False)
    return ov.save(name + "_overlay.png")


def fields(path, bg=(255, 255, 255)):
    rgb, alpha = mc.load(path, bg)
    f = {n: mc.metric(rgb, alpha, n, bg) for n in ("lum", "val", "min", "R", "B", "red", "bgdist")}
    if alpha is not None:
        f["alpha"] = alpha * 255.0
    return rgb, f


# ------------------------------------------------------------------- per image
def F01():
    """Ken Sugimori's official Poke Ball artwork (hand drawn, 3/4 view from above, ~6.5 px outlines)."""
    rgb, f = fields(HERE / "F01_sugimori_artwork.png")
    v = f["val"]
    c = (347, 345)
    # silhouette = centre line of the drawn outline
    ball, bp = ring_fit(v, c, 318, 342, A((0, 357), step=3), -1, kind="line", shape="circle", sigma=1.0)
    outer, _ = ring_fit(f["alpha"], c, 318, 345, A((0, 357), step=3), -1, shape="circle")
    w = 2 * (outer["a"] - ball["a"])                     # outline width
    c0 = (285, 482)
    # dark ring: outer boundary of (fill + outline) -> subtract one outline width for centre lines
    ring, rp = model_fit(v, ball, c0, 78, 112, A((28, 152), (208, 332), step=4), +1, sigma=1.0)
    # white disc: inner boundary of the ring's inner outline -> add one outline width
    disc, dp = model_fit(v, ball, c0, 46, 80, A((0, 356), step=4), -1, sigma=1.0)
    # button: its own drawn outline (centre line)
    butt, tp = model_fit(v, ball, c0, 30, 52, A((0, 356), step=4), -1, kind="line", sigma=1.0)
    band = {"f-0.62": band_perp(v, ball, -0.62, 60, 180, sigma=1.0),
            "f+0.50": band_perp(v, ball, +0.50, 80, 190, sigma=1.0)}
    draw(rgb, "F01", ball, (ring, disc, butt), ((bp, CYAN), (rp, YELLOW), (dp, GREEN), (tp, MAGENTA)), band, scale=1.5)
    return summarise("F01 Sugimori official artwork", "official 2D art", ball, ring, disc, butt, band,
                     f"hand-drawn, tilted view; outline width {w:.1f} px; ellipses are not mutually consistent "
                     "(button taller than wide, disc wider than tall) - artistic, not geometric",
                     corr={"ring_od": -w, "disc": +w, "band": -w})


def F02():
    """Pokemon GO item sprite (official 3D render, 186 px): tilted down ~20 deg, yawed right."""
    rgb, f = fields(HERE / "F02_pokemon_go_item_sprite.png")
    v = f["val"]
    ball, bp = ring_fit(f["alpha"], (93, 92), 78, 100, A((0, 357), step=3), -1, shape="circle", sigma=0.7)
    c0 = (119, 122)
    ring, rp = model_fit(v, ball, c0, 24, 40, A((50, 155), (220, 350), step=5), +1, sigma=0.7)
    disc, dp = model_fit(v, ball, c0, 14, 28, A((0, 355), step=5), -1, sigma=0.7)
    # button = thin bright rim highlight inside the bluish disc
    butt, tp = model_fit(f["min"], ball, c0, 8, 17.5, A((0, 355), step=10), +1, kind="line", sigma=0.6)
    band = {"f-0.50": band_perp(v, ball, -0.50, 5, 50, sigma=0.7),
            "f-0.70": band_perp(v, ball, -0.70, 5, 50, sigma=0.7),
            "f+0.80": band_perp(v, ball, +0.80, 0, 40, sigma=0.7)}
    draw(rgb, "F02", ball, (ring, disc, butt), ((bp, CYAN), (rp, YELLOW), (dp, GREEN), (tp, MAGENTA)), band, scale=5)
    return summarise("F02 Pokemon GO item sprite", "official 3D render", ball, ring, disc, butt, band,
                     "186 px sprite, +/-0.5 px edges => +/-5 % on the band, +/-2 % on the ring; "
                     "75 % column is inside the button ring, f=+0.8 used on that side")


def F03():
    """Let's Go Pikachu/Eevee screenshot: in-game model seen straight on; button glowing (no disc/button edges)."""
    rgb, f = fields(HERE / "F03_letsgo_screenshot.jpg")
    c = (805, 506)
    ball, bp = multi_circle([
        (f["red"], c, 88, 122, A((22, 158), step=4), -1, "edge", 1.2),          # red shell against grass
        (f["B"], c, 88, 122, A((186, 204), (-24, -6), step=3), -1, "edge", 1.2),  # white shell against grass
    ])
    v = f["val"]
    c0 = (805, 516)
    ring, rp = model_fit(v, ball, c0, 26, 48, A((35, 145), (215, 325), step=5), +1, sigma=1.0)
    band = {"25pct": band_perp(v, ball, -0.5, -25, 45, sigma=1.0),
            "75pct": band_perp(v, ball, +0.5, -25, 45, sigma=1.0)}
    draw(rgb, "F03", ball, (ring, None, None), ((bp, CYAN), (rp, YELLOW)), band, crop=(660, 360, 950, 650), scale=4)
    return summarise("F03 Let's Go in-game model (screenshot)", "official game 3D model", ball, ring, None, None, band,
                     "210 px ball in a JPEG screenshot; button is glowing so only D, band and ring OD are usable")


def F04():
    """The Wand Company die-cast Dusk Ball, straight front photo (same tooling as the Poke Ball).

    Band / ring / disc / button are all orange here; shell is green + black.
    Edges: orange->shell via the R channel; disc and button via the dark shadow
    groove around them (line centre).
    """
    rgb, f = fields(HERE / "F04_twc_dusk_ball_front.jpg")
    # silhouette: skip the floor shadow (bottom) and the band ends (0 / 180 deg, band is recessed there)
    ball, bp = ring_fit(f["bgdist"], (1230, 1092), 850, 1010, A((-30, -9), (9, 171), (189, 210), step=3), -1,
                        shape="circle", sigma=2.0)
    c0 = (1246, 1103)
    ring, rp = model_fit(f["R"], ball, c0, 300, 400, A((18, 162), (198, 342), step=4), -1, sigma=1.5)
    disc, dp = model_fit(f["lum"], ball, c0, 212, 262, A((0, 356), step=4), -1, kind="line", sigma=1.5)
    butt, tp = model_fit(f["lum"], ball, c0, 130, 178, A((0, 356), step=4), -1, kind="line", sigma=1.5)
    rg = rgb[..., 0] - rgb[..., 1]                       # orange-ness: band > 0, green/black shell <= 0
    band = {"25pct": band_perp(rg, ball, -0.5, -130, 150, pol=(+1, -1), sigma=1.5),
            "75pct": band_perp(rg, ball, +0.5, -130, 150, pol=(+1, -1), sigma=1.5)}
    draw(rgb, "F04", ball, (ring, disc, butt), ((bp, CYAN), (rp, YELLOW), (dp, GREEN), (tp, MAGENTA)), band, scale=0.45)
    return summarise("F04 TWC die-cast replica (Dusk Ball), front photo", "official replica, photo", ball,
                     ring, disc, butt, band,
                     "straight-on studio photo, 1876 px ball; ring/disc/button are separated by shadow grooves")


def F05():
    """The Wand Company Poke Ball held in a hand (3400 px): near-front, yawed ~15 deg, rolled ~2 deg."""
    rgb, alpha = mc.load(HERE / "F05_twc_pokeball_in_hand.jpg")
    f = {n: mc.metric(rgb, alpha, n) for n in ("val", "lum", "bgdist")}
    c = (1780, 1620)
    # Silhouette: only arcs where the ball borders the white background (fingers/palm hide the rest).
    # The glossy shells have a soft bright rim band inside the outline, so the OUTERMOST crossing of a
    # background-distance threshold is used instead of the strongest gradient.
    bp = mc.ray_crossings(f["bgdist"], c, A((-56, -4), (5, 15), (34, 46), (112, 124), step=2), 840, 1020, 30.0, sigma=1.5)
    cx, cy, r, rms, keep = mc.robust_circle(bp)
    ball, bp = mc.circle_as_ellipse(cx, cy, r, rms), bp[keep]
    v = f["val"]
    c0 = (2032, 1692)
    ring, rp = model_fit(v, ball, c0, 290, 400, A((22, 158), (204, 338), step=4), +1, sigma=1.5)
    disc, dp = model_fit(v, ball, c0, 190, 270, A((0, 356), step=4), -1, sigma=1.5)
    butt, tp = model_fit(f["lum"], ball, (2048, 1697), 125, 185, A((30, 150), (210, 330), step=4), -1, kind="line", sigma=1.5)
    band = {"25pct": band_perp(v, ball, -0.5, -150, 240, roll_deg=2.9, sigma=3.0),
            "f+0.80": band_perp(v, ball, +0.80, -220, 220, roll_deg=2.9, sigma=3.0)}
    draw(rgb, "F05", ball, (ring, disc, butt), ((bp, CYAN), (rp, YELLOW), (dp, GREEN), (tp, MAGENTA)), band,
         crop=(600, 500, 2950, 2800), scale=0.42)
    return summarise("F05 TWC die-cast replica (Poke Ball) in hand", "official replica, photo/composite", ball,
                     ring, disc, butt, band,
                     "silhouette partly hidden by fingers (circle fitted to the free arcs, -56..124 deg); 75 % column is inside the ring, "
                     "f=+0.8 used; button = groove around the raised button face", roll_deg=2.9)


def F06():
    """The Wand Company MINI Poke Ball (40 mm), official product render, front view."""
    rgb, f = fields(HERE / "F06_twc_mini_pokeball_front.jpg")
    v = f["val"]
    ball, bp = ring_fit(f["bgdist"], (935, 965), 700, 850, A((10, 170), (190, 258), step=3), -1, shape="circle", sigma=2.0)
    c0 = (915, 975)
    ring, rp = model_fit(v, ball, c0, 280, 380, A((28, 156), (204, 336), step=4), +1, sigma=1.5)
    disc, dp = model_fit(v, ball, c0, 180, 260, A((0, 356), step=4), -1, sigma=1.5)
    butt, tp = model_fit(f["lum"], ball, (922, 973), 118, 168, A((0, 356), step=4), -1, kind="line", sigma=1.5)
    band = {"f-0.60": band_perp(v, ball, -0.60, -120, 140, sigma=2.5),
            "f+0.60": band_perp(v, ball, +0.60, -120, 140, sigma=2.5)}
    draw(rgb, "F06", ball, (ring, disc, butt), ((bp, CYAN), (rp, YELLOW), (dp, GREEN), (tp, MAGENTA)), band, scale=0.5)
    return summarise("F06 TWC MINI replica (40 mm), render", "official replica, render", ball, ring, disc, butt, band,
                     "CG render with visibly strong perspective; different product from F04/F05 (40 mm, thicker band)")


def F08():
    """Flat vector Poke Ball in the official clip-art style (Commons 'Pokebola'), ~14 px outlines, tilted view."""
    rgb, f = fields(HERE / "F08_commons_pokebola_vector.png")
    v = f["val"]
    ball, bp = ring_fit(v, (579, 578), 545, 578, A((0, 357), step=3), -1, kind="line", shape="circle", sigma=1.5)
    c0 = (713, 509)
    ring, rp = model_fit(v, ball, c0, 160, 215, A((35, 150), (215, 325), step=5), -1, kind="line", sigma=1.5)
    disc, dp = model_fit(v, ball, c0, 112, 152, A((0, 355), step=5), -1, kind="line", sigma=1.5)
    butt, tp = model_fit(v, ball, c0, 70, 108, A((0, 355), step=5), -1, kind="line", sigma=1.5)
    band = {lab: band_perp(v, ball, fr, -130, 110, pol=(-1, -1), kind=("line", "line"), sigma=1.5, s_mid=-10)
            for lab, fr in (("f-0.66", -0.66), ("f+0.74", +0.74))}
    draw(rgb, "F08", ball, (ring, disc, butt), ((bp, CYAN), (rp, YELLOW), (dp, GREEN), (tp, MAGENTA)), band, scale=0.85)
    return summarise("F08 vector art, official clip-art style", "2D vector (provenance unverified)", ball, ring, disc,
                     butt, band, "all edges taken at outline centre lines; stylised, thick band")


def F09():
    """Fan 3D model (Sketchfab, JMGameDev 'Pokemon Basic Pokeball'), viewer thumbnail, camera slightly above."""
    rgb, f = fields(HERE / "F09_sketchfab_jmgamedev_basic_pokeball.jpg", bg=(67, 65, 66))
    v = f["val"]
    ball, bp = ring_fit(f["bgdist"], (987, 547), 255, 325, A((14, 166), (194, 346), step=3), -1, shape="circle", sigma=1.0)
    c0 = (897, 574)
    ring, rp = model_fit(v, ball, c0, 88, 125, A((25, 155), (205, 335), step=5), +1, sigma=1.0)
    disc, dp = model_fit(v, ball, c0, 60, 92, A((0, 355), step=5), -1, sigma=1.0)
    butt, tp = model_fit(f["lum"], ball, (895, 578), 30, 52, A((60, 250), step=5), -1, kind="line", sigma=1.0)
    band = {"f-0.78": band_perp(v, ball, -0.78, -40, 90, sigma=1.0),
            "75pct": band_perp(v, ball, +0.50, -40, 90, sigma=1.0)}
    draw(rgb, "F09", ball, (ring, disc, butt), ((bp, CYAN), (rp, YELLOW), (dp, GREEN), (tp, MAGENTA)), band,
         crop=(640, 200, 1340, 900), scale=1.4)
    return summarise("F09 fan 3D model (Sketchfab, JMGameDev)", "fan 3D model, render", ball, ring, disc, butt, band,
                     "low-poly silhouette; band deeply recessed, so its visible black height in this tilted view "
                     "understates the shell gap slightly; 25 % column is inside the ring, f=-0.78 used")


def F10():
    """Most-downloaded Printables Poke Ball (Gonz Heredia), phone photo of a painted print, front view."""
    rgb, f = fields(HERE / "F10_printables_gonzheredia_print_front.jpg")
    v = f["val"]
    c = (1515, 1080)
    ball, bp = multi_circle([
        (f["red"], c, 700, 860, A((12, 168), step=3), -1, "edge", 3.0),             # red shell vs wall / console
        (v, c, 700, 860, A((188, 236), (-52, -8), step=3), -1, "edge", 3.0),         # white shell vs dark table
    ])
    c0 = (1487, 1090)
    ring, rp = model_fit(v, ball, c0, 240, 340, A((30, 150), (212, 328), step=4), +1, sigma=3.0)
    disc, dp = model_fit(v, ball, c0, 170, 250, A((0, 356), step=4), -1, sigma=3.0)
    band = {"f-0.62": band_perp(v, ball, -0.62, -150, 150, sigma=6.0),
            "f+0.62": band_perp(v, ball, +0.62, -150, 150, sigma=6.0)}
    draw(rgb, "F10", ball, (ring, disc, None), ((bp, CYAN), (rp, YELLOW), (dp, GREEN)), band,
         crop=(600, 150, 2500, 2000), scale=0.5)
    return summarise("F10 fan 3D print (Printables, Gonz Heredia)", "fan 3D print, phone photo", ball, ring, disc,
                     None, band, "close-up phone photo (strong perspective); the white part is ONE big button "
                     "(reported as 'disc'), its faint raised centre is not a separate part; the band has the "
                     "parting seam in its middle")


def F11():
    """TV anime EP001: Poke Ball shown on the Pokedex screen (160 px, drawn, tilted)."""
    rgb, f = fields(HERE / "F11_anime_ep001_pokedex.png")
    v = f["val"]
    ball, bp = ring_fit(v, (328, 246), 70, 90, A((-40, 230), step=4), -1, kind="line", shape="circle", sigma=0.7)
    c0 = (316, 262.5)
    ring, rp = model_fit(v, ball, c0, 19, 34, A((40, 150), (215, 330), step=6), +1, sigma=0.7)
    disc, dp = model_fit(v, ball, c0, 9.5, 19, A((0, 354), step=6), -1, sigma=0.6)
    butt, tp = model_fit(v, ball, c0, 5, 11.5, A((0, 350), step=10), -1, kind="line", sigma=0.5)
    band = {"f-0.70": band_perp(v, ball, -0.70, -5, 45, sigma=0.7)}
    draw(rgb, "F11", ball, (ring, disc, butt), ((bp, CYAN), (rp, YELLOW), (dp, GREEN), (tp, MAGENTA)), band,
         crop=(230, 150, 425, 345), scale=5)
    return summarise("F11 TV anime EP001 (Pokedex screen)", "official anime frame", ball, ring, disc, butt, band,
                     "160 px, blurry TV frame: +/-1 px = +/-8 % on the band, +/-2 % on the ring; right half of the "
                     "band is merged with a drawn shadow, so only the left side is measured")


def F12():
    """Smash Bros. for Wii U trophy render of the Poke Ball: rolled ~11 deg, camera below the equator."""
    rgb, f = fields(HERE / "F12_ssb_wiiu_trophy_render.png")
    v = f["val"]
    ball, bp = ring_fit(f["alpha"], (253, 202), 100, 135, A((0, 357), step=3), -1, shape="circle", sigma=0.8)
    c0 = (288, 164)
    ring, rp = model_fit(v, ball, c0, 34, 54, A((40, 170), (225, 345), step=5), +1, sigma=0.8)
    disc, dp = model_fit(v, ball, c0, 22, 40, A((0, 355), step=5), -1, sigma=0.8)
    roll = 11.0
    band = {"f-0.55": band_perp(v, ball, -0.55, -60, 20, roll_deg=roll, sigma=0.8),
            "f+0.80": band_perp(v, ball, +0.80, -60, 20, roll_deg=roll, sigma=0.8)}
    draw(rgb, "F12", ball, (ring, disc, None), ((bp, CYAN), (rp, YELLOW), (dp, GREEN)), band,
         crop=(120, 70, 400, 350), scale=3.4)
    return summarise("F12 Smash Bros. Wii U trophy render", "official game 3D model (Nintendo)", ball, ring, disc,
                     None, band, "low-poly game model, strongly tilted and rolled; button is a small protruding "
                     "stub that cannot be fitted as a circle here", roll_deg=roll)


IMAGES = {"F01": F01, "F02": F02, "F03": F03, "F04": F04, "F05": F05, "F06": F06,
          "F08": F08, "F09": F09, "F10": F10, "F11": F11, "F12": F12}

SHOW = ("D_px", "yaw_deg", "tilt_deg", "band_over_D", "band_centre_offset_over_D", "ring_od_over_D", "disc_over_D",
        "button_over_D")


def _jsonable(o):
    if isinstance(o, np.ndarray):
        return [round(float(x), 2) for x in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    raise TypeError(type(o))


def main(argv):
    keys = argv or list(IMAGES)
    results = []
    for k in keys:
        r = IMAGES[k]()
        results.append(r)
        if argv:
            print(json.dumps(r, indent=1, default=_jsonable))
    print()
    print("image  " + "  ".join(f"{s:>12s}" for s in ("D_px", "yaw", "tilt", "band/D", "bandOff/D", "ringOD/D", "disc/D", "button/D")))
    for k, r in zip(keys, results):
        print(f"{k:6s} " + "  ".join(f"{'-' if r.get(s) is None else r[s]:>12}" for s in SHOW))
    if not argv:
        (HERE / "measurements_front.json").write_text(json.dumps(results, indent=1, default=_jsonable), encoding="utf-8")
        print("\nwrote measurements_front.json")


if __name__ == "__main__":
    main(sys.argv[1:])
