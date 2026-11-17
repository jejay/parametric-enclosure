# Blue "PN5180-NFC" breakout (R1.1-170710): mechanical geometry for a flat tray

**Project:** 3D-printed flat tray (6-7 mm) holding the blue PN5180 board flat, Tonie figurine standing on a 1.4 mm skin above the antenna.
**Scope:** board mechanics, antenna position, short-range behaviour, metal/ferrite. Extends `research/02_rfid_reader_modules.md` §1A and corrects several of its numbers (see §10).
**Access / research date: 2026-11-17.**

Confidence tags: **[VERIFIED ≥2]** = two or more independent sources agree; **[single]** = one source only;
**[inference]** = my own measurement or calculation from primary data. A photo measurement on two different physical units counts as two sources.

**Important limit:** no manufacturer drawing and no caliper measurement by a user was found. All positions below come from
(a) two community CAD models that physically fit the board and (b) my own photogrammetry on photos of two to three different units,
scaled by the 2.54 mm header pitch. Measure your own board before the final print.

---

## 0. Values to use in CAD

**Board frame used everywhere in this file:** component side up, header at the left. Origin = corner at the header end next to pin 1 (+5V, square pad).
**x** runs along the long edge towards the antenna end, **y** runs across the board from the pin-1 long edge towards pin 13 (REQ).

```
 y=0  +--------------------------------------------------------------+  pin-1 long edge
      | [1]+5V      (o) mid hole            ._____________________.   |
      | [2]                                 |   4-turn loop       |(o)| antenna-end hole
      |  :   electronics (all parts)        |        (+) centre   |   |
      | [13]REQ     (o) mid hole            |_____________________|(o)|
y=38.6+--------------------------------------------------------------+
     x=0 (header end)                 x=25.9          x=48.8    62.9  69.6 (antenna end)
```

| # | Dimension | Value to use | Tolerance | Confidence / basis |
|---|---|---|---|---|
| 1 | Outline length (x) | **69.6 mm** | ±0.4 (sellers say "70") | **[VERIFIED ≥2]** photogrammetry on 2 units, §2 |
| 2 | Outline width (y) | **38.6 mm** | ±0.2 (sellers say "39") | **[VERIFIED ≥2]** 3 photos, 2 units, §2 |
| 3 | Corners | **square**, radius ≤ 0.3 mm, no chamfer | - | **[VERIFIED ≥2]** 2 units |
| 4 | PCB thickness | **1.6 mm** | ±0.15 | **[single]** kosla 1.65 + standard FR4; not re-measured |
| 5 | Mounting holes | 4 × plated through, **finished Ø 3.3 mm** (M3 clearance), plated ring outer Ø 3.9 | Ø ±0.15 | Ø **[inference]** (one unit); "M3 screw fits" **[VERIFIED ≥2]** |
| 6 | Hole raster | **34.0 mm** (mid pair) and **25.0 mm** (antenna-end pair), pair lines **37.0 mm** apart, both pairs on one centre line | ±0.15 | **[VERIFIED ≥2]** §3 |
| 7 | Mid pair centres | **x = 25.9**, **y = 2.3 and 36.3** | ±0.3 | **[VERIFIED ≥2]** 2 units |
| 8 | Antenna-end pair centres | **x = 62.9** (= 6.7 from the antenna-end edge), **y = 6.8 and 31.8** | ±0.3 | **[VERIFIED ≥2]** 2 units |
| 9 | Header | 1 × 13, pitch 2.54; row axis at **x = 2.6**; **pin 1 at y = 4.05**, pin 13 at y = 34.53 (row centred on the width); hole Ø ≈ 1.0, land Ø ≈ 2.3 | ±0.25 | **[single]** (kosla photo gives x = 2.3) |
| 10 | Antenna copper, outer extent | x = **28.3 ... 69.2**, y = **0.4 ... 38.1** (40.9 × 37.7 mm) | ±0.3 | **[VERIFIED ≥2]** 2 units |
| 11 | Antenna, inner clear window | x = 31.6 ... 66.0, y = 3.6 ... 34.9 (34.4 × 31.3 mm) | ±0.3 | **[VERIFIED ≥2]** 2 units |
| 12 | **Antenna centre = figurine axis** | **x = 48.8, y = 19.3** (20.8 mm from the antenna-end edge, on the board centre line) | ±0.5 | **[VERIFIED ≥2]** 2 units |
| 13 | Same point from the holes | **22.9 mm** from the mid-pair line and **14.1 mm** from the antenna-end pair line, on the raster centre line | ±0.3 | **[VERIFIED ≥2]** |
| 14 | Silkscreen dot of the "wave" symbol | x = 48.1, y = 19.3: it sits **0.7 mm on the header side of the true loop centre** | ±0.2 | **[VERIFIED ≥2]** 3 units |
| 15 | Antenna | 4 turns, component side only, trace ≈ 0.5 mm at 0.9 mm pitch, one short bridge on the back | - | **[VERIFIED ≥2]** |
| 16 | Component zone | all parts on the component side, within **x = 4 ... 28.5**; tallest part ≈ **1.3 mm** above the PCB | clearance ≥ 1.8 | height **[inference]**; zone **[VERIFIED ≥2]** |
| 17 | Back side | **no components**; soldermask over traces and vias only | allow 0.3 | **[VERIFIED ≥2]** §6 |
| 18 | Antenna half (x > 28.5) | no components on either side: flat on both faces | - | **[VERIFIED ≥2]** |

