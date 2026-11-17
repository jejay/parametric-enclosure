"""Cross-check: position of the silkscreen centre dot relative to the mounting-hole raster in two
other photos (different units), using a 4-point homography from the hole centres.
Hole frame: u from the mid pair line towards the antenna end, v across (0 = raster centre line).
"""
import numpy as np


def homography(src, dst):
    A = []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y, -v])
    _, _, vt = np.linalg.svd(np.array(A, float))
    return vt[-1].reshape(3, 3)


def apply(H, p):
    q = H @ np.array([p[0], p[1], 1.0])
    return q[:2] / q[2]


brd = [(0.0, -17.0), (0.0, 17.0), (37.0, -12.5), (37.0, 12.5)]  # mid_p1side, mid_p13side, ant_p1side, ant_p13side
cases = {
    # oblique photo (kosla docs/images/pn5180.jpg, upright copy): far long edge = pin-1 side
    "kosla oblique": dict(holes=[(773.8, 1934.6), (1353.0, 2445.5), (1418.3, 1655.1), (1829.8, 1947.5)], dot=(1406.5, 1932.0)),
    # ATrappmann PN5180-NFC.png (top view, header left, pin 1 top); eyeballed centres, +-3 px
    "ATrappmann top": dict(holes=[(668.0, 45.0), (665.0, 925.0), (1605.0, 172.0), (1600.0, 805.0)], dot=(1230.5, 490.5)),
}
for name, c in cases.items():
    H = homography(c["holes"], brd)
    d = apply(H, c["dot"])
    print(f"{name}: silk dot at u={d[0]:.2f} mm from the mid-hole line, v={d[1]:+.2f} mm from the raster centre line")
print("reference (two rectified top views): dot u = 22.13 / 22.15, v = +0.0 (loop centre u = 22.9..23.0)")
