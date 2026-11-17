# 04 — MCU board, I2S audio, speaker, RGB LED, wake sensors (dimensions + compatibility)

Access date for all web sources: **2026-11-17**.
Downloaded reference files (untrusted, never executed): `research/downloads/mcu_audio/`.

## 0. How to read this file

Confidence tags used throughout:

| Tag | Meaning |
| --- | --- |
| **[V2+]** | Verified by two or more independent sources (e.g. manufacturer drawing/design file + shop listing or firmware pin file) |
| **[V1]** | Single source (usually the manufacturer only) |
| **[INF]** | Inference / calculation by the researcher, not stated by a source |
| **[MEM]** | From general knowledge, not re-checked against a source in this session — treat as unverified |

Project constraints assumed (from the brief): inner sphere radius ≈ 45 mm, ≥ 14 usable GPIO, ≥ 8 MB flash, MCU board ≤ ~26 × 36 mm, speaker depth ≤ 20 mm, one 18650 cell, BLE to phone.

### Summary of recommendations

| Function | First choice | Fallback |
| --- | --- | --- |
| MCU board | **Seeed XIAO ESP32-S3 Plus** (21 × 17.8 mm, 16 MB flash / 8 MB PSRAM) | **Unexpected Maker TinyS3** (35 × 17.8 mm, 8 MB / 8 MB, all GPIO on 2.54 mm pitch); budget/no-charger option: M5Stack StampS3 or Waveshare ESP32-S3-Zero-**N8R8** |
| I2S amplifier | **MAX98357A breakout** (Adafruit #3006 or generic clone), supplied from the battery rail | NS4168 module; DFPlayer Mini only if SD-card workflow is acceptable |
| Speaker | **Visaton K 40 – 8 Ω** (Ø40 × 4.3 mm, 83 dB) | Visaton K 28 WP – 8 Ω (Ø28 × 5.5 mm, 75 dB) if 40 mm does not fit; Visaton BF 32 (32 × 32 × 15 mm) for fuller sound |
| RGB LED | **Single WS2812B / SK6812 on Ø≈10 mm mini PCB**, powered from the switched battery rail | Adafruit NeoPixel Jewel 7 (Ø23 mm) if the light path is too short for one LED to fill the disc |
| Wake sensor | **TI DRV5032FB** hall switch (TO-92 or Adafruit/ScoutMakes breakout #6051), ≈0.7 µA | Glass reed switch Ø2.2 × 14 mm (0 µA); plus optional SW-18010P vibration switch for pick-up wake |

---

## 1. MCU boards

### 1.1 Chip-level facts that drive the choice

- ESP32-S3 / C3 / C6 have **Bluetooth LE only**. Bluetooth Classic (A2DP) exists only on the original ESP32 (ESP32-PICO-D4, WROOM-32 …). The brief needs BLE, so A2DP boards are documented but not needed. [MEM]
- ESP32-S3 strapping pins: GPIO0, GPIO3, GPIO45, GPIO46 (Seeed wiki). GPIO3 only selects the JTAG source and is harmless as normal I/O unless an eFuse is burnt. GPIO19/20 = USB D−/D+. GPIO26–32 = flash/PSRAM; GPIO33–37 additionally taken by **octal** PSRAM (R8 parts). GPIO43/44 = UART0 TX/RX (ROM boot log is printed on GPIO43 at reset). [V2+ for strapping list: Seeed wiki + Waveshare docs; rest MEM]
- Deep-sleep wake (ext0/ext1) needs an RTC GPIO: GPIO0–21 on the S3. ADC1 (usable with Wi-Fi on) = GPIO1–10. [MEM]

### 1.2 Comparison table

"Usable GPIO" = pads broken out, excluding GPIO0/45/46, USB D±, flash/PSRAM pins. GPIO3 and UART0 (43/44) are counted separately as "careful" pins.

| Board | PCB L × W (mm) | Height / thickness | Flash / PSRAM | GPIO broken out (clean + careful) | Charger | Board deep sleep | Price / EU availability | Conf. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Seeed XIAO ESP32-S3 Plus** | 21 × 17.8 nominal; **21.14 × 17.78** measured from Seeed DXF, corner R ≈ 1.9 | not in Seeed spec; see §6.1 | 16 MB / 8 MB (octal) | **20 pads D0–D19** (Seeed spec table says "18"): 2.54 mm edge: GPIO1,2,4,5,6,7,8,9 (8 clean) + 3, 43, 44; 1.27 mm back castellations: GPIO38,39,40,41,42,10,13,12,11 (9 clean) | Yes, **100 mA** fast / 0.9 mA trickle | **33.5 µA** @3.8 V (Seeed); one reseller table says ≈69 µA | US$7.90 Seeed; €8.78 RobotShop EU (restocking); €11.39 OpenELAB (DE); DigiKey/Mouser | [V2+] dims, pin map; [V1] sleep, charge |
| Seeed XIAO ESP32-S3 | 21 × 17.8 nominal; **21.14 × 17.79** from Seeed v1.1 DXF | as above | 8 MB / 8 MB | 11 edge pads (8 clean + 3, 43, 44) + 4 round JTAG test pads on the back (GPIO39–42) | Yes, 50 mA or 100 mA (Seeed tables disagree) | 14 µA @3.8 V (Seeed) | widely stocked | [V2+] dims; [V1] rest |
| **Unexpected Maker TinyS3** | **35 × 17.8** | max 4.3 mm at USB-C end (UM) | 8 MB (in-chip, S3FN8) / 8 MB QSPI | **17 on 2.54 mm headers**: GPIO0, 1–9, 21, 34, 35, 36, 37, 43, 44 → 13 clean (1,2,4–9,21,34–37) + 3, 43, 44 + GPIO0 (boot strap). VBAT sense on internal GPIO10, VBUS sense GPIO33 | Yes (charge current **not published** in sources found) | "ultra low", **no figure published**; sibling TinyPICO is officially 20 µA | US$20–24 class; Pimoroni (UK), Lectronz, UM shop; newer "TinyS3[D]" revision replaces ADC VBAT sense with an I2C fuel gauge | [V2+] dims, pin list (CircuitPython `pins.c` + arduino-esp32 variant); sleep/charge unverified |
| M5Stack StampS3 (S007) | **24.0 × 18.0** | **4.7** total, PCB 1.0; USB-C overhang ≈1.96 (drawing) | 8 MB / none (S3FN8) | 23: G0–G15, G39–G44, G46; mixed 2.54 / 1.27 mm pitch, row spacing 15.24 mm | No (5 V in → MUN3CAD01 DC-DC) | "sleep current" 311 µA (VIN) / 401 µA (USB) @5 V | M5Stack shop and EU distributors (price not re-checked) | [V1] (M5 docs + M5 drawing) |
| Waveshare ESP32-S3-Zero | **23.5 × 18** PCB, 24.8 incl. USB-C | n/a | 4 MB / 2 MB (S3FH4R2). An **-N8R8** SKU (33879 / 33549 with headers) is listed on the Waveshare docs page; its memory size is implied by the name only | "24 GPIO" per Waveshare; ≈15 on the 2.54 mm edge (GP1–13 + TX/RX per pinout image, not text-verified), rest on back pads. GPIO33–37 not broken out; GPIO21 = onboard WS2812 | No (ME6217 LDO, 3.7–6 V on "5V" pad) | no figure; onboard WS2812 (≈0.6–1 mA quiescent) keeps drawing unless removed [INF] | Waveshare, Amazon.de, EU resellers | [V2+] dims (CNX, CircuitPython, manuals site); N8R8 specs unverified |
| ESP32-S3 SuperMini (generic) | 22.52 × 18 (one source says 20 × 15) | n/a | 4 MB / 2 MB (S3FH4R2); varies by factory | varies by factory | No | no reliable figure ("~10 µA" claim is unsourced) | AliExpress / Amazon | [V1], inconsistent |
| LOLIN (Wemos) S3 Mini | **34.3 × 25.4**; 2 holes Ø2.0 at 20.4 mm spacing; header rows 22.86 mm apart | n/a | 4 MB / 2 MB (S3FH4R2) | 27 IO on double 2.54 mm rows | No | no figure | cheap, widely available | [V1] (LOLIN page + LOLIN drawing) |
| Adafruit QT Py ESP32-S3 (#5426 / #5700) | 21.7 × 17.8 | 5.7 (incl. STEMMA QT) | 8 MB / none (#5426) or 4 MB / 2 MB (#5700) | 13 (11 pads + 2 on STEMMA QT) | No (BFF add-on) | ≈70 µA (Adafruit) | US$12.50; #5426 out of stock at Adafruit | [V1] |
| LilyGO T7-S3 | 39 × 31 (× 6) | 6 | 16 MB / 8 MB (WROOM-1 N16R8) | many (not counted) | Yes (current not found) | 34.6 µA with battery (CNX, second-hand) | LilyGO, Amazon | [V2+] dims (LilyGO wiki + Notebookcheck) |
| UM OMGS3 / NanoS3 | 25 × 10 / 28 × 11 (27 × 12.7 in one source) | NanoS3 max 2.4 | 8 MB / 2 MB; 8 MB / 8 MB | 17 / 27, all on fine-pitch solder pads | Yes (+ MAX17048 fuel gauge on OMGS3) | n/a | Pimoroni, Lectronz | [V1] |
| Espressif ESP32-S3-DevKitC-1 (N16R8) | 62.74 × 25.40 on Espressif PCB drawing; third parties list 69 × 25.4 and 70 × 28 | header-on | 16 MB / 8 MB | ~36 pads | No | high (two USB chips, LED, LDO) [INF] | everywhere | dims disagree; far too long either way |
| M5Stamp Pico (classic ESP32, BT Classic) | 24.0 × 18.0 | 4.6 | 4 MB / none | 12 (G0,1,3,18,19,21,22,25,26,32,33,36); **no USB**, needs external downloader | No | 0.35 mA @5 V | M5 distributors | [V1] |
| UM TinyPICO (classic ESP32, BT Classic) | 32 × 18 (micro-USB) / 35 × 17.8 (USB-C v3) | n/a | 4 MB / 4 MB | 14 | Yes | 20 µA official | Pimoroni, Adafruit #5028 | [V2+] dims |
| ESP32-C3 SuperMini | ≈22.5 × 18 | n/a | 4 MB / none | 11–13 | No | ≈43 µA only after removing the power LED; users report 0.5–0.75 mA | very cheap | [V1], secondary sources |
| Seeed XIAO ESP32-C3 / C6 | 21 × 17.8 | as XIAO | 4 MB / none | 11 | Yes (C3: 380 mA fast per Seeed/RS sheet) | C3: 44 µA (Seeed); C6 not re-checked | widely stocked | [V1] |

Sources: Seeed wiki https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/ · Seeed product page https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32S3-Plus-p-6361.html · Seeed DXFs (see §7) · arduino-esp32 variant https://github.com/espressif/arduino-esp32/blob/master/variants/XIAO_ESP32S3_Plus/pins_arduino.h · https://www.espboards.dev/esp32/xiao-esp32s3-plus/ · https://ameridroid.com/products/xiao-esp32-s3-plus · https://eu.robotshop.com/products/seeed-studio-xiao-esp32s3-plus-unsoldered · https://openelab.io/de/products/seeed-studio-xiao-esp32s3-plus · TinyS3 https://esp32s3.com/tinys3.html , https://github.com/UnexpectedMaker/esp32s3 , CircuitPython `ports/espressif/boards/unexpectedmaker_tinys3/pins.c`, arduino-esp32 `variants/um_tinys3/pins_arduino.h`, https://www.cnx-software.com/2022/10/06/unexpected-maker-tinys3-feathers3-and-pros3-boards-esp32-s3/ , https://www.espboards.dev/esp32/tinys3/ · M5 https://docs.m5stack.com/en/core/StampS3 , https://docs.m5stack.com/en/core/stamp_pico · Waveshare https://docs.waveshare.com/ESP32-S3-Zero , https://www.cnx-software.com/2024/08/07/waveshare-esp32-s3-zero-is-a-tiny-wifi-and-ble-iot-module-with-a-usb-c-port-up-to-32-gpios/ , https://circuitpython.org/board/waveshare_esp32_s3_zero/ · LOLIN https://www.wemos.cc/en/latest/s3/s3_mini.html · Adafruit https://www.adafruit.com/product/5426 , https://learn.adafruit.com/adafruit-qt-py-esp32-s3/overview · LilyGO https://wiki.lilygo.cc/products/t7-series/t7-s3/ , https://www.cnx-software.com/2022/10/31/lilygo-t7-s3-esp32-s3-board-16mb-flash-8mb-psram-lipo-battery/ · OMGS3 https://www.cnx-software.com/2024/09/15/esp32-pico-s3-based-omgs3-is-the-worlds-smallest-fully-featured-esp32-s3-module-board/ · DevKitC-1 https://dl.espressif.com/dl/PCB_ESP32-S3-DevKitC-1_V1_20210312CB.pdf · SuperMini https://espboards.dev/boards/esp32-s3-supermini , https://mischianti.org/esp32-c3-super-mini-high-resolution-pinout-datasheet-and-specs/ · TinyPICO https://www.mouser.com/datasheet/2/1362/Unexpected_Maker_Datasheet_TinyPICO-3395053.pdf

### 1.3 Which boards meet "≥ 14 usable GPIO AND ≥ 8 MB flash in ≤ ~26 × 36 mm"?

| Board | ≥ 8 MB flash | ≥ 14 GPIO | ≤ 26 × 36 mm | Verdict |
| --- | --- | --- | --- | --- |
| XIAO ESP32-S3 Plus | yes (16 MB) | yes (17 clean, 20 total) — but only 11 are on 2.54 mm pads | yes | **Pass** |
| UM TinyS3 | yes (8 MB) | yes (13 clean + GPIO3 + 43/44 = 16, all 2.54 mm) | yes (35 × 17.8) | **Pass** |
| M5Stack StampS3 | yes (8 MB, no PSRAM) | yes (23) | yes | **Pass**, no charger, high sleep current through its DC-DC |
| Waveshare ESP32-S3-Zero-N8R8 | probably (name only) | yes | yes | **Likely pass, unverified** |
| XIAO ESP32-S3 (non-Plus) | yes | 11 + 4 tiny test pads | yes | Borderline fail |
| QT Py ESP32-S3 8 MB | yes | 13 | yes | Fail by one pin |
| S3-Zero (standard), S3 SuperMini, LOLIN S3 Mini | no (4 MB) | yes | yes | Fail on flash |
| LilyGO T7-S3, DevKitC-1 | yes | yes | no | Fail on size |
| C3 / C6 minis, M5Stamp Pico, TinyPICO | no (4 MB) | no (11–14) | yes | Fail |

### 1.4 Recommendation

**First choice: Seeed XIAO ESP32-S3 Plus.** Smallest board that passes, twice the required flash, PSRAM, on-board charger and battery pads, cheapest, best EU availability. Costs to accept:

1. Only 11 GPIO are on 2.54 mm pads. The project needs 14–16, so **at least 3–5 wires must be soldered to the 1.27 mm half-hole pads on the back** (GPIO38–42 are the natural choice; they are JTAG pins by default but JTAG runs over USB on this board).
2. The on-board charger is **100 mA** — roughly 30 h for a 3000 mAh 18650 [INF]. A separate 0.5–1 A charger/protection board is advisable; that belongs to the power research.
3. The pad labelled `ADC_BAT` (GPIO10 / D16) has **no voltage divider on the board** according to a Seeed forum thread (user with 20 boards) and espboards.dev; Seeed's own table only lists the label. Plan an external divider (the forum poster used 2 × 220 kΩ) on an ADC1 pin.
4. Height and USB-C overhang are not dimensioned by Seeed (see §6.1) — measure the part before freezing CAD.

Suggested pin use on the XIAO ESP32-S3 Plus [INF]: wake input on GPIO1 (RTC), battery ADC on GPIO2 (ADC1), LED data GPIO3, PN5180 BUSY/RST/NSS on GPIO4/5/6, SPI SCK/MISO/MOSI on GPIO7/8/9, I2S BCLK and DIN on GPIO43/44 (boot-log chatter on GPIO43 is harmless while the amp is held in shutdown), and LRCLK, servo PWM, 5 V enable, amp SD, PN5180 IRQ on back pads GPIO38–42. Do not put the servo or the power-enable on GPIO43.

**Fallback: Unexpected Maker TinyS3** — every one of its 17 GPIO is on a 2.54 mm header, battery voltage sensing is already wired (GPIO10), and 35 × 17.8 mm still fits the limit. Downsides: about 2.5× the price, thinner EU distribution, 8 MB instead of 16 MB, and neither its charge current nor a deep-sleep figure could be found in a published source.

**If no on-board charger is wanted:** M5Stack StampS3 (verified drawing, 8 MB, 23 GPIO, but 0.3–0.4 mA sleep through its 5 V DC-DC) or Waveshare ESP32-S3-Zero-N8R8 (confirm flash size and remove/accept the onboard WS2812 quiescent current).

---

## 2. I2S amplifier

### 2.1 MAX98357A — chip facts (Analog Devices / Maxim datasheet, read directly)

| Parameter | Value |
| --- | --- |
| Supply range | 2.5–5.5 V (UVLO 1.8 V typ) |
| Quiescent current | 2.75 mA typ (3.35 max) at 5 V; **2.4 mA** typ (2.85 max) at 3.7 V |
| Shutdown current (SD_MODE = 0 V) | **0.6 µA** typ, 2 µA max |
| Standby (SD_MODE high, no BCLK) | 340 µA typ, 400 µA max |
| Output power, 10 % THD+N | 3.2 W (4 Ω, 5 V) · 1.8 W (8 Ω, 5 V) · **0.93 W (8 Ω, 3.7 V)** |
| Output power, 1 % THD+N | 2.5 W (4 Ω, 5 V) · 1.4 W (8 Ω, 5 V) · **0.77 W (8 Ω, 3.7 V)** |
| 4 Ω at 3.7 V | not specified; ≈1.7 W at 10 % THD by V² scaling [INF]. Adafruit quotes 1.3 W / 1.0 W (10 % / 1 %) for 4 Ω at 3.3 V |
| Gain (GAIN_SLOT pin) | 15 dB: 100 kΩ to GND · 12 dB: GND · 9 dB: floating · 6 dB: VDD · 3 dB: 100 kΩ to VDD |
| SD_MODE thresholds (Adafruit / DFRobot, consistent) | < 0.16 V shutdown · 0.16–0.77 V (L+R)/2 · 0.77–1.4 V right · > 1.4 V left; internal 100 kΩ pull-down |
| Turn-on time | 7 ms typ |
| Efficiency | 92 % (8 Ω, 10 % THD) |
| Sample rates | 8–96 kHz, no MCLK needed |
| Current limit | 2.8 A |

Datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf (mirror read: https://cdn-shop.adafruit.com/product-files/3006/MAX98357A-MAX98357B.pdf). [V2+: datasheet + Adafruit + DFRobot agree on gain/SD tables]

### 2.2 Breakouts

| Board | PCB (mm) | Height | Pin order / connectors | Notes | Conf. |
| --- | --- | --- | --- | --- | --- |
| **Adafruit #3006** | **17.78 × 19.05** per Adafruit's Eagle board file (corner R 2.54); product page says 19.4 × 17.8 × 3.0 | 3.0 mm per product page (evidently without terminal block); terminal block ships **pre-soldered** → expect ≈10–11 mm over the block [INF] | 1 × 7 header, 2.54 mm: **LRC, BCLK, DIN, GAIN, SD, GND, Vin** (left→right, header edge at bottom, parts up). 3.5 mm 2-way terminal block opposite edge (− left, + right). 2 plated holes Ø2.5 mm | 1 MΩ from SD to Vin on board → (L+R)/2 mode at 3.3–5 V. US$5.95, out of stock at Adafruit on the access date; resellers carry it | [V2+] outline (design file vs. listing: 19.05 vs 19.4 mm long) |
| Generic "MAX98357 I2S" clone (AZ-Delivery, AliExpress) | 19 × 18 × 3 (AZ-Delivery listing) | 3 mm bare; header and terminal block usually supplied loose | same 7-pin order as Adafruit (clone of that layout) | supply stated 2.5–5.5 V; SD pull-up value varies between clones — check before relying on channel mode | [V1] |
| DFRobot DFR0954 | 18 × 18 | n/a | stamp holes + PH2.0 speaker socket; pads: SPK−, VCC, GND, NC, SD, GAIN, SPK+, DIN, BCLK, LRC | 3.3–5 V | [V2+] (DFRobot wiki + Farnell listing) |

Sources: https://www.adafruit.com/product/3006 · https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/pinouts · https://github.com/adafruit/Adafruit-MAX98357-I2S-Amp-Breakout (file `Adafruit MAX98357 Breakout.brd`, parsed) · https://www.az-delivery.de/en/products/i2s-3w-class-d-amplifier-breakout-max98357a · https://wiki.dfrobot.com/dfr0954

### 2.3 Alternatives (documented, not chosen)

| Part | Key data | Why not first choice | Conf. |
| --- | --- | --- | --- |
| MAX98360A | 2.5–5.5 V, 3.2 W into 4 Ω at 5 V, 1.2–5.5 V logic tolerant; ADI page quotes 1.5 µA standby, an e-brief 15 nA shutdown | WLP/tiny packages, no common hobby breakout found | [V1] |
| NS4168 (Nsiway) | I2S mono class D, 3.0–5.5 V, 2.5 W into 4 Ω at 5 V, ESOP-8 (3.9 × 4.9 mm) | Datasheet (shutdown current, CTRL pin) not retrieved; module sizes vary | [V1] |
| Adafruit PAM8302A #2130 | 15 × 24 × 2 mm, 2.0–5.5 V, 2.5 W/4 Ω, 1.5 W/8 Ω at 5.5 V, **analog** differential input, 4 mA quiescent, 0.5 mA shutdown, fixed 24 dB + trim pot | ESP32-S3 has no DAC; would need an external DAC or PDM + filter; 0.5 mA shutdown | [V1] |
| DFPlayer Mini (DFR0299) | 20 × 20 mm, 3.2–5 V, 24-bit DAC, on-board ≤3 W amp, UART 9600 baud, plays files from micro-SD ≤ 32 GB FAT16/32 (also USB stick / 64 MB NOR per DFRobot) | Audio lives on an SD card written from a PC — **the MCU cannot upload or generate audio**; no sample-accurate control; ≈20 mA standby [MEM]; clones vary in quality | [V1] dims |

---

## 3. Speaker

### 3.1 Comparison (all dimensions from manufacturer drawings unless noted)

| Speaker | Outline (mm) | Total depth (mm) | Magnet / rear | Mounting | Z | Rated / max | SPL (1 W/1 m) | Range (−10 dB) | fs | Weight | Conf. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Visaton K 40** (2840) | Ø40 ± 0.2, rim 1.3 ± 0.2 | **4.3 ± 0.3** | rear cup Ø16 ± 0.3; basket Ø36 ± 0.3 | glue/clamp; cut-out Ø36.5 | 8 Ω | 1 W / 2 W | **83 dB** | 350–6000 Hz | 520 Hz | 10 g | **[V2+]** Visaton sheet + Bürklin (40 × 4.3); element14/Digitec list 4.5 |
| **Visaton K 28 WP** (2909) | Ø28 (rim), Ø27 body | **5.5** | rear Ø16, step Ø26 | glue/clamp; cut-out Ø24 | 8 Ω | 1 W / 2 W | 75 dB (76 in two listings) | 300–20000 Hz | 700 Hz | 7 g | **[V2+]** Visaton + Bürklin (28 × 5.5) + DigiKey (28.00 / 5.50) |
| Visaton K 34 WP (2981) | Ø33.8 | 5.2 | rear Ø18 | glue/clamp | 8 Ω | 1 W | 79 dB | 320–20000 Hz | 570 Hz | 6 g | [V1] |
| Visaton K 36 WP (2912) | Ø36 ± 0.3, body Ø33.8 ± 0.2 | 6.2 ± 0.3 (< 6.5 over terminals) | — | glue/clamp; cut-out Ø31 | 8 Ω | 1 W / 2 W | 77 dB | 300–20000 Hz | 550 Hz | 6 g | [V1] |
| Visaton BF 32 (2242 8 Ω / 2243 4 Ω) | **32 × 32** square, flange 1.7 | **15** (11 behind the body step) | body Ø26 / Ø29 | 4 holes Ø2 on 24.5 mm square; cut-out Ø31.5 | 4 or 8 Ω | 2 W / 5 W | 78 dB | 150–20000 Hz | 280 Hz | 28 g | [V1] |
| Visaton K 45 (2849) | Ø45 | 18 | magnet Ø32, basket Ø42 | cut-out Ø41.5 | 8 Ω | 1 W | 83 dB | 300–14000 Hz | 520 Hz | 46 g | [V1] |
| Visaton K 50 WP (2915) | Ø50, body Ø45.5 | 18 | rear housing 31.5 × 31.5 | cut-out Ø46; 2.8 mm blade terminals | 8 Ω | 2 W | **84 dB** | 180–17000 Hz | 300 Hz | 48 g | [V1] |
| Visaton BF 37 (2260/2261) | 37 × 37, holes Ø2.5 on Ø41 circle | **23.8** | Ø22 / Ø34 | 4 holes | 4 / 8 Ω | 5 W | 74 dB | 100–20000 Hz | 170 Hz | 33 g | [V1] |
| Visaton BF 45 (2240) | Ø45 body, 61 × 51.5 over lugs | **27.6** | Ø21 | 2 holes Ø3 | 4 Ω | 4 W | 79 dB | 90–20000 Hz | 160 Hz | 32 g | [V1] |
| Visaton FRS 5 (2231) | Ø52.5, 68 over lugs (holes Ø4.2 at 60) | **31.5** | Ø45 | 2 lugs | 8 Ω | 5 W | 84 dB | 150–20000 Hz | 270 Hz | 126 g | [V1] |
| Adafruit #3968 "40 mm 4 Ω 5 W" (Fuxin H-23071740-02) | Ø40.0 ± 0.2 | **21 ± 0.5** on the maker's drawing; 20 on Adafruit's page | rear cup Ø23 ± 0.2, basket Ø36.5 | glue/clamp | 4 Ω | 5 W / 6 W | 78 ± 3 dB | fo–15 kHz | 150 Hz | 27.3 g | **[V2+]** (drawing vs. listing disagree by 1 mm) |
| Generic "40 mm 4 Ω 3 W" (Pimoroni, Roboter-Bausatz etc.) | Ø40 | 20 (one similar RS part 18.3) | — | glue/clamp, JST-PH option | 4 Ω | 3 W | not stated | not stated | — | — | [V2+] for Ø40 × 20 |
| Adafruit #3923 / #4227 mini oval | 30 × 20 | 5 | — | adhesive | 8 Ω | 1 W | not stated | not stated | — | 3 g | [V1]; both out of stock |
| Adafruit #1890 mini metal | Ø28 | 4.5 | — | adhesive | 8 Ω | 0.25 W / 0.5 W | not stated | ~600 Hz–10 kHz | 680 Hz | 6 g | [V1] |
| Adafruit #1891 thin plastic | Ø39 | not stated | — | adhesive | 8 Ω | 0.25 W / 0.5 W | not stated | 440 Hz–20 kHz | 440 Hz | 4.6 g | [V1] |
| Same Sky (CUI) CMS-40504N-L152 | Ø40 | 5 | — | wire leads | 4 Ω | 2 W / 2.5 W | 100 dB at 1 W / **0.1 m** (≈80 dB at 1 m [INF]) | 400 Hz–7 kHz | 500 Hz | — | [V1] distributor listings |

Notes: the brief called Adafruit #4227 a "40 mm 4 Ω 3 W" speaker; #4227 is actually the mini oval with short wires — the 40 mm 4 Ω part is **#3968**. Visaton has no "K 40 WP"; the 40 mm model is **K 40**. The generic "28 mm 8 Ω 2 W" speaker was not found with a datasheet; #1890 is the closest documented part.

Datasheets (Visaton, all read directly):
K 40 https://www.visaton.de/sites/default/files/dd_product/K%2040_2840_2841_0.pdf ·
K 28 WP https://www.visaton.de/sites/default/files/dd_product/K%2028%20WP_2909_2910_0.pdf ·
K 34 WP https://www.visaton.de/sites/default/files/dd_product/K%2034%20WP_2981.pdf ·
K 36 WP https://www.visaton.de/sites/default/files/dd_product/K%2036%20WP_2912_2913_0.pdf (drawing https://www.visaton.de/sites/default/files/2024-03/k36wp_tz_220928_3.GIF) ·
BF 32 https://www.visaton.de/sites/default/files/dd_product/BF%2032_2242_2243_0924_0.pdf ·
K 45 https://www.visaton.de/sites/default/files/dd_product/K%2045_2849.pdf ·
K 50 WP https://www.visaton.de/sites/default/files/dd_product/K%2050%20WP_2915-17_1.pdf ·
BF 37 https://www.visaton.de/sites/default/files/dd_product/BF37-4-8-Ohm_datasheet_2.pdf ·
BF 45 https://www.visaton.de/sites/default/files/dd_product/BF%2045_4%20Ohm_0.pdf ·
FRS 5 https://www.visaton.de/sites/default/files/dd_product/FRS%205_2231.pdf
Other: https://cdn-shop.adafruit.com/product-files/3968/H-23071740-02.pdf · https://cdn-shop.adafruit.com/datasheets/1890_8ohmMetalSpeaks.pdf · https://cdn-shop.adafruit.com/datasheets/1891_datasheet_2.pdf · https://www.buerklin.com/en/p/visaton/acoustic-signal-transmitters/k40-8-ohm/38M540 · https://www.buerklin.com/en/p/visaton/acoustic-signal-transmitters/k28-wp-8-ohm/38M526 · https://www.sameskydevices.com/product/audio/speakers/miniature-(10-mm~40-mm)/cms-40504n-l152 · https://shop.pimoroni.com/products/mini-speaker-4-3w-with-jst-ph-connector

### 3.2 Recommendation

**Main: Visaton K 40 – 8 Ω (Art. 2840).** Reasons: highest sensitivity among the thin candidates (83 dB), only 4.3 mm deep and 10 g, response concentrated in the speech band (350 Hz–6 kHz with a presence peak around 4 kHz on Visaton's curve), front rated IP 67 when sealed, ≈€4.3–5.3 in the EU (Bürklin €5.25, Mouser IE ≈€4.3–4.8, Micros €4.92). Its 1 W rating matches what a MAX98357A can deliver into 8 Ω from a Li-ion cell (0.77–0.93 W at 3.7 V), so the amp cannot overdrive it when run from the battery rail; on 5 V the amp reaches 1.4–1.8 W and volume must be capped in software/gain.

Expected level [INF]: ≈82 dB at 1 m (≈88 dB at 0.5 m) at full output from 3.7 V — more than a child's toy should produce, so there is headroom to run at reduced gain.

**Alternative (smaller): Visaton K 28 WP – 8 Ω (Art. 2909)**, Ø28 × 5.5 mm, 75 dB — 8 dB quieter for the same power but wider bandwidth and IP 65 front.
**Alternative (better voice body): Visaton BF 32 – 8 Ω (Art. 2242)**, 32 × 32 × 15 mm with screw holes, 150 Hz–20 kHz, 78 dB, 28 g — sounds fuller, needs a 5 V amp supply to reach the same loudness and three times the depth.

Fit check against a 45 mm inner radius [INF]: a flat Ø40 disc pressed toward the shell sits with its rim touching and its centre ≈4.7 mm inside the inner surface, so the K 40 occupies roughly the outer 9 mm of the sphere; the K 28 WP ≈7.7 mm; the BF 32 ≈21 mm.

---

## 4. RGB LED

| Part | Dimensions (mm) | Supply | Data VIH | Current | Conf. |
| --- | --- | --- | --- | --- | --- |
| WS2812B (5050), original v1 | 5.0 × 5.0 × ~1.6 | 3.5–5.3 V | 0.7 × VDD | up to ~18–20 mA per colour; ~1 mA quiescent class | [V2+] (several datasheet copies) |
| WS2812B-V5 | 5.0 × 5.4 × 1.57 | 3.7–5.3 V | **0.63 × VDD** (3.15 V at 5 V) | 12 mA per colour; **0.6 mA quiescent** | [V1] Worldsemi sheet, read directly |
| WS2812B-2020 V6 | 2.0 × 2.0 | 3.7–5.3 V (one variant 3.3–5.3 V) | 2.7 V fixed (one variant 0.55 × VDD) | — | [V1] |
| SK6812 MINI-E (reverse-mount) | body 3.2 × 2.8 × 1.78; 5.8 over leads | 3.7–5.5 V | 0.7 × VDD | 12 mA per colour (5 mA version exists); 1 mA static | [V2+] Opsco sheet + LCSC |
| **Single WS2812B/SK6812 on round mini PCB** (generic; Adafruit #1612) | **Ø ≈ 10 (±1) × 3.0–3.2 thick**; Adafruit lists 9.1 × 9.1 × 3.2 and "8 × 10 mm" in the text | 5 V nominal, "as low as 3.5 V, dimmer" (Adafruit) | as fitted LED | ≈18.5 mA per colour, ≈55 mA max per pixel (Adafruit) | **[V2+]** PMD Way, Tindie, Soldered, Adafruit |
| Adafruit Flora NeoPixel v3 #1260 | Ø12.5 × 2.5 | max 5.5 V since the 2024 revision; runs at 3.5 V dimmer | — | 18.5 mA per colour | [V1] |
| Adafruit NeoPixel Jewel 7 #2226 | **Ø23**, listed thickness 2 (probably PCB without LEDs; expect ≈3.3 [INF]) | 5 V | — | 7 × ~18 mA × 3 at full white | [V1] |
| Adafruit 8 mm diffused through-hole NeoPixel #1734 | Ø8 base × 11 tall, leads 27 | 5 V | — | RGB order (not GRB) | [V1] |
| 5 mm addressable PTH LED (SparkFun COM-12986, APA106/PL9823 class) | Ø5 | **4.5–6 V** | not found | — | [V1] |

Sources: https://learn.watterott.com/kb/ws281x/WS2812B-v5.pdf · https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8880/WS2812B.pdf · https://cdn-shop.adafruit.com/product-files/4960/4960_SK6812MINI-E_REV02_EN.pdf · https://www.adafruit.com/product/1612 · https://www.adafruit.com/product/2226 · https://www.adafruit.com/product/1260 · https://www.adafruit.com/product/1734 · https://pmdway.com/products/ws2812b-rgb-led-mini-pcbs-100-pack · https://www.tindie.com/products/mmm999/50pcs-dc-5v-3mm-x-10mm-ws2812b-smd-led-2/ · https://docs.soldered.com/ws2812b/hardware/ · https://www.sparkfun.com/products/12986

**Will it run from a 3.3–4.2 V Li-ion rail?** Partly in spec: the datasheet minimum is 3.5–3.7 V, so the top two-thirds of the discharge curve is covered; below that the LED keeps working in practice but blue fades first [INF + Adafruit's "dimmer" note]. Through-hole APA106/PL9823 types need ≥ 4.5 V and are not suitable for the battery rail.

**3.3 V data level:** the well-known problem exists only when the LED is on 5 V (VIH = 3.5 V for 0.7 × VDD parts; 3.15 V for V5 parts, which 3.3 V just meets). With the LED on the battery rail, VIH is at most 0.7 × 4.2 V = 2.94 V, so a 3.3 V GPIO is in spec with no level shifter. Since the version of the LED on a cheap mini PCB is unknown, **power the LED from the (switched) battery rail, not from 5 V**; if it must be on 5 V, add a 74AHCT1G125-type buffer [INF].

**Sleep:** an idle WS2812B draws 0.6–1 mA continuously, about 20–30 × the MCU board's deep-sleep current. The LED supply must be behind the power-enable switch.

**Recommendation:** single WS2812B/SK6812 mini PCB behind the disc. One 120° emitter needs roughly 8–12 mm of distance plus a diffusing disc to light Ø20–25 mm evenly [INF]; if that depth is unavailable, the Ø23 mm Jewel 7 fills the disc from ~5 mm at the cost of 7× the quiescent and peak current.

---

## 5. Wake / presence sensors

| Approach | Part / module | Dimensions (mm) | Idle current | Notes | Conf. |
| --- | --- | --- | --- | --- | --- |
| **Hall switch** | **TI DRV5032FB** (5 Hz, omnipolar, push-pull, B_OP 1.5 / 3 / 4.8 mT min/typ/max) | SOT-23 2.92 × 2.37; X2SON 1.4 × 1.1; **TO-92 (LPG) 4 × 1.52** (TI package table) | **0.54 µA** at 1.8 V, **0.69 µA** at 3 V (1.8 max), 1.06 µA at 5 V | 1.65–5.5 V; output low when magnet present; either pole | [V1] TI datasheet, read directly |
| Hall switch, faster | DRV5032FA / FC (20 Hz; FC open-drain) | same | 1.3 µA at 1.8 V, 1.6 µA at 3 V (3.5 max) | same thresholds | [V1] |
| Hall switch, less sensitive | DRV5032AJ (4 / 7 / 9.5 mT, open-drain, 20 Hz) · DRV5032ZE (33 / 47 / 63 mT) | SOT-23, TO-92 (AJ also X2SON) | 1.6 µA at 3 V | use if the speaker/servo magnets bias an FB part | [V1] |
| Hall breakout | Adafruit / ScoutMakes DRV5032 #6051 (uses DRV5032FB, SOT-23) | **25.6 × 17.8 × 7.2** incl. JST-PH | as chip | 3-pin JST-PH + header; US$4.95, £5.90 The Pi Hut, €9.50 OpenCircuit | [V1] |
| **Reed switch** | generic N/O glass reed "2 × 14" (Standex-Meder, Littelfuse FLEX-14 class) | glass Ø2.2–2.28 × 14.0, leads Ø0.5; overall length with leads not verified (~44–56) | **0** when open; V/R_pull-up while closed (e.g. 3.3 µA with 1 MΩ) | sensitivity bands 10–15 AT up to 10–40 AT; fragile glass; responds to field **along** its axis, so a magnet centred over it face-on can fail to close it | [V2+] glass size |
| Vibration (pick-up) | SW-18010P spring switch, N/O | body Ø4.4–4.5 × 11–15.5 (sources disagree), ≈25 incl. pins | 0 | closes briefly on shock; no hold state; rated ~12 V / 20 mA | [V1], inconsistent |
| Vibration module | SW-420 + LM393 board | 32 × 14 | several mA (comparator + LEDs) [INF] | N/C sensor; module unsuitable for deep sleep — use a bare switch instead | [V2+] board size |
| Tilt | SW-520D ball switch | Ø5.2 × 11.5 | 0 when open | state depends on orientation — awkward in a ball that has no defined "up" | [V1] |
| Motion IC (for reference) | LIS3DH breakout (Adafruit #2809) | STEP available | µA-class in low-power wake-on-motion [MEM] | most reliable pick-up detection, needs I2C (2 pins) + INT | [MEM] |

Sources: https://www.ti.com/lit/ds/symlink/drv5032.pdf · https://www.adafruit.com/product/6051 · https://learn.adafruit.com/scoutmakes-drv5032-hall-sensor · https://www.mouser.at/new/littelfuse/Hamlin-FLEX-14 · https://uk.rs-online.com/web/p/reed-switches/9058871 · https://www.lcsc.com/product-detail/C2681585.html · https://components101.com/sensors/sw-420-vibration-sensor-module · https://protosupplies.com/product/sw-520d-ball-tilt-switch-sensor-2-pack/

**Recommendation:** DRV5032FB on an RTC GPIO (GPIO1–9) as the figurine wake source: a hall switch senses the field perpendicular to the shell (the direction a Tonie's base magnet points), costs under 1 µA and has no glass to break. Lay the TO-92 part flat against the inside of the shell under the "dock" spot. Add a bare SW-18010P to a second RTC GPIO (ext1 wake) if pick-up wake is wanted. Keep the reed switch as the zero-power fallback.

---

## 6. CAD dimensions of recommended parts

All values in mm. "Envelope" = suggested keep-out box including tolerance; where sources disagree both values are given.

### 6.1 Seeed XIAO ESP32-S3 Plus (first-choice MCU)

| Feature | Value | Basis |
| --- | --- | --- |
| PCB outline | 21.0 × 17.8 nominal; **21.14 × 17.78** measured in Seeed `BOTTOM.dxf`; corner radius ≈ 1.9 | [V2+] Seeed spec + Seeed DXF + reseller listings |
| Edge pads | 7 per long side, 2.54 pitch, rows 15.24 apart (centres 1.27 in from the long edges); first pad centre ≈2.92 from the USB edge, last ≈2.98 from the antenna edge | measured in Seeed `XIAO_ESP32S3_v1.1_Dimensioning.dxf` (non-Plus, same form factor) [V1 + INF for Plus] |
| Back pads | 9 extra half-hole pads at 1.27 pitch on the long edges, plus BAT+/BAT− pads and a B2B connector on the underside | Seeed wiki/product page [V1]; exact positions: take from `BOTTOM.dxf` |
| USB-C | centred on one short edge; shell slots 8.64 apart; **overhang beyond the PCB edge not dimensioned by Seeed** — estimate 1.5–2 mm | [INF] from connector footprint |
| PCB thickness | not stated by Seeed; one community measurement on the sibling XIAO ESP32-C3: 1.2 (1.3 over plating) | [V1], different board |
| Total height | **unverified**: listings say 3.5; the same community measurement found 4.5 over the USB-C connector vs 3.9 in documentation; one tutorial quotes 5 for the Plus (underside connector) | sources disagree |
| **Suggested envelope** | **24 × 18.5 × 6** (length includes USB-C overhang and plug clearance is extra) | [INF] — measure the purchased board |
| Antenna | U.FL connector at the short edge opposite USB; external FPC/rod antenna must be routed | Seeed [V1] |

### 6.2 Unexpected Maker TinyS3 (fallback MCU)

| Feature | Value | Basis |
| --- | --- | --- |
| PCB outline | **35 × 17.8** | [V2+] UM site, CNX Software, espboards.dev |
| Max thickness | 4.3 at the USB-C end | [V1] UM |
| Headers | 2.54 pitch on both long edges; exact pin count/positions: take from UM's STEP / KiCad footprint | not extracted |
| Envelope | 37 × 18.5 × 5 (without headers) | [INF] |

### 6.3 M5Stack StampS3 (budget fallback, fully dimensioned drawing)

24.0 × 18.0 × 4.7 total; PCB 1.0; USB-C overhang ≈1.96 beyond the short edge; pad rows 15.24 apart, pads at 1.27 / 2.54 pitch; one screw boss (read off the drawing image as 8.5 from the USB edge and 4.5 from a long edge — confirm against the STEP). [V1, M5Stack drawing]

### 6.4 MAX98357A breakout

| Feature | Adafruit #3006 (from Eagle board file) | Generic clone |
| --- | --- | --- |
| Outline | **17.78 × 19.05**, corner R 2.54 (product page: 19.4 × 17.8) | 19 × 18 (AZ-Delivery); 18 × 18 (DFRobot variant) |
| Thickness | 3.0 (product page; excludes terminal block) | 3 |
| Mounting holes | 2 × Ø2.5 plated at (2.54, 16.51) and (15.24, 16.51) → 12.7 apart, 2.54 from the top and side edges | usually present, positions not verified |
| Header | 1 × 7 at 2.54 pitch on the line y = 2.54; pin centres x = 1.27 … 16.51; order LRC, BCLK, DIN, GAIN, SD, GND, Vin | same order |
| Terminal block | 3.5 pitch, centred at (8.89, 15.49); pads at x = 7.09 (−) and 10.59 (+) | loose in the bag |
| **Suggested envelope** | **20 × 18.5 × 4** with wires soldered directly and no terminal block; **20 × 18.5 × 11** with the terminal block fitted | [INF] |

Coordinate convention for the Adafruit column: components facing up, header along the bottom edge, origin at the lower-left board corner (the corner next to the LRC pin); x runs along the 17.78 side, y along the 19.05 side. Vin is the header pin at x = 16.51.

### 6.5 Speakers

| Part | Envelope | Details |
| --- | --- | --- |
| **Visaton K 40** | **Ø40.2 × 4.6** (Ø40 ± 0.2, depth 4.3 ± 0.3) | rim 1.3 ± 0.2 thick; basket Ø36 ± 0.3; rear cup Ø16 ± 0.3; solder tags on the back near the edge; baffle opening Ø36.5; no screw holes → printed clamp ring or adhesive bead |
| Visaton K 28 WP | Ø28 × 5.5 | body Ø27, step Ø26, rear cup Ø16; diaphragm zone Ø24.8; front rim 0.7; baffle opening Ø24 |
| Visaton BF 32 | 32 × 32 × 15 | flange 1.7; 4 holes Ø2 on a 24.5 × 24.5 square; body Ø29 / Ø26; 11 from flange back to rear face; opening Ø31.5 |

### 6.6 LED

Single WS2812B/SK6812 mini PCB: disc Ø10 nominal (9.1–11 across suppliers) × 3.0–3.2 total; LED body 5.0 × 5.0 (5.4 over leads) × 1.6 centred on the front; six solder pads on the back (5V/GND/DIN and 5V/GND/DOUT). **Envelope Ø11 × 3.5 plus wire exit at the back.** [V2+]

### 6.7 Wake sensors

- DRV5032 TO-92 (LPG): 4.0 × 1.52 per TI's package table; body height ≈3.2 and 1.27 lead pitch are from memory of the TI outline — confirm on the datasheet's mechanical page before modelling a pocket. [V1 / MEM]
- Adafruit/ScoutMakes #6051 breakout: 25.6 × 17.8 × 7.2. [V1]
- Reed switch: glass Ø2.3 × 14 max; allow a Ø3 × 16 pocket and bend the leads ≥ 3 mm away from the glass seals. [V2+ glass; INF pocket]
- SW-18010P: allow Ø5 × 16 body plus leads. [INF from disagreeing listings]

---

## 7. STEP / 3D / drawing sources (not all downloaded)

| Part | URL |
| --- | --- |
| XIAO ESP32-S3 3D model (STEP, zip) | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/seeed-studio-xiao-esp32s3-3d_model.zip |
| XIAO ESP32-S3 Plus 3D model | https://grabcad.com/library/seeed-studio-xiao-esp32s3-plus-1/files (login needed) |
| XIAO ESP32-S3 Plus DXF top / bottom | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/TOP.dxf · https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/BOTTOM.dxf |
| XIAO ESP32-S3 v1.1 dimension DXF | https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_v1.1_Dimensioning.dxf |
| UM TinyS3 STEP, KiCad symbol/footprint, schematic | https://github.com/UnexpectedMaker/esp32s3 |
| M5 StampS3 STEP and drawing | https://github.com/m5stack/M5_Hardware/blob/master/KiCad/3D/M5Stack.3dshapes/Stamp-S3.step · https://github.com/m5stack/M5_Hardware/tree/master/Products/S007_Stamp-S3/Structures |
| LOLIN S3 Mini drawing | https://www.wemos.cc/en/latest/_static/files/dim_s3_mini_v1.0.0.pdf |
| Adafruit MAX98357 #3006 (STEP/STL/F3D) | https://github.com/adafruit/Adafruit_CAD_Parts/tree/main/3006%20MAX98357 |
| Adafruit MAX98357 Eagle files | https://github.com/adafruit/Adafruit-MAX98357-I2S-Amp-Breakout |
| Adafruit CAD parts also present in the same repo | `3968 Speaker 40mm`, `3923 Mini Oval Speaker`, `2226 NeoPixel Jewel`, `2130 PAM8302`, `4682 Micro SD Breakout`, `5426 QT Py ESP32-S3`, `2809 LIS3DH` under https://github.com/adafruit/Adafruit_CAD_Parts |
| Visaton speakers | Datasheets carry a "CAD" badge, but no STEP link is present in the product-page HTML; request/download via visaton.de was not confirmed |
| KiCad packages3D (WS2812B 5050, SK6812 MINI, TO-92, SOT-23) | https://gitlab.com/kicad/libraries/kicad-packages3D (`LED_SMD.3dshapes`, `Package_TO_SOT_THT.3dshapes`, `Package_TO_SOT_SMD.3dshapes`) — file names not opened in this session [MEM] |

Files saved in `research/downloads/mcu_audio/`: Seeed DXFs and STEP zip (+ extracted folder), M5 StampS3 drawing, LOLIN drawing, MAX98357A datasheet, Adafruit `.brd`, ten Visaton datasheets and two sketches, Adafruit #3968 / #4227 speaker specs, TI DRV5032 datasheet, SK6812 MINI-E and two WS2812B datasheets, two XIAO reseller PDFs.

---

## 8. Unlikely candidates, documented briefly

### 8.1 GPS modules

| Module | Dimensions (mm) | Current | Conf. |
| --- | --- | --- | --- |
| ATGM336H-5N (bare) | 9.7 × 10.1 | — | [V2+] LCSC + spec sheet |
| ATGM336H breakout | 13.1 × 15.7 (≈13 × 16) + external active ceramic antenna on IPEX | < 25 mA at 3.3 V; 3.3–5 V supply | [V2+] Open Electronics + Powerlab |
| u-blox NEO-6M "GY-NEO6MV2" | 25 × 35 most listings (also 25.5 × 31 and 26 × 36.5 reported) + separate antenna 25 × 25 (28 × 28 in one manual) | ≈45 mA typ, 3.3–5 V | [V2+] |
| u-blox NEO-M8N boards | **not found** in this session | — | unverified |
| Quectel L76K (bare) | 9.7 × 10.1 × 2.4 (Quectel lists 10.1 × 9.7 × 2.3 for the L76 family) | not retrieved | [V2+] dims |

A GPS also needs a sky-facing patch antenna (15–25 mm square, 4–8 mm thick), which competes with the speaker and RFID antenna for shell area [INF].

### 8.2 microSD breakouts

| Board | Dimensions (mm) | Notes | Conf. |
| --- | --- | --- | --- |
| Adafruit #4682 (SPI/SDIO, 3 V only) | 25.4 × 22.8 × 3.5, 2.5 g | no level shifter, STEP in Adafruit CAD repo | [V1] |
| Adafruit #254 (5 V-ready) | 31.85 × 25.4 × 3.75, 3.43 g, four #2 holes | regulator (150 mA) + level-shift chip | [V1] |
| Generic "Micro SD card adapter" with LDO + buffer | ≈42 × 24 | mA-class idle due to LDO/buffer | [MEM] |

Card idle current is card-dependent (roughly 0.1–1 mA) and tens of mA when active [MEM]; a card must be power-gated in deep sleep.

---

## 9. Rejected / not chosen candidates

| Candidate | Reason |
| --- | --- |
| Waveshare ESP32-S3-Zero (standard), ESP32-S3 SuperMini, LOLIN S3 Mini | 4 MB flash (< 8 MB). LOLIN is also the largest footprint that still fits. SuperMini specs vary by factory |
| Seeed XIAO ESP32-S3 (non-Plus) | 11 header GPIO; reaching 14 means soldering to round JTAG test pads; Plus costs about the same |
| Adafruit QT Py ESP32-S3 | 13 GPIO (one short), no charger, ≈70 µA sleep, 8 MB version out of stock |
| LilyGO T7-S3, ESP32-S3-DevKitC-1 | exceed ~26 × 36 mm |
| UM OMGS3 / NanoS3 | fine-pitch pads only, costly; no advantage over XIAO Plus here |
| Classic ESP32 minis (M5Stamp Pico, TinyPICO) | only needed for Bluetooth Classic/A2DP, which the design does not use; 4 MB flash, 12–14 GPIO |
| ESP32-C3 / C6 minis | 4 MB flash, 11–13 GPIO |
| DFPlayer Mini | audio on SD card only, no MCU upload, UART-level control, high standby current |
| PAM8302A + DAC | extra DAC part needed on an S3; 0.5 mA shutdown |
| MAX98360A, NS4168 | no well-documented hobby breakout found; NS4168 datasheet not retrieved |
| Visaton BF 37, BF 45, FRS 5 | 23.8 / 27.6 / 31.5 mm deep (> 20 mm); FRS 5 weighs 126 g |
| Visaton K 45, K 50 WP | good speech drivers but Ø45–50 × 18 mm and 46–48 g; keep in mind only if the shell layout has room |
| Adafruit #3968 and generic 40 mm 4 Ω 3 W | 20–21 mm deep (at/over the limit), 78 dB — needs 3× the power of the K 40 for the same level |
| Adafruit #1890 / #1891 / #3923 / #4227 | 0.25–1 W, no SPL data, mostly out of stock |
| Same Sky CMS-40504N-L152 | thin and 4 Ω, but ≈80 dB at 1 m equivalent and narrower EU hobby availability; single-source data |
| APA106 / PL9823 through-hole LEDs | need 4.5–6 V and therefore a level shifter from 3.3 V logic |
| NeoPixel Jewel 7 (as first choice) | 7 LEDs for one indicator: 7× quiescent and peak current |
| SW-420 module, SW-520D tilt | module draws mA; tilt state is meaningless in a ball |

---

## 10. Open risks and items not verified

1. **XIAO ESP32-S3 Plus height and USB-C overhang** — no manufacturer dimension found; values in §6.1 are estimates. Measure before finalising the pocket.
2. **XIAO ESP32-S3 Plus deep sleep** — 33.5 µA (Seeed) vs ≈69 µA (one reseller table); Seeed's own feature text also quotes the non-Plus figure of 14 µA. Measure on the bench.
3. **XIAO Plus battery sensing** — community reports say there is no divider on GPIO10 despite the `ADC_BAT` label; Seeed's schematic was not opened. Budget one ADC1 pin and two resistors.
4. **XIAO Plus back pads** — 1.27 mm half-holes are the only way past 11 GPIO; soldering quality and strain relief of those wires is a build risk. The TinyS3 avoids this.
5. **TinyS3 charge current and deep-sleep figure** — not published in any source found; the newer TinyS3[D] revision changes battery sensing to an I2C fuel gauge (reseller text, not checked against UM documentation).
6. **Waveshare ESP32-S3-Zero-N8R8** — existence confirmed on the Waveshare docs SKU table; flash/PSRAM size, pinout text and sleep current not confirmed.
7. **Charging** — 100 mA on the XIAO Plus is slow for an 18650; interaction between an external charger and the on-board one needs a decision in the power design.
8. **Amp breakout variants** — clone boards differ in SD pull-up value and in whether the terminal block is fitted; the Adafruit board's 3.0 mm height excludes its pre-soldered terminal block. Hole positions are verified only for the Adafruit design file.
9. **Amp in sleep** — with clocks stopped but SD high the MAX98357A still draws ≈340 µA; SD must be driven low (0.6 µA, plus ≈4 µA through Adafruit's 1 MΩ pull-up) or the amp supply switched.
10. **LED quiescent current and low-battery colour** — 0.6–1 mA when idle; blue weakens below ≈3.5 V. Gate its supply; expect colour shift near empty.
11. **Magnet interactions** — the speaker magnet and the servo motor sit within a few centimetres of the hall/reed sensor; a DRV5032FB trips at 1.5–4.8 mT. The field of the Tonie base magnet through the shell was not measured. Place the sensor away from the speaker, and be ready to swap to the AJ (≤ 9.5 mT) or ZE (≤ 63 mT) variant after a bench test.
12. **Class-D EMI vs RFID** — the filterless amplifier output and speaker leads near the PN5180 antenna may disturb reads; keep leads short and twisted, and consider muting during a read [INF].
13. **Speaker acoustics** — SPL figures are free-air/baffle values at 1 W; behaviour in a small sealed printed sphere behind grille holes was not assessed. K 40's upper limit is 6 kHz (sibilants slightly dull).
14. **K 36 WP, K 34 WP, BF 32, K 50 WP** dimensions are single-source (Visaton). Only K 40 and K 28 WP have an independent shop confirmation.
15. **Prices and stock** are snapshots from search results on the access date; Reichelt, Conrad, Berrybase and Eckstein listings were not opened.
16. **Not verified at all:** NEO-M8N board sizes, generic "28 mm 8 Ω 2 W" speaker, generic microSD adapter size, DFPlayer standby current, DRV5032 TO-92 body height, KiCad 3D file names.