Derived suggestions **[inference]**: pocket 70.4 × 39.2 mm (accepts a board up to 70.0 × 39.0 with 0.1-0.2 play); locating pegs Ø 2.9-3.0 if pegs are used;
ferrite piece, if used, ≥ 45 × 42 mm centred on (48.8, 19.3).

---

## 1. Sources and method

### 1.1 Sources used

| Source | What it gives | Location |
|---|---|---|
| ATrappmann `PN5180-NFC.png` | blurred top photo, cropped inside the outline | `research/downloads/rfid_reader/ATrappmann_PN5180-Library/` |
| ATrappmann `PN5180_R1.1-170710_SCH.pdf` | schematic: part list, antenna symbol with one crossover, JP1 pin order | same directory |
| kosla photo `docs_images_pn5180.jpg` (unit A) | sharp oblique photo, header unpopulated, all corners visible | `research/downloads/rfid_reader/kosla_qalcosonic/` |
| kosla CadQuery model + validation JSON | 70.0 × 39.0 envelope, hole "estimate" table | same directory |
| lhm0 `PN5180_holder.stl` | holder for two boards with M3 screw holes and nut traps | `research/downloads/rfid_reader/lhm0_accessible_book_reader/` |
| lhm0 KiCad adapter PCBs | 13-pin footprint on a 14.224 × 39.0 mm adapter | same directory |
| Handsontec RC522 PDF | drawing with outline dimensions only (59.5 × 39) | `research/downloads/rfid_reader/alt_modules/handsontec_RC522.pdf` |
| **NEW** easyelecmodule listing photos (unit B) | two near-orthogonal top views (`3-26.png`, `1-50.png`), two back views (`7-10.png`, `5-26.png`), kit photo | `research/downloads/blue_board_mechanics/easyelecmodule_listing/` from https://easyelecmodule.com/product/pn5180-nfc-module/ |
| **NEW** Printables 1698547, SpoolSense scanner case | `top.stl` with four standoffs for the PN5180, BOM text | `research/downloads/blue_board_mechanics/printables_1698547_spoolsense_case/`, https://www.printables.com/model/1698547 |
| **NEW** Printables 1545289, "PN5180-tagomatic case" | STEP with the cavity that takes the board | `research/downloads/blue_board_mechanics/printables_1545289_tagomatic_case/`, https://www.printables.com/model/1545289 |
| **NEW** Würth ANP022 and ANP016 (mirror copies) | measured ferrite data | `research/downloads/blue_board_mechanics/wuerth_anp022_fsfs_selection/`, `.../wuerth_anp016_magnetic_shielding/` |
| **NEW** carrier-board README (text only) | mentions a "common red PN5180 module" | `research/downloads/blue_board_mechanics/hyiger_pn5180_carrier/README.md.txt` |
| forum.espuino.de threads 739, 1449, 1630, 3159, 4103, 4683, 4820, 4905 | field reports (German) | read through the Discourse JSON API |
| NXP AN11740, AN11564, TI SLOA241C | antenna, loading, metal, ferrite | `research/downloads/rfid_reader/nxp_docs/`, `.../ti_docs/` |

### 1.2 Two statements in the brief that the local files do not support

- The lhm0 KiCad adapter PCBs contain **no mounting holes**. They hold only the 13-pin footprint (drill 0.9 mm) and a 2 × 5 IDC header. Useful facts: adapter outline 14.224 × 39.0 mm, pin row centred on the 39 mm width.
- The Handsontec RC522 drawing dimensions **only the outline** (39 × 59.5). Hole positions can only be scaled from the drawing (§3).

### 1.3 How the photos were measured

