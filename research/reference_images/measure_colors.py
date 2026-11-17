"""Median red / black / white of the Poke Ball in each measured reference image.

    uv run python -I research/reference_images/measure_colors.py

Needs measurements_front.json (run measure_front_views.py first) for the ball
circle.  Pixels inside 0.96 R are classified very simply:
    red    R - max(G, B) > 60
    black  max(R, G, B) < 95
    white  min(R, G, B) > 150 and (max - min) < 40
and the median colour of each class is reported (photos and shaded art have
gradients, so the 15th..85th percentile range of the brightness is listed too).
Flat vector files (F07, F13) are read from their SVG source instead.
Writes measurements_colors.json.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("measure_common", HERE / "measure_common.py")
mc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mc)

FILES = {
    "F01": "F01_sugimori_artwork.png",
    "F02": "F02_pokemon_go_item_sprite.png",
    "F03": "F03_letsgo_screenshot.jpg",
    "F05": "F05_twc_pokeball_in_hand.jpg",
    "F06": "F06_twc_mini_pokeball_front.jpg",
    "F08": "F08_commons_pokebola_vector.png",
    "F09": "F09_sketchfab_jmgamedev_basic_pokeball.jpg",
    "F10": "F10_printables_gonzheredia_print_front.jpg",
    "F11": "F11_anime_ep001_pokedex.png",
    "F12": "F12_ssb_wiiu_trophy_render.png",
}


def hexs(c):
    return "#%02X%02X%02X" % tuple(int(round(float(v))) for v in c)


def classify(rgb, cx, cy, R):
    h, w, _ = rgb.shape
    yy, xx = np.mgrid[0:h, 0:w]
    inside = (xx - cx) ** 2 + (yy - cy) ** 2 < (0.96 * R) ** 2
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    classes = {
        "red": inside & (r - np.maximum(g, b) > 60),
        "black": inside & (mx < 95),
        "white": inside & (mn > 150) & (mx - mn < 40),
    }
    out = {}
    for name, m in classes.items():
        n = int(m.sum())
        if n < 30:
            continue
        px = rgb[m]
        med = np.median(px, axis=0)
        lum = 0.299 * px[:, 0] + 0.587 * px[:, 1] + 0.114 * px[:, 2]
        out[name] = dict(median=hexs(med), share_of_ball=round(n / int(inside.sum()), 3),
                         lum_p15_p85=[int(np.percentile(lum, 15)), int(np.percentile(lum, 85))])
    return out


def svg_fills(path):
    txt = path.read_text(encoding="utf-8", errors="replace")
    cols = re.findall(r"fill:\s*(#[0-9A-Fa-f]{3,6}|[a-z]+)", txt)
    seen = []
    for c in cols:
        if c not in seen and c != "none":
            seen.append(c)
    return seen


def main():
    front = {r["name"][:3]: r for r in json.loads((HERE / "measurements_front.json").read_text(encoding="utf-8"))}
    out = {}
    for key, fn in FILES.items():
        rgb, _ = mc.load(HERE / fn)
        m = front[key]
        cx, cy = m["ball_centre"]
        out[key] = dict(name=m["name"], **classify(rgb, cx, cy, m["D_raw_px"] / 2))
    out["F07"] = dict(name="F07 fan vector (Commons 'Poke Ball.svg')", svg_fills=svg_fills(HERE / "F07_commons_pokeball_fan_vector.svg"))
    out["F13"] = dict(name="F13 fan icon (Commons 'Poke Ball icon.svg')", svg_fills=svg_fills(HERE / "F13_commons_pokeball_icon_fan.svg"))
    for k, v in out.items():
        print(k, json.dumps({a: b for a, b in v.items() if a != "name"}))
    (HERE / "measurements_colors.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
