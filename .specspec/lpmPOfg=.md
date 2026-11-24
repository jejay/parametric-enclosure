---
id: lpmPOfg=
type: implementation
parents:
- siYJpX0=
sources:
- path: src/poketonieengagementhunt/params.py
- path: src/poketonieengagementhunt/parts_core.py
  symbol: _collar
- path: src/poketonieengagementhunt/parts_core.py
  symbol: stage
- path: src/poketonieengagementhunt/parts_shell.py
  symbol: lip_swing_tool
- path: src/poketonieengagementhunt/parts_shell.py
  symbol: bezel
- path: src/poketonieengagementhunt/checks.py
  symbol: check_play
- path: src/poketonieengagementhunt/checks.py
  symbol: grown_lid
- path: src/poketonieengagementhunt/checks.py
  symbol: skewed
- path: docs/verification.md
---
# Room for a lid that stands askew: collar, cut-back, bezel and their checks

params.py derives the play of the hinge from its bores (HINGE_SKEW_DEG, LID_SIDE_PLAY, HOOK_SIDE_PLAY) and holds PRINT_TOL, the gaps round the lid and LID_FREE_DEG. _collar builds the collar, 3 mm high and 0.6 mm inside the lip of the lid, within 100° of the front; stage adds it after the shell has been cut back. lip_swing_tool is the solid of revolution about the hinge axis that the lip of the lid sweeps at the back, widened for a lid that stands LID_SIDE_PLAY to either side; stage cuts it out of dome and base ring, together with the cylinder round the hinge, and removes what would be left of the base ring under that cylinder. bezel makes the tube 0.4 mm smaller from the rim of the bowl upwards.

check_play moves a lid whose surfaces lie 0.2 mm further out than drawn, except under its rim, where it lies on the band. It reports the play; measures the gaps round the closed lid (0.50 mm to the stage, 0.60 mm to the bezel, 0.39 mm in the pocket of the band) and finds a lid grown by 0.4 mm unwedged; turns the lid about the vertical so that its hook stands in eleven positions from 2.9 mm on one side to 2.9 mm on the other, at seven angles up to 8°, and finds that no free position is lost as the lid rises, that the middle is free throughout and that at 8° all are free; and from 8° to the stop finds no contact with stage, bezel, band or pawl for a lid turned 1.75° about the vertical or slid against a tower, and for a lid turned 1.75° about the fore-aft axis none from 30° on, below which its lower side lies on the band.

Bounds: geometry only, and for an assumed 0.2 mm per printed surface. The lid is turned about one axis at a time. Contacts with the guides are found, not weighed: no check knows friction. Of these parts the stage of revision six and the lid and band, which are unchanged, have been printed; the reworked stage and the bezel have not.