- Features in the top copper plane were located to sub-pixel level (edge fits on the soldermask boundary, circle and ellipse fits on plated rings and pads).
- Scale comes from the header: 12 pitches = 30.48 mm. In the top views the pitch was taken from the soldermask gaps between pads, because the visible bores are shifted by parallax (bore pitch reads 0.5 % short).
- Perspective was removed with the vanishing line of the outline (top views) or with a homography through the four hole centres (oblique photo).
- Independent check: the mid-pair spacing came out as **34.00 and 33.99 mm** in the two top views, against 34.0 in two unrelated CAD models. The scale is therefore good to about 0.1 %.
- Remaining weakness: the top views do not fix the camera position, so **length** is uncertain by about ±0.3 mm, while **width** is not affected.
- The measuring scripts are kept in `research/scripts/note08_blue_board/` (written for a scratch directory, so the picture paths have to be given anew; `top_generic.py`, `top_profiles.py`, `ant_edges.py`, `hole_radial.py`, `k_homography.py`, `k_rectify.py`, `stl_info.py`, `step_info.py`).

---

## 2. Q1: outline and corner shape

| Source | Length | Width | Note |
|---|---|---|---|
| Seller text (alt-text and listings quoted in file 02) | 70 | 39 | rounded nominal **[VERIFIED ≥2]** as a claim |
| easyelecmodule spec table | 69 | 37 | **[single]**; the 37 does not match its own photos (ratio 1.80) |
| kosla mount (physically test-fitted) | 70.0 | 39.0 | envelope with 0.3 mm play per side, so it only proves "≤ 70.6 × 39.6" |
| tagomatic case STEP | - | cavity 40.0 | proves "< 40" **[single]** |
| Photo unit A (kosla), hole-raster homography | 69.4-69.8 | 38.6-38.8 | **[inference]** |
| Photo unit B top view `3-26.png`, pitch-scaled | 69.4-69.6 | 38.57-38.60 | **[inference]** |
| Photo unit B top view `1-50.png`, pitch-scaled | 69.8-69.9 | 38.53-38.59 | **[inference]** |
| RC522 + 1 cm (ESPuino maintainer, t/4103/5; RC522 = 59.5 × 39) | ≈ 69.5 | 39 | **[single]** |

- **Result: 69.6 × 38.6 mm.** "70 × 39" is a rounded seller figure. The earlier 70 × 39 in file 02 is about 0.4 mm too large in both directions. **[VERIFIED ≥2]**
- Length divided by the hole-pair distance is 1.880 (unit A) and 1.888-1.889 (unit B). With the pair distance at 37.0 this gives 69.6-69.9.
- **Corners are square.** High-zoom crops of both header-end corners (unit A) and all four corners (unit B) show no radius and no chamfer. **[VERIFIED ≥2]**
- Edges are routed, no break-off tabs or mouse bites visible on either unit. **[VERIFIED ≥2]**

---

## 3. Q2: mounting holes

### 3.1 Raster

| Source | Mid pair spacing | Antenna-end pair spacing | Distance between pair lines | Kind of evidence |
|---|---|---|---|---|
| lhm0 `PN5180_holder.stl` (holes at 28.5/5.0, 28.5/39.0, 65.5/9.5, 65.5/34.5) | 34.0 | 25.0 | 37.0 | CAD of a built holder, M3 screws + nut traps |
| SpoolSense case `top.stl` (standoffs at 166.397/136.449, 166.397/170.449, 203.397/140.699, 203.397/166.199) | 34.0 | **25.5** | 37.0 | CAD of a printed case, "4 × M3 x 4mm - Mount the PN5180 scanner board" |
| kosla validation JSON | 34.0 | 25.0 | **37.25** | labelled "estimate" by its author |
| Photo unit B `3-26.png` | 34.00 | 24.86-24.96 | 36.7-36.9 | photogrammetry |
| Photo unit B `1-50.png` | 33.99 | 24.96 | 36.99 | photogrammetry |
| Photo unit A (kosla), outline forced to 70 × 39 | 34.29 | 25.15 | 37.17 | photogrammetry (scale 0.9 % high because the outline is not 70 × 39) |
| RC522 drawing (Handsontec), scaled from 59.5 × 39 | 34.25 | 25.03 | 37.07 | pixel scaling of a line drawing |

- **Use 34.0 / 25.0 / 37.0.** The 25.5 of one case and the 37.25 of the kosla estimate are outliers of 0.25-0.5 mm; M3 screws in Ø 3.3 holes hide that. **[VERIFIED ≥2]**
- **Same raster as the RC522:** stated by the ESPuino maintainer ("Das Raster der vier Löcher zur Befestigung ist bei beiden Readern identisch", t/4103/5) and confirmed by the scaled RC522 drawing. The antenna-end pair is 6.8 mm from the antenna-end edge on both boards; the PN5180 is longer only at the header end. **[VERIFIED ≥2]**

### 3.2 Position on the board

