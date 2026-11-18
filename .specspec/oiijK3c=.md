---
id: oiijK3c=
type: requirement
parents:
- BUD5n7s=
- iUrnS1k=
---
# The AH3661UA can take the place of the TI hall switch

The AH3661UA of Nanjing AH Electronic, which Conrad sells as TRU COMPONENTS under order number 1569221, has the same TO-92 body of 4.0 x 3.1 x 1.52 mm and the same order of legs as the DRV5032FB, answers to either pole, works from 2.4 to 5.4 V and pulls its output low while a magnet is near. It fits the seat, the wires and the wake logic without change.

What the design has to carry with it: the output is open-drain and needs 1 MOhm to 3.3 V at the controller. The part switches at 3.5 mT typically and at 7 mT at the latest instead of 3 and 4.8 mT; on the axis of the spot that leaves the margin large, but a part at the upper limit catches a magnet about 7 mm off the axis instead of about 9 mm, and not two like magnets 20 mm apart. Three or four parts are bought and the most sensitive one is fitted. It draws 2.75 µA on average instead of 0.7 µA.

The TI part stays the reference in the model and the manual; either may be fitted. Parts at Conrad that were not taken: Honeywell SL353LT (push-pull and 1.8 µA, but SOT-23 and 6 mT typically, 11 mT at the latest), Honeywell SM351LT (magnetoresistive, senses the field in the plane of the chip), Infineon TLE4913 (SC-59, sold by the reel).

Origin: agent conclusion from research/04_mcu_audio_led.md, section 5. Stock and prices at Conrad were read from search results of 18 November 2026, not from the shop itself, which refuses automated access.
