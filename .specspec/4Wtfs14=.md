---
id: 4Wtfs14=
type: implementation
parents:
- tTVJcGs=
- uuRV-lo=
sources:
- path: src/poketonieengagementhunt/parts_core.py
  symbol: stage
- path: src/poketonieengagementhunt/parts_core.py
  symbol: _ring_slot_walls
- path: src/poketonieengagementhunt/parts_core.py
  symbol: ring_pawl
- path: src/poketonieengagementhunt/params.py
- path: src/poketonieengagementhunt/assembly.py
  symbol: build
- path: src/poketonieengagementhunt/manual_text.py
- path: src/poketonieengagementhunt/checks.py
  symbol: check_ring_lock
---
# Stage with the slot of the ring, and the ring pawl

parts_core.py: stage() is the inner dome with the flat deck, the collar that centres the lid and the four screw wells. For the ring it fuses the walls and the floor of the slot under the deck, with the two windows for the finger, cuts the slot through deck and walls (ring_slot_void: a round bottom with upright ends above it), cuts the slit of the knob, and adds the pivot boss with its pilot hole, the pad on which the arm rests and the cup of the spring, turned along the way of the tail. ring_pawl() is the pawl: hub, arm, finger with sloped lower edges and a tapered end, the tail with knob, flat and nub for the spring, and the hole of the counterweight pin; ring_pawl_at() turns it and pushes it up against the deck, ring_pawl_pin() is the pin. params.py, section 5, holds the owner's sizes of the slot and the dimensions of the pawl. assembly.py places the pawl with its pin, its two washers, its screw and its spring, locked, released or at any angle.

checks.py, section Ring lock, confirms on the solids: the slot is 3.10 mm wide, 13.00 mm deep and 25.0 mm long, and its bottom lies on a circle of 25 mm; the finger passes 6.0 mm above the bottom; where it crosses the slot its middle lies 0.03 mm beside the middle of the ring; the locked finger stops the bare ring of the drawing after 4.5 mm of lift and bears on the deck with 9 and 6 mm²; at 17° the finger stands 0.99 mm behind the slot and the ring lifts out; from locked to 25° the pawl with its pin touches nothing when it is moved 0.65 mm in eight directions; the knob stands 4.5 mm above the deck, 4.3 mm from the shut lid and 3.3 mm from a lid that is grown and askew; the spring is 12.5, 8.0 and 5.9 mm long and leaves the axis of its cup by 0.17 mm; the pawl rises onto its boss when it is turned 19.9° or more; with the pin the centre of mass of the pawl lies on the pivot. Section Small screws confirms the thread and the hole depth of the pivot screw and that the M3 washer is wider than the bore of the pawl.

manual_text.py describes pressing in the pin and mounting the pawl (step 9), bedding and locking the ring (step 12) and freeing it (section 7); manual.py renders the lock from above, from below and in section.

Bounds: the ring dummy is a typical solitaire with a band of 2.5 x 1.8 mm; paper and cloth are not drawn. The spring is drawn as a tube. None of these parts has been printed; the ring pawl of revision ten was not printed either.
