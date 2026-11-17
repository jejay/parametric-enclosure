---
id: iUrnS1k=
type: requirement
parents:
- bgOIq54=
---
# A hall switch on the axis of the spot wakes the device; card detection is the second way

A hall switch senses a magnet in the foot of a figure that is stood on the spot and wakes the device, so neither a button nor a phone is needed. Because a figure may stay on the spot for months, the device arms its wake-up for the opposite state each time it goes to sleep: it wakes when a figure is placed, or when the one standing there is lifted.

The switch is laid out for the magnets of the classic Tonies: cylinders of 6 x 6 mm whose pole face lies 1 to 2 mm above the underside, one in the middle of the foot or one in each of two feet about 20 mm apart. It lies on the axis of the spot on the floor of the reader pocket, 6.8 mm below the standing surface, which puts its element 8.3 to 9.3 mm below such a pole face. The depth is chosen for magnets beside the axis: nearer to the foot, the field of a magnet 10 mm to the side passes through zero. At this depth an ideal magnet on the axis gives 19 to 24 mT, one that is 8 mm off the axis about 6 mT, and two magnets 20 mm apart with like poles down about 6.5 mT; the switch needs 4.8 mT at the latest. The layout counts on a figure that stands within about 8 mm of the spot. Since revision four nothing marks the spot, so the look of the tongue no longer assures that; the owner has accepted this risk.

One switch on the axis does not cover two magnets with unlike poles down, whose fields cancel between them, or magnets much weaker than assumed. The other means are prepared: the floor of the pocket is flat, so the switch can be glued where a bench test finds the field; a spare wire of the harness takes a second switch; and the reader's interrupt line is wired to the controller, so that the reader's own low-power card detection can wake the device instead, at 35 to 220 µA in sleep instead of 1 µA.

Open risk, to be closed on the bench before printing: number, position, polarity and strength of the magnets in the Pokémon figures themselves.

Origin: agent conclusion from research/04_mcu_audio_led.md, research/07_firmware_app_feasibility.md and research/09_tonie_figure_dimensions.md.
