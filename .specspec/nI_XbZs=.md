---
id: nI_XbZs=
type: implementation
parents:
- FQmWCSg=
- eZPMIyQ=
- 9ZfjiFY=
sources:
- path: src/poketonieengagementhunt/parts_core.py
  symbol: pawl
- path: src/poketonieengagementhunt/parts_core.py
  symbol: hook_slot
- path: src/poketonieengagementhunt/parts_core.py
  symbol: hook_guide
- path: src/poketonieengagementhunt/parts_core.py
  symbol: pawl_spring_cup
- path: src/poketonieengagementhunt/parts_shell.py
  symbol: _hook
- path: src/poketonieengagementhunt/parts_shell.py
  symbol: emergency_axis
- path: src/poketonieengagementhunt/parts_core.py
  symbol: _servo_bay
- path: src/poketonieengagementhunt/checks.py
  symbol: check_latch
- path: src/poketonieengagementhunt/checks.py
  symbol: LatchBench
- path: src/poketonieengagementhunt/checks.py
  symbol: check_play
---
# Latch and emergency path

The lid's hook with its sloped tooth, the pawl, the pivot boss, stop pin and spring cup under the deck, the slot of the hook through the stage and the servo bay in the chassis realise the latch. The pawl has a nose with a slope on top and a smaller one under its edge, a recess under the nose that is the latch face, a flank that stays behind the path of the hook's stem, a tail post for the servo arm, a nub for the return spring and a lug for the emergency paper clip that is as high as the pawl, so that it stands on the bed in the print. hook_slot cuts the slot with its two funnels, the sloped edge under the deck and the hollow inside the dome; hook_guide adds the rib beside the stem. The paper-clip path is one straight line defined once and used for the slot in the bezel wall, the notch in the baffle and the position of the pawl's lug.

check_latch confirms that the engaged pawl blocks the lid and that the pawl turned by 44° frees it; that the pawl turns 54° without contact, pushed up against the deck and lying on its washer; that the servo arm sweeps freely, meets the post 10° after its rest position, turns the pawl by 43.6° at its release angle and by 36° and 51° when the servo is 4° off; that an arm of 13 mm passes the pivot at 0.8 mm and one of 13.5 mm at 0.3 mm; that a 1.2 mm clip meets nothing before the lug, meets it after 16 mm and has opened the latch after 20.7 mm; and that the return spring is preloaded at rest and not solid at 54°.

check_play, with the class LatchBench, looks at hook, deck and pawl close up, the hook grown by 0.2 mm: the released pawl passes a hook 6 mm towards it and 3 mm with the servo 4° short; the pawl at rest holds a hook 1.8 mm away; it comes back over a tooth that stands 0.5 mm high; and with the lid moved in steps of 0.05°, a hook that starts up to 2.9 mm beside its place leaves the slot and finds it again, latched, while nothing is pushed further in a step than twice the way the hook travelled.

Bounds: geometry only. The servo arm is assumed trimmed to 13 mm; its rest and release angles are set at commissioning. Friction, the force of the return spring, how freely the printed pawl turns, and shock that could move the pawl are not analysed. None of these parts has been printed.
