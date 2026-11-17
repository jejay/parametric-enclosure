---
id: OHBWoNI=
type: implementation
parents:
- JcwcRlM=
- 8JHAWVE=
sources:
- path: src/poketonieengagementhunt/parts_core.py
  symbol: chassis
- path: src/poketonieengagementhunt/assembly.py
  symbol: build
- path: src/poketonieengagementhunt/checks.py
  symbol: check_assembly_paths
---
# Chassis and the assembled stack

The chassis is a bucket with a flange that rests on the bowl's bosses. It carries the snap cradle for the cell with slots for the contact plates, the servo bay, pockets for controller and amplifier, shelves for charger and boost converter, the speaker baffle, and a window in its floor plate for the reader harness that comes up from the bowl. assembly.py places every part and component and is the single description of the stack.

The checks confirm that the closed assembly has no collisions, that the core can be lowered into the bowl past the four lower bosses and the parked plugs, the band over the core and the stage onto both, and that the cell lifts straight out once the stage is off.

Bounds: wires are not modelled. The boards are held by glue; no clips are provided.