| Quantity | Unit A (kosla) | Unit B `3-26` | Unit B `1-50` | Use |
|---|---|---|---|---|
| Mid pair x from the header-end edge | 25.76 | 25.84 | 25.97 | 25.9 |
| Antenna-end pair to the antenna-end edge | 6.81 | 6.82 | 6.85 | 6.7-6.8 |
| Mid holes to the long edges (pin-1 side / pin-13 side) | 2.56 / 2.14 | 2.19 / 2.40 | 2.16 / 2.38 | 2.3 / 2.3 |
| Antenna-end holes to the long edges | 7.06 / 6.64 | 6.85 / 6.88 | 6.69 / 6.88 | 6.8 / 6.8 |

- Both pairs share one centre line. That line lies within ±0.2 mm of the board centre line; the sign of the offset differs between the units, so treat it as routing tolerance. **[inference]**
- kosla's table (x = 26.0 and 63.25) is right to 0.1-0.35 mm; its "Ø ≈ 4" is the plated ring, not the bore.

### 3.3 Diameter

- Radial brightness profiles in the rectified top view: clear bore out to r ≈ 1.6-1.7 mm, plated ring out to r = 1.95 mm. **Finished hole Ø 3.3 ± 0.15 mm, ring Ø 3.9 mm.** **[inference]**, one unit.
- M3 hardware is used through these holes in two independent builds (lhm0: Ø 3.5 printed clearance with 5.8 mm hex nut traps; SpoolSense: M3 × 4 into Ø 2.9 pilot holes). **[VERIFIED ≥2]**
- So "Ø 3.2 like the RC522" is plausible as the drawn value but is **not confirmed**; I found no source that states the RC522 or PN5180 drill size.
- All four holes are plated with a narrow ring. The antenna-end holes are **inside** the loop (§5).

---

## 4. Q3: header

| Item | Value | Confidence |
|---|---|---|
| Type | single row, 13 positions, 2.54 mm, plated through holes, pin 1 = square pad at the "JP1" silkscreen corner | **[VERIFIED ≥2]** |
| Pin order from pin 1 | +5V, +3.3V, RST, NSS, MOSI, MISO, SCK, BUSY, GND, GPIO, IRQ, AUX, REQ | **[VERIFIED ≥2]** schematic + silkscreen |
| Row axis from the header-end short edge | **2.6 mm** (2.59-2.65 in both unit B top views; 2.33 in the oblique unit A photo) | **[single]**; ±0.25 |
| Pin 1 from the pin-1 long edge | **4.05 mm** if centred (measured 3.88-3.98 on unit B, 4.12 on unit A) | **[inference]**; ±0.2 |
| Pin 13 from the other long edge | 4.05 mm (measured 4.11-4.17 on unit B, 3.93 on unit A) | **[inference]** |
| Row centred on the width | yes within ±0.15 mm; lhm0's adapter PCB also centres the row on 39.0 | **[VERIFIED ≥2]** |
| Hole / land | hole ≈ 1.0 mm, round land ≈ 2.3 mm, lands almost touch | **[inference]** |

**Delivery state:** the board ships with the header **loose**.
- Kit photo of the easyelecmodule listing: bare board, one loose straight 1 × 13 strip, one white card, one blue key fob (`3-26.png`, `4-34.png`, `5-26.png`).
- kosla README: the header strip is "usually included with the PN5180 module"; their photo shows unpopulated pads.
- **[VERIFIED ≥2]** I found no listing of this board with a factory-soldered header. Only a straight strip was seen, no right-angle strip.
- Consequence: the side is your choice. In the ATrappmann photo the user soldered from the component side, so the plastic body and the long pins are on the back.
- For a 6-7 mm tray a straight header does not fit upright (body 2.5 mm + 6 mm pins, standard part). Solder wires directly or fit a right-angle header pointing away from the antenna.

---

## 5. Q4: antenna

| Item | Unit B `3-26` | Unit B `1-50` | Unit A (kosla) | Use |
|---|---|---|---|---|
| Outer copper edge, header-side leg (x) | 28.26 | 28.34 | 28.35 | 28.3 |
| Outer copper edge, far leg, distance to the antenna-end edge | 0.40 | 0.42 | ≈ 0.4 | 0.4 |
| Outer copper edge, pin-1 side (y) | 0.39 | 0.39 | not resolved | 0.4 |
| Outer copper edge, pin-13 side (y) | 38.05 | 38.14 | 38.0-38.1 | 38.1 |
| Inner copper edge, header-side leg (x) | 31.54 | 31.59 | 31.6-32.0 | 31.6 |
| Inner copper edge, far leg (x) | 66.00 | 66.24 | 65.8 | 66.0 |
| Inner copper edge, pin-1 side / pin-13 side (y) | 3.61 / 34.84 | 3.62 / 34.86 | 3.7 / 34.8 | 3.6 / 34.9 |
| Loop centre x | 48.76 | 48.93 | 48.8 | **48.8** |
| Loop centre y | 19.22 | 19.25 | 19.2 | **19.3** (centre line) |

