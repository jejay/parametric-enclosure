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
# Grass tongue: tray, grass top, lawn, reader pocket and their checks

parts_base.py builds the tray with its hollow rear end, seat pads, reader pocket, ledge, hall seat, cable channel and the rim round its top, and the grass top: the turf plate with its leaning edge, fused with the lawn. The lawn comes from a random generator with a fixed seed; every blade is a lofted solid that is shortened where the ball is near and fused into the plate together with the mound of its tuft. components.py holds the dummy of the blue reader board, with outline, holes, header row and antenna as measured in research/08, and the harness with its two plug pairs. assembly.py places them and the fasteners; in the generic interference test the plate alone stands in for the grass top.

check_grass_base in checks.py confirms: the ball touches the four pads and nothing else; the underside of the tongue and the flat of the ball lie on one plane and nothing reaches below it; no blade comes nearer to the ball than 1.1 mm; the ball can be lowered onto the tongue; the reader drops into its pocket and the grass top goes into its frame along the slope of the frame walls; lifted straight up, the grass top runs into the rim at the tip; 5.0 mm of room remain under the board; a plug passes the hidden window; each of the four Pokémon figures, within an envelope of Ø52 x 78 mm, stays 11.4 mm clear of the ball; the standing surface is plain, the joint between grass top and rim lies 7.2 mm in front of a centred foot, and the grass keeps 8.5 mm from that foot and stays 20 mm behind the centre of the figure; no tuft has a twin on the other side of the centre line; 89 % of the blades are rooted in the two corners beside the ball and none in front of the middle of the ball; every turf screw ends inside the root of a tuft, with solid plastic round its pilot hole; the antenna lies 3.3 mm below the surface and 11.7 mm above the table, the hall switch 6.8 mm below the surface; the nearest metal, a turf screw, is 13 mm from the antenna.

Bounds: geometry only. Reading at this distance and on a metal table, the field of the real magnets at the switch, how close to the unmarked spot a figure is put down, the fit of the printed grass top in its frame and the strength of the blades are not established. The lawn of 37 blades in 11 tufts, with 2 to 5 blades each and 5 to 15 mm high, is one arrangement out of many; another seed gives another.
