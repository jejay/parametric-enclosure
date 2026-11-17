"""Scan the assumed principal point for puck3d.py and tabulate the results.

Usage: python -I pp_scan.py PUCK3D.py IMG RECT.json "u0 list" "v0 list" -- [puck3d args]
"""
import json, subprocess, sys
script, img, rect = sys.argv[1], sys.argv[2], sys.argv[3]
us = [float(v) for v in sys.argv[4].split()]
vs = [float(v) for v in sys.argv[5].split()]
extra = sys.argv[sys.argv.index("--") + 1:]
print("u0     v0     f_px   ortho   elev   dist   D_mm   rms_px")
for v0 in vs:
    for u0 in us:
        out = subprocess.run([sys.executable, "-I", "-B", script, img, rect, "NUL.png", "--pp", f"{u0},{v0}"] + extra,
                             capture_output=True, text=True)
        try:
            d = json.loads(out.stdout[out.stdout.index("{"):])
            print(f"{u0:6.0f} {v0:6.0f} {d['focal_length_px']:6.0f} {d['orthonormality_error']:7.3f} {d['view_elevation_deg']:6.1f} "
                  f"{d['camera_distance_to_puck_mm']:6.0f} {d['puck_diameter_mm']:6.2f} {d['fit_rms_px']:6.2f}")
        except Exception as e:  # noqa: BLE001
            print(u0, v0, "ERR", (out.stderr or out.stdout)[-200:])
