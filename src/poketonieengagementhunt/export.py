"""Write the printable and exchangeable CAD files.

export/stl/<part>.stl        printed parts, already turned into print orientation
export/stl/sleeve_4_0_hole_1_95.stl  the sleeve: its files carry outside diameter and hole in their names, and it is
                             written once for each hole size that is to be tried (assembly.export_name, extra_prints)
export/step/<part>.step      printed parts in assembly coordinates
export/stl/m2_test_coupon.stl  test piece for the M2 pilot holes (not a part of the device)
export/step/components/      dummy models of the purchased components
export/step/assembly.step    the complete, coloured and named assembly
"""

from __future__ import annotations

from pathlib import Path

import cadquery as cq

from . import assembly as A
from . import geom as g
from .checks import to_mesh
from .render import PALETTE


def export_all(root: Path) -> list[Path]:
    written: list[Path] = []
    stl_dir = root / "export" / "stl"
    step_dir = root / "export" / "step"
    comp_dir = step_dir / "components"
    for d in (stl_dir, step_dir, comp_dir):
        d.mkdir(parents=True, exist_ok=True)

    for key, (shape, _filament, _note) in A.printed_parts().items():
        mesh = to_mesh(A.print_oriented(key), *A.MESH.get(key, (0.01, 0.1)))
        p = stl_dir / f"{A.export_name(key)}.stl"
        mesh.export(p)
        written.append(p)
        p = step_dir / f"{A.export_name(key)}.step"
        cq.exporters.export(cq.Workplane(obj=shape), str(p))
        written.append(p)

    # test pieces: not parts of the device, exported as they are modelled
    for key, (shape, _filament, _note) in A.extra_prints().items():
        p = stl_dir / f"{key}.stl"
        to_mesh(shape).export(p)
        written.append(p)
        p = step_dir / f"{key}.step"
        cq.exporters.export(cq.Workplane(obj=shape), str(p))
        written.append(p)

    items = A.build()
    assy = cq.Assembly(name="pokeball")
    for it in items:
        if it.kind != "printed":
            p = comp_dir / f"{it.key}.step"
            cq.exporters.export(cq.Workplane(obj=it.shape()), str(p))
            written.append(p)
        for i, (shape, colour) in enumerate(it.bodies):
            r, gg, b, a = PALETTE.get(colour, (0.6, 0.6, 0.6, 1.0))
            assy.add(shape, name=f"{it.key}_{i}" if len(it.bodies) > 1 else it.key, color=cq.Color(r, gg, b, a))
    p = step_dir / "assembly.step"
    assy.save(str(p))
    written.append(p)
    return written
