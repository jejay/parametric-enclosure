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

parts_core.py: stage() is the inner dome with the flat deck, the collar that centres the lid and the four screw wells. For the ring it fuses the walls and the floor of the slot under the deck, with the two windows for the finger, cuts the slot through deck and walls, cuts the slit of the knob, and adds the pivot boss with its pilot hole, the post for the tail and the cup of the spring. ring_pawl() is the pawl: hub, bar, finger with sloped lower edges and a tapered end, knob, and the nub for the spring; ring_pawl_at() turns it and pushes it up against the deck. params.py, section 5, holds the owner's three sizes of the slot and the dimensions of the pawl. assembly.py places the pawl with its two washers, its screw and its spring, locked, released or at any angle.

checks.py, section Ring lock, confirms on the solids: the slot is 3.10 mm wide and its bottom lies on a circle of 25 mm; the finger passes 4.2 mm above the bottom and a ring of size 49 with a band of up to 4.2 mm stands under it; the locked finger stops the bare ring of the drawing after 2.7 mm of lift and bears on the deck with 9 and 7 mm²; at 18° the finger stands 0.87 mm behind the slot and the ring lifts out; from locked to 25° the pawl touches nothing when it is moved 0.65 mm in eight directions; the knob stands 4.5 mm above the deck and the shut lid keeps 13.2 mm from it; the spring is 12.5, 9.5 and 8.5 mm long; the pawl rises onto its boss when it is turned 20.9° or more. Section Small screws confirms the thread and the hole depth of the pivot screw and that the M3 washer is wider than the bore of the pawl.

manual_text.py describes mounting the pawl (step 9), bedding and locking the ring (step 12) and freeing it (section 7); manual.py renders the lock from above, from below and in section.

Bounds: the ring dummy is a typical solitaire with a band of 2.5 x 1.8 mm; paper and cloth are not drawn. The spring is drawn as a tube. None of these parts has been printed.
