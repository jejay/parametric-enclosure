# 05 – Power, charging and servo: dimensions, compatibility, architecture

Access date for all web sources: **2026-11-17**.
Downloaded reference documents (untrusted, never execute): `research/downloads/power_servo/`.

Evidence labels used throughout:

- **[V3]** verified by three or more independent sources
- **[V2]** verified by two independent sources
- **[S1]** single source
- **[INF]** inference / calculation from sourced numbers
- **[UNV]** not verified in this research run (typical value from general knowledge, measure before relying on it)

Disagreements between sources are reported as min–max ranges, never averaged.

---

## 1. SG90-class 9 g micro servo

### 1.1 Sources

| ID | Source | Kind | Local copy |
|---|---|---|---|
| A | "SG90 9 g Micro Servo" datasheet with TowerPro drawing (identical copies at Uni Hamburg, UNL, U Tokyo, Wiltronics HA9740, Rapid 37-1330, friendlywire). Counts as ONE source. https://tams.informatik.uni-hamburg.de/lehre/2023ss/vorlesung/es/doc/sg90.pdf , https://static.rapidonline.com/pdf/37-1330t.pdf | distributor datasheet with drawing | `sg90_tams_hamburg.pdf`, `sg90_rapid_37-1330t.pdf`, `sg90_wiltronics_HA9740.pdf`, `sg90_utokyo.pdf` |
| B | TowerPro (manufacturer) product page, table A–F. https://www.towerpro.com.tw/product/sg90-7/ ; same table in https://www.rcscomponents.kiev.ua/datasheets/SG90_Digital-info.pdf | manufacturer | `sg90_rcscomponents_digital.pdf` |
| C | Kitronik 2565 "Mini 180 Degree Servo" dimension datasheet (SG90 clone, fully dimensioned). https://static.chipdip.ru/lib/261/DOC044261156.pdf | distributor drawing of a clone | `kitronik_2565_chipdip.pdf` |
| D | OpenSCAD MCAD library `servos.scad`, module `towerprosg90()` (community CAD model). https://github.com/openscad/MCAD/blob/master/servos.scad | community CAD | `mcad_servos.scad` |
| E | Feetech FS90 specification V1.0 (SG90-class, manufacturer drawing + electrical table). https://core-electronics.com.au/attachments/uploads/FS90-specs.pdf | manufacturer datasheet (different brand, same class) | `fs90_core_electronics.pdf` |
| F | M5Stack SG90 (A076) docs. https://docs.m5stack.com/en/accessory/SG90_Servo | distributor | – |
| G | ProtoSupplies SG90 listing with own bench measurements. https://protosupplies.com/product/servo-motor-micro-sg90/ | shop + measurement | – |
| H | York University micro-servo test page (datasheet currents of several SG90-type clones, hard-stop observations). https://www.yorku.ca/professor/drsmith/2026/06/03/microservotests/ | community test | – |
| I | Handson Technology SG90 user guide; friendlywire compilation. https://handsontec.com/dataspecs/motor_fan/SG90-Servo.pdf , https://www.friendlywire.com/projects/ne555-servo-safe/SG90-datasheet.pdf | distributor | `sg90_handsontec.pdf`, `sg90_friendlywire.pdf` |

Note: D and C share most numbers (22.7/15.9/2.5/4.7/5.9/4.6/3.2); D may be derived from the same clone drawing, so treat C+D as "1.5 sources". A, B, C and E are independent of each other.

### 1.2 Mechanical dimensions (mm)

| Dimension | A (generic datasheet) | B (TowerPro) | C (Kitronik clone) | D (MCAD model) | E (Feetech FS90) | Others | **Spread min–max** | Label |
|---|---|---|---|---|---|---|---|---|
| Body length | 22.2 | 22.7 (table B); 23 (text) | 22.7 | 22.5 | 23.2 | 23.0 (F), 23 (G), 22.0 / 23.1 (I) | **22.0–23.2** | V3 |
| Body width | 11.8 | 12.2 | 11.8 | 11.8 | 12.5 | 12.2 (F), 12 (G), 11.5 (I) | **11.5–12.5** | V3 |
| Base to top of main case | – | – | 22.7 | 22.7 | 23 | – | **22.7–23.0** | V2 |
| Base to top of gear case | – | 27 (C) | 26.7 | 26.7 | 27.3 | 26 (G, "housing H") | **26.7–27.3** | V3 |
| Base to tip of output spline (no horn) | – | 30.3 (A); "29" in text | 29.9 | 29.9 | – | 29.0 (F, I) | **29.0–30.3** | V3 |
| Total height incl. horn + screw | 31 | – | – | – | – | 32 (G) | **31–32** | V2 |
| Flange (tab) overall span | 32.2 | 32.3 (E) | 32.1 (22.7 + 2 × 4.7) | 31.9 | 32.6 | 32 (G) | **31.9–32.6** | V3 |
| Tab length beyond body, each side | 5.0 (derived) | 4.8 (derived) | 4.7 | 4.7 | 4.7 (derived) | – | **4.7–5.0** | V3 |
| Flange thickness | – | – | 2.5 | 2.5 | 2.4 | – | **2.4–2.5** | V2 |
| Flange underside above base | 16 (which face not stated) | 17 (F, face not stated) | 15.9 | 15.9 | 16.4 | – | **15.9–16.4** (17 if B refers to the underside) | V3 |
| Flange top above base | – | – | 18.4 | 18.4 | 18.8 | – | **18.4–18.8** | V2 |
| Mounting hole diameter | – | – | 2.0 | 2.0 | 2.0 (2-R1.0) | – | **2.0** | V3 |
| Slot from hole to tab end | – | – | 1.3 wide | 1.3 wide | shown | – | 1.3 | V2 |
| Mounting hole spacing (centre–centre) | – | – | not dimensioned; ≈27.4 if hole is centred in the 4.7 tab [INF] | 27.1 | **27.0** | "27.5–28" is often quoted on the web but was NOT found in any drawing | **27.0–27.4** (27.5–28 unverified) | V2 / UNV |
| Output shaft axis from near body end | – | – | 5.9 | 5.9 | ≈ 6 (on the centre of the Ø11.8–12.5 round) | – | **5.9–6.3** | V2 |
| Output shaft axis from near tab end | – | – | 10.6 | 10.6 | – | – | 10.6 | V2 |
| Shaft across width | centred | centred | centred (3.6 from each side of the Ø4.6 spline) | centred | centred | – | centred | V3 |
| Gear-case round around shaft | – | – | Ø11.8 | Ø11.8 | full width | – | Ø11.8–12.5 | V2 |
| Idler-gear boss on gear case | – | – | Ø5, end 9.0 from shaft axis | Ø5, end 8.8 from axis | shown | – | end 8.8–9.0 from axis | V2 |
| Spline outer diameter | – | – | 4.6 | 4.6 | 4.8 (R2.4) | 4.8 (RobotShop, MakerWorld table), 4.9 (caliper, Turnigy TG9z, RCTech forum) | **4.6–4.9** | V3 |
| Spline tooth count | – | – | – | – | **20T** | **21T** (M5Stack; RobotShop forum; MakerWorld horn table) | **20T vs 21T – conflict** | – |
| Horn screw hole in shaft | – | – | Ø1.7 | – | – | "centre hole 2.5" for the horn (RobotShop) | Ø1.7 (S1) | S1 |
| Spline length above gear case | – | 3.3 (A − C) | 3.2 | 3.2 | – | – | 3.2–3.3 | V2 |
| Cable exit | drawing: near the bottom of the end face on the shaft side | – | – | 3.6 × 1.2 flat ribbon, 4.5–5.7 above base, on the shaft-side end face | drawn at the bottom | – | shaft-side end face, ≈ 4.5–6 above base | V2 |
| Cable length | – | 250 | – | – | 200 ± 5 | 240 (G), 248 / 150 (I) | **150–250** | V3 |
| Weight | 9 g | 9 g | – | – | 9 ± 0.2 g | 9 g (F); 10.6 g incl. lead (I) | **9 g body, ≈10.6 g with lead** | V3 |

