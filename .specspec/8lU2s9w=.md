---
id: 8lU2s9w=
type: requirement
parents:
- 8JHAWVE=
---
# Resistors keep the 5 V rail and the amplifier off while the controller does not drive them

The pins of the controller drive nothing while it is in reset, while it is being flashed, and in deep sleep unless the firmware holds them. In those states pull-down resistors decide: 4.7 kOhm on the enable of the boost converter and on the shutdown of the amplifier, 100 kOhm on the reset of the reader.

The first two are this small because both boards carry a pull-up to the battery: 100 kOhm from En to Vin on the MiniBoost and 1 MOhm from SD to Vin on the amplifier board, beside 100 kOhm to ground inside the amplifier chip. Against them a pull-down of 100 kOhm leaves 1.5 to 2.1 V at En, where the converter is on above 1.2 V, and 0.14 to 0.20 V at SD, where the amplifier shuts down below 0.16 V. With 4.7 kOhm En rests at 0.13 to 0.19 V and SD at 13 to 19 mV. The reader board has no pull-up on its reset line, so 100 kOhm suffices there.

The price: 29 to 40 µA flow through the pull-up of the boost board for as long as the rail is off, which brings the estimate for sleep to 70 to 130 µA. Taking that resistor off the board saves it. Boards of other makers can carry other pull-ups; the rule is a pull-down of at most a twentieth of the pull-up on the boost board and at most a hundredth of the one on the amplifier board, and measuring both off states is one of the checks before the ball is closed.

Origin: agent conclusion of 2026-11-26 from Adafruit's design files of both boards and the data sheets of TPS61023 and MAX98357A (research/05_power_servo.md, section 11, item 10; research/04_mcu_audio_led.md, section 10, item 9). It replaces pull-downs of 100 kOhm on both inputs, which the review for the schematic found not to work. Nothing has been built or measured.
