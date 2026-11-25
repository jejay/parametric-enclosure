---
id: dSbTDXw=
type: implementation
parents:
- Uo4_DaQ=
- KbN4vVQ=
- gmeAXTo=
- oxd_4KY=
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
  symbol: _hinge_towers
- path: src/poketonieengagementhunt/parts_core.py
  symbol: yoke_pin
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

params.py holds the two pilot diameters of the M2 screws, the hole and the lengths of the heat-set inserts, the room for their heads, the lengths of screws and pins, the two bores of the hinge pins, the blind holes of the sleeve, thickness and knuckle radius of the hinge towers, the pin under the spring's leg with the width and thickness of its feet, and the relief in the lid. parts_base.py and parts_core.py cut the pilot holes with their lead-ins into the grass top, the pivot boss of the stage and the baffle of the chassis. parts_core.py gives each hinge tower a knuckle that is a closed ring with a roof at 45°, added after tower, foot and buttress have been trimmed to the dome of the stage, makes each foot thicker than its tower towards the middle of the hinge, with a slope of 45° above the added thickness, and cuts the sliding bores and the holes for the pin under the spring's leg, 2.05 mm in the thickness of the towers and 2.3 mm in what the feet are thicker. It also builds that pin, the printed pivot washer, the spring sleeve with a blind hole and a funnel at each end, and two test pieces, one for the pilot holes and one for the two fits of the hinge pins. parts_shell.py gives the ribs of the lid their running bores, relieves the lid wall beside the knuckles and cuts the insert holes of the bowl; a test boss with both of these holes is a third extra print. assembly.py places screws, washer and pins, the hinge pins either mounted or waiting and the spring's forward leg either on its pin or on the rim of the lid, and names the test pieces as extra prints, which export.py writes beside the parts. The sleeve is written once for each hole of SLEEVE_HOLES in parts_core.py, 1.85, 1.90, 1.95, 2.00 and 2.05 mm, and once thicker, 4.5 mm outside. sleeve_file() gives each of these files a name that carries outside diameter and hole, and export_name() in assembly.py gives such a name to the sleeve of the model as well, which was sleeve.stl before. The tighter holes came first, on the agent's assumption that the sleeve the owner found too loose was the model's with 1.95 mm; it was the sleeve of revision 6, a pipe with a through hole of 2.30 mm that rode on pins which the towers gripped. Printed on the owner's printer, the tighter sleeves took no pin, so 2.00 and 2.05 mm followed. The hole that is known to grip on that printer is the level one of 2.05 mm in the feet of the stage. The sleeves beside the model's are exported standing on the bed like the printed parts; the first file of a tighter sleeve was not, and the sleeve the owner printed from it alone came out half a millimetre thin with closed holes, most likely from heat. manual_text.py lists the sleeve files in the table of printed parts and says in the section on printing that the hole has to be found by trying, and how.

checks.py, sections Small screws and Pins, confirms: every M2 screw has 4 mm of thread beyond the lead-in, in a hole of the diameter that belongs to its position in the print, and blind holes are deeper than the screws; the heat-set inserts have wall enough round their holes, room under them and thread for their screws; the printed washer overlaps the bore of the pawl and clears pawl and servo arm; the long arm of a 1.5 mm hex key reaches the two screws of the speaker clamp and its short arm can swing; the stage is solid for 1.2 mm all round the bore of each tower, and the knuckles keep 0.79 mm from the lid at every angle tried; each hinge pin slides in 2.0 mm of tower, carries a whole rib and stands on the floor of its hole in the sleeve, 1.35 mm of it a press fit; the sleeve cannot leave the gap between the ribs, so a pin has to be pulled out of it to come free; the lid's wall closes the hinge axis, which is why there are two pins; the waiting pins clear the lid by 0.32 mm and 1.3 mm of wall remain; the lid slides onto the hinge from behind; a screwdriver blade reaches the waiting pins, and plier jaws of 4 x 3 mm reach the pins from where pressing begins; the spring's forward leg can be lifted from the rim of the lid to 8° above its seat, which leaves 1.7 mm for the pin to pass under it, and the pin has a free way in from the side; each foot has 4.3 mm² of plastic before the hole and 3.7 mm² behind it in the plane through its axis, measured on the solid, is solid for 1.2 mm all round the hole, and keeps 1.66 mm from the lid as drawn, 1.02 mm from a lid that is grown by 0.2 mm and uses all the room of its hinge at once, askew and moved across its pins, and 0.75 mm when the feet are 0.2 mm fat as well; the pivot screw of the ring pawl has thread and hole depth like that of the latch pawl, and an M3 washer wider than the bore of the pawl lies under its M2 washer.

manual_text.py describes these steps (2, 6, 9 and 10), names screws and pins in the list of parts, has the test pieces printed first and the pin under the spring's leg tried in the level hole of its size, and warns against forcing that pin into a foot.

Bounds: geometry only. How the pilot holes, the bores and the blind holes come out of the owner's printer, how firmly a formed M2 thread holds, how firmly a pin holds in the sleeve or in the feet of the towers, and the force the pliers need are not established; the test pieces are there to find out. Lid, stage and band of revision six have been printed, and a stage of revision eight: the first print showed that its towers did not enclose the pins, the second that a foot of 4.3 x 2.0 mm splits through the hole of its pin. The feet as they are now have not been printed. The owner has since built latch and ring lock of revision eight (report of 2026-11-25): the latch pawl works really well, held by an M2 x 6 screw and a standard M2 steel washer in place of the printed washer, with a 4 x 15 mm compression spring cut to 12 mm. By the drawn sizes that washer is narrower than the bore of the pawl and the screw reaches 0.6 mm beyond its hole; what carries the pawl there, by the drawing the hook of the lid and the spring, was not examined. The two pilot diameters rest on one source.
