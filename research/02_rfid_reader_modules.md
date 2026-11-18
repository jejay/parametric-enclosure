# RFID Reader Modules for Reading Tonie Figurines (ISO 15693 / ICODE SLIX-L, privacy mode)

**Project:** 3D-printed Pokéball device (≈100 mm sphere, hard max 120 mm) for an engagement scavenger hunt.
**Reader-side research only** (tag/figurine side covered by another agent).
**Access / research date: 2026-11-17.** Prices and stock are snapshots and will drift.

Confidence tags used below: **[VERIFIED ≥2]** = two or more independent sources agree; **[single]** = one source only;
**[inference]** = my own reasoning/calculation from primary data. Disagreements between sources are called out explicitly.

---

## 0. Executive summary / recommendation

- **Recommended reader: the common "blue" PN5180-NFC breakout (board rev. R1.1-170710), ~70 × 39 mm, 13-pin 2.54 mm header.** It is the de-facto standard for reading original Tonies on ESP32, has the most proven code path (ESPuino / tueddy PN5180 library), the best ISO 15693 range of the hobby-grade readers, 3.3 V-logic-native (no level shifter), and a hobbyist can solder the through-hole header easily. **[VERIFIED ≥2]**
- **The single most load-bearing fact for your CAD:** this board is **~70 × 39 mm**, not 65 × 40 mm. The 65 mm figure in circulation is the NXP **evaluation-board antenna** (65 × 65 mm), a different product. **[VERIFIED ≥2]** The **Elechouse** PN5180 is a *different, smaller* board (**40.02 × 42.36 mm**) with a 1.25 mm connector — see the mechanical section; do not mix the two.
- **Reading original Tonies in privacy mode with PN5180 + ESP32 is proven in the field**, not just theory — multiple ESPuino forum users read their own original Tonie figurines successfully. The reader must send GET RANDOM NUMBER (0xB2) + SET PASSWORD (0xB3) unaddressed *before* inventory; the libraries expose this as `disablePrivacyMode()` / `unlockICODESLIX2()`. **[VERIFIED ≥2]**
- **If board footprint is the binding constraint (≤ 45 × 45 mm with privacy unlock):** the best alternative is an **ST25R3916 / ST25R3916B** board (≈43 × 40 mm, or the M5Stack Unit NFC at 48 × 24 mm). Same chip family as the Flipper Zero, which does SLIX privacy unlock; RFAL exposes `rfalNfcvPollerTransceiveReq()` for the raw 0xB2/0xB3 frames. Trade-off: smaller/less-optimised antenna ⇒ likely less range than the 70 × 39 PN5180, and **no ready-made Tonie example** — you implement the unlock yourself. **[VERIFIED ≥2]**
- **Rejected for Tonies:** PN532, MFRC522/RC522, M5Stack RFID2 (WS1850S) — **none support ISO 15693.** **[VERIFIED ≥2]**

### Comparison table (reader candidates)

| Module (chip) | ISO 15693? | Raw/custom cmd before inventory? | PCB size (mm) | Antenna | IF | Logic | EU avail. | ESP32 lib maturity | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| **PN5180 "blue" breakout** (PN5180) | **Yes** | **Yes** (lib: `disablePrivacyMode`) | **~70 × 39 × 1.65** | on-board loop, right half | SPI | 3.3 V native | high (AliExpress/Amazon/eBay/AZ-Delivery) | **high** (ESPuino, tueddy, ATrappmann) | **CHOSEN** |
| Elechouse PN5180 | Yes | Yes (same libs) | **40.02 × 42.36 × 1.6** | on-board loop | SPI | 1.65–3.6 V (PVDD) | Elechouse direct (CN), ~US$12.8 | high | good if you want smaller + cleaner board, but 1.25 mm connector |
| ST25R3916 board (NFC 4 Click / Elechouse / M5 Unit NFC) | **Yes (NFC-V)** | **Yes** (`rfalNfcvPollerTransceiveReq`) | ~43 × 40 (Elechouse); 48 × 24 (M5) | on-board | SPI/I2C | 3.3 V | Elechouse/M5 EU resellers | medium (RFAL; no Tonie example) | **best small-antenna alternative** |
| ST25R3916**B** board (Elechouse) | Yes | Yes | ~43 × 40 (est.) | on-board | SPI/I2C | 3.3 V | Elechouse ~US$13.9 | medium | newer silicon; same caveats |
| CR95HF / ST25R95 (BM019, MikroE RFID Click) | **Yes** | **Yes** (proven: ceres-c gist does ICODE privacy) | BM019 ~43 × 19; Click 57.15 × 25.4 | on-board trace | UART/SPI | 3.3 V | Mouser/DigiKey (Click **discontinued**) | low (no Arduino-ESP32 SLIX lib) | works, lower RF power ⇒ less range; more DIY |
| CLRC663 / RC663 (Elechouse) | Yes (tested) | likely (register-level) | 40.02 × 42.36 | on-board 4-turn ~39 × 42 | SPI/I2C/UART | 3.3 V | Elechouse | low-medium (no Tonie/privacy example) | capable, little community evidence |
| PN7150 / PN7160 (Elechouse PN7160) | PN7160 **Yes**, PN7150 **no** | **Awkward** — NCI does discovery first | 42.83 × 40.53 | on-board | I2C | 1.8/3.3 V | Elechouse ~US$21.8 | low for raw cmds | privacy-unlock-before-inventory is against NCI's grain; **caution/avoid** |
| TI TRF7970A (DLP-RFID2) | **Yes** | **Yes** ("Raw Write" 0x18) | 41.9 × 18.7 × 4.3 | on-board + U.FL ext. | UART | 3.3 V | DLP Design (US), ~US$35 | low (TI MSP430 host code) | **same chip family as the Toniebox**; small; pricey, UART |
| PN532 (incl. Elechouse) | **No** | — | ~43 × 40 | on-board | SPI/I2C/UART | 3.3 V | everywhere | n/a for 15693 | **REJECT (no ISO 15693)** |
| MFRC522 / RC522 | **No** | — | 59.5 × 39 | on-board | SPI/I2C/UART | 3.3 V | everywhere | n/a for 15693 | **REJECT (no ISO 15693)** |
| M5Stack Unit RFID2 (WS1850S) | **No** | — | 48 × 24 × 8 | on-board | I2C | — | M5 resellers | n/a | **REJECT (14443A only)** |

