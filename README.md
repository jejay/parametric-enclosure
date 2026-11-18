# Poké Ball in the tall grass, for the Tonie hunt

A 100 mm Poké Ball with a tongue of tall grass in front of it. It speaks, reads a Tonie figure that is stood on the grass in front of it, signals closeness with its glowing button and, on a command from the phone, jumps open to present an engagement ring.

![closed, with a Tonie](docs/img/hero_tonie.png)

This repository holds the hardware design: research, a parametric CAD model, a geometry verification suite and the building manual. Firmware and phone app are not written yet; `docs/electronics.md` shows that the hardware can carry them.

## Where things are

| Path | Content |
| --- | --- |
| `docs/building_manual.md` | bill of materials, print settings, twelve assembly steps with renderings, exploded view, commissioning, emergency opening |
| `docs/electronics.md` | block diagram, power rails, net list, pin map, harness to the grass tongue, behaviour the firmware must respect |
| `docs/verification.md` | result of every geometry check (watertightness, fit, clearances, motion, grass tongue, physics) |
| `research/` | ten research notes with sources, including the candidates that were rejected; start with `research/README.md` |
| `export/stl/` | the 16 printed parts, already in print orientation, and a test piece for the M2 pilot holes |
| `export/step/` | the same parts, the dummy models of all purchased components and the full coloured assembly |
| `src/poketonieengagementhunt/` | the CAD model as Python (CadQuery); `params.py` holds every dimension |
| `.specspec/` | the specification graph: owner intentions, design conclusions and the artifacts that realise them |

## Regenerating everything

```sh
uv run poketonieengagementhunt check     # verification -> docs/verification.md
uv run poketonieengagementhunt export    # STL and STEP  -> export/
uv run poketonieengagementhunt manual    # renderings and manual -> docs/
uv run poketonieengagementhunt all
```

Change a value in `src/poketonieengagementhunt/params.py` (for example the ring dimensions, or the values marked `MEASURE` once the parts have arrived) and run `all`. The checks fail loudly if the change makes parts collide.

## Revisions

**Revision 2.** Revision 1 read a Tonie at the flat underside of the ball, which invited turning the ball over. Revision 2 keeps the ball upright:

- A Tonie stands on a plain, level spot of green "tall grass" in front of the ball; nothing holds it.
- The reader, now the common blue PN5180 board, lies directly under that spot, with the hall switch that wakes the ball.
- The ball itself is unchanged except for its bowl, which lost the dock and gained screw bosses and a hidden cable window, and its chassis, which no longer carries a reader.

**Revision 3.** The grass of revision 2 was a ring round the ball's foot plus a tongue. Revision 3 keeps the tongue alone:

- No grass round the ball. The rear end of the tongue lies under the belly of the ball and is held by four screws from below.
- The tongue is 15 mm high instead of 6.5 mm, and its underside lies in the plane of the ball's flat foot: both stand on the table together.
- The grass is drawn by a random generator. Place, size, direction and leaf shape differ from tuft to tuft, and no tuft has a twin on the other side. `LAWN_SEED` in `params.py` gives another lawn.
- The hall switch is laid out for the magnets of the classic Tonies and lies deeper, so that it also catches magnets beside the axis. The bare ground round the spot is 2 mm wider.
- The antenna lies 11.7 mm above the table instead of 3.2 mm, which eases the risk of a metal table.

**Revision 4.** One colour, and a smaller tongue:

- Tongue and grass are one light green. The grass top, turf plate and tufts together, is one printed part. The bright disc that marked the place of the figure is gone, and nothing marks that place now: the owner's decision, with the risk accepted.
- The tongue is 72 mm wide at the ball and 66 mm at its round tip instead of 76 mm, and reaches 70 mm beyond the ball instead of 76 mm. Its height is unchanged. The tip is a circle round the place of the figure, so a centred figure shows the same 10.5 mm of ground at the front and at both sides.
- The grass is thinner and stands in the two corners beside the ball. None stands beside or in front of the figure.
- The grass top lies in a frame: a rim of the tray holds its tip, and four hidden screws hold its rear half.

**Revision 5.** The tongue ends just in front of the reader board:

- It reaches 61.5 mm beyond the ball instead of 70 mm. The reader board sets this length: it ends 20.8 mm in front of the centre of a figure, and the tongue needs 3.2 mm of wall in front of its pocket.
- The front end is blunt, a straight edge between two rounded corners, because the front corners of the board sit right inside it.
- A centred figure still stands on the tongue with its whole foot; the foot ends 2 mm short of the front edge. Grass, reader and height are unchanged.

**Revision 6.** Screws and pins that can be bought, and a hinge that can be pinned:

- The seven small screws are M2 machine screws with a hex socket, five M2 x 6 and two M2 x 8, in place of 2.2 mm self-tapping screws. They form their own thread in printed pilot holes; `export/stl/m2_test_coupon.stl` shows which hole size suits the printer.
- The washer of the latch pivot is printed. A standard M2 washer is 5 mm across and could not hold the pawl, whose bore is 5.3 mm.
- The pin of the ring lock is 3 x 25 mm instead of 3 x 24 mm.
- The hinge has two pins of 2 x 8 mm instead of one of 2 x 20 mm. The hinge axis lies inside the lid, whose wall closes it at both ends, so one long pin could never have been pushed in. The two pins wait in the hinge towers while the lid is slid on and are then pressed in with pliers. A relief inside the lid wall gives them room; nothing shows outside.
- The verification now also follows the paths by which the pins are put in and the reach of the tools.
- The hall switch may be an AH3661UA, which Conrad stocks, in place of the TI DRV5032FB: same TO-92 body and legs, but an open-drain output that needs 1 MOhm to 3.3 V, and a little less reach to the side (`docs/electronics.md`).
- The bowl takes the M3 heat-set inserts you have: 5.0 mm over the knurl, 6 mm long at the rim and 5 mm long low on the front wall, in holes of 4.4 mm. `export/stl/insert_test_boss.stl` is a test piece for them.
- Nothing else on the list of parts to buy has changed.

## State of the design

- 100 of 100 geometry checks pass. All 16 printed parts are valid and watertight; the closed assembly of 41 items has no collisions; the lid has been swept through its 95° travel in 39 positions without contact; latch, ring lock, emergency opening and the assembly sequence are checked the same way, including the paths of the hinge pins and the lock pin and the reach of the hex key for the screws inside the core.
- For the grass tongue the checks cover the seat of the ball on four pads, the flush underside, the reader pocket, the frame that holds the grass top, the hidden cable path, the clearance between a figure and the ball, the plain standing surface, where the grass stands and that it is not mirrored, the hidden ends of the turf screws, and the stance: the centre of gravity stays at least 24 mm inside the edge of the area on which ball and tongue stand.
- Not provable in CAD, and therefore the first thing to do (building manual, section 2): read all four Pokémon Tonies with the blue PN5180 board under a 1.6 mm sheet, on wood and on metal, find the magnets in their feet, and see how far off the middle a figure may stand. The tag is a small rod somewhere above the foot. The magnets are assumed to be those of the classic Tonies; `docs/electronics.md` says what to do if they are not.
- Also not provable in CAD: how the pilot holes for the M2 screws and the bores for the hinge pins come out of the printer. Print the test piece first and try a pin in a hinge tower before the lid goes on (building manual, sections 2 and 3).
- Dimensions of some delivered parts, of the figures and of the ring are still assumptions. They are marked `MEASURE` in `params.py`. The foot of a figure (45 mm, measured on pictures) sets the width of the tongue beside a figure and the ground that is kept free of grass; the reader board sets the length of the tongue.
