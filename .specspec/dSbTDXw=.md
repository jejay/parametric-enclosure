---
id: dSbTDXw=
type: implementation
parents:
- oxd_4KY=
- lsOs9jU=
- gmeAXTo=
sources:
- path: src/poketonieengagementhunt/params.py
- path: src/poketonieengagementhunt/parts_core.py
  symbol: pawl_cap
- path: src/poketonieengagementhunt/parts_core.py
  symbol: m2_coupon
- path: src/poketonieengagementhunt/parts_core.py
  symbol: hinge_pin_span
- path: src/poketonieengagementhunt/parts_shell.py
  symbol: lid
- path: src/poketonieengagementhunt/parts_base.py
  symbol: grass_top
- path: src/poketonieengagementhunt/assembly.py
  symbol: extra_prints
- path: src/poketonieengagementhunt/export.py
- path: src/poketonieengagementhunt/checks.py
  symbol: check_fasteners
- path: src/poketonieengagementhunt/checks.py
  symbol: check_pins
- path: src/poketonieengagementhunt/manual_text.py
---
# Screws, pins and their checks

params.py holds the two pilot diameters of the M2 screws, the hole and the lengths of the heat-set inserts, the room for their heads, the lengths of screws and pins, the positions of the hinge pins and the relief in the lid. parts_base.py and parts_core.py cut the pilot holes with their lead-ins into the grass top, the pivot boss of the stage and the baffle of the chassis, the press bores for the hinge pins into the towers and the bore of the lock pin through the rear wall of the stage. parts_core.py also builds the printed pivot washer, the spring sleeve with a funnel at each end and the test piece for the pilot holes. parts_shell.py gives the ribs of the lid their running bores, relieves the lid wall beside the knuckles and cuts the insert holes of the bowl; a test boss with both of these holes is a second extra print. assembly.py places screws, washer and pins, the hinge pins either mounted or waiting, and names the test piece as an extra print, which export.py writes beside the parts.

checks.py, sections Small screws and Pins, confirms: every M2 screw has 4 mm of thread beyond the lead-in, in a hole of the diameter that belongs to its position in the print, and blind holes are deeper than the screws; the heat-set inserts have wall enough round their holes, room under them and thread for their screws; the printed washer overlaps the bore of the pawl and clears pawl and servo arm; the long arm of a 1.5 mm hex key reaches the two screws of the speaker clamp and its short arm can swing; each hinge pin sits 2.9 mm in its tower, carries a whole rib and reaches the sleeve; the lid's wall closes the hinge axis, which is why there are two pins; the waiting pins clear the lid and 1.3 mm of wall remain; the lid slides onto the hinge from behind; pliers reach the waiting pins from above; the path of the lock pin from behind the stage is free.

manual_text.py describes these steps (2, 6, 9 and 10), names screws and pins in the list of parts and has the test piece printed first.

Bounds: geometry only. How the pilot holes and the press bores come out of the owner's printer, how firmly a formed M2 thread and a pressed pin hold in PETG, and the force the pliers need are not established; the test piece and a trial pin in a tower are there to find out. The two pilot diameters rest on one source.