Interpretation of TowerPro's letters A–F is an inference (the page shows only a picture): A = overall height incl. spline, B = body length, C = height to top of gear case, D = width, E = flange span, F = base to flange. This reading matches the well-known MG996R numbers in the same TowerPro table format. **[INF]**

### 1.3 Horns

Included: three (sometimes four) white POM/nylon horns – single arm, double arm, cross (source A, B, I: "comes with 3 horns (arms) and hardware"). **[V3]**

**Horn dimensions could not be verified from any dimensioned source in this run.** Typical values **[UNV]** – measure the delivered parts before modelling the latch linkage:

- single arm: ≈ 19–21 mm centre-to-tip, hub Ø ≈ 7 mm, ≈ 4 mm wide at the tip, 5–7 holes Ø ≈ 1 mm at ≈ 2 mm pitch, outermost hole ≈ 14–16 mm from the axis, hub height ≈ 4 mm, arm thickness ≈ 1.5 mm
- double arm: ≈ 32–36 mm tip-to-tip
- cross: ≈ 32 mm × 14–18 mm

Recommendation: do not design the latch around the stock horn geometry. Print a custom horn/cam with a spline bore (Ø 4.8 nominal, 21T, test-print a fit gauge at 4.6 / 4.7 / 4.8 / 4.9), or clamp the stock single arm in a printed pocket. A replacement-horn CAD model exists (section 9).

### 1.4 Electrical

| Parameter | Values found | Label |
|---|---|---|
| Rated supply | 4.8 V nominal (A, B); 4.8–6.0 V (E, F, G; TowerPro admin: "4.8–6 V is fine") | V3 |
| Claimed wider ranges | "3.0–7.2 V", "4.0–7.2 V", "3.3 V (~6 V)" appear on retail listings / modified datasheet copies (I, U Tokyo copy) | S1 each, not manufacturer-confirmed |
| Stall torque @ 4.8 V | 1.8 kg·cm (A, B) / 1.6 (F) / 1.3 (E) / 1.2 (I, retail) / 1.7 measured (G) | **1.2–1.8 kg·cm** |
| Speed @ 4.8 V | 0.10–0.12 s/60° | V3 |
| Stall current | 360 mA measured, generic SG90 (G); 700 mA @ 4.8 V / 800 mA @ 6 V (E datasheet); 500–750 mA (Miuzei MS18 datasheet via H); < 800 mA (DFRobot DF9GMS via H); "650 ± 80 mA" (forum-quoted datasheet) | **0.36–0.8 A → design for 0.8 A** |
| Idle current (powered, holding, no load) | 5 mA @ 4.8 V / 6 mA @ 6 V (E); 10 mA typical (G); "< 40 mA" (clone datasheets via H) | **5–10 mA typical** |
| Running current, no load | 100 mA @ 4.8 V / 120 mA @ 6 V (E); 100–250 mA while moving (G) | **100–250 mA** |
| PWM frame | 50 Hz (20 ms) | V3 |
| Pulse range | 1.0–2.0 ms (A, F, G) vs 0.5–2.4 ms (I, U Tokyo copy) vs 0.9–2.1 ms = 120° (E) | conflict |
| Dead band | 10 µs (A, E) / 1 µs (B "digital") / 4 µs (F) | – |

**Is it really 180°?** Not reliably.

- TowerPro (manufacturer comment on the product page): "all of our normal servos are operating 0–150 degrees unless specify 180 or 360". **[S1]**
- Feetech FS90: 120° for 900–2100 µs, mechanical limit angle listed as 120. **[S1]**
- ProtoSupplies: rated 180° ± 15°, actual range often less; recommends using 20–160° and warns that driving into the end stop causes stall current and stripped gears. **[S1]**
- York U tests: clone hard stops ranged from ≈ 200° to oddly inconsistent values; pulse limits vary between units of the same batch (also Hackaday). **[S1]**

Design consequence: the latch mechanism should need **≤ 90° of travel** (ideally 45–60°), with end points calibrated per unit in firmware, and must never rely on a mechanical end stop of the servo.

**Behaviour at 3.7–4.2 V (direct from the cell):** no measured data found. **[UNV]** Rated minimum is 4.8 V. Torque and speed scale roughly with voltage **[INF]**, so expect ≈ 75–85 % of the 4.8 V figures at 3.7–4.2 V, and less as the cell sags under the servo's own load. One forum report at 3.3 V: neutral worked but only ± 45° was reached (EDABoard). Recommendation: run the servo from the switched 5 V boost, not from the cell.

### 1.5 MG90S (metal gear) differences

