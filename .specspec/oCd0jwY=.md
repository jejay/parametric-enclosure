---
id: oCd0jwY=
type: implementation
parents:
- FAm8kbA=
sources:
- path: src/poketonieengagementhunt/parts_shell.py
  symbol: lid
- path: src/poketonieengagementhunt/parts_shell.py
  symbol: rim_swing_tool
- path: src/poketonieengagementhunt/parts_core.py
  symbol: _hinge_towers
- path: src/poketonieengagementhunt/components.py
  symbol: torsion_spring
- path: src/poketonieengagementhunt/checks.py
  symbol: check_lid_motion
---
# Lid, hinge and the pocket in the band

The lid carries two ribs with the pin bores, a stop tab on each rib and a wall thinned from inside so that the pin can sit close to it. The stage carries the two hinge towers, the yoke on which the spring's body leg rests and the beam that stops the tabs at 95°. The pocket in the band and the relief in the stage are cut with the surface of revolution that the lid's rear rim sweeps about the hinge axis.

The checks sweep the lid through 39 positions without contact, confirm that 3° beyond the stop collides, that the spring coil stays clear, and that the spring's torque exceeds gravity with a spring 20 % below nominal.

Bounds: the spring's winding direction and real torque, friction, and the impact on the stop are not modelled.
