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

Bounds: wiring is described in docs/electronics.md, not drawn. The instructions have not been tested by building the device. In revision six the steps for the hinge and the ring lock were rewritten after the paths of their pins had been followed in the model. The owner's first print then showed that the hinge could still not be put together as step 10 said; that step was rewritten once more after each of its moves, pins, tools, spring leg and its seat, had been followed in the model. In revision eight steps 9 to 12 and the commissioning got trials of the play of pawl and lid. By the owner's report of 2026-11-25 lid, latch and the ring lock of revision eight have since been built: the latch works, the slider of the ring lock could not be fixed on its pin. In revision ten steps 9 and 12 and the section on freeing the ring were rewritten for the ring pawl; these have not been tried on printed parts.
