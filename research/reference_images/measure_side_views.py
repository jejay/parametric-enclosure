"""Depth information from The Wand Company replica photos: camera perspective, band recess, button protrusion.

    uv run python -I research/reference_images/measure_side_views.py

Images used
  F04  Dusk Ball, straight front      (band thickness profile -> camera distance; band recess at both limbs)
  F05  Poke Ball in hand, near front  (band thickness profile -> camera distance)
  S01  Poke Ball, 3/4 view (yaw ~57)  (band profile; recess at the limb; ring / disc / button-face ellipses ->
                                       how far the button face stands above the ring plane)
  S03  Master Ball, 3/4 view          (same as S01, mirrored: independent second estimate, same tooling)

Model (all lengths in units of the ball radius R, camera at distance d from the ball centre, in the
equatorial plane, looking at the centre; pinhole projection):
  * silhouette radius on screen          R_app = F / sqrt(d^2 - 1)
  * a point at depth z (towards camera)  is magnified by F / (d - z)
  * the shell lips bounding the band are circles of radius ~1 at heights +/-h, so at screen position X the
    band appears  T(X) = 2 h F / (d - z),  z = cos(lambda),  X = F sin(lambda) / (d - cos(lambda)).
Fitting T(X) over many columns gives d (and the true h).  Front features (ring/disc/button) are then
de-magnified by (d - z_feature) / sqrt(d^2 - 1) to get true ratios of the diameter.

Writes measurements_side.json and overlays/S01_overlay.png, overlays/S03_overlay.png.
"""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mc = _load("measure_common")
fv = _load("measure_front_views")
A = mc.arange_deg
CYAN, YELLOW, GREEN, MAGENTA, BLUE = fv.CYAN, fv.YELLOW, fv.GREEN, fv.MAGENTA, fv.BLUE


# ------------------------------------------------------------ perspective fit
def _lambda_for(xa, d):
    """Azimuth lambda (0 = towards camera) of the lip point seen at screen position xa = X / R_app."""
    S = math.sqrt(d * d - 1.0)
    lo, hi = 0.0, math.acos(1.0 / d)          # hi = limb
    f = lambda lam: math.sin(lam) * S / (d - math.cos(lam))
    xa = min(abs(xa), f(hi) * 0.999999)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if f(mid) < xa:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def fit_camera_distance(xa, t_over_D, d_grid=None):
    """Least-squares camera distance d (in R) and true band height/D from a thickness profile.

    xa: screen positions X/R_app (signed), t_over_D: band thickness / apparent diameter.
    Returns dict(d, d_lo, d_hi (approx. 2-sigma), band_true_over_D, rms_rel, n).
    """
    xa = np.asarray(xa, float)
    t = np.asarray(t_over_D, float)
    d_grid = d_grid if d_grid is not None else np.exp(np.linspace(math.log(1.6), math.log(300.0), 500))
    sse = []
    hs = []
    for d in d_grid:
        S = math.sqrt(d * d - 1.0)
        g = np.array([S / (d - math.cos(_lambda_for(x, d))) for x in xa])   # T/D = h * g
        h = float((g * t).sum() / (g * g).sum())
        hs.append(h)
        sse.append(float(((t - h * g) ** 2).sum()))
    sse = np.array(sse)
    i = int(np.argmin(sse))
    n = len(xa)
    ok = sse <= sse[i] * (1.0 + 4.0 / max(n - 2, 1))
    return dict(d=round(float(d_grid[i]), 2), d_lo=round(float(d_grid[ok][0]), 2), d_hi=round(float(d_grid[ok][-1]), 2),
                band_true_over_D=round(hs[i], 4),
                band_true_over_D_range=[round(hs[int(np.nonzero(ok)[0][0])], 4), round(hs[int(np.nonzero(ok)[0][-1])], 4)],
                rms_rel=round(float(math.sqrt(sse[i] / n) / t.mean()), 4), n=n)


def demagnify(ratio_measured, d, z):
    """True (orthographic) ratio of D for a front feature measured at depth z (units of R)."""
    return ratio_measured * (d - z) / math.sqrt(d * d - 1.0)