- **4 turns**, counted on every leg in three photos and drawn as 4 turns in the schematic. **[VERIFIED ≥2]**
- Trace width ≈ 0.50-0.55 mm, pitch 0.90 mm, corners cut at 45°. **[inference]**, consistent on both units.
- **Outer size 40.9 × 37.7 mm, inner window 34.4 × 31.3 mm.** This matches the ESPuino library author's "Unserer Leser hat 4x4cm" (t/739/19). File 02's "~38 × 33" was too small. **[VERIFIED ≥2]**
- The loop runs 0.4 mm from three board edges. Any pocket wall or clamp on those edges touches board directly over antenna copper: use plastic only.
- **Layer:** the loop is on the component side. The back photos show a plain antenna half with one short link near the antenna-end edge. The top views show why: the turns step over by one pitch at the middle of the far leg, with two vias. The schematic shows the same single crossover. **[VERIFIED ≥2]**
- **Feed** is at the middle of the header-side leg, next to R3-R6 (2.2 Ω). The mid mounting holes sit just outside the loop at its chamfered corners.
- **The antenna-end mounting holes are inside the loop**, 18.8 mm from the loop centre (14.1 mm along x, ±12.5 mm along y).
- **Silkscreen dot:** 22.1-22.2 mm from the mid-pair line on three different units (unit A 22.23, ATrappmann photo 22.10, unit B 22.13/22.15). The loop centre is at 22.9-23.0. Do not centre on the dot if you want the copper centre; the difference is 0.7 mm. **[VERIFIED ≥2]**

---

## 6. Q5: component heights and back side

- **All components are on the component side.** Every designator of the schematic (C1-C36, R1-R15, L1-L3, Y1, U1, JP1) is printed on the top silkscreen, and both back photos of the listing show no parts. **[VERIFIED ≥2]**
- The back carries a ground pour with via stitching and a few signal traces under the electronics, all under soldermask. Allow 0.3 mm, and more at the header if you solder one.
- Components lie within x ≈ 4-28.5 mm. The antenna half is bare on both faces. **[VERIFIED ≥2]**

| Part | Position (x, y) | Height above PCB | Basis |
|---|---|---|---|
| C1, C2 (22 µF), C34, C35 (10 µF), L3: 0805-size bodies (≈ 2.0 mm long in the rectified top view) | ≈ 15-19, 9-18 | **≈ 1.25 mm, up to 1.45 with part tolerance: tallest** | **[inference]**: side face ≈ 1.4-1.6 × that of the QFN in `6-14.png`; an 0805 MLCC of 10-22 µF is normally 1.25 mm thick |
| U1 PN5180, HVQFN40 | ≈ 10-16, 17.5-24 | ≤ 1.0 mm | datasheet ordering table: "body 6 x 6 x 1.0 mm" (`nxp_docs/PN5180A0XX_C3_C4.pdf`) |
| Y1 crystal, metal lid | ≈ 6-8, 19.5-23 | ≈ 0.6-0.8 mm | **[inference]** from the photo |
| 0603 passives, L1/L2 | spread | ≈ 0.8-0.9 mm | package standard |

- **Use 1.3 mm as the tallest part and give at least 1.8 mm clearance.** Board plus parts ≈ 2.9 mm.
- This **disagrees** with the kosla JSON (`pcb_total_component_thickness 2.3`, i.e. 0.65 mm of parts). A 0.85 mm QFN alone exceeds that, so I do not use the kosla figure. Height was not measured with a caliper by anyone I could find. **[single / inference]**

---

## 7. Q6: behaviour at 2-6 mm

**Evidence that close ISO 15693 reading works on this board**

- ICODE stickers "bei ca 5mm Abstand zum Reader nicht 1 Heal" (no dropout at all), ESPuino t/4683/5, 2026-08-19. **[single]**
- Tonies read "absolut problemlos" through 6 mm ABS + 2 mm air while ISO 14443 cards failed at that gap, t/3159/6, 2024-12-05. **[single]**
- An original Tonie standing on the reader is polled continuously and successfully, t/1630/1. Wall thickness of that box is not stated. **[single]**
- The library author: "ISO-15693 Karten werden zuverlässig erkannt" while ISO 14443 cards drop out, t/739/10. **[single]**
- Together: reliable ISO 15693 reading at 5-8 mm is **[VERIFIED ≥2]**. **Nothing I found tests 2-4 mm explicitly.**

**Reports of trouble at very short distance**

