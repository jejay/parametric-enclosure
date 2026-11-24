---
id: dSbTDXw=
type: implementation
parents:
- oxd_4KY=
- gmeAXTo=
- cSIxfCw=
- BhwFwgI=
sources:
- path: src/poketonieengagementhunt/params.py
- path: src/poketonieengagementhunt/parts_core.py
  symbol: pawl_cap
- path: src/poketonieengagementhunt/parts_core.py
  symbol: m2_coupon
- path: src/poketonieengagementhunt/parts_core.py
  symbol: hinge_pin_span
- path: src/poketonieengagementhunt/parts_core.py
  symbol: tower_knuckle
- path: src/poketonieengagementhunt/parts_core.py
  symbol: yoke_wire
- path: src/poketonieengagementhunt/parts_core.py
  symbol: sleeve
- path: src/poketonieengagementhunt/parts_core.py
  symbol: pin_coupon
- path: src/poketonieengagementhunt/assembly.py
  symbol: spring_rest_deg
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

params.py holds the two pilot diameters of the M2 screws, the hole and the lengths of the heat-set inserts, the room for their heads, the lengths of screws and pins, the two bores of the hinge pins, the blind holes of the sleeve, thickness and knuckle radius of the hinge towers, the wire under the spring's leg and the relief in the lid. parts_base.py and parts_core.py cut the pilot holes with their lead-ins into the grass top, the pivot boss of the stage and the baffle of the chassis, and the bore of the lock pin through the rear wall of the stage. parts_core.py gives each hinge tower a knuckle that is a closed ring with a roof at 45°, added after tower and foot have been trimmed to the dome of the stage, and cuts the sliding bores and the holes for the wire. It also builds the wire, the printed pivot washer, the spring sleeve with a blind hole and a funnel at each end, and two test pieces, one for the pilot holes and one for the two fits of the hinge pins. parts_shell.py gives the ribs of the lid their running bores, relieves the lid wall beside the knuckles and cuts the insert holes of the bowl; a test boss with both of these holes is a third extra print. assembly.py places screws, washer, wire and pins, the hinge pins either mounted or waiting and the spring's forward leg either on its wire or on the rim of the lid, and names the test pieces as extra prints, which export.py writes beside the parts.

checks.py, sections Small screws and Pins, confirms: every M2 screw has 4 mm of thread beyond the lead-in, in a hole of the diameter that belongs to its position in the print, and blind holes are deeper than the screws; the heat-set inserts have wall enough round their holes, room under them and thread for their screws; the printed washer overlaps the bore of the pawl and clears pawl and servo arm; the long arm of a 1.5 mm hex key reaches the two screws of the speaker clamp and its short arm can swing; the stage is solid for 1.6 mm all round the bore of each tower, and the knuckles keep 0.51 mm from the lid at every angle tried; each hinge pin slides in 2.2 mm of tower, carries a whole rib and stands on the floor of its hole in the sleeve, 1.35 mm of it a press fit; the sleeve cannot leave the gap between the ribs, so a pin has to be pulled out of it to come free; the lid's wall closes the hinge axis, which is why there are two pins; the waiting pins clear the lid and 1.3 mm of wall remain; the lid slides onto the hinge from behind; a screwdriver blade reaches the waiting pins, and plier jaws of 4 x 3 mm reach the pins from where pressing begins; the spring's forward leg can be lifted from the rim of the lid to above its seat, and the wire has a free way under it; the path of the lock pin from behind the stage is free.

manual_text.py describes these steps (2, 6, 9 and 10), names screws, pins and wire in the list of parts and has the test pieces printed first.

Bounds: geometry only. How the pilot holes, the bores and the blind holes come out of the owner's printer, how firmly a formed M2 thread holds, how firmly a pin holds in the sleeve, and the force the pliers need are not established; the test pieces are there to find out. Of all this only lid, stage and band of revision six have been printed; that print is what showed that its towers did not enclose the pins. The two pilot diameters rest on one source.
