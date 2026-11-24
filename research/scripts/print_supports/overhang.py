"""Where would the exported parts need support?  Every STL is already in print orientation (bed = lowest z)."""
import math, pathlib, sys
import numpy as np
import trimesh

def analyse(path, limit_deg):
    m = trimesh.load(path, force="mesh")
    zmin = m.bounds[0][2]
    n, a, c = m.face_normals, m.area_faces, m.triangles_center
    on_bed = (c[:, 2] < zmin + 0.06) & (n[:, 2] < -0.99)
    sel = (n[:, 2] < -math.cos(math.radians(limit_deg))) & ~on_bed
    idx = np.nonzero(sel)[0]
    if len(idx) == 0:
        return m, []
    pairs = m.face_adjacency
    keep = sel[pairs[:, 0]] & sel[pairs[:, 1]]
    comps = trimesh.graph.connected_components(pairs[keep], nodes=idx, min_len=1)
    out = []
    for comp in comps:
        area = a[comp].sum()
        if area < 12.0:
            continue
        pts = m.triangles[comp].reshape(-1, 3)
        lo, hi = pts.min(axis=0), pts.max(axis=0)
        # width of the region across its narrow direction (principal axes in plan)
        xy = pts[:, :2] - pts[:, :2].mean(axis=0)
        ext = sorted(np.ptp(xy @ np.linalg.eigh(np.cov(xy.T))[1], axis=0)) if len(xy) > 2 else [0, 0]
        cen = (c[comp] * a[comp][:, None]).sum(axis=0) / area
        out.append({"area": area, "z": (lo[2] - zmin, hi[2] - zmin), "short": ext[0], "long": ext[1], "cen": cen, "faces": comp})
    return m, sorted(out, key=lambda r: -r["area"])

def lands_on(m, region):
    """Does a support under this region stand on the bed or on the part?  Vertical rays from a few of its faces."""
    zmin = m.bounds[0][2]
    comp = region["faces"]
    pick = comp[:: max(1, len(comp) // 12)][:12]
    t = m.triangles
    A, B, C = t[:, 0], t[:, 1], t[:, 2]
    v0, v1 = (B - A)[:, :2], (C - A)[:, :2]
    den = v0[:, 0] * v1[:, 1] - v1[:, 0] * v0[:, 1]
    ok = np.abs(den) > 1e-12
    on_model = 0
    for p in m.triangles_center[pick]:
        v2 = p[:2] - A[:, :2]
        with np.errstate(divide="ignore", invalid="ignore"):
            u = (v2[:, 0] * v1[:, 1] - v1[:, 0] * v2[:, 1]) / den
            v = (v0[:, 0] * v2[:, 1] - v2[:, 0] * v0[:, 1]) / den
        inside = ok & (u >= 0) & (v >= 0) & (u + v <= 1)
        z = A[:, 2] + u * (B[:, 2] - A[:, 2]) + v * (C[:, 2] - A[:, 2])
        below = inside & (z < p[2] - 0.05)
        if below.any() and z[below].max() > zmin + 0.1:
            on_model += 1
    return on_model, len(pick)

names = sys.argv[1:] or sorted(p.stem for p in pathlib.Path("export/stl").glob("*.stl"))
for name in names:
    path = pathlib.Path("export/stl") / f"{name}.stl"
    m, r30 = analyse(path, 30.0)
    _, r45 = analyse(path, 45.0)
    size = m.extents
    big30 = [r for r in r30 if r["short"] > 5.0]
    big45 = [r for r in r45 if r["short"] > 5.0]
    print(f"{name:16s} {size[0]:5.1f} x {size[1]:5.1f} x {size[2]:5.1f} mm | flatter than 30 deg: {sum(r['area'] for r in big30):7.0f} mm2 in {len(big30)} regions wider than 5 mm (+{len(r30) - len(big30)} narrow) | flatter than 45 deg: {sum(r['area'] for r in big45):7.0f} mm2 in {len(big45)}")
    for r in big30[:5]:
        on_model, n = lands_on(m, r)
        print(f"      {r['area']:7.0f} mm2, {r['short']:5.1f} x {r['long']:5.1f} mm, {r['z'][0]:5.1f}..{r['z'][1]:5.1f} mm above the bed, at x {r['cen'][0]:6.1f} y {r['cen'][1]:6.1f}; support would stand on the {'part' if on_model > n / 2 else 'bed'} ({on_model}/{n} rays hit the part)")