- Only for **ISO 14443** cards and stickers: "je weiter weg die Karte, desto zuverlässiger die Erkennung" and "Hat der PN5180 evtl. einen blinden Punkt?", t/739/3 and /16. The library author answers that field hotspots "liegen aber nicht zwangsläufig direkt an der Antenne", t/739/17. **[single]**
- That case was traced mainly to the 5V pin being fed with 3.3 V and to library timing (t/739/33 and /38). Measured there: about 30 mA at 3.3 V and more than 50 mA at 5 V into the RF supply. **[single]**
- That current is far below the 250 mA limit of the chip, so the over-current risk that NXP describes for close loading (AN11740 §4.2.2) is remote on this board. **[inference]**
- The board copies NXP's "symmetrical" EMC filter (L1/L2 470 nH, 220 pF + 33 pF, cut-off 14.6 MHz), which NXP ties to a calibrated DPC and a larger antenna. Default settings are reported to be tuned for 6 × 6 cm antennas (t/739/19). The board is therefore not tuned for its own loop. **[inference + single]**

**Lateral offset**

- No user report with numbers was found. **[not verified]**
- AN11740 §3 (Fig. 15): there are "zero points ... slightly outside the antenna area" where "no tag device can be operated". The null ring lies just outside the 41 × 38 mm loop.
- A Tonie inlay (≤ 39 mm Ø, file 01) is as large as the loop, so coupling falls gradually with offset instead of dropping at an edge. I expect reading to survive roughly ±8-10 mm at 3 mm height. **[inference]**
- Design recommendation: centre the figurine within ±2 mm with a printed recess or ring. The centre magnet of the Tonie (≈ 10 mm Ø) over the loop centre is harmless: 10 mm magnets in tags work without loss, 15 mm magnets shield a 25 mm sticker (t/1449/5 and /35). **[single]**

---

## 8. Q7: metal table under the tray, ferrite

### 8.1 What the application notes say

| Statement | Source |
|---|---|
| Metal near the coil lowers inductance and Q, absorbs power and detunes; tags may become unreadable | NXP AN11564 §2.2; TI SLOA241C §1.2; Würth ANP016 §4 **[VERIFIED ≥2]** |
| "Recommended spacing ... between metal surfaces and the NFC/HF RFID antenna coil is 10 mm"; even then Q and range are reduced "to a manageable level" | TI SLOA241C §1.2 **[single]** |
| Metal loading lowers the antenna impedance, so transmitter current rises ("ITVDDloaded > ITVDDunloaded") | NXP AN11740 §4.2.2.2 **[single]** |
| A ferrite plane between coil and metal restores the operating distance to "its original open air level" (simulation, µr = 40) | NXP AN11564 Fig. 4 **[single]** |
| The ferrite itself causes "a fixed detuning"; the antenna must be measured and matched "with the ferrite already in place" | NXP AN11564 §2.2; TI SLOA241C §1.2 **[VERIFIED ≥2]** |
| Sheet must cover the antenna plus about 0.1 × its size, not much more; µr' > 40 and µr''/µr' < 0.1 at 13.56 MHz; thicker shields more | NXP AN11564 §2.2.1 **[single]** |
| A sheet directly on a PCB coil raises inductance from 8.4 µH to 12.8 / 13.6 / 14.2 µH (0.1 / 0.2 / 0.3 mm) | Würth ANP022 §4.1 (354 material) **[single]** |
| With WE-FSFS 364 between an RFID antenna and a 2 mm aluminium plate the resonance sits at about 12.1 / 11.4 / 11.0 MHz for 0.1 / 0.2 / 0.3 mm; "Correct thickness must be chosen in each application" | Würth ANP022 Fig. 6, read from the plot **[single]** |
| A gap between antenna and ferrite is a known way to soften the effect of the sheet | patent US 9,002,264, seen only as a search excerpt **[single, not opened]** |

### 8.2 What this means for the tray **[inference unless tagged]**

- In a 6-7 mm tray the antenna copper is about 3 mm under the top surface, so a metal table is only **3.5-5 mm below the copper**.
- Image-current estimate for this loop (mean 37.9 × 34.5 mm, 4 turns, about 1.4 µH): metal at 3.5 mm couples at k ≈ 0.35, at 5 mm k ≈ 0.26, at 10 mm k ≈ 0.08.
- Inductance therefore drops by roughly 26-35 % and the resonance rises by 16-24 %. The opposing image field also cancels most of the field at the tag: about 26 % of the free-air field remains on the axis 3 mm above the loop, before detuning losses.
- Expect the reader to lose most of its range on a metal table. Whether a tag at 3 mm still reads is open. It helps that ISO 15693 tags need only about a tenth of the field of ISO 14443 cards (standard minimum fields 0.15 A/m against 1.5 A/m; the 1.5 A/m figure is in AN11740 Fig. 14, the 0.15 A/m figure is from memory of the standard and was not re-checked).
- Field report with a similar reader board: an RC522 stacked over a main PCB read nothing until ferrite foil was inserted ("Bevor ich diese eingelegt hatte, konnte der RFID-Reader nichts lesen"), ESPuino t/4820. **[single]**

