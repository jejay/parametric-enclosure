"""Parametric CAD model, verification and building manual of the Poké Ball
engagement-hunt device.

    uv run poketonieengagementhunt check     geometry verification -> docs/verification.md
    uv run poketonieengagementhunt export    STL / STEP files       -> export/
    uv run poketonieengagementhunt manual    renderings + manual    -> docs/
    uv run poketonieengagementhunt all       everything above
    uv run poketonieengagementhunt schematic electronics schematic  -> docs/img/schematic.svg, .png

All dimensions live in ``params.py``.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "schematic":
        from . import schematic

        files = schematic.write(ROOT)
        print("wrote " + ", ".join(f.relative_to(ROOT).as_posix() for f in files))
        raise SystemExit(0)
    if cmd not in {"check", "export", "manual", "all"}:
        print(__doc__)
        raise SystemExit(0 if cmd in {"help", "-h", "--help"} else 2)
    t0 = time.time()
    failed = 0
    if cmd in {"check", "all"}:
        from . import checks

        results = checks.run_all()
        checks.write_report(results, ROOT / "docs")
        failed = sum(not r.ok for r in results)
        print(f"\n{len(results) - failed} of {len(results)} checks pass -> docs/verification.md")
    if cmd in {"export", "all"}:
        from . import export

        files = export.export_all(ROOT)
        print(f"wrote {len(files)} CAD files -> export/")
    if cmd in {"manual", "all"}:
        from . import manual

        files = manual.build_manual(ROOT)
        print(f"wrote {len(files)} manual files -> docs/")
    print(f"done in {time.time() - t0:.0f} s")
    raise SystemExit(1 if failed else 0)
