---
id: eywEEH4=
type: implementation
parents:
- OjSCkp8=
sources:
- path: src/poketonieengagementhunt/schematic.py
- path: docs/img/schematic.svg
- path: docs/electronics.md
---
# Schematic drawn by schematic.py

schematic.py draws one sheet as an SVG: charger and cell, boost converter, controller, amplifier and speaker, servo, LED, the two plugs of the harness, reader and hall switch. Every pad carries its name, the eleven pads that stay empty end in a cross, the nine small pads on the underside of the controller are marked, and the loose parts R1 to R5, C1 to C3 and D1 stand where they are soldered. The parts that only one variant needs, for the AH3661UA hall switch and for waking by card detection, are drawn in two boxes of their own. The command poketonieengagementhunt schematic writes docs/img/schematic.svg and, through resvg, docs/img/schematic.png. docs/electronics.md shows the picture in its section Schematic, with a table of the loose parts and a table of the empty pads and why each is empty.

The review before the drawing covered the pad order of the reader against the schematic of its board and both libraries, the pads of the controller against the variant file of the Arduino core, the legs of both hall switches against their data sheets, pads and resistors of boost converter and amplifier board against Adafruit's design files, and every net against the levels and currents of the data sheets. It led to the pull-downs of 4.7 kOhm and to the capacitor at the input of the boost converter, which the list of small parts had left out.

Bounds: the sheet is laid out by hand. The program only refuses a sheet on which a declared pad ends neither in a wire nor in a cross; that the sheet agrees with the tables of the document was established by reading both side by side and by inspecting the rendering at double size on 2026-11-26. The pads of the charger module and of the LED board are those of the usual boards, not of delivered ones. Nothing electrical has been built or measured.
