"""Board-coordinate intensity profiles / rectified crops from the top-view photos.

usage: top_profiles.py IMAGE CONFIG OUT_PREFIX
Re-uses the outline corners + pad-gap scale printed by top_generic.py (hard-coded here per config),
builds the plane<->image mapping (pinhole, pp at the image centre, f = 3000 px per 2048 px width)
and writes:
  OUT_PREFIX_rect.png   : metric-rectified board image, 20 px/mm, x right = towards the antenna end,
                          y down = from the pin-1 long edge, with a 5 mm grid
and prints numeric profiles across the antenna traces and the hole bores.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

src, cfgname, outp = sys.argv[1], sys.argv[2], sys.argv[3]
CFG = {
    "e326": dict(C={"TL": (71.87, 282.01), "TR": (1467.87, 281.49), "BL": (74.79, 1051.57), "BR": (1459.64, 1065.08)},
                 roles=dict(HP1="BR", HP13="TR", AP1="BL", AP13="TL"),
                 col=((1413.97, 366.48), (1406.73, 984.80)), pitch_px=51.56),
    "e150": dict(C={"TL": (20.61, 143.63), "TR": (1184.96, 146.14), "BL": (21.3, 781.53), "BR": (1180.38, 790.52)},
                 roles=dict(HP1="TL", HP13="BL", AP1="TR", AP13="BR"),
                 col=((63.18, 209.95), (63.42, 714.01)), pitch_px=42.03),
}[cfgname]
img = Image.open(src).convert("RGB")
A = np.asarray(img).astype(np.float32) / 255.0
Himg, Wimg = A.shape[:2]
f = 3000.0 * Wimg / 2048.0
pp = (Wimg / 2.0, Himg / 2.0)
C = {k: np.array(v, float) for k, v in CFG["C"].items()}
R = {role: C[name] for role, name in CFG["roles"].items()}


def hom(p):
    return np.array([p[0], p[1], 1.0])


def line(p, q):
    return np.cross(hom(p), hom(q))


V1 = np.cross(line(C["TL"], C["TR"]), line(C["BL"], C["BR"]))
V2 = np.cross(line(C["TL"], C["BL"]), line(C["TR"], C["BR"]))
VL = np.cross(V1, V2); VL /= np.linalg.norm(VL[:2])
K = np.array([[f, 0, pp[0]], [0, f, pp[1]], [0, 0, 1.0]])
Kinv = np.linalg.inv(K)
n = K.T @ VL; n /= np.linalg.norm(n)


def back(p):
    d = Kinv @ hom(p)
    return d / np.dot(n, d)


O = back(R["HP1"])
e1 = back(R["AP1"]) - O; e1 /= np.linalg.norm(e1)
e2 = np.cross(n, e1); e2 /= np.linalg.norm(e2)
if np.dot(back(R["HP13"]) - O, e2) < 0:
    e2 = -e2
# scale from the pad column: 12 pitches between the first and last land centre
pa, pb = (np.array(p, float) for p in CFG["col"])
ra = np.array([np.dot(back(pa) - O, e1), np.dot(back(pa) - O, e2)])
rb = np.array([np.dot(back(pb) - O, e1), np.dot(back(pb) - O, e2)])
scale = 30.48 / np.linalg.norm(rb - ra)  # mm per plane unit (land-centre based)


def to_mm(p):
    X = back(p) - O
    return np.array([np.dot(X, e1), np.dot(X, e2)]) * scale


def to_px(xy):
    X = O + (xy[0] * e1 + xy[1] * e2) / scale
    q = K @ X
    return q[:2] / q[2]


L = 0.5 * (np.linalg.norm(to_mm(R["AP1"]) - to_mm(R["HP1"])) + np.linalg.norm(to_mm(R["AP13"]) - to_mm(R["HP13"])))
W = 0.5 * (np.linalg.norm(to_mm(R["HP13"]) - to_mm(R["HP1"])) + np.linalg.norm(to_mm(R["AP13"]) - to_mm(R["AP1"])))
print(f"{cfgname}: L={L:.3f} W={W:.3f} (land-centre scale)")

# rectified image
PPM = 20.0
xs = np.arange(-2, L + 2, 1 / PPM); ys = np.arange(-2, W + 2, 1 / PPM)
XX, YY = np.meshgrid(xs, ys)
Xw = O[None, None, :] + (XX[..., None] * e1 + YY[..., None] * e2) / scale
q = Xw @ K.T
U, Vv = q[..., 0] / q[..., 2], q[..., 1] / q[..., 2]
rect = np.stack([ndi.map_coordinates(A[..., c], [Vv, U], order=1, mode="constant", cval=1.0) for c in range(3)], axis=-1)
np.save(outp + "_rect.npy", rect.astype(np.float32))
ri = Image.fromarray((np.clip(rect, 0, 1) * 255).astype(np.uint8))
dr = ImageDraw.Draw(ri)
for gx in range(0, int(L) + 1, 5):
    px = (gx + 2) * PPM
    dr.line([(px, 0), (px, ri.height)], fill=(255, 255, 0), width=1)
    dr.text((px + 2, 2), str(gx), fill=(255, 255, 0))
for gy in range(0, int(W) + 1, 5):
    py = (gy + 2) * PPM
    dr.line([(0, py), (ri.width, py)], fill=(0, 255, 255), width=1)
    dr.text((2, py + 2), str(gy), fill=(0, 255, 255))
ri.save(outp + "_rect.png")
print("saved", outp + "_rect.png", ri.size, "origin offset 2 mm, 20 px/mm")
