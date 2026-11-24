---
id: vfIxugA=
type: implementation
parents:
- F7C8Of8=
sources:
- path: src/poketonieengagementhunt/manual.py
- path: src/poketonieengagementhunt/manual_text.py
- path: docs/building_manual.md
---
# Building manual with step and explosion renderings

manual.py renders the overview, a labelled section, the exploded view, one to three pictures for each of the twelve assembly steps, and detail views of latch, hinge, ring lock, emergency path, a figure on the grass with a section through the tongue, and print orientation. manual_text.py holds the instructions and the purchasing notes. Position numbers come from the assembly list, so the balloons in every picture match the bill of materials in docs/building_manual.md.

Bounds: wiring is described in docs/electronics.md, not drawn. The instructions have not been tested by building the device. In revision six the steps for the hinge and the ring lock were rewritten after the paths of their pins had been followed in the model. The owner's first print then showed that the hinge could still not be put together as step 10 said; that step was rewritten once more after each of its moves, pins, tools, spring leg and wire, had been followed in the model, and has not been tried since.