**Does a thin ferrite sheet help on metal?** Yes, that is its purpose, and the field report above shows it on a hobby board. **[VERIFIED ≥2]** as a principle, **[single]** for hobby boards.

**What does it cost on non-metal surfaces?**
- A sheet stuck directly to the back of the PCB is 1.6 mm from the copper. Würth's data imply +50-70 % inductance, i.e. a resonance near 10.5-11.5 MHz for a board that was matched without ferrite.
- This board has little damping (2 × 1.1 Ω in series, estimated Q around 30), so that much detuning costs a large part of the field.
- No source gives a range figure for an unmatched hobby board. **[not verified]**

**Is a spacer recommended?**
- No vendor note gives a gap in millimetres. The notes assume that you re-match the antenna, which is not practical here.
- For a fixed-match board the logical layout is: ferrite **on the tray floor**, i.e. as far below the antenna as the tray allows (3-4 mm), not on the PCB.
- At that gap my estimate is +15-25 % inductance in free air (resonance 7-11 % low) and a much smaller net shift on metal, because the two effects oppose each other.
- Start with 0.1 or 0.2 mm rather than 0.3 mm: Würth's plot shows thicker sheets over-compensating.

**Recommendation:** leave a 0.3-0.4 mm recess of about 45 × 42 mm in the tray floor under the antenna half. Test on wood and on a steel or aluminium sheet with (a) nothing, (b) 0.1 mm, (c) 0.3 mm. If metal still defeats it, add feet: 10 mm of air is the only remedy all three vendors agree on.

**Update for revision 3 (2026-11-17).** The tongue is now 15 mm high instead of 6.5 mm. The antenna copper lies 11.7 mm above the table, so the 10 mm of air named above are built in, and the estimate of this section gives k ≈ 0.08 at that distance instead of 0.35. No recess for ferrite was built. The floor of the pocket lies 5 mm under the board and takes a sheet if a test on metal asks for one. Nothing of this has been measured.

---

## 9. Q8: other points for the mechanical design

- **Which face up.** The loop is on the component side. With the component side down the flat back lies against the skin: copper is 1.4 + 1.6 = 3.0 mm from the standing surface and the parts need a 1.8 mm relief below x = 4-28.5. With the component side up the whole board must sit 1.8 mm below the skin, which gives a similar 3.2 mm. **[inference]**
- **No metal screws in the antenna-end holes.** They are inside the loop and under a 40 mm figurine base. Use printed pegs or edge clamps there; metal M3 screws are acceptable in the mid pair, which is outside the loop. **[inference]**
- **Nothing conductive between figurine and loop.** A PN5180 behind a small LED ring read no tags at all; a larger ring that does not cover the loop works ("Der Ring frisst definitiv Reichweite - die Karten werden aber auf 2cm erkannt"), t/4905. **[VERIFIED ≥2]** within that thread (three users).
- **Feed 5 V (or the cell voltage) to the 5V pin.** It supplies the RF stage; 3.3 V there is the commonest cause of marginal reads (t/739/33, t/3159/8). **[VERIFIED ≥2]**
- **Keep the cable short and away from audio lines**; users report read dropouts and audible clicks otherwise (t/4683/13, t/4103/22). **[VERIFIED ≥2]**
- **Unit-to-unit spread.** One user's board had far less range than its replacement ("Montagsmodell", t/3159/9), and the maintainer notes that "die Qualität der PN5180 haben wir auch nicht im Griff" (t/4683/2). Test the board before gluing anything. **[VERIFIED ≥2]**
- **Variants.**
  - The blue R1.1-170710 layout was identical on all three units examined (silk dot to hole raster within 0.1 mm). **[inference]**
  - A README of a carrier-board project speaks of "the common red PN5180 module" with the same first nine header positions. I could not find a photo or a drawing of it, so its outline is unknown. **[single]**
  - The Elechouse PN5180 is a different, smaller board (file 02 §1B). The NXP evaluation board is far larger. Neither fits this pocket.
- **Kit contents.** White card plus blue key fob (listing photos). A reseller review, seen only as a search excerpt, says the fob is ISO 14443 only while the card is ISO 15693. **[single, not opened]**
- **Bent boards.** kosla warns twice not to bow the PCB when clamping. Support the board on its edges or on the hole bosses, not in the middle of the antenna half. **[single]**

---

## 10. Corrections to `research/02_rfid_reader_modules.md` §1A (file 02 itself was not edited)

