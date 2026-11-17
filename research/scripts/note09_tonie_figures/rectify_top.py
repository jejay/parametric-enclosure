"""Metric rectification of the Toniebox 2 top face in an oblique picture, and the size of the
puck base of a Tonie standing on it.

Usage:
  python -I rectify_top.py IMG MODEL.json OVERLAY.png --corners "x1,y1 x2,y2 x3,y3 x4,y4"
         --rim red|yellow|blue --puck "cx,cy" [--puck-d 45] [--ring lit|all|none] [--arc a0:a1]

  --corners  rough image positions of the four virtual corners of the white panel's bounding square,
             going round the panel (any start corner, either sense); only a starting value.
  --puck     rough image position of the centre of the puck's footprint.
  --arc      range of plane angles (deg, model frame) of the footprint arc that is visible; default: auto.

Method: the white panel outline (shape taken from the top view, MODEL.json) and the light ring are
located in the picture; a plane homography H (8 parameters) is fitted so that these points fall on
the model curves. The visible front arc of the puck footprint is then mapped into the plane with
H^-1 and fitted with a circle. No camera intrinsics are needed; perspective is handled exactly for
everything that lies in the top plane.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from PIL import ImageDraw
from scipy.optimize import least_squares

import mcommon as mc


def arg(name, default=None):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    if default is None:
        raise SystemExit(f"missing {name}")
    return default


def homography_from_points(src, dst):
    A = []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y, -v])
    _, _, vt = np.linalg.svd(np.array(A, float))
    H = vt[-1].reshape(3, 3)
    return H / H[2, 2]


def apply(H, pts):
    pts = np.atleast_2d(pts)
    q = np.column_stack([pts, np.ones(len(pts))]) @ H.T
    return q[:, :2] / q[:, 2:3]


def bilinear(arr, x, y):
    h, w = arr.shape
    x = np.clip(x, 0, w - 1.001)
    y = np.clip(y, 0, h - 1.001)
    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)
    fx, fy = x - x0, y - y0
    return (arr[y0, x0] * (1 - fx) * (1 - fy) + arr[y0, x0 + 1] * fx * (1 - fy)
            + arr[y0 + 1, x0] * (1 - fx) * fy + arr[y0 + 1, x0 + 1] * fx * fy)


def main():
    path, model_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    model = json.load(open(model_path, encoding="utf-8"))
    ang_m = np.radians(np.array(model["panel_angles_deg"]))
    rad_m = np.array([np.nan if v is None else v for v in model["panel_radius_mm"]], float)
    ring_c = np.array(model["ring_centre_mm"])
    r_in, r_out = model["ring_inner_radius_mm"], model["ring_outer_radius_mm"]
    r_mid = 0.5 * (r_in + r_out)
    half = 0.5 * model["panel_width_mm"]

    def r_panel(theta):
        return np.interp(np.mod(theta, 2 * np.pi), ang_m, rad_m, period=2 * np.pi)

    a = mc.load_rgba(path)
    r, g, b, al, sat, lum = mc.channels(a)
    h, w = al.shape
    rim = arg("--rim", "red")
    if rim == "red":
        rimness = np.clip((r - np.maximum(g, b)) / 255.0, 0, 1)        # red rim: r >> g,b
    elif rim == "yellow":
        rimness = np.clip((np.minimum(r, g) - b) / 255.0, 0, 1)        # yellow rim: r,g >> b
    else:
        rimness = np.clip((b - r) / 255.0, 0, 1)                        # blue rim
    whiteness = (lum / 255.0) * (1 - np.clip(sat * 3, 0, 1))
    # where "white inside" is tested, in px inside the edge; video footage needs 5:16 (soft seam line)
    in_a, in_b = (int(round(2 * float(v))) for v in arg("--inside-px", "1:7").split(":"))
    white_min = float(arg("--white-min", "0.55"))
    rim_min = float(arg("--rim-min", "0.35"))
    glow_min = float(arg("--glow-min", "0.22"))
    ring_hue = arg("--ring-hue", "any")
    if ring_hue == "green":
        glow_img = np.clip((g - np.maximum(r, b)) / 255.0, 0, 1) * 2.0
    else:
        glow_img = np.where(lum > 120, sat, 0.0)

    corners_img = np.array([[float(v) for v in p.split(",")] for p in arg("--corners").split()])
    sq = np.array([[-half, half], [half, half], [half, -half], [-half, -half]])
    use_ring = arg("--ring", "lit")

    def collect(H, search, ring_mode):
        """Locate panel-outline and ring points near their predicted positions."""
        pan_pts, ring_pts = [], []
        # profile is sampled every 0.5 px from 17 px inside the search window to 8 px outside it,
        # so that the "white inside / rim outside" test always has its full support
        ts = np.arange(-(search + 17.0), search + 8.0 + 1e-9, 0.5)
        for th in np.radians(np.arange(0, 360, 1.0)):
            rp = r_panel(th)
            if np.isnan(rp):
                continue
            d = np.array([np.cos(th), np.sin(th)])
            p0 = apply(H, rp * d)[0]
            p1 = apply(H, (rp + 1.0) * d)[0]
            n = p1 - p0
            ln = np.hypot(*n)
            if ln < 1e-6:
                continue
            n /= ln                                   # image direction of "outwards", per mm: ln px
            xs, ys = p0[0] + ts * n[0], p0[1] + ts * n[1]
            if xs.min() < 2 or ys.min() < 2 or xs.max() > w - 3 or ys.max() > h - 3:
                continue
            prof = bilinear(rimness, xs, ys)
            wh = bilinear(whiteness, xs, ys)
            if "--debug" in sys.argv and abs(np.degrees(th) % 90 - 45) > 44.4 and search > 30:
                print("DBG th", round(float(np.degrees(th))), "p0", np.round(p0, 1), "n", np.round(n, 2), "ln", round(float(ln), 2),
                      "prof", " ".join(f"{v:.2f}" for v in prof[::12]), "| wh", " ".join(f"{v:.2f}" for v in wh[::12]), file=sys.stderr)
            # crossing of rimness 0.25 with white inside and rim outside
            best = None
            for i in range(3, len(ts) - 3):
                if abs(ts[i]) > search:
                    continue
                if prof[i - 1] < 0.25 <= prof[i]:
                    inside = wh[max(i - in_b, 0): max(i - in_a, 1)]   # window inside the edge (0.5 px samples)
                    outside = prof[i + 2: i + 14]
                    if len(inside) > 4 and len(outside) > 4 and inside.mean() > white_min and outside.mean() > rim_min:
                        t = ts[i - 1] + (0.25 - prof[i - 1]) / (prof[i] - prof[i - 1]) * (ts[i] - ts[i - 1])
                        if best is None or abs(t) < abs(best):
                            best = t
            if best is not None:
                pan_pts.append((p0[0] + best * n[0], p0[1] + best * n[1]))
        if ring_mode != "none":
            for ph in np.radians(np.arange(0, 360, 1.5)):
                d = np.array([np.cos(ph), np.sin(ph)])
                p0 = apply(H, ring_c + r_mid * d)[0]
                p1 = apply(H, ring_c + (r_mid + 1.0) * d)[0]
                n = p1 - p0
                ln = np.hypot(*n)                     # px per mm along the radial direction
                if ln < 1e-6:
                    continue
                n /= ln
                half_mm = min(6.0, search / max(ln, 1e-6) + 2.0)
                tr = np.linspace(-half_mm * ln, half_mm * ln, 161)
                xs, ys = p0[0] + tr * n[0], p0[1] + tr * n[1]
                if xs.min() < 2 or ys.min() < 2 or xs.max() > w - 3 or ys.max() > h - 3:
                    continue
                lm = bilinear(lum, xs, ys)
                glow = bilinear(glow_img, xs, ys)     # coloured light on a bright surface
                i = int(np.argmax(glow))
                if glow[i] < glow_min or i < 8 or i > len(tr) - 9:
                    continue
                # window of +-2.6 mm around the maximum; reject if a dark object (puck, ear) is inside it
                win = np.abs(tr - tr[i]) <= 2.6 * ln
                if lm[win].min() < 95:
                    continue
                base = min(glow[win][0], glow[win][-1])
                wgt = np.clip(glow[win] - base, 0, None)
                if wgt.sum() <= 0:
                    continue
                t = float((wgt * tr[win]).sum() / wgt.sum())
                ring_pts.append((p0[0] + t * n[0], p0[1] + t * n[1]))
        return np.array(pan_pts), np.array(ring_pts)

    def fit(H0, pan, ring):
        def unpack(p):
            return np.append(p, 1.0).reshape(3, 3)

        def resid(p):
            H = unpack(p)
            Hi = np.linalg.inv(H)
            res = []
            if len(pan):
                q = apply(Hi, pan)
                rho = np.hypot(q[:, 0], q[:, 1])
                th = np.arctan2(q[:, 1], q[:, 0])
                res.append(rho - r_panel(th))
            if len(ring):
                q = apply(Hi, ring) - ring_c
                res.append((np.hypot(q[:, 0], q[:, 1]) - r_mid) * 1.0)
            return np.concatenate(res)

        sol = least_squares(resid, (H0 / H0[2, 2]).ravel()[:8], loss="soft_l1", f_scale=0.4, x_scale="jac", max_nfev=400)
        H = unpack(sol.x)
        rs = resid(sol.x)
        return H, rs

    # ---- 1) panel-only fit (the rounded square is 4-fold symmetric, so its orientation is arbitrary here)
    H0 = homography_from_points(sq, corners_img)
    j0 = apply(H0, [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    if np.linalg.det(np.array([j0[1] - j0[0], j0[2] - j0[0]])) < 0:      # corners were given in the other sense
        H0 = homography_from_points(sq, corners_img[::-1])
    search0 = float(arg("--search0", "22"))
    pan, _ = collect(H0, search0, "none")
    if "--debug" in sys.argv or len(pan) < 30:
        print("initial panel points:", len(pan), file=sys.stderr)
        imd = mc.overlay_base(a)
        dd = ImageDraw.Draw(imd)
        thd = np.radians(np.arange(0, 361, 1.0))
        ptsd = apply(H0, np.column_stack([r_panel(thd) * np.cos(thd), r_panel(thd) * np.sin(thd)]))
        dd.line([tuple(p) for p in ptsd], fill=(0, 200, 255), width=2)
        for x, y in corners_img:
            mc.draw_cross(dd, x, y, (255, 0, 0), 12, 3)
        for x, y in pan:
            dd.ellipse([x - 2, y - 2, x + 2, y + 2], outline=(255, 0, 255))
        imd.save(out.replace(".png", "_init.png"))
        if len(pan) < 30:
            raise SystemExit("too few panel points for the first fit; see *_init.png")
    H, rs = fit(H0, pan, np.zeros((0, 2)))
    for search in (search0 * 0.6, search0 * 0.35, 6, 4):
        pan, _ = collect(H, search, "none")
        H, rs = fit(H, pan, np.zeros((0, 2)))
    rms_pan = float(np.sqrt(np.mean(rs ** 2)))

    # ---- 2) orientation: the ring is 6.5 mm off-centre; pick the rotation whose predicted ring meets the glow
    best = None
    for rot in range(4):
        c, s_ = np.cos(rot * np.pi / 2), np.sin(rot * np.pi / 2)
        Rm = np.array([[c, -s_, 0], [s_, c, 0], [0, 0, 1.0]])
        Hk = H @ Rm
        _, ring = collect(Hk, 8, "lit")
        if len(ring) == 0:
            cand = (1e9, rot, Hk, ring, float("nan"))
        else:
            q = apply(np.linalg.inv(Hk), ring) - ring_c
            rr_ = np.hypot(q[:, 0], q[:, 1]) - r_mid
            rms_ring = float(np.sqrt(np.mean(rr_ ** 2)))
            cand = (rms_ring - 0.02 * len(ring), rot, Hk, ring, rms_ring)
        if best is None or cand[0] < best[0]:
            best = cand
    _, rot, H, ring, rms_ring = best
    flip = False
    det = 1.0
    ring_bias = float("nan")
    if len(ring):
        q = apply(np.linalg.inv(H), ring) - ring_c
        ring_bias = float(np.mean(np.hypot(q[:, 0], q[:, 1]) - r_mid))
    if use_ring == "refine" and len(ring) > 10:
        H, rs2 = fit(H, apply(H, apply(np.linalg.inv(H), pan)), ring)   # joint refinement
    Hi = np.linalg.inv(H)

    # ---------- puck footprint: dark -> bright transition along rays from the footprint centre
    pc_img = np.array([float(v) for v in arg("--puck", "0,0").split(",")])
    skip_foot = "--puck" not in sys.argv
    pc = apply(Hi, pc_img)[0]
    d_guess = float(arg("--puck-d", "45"))
    rad_p = d_guess / 2
    arc = arg("--arc", "auto")
    fb = arg("--foot-box", "none")
    foot_box = None if fb == "none" else [float(v) for v in fb.split(",")]
    foot = []
    front_half_angle = float(arg("--front-half-angle", "78"))
    for it in range(0 if skip_foot else 4):
        foot = []
        # plane direction that points "down" in the picture at the footprint centre = towards the camera
        c0 = apply(H, pc)[0]
        J = np.column_stack([apply(H, pc + [1.0, 0.0])[0] - c0, apply(H, pc + [0.0, 1.0])[0] - c0])
        u = np.linalg.solve(J, np.array([0.0, 1.0]))
        phi_cam = float(np.degrees(np.arctan2(u[1], u[0])))
        for ph in np.radians(np.arange(0, 360, 1.0)):
            d = np.array([np.cos(ph), np.sin(ph)])
            p0 = apply(H, pc + rad_p * d)[0]
            p1 = apply(H, pc + (rad_p + 1.0) * d)[0]
            n = p1 - p0
            ln = np.hypot(*n)
            if ln < 1e-6:
                continue
            n /= ln
            tr = np.linspace(-9 * ln, 9 * ln, 145)
            xs, ys = p0[0] + tr * n[0], p0[1] + tr * n[1]
            if xs.min() < 2 or ys.min() < 2 or xs.max() > w - 3 or ys.max() > h - 3:
                continue
            lm = bilinear(lum, xs, ys)
            st = bilinear(sat, xs, ys)
            # inside (t<0) must be dark, outside (t>0) bright (white panel or lit ring)
            i_in = lm[:30].mean()
            i_out = lm[-30:].mean()
            if i_in > 110 or i_out < 150:
                continue
            level = 0.5 * (i_in + i_out)
            below = np.nonzero(lm < level)[0]
            if len(below) == 0:
                continue
            i = int(below[-1])                       # outermost dark sample: beyond it everything is bright
            if i < 20 or i > len(tr) - 6:
                continue
            t = tr[i] + (level - lm[i]) / (lm[i + 1] - lm[i]) * (tr[i + 1] - tr[i])
            # only the arc facing the camera is the footprint; elsewhere the silhouette is the puck's side wall
            dphi = (np.degrees(ph) - phi_cam + 180.0) % 360.0 - 180.0
            if abs(dphi) > front_half_angle:
                continue
            fx_, fy_ = p0[0] + t * n[0], p0[1] + t * n[1]
            if foot_box is not None and not (foot_box[0] <= fx_ <= foot_box[2] and foot_box[1] <= fy_ <= foot_box[3]):
                continue
            foot.append((fx_, fy_, np.degrees(ph)))
        if len(foot) < 12:
            break
        fa = np.array(foot)
        if arc != "auto":
            a0, a1 = (float(v) for v in arc.split(":"))
            angs = np.mod(fa[:, 2] - a0, 360)
            fa = fa[angs <= np.mod(a1 - a0, 360)]
        q = apply(Hi, fa[:, :2])
        cxp, cyp, rp = mc.fit_circle(q[:, 0], q[:, 1])
        rr_ = np.hypot(q[:, 0] - cxp, q[:, 1] - cyp) - rp
        keep = np.abs(rr_) < max(2.5 * np.std(rr_), 0.25)
        if keep.sum() >= 8:
            cxp, cyp, rp = mc.fit_circle(q[keep, 0], q[keep, 1])
            rr_ = (np.hypot(q[:, 0] - cxp, q[:, 1] - cyp) - rp)[keep]
            fa = fa[keep]
        pc = np.array([cxp, cyp])
        rad_p = rp
        foot_used = fa
        foot_rms = float(np.sqrt(np.mean(rr_ ** 2)))

    res = {
        "image": os.path.basename(path),
        "orientation": {"rot": rot, "flip": flip, "det_sign": float(np.sign(det))},
        "n_panel_points": int(len(pan)),
        "n_ring_points": int(len(ring)),
        "rms_panel_mm": round(rms_pan, 3),
        "rms_ring_mm": None if np.isnan(rms_ring) else round(rms_ring, 3),
        "ring_mean_radial_offset_mm": None if np.isnan(ring_bias) else round(ring_bias, 3),
        "local_scale_px_per_mm_at_ring_centre": round(float(np.hypot(*(apply(H, ring_c + [1, 0])[0] - apply(H, ring_c)[0]))), 3),
    }
    if len(foot) >= 12:
        angs = np.sort(np.mod(foot_used[:, 2], 360))
        res.update({
            "puck_footprint_diameter_mm": round(2 * float(rad_p), 2),
            "puck_footprint_centre_mm": [round(float(pc[0]), 2), round(float(pc[1]), 2)],
            "puck_centre_offset_from_ring_centre_mm": [round(float(pc[0] - ring_c[0]), 2), round(float(pc[1] - ring_c[1]), 2)],
            "puck_footprint_points": int(len(foot_used)),
            "puck_footprint_arc_deg": [round(float(angs.min()), 1), round(float(angs.max()), 1)],
            "puck_footprint_fit_rms_mm": round(foot_rms, 3),
        })
    res["H_plane_mm_to_image_px"] = [[float(v) for v in row] for row in H]
    print(json.dumps(res, indent=1))
    hout = arg("--save", "none")
    if hout != "none":
        with open(hout, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=1)

    im = mc.overlay_base(a)
    d = ImageDraw.Draw(im)
    # model curves projected with the fitted H
    th = np.radians(np.arange(0, 361, 1.0))
    pts = apply(H, np.column_stack([r_panel(th) * np.cos(th), r_panel(th) * np.sin(th)]))
    d.line([tuple(p) for p in pts], fill=(0, 200, 255), width=1)
    for rr in (r_in, r_out):
        pts = apply(H, ring_c + rr * np.column_stack([np.cos(th), np.sin(th)]))
        d.line([tuple(p) for p in pts], fill=(255, 220, 0), width=1)
    if len(foot) >= 12:
        pts = apply(H, pc + rad_p * np.column_stack([np.cos(th), np.sin(th)]))
        d.line([tuple(p) for p in pts], fill=(255, 0, 255), width=1)
        for x, y, _ in foot_used:
            d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], outline=(0, 255, 0))
    for x, y in pan:
        d.point((x, y), fill=(255, 0, 0))
    for x, y in ring:
        d.point((x, y), fill=(0, 0, 255))
    im.save(out)


if __name__ == "__main__":
    main()
