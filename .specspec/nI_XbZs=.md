---
id: nI_XbZs=
type: implementation
parents:
- FQmWCSg=
sources:
- path: src/poketonieengagementhunt/parts_core.py
  symbol: pawl
- path: src/poketonieengagementhunt/parts_shell.py
  symbol: _hook
- path: src/poketonieengagementhunt/parts_shell.py
  symbol: emergency_axis
- path: src/poketonieengagementhunt/parts_core.py
  symbol: _servo_bay
- path: src/poketonieengagementhunt/checks.py
  symbol: check_latch
---
# Latch and emergency path

The lid's hook with its sloped tooth, the pawl with nose, tail post, spring seat and emergency lug, the pivot boss, stop pin and spring seat under the deck, and the servo bay in the chassis realise the latch. The paper-clip path is one straight line defined once and used for the slot in the bezel wall, the notch in the baffle and the position of the pawl's lug.

The checks confirm that the engaged pawl blocks the lid, that the pawl turned by 24° frees it, that pawl and trimmed servo arm sweep without contact, that the arm reaches the post, and that a 1.2 mm wire along the path meets nothing before the lug.

Bounds: the servo arm is assumed trimmed to 13 mm; its rest and release angles are set at commissioning. Shock that could move the pawl is not analysed.