| Dimension | SG90 (TowerPro B) | MG90S (TowerPro, https://www.towerpro.com.tw/product/mg90s-3/) | Delta |
|---|---|---|---|
| A overall height incl. spline | 30.3 | 32.5 | + 2.2 |
| B body length | 22.7 | 22.8 | + 0.1 |
| C to top of gear case | 27.0 | 28.4 (text: 28.5) | + 1.4 |
| D width | 12.2 | 12.4 (text: 12.2) | + 0.2 |
| E flange span | 32.3 | 32.1 | − 0.2 |
| F base to flange | 17.0 | 18.5 | + 1.5 |
| Weight | 9 g | 13.4 g | + 4.4 g |
| Torque | 1.8 kg·cm @ 4.8 V | 1.8 @ 4.8 V, 2.2 @ 6.6 V | – |
| Stall current | 0.36–0.8 A | 700 mA measured (ProtoSupplies MG90S page) | higher |

Label: dimensions **[S1]** (manufacturer), stall current **[S1]**. The same spline class (21T, Ø 4.8) is listed for MG90S in the MakerWorld horn table. To keep both options open, make the pocket below the flange ≥ 19 mm deep and allow 14.5 mm above the flange underside to the spline tip.

---

## 2. 18650 cells

### 2.1 Dimensions and ratings

| Cell | Capacity typ / min | Max continuous discharge | Diameter | Length | Weight | Cut-off | Sources | Label |
|---|---|---|---|---|---|---|---|---|
| Samsung INR18650-35E | 3500 nominal / 3350 min | 8 A (13 A non-continuous) | max 18.55 (shop: 18.55 ± 0.1) | max 65.25 (shop: ± 0.15) | max 50 g (shop 48 ± 1) | 2.65 V | Samsung SDI spec v1.0 (`samsung_35E_mikrocontroller.pdf`, https://mikrocontroller.net/attachment/476470/Samsung__35E.pdf); Akkuteile listing; lygte-info | V3 |
| LG INR18650-MJ1 | 3500 / 3400 | 10 A | 18.2 (Nkon) – 18.41 (seller measurement) | 65.0–65.1; button-top version 66.1 | 47–49 g (max 49.0) | 2.5 V [UNV] | lygte-info (official spec lines), Nkon listing, marketplace seller. Manufacturer datasheet not retrieved | V2 (shops) |
| Molicel INR18650-M35A | 3500 / 3350 | 10 A | max 18.6 (shop 18.45 ± 0.15) | max 65.2 (shop 65.0 ± 0.2) | max 48 g (shop 47 ± 1) | 2.5 V | Molicel datasheet (`molicel_m35a.pdf`, https://www.molicel.com/wp-content/uploads/INR18650M35A-V2-80096.pdf); Akkuteile | V2 |
| Panasonic NCR18650B | 3350 typ / 3250 min (3200 rated) | 4.87 A (retail figure, not in datasheet) | max 18.5 (typical 18.25 quoted) | max 65.3 (typical 65.10 quoted) | max 48.5 g (typ 47.5) | 2.5 V | Panasonic datasheet (`ncr18650b_batteryjunction.pdf`); retail | V2 |
| Panasonic/Sanyo NCR18650GA | 3450 typ / 3350 min (3300 rated) | 10 A | 18.5 | 65.0–65.2 | 46.5–48 g (official < 49.5 g) | 2.5 V [UNV] | lygte-info, Digitec, marketplace seller | V2 (shops) |
| Sony/Murata US18650VTC6 | 3120 typ / 3000 rated | 15 A (30 A with temperature cut) | max 18.50 | max 65.20 (drawing 65.0 ± 0.2) | 46.5 g average (46.4 ± 1.5) | 2.0–2.5 V | Sony spec (`vtc6_kronium.pdf`); lygte-info | V2 |
| Protected example: Keeppower P1835K / P1835J / P1835U (USB) | 3500 | 10 A (PCB limited) | 18.6 / 18.65 / 18.5 | **69.0–69.1 / 68.9–69.25 / 70.2** | ≈ 50 g [UNV] | PCB ≈ 2.5 V | Keeppower site, Nkon, Illumn | V2 |

### 2.2 Envelope rules for CAD

- Unprotected flat-top: Ø ≤ 18.6, length ≤ 65.3. **[V3]** Use a 19.0 mm bore / cradle radius 9.5.
- Unprotected button-top: about + 1 mm (MJ1: 66.1 vs 65.1). **[S1]**
- Protected (button-top with PCB): Ø up to 18.65–18.8, length **68.2–70.2**. **[V2]**
- Weight 45–50 g.

### 2.3 Which cell

For this load profile (≤ 1.5 A battery-side peaks, long standby) every cell in the table is far above the requirement. Pick by capacity and availability: **Samsung INR18650-35E or Molicel INR18650-M35A, unprotected, flat-top**. VTC6 gives nothing here except less capacity. Protected cells are not needed when the charger board carries DW01A protection, and they cause holder-fit problems (section 3.3).

Do not plan two cells in parallel with user-swappable cells: inserting two cells at different states of charge produces large equalising currents. One cell is sufficient (section 5).

Reputable EU shops: **Akkuteile.de** (listings for 35E, M35A, NCR18650GA confirmed, with dimension tolerances), **Nkon.nl** (listings for 35E, MJ1, M35A, Keeppower protected confirmed via search; site blocks automated fetch). Reichelt, Conrad and Eckstein carry cells too but were not checked individually. **[UNV]**

---

## 3. 18650 holders and contacts

### 3.1 Dimension table (mm)

| Part | Length | Width | Height | Mounting / contacts | Source | Label |
|---|---|---|---|---|---|---|
| Keystone 1042 / 1042P (SMT, leaf springs, gold flash) | 77.1 body (3.034"); **86.0 over SMT tabs** | 20.7 (.813"); KiCad/distributors: 20.65 | **18.0 (.709") in the catalogue end view; distributors list 14.86 or 15.11 – conflict** | pads 7.5 × 6.5 at ± 39.69 from centre (KiCad); locating pegs Ø 2.39 / 3.45; cell cavity 68.9 (2.710") | Keystone catalogue M65 p.27 (`keystone_m65p27.pdf`, https://www.keyelco.com/userAssets/file/M65p27.pdf); KiCad footprint `BatteryHolder_Keystone_1042_1x18650`; DigiKey/Octopart parametrics | V3 (L, W); height unresolved |
| Keystone 1043 / 1043P (THT leaf springs, tin-nickel), 1044 (solder lugs) | 77.1 | 20.7 | 18.0 (same drawing) / 14.86–15.11 (distributors) | PC pins 71.6 apart (2.822"), pin Ø 1.57 × 3.3 long; pegs 55.2 apart (2.175"), Ø 3.7 | same catalogue page; Rapid listing "77 × 20.65 × 14.86" | V2 |
| MPD BH-18650-PC (THT) | 77.7 | 20.9 | 21.31 above board (DigiKey) | pins 72.9 apart, drill 1.57; mounting holes Ø 3.2, 55.61 apart | KiCad footprint `BatteryHolder_MPD_BH-18650-PC`; DigiKey | V2 |
| MPD BK-18650-PC2 | 76.96 | 20.98 | – | same pin pattern | KiCad footprint | S1 |
| Comf BHC-18650-1P (the common black PBT holder with PCB pins; sold by Electrokit) | 75.0 ± 0.5 | 21.0 ± 0.5 | not legible in the datasheet | pins 71.4 ± 0.5 apart, 3.3 ± 0.5 long; mounting holes 2 × Ø 3.0, 53.7 ± 0.3 apart | `electrokit_holder_tds.pdf`, https://electrokit.com/upload/quick/e3/73/4234_41022169-tds.pdf | S1 |
| Generic black holder, wire leads – Berrybase | 76 | 21 | 18 | leads ≈ 13 cm | https://www.berrybase.de/en/batteriehalter-fuer-1x-18650-mit-anschlusskabel | S1 |
| Generic – Nkon | 77.5 | 21 | 21.5 | "only standard cells without protection circuit" | https://www.nkon.nl/novat/1x-18650-batterijhouder-met-klemmen-en-losse-draden.html | S1 |
| Generic – Tinytronics | 77 | 22 | 20 | accepts cells with and without protection | https://www.tinytronics.nl/shop/nl/batterij-en-accu/batterijhouders/1x-18650-batterij-houder-met-losse-draden | S1 |
| Generic – Purecrea / Bastelgarage | 77.5 | 21 | 22.3 | contact springs 62.8 apart | https://www.bastelgarage.ch/1-slot-18650-battery-case-battery-holder | S1 |
| SparkFun PRT-12899 | 74.5 | 21.5 | 17.7 | a ≈ 70 mm protected cell barely makes contact | https://sparkfun.com/products/12899 | S1 |

**Verdict on "≈ 77 × 21 × 19–21":** correct as an order of magnitude, but clones spread over **L 74.5–77.7, W 20.65–22.0, H 17.7–22.3**. The listed "height" is inconsistent between sellers (holder body only vs. including the seated cell). With a cell seated, the top of the cell sits ≈ 20–22 mm above the holder base regardless of the body height. **[INF]** Buy the holder first, then measure; or model for the worst case 78.5 × 22.5 × 23.

### 3.2 Spring clips and discrete contacts

| Part | Dimensions (mm) | Notes | Source | Label |
|---|---|---|---|---|
| Keystone 54 (THT PC battery clip, "A" / 17–19 mm cells; 18650 explicitly listed) | A 8.9, B 9.5, C 9.8, D 1.6, **H 16.6, L 7.6, W 11.1**, material 0.30 spring steel, tin-nickel | A clip that grips the cell body. With a sleeved Li-ion cell it is a mechanical retainer, not an electrical contact | Keystone catalogue M65 p.11 (`keystone_m65p11.pdf`) | S1 (manufacturer) |
| Keystone 254 (SMT version) | H 16.61 × L 11.13 (GlobalSpec listing) | tape-and-reel variant 254TR | distributor listing | S1 |
| Keystone 209 / 228 | – | Keystone lists these as A/AA spring and button contacts (0.30 / 0.25 spring steel, nickel plate). Not 18650-specific; no dimensioned drawing retrieved | DigiKey-hosted catalogue excerpt | UNV |
| Generic nickel-plated "18650 SMT/THT battery clips" (e.g. MYOUNG MY-18650-02, LCSC C2979182) | – | exist, no dimensions retrieved | LCSC/JLCPCB listing | UNV |

### 3.3 Contact and fit problems

- Protected cells in standard holders: a 74.5 mm holder barely accepts a ≈ 70 mm cell (SparkFun comments); forcing protected cells in flattens the springs so that normal cells no longer make contact (Core Electronics forum); some generic holders are explicitly "unprotected only" (Nkon). Keystone 1042/1043 are specified for cells "with or without built-in PCB protection circuits". **[V2]**
- Momentary disconnects: if the housing grips the cell tightly, the end springs cannot follow the cell, so a bump slides the cell off one contact (PIClist report). A DigiKey forum measurement of an MPD holder gave ≈ 63 mm contact spacing, i.e. only ≈ 2 mm preload on a 65 mm cell. **[S1 each]**
- High-current heating of holder contacts is real but irrelevant here (lygte-info melted a holder at 15 A; this design peaks at ≈ 1.5 A).
- Contact resistance of spring holders: no measured value found. **[UNV]** Budget 20–100 mΩ.

Mitigations: leaf-spring holder (Keystone 1042/1043) rather than coil spring; a printed strap or foam pad that presses the cell into the holder so a drop cannot unseat it; flat-top unprotected cell; bulk capacitance on the battery rail (rides through sub-millisecond bounce only – at 100 mA load, 470 µF holds 0.3 V of droop for 1.4 ms **[INF]**).

### 3.4 Fit inside the sphere (inner radius 45 mm) **[INF]**

- A 77 × 21 × 21 box (holder with cell), centred on the sphere centre, has a half-diagonal of 41.3 mm: it fits with 3.7 mm margin. It can be shifted off-centre along its height by at most ≈ 10 mm before a corner touches the wall. The holder therefore pins the layout to the equatorial region.
- Keystone 1042 with its SMT tabs (86.0 long) only fits if its tab plane is within ≈ 13 mm of a diameter; the THT 1043 (77.1) is easier.
- A bare cell (65.25 × Ø 18.55) in a printed cradle with ≈ 3 mm of contact + wall at each end (≈ 71.3 total) can have its axis up to ≈ 18 mm away from the centre. A printed cradle with discrete end contacts buys ≈ 8 mm more placement freedom than a 77 mm commercial holder, at the price of designing the contacts yourself.

---

## 4. Charging, protection, boost, 3.3 V

### 4.1 TP4056 USB-C module with DW01A + FS8205A

| Item | Value | Source | Label |
|---|---|---|---|
| Board size (USB-C version) | 28 × 17 × 4 (ShillehTek manual); 29 × 17 (Purecrea/Digitec); 29 × 18 × 4 (Berrybase, TC4056A); 16.5 × 28 (OpenELAB) → **28–29 × 16.5–18 × ≈ 4** | vendor listings | V3 |
| Other variants | micro-USB version ≈ 26 × 17 [UNV]; a DW01 listing at 25 × 19; Soldered/Electrokit protected charger 38 × 22 | listings | S1 each |
| Pads | IN+ / IN− beside the USB connector; B+ / B− (cell) and OUT+ / OUT− (load, behind the protection) at the opposite edge. Load must go to OUT±, not B±. Exact pad order: verify on the delivered board | vendor manuals (ShillehTek, Cirkit Designer) | V2 (names), UNV (order) |
| Charge current | set by R_PROG; boards ship with 1.2 kΩ = 1 A | TP4056 datasheet (`tp4056_sparkfun.pdf`) | V2 |
| R_PROG table | 10 k → 130 mA; 5 k → 250; 4 k → 300; 3 k → 400; 2 k → 580; 1.66 k → 690; 1.5 k → 780; 1.33 k → 900; 1.2 k → 1000 mA | TP4056 datasheet | S1 (manufacturer) |
| Termination | 4.2 V ± 1.5 %, terminates at C/10 of the programmed current; trickle below 2.9 V; automatic recharge | TP4056 datasheet | S1 |
| TP4056 drain on the cell | BAT pin < 2 µA in sleep/disabled mode (no USB); 2.5 µA typ / 6 µA max in standby with USB present | TP4056 datasheet | S1 |
| DW01A supply current | 3.0 µA typ, 6.0 µA max | DW01A datasheet (`dw01a_hmsemi.pdf`) | S1 |
| Module quiescent (vendor claim) | "< 6 µA" | ShillehTek manual | S1, unmeasured |
| Over-discharge cut-off | **2.40 V ± 0.10 V**, release at 3.0 V ± 0.1 V, delay 40–200 ms | DW01A datasheet | S1 |
| Over-charge cut-off | 4.30 V ± 0.05 V, release 4.10 V | DW01A datasheet | S1 |
| Over-current | trips at 150 mV ± 30 mV across the FET pair; FS8205A R_DS(on) ≤ 25 mΩ per FET at V_GS 4.5 V, ≤ 35 mΩ at 2.5 V → ≈ 2.1–3.0 A trip at the nominal 150 mV, **≈ 1.7 A in the worst case** (120 mV, 2 × 35 mΩ) **[INF]**; over-current delay 10–20 ms; short-circuit threshold 1.2 V typ | DW01A + FS8205A datasheets (`fs8205a.pdf`) | S1 + INF |

Assessment:

- **2.4 V cut-off is too low to be the working cut-off.** Cell datasheets specify 2.5–2.65 V as the absolute discharge end; routinely going there costs cycle life. Treat DW01A as a last-resort safety. The firmware must stop at ≈ 3.3 V (resting) and go to deep sleep; in practice the 3.3 V regulator's dropout forces this anyway.
- **Charging with the load connected:** TP4056 has no power-path. The load on OUT± is in parallel with the cell, so the charger cannot distinguish load current from charge current. If the load draws more than C/10 (100 mA at the 1 A setting) continuously, the charge never terminates and the cell is held at 4.2 V. In deep sleep (µA) or light idle, termination works normally. Rule: do not play audio or poll RFID for hours while on the charger, or accept that "full" is not indicated. True load sharing needs an extra MOSFET or a power-path charger. **[V2]** (vendor manual + datasheet behaviour)
- **Heat:** TP4056 is linear. At 1 A into a 3.6 V cell it dissipates ≈ (5 − 3.6) × 1 = 1.4 W on a 28 × 17 mm board inside a closed printed sphere. **[INF]** Recommendation: change R_PROG to 2.0–2.4 kΩ (≈ 0.5–0.58 A, ≈ 0.7 W, ≈ 7–8 h for 3350 mAh) and keep the module away from PLA walls.
- **Over-current margin:** the worst-case DW01A trip (≈ 1.7 A, after 10–20 ms) is only ≈ 15–30 % above the calculated servo-stall battery current of 1.3–1.5 A (section 5.1). A trip cuts OUT± and resets the whole device. This is a second reason to forbid stalls and concurrent loads in firmware, and to measure the real stall current of the purchased servo. **[INF]**
- **Known quirks to test on the bench [UNV]:** (a) after inserting a cell, a DW01A board may stay in lock-out until USB power is applied once – relevant for a swappable cell; (b) some USB-C TP4056 boards lack the 5.1 kΩ CC pull-downs, in which case USB-C-to-C chargers do not supply power (USB-A-to-C cables still work).

### 4.2 Integrated charge + 5 V boost modules

| Module | Size (mm) | Charge / output | Standby / quiescent | Enable / auto-off | Source | Label |
|---|---|---|---|---|---|---|
| IP5306 (IC) | eSOP8 | 2.1 A charge, 5 V 2.1 A boost (table in datasheet lists 2.4 A charge) | battery standby 50 µA typ (headline "< 100 µA"); 3 mA battery operating current with boost on | **auto-off: load continuously below 45 mA for 32 s → standby.** KEY: short press on, double press off | IP5306 datasheet v1.10 (`ip5306_electrokit.pdf`) | S1 (manufacturer); the "≈ 50 mA" figure in the task is 45 mA in the datasheet |
| MH-CD42 (IP5306 board) | 16 × 25 | 2.1 A charge, 2–2.4 A out | not stated | same 45 mA / 32 s auto-off; KEY pad; over-discharge at 2.8–2.9 V; plugging/unplugging USB can interrupt the output briefly and reboot an MCU | https://done.land/components/power/powersupplies/battery/chargers/charge-discharge/ip5306/mh-cd42/ | S1 |
| "18650 battery shield" V3 (holder + IP5306-type IC) | ≈ 98–106 × 29–31 × 17 | 0.5 A charge; 5 V 1–2 A, 3 V 1 A (listings disagree) | not stated | IP5306 behaviour assumed | Funduinoshop listing (106 × 31 × 17), CNX-Software | S1 / UNV |
| DD05CVSA | 22 × 17 × 4 vs 23 × 15.4 × 5.7 (conflict) | 5 V (or 12 V variant) up to 2 A claimed | "discharge quiescent 450 µA" | no enable documented | Cirkit Designer; blog repost of a listing | S1, low quality |
| J5019 | 33 × 24 (one listing; the ≈ 25 × 20 guess was not confirmed) | TP4056-type 1 A charge + adjustable 4.5–24/27 V boost | not found | trim-pot output, no enable | DNA Technology listing | S1, low quality |
| Adafruit PowerBoost 500C (#1944) | 22 × 37 × 2 (7 with JST) | 500 mA charge, 5.2 V 500 mA+ (TPS61090, 2 A switch) | **5 mA enabled (power LED), 20 µA disabled** | EN to GND fully disconnects output; LBO at 3.2 V; micro-USB | https://www.adafruit.com/product/1944 | S1 (manufacturer) |
| Adafruit PowerBoost 1000C (#2465) | 23 × 45 × 10 | 1 A charge (MCP73871 with load sharing), 5.2 V 1 A+ | 5 mA enabled, 20 µA disabled | EN; LBO 3.2 V; micro-USB | https://www.adafruit.com/product/2465 | S1 (manufacturer) |

### 4.3 Stand-alone 5 V boost / buck-boost

| Module | Size (mm) | Input | Output capability at Li-ion voltages | Quiescent | Enable / disconnect | Source | Label |
|---|---|---|---|---|---|---|---|
| **Adafruit MiniBoost 5V (TPS61023), #4654** | **17.8 × 11.3 × 5.6**, 1.0 g | 2–5 V (IC 0.5–5.5 V) | **800 mA @ 3.0 V in, 1100 mA @ 3.5 V, 1400 mA @ 4.0 V**; 1 A out needs 1.8 A in at 3.7 V (78 %); 0.5 A out needs 0.8 A in (88 %) | IC: 20 µA typ from VOUT, 0.9 µA from VIN (TI datasheet SLVSF14) | EN low = **true disconnect**, 0.1 µA typ shutdown. The board pulls EN up to VIN with **100 kΩ** (R1 in Adafruit's schematic, section 11 item 10): left alone the converter is on | https://www.adafruit.com/product/4654 ; https://www.ti.com/product/TPS61023 ; https://github.com/adafruit/Adafruit-TPS61023-PCB | V2 |
| Pololu U3V16F5 (#4941) | 13.1 × 8.1 × 3, 0.4 g | 1.3–16 V (start ≥ 2.7 V) | input current 1.6 A typ max (2 A switch) → ≈ 0.85 A @ 3.0 V, ≈ 1.0 A @ 3.7 V, ≈ 1.2 A @ 4.2 V **[INF, 88 % assumed]** | "< 1 mA" no-load | **no enable pin, no load disconnect** (output follows input through inductor + diode) | https://www.pololu.com/product/4941 | S1 (manufacturer) |
| Pololu U1V11F5 (#2562) | 12 × 15 × 3 | 0.5–5.5 V | 1.2 A switch → ≈ 0.6 A @ 3.0 V, ≈ 0.75 A @ 3.7 V **[INF]** | "< 1 mA"; with SHDN low "< 100 µA" (100 kΩ SHDN pull-up to VIN: ≈ 37 µA at 3.7 V **[INF]**) | SHDN, true shutdown | https://www.pololu.com/product/2562 | S1 (manufacturer) |
| Pololu S7V8F5 (#2123) buck-boost | 11 × 17 × 3 | 2.7–11.8 V | 0.5–1 A depending on ratio; lower end when boosting from 3 V | < 0.2 mA | SHDN (100 kΩ pull-up: 10 µA per volt of VIN when held low) | https://www.pololu.com/product/2123 | S1 (manufacturer) |
| MT3608 module | 36 × 17 × 6.25 (taller with trim-pot) | 2–24 V | sold as "2 A"; sellers themselves advise ≈ 1 A | not found | EN tied on-board, no disconnect; output set by trim-pot (up to 28 V) | Robu / seller listings | S1, low quality |

### 4.4 3.3 V for the MCU from 3.0–4.2 V

- **Board LDO fed from the cell:** works only if the board's regulator is a genuine low-dropout, low-quiescent part. An AMS1117-3.3 (dropout ≈ 1.1–1.3 V, ≈ 5 mA quiescent) cannot regulate 3.3 V from a Li-ion cell and wastes the standby budget. Parts such as ME6211 / ME6217 / RT9080 / XC6220 (dropout ≈ 0.1–0.25 V at 100–300 mA, 1–55 µA quiescent) are suitable. **[UNV – typical datasheet figures, the MCU board choice belongs to another research note]** With ≈ 0.2 V dropout plus rail sag, the MCU browns out when the cell falls to ≈ 3.4–3.5 V under load, leaving ≈ 10–15 % of the capacity unused. **[INF]**
- **Buck-boost:** Pololu S7V8F3 (#2122): 11 × 17 × 3 mm, 2.7–11.8 V in, 3.3 V out, 0.5–1 A, quiescent < 0.1 mA, power-save mode, SHDN pin. https://www.pololu.com/product/2122 **[S1, manufacturer]** Uses the full cell down to 3.0 V but costs up to 100 µA standby (≈ 0.9 Ah per year) unless shut down.
- Generic "TPS63020 3.3 V" modules exist (Robozar listing; `TPS63020-module.pdf` at rcscomponents) but no trustworthy board dimensions or quiescent figure were found. **[UNV]**

---

## 5. Recommended power architecture

```
18650 (unprotected, flat-top) in holder
   │ B+/B−
TP4056 USB-C module + DW01A/FS8205A  ◄── USB-C (5 V), R_PROG → ≈ 0.5 A
   │ OUT+/OUT−  = "VBAT" rail (3.0–4.2 V), 220–470 µF bulk
   ├── MCU board battery/5V input → on-board low-Iq LDO → 3.3 V
   │       (3.3 V also feeds PN5180 logic; PN5180 RESET held low in sleep)
   ├── MAX98357A VIN (amp runs directly from VBAT; SD_MODE held low in sleep)
   ├── VBAT sense divider (≥ 2 × 1 MΩ, or switched)
   └── TPS61023 boost (Adafruit MiniBoost 5V), EN ← GPIO with pull-down
           │ 5 V switched rail, 470–1000 µF bulk at the servo
           ├── servo (SG90)
           ├── PN5180 5 V / TVDD
           └── RGB LED
```

Why this set:

- TP4056 + DW01A has the lowest standing drain of all candidates (≈ 5 µA typ, ≤ 12 µA worst case from the two datasheets) and no auto-shutdown logic. **[INF from S1 datasheets]**
- TPS61023 is the only small boost found that combines a true-disconnect enable (0.1 µA) with enough current for a servo stall from a nearly empty cell (800 mA at 3.0 V, 1100 mA at 3.5 V).
- Switching the whole 5 V rail by the boost's EN removes servo idle current (5–10 mA), LED idle current and the PN5180 transmitter supply in sleep with no extra load switch.
- The amplifier on VBAT avoids pulling audio power through the boost; at 3.7 V into 4 Ω roughly 1.3 W is available **[INF: (0.9 × V)² / 2R]**, against 3.2 W at 5 V (MAX98357A datasheet headline).

Firmware rules that the hardware depends on:

1. Never run the RFID field or audio while the servo moves; enable 5 V, wait ≈ 5–10 ms, move, stop PWM, disable.
2. Do not command the servo into a hard stop; lock out the servo below ≈ 3.4 V cell voltage.
3. Go to deep sleep at ≈ 3.3 V resting cell voltage; DW01A (2.4 V) is only the backstop.
4. Hold EN, SD_MODE and PN5180 RESET at defined levels during deep sleep (external pull-downs or GPIO hold).

Open point: a WS2812-type LED on a 5 V rail wants ≥ 3.5 V data-high (0.7 × VDD); 3.3 V logic is marginal. Use a level shifter, or drop the LED supply by one diode, or an LED type specified for 3.3 V logic. **[UNV – check in the LED note]**

### 5.1 Current budget (battery side, 3.7 V nominal, boost efficiency 85 % assumed)

| State | Contributors | Battery current | Label |
|---|---|---|---|
| **Deep sleep, 5 V rail off** | ESP32-S3 chip 7–8 µA (Espressif datasheet; 8 µA measured on a stripped DevKitM, lucidar.me); LDO 1–55 µA (board dependent); TP4056 < 2 µA; DW01A 3 µA typ; TPS61023 0.1 µA; PN5180 hard power-down ≈ 10 µA (NXP datasheet); divider ≈ 2 µA; amp shutdown µA-class [UNV]. Added on 2026-11-26: 29–40 µA through the EN pull-up of the MiniBoost (section 11 item 10) and 3–4 µA through the SD pull-up of the amplifier board (note 04) | **≈ 30–90 µA** without the two pull-ups, **≈ 70–130 µA** with them | INF from datasheets |
| Deep sleep on an unsuitable dev board (AMS1117, power LED, USB-UART always on) | – | **≈ 5–15 mA** | UNV, typical |
| Awake, BLE advertising/connected, no power management | ESP32-S3 CPU + radio duty | ≈ 35–60 mA | UNV – Espressif table values not retrieved |
| Awake with automatic light sleep | – | ≈ 1–5 mA | UNV estimate |
| RFID field on continuously | PN5180 TVDD 180 mA typ (250 mA max) at 5 V → 0.29 A at the cell; + logic ≈ 15 mA + MCU ≈ 40 mA | **≈ 0.35 A** | INF from NXP figures |
| RFID polling at 10 % duty | – | ≈ 75 mA | INF |
| PN5180 LPCD (card-detect) with 5 V rail kept on | NXP example: ≈ 200 µA average at 200 ms interval; + boost ≈ 30 µA | ≈ 0.25–0.4 mA | S1 (NXP knowledge base) + INF |
| Audio, moderate volume (≈ 0.25 W average) | amp ≈ 75 mA + MCU decoding ≈ 60 mA | **≈ 130–180 mA** | INF / UNV |
| Audio, loud (≈ 1 W average) | amp ≈ 300 mA + MCU | ≈ 370 mA | INF |
| Servo move, no load | 100–250 mA at 5 V | 0.2–0.45 A for ≈ 0.2 s | INF |
| **Servo stall peak** | 0.75 A at 5 V → 5 × 0.75 / (0.82 × 3.5) | **≈ 1.3–1.5 A** for as long as the stall lasts | INF |

### 5.2 Runtime on a 3350 mAh (min) cell

Usable capacity ≈ 2850 mAh assumed (≈ 85 %, firmware cut-off ≈ 3.3–3.4 V). **[INF]**

| Use | Estimate |
|---|---|
| Deep sleep at 80 µA (at 130 µA: ≈ 2.5 years) | ≈ 4 years arithmetically; the cell's self-discharge (≈ 1–2 % per month) dominates → **more than a year of standby in practice** |
| Deep sleep on an unsuitable dev board at 10 mA | ≈ 12 days |
| LPCD wake-on-tag at ≈ 0.35 mA | ≈ 11 months |
| Awake BLE idle at 45 mA | ≈ 63 h |
| RFID field on continuously | ≈ 8 h |
| Audio, moderate volume | **≈ 16–22 h** |
| Audio, loud | ≈ 7–8 h |
| Lid actuations | ≈ 0.04 mAh each – negligible |

The largest lever is the MCU board's regulator and always-on parts, not the cell.

---

## 6. Concealed charging options

### 6.1 USB-C

Connector geometry:

| Item | Value | Source | Label |
|---|---|---|---|
| Receptacle shell inner opening | 8.34 (+0.06/−0.02) × 2.56 ± 0.04 | GCT USB4105 drawing (`gct_usb4105.pdf`, https://gct.co/files/drawings/usb4105.pdf); Access Communications page | V2 |
| Receptacle shell outer width | 8.94; body depth 7.35; height ≈ 3.2–3.3 | GCT USB4105 drawing | S1 |
| Plug shell (outer) | 8.25 × 2.40 (± 0.03) | vendor plug drawings found via search (24-position plug drawing, Amphenol 12401562E4#2A) | V2 (vendor drawings) |
| Plug insertion length | ≈ 6.65 | Access Communications page | S1 |
| Cable overmold | thickness **6.5 max** (GCT mating view); width limit 12.35 from the USB-IF specification was NOT re-confirmed (a DigiKey forum post cites 12.5) | GCT drawing; forum | S1 / UNV |

Correction to the brief: **8.34 × 2.56 is the receptacle's inner opening, not the plug shell.** The plug shell is 8.25 × 2.40.

Opening in the printed shell – two cases **[INF]**:

1. Receptacle shell flush with (or within ≈ 1 mm of) the outer surface: opening = receptacle outer shell + clearance ≈ **9.3 × 3.6 mm**. This matches the "≈ 9 × 3.3" in the brief.
2. Receptacle recessed behind a wall (the normal case in a 5 mm shell): the cable overmold must enter the recess, so the recess must be **≈ 13 × 7 mm**, narrowing to ≈ 9.3 × 3.6 only for the last ≈ 1 mm in front of the receptacle face.

Breakout boards for panel mounting:

| Board | Size (mm) | Notes | Source | Label |
|---|---|---|---|---|
| Pololu USB 2.0 Type-C breakout usb07a (#2585) | 20.3 × 14.0 (0.8" × 0.55"; 15.2 deep incl. connector) | two Ø 2.18 holes for M2; 5.11 kΩ CC pull-downs fitted | https://www.pololu.com/product/2585 | S1 (manufacturer) |
| Adafruit USB Type-C breakout, downstream (#4090) | 20.4 × 14.2 × 5.0, 1.3 g | 5.1 kΩ CC resistors fitted | https://www.adafruit.com/product/4090 | S1 (manufacturer) |
| TP4056 module's own USB-C | 28–29 × 17–18 board, connector on a short edge | no mounting holes; glue or clamp in a printed pocket | section 4.1 | – |

### 6.2 Qi receiver

| Module | Coil | Thickness | Output | Distance | Source | Label |
|---|---|---|---|---|---|---|
| Adafruit universal Qi receiver (#1901) | 40 × 29 on a 48 × 32 × 0.5 backing; electronics 19 × 12 × 1.3 | ≈ 0.5–1.3 | 5 V, **500 mA** | "too far → does not activate", no figure | https://www.adafruit.com/product/1901 | S1 |
| Generic 5 V / 1 A Qi receiver PCBA | 41.5 × 29 × 0.38 coil | – | 5 V 1 A | – | Kitsguru listing | S1 |
| DFRobot DFR0362 pair (not Qi) | Ø 43 outer / Ø 20 inner × 2.3 | 2.3 | 5 V 1 A (1.2 A max) | 2–10 mm | Core Electronics listing | S1 |
| QST QPR-882Q receiver datasheet | – | – | – | Tx-to-Rx coil 3.0–5.0 mm; cover plastic < 1.8 mm | LCSC-hosted datasheet (via search) | S1 |

Problems specific to this device:

- **Geometry [INF]:** a flat Ø 43 coil inside a sphere of 45 mm inner / 50 mm outer radius cannot sit lower than 50 − √(45² − 21.5²) = **10.5 mm** above the charging pad; a 40 × 29 coil sits at ≥ 12.4 mm. Listed working distances are 2–8 mm (10 mm at best). Qi therefore needs a flattened base or a dedicated cradle.
- **NFC:** Qi operates at ≈ 100–205 kHz; ST and the Qi specification treat NFC/RFID cards in the charging field as something that can be **damaged**, which is why Qi chargers add NFC card detection (ST "ST25 NFC for Qi charging protection", WPC FOD documents). A Tonie figure left on the ball while it charges, and the PN5180 antenna itself, would sit in or near that field. Detuning of the 13.56 MHz antenna by the receiver's ferrite/foil was not quantified by any source. **[S1 + UNV]**
- The steel can of the 18650 directly above the receiver coil needs the ferrite shield between them; heat from ≈ 60–70 % efficient transfer ends up inside a closed PLA shell. **[INF]**

### 6.3 Magnetic pogo-pin connectors

| Part | Size | Rating | Source | Label |
|---|---|---|---|---|
| Electrokit 2-pin magnetic pogo pair (41035991 male / 41035992 female) | 2.54 pitch, PCB pins Ø 0.7 × 1.5, travel 1.1; housing size not listed | 12 V, 2 A | https://www.electrokit.com/en/2-pin-female-magnetic-pogo-pin-connector | S1 |
| Adafruit DIY magnetic connector, right-angle 4-pin (#5358) | 21 × 7 × 7, 2.54 pitch | 36 V, 2 A | Botland listing for the Adafruit part | S1 |
| Adafruit right-angle 3-pin (#5360) | 2.54 pitch, size not listed | – | https://www.adafruit.com/product/5360 | S1 |

Works electrically (wired to IN+ / IN− of the TP4056, the pads are dead when no charger is attached because the TP4056 does not back-feed its input). Drawbacks: proprietary cable, exposed metal dots on the shell, magnets collect ferrous debris.

### 6.4 Recommendation

**USB-C, recessed in the black equator band on the hinge side (or at the south pole), closed by a black press-fit plug.** Use either the TP4056 module's own connector in a printed pocket or, for placement freedom, a small USB-C breakout (with CC resistors) wired to IN+ / IN−. Model the recess as 13 × 7 mm, tapering to 9.3 × 3.6 mm at the receptacle face. Qi is not recommended; magnetic pogo is the fallback if a visible slot is unacceptable.

---

## 7. Power switching and brown-out

- **Hard power switch vs deep sleep:** with the recommended parts, deep sleep costs ≈ 30–90 µA, so a hard switch is not needed for battery life. The cell is removable when the ball is open, which already provides a hard off and a hard reset. A hidden external switch adds a shell penetration for little benefit. If one is wanted for transport, do not route battery current (≈ 1.5 A peaks) through a miniature slide switch; let the switch drive a high-side MOSFET.
- **High-side switch breakout:** Pololu Mini MOSFET Slide Switch with Reverse Voltage Protection, LV (#2810): 15.2 × 15.2 × 2.5 mm, 1.8–16 V, 16 mΩ max at 4.5 V, 3 A continuous, on-board slide switch plus "ON" control pin, on-state consumption ≈ 210 µA/V (indicator LED), off-state current not specified. https://www.pololu.com/product/2810 **[S1, manufacturer]** The LED current (≈ 0.8 mA at 3.7 V) makes it unsuitable as an always-on element unless the LED is removed.
- **5 V rail:** switched by the TPS61023 enable (true disconnect). No separate P-MOSFET is needed. A boost without disconnect (U3V16F5, MT3608) would need one.
- **Brown-out under servo stall [INF]:** 1.3–1.5 A at the cell through cell resistance + two FS8205A FETs (≤ 50–70 mΩ) + holder contacts + wiring (together ≈ 0.12–0.25 Ω) gives ≈ 0.16–0.37 V of sag on VBAT. At a cell voltage of 3.5 V this pushes the LDO input to ≈ 3.2 V and the 3.3 V rail out of regulation. A capacitor cannot carry a stall lasting hundreds of milliseconds (1.3 A × 0.3 s would need ≈ 1.3 F for 0.3 V); it only absorbs the start-up spike of a few milliseconds.
- **Capacitors:** 470–1000 µF / 10 V low-ESR electrolytic or polymer on the 5 V rail next to the servo connector (several servo guides recommend 470–1000 µF; a forum case reports that 100 µF on a LiPo boost was not enough); 220–470 µF on VBAT at the MCU regulator input; 10 µF ceramic at PN5180 TVDD. **[S1 forum-level + INF]** Typical can sizes: 470 µF/10 V ≈ Ø 6.3 × 11 mm, 1000 µF/10 V ≈ Ø 8 × 12 mm. **[UNV]**
- The real protection is behavioural: no stalls, servo lock-out at low battery, nothing else drawing current during the move.

---

## 8. CAD dimensions of recommended parts

All values in mm. "Model as" already includes the spread plus ≈ 0.3–0.4 mm print clearance.

### 8.1 SG90 servo

Datum: origin on the output-shaft axis at the bottom face of the body. +X along the body away from the shaft end, Y across the width, Z up.

| Feature | Nominal (source C) | Min–max over sources | Model as |
|---|---|---|---|
| Body, X extent | −5.9 … +16.8 (L 22.7) | L 22.0–23.2 | pocket −6.3 … +17.5 (23.8 long) |
| Body, Y extent | ± 5.9 (W 11.8) | W 11.5–12.5 | pocket ± 6.45 (12.9 wide) |
| Body below flange underside | 15.9 | 15.9–16.4 (17.0 TowerPro; MG90S 18.5) | pocket depth ≥ 17.5 (≥ 19 for MG90S); do not support the body on its bottom face – locate on the flange |
| Flange, X extent | −10.6 … +21.5 (span 32.1) | span 31.9–32.6 | seat 33.2 long |
| Flange thickness | 2.5 | 2.4–2.5 | clamp gap 2.6 |
| Mounting holes | Ø 2.0 at X = −8.25 and +19.15, Y = 0 (27.4 apart, derived) | spacing 27.0–27.4 from drawings; 27.5–28 quoted elsewhere, unverified | pilot holes Ø 1.5–1.6 at **27.5 apart as 1.5 mm-long slots**, or (preferred) a printed clamp bar over the flange that does not depend on hole spacing |
| Main case top | Z 22.7 | 22.7–23.0 | – |
| Gear case | Ø 11.8 on the axis plus Ø 5 boss ending at X ≈ +9.0, Z 22.7 … 26.7 | top 26.7–27.3 | clearance to Z 27.7 |
| Spline | Ø 4.6, Z 26.7 … 29.9 | Ø 4.6–4.9; tip 29.0–30.3; 20T/21T | horn bore test gauge Ø 4.6–4.9; tip clearance to Z 30.7 |
| With stock horn + screw | – | 31–32 | clearance to Z 33 |
| Cable | exits the −X end face (shaft side), Z ≈ 4.5–5.7, ribbon 3.6 × 1.2 | – | slot 5 × 3 at Z 3–7 on the −X face, plus ≥ 8 mm free length for the bend [INF] |

MG90S deltas: flange underside ≈ 1.5 higher, spline tip ≈ 2.2 higher, width + 0.2.

### 8.2 Cell and holder

| Part | Model as |
|---|---|
| 18650 unprotected flat-top | cylinder Ø 18.6 × 65.3 max; cradle bore Ø 19.0 |
| Keystone 1043 (THT) | 77.1 × 20.7 base, 18.0 high (catalogue; distributors say 14.9–15.1), pins 71.6 apart, pegs 55.2 apart; with cell seated reserve 21.5 height; envelope 78 × 21.5 × 22 |
| Keystone 1042 (SMT) | as above but 86.0 over the solder tabs |
| Generic black holder, unknown clone | worst case 78.5 × 22.5 × 23; measure the purchased part |
| Lead exit | wire-lead versions: leads leave both ends; reserve ≈ 5 mm beyond each end for the bend [INF] |

Placement constraint in the R = 45 mm cavity: holder centre within ≈ 10 mm of the sphere centre (section 3.4).

### 8.3 Electronics modules

| Part | Board | Model as | Notes |
|---|---|---|---|
| TP4056 USB-C + DW01A | 28–29 × 16.5–18 × ≈ 4 | 30 × 18.5 × 5 pocket | no mounting holes; USB-C on a short edge; gets warm – keep 2 mm air gap to the wall |
| Adafruit MiniBoost 5V #4654 | 17.8 × 11.3 × 5.6 | 18.5 × 12 × 6.5 | – |
| Pololu S7V8F3 (optional 3.3 V buck-boost) | 11 × 17 × 3 | 12 × 18 × 4 | – |
| USB-C breakout (Pololu #2585 / Adafruit #4090) | 20.3 × 14.0 / 20.4 × 14.2 × 5.0 | 21 × 15 × 5.5 | Pololu has two M2 holes |
| USB-C shell opening | – | recess 13 × 7, throat 9.3 × 3.6, receptacle face ≤ 1 mm behind the throat | section 6.1 |
| Bulk capacitor 470–1000 µF / 10 V | Ø 6.3 × 11 to Ø 8 × 12 [UNV] | Ø 8.5 × 13 lying flat | near the servo |

---

## 9. Free 3D models (not downloaded)

| Part | URL | Format / note |
|---|---|---|
| SG90 with horns | https://grabcad.com/library/sg90-micro-servo-9g-tower-pro-1 | STEP + x_t (≈ 80 k downloads) |
| SG90 (alternative) | https://grabcad.com/library/micro-servo-9g-sg90-tower-pro-1 | described as dimensionally accurate |
| SG90 (alternative) | https://grabcad.com/library/4145-towerpro-sg90-mini-servo-sunrobotics_in-1 | SOLIDWORKS + STEP |
| SG90 replacement horn with spline | https://grabcad.com/library/sg-90-tower-pro-micro-servo-motor-horn-1 | STEP / SLDPRT / STL |
| SG90 parametric | https://github.com/openscad/MCAD/blob/master/servos.scad (`towerprosg90`) | OpenSCAD |
| Keystone 1042 holder | https://gitlab.com/kicad/libraries/kicad-packages3D/-/tree/master/Battery.3dshapes → `BatteryHolder_Keystone_1042_1x18650.step` | STEP (file presence confirmed via GitLab API) |
| MPD 18650 holder | same folder → `BatteryHolder_MPD_BH-18650-PC2.step` | STEP |
| KiCad footprints | https://gitlab.com/kicad/libraries/kicad-footprints/-/tree/master/Battery.pretty (`BatteryHolder_Keystone_1042_1x18650`, `BatteryHolder_MPD_BH-18650-PC`, `BatteryHolder_MPD_BK-18650-PC2`) | pad positions used in section 3.1 |
| TP4056 module, USB-C | GrabCAD model titled "TP4056 Charging Module Type C" (STEP + Fusion 360) – seen only on user pages, direct library URL not confirmed | check dimensions against the real board |
| TC4056A module, micro-USB | https://grabcad.com/library/tc4056a-charger-module-5v-1a-usb-micro-1 | STEP, "measured from the actual module" – different connector |
| USB-C receptacle | https://gct.co (USB4105 product page offers 3D models) | STEP [UNV] |

Community CAD models of clones are no substitute for measuring the purchased servo.

---

## 10. Rejected / not chosen candidates

| Candidate | Reason |
|---|---|
| IP5306 boards (MH-CD42 and similar) | Output switches off after 32 s below 45 mA – incompatible with deep sleep unless a dummy load or I2C variant is used; 50 µA typ standby and 3 mA operating overhead; output glitch on USB plug/unplug; 2.1 A charge is unnecessary. |
| "18650 battery shield" boards | ≈ 98–106 mm long – longer than the 90 mm cavity; same IP5306-type behaviour; fixed coil-spring holder. |
| DD05CVSA / DD06CVSA | Only low-quality listings; quoted 450 µA discharge quiescent current; no enable; conflicting dimensions. |
| J5019 | Trim-pot output up to 24–27 V (a bumped pot destroys servo and PN5180); no enable; quiescent unknown; 33 × 24 mm. |
| Adafruit PowerBoost 500C / 1000C | 5 mA quiescent when enabled (LED), micro-USB, 22 × 37 and 23 × 45 mm footprints; 1000C's load sharing is attractive but the board is too large and the port is the wrong type. Usable only with EN gating and LED removal. |
| MT3608 module | No load disconnect and no usable enable; trim-pot set point up to 28 V; 36 × 17 mm plus tall pot; realistic output ≈ 1 A according to sellers; quiescent and ripple undocumented. |
| Pololu U3V16F5 | Excellent size (13.1 × 8.1 × 3) but no enable and no load disconnect: the 5 V rail would sit at battery voltage when "off", keeping servo, LED and PN5180 TVDD powered. Needs an extra load switch. |
| Pololu U1V11F5 | True shutdown, but the 1.2 A switch limit gives only ≈ 0.6–0.75 A at 3.0–3.7 V – below a worst-case servo stall plus anything else; ≈ 37 µA through the SHDN pull-up while off. Acceptable fallback if the servo measures ≤ 0.4 A stall. |
| Pololu S7V8F5 (5 V buck-boost) | Output current falls toward 0.5 A when boosting from 3 V; buck capability is not needed. |
| Servo directly on the cell | Below the rated 4.8 V; torque/travel loss unquantified; stall current straight on the MCU's supply rail. |
| Protected 18650 cells | 68–70 mm length does not fit many holders and damages springs; protection is already on the charger board. |
| Two cells in parallel | Equalising currents with swappable cells; no space; one cell already gives > 16 h of audio. |
| Qi receiver | Coil cannot get within range through a 100 mm sphere without a flat base; Qi field is a documented hazard for NFC tags; heat in a closed shell; 500 mA modules are slow. |
| Magnetic pogo connector | Proprietary cable, visible contacts, debris attraction. Kept as fallback. |
| MG90S instead of SG90 | 2.2 mm taller, 4.4 g heavier, ≈ 700 mA measured stall. Only if the plastic gears prove too weak for the latch. |
| Keystone 54 clip as the electrical contact | It grips the insulated cell body; it is a retainer, not an end contact. |

---

## 11. Open risks and unverified items

1. **Servo horn dimensions** – no dimensioned source found. Measure.
2. **Mounting-hole spacing** – 27.0–27.4 from drawings; the often-quoted 27.5–28 was not confirmed. Use a clamp or slotted holes.
3. **Spline** – 20T (Feetech) vs 21T (others), Ø 4.6–4.9. Horns from one batch may not fit another.
4. **Servo travel** – 120°, 150° or 180° depending on the clone; calibrate per unit and design for ≤ 90°.
5. **Servo at 3.7–4.2 V** – no measured data.
6. **Stall current of the unit actually bought** – 0.36 A to 0.8 A in the sources. Measure it; it decides whether the cheaper/smaller boost options are viable.
7. **Keystone 1042/1043 height** – 18.0 mm (manufacturer catalogue drawing) vs 14.86 / 15.11 mm (distributors).
8. **Generic holder dimensions** – clone spread of several millimetres; contact resistance unmeasured.
9. **TP4056 module** – board-level standby current is a vendor claim (< 6 µA); pad order, CC resistors and the "needs USB once after cell insertion" behaviour must be checked on the delivered board.
10. **MiniBoost EN pull-up** – found on 2026-11-26 in Adafruit's Eagle files (`research/downloads/power_servo/adafruit_tps61023.sch`, from https://github.com/adafruit/Adafruit-TPS61023-PCB): R1 = 100 kΩ between the nets EN and VIN; the pads are printed `En`, `5V`, `GND`, `Vin`; the feedback divider is 732 kΩ / 100 kΩ. **[S1, manufacturer's design file]** Consequences **[INF]**: (a) 29–40 µA flow through R1 for as long as EN is held low at 3.0–4.2 V, which the sleep budget of section 5.1 did not contain; (b) a pull-down forms a divider with R1. TI gives "above 1.2 V" for on and "below 0.4 V" for shutdown, with 0.35 V as the minimum of the low threshold (SLVSF14B, sections 6.5 and 7.3.2). A pull-down of 100 kΩ leaves VIN / 2 = 1.5–2.1 V at EN: the converter stays **on** whenever the controller does not drive the pin. 10 kΩ leaves 0.27–0.38 V, which is not safely below 0.35 V. **4.7 kΩ leaves 0.13–0.19 V.** Removing R1 from the board makes any pull-down work and saves the current of (a).
11. **MCU board regulator** – decides standby life (30–90 µA vs 5–15 mA) and the usable fraction of the cell. Not part of this note.
12. **ESP32-S3 awake/BLE currents, MAX98357A shutdown current, WS2812 idle current** – not retrieved from datasheets here; the budget rows marked UNV depend on them.
13. **USB-C overmold width limit (12.35 mm)** – from memory of the USB-IF specification, not re-verified; 6.5 mm thickness is confirmed by the GCT drawing.
14. **Charging heat** – 0.7–1.4 W in a closed PLA sphere; verify temperature on the first build.
15. **Wake source** – if the product must wake on tag presence, PN5180 LPCD needs the 5 V rail (or at least TVDD) alive in sleep; the budget then moves from ≈ 0.08 mA to ≈ 0.3–0.4 mA.
16. **Nkon, Keystone and GrabCAD pages** blocked automated fetching; their figures here come from search-result excerpts or mirrored PDFs.
17. **Protection over-current trip vs servo stall** – worst-case DW01A/FS8205A trip ≈ 1.7 A against a calculated 1.3–1.5 A stall draw at low cell voltage; a trip resets the device.