---

## 1. PN5180 module mechanical data for CAD

**There are (at least) two physically different PN5180 breakouts on the market. Decide which one you buy before modelling.**

### 1A. The common "blue" PN5180-NFC breakout (board rev. **R1.1-170710**) — RECOMMENDED

> **Superseded for dimensions:** `08_blue_board_mechanics.md` measured this board on photographs of two units. Use its values (69.6 x 38.6 mm, holes Ø3.3, antenna centre 48.8 mm from the header end, tallest part about 1.3 mm) instead of the ones in the table below.

This is the board sold by AliExpress sellers, AZ-Delivery, Amazon, eBay, diymore, etc., and shown in the ATrappmann/tueddy library docs. It is the AITRIP/generic blue board.

| Parameter | Value | Confidence / source |
|---|---|---|
| **Outer PCB size** | **≈ 70 × 39 mm** | **[VERIFIED ≥2]** diymore/Alibaba seller alt-text "70x39mm"; a second Alibaba listing "70mm*39mm, 23 g"; a vendor page "70x39mm". easyelecmodule lists **69 × 37 mm** (close variant/measuring difference). The kosla project built & *physically validated* a mount to a **70.0 × 39.0 mm** envelope. |
| Cross-check on length | PN5180 long side is **~10 mm longer** than an RC522 (59.5 mm), short side equal (39 mm) ⇒ ~70 × 39 | **[VERIFIED ≥2]** ESPuino dev "biologist" (forum t/4103/5): *"der PN5180 ist in Richtung der Anschlussleiste 1 cm länger … Die kürzere Seite ist gleich lang"*; RC522 = 59.5 × 39 mm (Handson Technology datasheet drawing). |
| **PCB thickness** | **1.65 mm** (≈1.6) | **[VERIFIED ≥2]** kosla validated model `pcb_thickness 1.65`; Elechouse STEP shows 1.60 mm for its board — standard 1.6 mm FR4. |
| **Max component height** | **total stack ≈ 2.3 mm**; components sit ~0.65 mm below the PCB on the back and ~0.65–0.7 mm above on the front (SMD 0402/0603, a QFN40 chip, a 4-pin crystal) | **[single]** kosla `pcb_total_component_thickness 2.3`, `component_projection_below_pcb 0.65`. Allow **~3 mm clearance** each side to be safe. **[inference]** |
| **Mounting holes** | **4 holes**, one near each corner region | **[VERIFIED ≥2]** visible in board photo; kosla model. |
| Hole positions (from board left edge, long axis = x) | pair at **x≈26 mm (y≈2.5 & 36.5)**, pair at **x≈63.25 mm (y≈7.0 & 32.0)**; **Ø ≈ 4 mm (M3 clearance)** | **[single, "estimate"]** kosla validation JSON (`hole_*`, `hole_diameter_estimate 4.0`). This came from an AI-assisted parametric model — **treat positions as ±1 mm and confirm against your own unit before committing the print.** |
| Hole-pattern note | the 4-hole raster is reportedly **identical to the RC522's** | **[single]** ESPuino "biologist" (t/4103/5). |
| **Header** | **single-row 13-pin, 2.54 mm (0.1") pitch**, through-hole, along one short end | **[VERIFIED ≥2]** schematic JP1 "CON13" + board silkscreen. |
| **Pin order** (silkscreen, from the marked end) | **+5V, +3.3V, RST, NSS, MOSI, MISO, SCK, BUSY, GND, GPIO (GPO1), IRQ, AUX (AUX1), REQ** | **[VERIFIED ≥2]** board photo silkscreen + ATrappmann README mapping (RST→RESET_N, NSS→SPI-NSS, GPIO→GPO1, AUX→AUX1, REQ→AUX2/DWL_REQ). |
| **Antenna** | rectangular multi-turn spiral loop occupying the **right ~half** of the board; it does **NOT** surround the PN5180 chip (chip + matching are on the left half). Loop outer size roughly **~38 × 33 mm** (fills the right portion up to the 2 right mounting holes). | **[VERIFIED ≥2]** board photo (ATrappmann PN5180-NFC.png) + kosla install photo. Exact copper outline not published; measure if critical. |
| **Weight** | **~20–23 g** (Alibaba "23 g"); Elechouse lists its (smaller) board at 20 g | **[single]** |
| **Supply** | 5V pin → TVDD (RF); 3.3V pin → logic/PVDD. **Both must be connected.** | **[VERIFIED ≥2]** ESPuino README + forum t/387. |
| **Reference 3D / footprint** | No official vendor STEP for the blue board. Usable community geometry: kosla parametric CadQuery model (70×39, hole table) and `lhm0/accessible_book_reader` KiCad `13_pin` footprint + `PN5180_holder.stl`. | downloaded to `research/downloads/rfid_reader/kosla_qalcosonic/` and `.../lhm0_accessible_book_reader/` |

**Schematic (blue board, `PN5180 R1.1-170710_SCH.PDF`, drawn "Acre Peng", Future Electronics):** on-board 27 MHz crystal (ABM10-27.000MHZ), EMC filter L1/L2 = 470 nH + 220 pF, series damping R3–R6 = 2.2 Ω, match caps around C6/C7/C16/C17 (15/18 pF) and C11/C15 (82 pF). R12 = 0 Ω ties VBAT to **+3.3 V** (R13 "NC" for the +5V option) — i.e. **the stock board bridges VBAT to 3.3 V**, which is why 3.3 V-only operation works. The "5V" and "3.3V" header pins both feed the supply network; connecting both to 3.3 V is valid (reduced range), connecting 5V→~4 V/5 V raises RF range. **[VERIFIED ≥2]** schematic + ESPuino forum (compactflash t/387/9, tueddy t/387/8).

### 1B. Elechouse PN5180 module — smaller, different connector

| Parameter | Value | Source |
|---|---|---|
| **Outer PCB size** | **40.02 × 42.36 mm** (1575.4 × 1667.8 mil) | **[VERIFIED ≥2]** Elechouse product manual §2 + §5; confirmed by STEP bbox **39.99 × 42.34 mm**. |
| **PCB thickness** | **1.60 mm** | **[VERIFIED ≥2]** STEP (board solid z = 0…1.60). |
| **Mounting holes** | manual says **"3 × M3 equivalent"**; STEP shows **2 clear Ø3.05 mm holes** on a diagonal (rel. ~(7.9, 34.5) and (32.1, 7.8) mm) plus 4 large Ø≈7.8 mm corner ring features | **[single]** Elechouse manual + my STEP analysis. Disagreement: manual "3", STEP clearly shows 2 fastening holes — **verify on a real unit.** |
| **Main connector** | **1.25 mm pitch, 10-pin** JST-type (HX1.25-10P / Hanxia), **NOT a 2.54 mm pin header** | **[single, but STEP + manual agree]** STEP part "CONN-SMD_10P-P1.25_HANXIA"; manual spec table "HX1.25-10P, 1.25mm". (The Elechouse *product web page* confusingly also says "Standard 2.54 mm Header" — contradicts its own manual + the STEP. The physical part is 1.25 mm.) ⇒ **you need a matching 1.25 mm cable; less solder-friendly than the blue board.** |
| **Extension header** | separate **4-pin, 2.54 mm**: REQ, AUX1, IRQ, GPO1 | **[VERIFIED ≥2]** STEP shows 4 holes at 2.54 mm pitch; manual §3.3. |
| Main 10 pins | PD/CE, 5V, PVDD, GND, NSS, MOSI, MISO, SCK, BUSY, RST | Elechouse manual §3.1 |
| Chip package on board | HVQFN-40 (6 × 6 mm) | STEP |
| Logic jumper | solder jumper "SPI=3V3" / "PVDD=3V3": bridge for 3.3 V MCUs (ESP32); leave open + feed PVDD for 1.8 V MCUs | **[VERIFIED ≥2]** manual §3.2 + product page |
| Price / weight | US$12.80 (1–9), US$10.60 (10–99); 0.02 kg | Elechouse page |
| 3D STEP | official: `elechouse.com/.../3D_PN5180.zip` (downloaded) | — |

> Both boards carry the **same PN5180A0 chip**, so all firmware/library notes below apply to either. The blue board is bigger but has the better-tuned, larger antenna and a solder-friendly 0.1" header; the Elechouse board is smaller/cleaner but needs a 1.25 mm cable.

### 1C. Electrical (PN5180A0 chip, datasheet rev. 4.0, C3/C4)

| Parameter | Value | Source |
|---|---|---|
| TVDD (RF transmitter supply) | rec. **2.7–5.5 V, typ 5.0**; **5 V gives best range** | datasheet Table 124 |
| VBAT | rec. 2.7–5.5 V (typ 3.3) | Table 124 |
| PVDD (logic ref) | **2.7–3.6 V for 3.3 V logic** (1.65–1.95 for 1.8 V) | Table 124 |
| **I(TVDD) during RF** | **typ 180 mA, max 250 mA** (abs-max 300 mA) — this is the current the on-board reservoir caps must buffer | Table 124/123 |
| I(PVDD) | ~20 mA | Table 128 |
| I(VBAT) | ≤ 20 mA | Table 128 |
| **Standby** | **~15 µA** | Table 128 |
| **Hard power-down** | **~10 µA** | Table 128 |
| **LPCD (low-power card detection)** avg | not a single datasheet number — it is duty-cycled RF-on bursts; real figure depends on wake interval. The chip wakes on field change; ESPuino uses it for deep-sleep wake. | datasheet §11.8.10; ESPuino |
| Can it run from 3.3 V only? | **Yes** — tie both 5V and 3.3V pins to 3.3 V. **Reduced range.** Datasheet min TVDD is 2.7 V. | **[VERIFIED ≥2]** ESPuino README + forum; datasheet |
| 3.3 V ESP32 logic compat | **Direct, no level shifter** (ESP32 is already 3.3 V). On a 5 V Arduino you'd need a shifter. | **[VERIFIED ≥2]** tueddy example header comment; datasheet PVDD |
| SPI | up to **7 Mbit/s**, Mode 0, plus **BUSY** flow-control line (mandatory) | datasheet; Elechouse |

---

## 2. Libraries / firmware evidence (reader side)

### 2.1 Arduino libraries — exact ISO 15693 / ICODE privacy functions (read from source)

**`tueddy/PN5180-Library`** (master, v2.3.7, LGPL-2.1) — *the library ESPuino forks.* File `PN5180ISO15693.h/.cpp`:
```cpp
ISO15693ErrorCode getRandomNumber(uint8_t *randomData);                       // sends {0x02,0xB2,0x04}
ISO15693ErrorCode setPassword(uint8_t identifier, const uint8_t *password, const uint8_t *random);
                                                                              // sends {0x02,0xB3,0x04,id, pw^rnd...}
ISO15693ErrorCode enablePrivacy(const uint8_t *password, const uint8_t *random); // {0x02,0xBA,...}
ISO15693ErrorCode enablePrivacyMode(const uint8_t *password);                 // getRandom + enablePrivacy
ISO15693ErrorCode disablePrivacyMode(const uint8_t *password);                // getRandom + setPassword(0x04,…)
ISO15693ErrorCode getInventory(uint8_t *uid);                                 // {0x26,0x01,0x00} single-slot
ISO15693ErrorCode getInventoryMultiple(...); readSingleBlock(...); getSystemInfo(...);
```
The key frames (verified in `.cpp`): GET RANDOM = `{0x02, 0xB2, 0x04}`; SET PASSWORD = `{0x02, 0xB3, 0x04, identifier, pw0^rnd0, pw1^rnd1, pw2^rnd0, pw3^rnd1}`. `disablePrivacyMode(pw)` does GET RANDOM then SET PASSWORD with identifier `0x04` (the privacy password slot) — **exactly the unaddressed 0xB2 + 0xB3 sequence your brief requires.** These are sent before any inventory. **[VERIFIED — source read]**

**`ATrappmann/PN5180-Library`** (master, v2.x, LGPL-2.1) — the upstream. Same chip ops, slightly different names:
```cpp
getRandomNumber(uint8_t*);  setPassword(uint8_t *password, uint8_t *random);
unlockICODESLIX2(uint8_t *password);   // = getRandom + setPassword  (your "disablePrivacy")
lockICODESLIX2(uint8_t *password);     // = getRandom + enablePrivacy
newpasswordICODESLIX2(uint8_t *newpw, uint8_t *oldpw, uint8_t *uid);
writePassword(...); enablePrivacy(...);
```
124★, last code push 2022 (stable). **[VERIFIED — source read]**

`playfultechnology/PN5180` and `SpoolSense/spoolsense_scanner`'s bundled `lib/PN5180` are forks of ATrappmann (same `getRandomNumber/setPassword/enablePrivacy`). SpoolSense builds for ESP32/S3/C3/C6 with **Arduino-ESP32 core 3.x (pioarduino platform 55.03.39)**. **[VERIFIED — source read]**

### 2.2 ESPuino's PN5180 implementation (biologist79/ESPuino, `src/RfidPn5180.cpp`)

- **Privacy-mode handling:** a state machine does, per ISO-15693 cycle: RESET → SETUPRF → **DISABLEPRIVACYMODE** (`nfc15693.disablePrivacyMode(currentSlixPrivacyPassword.data())`) → GETINVENTORY. So it unlocks *before* inventory, every poll. **[VERIFIED — source read]**
- **Password storage:** `src/RfidPn5180.h` defines `SLIX_PRIVACY_PASSWORD_DEFAULT = {0x0F,0x0F,0x0F,0x0F}` and NVS key `"slixPwd"`. Since **PR #457 (merged 2026-08-25)** the password is editable in the web UI ("Passwort für ICODE-SLIX2", restricted to 4 hex bytes). **The `0F 0F 0F 0F` default is a placeholder, NOT the real Tonie password** — the box-specific privacy password is published elsewhere (see §2.4). **[VERIFIED ≥2]**
- **LPCD:** full deep-sleep wake via IRQ pin; requires **PN5180 firmware ≥ 4.0** (code checks `firmwareVersion[1] < 4`; the docs/forum say flash ≥4.0 using `abidxraihan/PN5180_Updater_ESP32` or JanLoebel updater). LPCD needs IRQ on an **RTC-capable GPIO** (GPIO 32 on the Complete board). **[VERIFIED ≥2]** source + ESPuino docs.
- **Core/target:** ESPuino `platformio.ini` builds on **pioarduino Arduino 3.3.12 / ESP-IDF 5.5.5**, and has an explicit **`esp32-s3-devkitc-1`** env ⇒ **PN5180 + Arduino-ESP32 core 3.x + ESP32-S3 is a supported, building combination.** It uses a fork `biologist79/PN5180-Library` (tueddy fork with RF/transceive timeouts cut 500→100 ms to fix false "card removed" at marginal range). **[VERIFIED — source read]**

### 2.3 ESP-IDF-native driver

**`jef-sure/esp32-component-pn5180`** (v0.8.2, MIT, **ESP-IDF 5.0.4+/6.x**, "all targets" incl. **ESP32-S3**). ISO 15693: inventory w/ collision, select, block read/write, system info. **Privacy/password NOT built in** — docs state: *"password protection, privacy mode and the other custom commands of ICODE tags are not implemented. Send them with `pn5180_rf_transceive()` if you need them."* So on ESP-IDF you implement 0xB2/0xB3 yourself via the raw frame API `pn5180_rf_transceive(tx, tx_len, …)`. Good docs, LPCD support, dual-reader support. **[VERIFIED — source read]** (Other ESP-IDF forks: `laplacier/PN5180_ESP-IDF`, `Garag/esp-idf-pn5180` — smaller/less maintained.)

### 2.4 CONCRETE evidence: original Tonies (privacy mode) read with PN5180 + ESP32

- **ESPuino forum t/1630 (froido, 2023-01-03):** used original Tonie figurines ("original Toniefiguren meines Patenkindes"), *"Mit den passenden Einstellungen funktioniert das wunderbar"* — reads a real UID (`ID: 59-50-fd-13`), log floods `disabling privacy-mode successful` while the figure sits on the reader. **Strongest direct evidence.** **[VERIFIED]**
- **ESPuino t/77 (tueddy, 2021-07-08):** *"Ein Tonie ist ein ISO-15693 Tag der sich aber zunächst totstellt (Privacy-Mode). Erst wenn er mit dem privacy Kennwort entsperrt ist kann man die UID auslesen. Das Kennwort hat jemand herausgeschnüffelt, ein entsprechender Link ist im Quelltext vermerkt."* **[VERIFIED]**
- **ESPuino t/4405 (2026):** fhirschmann got silence from Tonies until fixing a **typo in the password** ("Zahlendreher"); joker: *"Mit falschem Passwort passiert nämlich nix – keine Reaktion."* After the correct password, Tonies read fine on the Complete board. **Important nuance from this thread:** several users (joker, harle, openplayer) in 2026 found library Tonies **already unlocked** ("Die Tags bleiben nach dem Lesen offen und werden nicht wieder gesperrt") — either the manufacturer stopped re-locking, or a prior reader left them open. So in practice some Tonies read even with the wrong/placeholder password. **[VERIFIED ≥2]**
- **Toniebox's own reader IC:** iFixit teardown lists **TI TRF7962A** ("to read the NFC chips from the Tonies"), MCU **TI CC3200** (C3200R1M2), accel NXP MMA8451 — confirms your "the box uses a TI TRF796x" and that the tags are ISO 15693. **[VERIFIED ≥2]** iFixit + forum.
- **Reverse-engineered box firmware** `toniebox-reverse-engineering/hackiebox_cfw` `BoxRFID.cpp` (runs on the box's TRF7962A) documents the exact unlock flow and the real passwords it tries: `knownPasswords[] = {0x7FFD6E5B, 0x0F0F0F0F, 0x00000000}`, then GET RANDOM (`ISO15693_getRandomSlixL`) → SET PASSWORD id `0x04` (`ISO15693_setPassSlixL`) → single-slot inventory. The non-trivial value `0x7FFD6E5B` is the boxine/Tonie privacy password (published openly in that project). **[VERIFIED — source read]** *(Tag-side detail; the other agent owns the exact value. Reader-side takeaway: ESPuino's `0F0F0F0F` default is a placeholder, and the working password is public in open-source projects.)*
- **Cross-chip corroboration:** `ceres-c` CR95HF gist (2019) reads ICODE privacy tags with the same `0xB2` GET RANDOM + `0xB3` SET PASSWORD sequence; **Flipper Zero** firmware (`slix_poller.h`) has `slix_poller_get_random_number` + `slix_poller_set_password` + a "PrivacyUnlockRequest" event and SLIX-L UID-prefix detection. Both confirm the method generalises across readers. **[VERIFIED — source read]**

---

## 3. Read range, metal and mitigation

### 3.1 Range expectations (PN5180)

- **ISO 15693 is markedly better than ISO 14443** on the PN5180. tueddy (ESPuino t/387/14): open bench, 15693 **~12 cm**; through a thin wood wall far less. Users read **Tonies "absolut problemlos"** through **6 mm ABS + 2 mm air**, while 14443 cards failed at the same gap (Kruppes/biologist t/3159). **[VERIFIED ≥2]**
- **Small tags are the limiter.** Those ~12 cm / ~11 cm figures are with **big card-sized tags**. Tonie coils and 20–30 mm coin/sticker tags are much smaller, so expect **substantially less** — realistically a **few cm** through 2–4 mm plastic, less again with the battery nearby. Vendor "up to 11 cm" numbers (Elechouse ST25R3916 SLIX2, CLRC663 9 cm) are best-case, large-tag, no-metal. **[inference, consistent with multiple sources]**
- **5 V on the 5V pin raises range** vs 3.3 V-only (tueddy t/387/8, t/3159/8). With a LiPo you can feed ~4 V; with an 18650 (3.0–4.2 V) you can feed the cell voltage to the 5V/TVDD pin for more range. **[VERIFIED ≥2]**
- Field drops ~1/d³ on-axis. At your **15–25 mm** shell gap a Tonie will still read if the antenna is decently coupled, but margin is thin — budget for it. **[inference]**

### 3.2 Metal (18650 steel can, speaker magnet, servo, ground planes) — rules of thumb

- **TI SLOA241C (TRF79xxA antenna guide):** *"Recommended spacing for both vertically stacked and side-by-side geometries between metal surfaces and the NFC/HF RFID antenna coil is **10 mm**."* At 10 mm metal still lowers Q/range but to a "manageable level." Also: keep the coil **off ground planes**, **~10 mm** from any ground plane; *"too large of an antenna proportional to the size of an NFC/HF RFID tag … can result in a read hole."* **[VERIFIED ≥2]** (TI SCBA034 agrees: bigger antenna ⇒ bigger minimum metal separation; tune in final position.)
- **Your 18650 at 15–25 mm behind the antenna is beyond the 10 mm rule but still close enough to cut range.** Mitigate with a ferrite sheet on the battery-facing side and keep the cell as far back / off-axis as the sphere allows. The **speaker magnet and servo motor are the worst offenders** — keep them farthest from, and ideally not directly behind, the antenna. **[inference from TI/NXP guides]**
- **NXP AN11564 (ferrite recommendation):** the ferrite sheet must **at least fully cover the antenna** plus a small overlay (~0.1 × antenna dimension), *not more* (over-large reduces stray field). Material: **µr′ > 40 at 13.56 MHz, with µr″/µr′ < 0.1** (low loss); thicker sheet = stronger shielding. In a ferrite/metal environment a **Q of 20–35** is realistic (above 35 "very unlikely"). Crucially: **re-tune/measure the antenna with the ferrite + metal in place** — the shielding detunes it. **[VERIFIED ≥2]** AN11564 + TI SLOA241C.

### 3.3 Ferrite sheets — types, thickness, EU sources

- **Würth WE-FSFS flexible sintered ferrite** meets NXP's criterion. From Würth's catalog (µ′ @13.56 MHz / µ″ @13.56 MHz):
  - **364004 / 364005 / 364006** = 60 × 60 mm × **0.1 / 0.2 / 0.3 mm**, µ′≈**120**, µ″≈**2** → **µ″/µ′≈0.017, excellent for 13.56 MHz.**
  - 364001–364003 = 120 × 120 mm, same material; 364103/364104/364105 (60 × 60) µ′≈150/µ″≈3.
  - (Avoid the **354xxx / 374xxx** families: µ″≈90 at 13.56 MHz = lossy, wrong frequency band.) **[VERIFIED ≥2]** Würth page; thickness listings disagree 0.3 vs 0.38 mm for some codes — check the SPEC PDF before ordering.
  - **EU stock:** Würth WE-FSFS at **Mouser, DigiKey, Farnell/Conrad/RS, Reichelt**. For a hobbyist, a 60 × 60 × 0.3 mm piece (364006) sits well behind the ~38 × 33 mm PN5180 loop with the required small overlay.
- Cheaper generic "NFC anti-metal ferrite stickers" (0.2–0.3 mm) work too but spec is unknown — Würth is the safe, documented choice. **[inference]**
- Elechouse also sells a "FeSiAl EMI Shielding Sheet" as an accessory for its NFC boards. **[single]**

---

## 4. Rejected / not-chosen candidates (with reasons)

- **PN532 (incl. Elechouse PN532 V4/Mini/USB):** **No ISO 15693** — datasheet lists only ISO 14443A/B + FeliCa + NFCIP-1; Elechouse's own comparison marks ISO 15693 "—". Cannot read Tonies. **[VERIFIED ≥2]**
- **MFRC522 / RC522:** **ISO 14443A only.** 59.5 × 39 mm, 8-pin. Cheap and everywhere, but blind to ISO 15693 / Tonies. **[VERIFIED ≥2]**
- **M5Stack Unit RFID2 (WS1850S):** **ISO 14443A only** (MIFARE/NTAG), I2C @0x28, <20 mm range, 48 × 24 mm. Reject for Tonies. (Do not confuse with the M5Stack **Unit NFC U216** = ST25R3916, which *does* do NFC-V — see below.) **[VERIFIED ≥2]**
- **PN7150:** no ISO 15693 (PN7150 is 14443/FeliCa/P2P). **PN7160** *does* add ISO 15693, but both run **NCI firmware** that performs tag discovery first; sending a raw unaddressed GET RANDOM + SET PASSWORD *before* any inventory succeeds is against NCI's model, and I found **no evidence** anyone has done a Tonie/SLIX privacy unlock on PN7150/PN7160. NXP forum threads show people struggling just to activate SLIX on PN7150. **High risk — avoid** unless you specifically want NCI/Android-style integration. **[VERIFIED ≥2]** (chip caps); **[single]** (privacy difficulty).
- **StrongLink SL0xx / M5 RFID2 / small UART 14443 modules:** the common ones are ISO 14443 only; SL015M page wouldn't load to confirm 15693 + raw privacy. **Unverified / likely unsuitable.** Jinmuyu JMY series: not confirmed for ISO 15693 + raw custom SLIX commands. **[not verified — treat as unknown]**

*(ST25R3916, CR95HF, CLRC663, TRF7970A are NOT rejected — they are viable alternatives, detailed in §5/§0 table.)*

---

## 5. Smaller boards, external antennas, and the "≤45 × 45 mm with privacy unlock" question

### 5.1 Smaller PN5180 boards
- The **Elechouse PN5180 (40 × 42 mm)** is the smallest *ready-made* PN5180 board (§1B). Smaller than the blue board, but **smaller antenna ⇒ expect less range**, and it uses a 1.25 mm connector.
- **NFC 3 Click (MikroE, PN5180A0HN):** 57.15 × 25.4 mm, SPI, on-board etched antenna, 3.3 V. ISO 15693 supported. **Discontinued / out of stock**, ~US$47. Not recommended (availability). **[VERIFIED]**
- No mainstream "mini PN5180" below ~40 mm exists. **[inference]**

### 5.2 PN5180 with a separate / external coil
- **It is possible but is an RF-matching job.** Community evidence: ESPuino forum — somebuddy87 (t/2030) *"habe auf gut Glück einen Widerstand auf dem PN5180 vor der Antenne entfernt und die originale [Toniebox-Antenne] angelötet. Funktioniert tatsächlich erschreckend gut"* (removed a resistor ahead of the on-board antenna, soldered an external coil, works surprisingly well); arch3r (t/2106) did the same with the marked resistors. `lhm0/accessible_book_reader` ships a full **custom PN5180 board + `Antennenanpassung.md` + `NXP_antenna_matching.xls`** for exactly this. **[VERIFIED ≥2]**
- **Effort:** you must (a) lift the on-board antenna (desolder the series/match components), (b) know/measure your coil's inductance & Q, (c) recompute the EMC filter (L0/C0) and match caps (C1/C2) per the NXP symmetrical-match formulas, and (d) with the PN5180's DPC, re-run calibration. Stock-coil inductance is ~1.2–2.3 µH range (my calc from the NXP worked example & schematic values). **Non-trivial; only worth it if a custom coil geometry is essential.** **[inference + lhm0 doc]**

### 5.3 Best ≤45 × 45 mm candidate that keeps privacy unlock: **ST25R3916 / ST25R3916B**
- **Why it qualifies:** NFC-V (ISO 15693) + a **raw transceive** path. Elechouse's RFAL fork exposes `rfalNfcvPollerTransceiveReq(cmd, flags, param, uid, data, dataLen, rxBuf, rxBufLen, rcvLen)` — you can issue `0xB2`/`0xB3` with your own flags; its examples include **`ESP32_SPI_icode_slix2_read_write_test`** and target **ESP32 / S3 / C3 (Arduino-ESP32 core 3.3.8)**. The M5Unit-NFC library exposes `nfcvTransceive()` (raw NFC-V frame). **Flipper Zero uses ST25R3916 and does SLIX privacy unlock** — proof the silicon + stack can do it. **[VERIFIED — source read]**
- **Boards & size:** Elechouse ST25R3916 ≈ **42.8 × 40.3 × 5.4 mm** (US$9.90) / ST25R3916**B** (US$13.90, recommended for new designs); **M5Stack Unit NFC U216** = ST25R3916, **48 × 24 × 8 mm**, I2C @0x50, 5.9 g (nicely narrow); MikroE **NFC 4 Click** 57.15 × 25.4 mm (discontinued). **[VERIFIED ≥2]**
- **Caveats:** (1) **no ready-made Tonie/privacy example** — you port the 0xB2/0xB3 sequence yourself; (2) RFAL is a heavier stack than the little PN5180 Arduino lib; (3) the smaller on-board antennas (esp. M5's 24 mm-wide board) will likely give **less range than the 70 × 39 PN5180** — bench-test before committing; (4) Elechouse ST25R3916 vendor read-range numbers (SLIX2 ~11 cm) are with a large card antenna. **[VERIFIED ≥2 / inference]**
- **Other raw-capable small readers:** **CR95HF** (BM019 ≈43 × 19 mm, US$16, UART/SPI; the ceres-c gist proves ICODE privacy unlock) — lower RF power ⇒ less range, little Arduino-ESP32 library support. **TI TRF7970A** (DLP-RFID2 41.9 × 18.7 mm, US$35, UART, "Raw Write" 0x18, U.FL external-antenna option) — **the Toniebox's own chip family**, but pricey and host code is TI/MSP430-oriented. **[VERIFIED — datasheets read]**

---

### 5.4 Sourcing check of 2026-11-18: no blue board from German stock; MikroE NFC 3 Click as a PN5180 board that ships at once

The owner found every offer of the blue PN5180 board with about two weeks of delivery, one week before the device is needed. Checked that day:

| Source | Finding | Status |
|---|---|---|
| BerryBase, PN5180-MOD (10.80 EUR, with card and fob) | "Currently not available" | **[single]** shop page read directly |
| Roboter-Bausatz | no PN5180 product | **[single]** shop search read directly |
| Amazon.de (RAKSTORE, Onmancy, ARCELI, Quata, Fhdpeebu and others) | several listings "currently unavailable"; stock of the rest not readable (the site refuses automated access) | **[single]** search copies |
| eBay.de | mostly sellers in Shenzhen with delivery in one to two weeks; German sellers not verifiable (the site refuses automated access) | **[single]** search copies |
| **DigiKey.de, MikroElektronika MIKROE-5538 "NFC 3 Click"** | **12 in stock**, 41.72 EUR without VAT, "typically delivered to Germany within 48 hours"; shipping 25 EUR below an order of 75 EUR | **[single]** DigiKey page read directly |
| DigiKey.de, Visaton K 40 8 Ohm / TI DRV5032FBLPG | 690 / 710 in stock, 7.14 / 0.72 EUR | **[single]** DigiKey pages read directly |

**NFC 3 Click (MIKROE-5538)** [product sheet saved in `research/downloads/rfid_reader/mikroe_nfc3_click/`; DigiKey product highlight]: PN5180A0HN, the chip of the blue board, so libraries and the privacy unlock apply unchanged **[inference]**. Board 57.15 x 25.4 mm (mikroBUS size L). Supply 3.3 V and 5 V. Pins as printed on the board: AUX, RST, CS, SCK, SDO, SDI, 3V3, GND on one row and BSY, IRQ, four unused, 5V, GND on the other: every signal of the present harness is there. Two rows of pin headers are fitted at the factory.

Its antenna is etched on the half of the board away from the pins and measures about 23 x 31 mm over the copper (read off the product picture, +-1.5 mm) **[inference]**. The blue board's loop measures 40.9 x 37.7 mm (note 08). The mean loop area is therefore about 45 % of the blue board's, and at the height of a Tonie's tag (20 to 50 mm above the foot in classic figures, note 09) the field of a loop falls roughly with its area: expect about half the field, i.e. clearly less reserve than with the blue board **[inference]**. No report of a Tonie read with this board was found. It has to be tried with the figures before it is relied on.

What the board would need in this design **[inference]**: a printed carrier that fills the reader pocket (cut for 69.6 x 38.6 mm) and holds the smaller board with the centre of its antenna under the standing spot; the pin headers removed or cut short, because only 5 mm are free under the board; the same twelve wires.

Not available quickly and therefore not pursued: the Elechouse boards (ship from China), ST25R3916 boards (another chip, no Tonie code).

Sources: https://www.digikey.de/en/products/detail/mikroelektronika/MIKROE-5538/18110732 · https://www.digikey.hu/en/product-highlight/m/mikroelektronika/mikroe-5538-nfc-3-click-board · https://doc.7-el.ru/n/nfc_3_click.pdf (copy of MikroElektronika's product sheet) · https://www.berrybase.de/en/pn5180-nfc-und-rfid-modul-iso15693-iso14443-spi-inkl.-karte-dongle · https://www.digikey.de/en/products/detail/visaton-gmbh-co-kg/K-40-8-OHM/9842363 · https://www.digikey.de/en/products/detail/texas-instruments/DRV5032FBLPG/12165120

---

### 5.5 M5Stack Unit NFC (U216, ST25R3916) looked at again, 2026-11-18

The owner asked whether the M5Stack unit, which costs about a quarter of the NFC 3 Click and can be had by next-day delivery, would do, and what the "SYN513R variant" is.

| Fact | Value | Status |
|---|---|---|
| Chip, interface | ST25R3916-AQWT, I2C at 0x50 only (I2C_EN tied high); IRQ is not brought out | **[VERIFIED >=2]** M5 documentation + schematic read directly (saved in `research/downloads/rfid_reader/m5stack_unit_nfc/`) |
| Protocols | reader/writer for NFC-A/B, NFC-F and **NFC-V (ISO 15693)** | **[VERIFIED >=2]** M5 documentation, library README |
| Supply | 5 V on the Grove plug into a 3.3 V regulator (TPAP7343D-33); **every supply pin of the chip, the transmitter driver included, is on 3.3 V** | **[single]** schematic |
| Current | 67.65 mA at 5 V while reading, 19 µA asleep | **[single]** M5 documentation |
| Stated range | "<= 40 mm", no tag type named | **[single]** M5 documentation |
| Size | housing 48.0 x 24.0 x 8.0 mm, 5.9 g; the antenna field in the dimension drawing measures about 17 x 28 mm (scaled from the drawing, +-1.5 mm) | **[single]** documentation; **[inference]** antenna |
| Library | `m5stack/M5Unit-NFC` (Arduino and ESP-IDF 5.x; needs M5UnitUnified, M5Utility, M5HAL). NFC-V layer with detect, read, write, dump for ICODE SLI/SLIX/SLIX2. No function for the SLIX password or privacy commands. `nfcvTransceive()` in `src/unit/unit_ST25R3916_nfcv.cpp` sends any frame once `configure_nfc_v()` has switched the field on, with no inventory needed first; the public NFC-V layer does not expose it | **[single]** README and two source files read directly |
| Price, stock | not verified here (Amazon refuses automated access); owner's statement: about a quarter of the Click, next-day delivery | owner |

Assessment **[inference]**: it can do what a Tonie needs, ISO 15693 plus raw frames before any inventory, but the unlock (GET RANDOM, SET PASSWORD) has to be written on top of M5's driver. Its weak side is reach. Loop area about 30 % of the blue board's (17 x 28 against 40.9 x 37.7 mm over the copper) and a transmitter fed from 3.3 V instead of 5 V. With equal ampere-turns a loop of that size gives about half the blue board's field 20 mm above the antenna and about a third at 35 to 50 mm; the lower drive comes on top. A rod tag that sits in the 15 mm foot of a figure would be reached, one that sits 20 to 50 mm up in the body, as in classic Tonies, probably not. The design of the tongue can save one or two millimetres between antenna and foot, no more: the rest of the distance lies inside the figure.

Do not confuse: **Unit RFID 2 (WS1850S)** reads ISO 14443A only. The **"SYN513R"** unit is M5Stack's 433 MHz radio receiver (Unit RF433R; the documentation spells the chip SYN531R) and has nothing to do with NFC.

Sources: https://docs.m5stack.com/en/unit/Unit_NFC · https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1229/SCH_Unit_NFC_V0.1_2025_11_28_12_15_35.pdf · https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1229/u216unitnfc-model-size.pdf · https://github.com/m5stack/M5Unit-NFC · https://docs.m5stack.com/en/unit/rf433_r

---

## 6. Risks & open items

1. **Hole-position numbers for the blue board are from an AI-assisted parametric model ("estimate") — ±1 mm.** I could NOT find a dimensioned manufacturer drawing for the generic blue board. **Buy the board first and measure the 4 holes + outline before finalising the CAD pocket.** [open]
2. **Antenna copper outline of the blue board is not published** — I give ~38 × 33 mm from photos. If you want the ferrite overlay exactly right, measure it. [open]
3. **Which blue-board size: 70 × 39 vs 69 × 37 vs 70 × 39.** Seller listings vary ~1–2 mm; the physically-validated kosla mount used 70.0 × 39.0. Design with ~0.3 mm clearance per side. [minor]
4. **Elechouse board connector contradiction:** its web page says "2.54 mm header" but the manual + STEP say **1.25 mm HX1.25-10P**. Trust the manual/STEP (1.25 mm). If you want pure through-hole soldering, pick the blue board. [resolved-ish]
5. **Range through plastic + near the 18650 is the real project risk.** Vendor "11–12 cm" numbers are large-tag/no-metal. Expect a few cm for a Tonie at 15–25 mm with a battery behind. **Mitigate: 5 V (or cell voltage) on TVDD, ferrite on the battery/speaker side, keep magnet+servo away from the antenna axis, antenna as close to the shell as possible.** [open — bench test]
6. **Some 2026-era Tonies arrive already unlocked; others need the published box password.** ESPuino's `0F0F0F0F` default will NOT unlock a locked original Tonie. The real value is the tag-agent's domain, but the reader firmware must let you set it (ESPuino does, since PR #457). [cross-team]
7. **LPCD needs PN5180 firmware ≥ 4.0** (flash with `abidxraihan/PN5180_Updater_ESP32`). The common blue boards often ship with older firmware. If you want RFID-wake, budget a one-time firmware flash. [open if LPCD wanted]
8. **ESPuino is an ESP32-"classic" / Lolin-D32 project by default**; your ESP32-S3 target builds (there's an `esp32-s3-devkitc-1` env), but if you fork ESPuino rather than write your own, expect pin/SD-MMC config work. The tueddy/ATrappmann PN5180 libraries themselves are plain Arduino and S3-clean. [minor]

---

## 7. Bench-test checklist (do these first, in order)

1. **Smoke test the reader bare on the bench.** ESP32-S3 + PN5180, both 5V & 3.3V pins powered, SPI + BUSY wired. Run tueddy's `PN5180-ReadUID.ino`; confirm it prints a sane **firmware version** (not 255 / not 0xFF). If 255 → wiring/power fault. **[VERIFIED path]**
2. **Read the two tags in the PN5180 bag** (one ISO 15693, one 14443) to prove the RF front-end and library. 15693 should read at noticeably greater distance.
3. **Read an original Tonie in free air.** Put the real privacy password in (the tag agent supplies it; it is NOT `0F0F0F0F`). Expect repeated `disablePrivacyMode successful` + a UID. If silence: wrong password (most common), or the Tonie is already unlocked (try a plain inventory).
4. **Measure free-air range** vs (a) a Tonie and (b) a 25–30 mm coin/sticker ISO 15693 tag. Record cm. This is your ceiling.
5. **Add the plastic shell mock-up** (print a flat 2–4 mm coupon of your shell material) between antenna and tag; re-measure. 
6. **Introduce the 18650** at the intended 15–25 mm behind the antenna; re-measure. Then add a **Würth 364006 ferrite** on the battery side (covering the loop + small overlay); re-measure. Quantify the recovery.
7. **Introduce the speaker and servo** at their real positions; re-measure. These may force relocation more than the battery does.
8. **Try 5 V (or raw cell) on the TVDD/5V pin** vs 3.3 V-only; record the range delta.
9. **Only if range is still short:** evaluate (a) ST25R3916 board for a smaller/repositionable antenna, or (b) a tuned external coil on the PN5180 (RF-matching effort per §5.2).
10. **Soak test** continuous presence (a Tonie sitting on the reader) for pause/resume stability; ESPuino's debounce/"silent heal" logic (`RfidPn5180.cpp`) is a good reference if you see flapping.

---

## Appendix — key sources (accessed 2026-11-17)

**Primary datasheets / app notes (downloaded to `research/downloads/rfid_reader/`):**
- NXP PN5180A0xx C3/C4 datasheet rev 4.0 (`nxp_docs/PN5180A0XX_C3_C4.pdf`)
- NXP AN11740 PN5180 Antenna design guide; AN11564 PN7120 guide (ferrite µr′>40, 0.1×D overlay, Q 20–35); AN13219 PN7160 guide (`nxp_docs/`)
- TI SLOA241C (10 mm metal spacing, read holes) + SCBA034 (`ti_docs/`)
- PN5180 R1.1-170710 schematic (`ATrappmann_PN5180-Library/PN5180_R1.1-170710_SCH.pdf`); board photo `PN5180-NFC.png`
- Elechouse PN5180 product manual + official STEP (`elechouse_PN5180_Product_Manual.pdf`, `elechouse_3d_pn5180/3D_PN5180.zip`); ST25R3916 STEP (`elechouse_3d_st25r3916/`)
- BM019 (CR95HF) + DLP-RFID2 (TRF7970A) + RC522 datasheets (`alt_modules/`)

**Libraries / firmware (source read, downloaded):**
- tueddy/PN5180-Library (v2.3.7) & ATrappmann/PN5180-Library — ICODE SLIX privacy functions
- biologist79/ESPuino `src/RfidPn5180.cpp`, `RfidPn5180.h`, `platformio.ini`, `changelog.md`; ESPuino PR #457 (merged 2026-08-25)
- jef-sure/esp32-component-pn5180 (ESP-IDF, raw `pn5180_rf_transceive`)
- wilson-elechouse/ST25R3916 (RFAL `rfalNfcvPollerTransceiveReq`) + PN5180_ELECHOUSE + CLRC663_ELECHOUSE
- m5stack/M5Unit-NFC (`nfcvTransceive`); toniebox-reverse-engineering/hackiebox_cfw `BoxRFID.cpp`; flipperdevices SLIX poller; ceres-c CR95HF gist

**Community (range / Tonies / dimensions / antenna mods):**
- forum.espuino.de threads 77, 387, 1630, 1929, 2030, 2106, 3159, 4103, 4405 (German)
- kosla-dev/qalcosonic-w1-nfc-reader (validated 70×39 mount) & lhm0/accessible_book_reader (custom PN5180 + antenna matching)
- iFixit Toniebox teardown (TRF7962A, CC3200)

*Note: forum.espuino.de became intermittently unreachable from this environment during the session; I captured the relevant threads before that and via its Discourse JSON API. Printables/eBay/MikroE pages that 403'd were recovered via their APIs or alternate fetches where possible.*
