# Research index

All research was done on 2026-11-17; notes 08 to 10 were added the same day for revision 2, which moved the reader into a patch of grass in front of the ball. Revisions 3 and 4 reshaped that grass (a tongue alone, then one colour, shorter, with the grass in two corners) and needed no new research; they use the same notes. Each note lists its sources next to the claims and marks every value as verified by several independent sources, taken from a single source, or inferred. Candidates that were not chosen are kept, with the reason.

| Note | Question | Result in one line |
| --- | --- | --- |
| [01_tonie_rfid_tag.md](01_tonie_rfid_tag.md) | What is inside a Tonie and how is it read? | NXP ICODE SLIX-L, ISO 15693, privacy mode; unlock with GET RANDOM + SET PASSWORD (`5B 6E FD 7F`), then the UID identifies the figure |
| [02_rfid_reader_modules.md](02_rfid_reader_modules.md) | Which reader can do that, and how big is it? | PN5180; the common blue board is 70 x 39 mm, the Elechouse board 40 x 42 mm |
| [03_pokeball_proportions.md](03_pokeball_proportions.md) | What are the true proportions of a Poké Ball? | band 0.070 D, black ring 0.34 D, white disc 0.225 D, button 0.14 D, measured on seven sources |
| [04_mcu_audio_led.md](04_mcu_audio_led.md) | Controller, amplifier, speaker, LED, wake sensor | XIAO ESP32-S3 Plus, MAX98357A, Visaton K 40, one WS2812B, DRV5032FB hall switch |
| [05_power_servo.md](05_power_servo.md) | Cell, charging, 5 V, servo | one 18650, TP4056 USB-C with protection, TPS61023 boost, SG90 dimensions with their spread |
| [06_mechanics_printing_ring.md](06_mechanics_printing_ring.md) | Ring size, springs, fasteners, print rules | EU 49 = 15.6 mm; Gutekunst T-16324 torsion spring; PETG; insert and clearance values |
| [07_firmware_app_feasibility.md](07_firmware_app_feasibility.md) | Can firmware and app be built on this hardware? | yes; pin map, storage layout, BLE service sketch and risk register |
| [08_blue_board_mechanics.md](08_blue_board_mechanics.md) | How big is the blue PN5180 board really, where is its antenna, what do short range and metal do? | 69.6 x 38.6 x 1.6 mm, antenna centre 48.8 mm from the header end; reads are documented at 5-8 mm; metal under the tongue needs a test |
| [09_tonie_figure_dimensions.md](09_tonie_figure_dimensions.md) | How big are the four Pokémon Tonies? | the same black round foot of 45 x 15 mm under all four; 60-70 mm tall; nothing overhangs the foot by more than about 1 mm; the tag is an upright rod somewhere above the foot; the magnets are not located |
| [10_grass_look_and_small_parts.md](10_grass_look_and_small_parts.md) | How is tall grass drawn, how does it print, which plugs and screws fit? | clumps of broad lance-shaped blades; blunt tips and merged roots; 1.25 mm wire-to-wire 6-pin pairs; M3 countersunk ISO 10642 |

`reference_images/` holds the pictures that were measured for note 03 together with the measuring scripts, and in the sub-folders `tall_grass/` and `tonie_figures/` the pictures for notes 10 and 09. `downloads/` holds datasheets, drawings, source files and the Elechouse STEP model that the notes quote. `scripts/` holds the measuring scripts of notes 08 and 09. Both folders contain third-party, mostly copyrighted material (about 210 MB): keep them private and decide yourself whether they belong under version control.

## Decisions taken from the research

