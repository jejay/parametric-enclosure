---
id: bxoY9Uk=
type: implementation
parents:
- oiijK3c=
sources:
- path: docs/electronics.md
- path: src/poketonieengagementhunt/manual_text.py
  symbol: BOM_NOTES
- path: research/04_mcu_audio_led.md
---
# Substitute hall switch in the wiring notes and the parts list

docs/electronics.md names both parts at the wake pad, with the pull-up that the AH3661UA needs, and has a paragraph on what differs and on choosing the most sensitive of several parts. manual_text.py names the substitute and its Conrad order number in the list of parts and lists the resistor and the capacitor among the small parts. research/04_mcu_audio_led.md, section 5, holds the comparison with the parts that were not taken; both data sheets are in research/downloads/hall_alternatives.

Bounds: nothing has been bought or measured. The reach to the side is derived from the calculated field of an ideal magnet; the check of the hall switch in checks.py still counts with the 4.8 mT of the TI part.
