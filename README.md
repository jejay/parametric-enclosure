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
| `export/stl/` | the 16 printed parts, already in print orientation, and test pieces for the M2 pilot holes, the heat-set inserts and the two fits of the hinge pins |
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

**Revision 7.** A hinge that holds its pins and can be put together, after the first print of lid, stage and band:

- That print showed that the hinge towers did not enclose their pins: the dome of the stage had cut each knuckle in half, bore included, so a pin lay in an open groove. Each tower now ends in a closed ring round its pin. Half of that ring stands out of the dome, into the room behind the hinge, and keeps 0.5 mm from the wall of the lid at every opening angle.
- The pins slide in the towers and are pressed into the two ends of the spring sleeve. The sleeve cannot leave the gap between the ribs of the lid, so a pin can only come out by being pulled out of the sleeve. `export/stl/pin_test_coupon.stl` shows which hole sizes suit the printer.
- The pins are pushed through the ribs with a small screwdriver, without force, and pressed home with ordinary long-nose pliers. The earlier way needed plier jaws 1.5 mm thin, opened 30 mm, to make a press fit.
- The forward leg of the lid spring rests on a piece of steel wire, pushed through the feet of the towers after the leg has been lifted. The printed yoke of revisions 1 to 6 could not have been reached by the leg once the pins were in.
- The manual now says that the legs of the spring are cut to 14 mm.
- Only the stage and the sleeve have changed; the lid, the band and every other printed part are as they were. New on the list of parts: 23 mm of steel wire of about 1 mm, for which a paper clip does.

**Revision 8.** Play and tolerances. A printed hinge does not run on one line, and a printed surface lies a few tenths of a millimetre beside the model. Everything the lid passes, and the latch that holds it, was gone through for a lid that stands as askew as its hinge lets it and for surfaces that come out 0.2 mm fat:

- What the hinge allows: 0.3 mm of room round the pins in the ribs of the lid and 0.15 mm in the towers let the lid stand ±1.75° askew, about the vertical and about the fore-aft axis, and slide ±0.5 mm along its pins. That moves the hook of the latch up to 2.9 mm sideways. The checks have a new section, Play and tolerances, that works with these numbers.
- Gaps round the lid. The collar of the stage now keeps 0.6 mm from the lid (0.35 before), the ring of the button 0.6 mm (0.2), the hinge towers 0.5 mm from the ribs (0.2). A lid whose every surface is 0.4 mm fat, as if both sides of every gap had come out wrong, still lies down without being wedged. For the ring of the button the room was made on the bezel, which is 0.4 mm smaller from the rim of the bowl upwards; the lid is unchanged.
- Guided at first, then free. The collar is 3 mm high instead of 1.6 and guides the lid until the hook of the latch stands inside its slot. It ends beside the ball; behind it the stage is cut back along the path of the lid's lip, for a lid pushed as far to one side as it goes. In revision 7 that lip passed the back of the stage at 0.1 to 0.3 mm: with ordinary print tolerances it would have rubbed there. Now nothing touches the lid from 8° of opening to the stop, however it stands, and up to 8° collar, bezel and slot guide it and only widen as it rises.
- The latch lets go with room to spare. The pawl turns 44° instead of 24° and could turn 54°. Released, it lets a hook pass that stands 6 mm towards it; a servo that stops 4° short still frees a hook that is 3 mm off, twice what the collar lets it be. The nose of the pawl lies 0.75 mm above the tooth instead of 0.15 mm, and the pawl has a defined 0.3 mm of play on its pivot; in revision 7 the model let it float by 1.1 mm, more than the latch could take. The price: a latched lid can be pressed down by a little less than a millimetre at the front.
- The hook finds its slot and leaves it. The slot has a funnel on both sides that takes a hook 3.5 mm off, its edge under the deck is sloped beside the tooth, the inside of the dome is hollowed for the front end of the tooth, and a rib under the deck guides the stem. The checks now open and close the lid in steps of 0.05° with the hook up to 2.9 mm beside its place and accept only slopes: nothing may be pushed further in a step than twice the way the hook travelled.
- Closing had never been followed in the model, only opening, and it showed a fault of every revision so far: the hook comes down in an arc, and with the lid 5° from shut even the stem of a centred lid landed on a flat corner of the pawl, 0.5 mm wide, behind its nose. The flank of the pawl now keeps out of the way of the stem at every angle, and the sloped edge of the nose runs on behind it.
- Smaller things: the return spring of the pawl is a 12 mm piece of ball-pen spring that sits in a cup; the pawl's bore is 5.5 mm; the paper clip of the emergency opening meets the pawl after 16 mm and is pushed 5 mm further; the bores of the lock pin are 3.4 mm; the towers have a buttress each.
- The forward leg of the lid spring rests on a third dowel pin, 2 x 18 mm, pressed through the feet of the towers, instead of on a piece of wire.
- To print anew: stage, pawl, bezel, ring cradle and the test piece for the pins. Lid, band, sleeve, pivot washer and every other printed part are as they were. Nothing has to be bought: the 2 x 18 pin is among the pins you have, and cross-head countersunk M3 x 16 screws fit under the tongue.
- What the model could not give: the rear rim of the lid runs in the pocket of the band with 0.4 mm of room, and lid and band are printed. Step 11 of the manual says how to check it and what to do if it scrapes.