| Function | Chosen | Not chosen, and why | Note |
| --- | --- | --- | --- |
| Reader | the common blue PN5180 board, 69.6 x 38.6 mm (owner's choice, revision 2) | Elechouse PN5180 module (40 x 42 mm): chosen in revision 1, when the reader had to fit inside the ball. In the grass tongue its small size no longer counts, and it lacks the field reports of Tonie reads and the 2.54 mm pads. PN532, RC522, M5Stack RFID2: no ISO 15693. PN7150/PN7160: NCI firmware discovers tags before it lets raw commands through, which a privacy-mode tag never answers. ST25R3916, CR95HF, CLRC663, TRF7970A: capable, but no proven Tonie code path. | 02, 08 |
| Reader position | in the grass tongue in front of the ball, antenna centre under the standing spot, copper 1.7-3.3 mm below the figure's foot (owner's decision, revision 2) and, since the tongue is 15 mm high, 11.7 mm above the table (revision 3) | Under the flat on the underside (revision 1): 10.6 mm to the tag, and the ball had to be turned over to present a figure. Under the lid: the ring compartment lies in between. | 08; geometry of this design |
| Reader orientation | components down, plain side against the turf | Components up: the copper would be 1.6 mm closer to the tag, but the parts on the board need 1.8 mm of room above it, which means a step in the standing surface or a thicker turf. | 08 §0 |
| Joint of the tongue | the tongue alone (owner's decision, revision 3): 15 mm high, its rear end under the belly of the ball, four M3 x 16 countersunk screws from below into inserts in the bowl, underside in the plane of the ball's flat. Since revision 4 it is 72 mm wide at the ball and 66 mm at its round tip and reaches 70 mm beyond the ball (owner: a bit shorter, a tiny bit narrower, same height) | A ring with a cup round the foot of the ball (revision 2): the owner did not want grass round the ball. A thin tongue on a short flange: every push on the tip would act on a joint a few millimetres long; at 15 mm the tongue is 7 mm thick under its screws. Screws from inside the bowl: the tongue could not be taken off without stripping the ball. Glue: not serviceable. Magnets: they would hold the figure and disturb the hall switch. | 10 C2, C3 |
| Harness plugs | two 6-pin wire-to-wire pairs, 1.25 mm pitch (Molex PicoBlade type), 9.25 x 3.2 mm | JST PH: the series has no wire-to-wire part, and the in-line clones measure about 15 x 6 mm, too big to pass the hidden window mated. JST SH: wire-to-board only. A pin header on the reader: 8.5 mm tall, does not fit under the turf. | 10 C1 |
| Grass | tufts of two to seven broad, lance-shaped blades after Pokémon Let's Go; place, size, direction and leaf shape of every tuft drawn at random (owner's decision, revision 3); thin, and gathered in the two corners between the ball and the sides of the tongue, in the same light green as the tongue (owner's decisions, revision 4) | Two greens, bright blades on a darker ground (revisions 2 and 3): the owner wanted one colour. Tufts all round the standing place (revision 3): they cost width and length. Rows of like tufts along the edges and a ring of them round the ball (revision 2): the owner found them too symmetric. The needle grass of Sword/Shield and of the Pokémon GO icon (10-15 : 1): too thin to print at 8-20 mm and it reads as lawn. The two-blade tufts of the Game Boy tiles: too small a motif for a 16 mm blade. | 10 A |
| Standing spot | no mark (owner's decision, revision 4, with the risk accepted: "if it fails I will try to redesign just this part"). The round tip of the tongue is concentric with the spot and shows 10.5 mm of ground round a centred foot; that is the only cue | A disc in a second, brighter green, 1 mm deep and level with the turf (revisions 2 and 3): it needs a second filament. The same disc in the same green with another top-layer pattern: offered, not taken. Recess, rim or engraved ring: an inset, which the owner excluded. Magnet or steel disc under the spot: it would hold the figure, and the hall switch sits there. | 10 B2, 09 |
| Controller | Seeed XIAO ESP32-S3 Plus (16 MB flash) | XIAO ESP32-S3 (non-Plus) and QT Py ESP32-S3: too few pins for the 15 signals. Standard S3-Zero, S3 SuperMini, LOLIN S3 Mini: 4 MB flash. DevKitC-1, LilyGO T7-S3: too large. Classic ESP32 with A2DP: no advantage, live audio is not required. Fallback with easier soldering: Unexpected Maker TinyS3. | 04 §1, 07 §1 |
| Amplifier | MAX98357A on the battery rail | DFPlayer Mini: its SD card cannot be written from the controller, so the app could not upload messages. | 04 §2 |
| Speaker | Visaton K 40 (Ø40 x 4.3 mm, 83 dB) | K 28 WP: 8 dB quieter. BF 32, 40 mm 4 ohm types, K 45, K 50 WP: 15-21 mm deep. | 04 §3 |
| LED | one WS2812B on a Ø10 mm PCB | NeoPixel Jewel 7: Ø23 mm and seven times the current. Through-hole addressable LEDs: need 4.5 V or more. | 04 §4 |
| Wake | DRV5032FB hall switch under the standing spot, triggered by a magnet in the Tonie's foot and armed for the opposite state while a figure stays. By the owner's decision (revision 3) it is laid out for the magnets of the classic Tonies, because the Pokémon figures are sold for the first Toniebox too: its element lies 8-9 mm below the pole face. The reader's IRQ line is wired as a second way to wake, because the magnets in the Pokémon foot are not located | PN5180 low-power card detection as the only way: 35-220 µA in sleep instead of 1 µA, and reader firmware 4.0 or later; it is the prepared fallback. Vibration and tilt switches: no defined state in a ball. Reed switch: needs the field along its axis. | 04 §5, 07 §6.5, §6.6, 09 §7 |
| Position finding | the phone's GPS; the ball only blinks | GPS module in the ball (ATGM336H, NEO-6M, L76K): needs volume, current and sky view, and the owner's phone is present anyway. | 04 §8.1, 07 §5 |
| Cell | one unprotected flat-top 18650 in a printed cradle | Two cells: one gives 16-22 h of speech. Protected cells: up to 70 mm long. Commercial 77 mm holders: only fit on the centre plane. | 05 §2, §3 |
| Charging | TP4056 USB-C module with DW01A, socket in the black band | IP5306 boards: switch off below 45 mA load. Qi: the coil cannot get closer than about 10 mm in a sphere and its field is a hazard for NFC tags. Magnetic pogo pins: fallback. | 05 §4, §6 |
| 5 V | Adafruit MiniBoost (TPS61023) with enable | MT3608, Pololu U3V16F5: no load disconnect, so the 5 V loads would drain the cell in sleep. | 05 §4.3 |
| Servo | any SG90-class 9 g servo | Pocket and seat are sized for the spread between clones; an MG90S needs `SG90_*` values changed. | 05 §1 |
| Lid spring | Gutekunst T-16324 (0.7 mm wire, 33 N mm at 115°) | T-18460: stronger, but its 8.8 mm coil would push the hinge 2 mm forward and deepen the pocket in the band. Assortment springs: no data. Compression plunger: fallback, no hold-open force. | 06 §2 |
| Material | PETG for all parts | PLA: creeps under the spring preload and softens at 55-60 °C. ASA only if the ball may lie in a hot car. | 06 §5.7 |
| Exterior | single-colour shells plus a separate black band and bezel | Inlaid multi-colour band: about a hundred colour changes including black into white, with bleed at the most visible line. | 06 §5.5 |
| Proportions | the "thin band" family of the official replica | The thick-band family (0.10-0.12 D) of Let's Go and of fan models. | 03 |

## Corrections that the research made to the first assumptions

- The PN5180 board is not 65 x 40 mm. The 65 mm figure belongs to NXP's evaluation antenna. The blue hobby board is about 70 x 39 mm, the Elechouse board 40.0 x 42.3 mm [02 §1].
- The Tonie password is one value written in two byte orders: `0x7FFD6E5B` (Toniebox community firmware) and `0x5B6EFD7F` (Flipper Zero) both mean the bytes `5B 6E FD 7F` on air [01 §2, 02 §2.4].
- The unlock does not lapse when the field is removed. It is stored in the tag until a Toniebox or an explicit command locks it again [01 §3].
- CadQuery's `makeSphere` builds a hemisphere by default; this is noted in `geom.py` because it silently broke the first shells.
- The blue board is not 70 x 39 mm either: that is the sellers' rounded figure. Measured on photographs of two boards it is 69.6 x 38.6 mm, its holes are Ø3.3 and not Ø4, its antenna covers 40.9 x 37.7 mm and its tallest part is about 1.3 mm [08 §0, §10].
- JST PH connectors do not exist as a wire-to-wire pair; what is sold as such is a clone with a different housing [10 C1].
- The tag of a Tonie is not a flat inlay in the sole. It is an upright ferrite rod of about 10 x 4 mm, in classic figures 20 to 50 mm above the underside, and the magnets are cylinders of 6 x 6 mm, in the Creative Tonie one in each foot. The flat inlay with a centred 10 mm magnet in note 01 is the layout of replica bases [09 §7, §8].
- The four Pokémon Tonies stand on a black round foot of 45 mm, not on the 36 mm assumed in revision 1 [09 §3].

## Where the notes disagreed, and what was decided

| Topic | Notes | Decision |
| --- | --- | --- |
| LED supply | 04 prefers the battery rail, 05 and 07 the switched 5 V rail | 5 V rail through one series diode; data level is then in spec and the LED is off in sleep (`docs/electronics.md`) |
| Pin map | 04 sketches one, 07 derives another from wake and ADC rules | the map of note 07 |
| Wake button | 07 keeps an optional button | no button: the owner asked for a button that is only a light; the hall switch under the standing spot wakes the ball |
| Two chargers on one cell | 07 flags the XIAO's own charger | do not power both USB-C ports at once |
| Size of the blue reader board | 02 gives 70 x 39 mm with Ø4 holes, 08 measured 69.6 x 38.6 mm with Ø3.3 holes | the values of 08; the pocket also takes a board of 70.0 x 39.0 mm |
| Tag and magnet inside a figure | 01 describes a flat inlay and one centred 10 mm magnet, 09 an upright rod tag and 6 mm magnets in the feet | 09; note 01 had described replica bases. The antenna stays centred under the spot, and the wake has a second path |

## Not verified by any source

These are the open risks. The building manual puts them first, before anything is printed.

1. The tag type inside the 2026 Pokémon Tonies themselves. One forum screenshot shows UIDs beginning `E0 04 03 50` for three of them, which is SLIX-L; there is no second source and nobody has opened one [09 §8].
2. The read itself. The tag is a small rod somewhere inside the figure, in classic Tonies 20 to 50 mm above the underside, and nobody has published a read of a Pokémon Tonie with this board. What is published: classic Tonies read on 6 mm of plastic plus 2 mm of air above this antenna, and stickers at 5 mm; nothing at 2-4 mm, though no dead zone is reported for ISO 15693 [02 §3.1, 08 §7, 09 §8].
3. A read with the tongue standing on a metal table. Since revision 3 the antenna copper lies 11.7 mm above the table, a little more than the 10 mm that TI recommends; the estimate of note 08 gives a coupling of about 0.08 at 10 mm against 0.35 at the 3.5 mm of revision 2. A ferrite sheet on the floor of the pocket remains the remedy to try, and no source gives its right distance [08 §8].
4. The blue board has no dimensioned drawing. Outline, antenna position and part height were measured on photographs; the pocket has 0.5 / 0.35 mm of clearance per side [08].
5. The four figures themselves. Every size was measured on official pictures against the Toniebox 2 (foot 45 mm, +2 / -1.5). Not known at all: how high the tag sits in them, and number, position and polarity of the magnets in the black foot [09 §7, §8, §11]. The hall switch assumes the magnets of the classic Tonies (owner's decision). Measure a figure and find its magnets before printing.
6. Height of the XIAO Plus, connector overhang of the TP4056 module, and the servo horn: no dimensioned source. Marked `MEASURE` in `params.py`.
7. The ring. "Diameter 2.5 mm" was read as the band width; thickness and setting height are typical values.
8. Whether a stalled SG90 trips the cell protection, and how the servo behaves near 3.4 V.
9. BLE upload speed on the owner's phone, and the phone's operating system.
10. The strength of the printed grass blades (an estimate from tensile values) [10 B1].
11. How far from the unmarked spot a figure is put down by eye, and whether reader and hall switch still answer there. The layout counts on about 8 mm; the owner has accepted this risk (revision 4).