def band_profile(field, ball, fracs, s0, s1, pol, sigma, roll_deg=0.0):
    xs, ts, segs = [], [], {}
    for f in fracs:
        try:
            b = fv.band_perp(field, ball, f, s0, s1, roll_deg=roll_deg, pol=pol, sigma=sigma)
        except RuntimeError:
            continue
        xs.append(f)
        ts.append(b["t"] / (2 * ball["a"]))
        segs[f"{f:+.2f}"] = b
    xs, ts = np.array(xs), np.array(ts)
    ok = np.abs(ts / np.median(ts) - 1.0) < 0.25          # drop gross mis-detections (seams, highlights)
    return xs[ok], ts[ok], segs


def limb_recess(field, ball, y_band, y_shell, side, thr, span=70):
    """Depth of the band surface below the shell surface, seen in profile at the limb.

    On the row y_band the outline of the band itself is found, on the row y_shell
    (just above the band, on the upper shell) the outline of the shell, both as
    the outermost crossing of the same background-distance threshold.  Each is
    referred to the fitted silhouette circle on its row, so the result does not
    depend on the two rows being at different heights.
    side = -1 for the left limb, +1 for the right limb.
    """
    R = ball["a"]

    def gap(y):
        xe = ball["cx"] + side * math.sqrt(max(R * R - (y - ball["cy"]) ** 2, 0.0))
        p = mc.first_crossing(field, (xe + side * span, y), (xe - side * span, y), thr, sigma=1.0)
        return None if p is None else (xe - p[0]) * side          # > 0: inside the circle

    gb, gs = gap(y_band), gap(y_shell)
    if gb is None or gs is None:
        return None
    return dict(row_band=round(float(y_band), 1), row_shell=round(float(y_shell), 1),
                band_inside_circle_px=round(float(gb), 2), shell_inside_circle_px=round(float(gs), 2),
                recess_px=round(float(gb - gs), 2), recess_over_D=round(float(gb - gs) / (2 * R), 4))


# ----------------------------------------------------------------- per image
def front_F04():
    rgb, f = fv.fields(HERE / "F04_twc_dusk_ball_front.jpg")
    ball, _ = fv.ring_fit(f["bgdist"], (1230, 1092), 850, 1010, A((-30, -9), (9, 171), (189, 210), step=3), -1,
                          shape="circle", sigma=2.0)
    rg = rgb[..., 0] - rgb[..., 1]
    fr = [s * v for v in np.arange(0.44, 0.951, 0.03) for s in (-1, 1)]
    xa, t, segs = band_profile(rg, ball, fr, -130, 150, (+1, -1), 1.5)
    cam = fit_camera_distance(xa, t)
    b = segs["-0.92"]
    ytop, ybot = b["p0"][1], b["p1"][1]
    rec = [limb_recess(f["bgdist"], ball, 0.5 * (ytop + ybot), ytop - 22, side, 60.0) for side in (-1, +1)]
    return dict(image="F04", D_px=round(2 * ball["a"], 1), band_profile=[[round(a, 2), round(b, 4)] for a, b in zip(xa, t)],
                camera=cam, limb_recess=rec)


def front_F05():
    rgb, alpha = mc.load(HERE / "F05_twc_pokeball_in_hand.jpg")
    bgd = mc.metric(rgb, alpha, "bgdist")
    val = mc.metric(rgb, alpha, "val")
    bp = mc.ray_crossings(bgd, (1780, 1620), A((-56, -4), (5, 15), (34, 46), (112, 124), step=2), 840, 1020, 30.0, sigma=1.5)
    cx, cy, r, rms, keep = mc.robust_circle(bp)
    ball = mc.circle_as_ellipse(cx, cy, r, rms)
    fr = list(np.arange(-0.85, -0.119, 0.045))          # limb-most columns left out: fingers / lip effects
    xa, t, _ = band_profile(val, ball, fr, -230, 260, (-1, +1), 3.0, roll_deg=2.9)
    cam = fit_camera_distance(xa, t)
    return dict(image="F05", D_px=round(2 * ball["a"], 1), band_profile=[[round(a, 2), round(b, 4)] for a, b in zip(xa, t)],
                camera=cam)