**Revision 9.** Stronger feet for the pin under the spring leg, after one of them broke in the printed stage of revision 8:

- The foot split through its hole: half of the hole stayed on the stage, half was in the piece that came off. The stage is printed in level layers and the hole lies level, so a pin that is pressed in pushes the two halves of the hole apart across the layers. In that plane the foot had 1.1 mm of plastic on each side of the hole, 2.0 mm thick.
- Each foot is now 4.8 mm wide instead of 4.3 and 3.0 mm thick instead of 2.0, the added millimetre towards the middle of the hinge. Beside the hole it has 1.5 mm before and 1.3 mm behind, and in the plane in which the foot split 8.0 mm² instead of 4.5. In the added millimetre the hole is 2.3 mm wide: the pin is held in 1.8 mm of each foot as before, and the rest only carries. More was not added: behind the feet the stop tabs of the lid pass, at 1.7 mm as drawn, and at 0.75 mm when lid and feet are both 0.2 mm fat and the lid uses all the play of its hinge at once.
- More plastic does not make a hole safe that is too tight. The manual now has the 2 x 18 pin tried in the 2.05 mm hole of the test piece for the pins before the stage is printed, and says not to force it: inside the stage no drill reaches these holes, and `YOKE_HOLE` is the value to change.
- To print anew: the stage. Every other printed part is as it was, the test piece included. Nothing has to be bought.

**Revision 10.** The ring is locked by a pawl. In the first build the latch pawl works really well; the lock of the ring, a printed slider on a steel pin, did not: the slider could not be fixed on the pin.

- Cradle, pin and slider are gone. The slot of the ring is cut into the stage itself, with the owner's dimensions: 3.1 mm wide, a round bottom of 25 mm diameter, and 4.2 mm under the lock for the band of the ring. What the ring leaves free is filled with paper or cloth, which holds it and keeps it from being scratched.
- The lock is a second pawl under the deck, a modified copy of the latch pawl on the same kind of pivot. Its finger passes through the ring from behind, directly under the deck, so a pull at the ring presses the finger against the deck and does not load the arm or the pivot. Its knob stands up through a curved slit behind the middle of the ring: pulled 6 mm back it frees the ring, and a compression spring of 4 x 15 mm, uncut, takes it back. Only a hand moves it.
- Room: finger and knob have 1 mm on each side in their windows and in the slit. The checks move the pawl by the play of its pivot and 0.2 mm for each printed surface, in eight directions, over its whole way.
- The pivot takes the M2 x 6 screw and the standard M2 washer of the latch pawl as built. By the drawn sizes that washer (5.0 mm) is narrower than the bore of a pawl (5.5 mm) and cannot hold it, so an M3 washer lies between it and the ring pawl. The pawl is 4.3 mm thick, so that the screw has a hole deep enough and 1 mm of deck over it.
- The ring stands 2.6 mm deeper than before: the slot is 11.2 mm deep, which is the deck, the finger and the 4.2 mm under it.
- Not in the model: how strong the spring is. The pawl is not balanced about its pivot, so by a hand estimate a blow of some 90 g from behind turns it against a spring that holds with 1 N; a hard drop gives more. The ring would have to be thrown 11 mm upwards in the same instant, against what it is bedded in (`research/06`, section 1.6).
- On the list of parts: one more M2 x 6 screw, an M2 and an M3 washer, a 4 x 15 mm spring; the 3 x 25 pin and the felt for the slot are no longer needed. To print: the stage anew, and the ring pawl. Cradle and slider are no longer parts.

**Revision 11.** The ring pawl once more, after the owner had seen the layout of revision 10:

- The knob stands on the tail of the pawl, to the front left of the ring, and no longer behind the ring, where the ring itself was in the way of a hand. It is pulled 4.4 mm towards the middle line of the deck.
- The finger crosses the slot square and in the middle of the ring: the pivot now lies in the plane of the ring, 20 mm from its middle. Before, the finger crossed 21° off square and its windows lay beside the middle.
- The slot is 13 mm deep instead of 11.2 mm: a half-round bottom of 25 mm with half a millimetre of upright wall above it. The ring of the drawing stands in it with 68 % of its height. Under the finger there are now 6.0 mm.
- The spring is used harder: the uncut 4 x 15 mm spring is pressed from 12.5 mm to 8.0 mm, where it was 9.5 mm. It bears on the tail 15.2 mm from the pivot, and its cup is turned so that it opens along the way of the tail.
- The pawl is balanced. A steel dowel pin of 4 x 8 mm, pressed into it beside the hub, brings its centre of mass onto the pivot; it lay 9.1 mm beside it. A blow then has almost nothing to turn the pawl with.
- When the pawl is locked, its arm rests against a pad on the wall of the slot; the post under the deck is gone.
- On the list of parts: one dowel pin of 4 x 8 mm more. To print: the stage and the ring pawl, both anew if revision 10 was printed. Nothing else has changed.

