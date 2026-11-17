---
id: NtAG8DQ=
type: implementation
parents:
- NYeBfm0=
- tzVPwR0=
- cz4F_cg=
- iUrnS1k=
sources:
- path: src/poketonieengagementhunt/parts_base.py
  symbol: grass_base
- path: src/poketonieengagementhunt/parts_base.py
  symbol: grass_top
- path: src/poketonieengagementhunt/parts_base.py
  symbol: tufts
- path: src/poketonieengagementhunt/parts_base.py
  symbol: blades
- path: src/poketonieengagementhunt/components.py
  symbol: pn5180_blue
- path: src/poketonieengagementhunt/components.py
  symbol: harness
- path: src/poketonieengagementhunt/assembly.py
  symbol: build
- path: src/poketonieengagementhunt/checks.py
  symbol: check_grass_base
---
# Grass tongue: tray, turf, lawn, reader pocket and their checks

parts_base.py builds the tray with its hollow rear end, seat pads, reader pocket, ledge, hall seat and cable channel, the turf, and the lawn. The lawn comes from a random generator with a fixed seed; every blade is a lofted solid that is shortened where the ball is near and fused into the turf together with the mound of its tuft. components.py holds the dummy of the blue reader board, with outline, holes, header row and antenna as measured in research/08, and the harness with its two plug pairs. assembly.py places them and the fasteners.

check_grass_base in checks.py confirms: the ball touches the four pads and nothing else; the underside of the tongue and the flat of the ball lie on one plane and nothing reaches below it; no blade comes nearer to the ball than 1.1 mm; the ball can be lowered onto the tongue; the reader drops into its pocket and the turf closes it; 5.0 mm of room remain under the board; a plug passes the hidden window; each of the four Pokémon figures, within an envelope of Ø52 x 78 mm, stays 12.4 mm clear of the ball; the standing surface is plain and the grass keeps 8.3 mm from a foot; no tuft has a twin on the other side of the centre line; every turf screw ends inside the root of a tuft, with solid plastic round its pilot hole; the antenna lies 3.3 mm below the surface and 11.7 mm above the table, the hall switch 6.8 mm below the surface; the nearest metal, a turf screw, is 9 mm from the antenna.

Bounds: geometry only. Reading at this distance and on a metal table, the field of the real magnets at the switch, the strength of the blades and the look of the two greens are not established. The lawn of 71 blades in 18 tufts, with 2 to 6 blades each and 5 to 18 mm high, is one arrangement out of many; another seed gives another.