def front_F06():
    """Mini replica render: camera distance from the band profile (the render is visibly wide-angle)."""
    rgb, f = fv.fields(HERE / "F06_twc_mini_pokeball_front.jpg")
    ball, _ = fv.ring_fit(f["bgdist"], (935, 965), 700, 850, A((10, 170), (190, 258), step=3), -1, shape="circle", sigma=2.0)
    fr = [s * v for v in np.arange(0.50, 0.931, 0.03) for s in (-1, 1)]
    xa, t, _ = band_profile(f["val"], ball, fr, -120, 140, (-1, +1), 2.5)
    return dict(image="F06", D_px=round(2 * ball["a"], 1), band_profile=[[round(a, 2), round(b, 4)] for a, b in zip(xa, t)],
                camera=fit_camera_distance(xa, t))


def front_F10():
    """Fan print, phone photo: camera distance from the band profile."""
    rgb, f = fv.fields(HERE / "F10_printables_gonzheredia_print_front.jpg")
    c = (1515, 1080)
    ball, _ = fv.multi_circle([
        (f["red"], c, 700, 860, A((12, 168), step=3), -1, "edge", 3.0),
        (f["val"], c, 700, 860, A((188, 236), (-52, -8), step=3), -1, "edge", 3.0),
    ])
    fr = [s * v for v in np.arange(0.55, 0.901, 0.035) for s in (-1, 1)]
    xa, t, _ = band_profile(f["val"], ball, fr, -150, 150, (-1, +1), 6.0)
    return dict(image="F10", D_px=round(2 * ball["a"], 1), band_profile=[[round(a, 2), round(b, 4)] for a, b in zip(xa, t)],
                camera=fit_camera_distance(xa, t))


def front_F09():
    """Fan 3D model render (Sketchfab thumbnail): camera distance from the band profile (62 px band, coarse)."""
    rgb, f = fv.fields(HERE / "F09_sketchfab_jmgamedev_basic_pokeball.jpg", bg=(67, 65, 66))
    ball, _ = fv.ring_fit(f["bgdist"], (987, 547), 255, 325, A((14, 166), (194, 346), step=3), -1, shape="circle", sigma=1.0)
    fr = list(np.arange(-0.92, -0.699, 0.03)) + list(np.arange(0.10, 0.921, 0.04))
    xa, t, _ = band_profile(f["val"], ball, fr, -40, 90, (-1, +1), 1.0)
    return dict(image="F09", D_px=round(2 * ball["a"], 1), band_profile=[[round(a, 2), round(b, 4)] for a, b in zip(xa, t)],
                camera=fit_camera_distance(xa, t))


