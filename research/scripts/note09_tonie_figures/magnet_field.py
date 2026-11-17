"""Axial field component of an axially magnetised cylinder magnet (magnetic surface-charge model).

Usage: python -I magnet_field.py DIAMETER_MM LENGTH_MM BR_TESLA
Prints Bz [mT] at distances z below the lower pole face, on the axis and at lateral offsets.
Pure physics estimate (ideal uniform magnetisation), not a measurement of a Tonie.
"""
import sys

import numpy as np


def bz(rho, z, R, L, Br, n_r=160, n_p=180):
    """Bz at lateral offset rho and distance z below the lower pole face (z > 0)."""
    # two uniformly charged discs: lower face (charge +) at z0 = 0, upper face (charge -) at z0 = -L (above)
    rr = (np.arange(n_r) + 0.5) / n_r * R
    pp = (np.arange(n_p) + 0.5) / n_p * 2 * np.pi
    r, p = np.meshgrid(rr, pp, indexing="ij")
    dA = (R / n_r) * (2 * np.pi / n_p) * r
    xs, ys = r * np.cos(p), r * np.sin(p)
    out = 0.0
    for sign, dz in ((+1.0, z), (-1.0, z + L)):
        d3 = ((rho - xs) ** 2 + ys ** 2 + dz ** 2) ** 1.5
        out += sign * np.sum(dz / d3 * dA)
    return Br / (4 * np.pi) * out


def main():
    D, L, Br = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    R = D / 2
    offs = [0, 3, 5, 8, 10, 12, 15]
    print(f"magnet D={D} mm, L={L} mm, Br={Br} T; Bz in mT (sign: + = same direction as on the axis)")
    print("z[mm] | " + " ".join(f"rho={o:>2d}" for o in offs))
    for z in (1.5, 2, 3, 4, 5, 6, 8, 10, 12, 15):
        print(f"{z:5.1f} | " + " ".join(f"{1000 * bz(o, z, R, L, Br):6.1f}" for o in offs))


if __name__ == "__main__":
    main()
