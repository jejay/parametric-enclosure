"""Fit an upright cylinder (the puck base of a Tonie) standing on the rectified Toniebox top.

Usage:
  python -I puck3d.py IMG RECT.json OVERLAY.png [--left x0,x1,y0,y1] [--right x0,x1,y0,y1]
         [--bottom x0,x1,y0,y1] [--top x0,x1,y0,y1] [--height 15] [--fit-height] [--level 125]

  RECT.json   output of rectify_top.py --save (contains the plane homography H, mm -> px)
  --left      image box in which the left silhouette of the puck is searched (rows scanned left -> right)
  --right     box for the right silhouette (rows scanned right -> left)
  --bottom    box for the lower silhouette = front arc of the footprint (columns scanned bottom -> top)
  --top       box for the upper silhouette = back arc of the top face (columns scanned top -> bottom)

The camera is recovered from H (square pixels, principal point at the picture centre): H = K [r1 r2 t].
The cylinder silhouette is the convex hull of the projected bottom and top circles; centre, radius
(and optionally height) are fitted so that the hull passes through the silhouette points.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from PIL import ImageDraw
from scipy.optimize import least_squares
from scipy.spatial import ConvexHull

import mcommon as mc


def arg(name, default=None):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


def box(name):
    v = arg(name)
    return None if v is None else [int(float(t)) for t in v.split(",")]


def decompose(H, w, h, f_fixed=None, pp=None):
    """K (focal length), rotation columns r1, r2, up-vector and translation from a plane homography."""
    u0, v0 = (w / 2.0, h / 2.0) if pp is None else pp
    T = np.array([[1, 0, -u0], [0, 1, -v0], [0, 0, 1.0]])
    Hn = T @ H
    h1, h2 = Hn[:, 0], Hn[:, 1]
    cands = []
    den1 = h1[2] * h2[2]
    if abs(den1) > 1e-12:
        cands.append(-(h1[0] * h2[0] + h1[1] * h2[1]) / den1)
    den2 = h1[2] ** 2 - h2[2] ** 2
    if abs(den2) > 1e-12:
        cands.append((h2[0] ** 2 + h2[1] ** 2 - h1[0] ** 2 - h1[1] ** 2) / den2)
    f2s = [c for c in cands if c > 0]

    def build(f):
        Ki = np.diag([1 / f, 1 / f, 1.0])
        a1, a2, a3 = Ki @ h1, Ki @ h2, Ki @ Hn[:, 2]
        lam = 0.5 * (np.linalg.norm(a1) + np.linalg.norm(a2))
        r1, r2, t = a1 / lam, a2 / lam, a3 / lam
        if t[2] < 0:                      # the plane must be in front of the camera
            r1, r2, t = -r1, -r2, -t
        # orthonormalise r1, r2
        u, _, vt = np.linalg.svd(np.column_stack([r1, r2]), full_matrices=False)
        r12 = u @ vt
        r1, r2 = r12[:, 0], r12[:, 1]
        n = np.cross(r1, r2)
        if n @ (-t) < 0:                  # "up" = the side of the plane on which the camera is
            n = -n
        return r1, r2, n, t

    def ortho_err(f):
        Ki = np.diag([1 / f, 1 / f, 1.0])
        a1, a2 = Ki @ h1, Ki @ h2
        return abs(a1 @ a2) / (np.linalg.norm(a1) * np.linalg.norm(a2)) + abs(np.linalg.norm(a1) - np.linalg.norm(a2)) / np.linalg.norm(a1)

    # best focal length: minimise the orthonormality error on a log grid around the candidates
    grid = np.exp(np.linspace(np.log(0.3 * max(w, h)), np.log(40 * max(w, h)), 4000))
    errs = np.array([ortho_err(f) for f in grid])
    f = float(grid[int(np.argmin(errs))]) if f_fixed is None else float(f_fixed)
    r1, r2, n, t = build(f)
    return f, r1, r2, n, t, [float(np.sqrt(c)) for c in f2s], float(ortho_err(f))


def main():
    path, rect_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    rect = json.load(open(rect_path, encoding="utf-8"))
    H = np.array(rect["H_plane_mm_to_image_px"])
    a = mc.load_rgba(path)
    r, g, b, al, sat, lum = mc.channels(a)
    hh, ww = al.shape
    # "value" (max channel) separates the black puck from white plastic *and* from coloured light
    lum = np.maximum(np.maximum(r, g), b)
    level = float(arg("--level", "140"))
    bright = float(arg("--bright", "175"))
    f_override = arg("--focal")
    pp_arg = arg("--pp")
    pp = None if pp_arg is None else tuple(float(v) for v in pp_arg.split(","))
    f, r1, r2, n, t, f_cands, oerr = decompose(H, ww, hh, None if f_override is None else float(f_override), pp)
    u0, v0 = (ww / 2.0, hh / 2.0) if pp is None else pp

    def project(P):
        P = np.atleast_2d(P)
        c = P[:, 0:1] * r1 + P[:, 1:2] * r2 + P[:, 2:3] * n + t
        return np.column_stack([f * c[:, 0] / c[:, 2] + u0, f * c[:, 1] / c[:, 2] + v0])

    # ---------- silhouette points
    def edge_rows(bx, from_left):
        pts = []
        x0, x1, y0, y1 = bx
        for y in range(y0, y1 + 1):
            prof = lum[y, x0:x1 + 1]
            if not from_left:
                prof = prof[::-1]
            idx = np.nonzero(prof < level)[0]
            if len(idx) == 0 or idx[0] < 3:
                continue
            i = idx[0]
            if prof[max(i - 6, 0):i - 1].mean() < bright:      # must be bright before the edge
                continue
            tt = (i - 1) + (prof[i - 1] - level) / (prof[i - 1] - prof[i])
            x = x0 + tt if from_left else x1 - tt
            pts.append((x, float(y)))
        return pts

    def edge_cols(bx, from_bottom):
        pts = []
        x0, x1, y0, y1 = bx
        for x in range(x0, x1 + 1):
            prof = lum[y0:y1 + 1, x]
            if from_bottom:
                prof = prof[::-1]
            idx = np.nonzero(prof < level)[0]
            if len(idx) == 0 or idx[0] < 3:
                continue
            i = idx[0]
            if prof[max(i - 6, 0):i - 1].mean() < bright:
                continue
            tt = (i - 1) + (prof[i - 1] - level) / (prof[i - 1] - prof[i])
            y = y1 - tt if from_bottom else y0 + tt
            pts.append((float(x), y))
        return pts

    groups = {}
    if box("--left"):
        groups["left"] = edge_rows(box("--left"), True)
    if box("--right"):
        groups["right"] = edge_rows(box("--right"), False)
    if box("--bottom"):
        groups["bottom"] = edge_cols(box("--bottom"), True)
    if box("--top"):
        groups["top"] = edge_cols(box("--top"), False)
    if "--dump" in sys.argv:
        for k, pts in groups.items():
            print(k, " ".join(f"({x:.1f},{y:.0f})" for x, y in pts[:: max(len(pts) // 25, 1)]))
    obs = np.array([p for k in groups for p in groups[k]], float)
    if len(obs) < 10:
        raise SystemExit("too few silhouette points")

    hp0 = float(arg("--height", "15"))
    fit_h = "--fit-height" in sys.argv
    ang = np.linspace(0, 2 * np.pi, 240, endpoint=False)

    def hull_pts(cx, cy, rad, hp):
        ring = np.column_stack([cx + rad * np.cos(ang), cy + rad * np.sin(ang)])
        P = np.vstack([np.column_stack([ring, np.zeros(len(ang))]), np.column_stack([ring, np.full(len(ang), hp)])])
        q = project(P)
        hull = ConvexHull(q)
        return q[hull.vertices]

    def dist_to_poly(pts, poly):
        # signed distance to a convex polygon (positive outside)
        d_best = np.full(len(pts), np.inf)
        inside = np.ones(len(pts), bool)
        m = len(poly)
        ctr = poly.mean(axis=0)
        for i in range(m):
            p0, p1 = poly[i], poly[(i + 1) % m]
            e = p1 - p0
            L = np.hypot(*e)
            if L < 1e-9:
                continue
            nrm = np.array([e[1], -e[0]]) / L
            if nrm @ (ctr - p0) > 0:
                nrm = -nrm                                    # outward normal
            rel = pts - p0
            s = np.clip((rel @ e) / (L * L), 0, 1)
            proj = p0 + s[:, None] * e
            d = np.hypot(*(pts - proj).T)
            d_best = np.minimum(d_best, d)
            inside &= (rel @ nrm) <= 0
        return np.where(inside, -d_best, d_best)

    # start: centre = plane point under the mean of the left/right extremes and the bottom
    Hi = np.linalg.inv(H)
    guess_img = np.array([np.mean(obs[:, 0]), np.mean(obs[:, 1])])
    g0 = np.column_stack([guess_img[None, :], [[1.0]]]) @ Hi.T
    g0 = (g0[:, :2] / g0[:, 2:3])[0]

    def resid(p):
        cx, cy, rad = p[:3]
        hp = p[3] if fit_h else hp0
        return dist_to_poly(obs, hull_pts(cx, cy, abs(rad), abs(hp)))

    best = None
    for r0 in (18.0, 22.0, 26.0):
        p0 = [g0[0], g0[1], r0] + ([hp0] if fit_h else [])
        sol = least_squares(resid, p0, loss="soft_l1", f_scale=1.0, max_nfev=300)
        if best is None or sol.cost < best.cost:
            best = sol
    sol = best
    cx, cy, rad = sol.x[:3]
    hp = abs(sol.x[3]) if fit_h else hp0
    rs = resid(sol.x)
    c0 = project([[cx, cy, 0.0]])[0]
    cam_dist = float(np.linalg.norm(cx * r1 + cy * r2 + t))
    elev = float(np.degrees(np.arcsin(abs((cx * r1 + cy * r2 + t) @ n) / cam_dist)))
    res = {
        "image": os.path.basename(path),
        "focal_length_px": round(f, 1),
        "focal_candidates_px": [round(v, 1) for v in f_cands],
        "orthonormality_error": round(oerr, 5),
        "camera_distance_to_puck_mm": round(cam_dist, 1),
        "view_elevation_deg": round(elev, 2),
        "n_points": {k: len(v) for k, v in groups.items()},
        "puck_diameter_mm": round(2 * abs(float(rad)), 2),
        "puck_height_mm": round(float(hp), 2),
        "puck_height_fitted": fit_h,
        "puck_centre_plane_mm": [round(float(cx), 2), round(float(cy), 2)],
        "fit_rms_px": round(float(np.sqrt(np.mean(rs ** 2))), 3),
        "fit_rms_mm_at_puck": round(float(np.sqrt(np.mean(rs ** 2))) / rect["local_scale_px_per_mm_at_ring_centre"], 3),
    }
    # optional: height of an image point, assuming it lies in the vertical plane through the cylinder
    # axis that faces the camera (i.e. the point is neither in front of nor behind the axis)
    tp = arg("--top-point")
    if tp is not None:
        px_, py_ = (float(v) for v in tp.split(","))
        ray = np.array([(px_ - u0) / f, (py_ - v0) / f, 1.0])          # camera frame
        C = cx * r1 + cy * r2 + t                                         # axis foot point in camera frame
        horiz = C - (C @ n) * n                                           # horizontal part of the view direction
        horiz /= np.linalg.norm(horiz)
        lam = (C @ horiz) / (ray @ horiz)                                 # ray hits the plane (X - C).horiz = 0
        X = lam * ray
        res["top_point_height_mm"] = round(float((X - C) @ n), 2)
        lat = np.cross(n, horiz)
        res["top_point_lateral_offset_mm"] = round(float((X - C) @ lat), 2)
        res["top_point_height_per_mm_depth_offset"] = round(float(np.tan(np.radians(elev))), 3)
    print(json.dumps(res, indent=1))

    im = mc.overlay_base(a)
    d = ImageDraw.Draw(im)
    poly = hull_pts(cx, cy, abs(rad), hp)
    d.line([tuple(p) for p in poly] + [tuple(poly[0])], fill=(255, 0, 255), width=1)
    ringb = project(np.column_stack([cx + abs(rad) * np.cos(ang), cy + abs(rad) * np.sin(ang), np.zeros(len(ang))]))
    d.line([tuple(p) for p in ringb] + [tuple(ringb[0])], fill=(0, 255, 255), width=1)
    cols = {"left": (0, 255, 0), "right": (255, 128, 0), "bottom": (255, 255, 0), "top": (0, 128, 255)}
    for k, pts in groups.items():
        for x, y in pts:
            d.point((x, y), fill=cols[k])
    mc.draw_cross(d, c0[0], c0[1], (255, 0, 255), 5, 1)
    im.save(out)


if __name__ == "__main__":
    main()
