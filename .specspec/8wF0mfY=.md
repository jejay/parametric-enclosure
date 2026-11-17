---
id: 8wF0mfY=
type: implementation
parents:
- F7C8Of8=
sources:
- path: src/poketonieengagementhunt/geom.py
- path: src/poketonieengagementhunt/components.py
- path: src/poketonieengagementhunt/assembly.py
- path: src/poketonieengagementhunt/export.py
- path: src/poketonieengagementhunt/render.py
- path: src/poketonieengagementhunt/__init__.py
  symbol: main
---
# The CAD package

geom.py wraps the CadQuery operations used everywhere, parts_shell.py, parts_core.py and parts_base.py build the printed parts of ball, core and grass tongue, components.py holds the dummy models of the purchased parts, assembly.py the placement, export.py writes STL files in print orientation, STEP files of every part and component and one coloured assembly, render.py draws shaded pictures with true edges off-screen. The command poketonieengagementhunt runs checks, export and manual.

Bounds: the dummy components are envelopes with a few recognisable features, not detailed models.
