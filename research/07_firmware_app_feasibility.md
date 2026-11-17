# 07 – Firmware and phone app: feasibility, architecture, pin map, risks

Access date for all web sources: **2026-11-17**.
Downloaded reference material (untrusted, never executed): `research/downloads/firmware/`.
No firmware or app code was written for this note.

Evidence labels (same scheme as note 05):

- **[V3]** verified by three or more independent sources
- **[V2]** verified by two independent sources
- **[S1]** single source
- **[INF]** inference / calculation from sourced numbers
- **[UNV]** not verified in this research run (general knowledge or estimate; measure before relying on it)

Scope. This note covers the firmware and the phone app. The tag protocol is in note 01, reader modules, read range and ferrite in note 02, boards / amplifier / LED / wake sensor in note 04, power and servo in note 05, mechanics in note 06. Where this note depends on or disagrees with them, it says so (section 16).

Limits of this run. The session's web-search budget ran out near the end, and esp32.com (bot wall) and community.nxp.com (HTTP 403) could not be opened directly. Figures from those two sites come from search-result summaries and are marked **[S1, snippet]**. Everything still open is listed in section 16.

---

## 1. Verdict

| # | Requirement | Feasible? | How | Evidence |
|---|---|---|---|---|
| 1 | All hunt functions managed from the app over a wireless link | **Yes** | BLE GATT, phone = central, device = NimBLE peripheral with one custom service | S3 supports LE Data Length Extension, 2M PHY, advertising extensions (Espressif feature table) **[S1 official]**; NimBLE-Arduino 2.5.2 lists ESP32S3 **[S1]** |
| 2 | BLE + I2S audio + SPI RFID + LED + servo on one ESP32-S3 | **Yes, with three firmware rules** | Independent peripherals (SPI2, I2S0, RMT, LEDC). Rules: no flash writes while audio plays; servo never together with RF field or audio (note 05); RFID task started after the other drivers | MP3 decode ≈ 8 % of one core, 23–28 kB RAM **[V2]**; ESPuino runs PN5180 + audio + Bluetooth/Wi-Fi on the classic ESP32 **[S1]**; the same mix on an S3 with NimBLE was not found documented **[INF]** → breadboard soak test |
| 3 | Read Tonies (SLIX-L in privacy mode) with a PN5180 | **Yes (protocol)**; range unproven | `tueddy/PN5180-Library` already contains GET RANDOM NUMBER (0xB2), SET PASSWORD (0xB3) and `disablePrivacyMode()`; ESPuino shows the poll loop | Library source + ESPuino source + note 01 **[V3]**; read distance through the shell: **[UNV]** |
| 4 | Four voice messages stored in the device, playable years later without a phone | **Yes for the data; the battery needs a recharge after long storage** | Files in a LittleFS partition of the module's NOR flash, UID→file table in NVS + file | LittleFS has integrated power-failure protection (Espressif) **[S1 official]**; NOR flash class figures ≥ 20 years retention, 100 k cycles **[V2, snippet]**; Li-ion self-discharge 1–2 %/month plus protection circuit **[S1]** |
| 5 | Deep sleep, wake by presenting a Tonie, identify, play, sleep | **Yes** | ext1 wake on an RTC GPIO (0–21) from the hall switch / reed; enable 5 V; unlock + inventory; play | Wake sources and GPIO range (Espressif) **[S1 official]**; chip 7–8 µA (datasheet) **[S1]**; wake-to-sound ≈ 0.4–1 s **[INF]** |
| 6 | Upload the recordings from the phone | **Yes** | Chunked file transfer over BLE (write without response + acknowledgements). 500 kB takes ≈ 6–60 s depending on the phone. Fallbacks: Wi-Fi SoftAP + HTTP, or USB | ESP32-S3 GATT write 753 kbps (1M) / 1.34 Mbps (2M) between two ESP32s **[S1 official]**; phone figures 8–90 kB/s **[S1 each]** |
| 7 | Spoken hints triggered from the app | **Yes** | Pre-stored clips, "play clip n" command | follows from 1, 2, 4 |
| 8 | Audio pushed live from the phone | **Partly** | "Record → upload → play" over BLE works with a few seconds of delay. True live audio: no LE Audio on the S3, no A2DP on the S3; a custom BLE or Wi-Fi stream is possible but is a project of its own | LE Isochronous Channels "unsupported" on ESP32-S3 in ESP-IDF v6.0.2 and in the latest docs **[V2, same vendor, two doc versions]** |
| 9 | LED blink pattern from phone GPS proximity | **Yes, in coarse bands** | Phone computes the distance and sends a blink command only when the band changes; device blinks autonomously | Smartphone GPS ≈ 4.9 m radius under open sky, worse near buildings (GPS.gov) **[S1 official]** |
| 10 | Lid opening by servo on command | **Yes** | LEDC 50 Hz, 14-bit; switched 5 V boost; sequencing in firmware | LEDC limits from `soc_caps.h`, API from core header **[S1 official each]**; power integrity per note 05 **[INF]** |
| 11 | Battery monitoring | **Yes** | External divider on an ADC1 pin, eFuse-calibrated reading | ADC1 = GPIO1–10, calibration scheme, ranges (Espressif) **[S1 official]** |
| 12 | Phone app by one hobby developer | **Yes on Android; iOS costs more** | Android: Flutter or Kotlin, or a Web Bluetooth page in Chrome. iOS: native app (Mac, Xcode) or a third-party Web-BLE browser | Web Bluetooth: Chrome for Android yes, Safari no (caniuse + W3C CG status page) **[V2]** |
| 13 | Enough pins on a small ESP32-S3 board | **Yes on XIAO ESP32-S3 Plus (20 pads) and TinyS3; no on the plain XIAO ESP32-S3 (11)** | 15 signals mandatory, 17 with button and PN5180 IRQ | Seeed wiki + arduino-esp32 variant file **[V2]** |

**Nothing found makes the planned hardware unable to do the job.** The points that can still sink it are physical, not software: Tonie read range through the shell next to the figure's magnet, the wake sensor's response to that magnet, the real sleep current of the assembled device, and supply sag when the servo stalls.

### Recommended baseline

