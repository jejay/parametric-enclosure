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
- path: src/poketonieengagementhunt/parts_core.py
  symbol: tower_knuckle
- path: src/poketonieengagementhunt/components.py
  symbol: torsion_spring
- path: src/poketonieengagementhunt/checks.py
  symbol: check_lid_motion
---
# Lid, hinge and the pocket in the band

The lid carries two ribs with the bores in which it turns on the two hinge pins, a stop tab on each rib, a wall thinned from inside so that the hinge can sit close to it, and beside that a relief for the pins while they wait in their towers. The stage carries the two hinge towers, 0.5 mm beside the ribs, whose knuckles enclose the pins and stand half out of its dome, a buttress outside each tower, a foot under each tower for the pin on which the spring's forward leg rests, and the beam that stops the tabs at 95°. The pocket in the band and the relief in the stage round the hinge are cut with the surface of revolution that the lid's rear rim sweeps about the hinge axis.

The checks sweep the lid through 39 positions without contact, confirm that 3° beyond the stop collides, that the spring coil stays clear, and that the spring's torque exceeds gravity with a spring 20 % below nominal.

Bounds: the spring's winding direction and real torque, friction, and the impact on the stop are not modelled. The rear rim of the lid runs in the pocket of the band with 0.4 mm; lid and band are printed with that gap.