**Revision 12.** The ring pawl slimmed, because the owner found the pawl of revision 11 bulky:

- The tail is a bar of 6 mm from the hub to the knob, where it was a filled plate that spanned hub, knob and pin, and the arm is 4 mm wide instead of 5. The printed pawl weighs 1.87 g instead of 2.24 g.
- The counterweight pin stays, in a small round of its own beside the hub, 7.0 mm from the pivot, and the pawl is balanced with it. Without pin and round the pawl would weigh 1.68 g and its centre of mass would lie 4.1 mm beside the pivot: a blow of about 220 g would turn it against a spring that holds with 1 N, where the balanced pawl takes about 1900 g. `RPAWL_PIN` in `params.py` leaves the pin out.
- Knob, finger, spring and slot are as in revision 11. To print: the stage, in which the pad for the arm and the slit of the knob follow, and the ring pawl.

**Revision 13.** The ring pawl without its counterweight pin, by the owner's final decision: a steel pin that is held by a press fit or by glue could fall out one day, into the electronics.

- The pawl is the slim one of revision 12 without the round beside its hub: knob on the tail, the finger square and in the middle of the ring, the spring pressed from 12.5 to 8.0 mm, the slot 13 mm deep. It weighs 1.68 g.
- It is not balanced: its centre of mass lies 4.1 mm beside the pivot. By a hand estimate a blow of about 220 g on the back right of the ball starts to turn it against a spring that holds with 1 N, where revision 10 took about 90 g and the balanced pawl about 1900 g. A hard drop is taken to give 500 to 2000 g. For the ring to be lost it has to be thrown 13 mm upwards out of its slot in the same instant, against what it is bedded in.
- `RPAWL_PIN` in `params.py` puts the pin back.
- On the list of parts the dowel pin of 4 x 8 mm is gone again. To print: the ring pawl; the stage is as in revision 12.
- Besides: the spring sleeve is also exported with blind holes of 1.90 and 1.85 mm (`sleeve_1_90.stl`, `sleeve_1_85.stl`); a sleeve is to be printed with others, because a single one stays too hot.

## State of the design

- 117 of 117 geometry checks pass. All 15 printed parts are valid and watertight; the closed assembly of 43 items has no collisions; the lid has been swept through its 95° travel in 39 positions without contact; latch, ring pawl, emergency opening and the assembly sequence are checked the same way, including the paths of the hinge pins and the lock pin, the reach of screwdriver and pliers at the hinge and of the hex key for the screws inside the core. The checks also confirm that the hinge towers enclose their pins all round, that the sleeve keeps the pins, that the spring's forward leg can be lifted onto its pin, and how much plastic the feet of that pin have round its hole.
- The same is checked for a lid that is not where the model has it: grown by 0.2 mm, askew by the ±1.75° its hinge allows, with its hook up to 2.9 mm beside its place. Nothing closes in on it over the first 8° and nothing touches it from there to the stop; the latch lets go, holds, and closes again from every such position.
- For the grass tongue the checks cover the seat of the ball on four pads, the flush underside, the reader pocket, the frame that holds the grass top, the hidden cable path, the clearance between a figure and the ball, the plain standing surface, where the grass stands and that it is not mirrored, the hidden ends of the turf screws, and the stance: the centre of gravity stays at least 24 mm inside the edge of the area on which ball and tongue stand.
- Not provable in CAD, and therefore the first thing to do (building manual, section 2): read all four Pokémon Tonies with the blue PN5180 board under a 1.6 mm sheet, on wood and on metal, find the magnets in their feet, and see how far off the middle a figure may stand. The tag is a small rod somewhere above the foot. The magnets are assumed to be those of the classic Tonies; `docs/electronics.md` says what to do if they are not.
- Also not provable in CAD: how the pilot holes for the M2 screws and the bores for the hinge pins come out of the printer, how firmly a hinge pin holds in the sleeve, which is all that keeps it in the hinge, and how tight the holes for the pin under the spring leg come out, which decides whether a foot stands that pin being pressed in. Print the test pieces first (building manual, sections 2 and 3). The device of revision 8 has been built as far as lid, latch and ring lock; the feet of revision 9 and the ring pawl of revisions 10 to 13 have not been printed.
- The checks of play take 0.2 mm per surface as what a printer may be off, and friction is not in them at all: a contact counts as harmless when it is a slope. Whether the pawl turns freely on its boss and comes back by its spring, and whether the lid scrapes in the pocket of the band, show on the printed parts only; the manual has a test for each (steps 9, 10 and 11, section 6).
- Dimensions of some delivered parts, of the figures and of the ring are still assumptions. They are marked `MEASURE` in `params.py`. The foot of a figure (45 mm, measured on pictures) sets the width of the tongue beside a figure and the ground that is kept free of grass; the reader board sets the length of the tongue.