| Item | Recommendation |
|---|---|
| Flash | **16 MB** (XIAO ESP32-S3 Plus has it). 8 MB works with a custom partition table. 4 MB is not recommended |
| PSRAM | Not needed for MP3/AAC decoding; **recommended** (≥ 2 MB) because it removes the RAM risk and lets every audio library be used. `ESP32-audioI2S` refuses to work without it |
| Board | ≥ 15 usable GPIO of which ≥ 2 RTC-capable (GPIO0–21) and 1 on ADC1 (GPIO1–10); board deep-sleep current ≤ ≈ 50 µA; native USB; BOOT/RESET reachable after assembly |
| Firmware stack | Arduino-ESP32 **3.3.x** (ESP-IDF 5.5) through PlatformIO/pioarduino with pinned versions; NimBLE (NimBLE-Arduino 2.5.x or the core's BLE library, which runs on NimBLE on the S3 since 3.3.0); `tueddy/PN5180-Library` 2.3.7; LittleFS; one audio library (section 2.1); direct LEDC calls for the servo; `rgbLedWrite()` for the LED |
| Wireless | BLE only during the hunt. Wi-Fi SoftAP + HTTP as an optional maintenance mode (bulk upload, OTA) |
| Audio files | Prepared on a PC: **MP3, mono, 44.1 kHz (or 32 kHz), 48–64 kbit/s**. The app uploads files; it does not need to encode |
| Wake | Hall switch (note 04) and, if the translucent button is a real switch, the button; both active-low on ext1. PN5180 LPCD not recommended |

---

## 2. Q1 – Concurrent BLE + I2S audio + SPI RFID on the ESP32-S3

### 2.1 Framework and library status

| Component | State on the access date | ESP32-S3 | Notes | Label |
|---|---|---|---|---|
| Arduino-ESP32 core | 3.3.12 (2026-09-18, ESP-IDF 5.5.5); 4.0.0-RC1 (2026-09-23, ESP-IDF 6.1) | yes | Stay on 3.3.x; 4.0 is a release candidate with a rewritten Bluetooth layer (Espressif blog, 2026-10-20) | S1 (GitHub releases) |
| ESP-IDF | "stable" documentation is v6.1.1; 5.5.x is what Arduino 3.3 uses | yes | – | S1 |
| NimBLE-Arduino (h2zero) | 2.5.2 (2026-10-25) | "ESP32, ESP32C3, ESP32S3, ESP32C6, ESP32H2, ESP32C2, ESP32C5" | 2.5.1 fixed "Arduino 3.3.11 build/crash with esp32 c5/c6 variants", so it tracks core 3.3.x. An L2CAP API exists (2.5.0 notes: "l2Cap Disconnect API") | S1 |
| esp-nimble-cpp (same author, for ESP-IDF) | active | yes | "nearly 50% reduction in flash use and approx. 100kB less ram consumed vs the original! … Your results may vary" (versus the Bluedroid-based library) | S1 (author's claim) |
| Core's own `BLE` library | NimBLE support added in 3.3.0 ("feat(NimBLE): Add support for NimBLE") | lib-builder `defconfig.esp32s3`: `CONFIG_BT_NIMBLE_ENABLED=y`, `CONFIG_BT_BLUEDROID_ENABLED=n` | On the S3 the built-in library therefore already runs on NimBLE; Bluedroid-only sketches no longer compile | V2 (release notes + build config; a third-party report says the same) |
| arduino-audio-tools (pschatzmann) | pushed 2026-11-09; ESPuino pins v1.2.6 | yes | Stream pipeline; decoders: MP3 (Helix, MAD, minimp3), AAC (Helix, FDK), Opus/Ogg, ADPCM, WAV, FLAC, Vorbis. Author: MP3/AAC "require a lot of memory and are at the edge what a Microcontroller can do … prefer a lean format like ADPCM" (written for all MCUs, not only the S3) | S1 |
| ESP32-audioI2S (schreibfaul1) | pushed 2026-11-16; ESPuino pins v4.0.1 | yes | README: "only works on multi-core chips like ESP32-S3, ESP32-S31 and ESP32-P4 … **PSRAM is required!**". Codecs wav, mp3, aac, flac, opus, vorbis; containers ogg, mp4, m3u8; 16–48 kHz input; "The I2S output frequency is always 48kHz"; "Works with MAX98357A". Issues and discussions report PSRAM-related problems on core 3.x (#875, #983, #1006) | S1 (README); issues S1, snippet |
| ESP8266Audio (earlephilhower) | pushed 2026-11-16 | yes, needs the IDF 5 I2S API (pioarduino) | MP3 (libMAD), AAC (Helix, "about 30KB of heap"), Opus, FLAC, WAV. README points ESP32 users to the author's BackgroundAudio | S1 |
| Espressif `esp_audio_codec` (ESP-IDF / ESP-ADF) | 2.6.2 | measured on ESP32-S3R8 | Closed-source, light decoders – table in 2.2 | S1 (Espressif) |
| ESPuino (integration precedent) | active; changelog entries to 2026-07 | has an `esp32-s3-devkitc-1` environment | PN5180 (own fork of the tueddy library) + ESP32-audioI2S v4.0.1 + arduino-audio-tools + ESP32-A2DP + ESPAsyncWebServer v3.12.1 on pioarduino 55.03.312-1 = "Arduino 3.3.12 (ESP-IDF 5.5.5)". README: "ESPuino doesn't run safely on ESP32 without PSRAM" | S1 (repository files read directly) |

Reading: every building block exists for the S3 on core 3.3.x and is maintained. **ESPuino is the closest working reference** (same reader, same amplifier family, audio from files, deep sleep), but it targets the classic ESP32 and Bluedroid; nobody was found documenting exactly "NimBLE GATT + file playback + PN5180 on an S3", so that combination is plausible, not proven **[INF]**.

Choice of audio library **[INF]**:

- **With PSRAM on the board: ESP32-audioI2S first.** It is what ESPuino uses for file playback, it handles MP3 and AAC/M4A, and its fixed 48 kHz output sidesteps the amplifier's sample-rate restriction (2.2). Its behaviour next to NimBLE is the thing to test.
- **Fallback, and the choice without PSRAM: arduino-audio-tools.** An explicit pipeline (file → decoder → resampler / volume → I2S) with no PSRAM requirement; more assembly work.
- **ESP-IDF route:** Espressif's `esp_audio_codec` has the smallest decoders, at the price of leaving the Arduino libraries behind.

### 2.2 Codecs for speech

| Codec | Sensible setting for speech | Decoder RAM on the S3 | CPU on the S3 (240 MHz) | PSRAM needed? | Where the file can be made | Label |
|---|---|---|---|---|---|---|
| **MP3** | mono, 44.1 or 32 kHz, 48–64 kbit/s | 28 kB heap (Espressif); ≈ 22.8 kB (ESPHome micro-mp3) | 8.17 % (Espressif, 44.1 kHz stereo); real-time factor 0.076 = 13× real time (micro-mp3, 48 kHz stereo 128 kbit/s) | **No** | PC (ffmpeg, Audacity). No stock MP3 encoder on Android **[UNV]** | V2 |
| AAC-LC | mono, 44.1 kHz, 32–64 kbit/s, ADTS or M4A | 51.2 kB (Espressif); "about 30KB" (ESP8266Audio, Helix) | 6.75 % | No | Android `MediaRecorder` `AAC_ADTS`; iOS natively **[UNV for iOS]** | S1 each |
| Opus | mono, 16–24 kbit/s | 26.6 kB (Espressif decoder). libopus ports: 30–50 kB state **plus** 40–60 kB task stack, or a 120 kB "pseudostack" (ESPHome micro-opus) | 5.86 % (Espressif); SILK ≈ 2 %, CELT ≈ 8–9 % (micro-opus) | Espressif decoder: no. libopus ports: "PSRAM is strongly recommended" | Android `MediaRecorder` OGG + OPUS from API 29; ffmpeg | S1 each |
| IMA ADPCM (WAV) | 16 kHz, 4 bit = 64 kbit/s | 0.11 kB | 2.43 % | No | ffmpeg | S1 |
| PCM WAV | 16 kHz, 16 bit = 256 kbit/s | none | negligible | No | anything | – |

Espressif adds that "the task running the decoder should have stack size of about 20K" for its decoders **[S1]**.

**Does MP3/Opus decoding need PSRAM?** MP3: no (two sources). Opus: not with Espressif's decoder; yes in practice with the libopus-based Arduino ports once BLE (and possibly Wi-Fi) share the internal RAM. For orientation on RAM: ESP-ADF's table (classic ESP32, Bluedroid) starts from 290 kB spare internal RAM and charges 50 kB+ for Wi-Fi and 140 kB for Bluetooth, "50kB if only BLE needed" **[S1]**; NimBLE is lighter than that **[S1, author's claim]**. With a PSRAM board (XIAO ESP32-S3 Plus, TinyS3) the question disappears.

**MAX98357A sample-rate trap.** The datasheet states: "LRCLK ONLY supports 8kHz, 16kHz, 32kHz, 44.1kHz, 48kHz, 88.2kHz and 96kHz frequencies. LRCLK clocks at 11.025kHz, 12kHz, 22.05kHz and 24kHz are NOT supported." **[S1, datasheet read directly]** MP3 below roughly 40 kbit/s mono is normally MPEG-2 at 16 / 22.05 / 24 kHz **[S1 for the MPEG-2 rate set; the exact switch-over is UNV]**, and Opus decoders can output 24 kHz **[UNV]**. Either encode at 44.1 / 32 / 16 kHz, or let the library resample (ESP32-audioI2S always outputs 48 kHz). Also: driving `SD_MODE` straight to 3.3 V selects the **left** channel (> 1.4 V), so mono material must be on the left channel or on both (note 04 has the threshold table).

### 2.3 Known conflicts and how they apply here

| Conflict | Source statement | Consequence for this device | Label |
|---|---|---|---|
| Flash writes stall everything | "When the caches are disabled, all non-IRAM-safe interrupts will be disabled, and all other tasks are suspended. The other core will be polling in a busy loop." (ESP-IDF, SPI flash concurrency). Forum reports of I2S recording breaking up while writing SPIFFS/LittleFS | **Never write to flash while audio plays**: no upload during playback, no NVS commit (settings, bonding) during playback. Upload and playback are separate states | S1 official + S1 forum, snippet |
| BLE + Wi-Fi share one radio | Coexistence table for the S3: Wi-Fi STA (scan / connecting / connected) with BLE scan / advertising / connected = "Y"; **SoftAP connecting / connected with BLE = "C1: supported but the performance is unstable"** | Do not rely on BLE while a phone is attached to the device's SoftAP. Maintenance mode = Wi-Fi only | S1 official |
| RMT LED flicker with radio active | Known for long strips: late refill interrupts starve the RMT memory (several forum threads) | One LED = 24 RMT symbols; a channel's own memory holds 48 (`SOC_RMT_MEM_WORDS_PER_CHANNEL 48`). The whole frame is loaded before transmission, so no refill interrupt is involved and the usual flicker mechanism does not apply **[INF]** | S1, snippet + S1 official + INF |
| PN5180 task versus start-up | ESPuino comment: running the RFID task's SPI traffic "concurrently with the rest of setup()'s peripheral init … was found to cause an intermittent full boot-hang", fixed by starting the task after peripheral init (changelog 2026-07-10) | Start RFID polling last | S1 |
| PN5180 can wedge | ESPuino comment: "The PN5180 can start returning corrupted responses and then stop answering until it is reset" | Keep a re-initialisation path (hard reset through RST) and a command timeout | S1 |
| ADC2 with radio | "ADC2 is also used by Wi-Fi" (ESP-IDF) | Battery sense on ADC1 (GPIO1–10) | S1 official |
| USB console and sleep | "If the application enters Deep-sleep mode, the USB Serial/JTAG device disappears from the system." Recovery after a pin mishap: "manually put the ESP32-S3 into download mode by pulling low GPIO0 and resetting the chip" | Keep BOOT and RESET reachable in the finished ball, or keep the device awake for some seconds after a button wake so a flash tool can connect | S1 official |
| PSRAM test at every boot | Arduino `psramInit()` calls `testSPIRAM()` → `esp_psram_extram_test()`; the function is weak ("allows user to bypass SPI RAM test routine"). ESP-IDF: "Disable this for slightly faster startup" | Adds to wake latency on an 8 MB PSRAM board; duration not measured **[UNV]**. Can be bypassed | S1 official (source code) |

Sources: https://github.com/espressif/arduino-esp32/releases · https://developer.espressif.com/blog/2026/10/arduino-bluetooth-refactor/ · https://newreleases.io/project/github/espressif/arduino-esp32/release/3.3.0 · https://github.com/espressif/esp32-arduino-lib-builder/tree/master/configs · https://github.com/h2zero/NimBLE-Arduino · https://github.com/h2zero/esp-nimble-cpp · https://github.com/pschatzmann/arduino-audio-tools/wiki/Encoding-and-Decoding-of-Audio · https://github.com/schreibfaul1/ESP32-audioI2S · https://github.com/earlephilhower/ESP8266Audio · https://components.espressif.com/components/espressif/esp_audio_codec · https://components.espressif.com/components/esphome/micro-mp3 · https://components.espressif.com/components/esphome/micro-opus · https://docs.espressif.com/projects/esp-adf/en/release-v2.x/design-guide/design-considerations.html · https://github.com/biologist79/ESPuino (`platformio.ini`, `README.md`, `changelog.md`, `src/RfidPn5180.cpp`) · https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/spi_flash/spi_flash_concurrency.html · https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/coexist.html · https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/usb-serial-jtag-console.html · https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-psram.c · MAX98357A datasheet (mirror read: https://www.hestore.eu/prod_getfile.php?id=16440)

---

## 3. Q2 – Audio storage sizing

### 3.1 Application size

No measured build of this firmware exists. Reference points:

- Arduino's default layouts give the application 1.25 MiB (4 MB flash), 3.19 MiB (8 MB) or 6.25 MiB (16 MB) per OTA slot **[S1, partition CSVs read directly]**.
- ESPuino (Wi-Fi, web interface, FTP, MQTT, A2DP, audio, RFID) reserves **3.69 MiB** per application slot (`0x3B0000`) on 4 / 8 MB and 6.25 MiB on 16 MB **[S1]**. That is the upper bound for a far larger feature set.
- Estimate for this device: **≈ 0.9–1.3 MB** with NimBLE + one audio library + PN5180 + LittleFS, **≈ 1.5–1.9 MB** if Wi-Fi and an HTTP server are added **[UNV estimate]**.

Plan for **3 MiB per application slot**. That leaves margin and costs nothing on a 16 MB module.

**OTA or not?** Keep two OTA slots. The MCU board will be buried in a closed ball; a firmware fix after assembly then needs either its USB port or an update over BLE / Wi-Fi. On 16 MB the second slot is free. A BLE update of a 1.2 MB image takes about 15–150 s at the rates in section 4 **[INF]**.

### 3.2 File system

| | FatFS (+ wear levelling) | SPIFFS | LittleFS |
|---|---|---|---|
| Power-failure protection | "No" – "The biggest weakness is its low resilience against sudden power-off events" | "Partial" | **"Yes (integrated)"** |
| Wear levelling | optional layer | integrated (static) | integrated |
| Directories | yes | no | yes |
| Status | most supported | "Limited documentation, no ongoing development" | "Designed as fail-safe … fixed amount of RAM usage" |

All cells are quotations or paraphrases from Espressif's "File System Considerations" **[S1 official]**. **Use LittleFS.** Wear is not a concern: the message files are written a handful of times, against a class figure of 100 000 erase cycles **[V2, snippet]**.

Further protection for the four irreplaceable files **[INF]**:

1. Put them in their **own partition**, separate from hint clips and settings, and stop writing to it once the final recordings are in.
2. Upload to a temporary name, verify a CRC32, then rename.
3. Store size + CRC32 per file and check them on a schedule that does not delay playback.
4. After the final upload, read the partition back over USB (`esptool read_flash`) and keep the image with the original recordings.
5. A full-chip erase destroys the messages. The Arduino IDE option "Erase All Flash Before Sketch Upload" and `esptool erase_flash` must not be used after that point **[UNV for the menu wording]**.

### 3.3 Minutes of speech per layout

Assumption: 90 % of the partition is usable for file data **[UNV]**. Minutes of audio:

| Flash / layout | FS partition | MP3 64k | MP3 48k | MP3 32k | Opus 24k | Opus 16k | WAV 16 kHz 16 bit | ADPCM 16 kHz |
|---|---|---|---|---|---|---|---|---|
| 4 MB, `no_ota.csv` (app 2.0 MiB) | 1.88 MiB | 3.7 | 4.9 | 7.4 | 9.8 | 14.7 | 0.9 | 3.7 |
| 4 MB, `default.csv` (2 × 1.25 MiB) | 1.38 MiB | 2.7 | 3.6 | 5.4 | 7.2 | 10.8 | 0.7 | 2.7 |
| 8 MB, `default_8MB.csv` (2 × 3.19 MiB) | 1.50 MiB | 2.9 | 3.9 | 5.9 | 7.9 | 11.8 | 0.7 | 2.9 |
| 8 MB, custom: 2 × 2 MiB app | 3.81 MiB | 7.5 | 10.0 | 15.0 | 20.0 | 30.0 | 1.9 | 7.5 |
| 8 MB, custom: 1 × 3 MiB app, no OTA | 4.88 MiB | 9.6 | 12.8 | 19.2 | 25.6 | 38.3 | 2.4 | 9.6 |
| 16 MB, `default_16MB.csv` (2 × 6.25 MiB) | 3.38 MiB | 6.6 | 8.8 | 13.3 | 17.7 | 26.5 | 1.7 | 6.6 |
| 16 MB, `large_spiffs_16MB.csv` (2 × 4.5 MiB) | 6.88 MiB | 13.5 | 18.0 | 27.0 | 36.0 | 54.1 | 3.4 | 13.5 |
| **16 MB, `app3M_fat9M_16MB.csv` geometry (2 × 3 MiB)** | **9.88 MiB** | **19.4** | 25.9 | 38.8 | 51.8 | 77.7 | 4.9 | 19.4 |

Partition sizes are from the CSV files in `arduino-esp32/tools/partitions` **[S1]**; the minutes are arithmetic **[INF]**. Per MiB: 2.18 min at 64 kbit/s, 2.91 at 48, 4.37 at 32, 5.83 at 24, 8.74 at 16, 0.55 for 16 kHz/16-bit WAV. One minute costs 480 kB at 64 kbit/s and 1.92 MB as WAV.

Note that the stock 8 MB and 16 MB "default" tables waste most of the flash on oversized application slots; a custom table is needed either way.

**Demand estimate [INF]:** four messages of 1–2 min plus ten 15-second hints plus a few effects = 7–11 min. At 64 kbit/s that is 3.4–5.3 MB.

**Recommendation: 16 MB flash, two 3 MiB application slots, ≈ 9.7 MiB of LittleFS** (≈ 19 min at 64 kbit/s). An 8 MB board works with 2 × 2 MiB + 3.8 MiB (≈ 7.5 min at 64 kbit/s; use 48 kbit/s or Opus if more is needed). Uncompressed WAV does not fit sensibly on anything.

Sources: https://github.com/espressif/arduino-esp32/tree/master/tools/partitions · https://github.com/biologist79/ESPuino (`custom_4mb_noota.csv`, `custom_8mb_ota.csv`, `custom_16mb_ota.csv`) · https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/file-system-considerations.html · Winbond W25Q64JV / W25Q128JV distributor listings (search excerpts: "Min. 100K Program-Erase cycles per sector – More than 20-year data retention")

---

## 4. Q3 – Getting recordings into the device; live audio

### 4.1 BLE GATT file transfer

**What the link can do**

| Measurement | Value | Conditions | Label |
|---|---|---|---|
| ESP32-S3 GATT write, ESP32 ↔ ESP32 | ~753 kbit/s (94 kB/s) on 1M PHY; ~1.34 Mbit/s (168 kB/s) on 2M PHY | Espressif NimBLE throughput example, shield box, MTU 512, DLE 251, connection interval 7.5 ms. "Open-air results are typically lower" | S1 official |
| Same example, users' boards | 46 kB/s unmodified; 68.6 kB/s (1M) and 102.5 kB/s (2M) with logging off | ESP32-S3, IDF 5.0.2 | S1, snippet |
| Tuned link with a phone on one end | "around 90 kB/s" | Punch Through, all optimisations, no phone model given | S1 |
| "Newer Android and iOS devices with DLE on LE 1M PHY" | about 50 kB/s | Punch Through, older article | S1 |
| iPhone as central | about 5 packets of 242 bytes per connection event (≈ 80 kB/s at 15 ms) **[INF for the rate]** | Apple developer forum, peripheral → phone | S1 |
| iPad (A16, iPadOS 18.4.1) as central | one packet per event, "around 8 kB/s"; another report: one transmission per 30 ms on iPadOS 18 | Apple developer forum | S1 |

**Platform limits**

| | Android | iOS |
|---|---|---|
| ATT MTU | From Android 14 the stack "requests the BLE ATT MTU to 517 bytes when the first GATT client requests an MTU … and disregards all subsequent MTU requests" – the peripheral must accept 517 **[S1 official]** | "the device will request the optimal MTU size"; the accessory "should select an MTU equal to or greater than the device's MTU request" (Apple Accessory Design Guidelines R32 Update 1, §57.11) **[S1 official]**. No number is published |
| Connection interval | `requestConnectionPriority(HIGH)` → 11.25–15 ms (AOSP defaults 9–12 × 1.25 ms) **[S1, snippet]** | Requests must satisfy "Interval Min ≥ 15 ms", "Interval Min is a multiple of 15 ms", Interval Max ≥ Min + 15 ms or both 15 ms; supervision timeout 6–18 s (§57.6) **[V2: Apple + Silicon Labs note]**. The 7.5 ms used in Espressif's benchmark is refused |
| Data length extension | negotiated by the stack | "Accessories should support Data Packet Length Extension"; and "shall perform the packet length update procedure **before** … the Exchange MTU Request" (§57.7, §57.11) **[S1 official]** |
| 2M PHY | `setPreferredPhy`, API 26+; one report of the callback never firing on Android 13 **[S1, snippet]** | recommended by Apple engineers in the forum thread **[S1]** |
| Write queue | "We have observed undocumented queue depths of 1 with no feedback if the queue is overwritten … avoid relying on the OS to queue BLE writes" (Punch Through) **[S1]** | "the OS queue behaves predictably" **[S1]** |
| Alternative channel | L2CAP CoC from API 29 **[UNV]** | L2CAP channels "will dramatically increase your throughput" (Apple engineer) **[S1]** |

**Time to upload 500 kB [INF]**

| Effective rate | Case | 500 kB | All four messages (3.8 MB) |
|---|---|---|---|
| 0.5–2 kB/s | Naive implementation: MTU 23, write with response | 4–17 min | 0.5–2 h |
| 8 kB/s | One 244-byte packet per 30 ms (the bad iOS reports) | 62 s | 8 min |
| 20 kB/s | Conservative planning figure | 25 s | 3.2 min |
| 50 kB/s | Typical good phone, 1M PHY, DLE | 10 s | 77 s |
| 90 kB/s | Best case with a phone | 6 s | 43 s |

So BLE upload is practical **provided** the firmware accepts MTU 517 and DLE 251, the app uses write-without-response, and both sides implement flow control (window of chunks, acknowledgement with offset, resume after a drop, CRC at the end). Espressif's example lists the same levers: connection interval, connection event length, MTU, DLE, payload size, enough MSYS buffers (`CONFIG_BT_NIMBLE_MSYS_1_BLOCK_COUNT=50`), PHY **[S1 official]**. A naive transfer is unusable.

### 4.2 Wi-Fi SoftAP + HTTP upload

| Pro | Con |
|---|---|
| Works from any browser, including an iPhone or a laptop, with no app | The S3 lists SoftAP-connected + BLE as "unstable" → treat it as an exclusive mode **[S1 official]** |
| Fast: the flash, not the radio, is the limit (raw SPI-flash write ≈ 0.65 MB/s in Espressif's storage benchmark **[S1, snippet]**) | Android routes traffic away from a Wi-Fi network without internet; an app needs `WifiNetworkSpecifier` and to bind its sockets to that network **[S1, snippet]**. A browser user sees "no internet" prompts |
| Also gives OTA update and a file browser | Android 16 introduces a local-network runtime permission: opt-in now, "will be enforced at a later Android release" **[S1 official]** |
| Proven pattern (ESPuino uses ESPAsyncWebServer for exactly this) **[S1]** | More code, ≈ 50 kB+ RAM for Wi-Fi (ESP-ADF table) **[S1]**, larger image; Wi-Fi transmit peaks of 340 mA (datasheet, 802.11b at 21 dBm) on a rail that sags (note 05) **[S1 + INF]** |

**Recommendation.** BLE for control and for uploads in the normal app. A Wi-Fi maintenance mode (entered by a BLE command or by holding the button at power-up) is worthwhile as the fallback for bulk upload and firmware update. Lowest-effort fallback while the board is still accessible: write the files with the firmware's file-system image over USB.

### 4.3 Live audio "push" without A2DP

| Option | Verdict | Reason | Label |
|---|---|---|---|
| **Record on the phone → upload over BLE → play** | **Recommended** | A 10 s clip at 24–64 kbit/s is 30–80 kB = 1–10 s of transfer. Uses only what sections 4.1 and 2 already need | INF |
| Real-time stream over GATT | Possible, not recommended | Bit rate fits (16–64 kbit/s against ≥ 8 kB/s = 64 kbit/s worst case), but it needs a streaming codec path, jitter buffer and underrun handling on a link whose rate varies 10× between phones | INF |
| Wi-Fi stream (phone → device) | Possible, not recommended for the hunt | Needs a Wi-Fi link outdoors (phone hotspot or device SoftAP), coexistence with BLE, more power and code | INF |
| **Bluetooth LE Audio on the S3** | **Not available** | "LE Isochronous Channels (BIS/CIS)": controller, Bluedroid host and NimBLE host all "unsupported" for the ESP32-S3 in ESP-IDF v6.0.2 and in the latest documentation. Espressif's LE Audio documentation exists for the ESP32-H4 and ESP32-S31 and is labelled a preview. Arduino: "Support for Bluetooth LE Audio is actively in development for compatible Espressif SoCs" | V2 (two doc versions) + S1 |
| Classic ESP32 with A2DP sink + BLE | Works, different trade-off | see 4.4 | – |

### 4.4 Would a classic ESP32 (A2DP sink + BLE) be a better fit?

| Aspect | ESP32-S3 (plan) | Classic ESP32 with A2DP |
|---|---|---|
| Phone audio | Files only | The ball is a Bluetooth speaker: any app, voice memo or text-to-speech plays through it, no app code |
| Coexistence | BLE only | A2DP sink + GATT server in one image is an official Espressif example (`bluedroid/coex/a2dp_gatts_coex`, target ESP32) **[S1, snippet]**. One report of an iPhone refusing A2DP while a GATT link was active on IDF 4.2 **[S1, snippet]** |
| Host stack and RAM | NimBLE | Bluedroid is mandatory for Classic. ESP-ADF: Bluetooth 140 kB of 290 kB spare internal RAM without PSRAM, 95 kB with; "Bluetooth and Wi-Fi can not coexist without PSRAM because it will not leave enough memory for an audio application" **[S1]**. ESPuino requires a PSRAM module **[S1]** |
| BLE features | DLE, 2M PHY, advertising extensions | DLE supported; 2M PHY and advertising extensions "unsupported" **[S1 official]** → slower uploads |
| Boards | Small 16 MB boards with native USB exist (note 04) | Small boards are 4 MB (TinyPICO, M5Stamp Pico; note 04); no native USB |
| Behaviour on the day | App controls everything | The phone routes *all* media audio to the ball while connected; reconnecting after each sleep takes seconds; the app cannot keep its own audio on the phone easily **[UNV]** |

**Assessment.** Not a better fit for the stated requirements. It only wins if speaking live through the ball is a must-have, and it loses on flash size, upload speed, RAM and board choice. The newest alternative is the **ESP32-S31** (announced 2026-03-26: dual-core RISC-V, Wi-Fi 6, "Bluetooth 5.4 with both Bluetooth LE (Low Energy) and Classic (BR/EDR) support", LE Audio; mass production reported for July 2026) **[S1 for the specification, S1 snippet for availability]** – too new for a deadline project: small boards, Arduino support (4.0 release candidate only) and library support are not there yet **[INF]**.

Sources: https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/nimble/throughput_app/README.md · https://esp32.com/viewtopic.php?p=134183 (search excerpt) · https://punchthrough.com/ble-transfer-methods-for-throughput/ · https://punchthrough.com/ble-throughput-part-4/ · https://developer.apple.com/accessories/Accessory-Design-Guidelines.pdf (Release R32 Update 1, dated 2026-10-30; excerpt saved) · https://developer.apple.com/forums/thread/773555 · https://docs.silabs.com/bluetooth/8.3.0/mobile-apps-suitable-connection-parameters (search excerpt) · https://developer.android.com/about/versions/14/behavior-changes-all · https://developer.android.com/about/versions/16/behavior-changes-16 · https://docs.espressif.com/projects/esp-idf/en/v6.0.2/esp32s3/api-guides/ble/ble-feature-support-status.html · https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-guides/ble/ble-feature-support-status.html · https://docs.espressif.com/projects/esp-idf/en/v5.5.1/esp32/api-guides/ble/ble-feature-support-status.html · https://docs.espressif.com/projects/esp-idf/en/latest/esp32s31/api-guides/esp-ble-audio/ble-audio-feature-support-status.html · https://www.espressif.com/news/ESP32_S31_Release · https://developer.espressif.com/blog/2026/10/arduino-bluetooth-refactor/ · https://docs.espressif.com/projects/esp-adf/en/release-v2.x/design-guide/design-considerations.html · https://github.com/pschatzmann/ESP32-A2DP

---

## 5. Q4 – Phone app options

**Unknown that decides most of this: which phone the owner uses.** Nothing in the brief says Android or iPhone.

### 5.1 Options

| Option | Fit | Facts | Label |
|---|---|---|---|
| **Flutter** (`flutter_blue_plus` or `flutter_reactive_ble` + `geolocator`) | Good default on Android; same code can later run on iOS | flutter_blue_plus 2.3.15 (2026-11-05): since 2.0 a custom licence – free for personal, non-profit and educational use, paid for for-profit organisations (fine here). flutter_reactive_ble 5.6.0 (2026-09-23, Philips Hue). universal_ble 3.3.0 (also web). geolocator 14.1.2 | S1 (pub.dev API for versions; licence via search excerpt of the pub.dev licence page) |
| **Native Android (Kotlin)** | Most control over background behaviour; best if the owner already knows Kotlin | Nordic Kotlin-BLE-Library and Android-BLE-Library, BSD-3, pushed 2026-11 / 2026-10 | S1 (GitHub API) |
| React Native | No advantage here | react-native-ble-plx last pushed 2026-03; react-native-ble-manager 2026-11 | S1 |
| **Web Bluetooth page (PWA)** | Fastest route to a working prototype on Android; zero install | Chrome for Android: supported (needs Android 6+), GATT connect / read / write / notifications, `writeValueWithoutResponse` since Chrome 85. Needs HTTPS and a user gesture to pick the device. `getDevices()` (remembered devices) and `watchAdvertisements()` are still behind flags → the device must be picked again after every page load. Firefox: not supported ("Harmful") | V2 (caniuse + W3C community-group status page + Chrome docs) |
| Web Bluetooth on iOS | Only through third-party browsers | Safari: not supported on any version, WebKit lists it as not considered. Workarounds: **Bluefy** (PNN Soft, App Store, updated 2026) and a Safari web-extension polyfill listed as "iOSWebBLE" / "beacio" (free, needs iOS 26.2+). Chrome on iOS uses WKWebView and has no implementation | V2 (caniuse + status page + App Store listing) |
| Native iOS (Swift) | Needed for a proper iPhone app | Requires a Mac and Xcode; free provisioning expires after a few days, the paid programme is 99 USD/year **[UNV]** | UNV |
| No app at all for early tests | Use it first | nRF Connect (phone) can exercise every characteristic, including MTU / PHY requests | UNV |

### 5.2 Continuous GPS + BLE in the background

**Android** **[S1 official unless noted]**

- From Android 14 (API 34) "you must declare an appropriate service type for each foreground service". Needed here: `location` (permission `FOREGROUND_SERVICE_LOCATION`, runtime `ACCESS_FINE_LOCATION`) and `connectedDevice` (permission `FOREGROUND_SERVICE_CONNECTED_DEVICE`, runtime `BLUETOOTH_CONNECT` / `BLUETOOTH_SCAN`).
- "you cannot create a `location` foreground service while your app is in the background, unless you've been granted the `ACCESS_BACKGROUND_LOCATION` runtime permission." Starting the service while the app is on screen avoids the background-location permission.
- Android 15: the new 6-hour limit applies to `dataSync` and `mediaProcessing` only; no time limit was found for `location` or `connectedDevice`.
- Android 16 (API 36): no foreground-service change touching these two types was found; new Bluetooth bond-loss intents (`ACTION_KEY_MISSING`), and the local-network permission mentioned in 4.2.
- Google Play's foreground-service declaration applies only to store distribution. A sideloaded personal app is not affected **[INF]**.
- A Web Bluetooth page has no background mode: with the tab hidden or the screen off the page is not guaranteed to keep running **[UNV – not stated in the sources opened]**. Usable only with the screen on.

**iOS** **[mostly UNV – Apple's technote could not be read]**

- Background modes `bluetooth-central` and `location` keep a connected app running and receiving location updates **[UNV]**.
- Apple forum reply: no major iOS 26 differences in background Bluetooth compared with iOS 18; from iOS 26 only apps that set accessories up with AccessorySetupKit are relaunched after termination (TN3115, via search excerpt); several user reports of background scanning stopping on iPhone 17 **[S1, snippet]**. Relevant only if the app is killed; a force-quit app is never relaunched **[UNV]**.

**Practical consequence.** The owner walks along with the phone. Design the app to work with the **screen on** (wake lock) as the baseline; add the Android foreground service as an improvement so the hunt survives a pocketed phone. Do not make the hunt depend on background behaviour that was not tested on the owner's own handset.

### 5.3 GPS accuracy and the hot/cold indicator

- "GPS-enabled smartphones are typically accurate to within a 4.9 m (16 ft.) radius under open sky … their accuracy worsens near buildings, bridges, and trees" (GPS.gov) **[S1 official]**. The brief's 3–10 m urban figure is consistent with that; no urban measurement was retrieved **[UNV]**.
- Android's `Location.getAccuracy()` is "the estimated horizontal accuracy radius in meters of this location at the 68th percentile confidence level" **[S1 official]** – one fix in three lies outside it.

Design consequences **[INF]**:

1. Use distance **bands**, not a continuous rate. Steps finer than ≈ 10 m are noise.
2. The innermost "hot" band should not be smaller than ≈ 15–20 m in built-up areas. The last metres need another cue (a spoken hint, a photo, a riddle).
3. Add hysteresis (≈ 5 m, or "two consecutive fixes in the new band") so the blink rate does not flutter at a boundary.
4. Discard fixes whose reported accuracy is worse than ≈ 25 m; smooth over 3–5 fixes.
5. The phone computes the great-circle distance (haversine is exact enough below 1 km) and sends a command only when the band changes, plus a keep-alive every few seconds. The device blinks on its own timer and switches to a neutral "no signal" pattern if the keep-alive stops, so a lost link never shows a stale "hot".
6. Walk the real route once with a GPS logger before choosing hiding places; move any spot where the track scatters.

Sources: https://pub.dev/packages/flutter_blue_plus · https://pub.dev/packages/flutter_reactive_ble · https://pub.dev/packages/universal_ble · https://github.com/NordicSemiconductor/Kotlin-BLE-Library · https://caniuse.com/web-bluetooth · https://github.com/WebBluetoothCG/web-bluetooth/blob/main/implementation-status.md · https://developer.chrome.com/docs/capabilities/bluetooth · https://apps.apple.com/de/app/ioswebble/id6761301368 · https://apps.apple.com/app/id1492822055 · https://developer.android.com/develop/background-work/services/fgs/service-types · https://developer.android.com/about/versions/15/behavior-changes-15 · https://developer.android.com/about/versions/16/behavior-changes-16 · https://developer.android.com/develop/connectivity/bluetooth/ble/background · https://developer.apple.com/forums/thread/809741 (search excerpt) · https://www.gps.gov/gps-accuracy · https://developer.android.com/reference/android/location/Location

---

## 6. Q5 – PN5180 with the ESP32-S3

### 6.1 Libraries

| Library | State | ISO 15693 privacy commands | Notes | Label |
|---|---|---|---|---|
| `ATrappmann/PN5180-Library` | **Archived**, last push 2022-06-03, 23 open issues | `getRandomNumber`, `setPassword`, `unlockICODESLIX2`, `lockICODESLIX2` | Do not start from this one | S1 (GitHub API + source) |
| **`tueddy/PN5180-Library`** | v2.3.7 (2025-09-01), 1 open issue | `getRandomNumber()`, `setPassword(identifier, password, random)`, `disablePrivacyMode(password)`, `enablePrivacyMode(password)` | Custom SPI pins (`begin(sck, miso, mosi, ss)`, v2.3.2), settable SPI frequency (v2.3.6), LPCD (`prepareLPCD`, `switchToLPCD`), ISO 14443 as well | S1 (source read directly) |
| `biologist79/PN5180-Library` (ESPuino's fork of the above) | pinned by ESPuino | same | "reduced hardcoded RF-field/transceive timeouts (500/200ms -> 100ms) to fix intermittent false 'card removed' events" | S1 |
| `jef-sure/pn5180` (ESP-IDF component, MIT) | v0.8.2, uploaded within weeks of the access date | Not mentioned; a raw `pn5180_rf_transceive()` exists | ISO 14443A + ISO 15693 inventory / read / write, LPCD; ESP32-S3 example pins RST 4, SCK 6, MOSI 7, MISO 8, NSS 9, BUSY 5; IDF ≥ 5.0.4 | S1 |

The frames the tueddy library sends are exactly those note 01 derived from the NXP datasheet, Flipper and Proxmark:

```
getrandom[]   = {0x02, 0xB2, 0x04}
setPassword[] = {0x02, 0xB3, 0x04, <identifier>, pw0^rnd0, pw1^rnd1, pw2^rnd0, pw3^rnd1}
disablePrivacyMode(): getRandomNumber() then setPassword(0x04, password, random)
```

(condensed from `PN5180ISO15693.cpp`). **[V3 together with note 01]** With this API the password array is `{0x5B, 0x6E, 0xFD, 0x7F}` if note 01's byte order is right; the reversed order and `0F 0F 0F 0F` are the other candidates. Because a wrong password makes the tag ignore everything "until a Power-On Reset (RF reset)" (note 01), the firmware must switch the field off and on between candidates; it can then remember the working one.

Note 02 adds what this note did not research: forum evidence of original Tonies being read with a PN5180 on an ESP32, a second project that builds a PN5180 library for the S3 on core 3.x, and reports that some figures are found already unlocked – which is why a plain inventory is tried first (section 12.2).

### 6.2 How ESPuino does it (read from `src/RfidPn5180.cpp`)

- A dedicated task (priority 2, core 0, 3072 words of stack) steps a state machine every 10 ms: reset → set up RF → inventory → `disablePrivacyMode(password)` → inventory again. The privacy password is a setting, default `{0x0F, 0x0F, 0x0F, 0x0F}`, stored in NVS.
- It clears stale IRQ flags before each ISO 15693 inventory ("a stale RX-IRQ flag … could make the next poll immediately look like 'new data arrived' and return leftover buffer content as a phantom card").
- It avoids a hard reset on every poll while a tag is present, and runs one "silent re-init sweep" before declaring a tag removed, to tell a wedged reader from a removed tag.
- Deep-sleep wake uses LPCD: IRQ pin set active-low in the PN5180's EEPROM, `switchToLPCD(0x3FF)` (≈ 1 s period), `esp_sleep_enable_ext1_wakeup(…)`, and `gpio_hold_en()` on NSS and RST plus `gpio_deep_sleep_hold_en()`. On wake it reads the tag and goes back to sleep if the tag is unknown.
- It refuses LPCD on PN5180 firmware below 4.0: "PN5180 firmware < 4.0 has several bugs preventing the LPCD mode".
- Its wake check carries the comment "do not handle encrypted cards in any way here" – a Tonie in privacy mode would be treated as "no card". This device needs its own wake path. **[S1 for all points]**

### 6.3 ESP32-S3 and core 3.x pitfalls

| Topic | Finding | Label |
|---|---|---|
| SPI pins | Freely assignable on the S3 (GPIO matrix); the library takes them in `begin()`. Maximum SPI speed "7 Mbps", mode 0 (datasheet); the library uses 7 MHz | S1 official + source |
| Swapped data lines | An Arduino Nano ESP32 (S3) user's "library does not work" turned out to be MOSI/MISO swapped ("you have CIPO and COPI reversed") | S1 |
| BUSY line | Mandatory handshake. Datasheet procedure: wait for BUSY high, then low. The library polls it with 1 ms sleeps and a command timeout (default 500 ms, ESPuino sets 100 ms). A forum user needed 1 ms after asserting NSS before sampling BUSY on an ESP32 | S1 official + S1 snippet |
| IRQ line | Needed **only** for LPCD wake. The library reads the IRQ status register over SPI | S1 (source) |
| Logic levels | PVDD 3.3 V → 3.3 V logic, no level shifter | S1 (datasheet) |
| Supplies | VBAT 2.7–5.5 V, TVDD 2.7–5.5 V (5.0 typ). Transmitter current I_DD(TVDD) 180 mA typ, 250 mA max. Power-up: "First ramp VBAT, PVDD can immediately follow, latest 2 ms after"; "**TVDD has no other relationship to VBAT or PVDD**" → switching only the 5 V transmitter supply (note 05) is allowed by the datasheet | S1 (datasheet) |
| Power-down | Hard power-down (RESET_N low) 10 µA typ; standby 15 µA typ | S1 (datasheet) |
| Chip firmware | Datasheets list 3.4 / 3.5 for the C1 / C2 parts and 4.0 for C3; which one a cheap module carries is unknown until read from EEPROM address 0x12. An ESP32 updater project exists (last pushed 2021) | S1 + S1 |
| Supply noise | "Any additional filtering/damping of the transmitter supply, e.g. by ferrite beads, might have an impact on the analog RF signal quality" (datasheet). TVDD from a switching boost is untested | S1 + UNV |

### 6.4 Poll timing and current

From the library's own delays **[INF from source]**: hard reset 1 ms + 5 ms + wait for the idle IRQ; RF on until the field-on IRQ; each ISO 15693 command = transmit + fixed 10 ms + wait for the receive IRQ ≈ 15–25 ms. One attempt (reset, RF set-up, GET RANDOM, SET PASSWORD, INVENTORY) is therefore **≈ 80–150 ms** of field-on time. A tag already unlocked on a previous visit answers a plain INVENTORY and skips two commands (note 01: the unlock persists until a Toniebox re-locks it).

Current while the field is on: ≈ 0.35 A at the cell (note 05, from the 180 mA TVDD figure). Two attempts per second ≈ 20–30 % duty ≈ 70–110 mA average at the cell **[INF]**. During the hunt, poll only when the wake sensor says a figure is present, or when the app arms a scan.

### 6.5 LPCD (low-power card detection)

- The PN5180 sleeps, wakes on its own counter (1–2690 ms), switches the field on briefly and compares the antenna load with a reference. It raises the IRQ on "Card / **metal**" **[S1, datasheet]**.
- Average current: NXP knowledge-base example ≈ 200 µA at a 200 ms period; a user measured 220 µA at 300 ms and ≈ 35 µA at 2690 ms (with doubts about that setting) **[S1 each, snippet]**.
- The PN5180's supplies must stay up in sleep (the datasheet offers a GPO to switch an external TVDD regulator on only for the measurement) **[S1]**.
- ESPuino needs chip firmware ≥ 4.0 **[S1]**.

**Usable, but not recommended here**: 5–30× the sleep budget, a firmware-version dependency on a cheap module, the boost or TVDD must stay available in sleep (note 05, risk 15), and anything metallic that shifts near the antenna wakes the device. A hall switch on the figure's magnet costs < 1 µA (note 04).

### 6.6 Wake strategies compared

| Strategy | Sleep cost | Works without touching the device? | Risk |
|---|---|---|---|
| **Hall switch / reed on the Tonie's magnet → ext1** | ≈ 0.7 µA (hall) / 0 (reed) | yes | Field strength through the shell unmeasured; speaker magnet may bias it (note 04) |
| **Button → ext1** | 0 | no, one press | none; also the natural way to start pairing and to show battery state |
| PN5180 LPCD → ext1 | ≈ 35–220 µA + supplies | yes | see 6.5 |
| Timer wake + RFID poll | every 2 s × ≈ 0.15 s × ≈ 0.35 A ≈ **26 mA average** | yes | Not viable for standby **[INF]** |
| Vibration switch → ext1 | 0 | pick-up only | False wakes in transport |

Recommendation: hall switch **and** button, both on ext1. The button is the fallback if the magnet sensing disappoints.

Sources: https://github.com/tueddy/PN5180-Library · https://github.com/ATrappmann/PN5180-Library · https://github.com/biologist79/ESPuino/blob/master/src/RfidPn5180.cpp · https://components.espressif.com/components/jef-sure/pn5180 · https://github.com/abidxraihan/PN5180_Updater_ESP32 · PN5180 data sheet Rev. 3.0 (mirror https://static.chipdip.ru/lib/101/DOC032101818.pdf) and PN5180A0xx/C3 Rev. 3.4 (mirror https://datasheet.chipsmall.com/PN5180A0HN-C3Y/393750.pdf); NXP's own PDF returned 404/403 to the fetch tool · https://forum.arduino.cc/t/arduino-nano-esp32-not-working-with-pn5180-library/1178847 · https://community.nxp.com/t5/NFC/PN5180-low-power-card-detection-current-consumption/td-p/623185 and https://community.nxp.com/t5/NFC-Knowledge-Base/How-to-configure-PN5180-LPCD/ta-p/1753793 (search excerpts)

---

## 7. Q6 – Deep sleep and wake

### 7.1 Facts

| Item | Value | Label |
|---|---|---|
| RTC-capable GPIO on the S3 | ext0 and ext1: "ESP32-S3: 0-21"; `SOC_RTCIO_PIN_COUNT 22` | V2 (docs + header, same vendor) |
| ext0 | one pin, one level; keeps the RTC peripheral domain powered; internal pulls usable | S1 official |
| ext1 | several pins; `ESP_EXT1_WAKEUP_ANY_LOW` or `ESP_EXT1_WAKEUP_ANY_HIGH`; works with RTC peripherals powered down; ESP-IDF holds the pin's pull configuration; with more than one pin all must use the **same** level | S1 official |
| After wake | wake pads are configured as RTC IO; call `rtc_gpio_deinit()` before normal use | S1 official |
| Holding outputs in sleep | `gpio_hold_en()` alone "cannot be used to hold the state of a digital GPIO during Deep-sleep"; `gpio_deep_sleep_hold_en()` is also required. RTC pads use `rtc_gpio_hold_en()` | S1 official |
| Internal pull-up / pull-down | 45 kΩ typ | S1 (datasheet) |
| Chip deep-sleep current | 8 µA (RTC memory + RTC peripherals on), 7 µA (RTC peripherals off); light sleep 240 µA; chip off 1 µA | S1 (datasheet v2.2) |
| Module level | 8.14 µA measured on an ESP32-S3-WROOM-1 by Espressif | S1, snippet |
| Board level | XIAO ESP32-S3 14 µA; XIAO ESP32-S3 Plus 33.51 µA at 3.8 V (Seeed); a reseller table says 69 µA (note 04). DevKitC-class boards with LDO, USB bridge and LEDs: mA range | S1 each; UNV for devkits |
| Start-up time | ESP32-S3, ESP-IDF 5.2.1: **318.8 ms** unoptimised → **26.9 ms** with all optimisations (bootloader log off, image validation skipped, ROM log off, QIO 80 MHz, …) | S1 (Espressif techpedia) |
| Arduino default | `CONFIG_BOOTLOADER_SKIP_VALIDATE_IN_DEEP_SLEEP=y` is already set in the Arduino build configuration; the PSRAM test runs on every boot unless bypassed | S1 (build config + source) |
| Power-up glitches | GPIO1–17: low-level glitch ≈ 60 µs; GPIO18: low and high; GPIO19/20: also high-level | S1 (datasheet table 2-2) |

What decides the board-level figure is not the chip. The usual offenders are a high-quiescent linear regulator, a power LED, a USB-UART bridge that stays powered, an on-board addressable LED (0.6 mA quiescent, section 9) and a permanently connected battery divider. Example from Espressif's forum for a C3 devkit: 600 µA in deep sleep, 300 µA after isolating pins, the rest traced to board parts **[S1, snippet, different chip]**. A DevKitC-class board is therefore fine for the functional tests but its sleep current says nothing about the final device; measure sleep on the board that will be built in. Note 05 budgets ≈ 30–90 µA for the complete device.

### 7.2 Wake input design

- The DRV5032FB recommended in note 04 is push-pull and goes **low** with a magnet present: connect it straight to an RTC GPIO, wake on `ANY_LOW`, no pull-up.
- A reed switch (normally open, to ground) needs a pull-up. The internal 45 kΩ costs 73 µA for as long as the switch is closed; an external 1 MΩ costs 3.3 µA **[INF]**. Use the external resistor plus ≈ 100 nF against bounce.
- **Level-triggered wake trap.** Deep-sleep wake is by level, not by edge. If the figure is left on the ball, the input stays low and the chip wakes again the moment it sleeps – an endless loop that empties the cell. Reported repeatedly for door-switch projects **[S1, snippet]**. Remedy **[INF]**: before sleeping, read the sensor. If it is still active, arm the wake for the *opposite* level on that pin (ext0, "figure removed"), keep the button on ext1, and re-arm normally after that wake. The same applies to a button held down.
- The same-level rule of ext1 means hall switch, button and (if used) PN5180 IRQ must all be active-low.

### 7.3 Time from wake to sound **[INF]**

| Step | Estimate | Basis |
|---|---|---|
| ROM + bootloader + start-up to application code | 30–320 ms | Espressif figures above |
| PSRAM test (8 MB) | unknown, bypassable | source code; duration UNV |
| 5 V rail up, PN5180 reset | 10–30 ms | library delays; boost start-up UNV |
| Unlock + inventory | 80–150 ms per attempt | section 6.4 |
| Mount file system, open file, start I2S, first decoded frames | 20–150 ms | UNV |
| Amplifier turn-on | 7 ms typ | MAX98357A datasheet |
| **Total** | **≈ 0.4–1.0 s** | to be measured on the breadboard |

Under a second is acceptable for "hold the figure to the ball and it speaks".

### 7.4 Battery life in sleep, 3000 mAh cell

| Total sleep current | Ideal (3000 mAh, no self-discharge) | With 80 % usable capacity and 2 %/month self-discharge (≈ 83 µA equivalent) |
|---|---|---|
| 20 µA | 17 years | ≈ 2.7 years |
| **50 µA** | **6.8 years** | **≈ 2.1 years** |
| 100 µA | 3.4 years | ≈ 1.5 years |
| **200 µA** | **1.7 years** | **≈ 1.0 year** |
| 500 µA | 250 days | ≈ 170 days |
| **1 mA** | **125 days** | **≈ 92 days** |

Arithmetic **[INF]**. Self-discharge figure: Li-ion "self-discharges about 5 percent in the first 24 hours and then loses 1–2 percent per month", and the protection circuit adds more (Battery University) **[S1]**.

Reading:

1. Below ≈ 50–100 µA the cell's own self-discharge dominates. Chasing 20 µA instead of 50 µA buys little; avoiding a forgotten **1 mA** (a WS2812's 0.6 mA quiescent, an amplifier left in standby at 340 µA, a boost that is not truly off) buys everything.
2. "Playable years later" is true for the **data**. For the **energy**, expect one to two years per charge at best. The honest product statement is "plug it into USB-C if it has been in a drawer for a long time". The firmware should therefore start cleanly from a fully discharged and recharged cell, and show a clear low-battery signal instead of failing silently.
3. Each playback is cheap: 30 s at ≈ 150 mA is 1.25 mAh.

Sources: https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/sleep_modes.html · https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/gpio.html · ESP32-S3 datasheet v2.2 https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf · https://docs.espressif.com/projects/esp-techpedia/en/latest/esp-friends/advanced-development/performance/reduce-boot-time.html · https://github.com/espressif/esp32-arduino-lib-builder/blob/master/configs/defconfig.common · https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/ · https://batteryuniversity.com/article/bu-802b-what-does-elevated-self-discharge-do

---

## 8. Q7 – Servo and power integrity

| Item | Finding | Label |
|---|---|---|
| LEDC on the S3 | 8 channels, 4 timers, low-speed mode only, **maximum duty resolution 14 bit** (`SOC_LEDC_TIMER_BIT_WIDTH 14`). Code copied from classic-ESP32 examples with 16-bit resolution fails | S1 official (header + docs) |
| 50 Hz at 14 bit | 1 count = 1.22 µs; 1.0 / 1.5 / 2.0 ms = 819 / 1229 / 1638 counts | INF |
| Core 3.x API | `ledcSetup` and `ledcAttachPin` are removed. New: `bool ledcAttach(uint8_t pin, uint32_t freq, uint8_t resolution)`, `bool ledcAttachChannel(uint8_t pin, uint32_t freq, uint8_t resolution, uint8_t channel)`, `bool ledcWrite(uint8_t pin, uint32_t duty)`, `bool ledcDetach(uint8_t pin)` – the first argument is now the pin, not the channel | V2 (migration guide + core header) |
| ESP32Servo library | 3.2.1 (2026-05-31): "Compatible with Arduino ESP32 v3.0.0+"; on the S3 "20 PWM channels (8 LEDC + 12 MCPWM)". The issue tracker lists S3-specific reports (first attach after a detach not starting PWM; a crash with two servos from core 3.3.2) | S1 (library files); issues S1, snippet |
| Choice | For one servo, three direct LEDC calls are simpler and avoid the library's open issues | INF |
| Brown-out detector | S3 default threshold level 7 = **2.44 V**; selectable 2.44 / 2.56 / 2.67 / 2.84 / 2.98 / 3.19 / 3.30 V (ESP-IDF Kconfig; "estimates") | S1 official |

Power side (taken from note 05, not re-derived): servo on its own switched 5 V boost with true disconnect, 470–1000 µF at the servo, stall draw ≈ 1.3–1.5 A at the cell, worst-case protection trip ≈ 1.7 A, sag of 0.16–0.37 V on the battery rail. A capacitor covers the start spike, not a stall.

What the firmware must do **[INF, consistent with note 05]**:

1. Order: stop audio and RF field → enable 5 V → wait for the rail (≥ 10–20 ms) → start PWM **at the current (closed) position** → move → wait a fixed time → stop PWM → disable 5 V.
2. Never command a position at or beyond a mechanical stop; store the two end positions per unit.
3. Refuse the move below a cell voltage measured under load (note 05: ≈ 3.4 V) and tell the app why.
4. Time-limit every move; a stalled servo must lose power after a few hundred milliseconds.
5. Read `esp_reset_reason()` at boot and count brown-out resets in NVS. If the device resets during the opening move it must come back in a state that still allows a retry.
6. With PWM stopped an analogue SG90 no longer holds position **[UNV]**, so the latch has to stay released or locked mechanically without servo torque (note 06).

Sources: https://github.com/espressif/esp-idf/blob/release/v5.5/components/soc/esp32s3/include/soc/soc_caps.h · https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/ledc.html · https://docs.espressif.com/projects/arduino-esp32/en/latest/migration_guides/2.x_to_3.0.html · https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-ledc.h · https://github.com/madhephaestus/ESP32Servo · https://github.com/espressif/esp-idf/blob/v5.5.1/components/esp_hw_support/power_supply/port/esp32s3/Kconfig.power

---

## 9. Q8 – WS2812-class LED from a 3.3 V GPIO

| Item | Finding | Label |
|---|---|---|
| Driver | RMT: 4 transmit-capable channels on the S3, 48 symbols of memory each, DMA available. Core 3.x has `rgbLedWrite(pin, r, g, b)`; `neopixelWrite()` is deprecated. It sends 24 symbols at a 10 MHz tick | S1 official (header + core source) |
| With BLE / I2S | No shared resource. The flicker known from strips does not apply to a single LED (section 2.3) | INF |
| Data high level | Older WS2812B: 0.7 × VDD → 3.5 V on a 5 V supply, above a 3.3 V output. WS2812B-V5 sheets disagree between revisions: "0.63 VDD" in one copy, a fixed "2.7 V" in another | V2 for the spread (two datasheet copies read here; note 04 has more) |
| Quiescent current | "Quiescent Current: 0.6mA" in both V5 sheets | V2 (two revisions, one maker) |
| Supply range | "+3.7~+5.3" V in both sheets | V2 (as above) |

Consequences:

- **LED on the 5 V rail:** a 3.3 V data level is inside the specification only for some LED revisions, and the revision on a cheap mini-board is unknown. Standard fixes: a 74AHCT1G125 / 74HCT buffer, or a series diode in the LED's supply (≈ 4.3 V → 0.7 × VDD ≈ 3.0 V).
- **LED on the battery rail (3.0–4.2 V):** data level is always inside the specification (0.7 × 4.2 V = 2.94 V), but the supply is below the datasheet minimum for the lower part of the discharge curve; blue fades first (note 04).
- Either way the LED's supply **must be switched off in sleep**: 0.6 mA is ten to twenty times the rest of the sleep budget.

Notes 04 and 05 place the LED on different rails (section 16, item C1). From the firmware side both work; the 5 V rail with a diode or buffer is the cleaner electrical answer, and it only requires the boost to be on whenever the LED is lit, which is the case during the hunt anyway.

Sources: https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-rgb-led.c · `soc_caps.h` as above · https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/rmt.html · https://learn.watterott.com/kb/ws281x/WS2812B-v5.pdf · https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8880/WS2812B.pdf

---

## 10. Q9 – Battery monitoring

| Item | Finding | Label |
|---|---|---|
| ADC pins | ADC1 = GPIO1–10 (channels 0–9); ADC2 = GPIO11–20 | S1 official (GPIO table) |
| With radio | "ADC2 is also used by Wi-Fi." Use ADC1 | S1 official |
| Reference | "By design, the ADC reference voltage for ESP32-S3 is 1100 mV. However, the true reference voltage can range from 1000 mV to 1200 mV among different chips" → use the calibrated API (curve-fitting scheme from eFuse; `analogReadMilliVolts()` in Arduino) | S1 official |
| Ranges and error after calibration | ATTEN0 0–850 mV ± 5 mV; ATTEN1 0–1100 mV ± 6 mV; ATTEN2 (6 dB) 0–1600 mV ± 10 mV; ATTEN3 (12 dB) 0–2900 mV ± 50 mV | S1 (datasheet table 5-6) |
| Noise | "The ESP32-S3 ADC is sensitive to noise … connect a bypass capacitor (e.g., a 100 nF ceramic capacitor) to the ADC input pad", and average several samples. The datasheet's own figures are taken with 100 nF | S1 official |
| Core 3.x | `analogSetClockDiv`, `adcAttachPin`, `analogSetVRefPin` removed | S1 official |
| XIAO ESP32-S3 Plus | `ADC_BAT` = GPIO10 is only a label; users find **no divider on the board** and add their own (2 × 220 kΩ; 2 × 200 kΩ + 100 nF "instantly eliminate[d] my noise issues"; another user recommends 1 MΩ + 1 MΩ). No Seeed statement in the thread | S1 (forum, several users) |

Divider choice **[INF]**:

| Divider (top / bottom) | Ratio | Drain at 4.2 V | Pin voltage at 4.2 V | Attenuation | Error referred to the cell |
|---|---|---|---|---|---|
| 100 kΩ / 100 kΩ | 2 : 1 | 21 µA | 2.10 V | 12 dB | ± 100 mV |
| 470 kΩ / 470 kΩ | 2 : 1 | 4.5 µA | 2.10 V | 12 dB | ± 100 mV |
| 1 MΩ / 1 MΩ | 2 : 1 | 2.1 µA | 2.10 V | 12 dB | ± 100 mV |
| **2 MΩ / 1 MΩ** | 3 : 1 | **1.4 µA** | 1.40 V | **6 dB** | **± 30 mV** |

A 3 : 1 divider with 6 dB attenuation is both lower-drain and three times more accurate than the usual 2 : 1 with 12 dB. High-value dividers need the 100 nF capacitor at the pin and a slow, averaged reading. Resistor tolerance adds a fixed scale error; one calibration point against a multimeter removes it.

Measure under a known load. A resting reading overstates what the cell can deliver into a servo; the "refuse to open the lid" threshold has to be taken with the 5 V rail and a load on.

Sources: https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/adc/adc_oneshot.html · https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/adc/adc_calibration.html · ESP32-S3 datasheet v2.2 · https://forum.seeedstudio.com/t/xiao-esp32s3-plus-adc-bat-on-gpio10/291965

---

## 11. Q10 – Pin map

### 11.1 Hard rules from the firmware side

| Rule | Reason | Label |
|---|---|---|
| Wake inputs (hall / reed, button, PN5180 IRQ if LPCD) on GPIO0–21 | only RTC pads can wake from deep sleep | S1 official |
| Battery sense on GPIO1–10 | ADC1 | S1 official |
| Not GPIO0, 3, 45, 46 | strapping pins (boot mode, JTAG source, VDD_SPI, ROM log) | V2 (datasheet + Seeed) |
| Not GPIO19, 20 | USB D− / D+; reconfiguring them makes the USB device disappear | S1 official |
| Not GPIO26–32; not GPIO33–37 on octal-PSRAM parts | "GPIO26 ~ GPIO32 are usually used for SPI flash and PSRAM … on boards embedded with ESP32-S3R8 / ESP32-S3R8V chip, GPIO33 ~ GPIO37 are also not recommended". WROOM-1 datasheet: IO35–37 "not available" on R8 / R16V modules | V2 (two Espressif documents) |
| Active-high enables (5 V boost, amplifier) get an **external pull-down** and are verified with a scope through reset, flashing and sleep | pads are inputs after reset; one JTAG pad has a pull-up after reset unless an eFuse is set (datasheet note 7; which pad could not be read reliably from the extracted table – believed to be MTCK = GPIO39) | S1 + UNV |
| Nothing critical on GPIO43 | UART0 TX: the ROM prints its boot text there at every reset, including every wake | UNV (general knowledge; also assumed in note 04) |
| Everything else is free | SPI, I2S, RMT and LEDC route to any pad through the GPIO matrix | S1 official |

### 11.2 Signals

Fifteen mandatory: PN5180 SCK, MOSI, MISO, NSS, BUSY, RST · I2S BCLK, LRCLK, DOUT · amplifier SD_MODE · LED data · servo PWM · battery ADC · wake input · 5 V enable. Optional: button (second wake input), PN5180 IRQ (LPCD only).

The amplifier's SD_MODE needs a pin because note 05 keeps the amplifier on the unswitched battery rail; an amplifier left enabled without clocks draws 340 µA.

### 11.3 Proposed map

GPIO numbers are valid on any ESP32-S3-WROOM-1-class board; the pad column is for the XIAO ESP32-S3 Plus, the first-choice board of note 04.

| Signal | GPIO | XIAO Plus pad | Direction | Notes |
|---|---|---|---|---|
| Wake: hall switch / reed | **GPIO1** | D0 (edge) | in, RTC | ext1, active-low |
| Battery ADC | **GPIO2** | D1 (edge) | analogue, ADC1_CH1 | divider + 100 nF |
| *(unused)* | GPIO3 | D2 (edge) | – | strapping pin; leave open, last-resort spare |
| PN5180 BUSY | **GPIO4** | D3 (edge) | in | |
| PN5180 RST | **GPIO5** | D4 (edge) | out | external pull-down → hard power-down in sleep and reset |
| PN5180 NSS | **GPIO6** | D5 (edge) | out | |
| PN5180 SCK | **GPIO7** | D8 (edge) | out | board's default SPI pins |
| PN5180 MISO | **GPIO8** | D9 (edge) | in | |
| PN5180 MOSI | **GPIO9** | D10 (edge) | out | |
| Debug UART TX / spare | GPIO43 | D6 (edge) | – | ROM log at reset |
| Debug UART RX / spare | GPIO44 | D7 (edge) | – | |
| Button (optional) | **GPIO10** | D16 (back) | in, RTC | ext1, active-low, external 1 MΩ pull-up; the pad Seeed labels `ADC_BAT` |
| PN5180 IRQ (optional, LPCD only) | **GPIO11** | D19 (back) | in, RTC | ext1, active-low |
| 5 V boost enable | **GPIO12** | D18 (back) | out, RTC | external pull-down; RTC hold possible; only a 60 µs low glitch at power-up |
| Amplifier SD_MODE | **GPIO13** | D17 (back) | out, RTC | external pull-down |
| I2S DOUT → amplifier DIN | **GPIO38** | D11 (back) | out | the variant file names 38 / 39 / 40 `I2S_SD` / `I2S_SCK` / `I2S_WS` |
| I2S BCLK | **GPIO39** | D12 (back) | out | |
| I2S LRCLK | **GPIO40** | D13 (back) | out | |
| LED data | **GPIO41** | D14 (back) | out | RMT |
| Servo PWM | **GPIO42** | D15 (back) | out | LEDC, 50 Hz, 14 bit |

Pad-to-GPIO mapping: Seeed wiki and `variants/XIAO_ESP32S3_Plus/pins_arduino.h` agree **[V2]**. On-board LED: GPIO21 (not broken out).

Check before wiring the button: confirm with a multimeter that the `ADC_BAT` pad (GPIO10) is not connected to the battery on the delivered board (users report no divider; Seeed has not confirmed). If it is connected, swap the button to GPIO2 and take the battery reading on GPIO10.

Properties:

- Uses no strapping pin, no USB pin, no flash / PSRAM pin, and keeps UART0 free for debugging.
- The same numbers exist on an ESP32-S3-DevKitC-1, so the breadboard and the final board can run one firmware configuration. (DevKitC-1 v1.1 has its RGB LED on GPIO38 – it will flicker with I2S data; harmless.)
- Cost: **seven** mandatory joints on the 1.27 mm back pads (nine with both options). Note 04 flags those joints as a build risk.

**Variant with fewer back-pad joints:** move I2S BCLK to GPIO43 and DOUT to GPIO44 (as note 04 sketches). That frees two back pads (five mandatory). Price: no UART0 debug port, ROM boot text toggles BCLK at every reset (harmless while SD_MODE is low), and on a DevKitC-1 those two pins are wired to the USB-UART bridge, so the breadboard would need different pins.

**TinyS3 fallback:** all its pins are on 2.54 mm headers. Use GPIO21, 34, 35, 36, 37 in place of 38–42 (free there because its PSRAM is quad, not octal) and its built-in battery sense on GPIO10 (note 04).

Differences from note 04's tentative suggestion, and why: the LED is not on GPIO3 (strapping pin, excluded by the brief); the PN5180 IRQ is not on GPIO38–42 (not RTC pads, so it could never wake the chip – either drop it or use GPIO11); the two enables sit on RTC pads without reset pull-ups; a button input is included.

Sources: https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/gpio.html · ESP32-S3 datasheet v2.2 (tables 2-1, 2-2) · ESP32-S3-WROOM-1 datasheet v1.8 https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf · https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/ · https://github.com/espressif/arduino-esp32/blob/master/variants/XIAO_ESP32S3_Plus/pins_arduino.h

---

## 12. Proposed system architecture

### 12.1 BLE GATT service (sketch)

One custom service (random 128-bit UUID). All writes that change state or open the lid require an encrypted, bonded link; bonding is only possible in a pairing window opened by a long button press. Standard Device Information (0x180A) and Battery (0x180F) services alongside.

| Characteristic | Properties | Payload | Purpose |
|---|---|---|---|
| `status` | read, notify | state, battery mV and %, free bytes, slots filled, lid state, last error, firmware version | App dashboard; pushed on change |
| `command` | write (with response) | opcode + arguments | `PLAY_CLIP(id)`, `STOP`, `SET_VOLUME`, `OPEN_LID`, `LEARN_TAG(slot)`, `ASSIGN_TAG(slot, uid)`, `CLEAR_SLOT`, `ARM_SCAN(seconds)`, `ENTER_WIFI_MAINT`, `SLEEP_NOW`, `SET_TIME` |
| `led` | write without response | mode, colour, period ms, duty, brightness, time-to-live s | Proximity pattern; cheap enough to resend as keep-alive |
| `tag_event` | notify | 8-byte UID, slot or "unknown", which password worked | Registration of the four figures; "figure found" events during the hunt |
| `file_ctrl` | write (with response), notify | `BEGIN(name, size, crc32)`, `END`, `ABORT`, `DELETE`, `LIST`; notifications: `ACK(offset)`, `DONE`, `ERROR(code)` | Transfer control and resume |
| `file_data` | write without response | sequence number + up to MTU − 5 bytes | Bulk data; the device acknowledges every *n* chunks on `file_ctrl`, the app keeps a sliding window |

Link settings **[INF from section 4]**: accept MTU 517; request data length 251 on connect and before the MTU exchange (Apple §57.11); ask for the 2M PHY; request a 15–30 ms connection interval during transfers (valid for Apple's rules) and ≈ 100 ms otherwise; supervision timeout ≥ 6 s. An L2CAP channel is a later optimisation, not a prerequisite.

Registering the four figures: the app sends `LEARN_TAG(slot)`, the user holds a figure to the ball, the device unlocks and reads it and notifies the UID, the app confirms with `ASSIGN_TAG`. No UID is typed by hand.

### 12.2 State machine (prose)

**Deep sleep** is the resting state. 5 V rail off, amplifier in shutdown, PN5180 in hard power-down, LED unpowered, BLE off. Wake sources: wake sensor and button on ext1.

**Wake by figure.** Read the wake cause. Enable 5 V, reset the reader, switch the field on. Try a plain inventory; if silent, run the unlock with the remembered password, then the alternatives with a field reset between them; inventory again. Repeat for a few seconds at most.
– *Known UID:* switch the field off, play that slot's message, then wait for the figure to be removed or re-arm the wake for removal (section 7.2), and sleep.
– *Unknown or no tag:* short "not recognised" signal, sleep.
BLE is not started on this path. This is the "years later" path and has no dependency on a phone.

**Wake by button.** Show the battery state on the LED. Short press: advertise for one to two minutes. Long press: open the pairing window. No connection in time: sleep.

**Connected (hunt mode).** Stay awake. Accept commands; drive the LED from the last `led` command and fall back to a neutral pattern if its time-to-live expires. Scan for a figure only while the wake sensor is active or while the app has armed a scan; report results on `tag_event`. Clips play on command.

**Upload (sub-state).** Audio and RFID are off. Data goes to a temporary file; `END` checks length and CRC and renames. A dropped link leaves the partial file for resume.

**Lid opening.** Only on an authenticated `OPEN_LID` and with enough battery under load. Sequence as in section 8. Report success or the reason for refusal.

**Maintenance (optional).** Wi-Fi SoftAP with BLE idle: file manager and firmware update in a browser. Leaves by timeout or reboot.

**Going to sleep, always the same order.** Stop I2S; amplifier SD low; RF off; PN5180 RST low; all lines to unpowered parts low or high-impedance (no back-feeding through protection diodes); 5 V off; holds on; arm wake sources according to the sensor's present state; sleep.

**Low battery.** Below the firmware cut-off (note 05: ≈ 3.3 V resting): refuse servo and audio, blink a distinct pattern on button press, sleep.

Two failure rules **[INF]**: every wait has a timeout that ends in sleep, and a watchdog reset must land in a state that can still open the lid on the next command.

### 12.3 Storage layout (16 MB, sketch)

```
# Name,     Type, SubType,  Offset,    Size
nvs,        data, nvs,      0x9000,    0x6000     # settings, UID table, bonding keys
otadata,    data, ota,      0xF000,    0x2000
app0,       app,  ota_0,    0x20000,   0x300000   # 3 MiB
app1,       app,  ota_1,    0x320000,  0x300000   # 3 MiB
msg,        data, spiffs,   0x620000,  0x400000   # 4 MiB LittleFS: the four messages (about 7.9 min at 64 kbit/s)
media,      data, spiffs,   0xA20000,  0x5C0000   # 5.75 MiB LittleFS: hints, effects
coredump,   data, coredump, 0xFE0000,  0x10000
```

(Layout sketch, not a tested file. Arduino's own tables use the `spiffs` subtype for LittleFS partitions; a partition is selected by its label when mounting.)

- `msg`: `/1.mp3` … `/4.mp3` and a small manifest (size, CRC32, duration). Written during set-up, then left alone.
- `media`: `/hint/NN.mp3`, `/sfx/*.mp3`. Rewritten freely during development.
- NVS: UID → slot table (also copied into the `msg` manifest), working privacy password, servo end positions, volume, brown-out counter. The core's NimBLE build keeps bonds in NVS too (`CONFIG_BT_NIMBLE_NVS_PERSIST=y` in the Arduino S3 configuration) **[S1]**; the same is assumed for NimBLE-Arduino **[UNV]**.
- 8 MB variant: 2 × 2 MiB application, 1.5 MiB `msg`, 2.3 MiB `media`.

---

## 13. Q11 – Risk register

Likelihood / impact: H, M, L. "Test" refers to the plan in section 14.

| # | Risk | L | I | De-risk on the breadboard | Test |
|---|---|---|---|---|---|
| R1 | Tonie not read reliably: small coil next to the figure's magnet, shell thickness, TVDD from a switching boost, speaker / battery / servo metal detuning the antenna, class-D noise | M | H | Read all four real figures through a printed wall sample with the real boost, speaker and battery in their intended positions; log success rate per position | T1 |
| R2 | The 2026 Pokémon figures use a different chip or password than assumed | L | H | Covered by note 01's bench checklist; firmware tries both passwords in both byte orders with a field reset between | T1 |
| R3 | Wake sensor: figure magnet too weak through the shell, or the speaker magnet holds the sensor active | M | M | Sensor at the intended spot with the speaker fitted; the button is the fallback wake | T5 |
| R4 | Figure left on the ball → endless wake loop → empty cell | H if untreated | H | Opposite-level re-arm (section 7.2); leave a figure on overnight and log wake count and current | T5 |
| R5 | Real sleep current far above budget (LED quiescent 0.6 mA, amplifier standby 340 µA, boost-enable pull-up, back-feeding through data lines, board regulator, PN5180 not in power-down) | M | H | µA-range measurement of the complete assembly, then remove one consumer at a time | T5 |
| R6 | Brown-out or protection trip when the servo starts or stalls on a low cell | M | H | 50 openings at 3.4 V through the real protection board including a deliberate stall; scope on battery, 3.3 V and 5 V; reset-reason log | T6 |
| R7 | Audio drop-outs, heap exhaustion or resets with BLE + audio + RFID + LED together | M | M | 10-minute soak with everything active; watch heap low-water marks | T4 |
| R8 | BLE upload slow or fragile on the owner's phone (one packet per event; Android write-queue behaviour) | M | M | Measure on the actual phone; acknowledged, resumable protocol; Wi-Fi or USB fallback | T3 |
| R9 | PN5180 hangs or returns garbage until reset | M | M | Timeouts and a hard-reset recovery path as in ESPuino; fault injection (pull the figure mid-read 200 times) | T1, T4 |
| R10 | Messages lost: power loss during a write, later full-chip erase, corruption nobody notices | L | **H** | Separate partition, CRC, temp-file + rename, image backup; pull power during uploads 20 times | T8 |
| R11 | "Years later": cell self-discharges to the protection cut-off; device does not come back cleanly | M | M | Discharge to cut-off, recharge, confirm playback; define the low-battery signal | T8 |
| R12 | App platform surprises: iPhone (no Web Bluetooth in Safari, developer account), background limits | M | M | Decide the phone first; build the screen-on version first; test on that handset | T7 |
| R13 | GPS scatter at the actual hiding places makes "hot/cold" misleading | M | M | Log the route; bands ≥ 15–20 m; non-GPS cue for the last metres | T7 |
| R14 | Phone, app or link fails on the day and the lid cannot be opened | L | **H** | Rehearse; consider a device-only fallback (proposal for the owner, section 16) | T9 |
| R15 | Somebody else opens the lid or changes settings over BLE | L | H | Bonded, encrypted writes; pairing only after a physical long press | T3 |
| R16 | Wrong audio format: 22.05 / 24 kHz files give no or wrong sound on the MAX98357A; mono on the wrong channel | M | L | Fix the export preset (44.1 kHz mono); test one file per format | T2 |
| R17 | XIAO Plus specifics: seven to nine fine-pitch back-pad joints, no battery divider, on-board 100 mA charger next to an external one, PSRAM test delay, USB gone in deep sleep | M | M | Solder trial on a sacrificial board; keep BOOT / RESET reachable; measure wake latency | T5 |
| R18 | Tool-chain churn: core 4.0 / IDF 6, NimBLE now default in the core's BLE library, library API changes | M | L | Pin every version (ESPuino pins commit hashes); archive the build environment | – |
| R19 | Wi-Fi maintenance mode: unstable alongside BLE, Android local-network permission, transmit peaks on a sagging rail | M | L | Exclusive mode; reduced transmit power; treat as fallback only | T3 |
| R20 | LED colour or data errors: unknown LED revision on 5 V, low supply on the battery rail | L | L | Try the bought LED on the chosen rail at both ends of the battery range | T2 |

---

## 14. Breadboard validation plan

Use an ESP32-S3 DevKitC-class board (or the XIAO Plus on a carrier) with the pin numbers of section 11.3. Tools: logic analyser, oscilloscope, a current meter with µA resolution, a bench supply to stand in for the cell, a phone with nRF Connect.

| Step | What | Pass criterion |
|---|---|---|
| T1 | **RFID first, because everything depends on it.** PN5180 at 3.3 V logic and 5 V TVDD from the intended boost. Plain inventory (expect silence), unlock, inventory, UID, for all four figures. Repeat through a printed wall sample and with speaker, cell and servo placed as planned. Note the working password and byte order. Pull figures mid-read to provoke hangs | 100 % identification within 1 s at the intended position; recovery from every provoked hang without a power cycle |
| T2 | **Audio.** Play MP3 mono 44.1 kHz and one AAC file from LittleFS through the MAX98357A at 4.2 V and 3.4 V supply. Try a 22.05 kHz file deliberately. Check SD_MODE shutdown current and start-up pop. LED colours on the chosen rail | Clean speech at the target loudness; shutdown < 5 µA; format rules confirmed |
| T3 | **BLE.** GATT service exercised from nRF Connect. Log negotiated MTU, data length, PHY, interval. Upload a 500 kB file from the owner's phone model; break the link mid-transfer and resume. Bonding and the pairing window. Optional: Wi-Fi maintenance upload | ≥ 10 kB/s sustained, CRC correct, resume works; unbonded phone cannot write |
| T4 | **Concurrency soak.** Ten minutes: clip playing in a loop, BLE connected at 15–30 ms with LED updates at 5 Hz, RFID polling armed, battery ADC sampled. Then an upload while idle | No audible glitch, no reset, heap low-water mark stable |
| T5 | **Sleep and wake.** Sleep current of the full breadboard. Wake by sensor with a real figure, measure wake-to-sound. Figure left in place for an hour. Button wake. 100 wake cycles. Check the enable lines with a scope through reset, flashing, sleep and wake | < 100 µA total (target ≈ 50 µA); sound within 1.5 s; no wake loop; enables never glitch high |
| T6 | **Servo and supply.** Real cell protection board, bench supply at 4.2 / 3.7 / 3.4 V with series resistance to mimic the cell. 50 openings each, plus a forced stall. Scope battery rail, 3.3 V, 5 V | No reset, no protection trip in normal moves; a stall ends by timeout and the device stays responsive |
| T7 | **Phone app spike.** Minimal app or web page: connect, show status, send LED bands from live GPS. Walk the real route logging position and band. Check range with the ball in a hand or bag and the phone in a pocket. Lock the screen and watch what happens | Bands follow reality at every planned spot; link holds at walking distance; background behaviour known |
| T8 | **Persistence.** Final messages uploaded; cut power during uploads 20 times; verify CRCs; back up the partition image. Drain the cell to the protection cut-off, recharge, play all four | No corruption of completed files; playback after full discharge and recharge |
| T9 | **Dress rehearsal** in the printed enclosure: full hunt sequence end to end, twice, including a deliberate app crash and reconnection | Lid opens on command both times; a recovery procedure exists for each failure tried |

T1, T5 and T6 are the ones that can change the hardware. Do them before ordering quantity parts and before the enclosure is frozen.

---

## 15. What was read directly, and what was not

Read directly (files saved under `research/downloads/firmware/`): ESP-IDF documentation pages for the S3 (coexistence, sleep, GPIO, ADC, LEDC, RMT, file systems, SPI-flash concurrency, BLE low power) · ESP32-S3 datasheet v2.2 and ESP32-S3-WROOM-1 datasheet v1.8 · `soc_caps.h`, brown-out and PSRAM Kconfig files · Arduino core headers, partition tables, XIAO variant file, lib-builder build configuration · Espressif NimBLE throughput README · NimBLE-Arduino README and release notes · ESP32-audioI2S and ESP8266Audio READMEs · ESPuino `RfidPn5180.cpp`, `platformio.ini`, README, changelog, partition tables · tueddy and ATrappmann PN5180 library sources · PN5180 data sheets (two mirrored revisions) · MAX98357A datasheet (mirror) · two WS2812B-V5 datasheet copies · Apple Accessory Design Guidelines R32 Update 1 (BLE chapter excerpt kept) · Android behaviour-change and foreground-service pages · GPS.gov accuracy page · Seeed wiki.

Not readable in this run: esp32.com forum threads (bot wall) · community.nxp.com (403) · NXP's own PN5180 PDF (404 to the tool; mirrors used) · analog.com datasheet (timeout; mirror used) · Apple TN3115 (page body not returned).

---

## 16. Open items, conflicts with other notes, proposals

### A. Not verified

1. **Phone platform of the owner** – decides section 5.
2. ESP32-audioI2S (or any audio library) together with NimBLE on an S3: no documented precedent found.
3. Application image size and free heap of the real firmware: estimates only.
4. Duration of the Arduino PSRAM test on an 8 MB board, and total time from wake to application code in an Arduino build.
5. Sleep current of the XIAO ESP32-S3 Plus in this circuit (Seeed 33.5 µA, reseller 69 µA).
6. Which JTAG pad carries a pull-up after reset (datasheet note 7; table extraction was garbled).
7. PN5180 LPCD current figures and the "1 ms after NSS" report come from search excerpts of NXP's forum.
8. Real BLE throughput between NimBLE and the owner's phone; the 46–102 kB/s S3 figures are from a search excerpt of esp32.com.
9. iOS background behaviour for BLE + location on iOS 26; iOS free-provisioning limits; Opus container support on iOS.
10. Web Bluetooth behaviour with the tab hidden or the screen off.
11. MP3 encoder default sample rates at low bit rates (the exact bit rate at which encoders switch to 22.05 / 24 kHz).
12. LittleFS usable fraction (90 % assumed) and mount time on a 4–6 MiB partition.
13. SG90 holding behaviour with PWM stopped.
14. NOR-flash retention and endurance figures are distributor excerpts for Winbond parts; the flash vendor inside the chosen module is unknown.
15. TVDD from the boost converter: effect on read range.

### B. Dependencies on other notes

- Password and byte order, persistence of the unlock, "never send" command list: note 01.
- Reader module choice, its dimensions, read range, ferrite, field reports with real Tonies: note 02.
- Board choice and pad list, amplifier thresholds, wake-sensor part: note 04.
- Power tree, currents, firmware rules for the servo, protection thresholds: note 05.
- Latch mechanics that must not rely on servo holding torque: note 06.

### C. Conflicts and gaps between notes

1. **LED supply rail.** Note 04 recommends the switched battery rail (data level always valid); note 05's diagram puts the LED on the switched 5 V rail and lists the data level as an open point. Needs one decision; section 9 gives the firmware view.
2. **Note 04's tentative pin suggestion** puts LED data on GPIO3 and the PN5180 IRQ on GPIO38–42. Section 11.3 explains the changes.
3. **PN5180 IRQ.** Notes 04 and 05 carry it as a signal; it is only needed if LPCD is used, which sections 6.5 and 6.6 advise against. Dropping it saves a pin and a wire.
4. **"Switched battery rail" in note 04** has no switch in note 05's power tree (only the 5 V rail is switched). If the LED goes on the battery rail it needs its own switch and a GPIO.
5. **Two chargers.** The XIAO Plus carries a 100 mA charger and note 05 adds a TP4056 board. How the cell, the two chargers and the two USB-C sockets relate is not decided anywhere; it also decides which socket is usable for firmware updates.
6. **Password notation.** Note 01 gives the Tonie privacy password as `0x5B6EFD7F`, on air `5B 6E FD 7F` (Flipper). Note 02 cites the reverse-engineered box firmware with `0x7FFD6E5B`. These may be the same four bytes written in two conventions; neither note proves the on-air order on a 2026 figure. The firmware should try both orders (with a field reset between attempts) and store the one that works.

### D. Proposals for the owner (not part of the brief)

1. **A way to open the lid without the phone**, for the day the app or the link fails: for example all four figures presented in order, or a long button sequence. It costs little firmware and removes the single point of failure in R14.
2. **Prepare the audio on a PC and let the app upload files** instead of recording and encoding inside the app. It removes codec work from the app and fixes the format.
3. **Keep a Wi-Fi maintenance mode** even if the app never uses it: it is the only repair path once the ball is closed and the USB socket of the MCU board is out of reach.
4. **Treat "playable years later" as two statements**: the recordings persist; the battery needs charging after long storage. The low-battery behaviour then becomes a designed feature rather than a failure.