| File 02 says | This file finds |
|---|---|
| Outline ≈ 70 × 39 mm | 69.6 × 38.6 mm; "70 × 39" is a rounded seller figure |
| Holes "Ø ≈ 4 mm (estimate)" | bore Ø 3.3 mm, plated ring Ø 3.9 mm |
| Right pair at x ≈ 63.25 | x = 62.9; pair lines 37.0 mm apart, not 37.25 |
| Antenna "~38 × 33 mm" | copper 40.9 × 37.7 mm outer, 34.4 × 31.3 mm inner, 4 turns |
| Parts project ≈ 0.65 mm, some below the PCB | parts on the component side only, tallest ≈ 1.3 mm; back side empty |

---

## 11. What could not be verified

1. **Any dimension by caliper or manufacturer drawing.** None found. Everything in §0 is CAD-model or photo derived.
2. **Outline length to better than ±0.4 mm** (69.4-69.9 across the photos).
3. **Hole diameter.** Ø 3.3 comes from one unit's photo; Ø 3.2 nominal is neither confirmed nor refuted.
4. **Header row distance from the short edge:** 2.6 (unit B) against 2.3 (unit A).
5. **PCB thickness** was not re-measured (kosla 1.65).
6. **Tallest component height** (1.3 mm) is a photo ratio; the kosla model implies 0.65 mm.
7. **Reading at 2-4 mm.** Reports cover 5-8 mm and "standing on the box"; no explicit test at 2-4 mm, and no report of a dead zone for ISO 15693 either.
8. **Lateral tolerance.** No measured value; ±8-10 mm is my estimate.
9. **Metal at 3-5 mm and ferrite on this exact board.** All numbers in §8.2 are estimates; the only field report uses an RC522.
10. **Recommended antenna-to-ferrite gap.** No vendor figure exists in what I could open; the patent that describes a gap was seen only as a search excerpt.
11. **Research paper on ferrite thickness** (Universitat de València / IEEE 9139996) and the **Würth originals** could not be opened (HTTP 403); the Würth notes were read from mirror copies.
12. **The red PN5180 variant:** existence from one README only, geometry unknown.
13. **Thingiverse 7331650 and MakerWorld 2753906** (further PN5180 cases) could not be fetched (HTTP 403), so their hole patterns were not cross-checked.
14. **Whether sellers other than the one photographed also ship the header loose** in every case.

---

## Appendix: source list (accessed 2026-11-17)

**Local**
- `research/downloads/rfid_reader/ATrappmann_PN5180-Library/PN5180-NFC.png`, `PN5180_R1.1-170710_SCH.pdf`
- `research/downloads/rfid_reader/kosla_qalcosonic/` (photo, CadQuery source, validation JSON, README, assembly notes)
- `research/downloads/rfid_reader/lhm0_accessible_book_reader/PN5180_holder.stl` and the two `*.kicad_pcb` adapter files
- `research/downloads/rfid_reader/alt_modules/handsontec_RC522.pdf` (page 2)
- `research/downloads/rfid_reader/nxp_docs/AN11740_PN5180_Antenna_design_guide.pdf` (§3, §4.2.1.3, §4.2.2), `AN11564_PN7120_antenna_design.pdf` (§2.2)
- `research/downloads/rfid_reader/ti_docs/sloa241.pdf` (§1.2, §2.1)

**Downloaded for this file** (`research/downloads/blue_board_mechanics/`)
- `easyelecmodule_listing/` : https://easyelecmodule.com/product/pn5180-nfc-module/ (7 listing images)
- `printables_1698547_spoolsense_case/` : https://www.printables.com/model/1698547 (`top.stl`, `bottom.stl`)
- `printables_1545289_tagomatic_case/` : https://www.printables.com/model/1545289 (two STEP files)
- `wuerth_anp022_fsfs_selection/` : Würth ANP022, mirror https://static.chipdip.ru/lib/768/DOC016768902.pdf (original: https://www.we-online.com/components/media/o109046v410%20ANP022c%20EN.pdf)
- `wuerth_anp016_magnetic_shielding/` : Würth ANP016, mirror https://static.chipdip.ru/lib/921/DOC014921096.pdf
- `hyiger_pn5180_carrier/README.md.txt` : https://github.com/hyiger/pn5180_carrier

**Forum threads** (https://forum.espuino.de/t/NUMBER)
- 739 (stickers, close-range dropouts, supply), 1449 (magnets in tags), 1630 (Tonie on reader), 3159 (Tonies through 8 mm, weak unit),
  4103 (hole raster statement), 4683 (5 mm ICODE, 7 mm card distance, ferrite), 4820 (flat case, ferrite mandatory), 4905 (LED ring blocks reader)

**Download hygiene note:** the carrier-board repository shipped its own agent instruction files. They were treated as data, not followed, and deleted; only its README is kept, renamed to `.txt`.