def three_quarter(tag, path, c_ball, r_ball, sil_angles, disc_c, disc_r, wall_win, wall_pol,
                  ring_r=None, ring_ang=None, band_fracs=None, band_win=None, limb=None):
    """3/4 view of the Wand Company replica: how far the button stands above the white collar.

    * silhouette circle (outermost threshold crossing against the white background)
    * white collar ("disc"): its whole outline is visible -> free ellipse -> axis ratio q = cos(psi),
      psi = angle between the button axis and the viewing direction
    * button side wall: on the line from the collar centre towards the ball centre (the side of the button
      facing the camera) the wall is seen between the edge of the button face and the foot of the button;
      its width on screen is  p * sin(psi)  ->  p = height of the button face above the collar.
    """
    rgb, alpha = mc.load(HERE / path)
    bgd = mc.metric(rgb, alpha, "bgdist")
    val = mc.metric(rgb, alpha, "val")
    lum = mc.metric(rgb, alpha, "lum")
    bp = mc.ray_crossings(bgd, c_ball, sil_angles, r_ball * 0.9, r_ball * 1.1, 30.0, sigma=1.5)
    cx, cy, r, rms, keep = mc.robust_circle(bp)
    ball, bp = mc.circle_as_ellipse(cx, cy, r, rms), bp[keep]
    D = 2 * r
    out = dict(image=tag, D_px=round(D, 1), ball_fit_rms_px=round(rms, 2))

    disc_pts = mc.ray_edges(val, disc_c, A((0, 355), step=5), disc_r[0], disc_r[1], -1, sigma=1.5)
    disc = mc.fit_ellipse(disc_pts)
    q = disc["b"] / disc["a"]
    psi = math.acos(q)
    out.update(collar_major_over_D=round(2 * disc["a"] / D, 4), collar_axis_ratio=round(q, 4),
               button_axis_to_view_angle_deg=round(math.degrees(psi), 1), collar_fit_rms_px=round(disc["rms"], 2))

    # unit vector from the collar centre towards the ball centre = towards the camera-facing side of the button
    u = np.array([ball["cx"] - disc["cx"], ball["cy"] - disc["cy"]])
    off = float(np.hypot(*u))
    u /= off
    c = np.array([disc["cx"], disc["cy"]])
    # wall_win = (start, end of the window for the face edge, end of the window for the foot of the button)
    e1 = mc.find_edge(lum, c + wall_win[0] * u, c + wall_win[1] * u, wall_pol[0], sigma=1.5)
    e2 = mc.find_edge(lum, e1[0] + 4 * u, c + wall_win[2] * u, wall_pol[1], sigma=1.5)
    wall = float(np.hypot(*(e2[0] - e1[0])))
    p = wall / math.sin(psi)
    # collar plane height above the ball centre (orthographic estimate): offset = h * sin(psi)
    h_collar = off / math.sin(psi)
    out.update(wall_width_px=round(wall, 2), button_face_above_collar_over_D=round(p / D, 4),
               collar_plane_height_over_R=round(h_collar / r, 3),
               button_face_height_over_R=round((h_collar + p) / r, 3))

    ring = None
    if ring_r:
        ring, _ = fv.model_fit(val, ball, c, ring_r[0], ring_r[1], ring_ang, +1, sigma=1.5)
        out.update(ring_major_over_D=round(2 * ring["a"] / D, 4), ring_fit_rms_px=round(ring["rms"], 2))
    segs = {}
    if band_fracs is not None:
        xa, t, segs = band_profile(val, ball, band_fracs, band_win[0], band_win[1], (-1, +1), 1.5)
        out["band_profile"] = [[round(a, 2), round(b, 4)] for a, b in zip(xa, t)]
        out["camera"] = fit_camera_distance(xa, t)
    if limb is not None:
        b = segs[limb[1]]
        ytop, ybot = b["p0"][1], b["p1"][1]
        out["limb_recess"] = limb_recess(bgd, ball, 0.5 * (ytop + ybot), ytop - 15, limb[0], 60.0)

    ov = mc.Overlay(rgb, None, 0.5)
    ov.ellipse(ball, CYAN, 2)
    ov.ellipse(disc, GREEN, 2)
    if ring is not None:
        ov.ellipse(ring, YELLOW, 2)
    ov.dots(bp, CYAN)
    ov.poly([e1[0], e2[0]], MAGENTA, 5, closed=False)
    ov.poly([c, c + wall_win[2] * u], MAGENTA, 1, closed=False)
    for b in segs.values():
        ov.poly([b["p0"], b["p1"]], BLUE, 2, closed=False)
    ov.save(f"{tag}_overlay.png")
    return out


def run_S01():
    return three_quarter(
        "S01", "S01_twc_pokeball_on_white_3q.jpg", (1017, 1005), 632, A((-28, -8), (8, 170), (190, 235), step=3),
        disc_c=(1433, 972), disc_r=(85, 175), wall_win=(30, 60, 95), wall_pol=(-1, +1),
        ring_r=(150, 255), ring_ang=A((95, 155), (205, 265), step=5),
        band_fracs=list(np.arange(-0.93, 0.371, 0.05)), band_win=(-110, 90), limb=(-1, "-0.93"))


def run_S03():
    return three_quarter(
        "S03", "S03_twc_master_ball_on_white.jpg", (1550, 1025), 800,
        A((-40, -14), (18, 50), (128, 150), (195, 215), step=3),
        disc_c=(1044, 947), disc_r=(110, 215), wall_win=(35, 72, 100), wall_pol=(+1, -1))


RUNS = {"F04": front_F04, "F05": front_F05, "F06": front_F06, "F09": front_F09, "F10": front_F10, "S01": run_S01, "S03": run_S03}


def main(argv):
    out = {k: RUNS[k]() for k in (argv or RUNS)}
    print(json.dumps(out, indent=1))
    if not argv:
        (HERE / "measurements_side.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
