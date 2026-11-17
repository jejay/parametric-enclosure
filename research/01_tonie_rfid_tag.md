# Tonie Figurine RFID Tag — Research (tag / figurine side)

**Project:** PokeTonieEngagementHunt — 3D-printed Pokéball device that must identify four Pokémon Tonies (Pikachu, Bisasam/Bulbasaur, Glumanda/Charmander, Schiggy/Squirtle) by RFID.
**Scope of this file:** the *tag / figurine* side only (reader modules are covered separately).
**Access date of all web sources:** 2026-11-17.
**Confidence legend:** VERIFIED = ≥2 independent sources agree · HIGH = strong single-origin primary source + corroboration · MED = indirect / inferred / community-derived · LOW = weak or no direct source, inference only.

---

## Summary table

| Fact | Value | Confidence | Key sources |
|---|---|---|---|
| Chip | NXP ICODE **SLIX-L** (ordering codes **SL2S5002** 23.5 pF / **SL2S5102** 97 pF) | VERIFIED | tonies-wiki, teardown, wakdev, Flipper+Proxmark SLIX-L code |
| Protocol / freq | **ISO/IEC 15693** (vicinity), **13.56 MHz** | VERIFIED | wakdev, tonies-wiki, teardown |
| UID | **8 bytes / 16 hex**, factory-unique, prefix **E0 04 03** | VERIFIED | tonies-wiki, teddycloud issue #378 (`E0040350178864AE`), NXP |
| Tag memory | 64-byte EEPROM, 16×4-byte blocks, blocks 0–7 (32 B) user-readable; identity is the UID, not block data | HIGH | wakdev (SLIX-L), NXP datasheet family |
| Privacy mode | Tonies are shipped/kept in SLIX-L **privacy mode**; silent to INVENTORY until unlocked. Box re-enables privacy after each read | VERIFIED | tonies-wiki custom-tags + ofw-patches |
| Unlock commands | **GET RANDOM NUMBER = 0xB2**, then **SET PASSWORD = 0xB3**, IC mfg = **0x04** (NXP), password identifier = **0x04** (Privacy), sent **unaddressed** | VERIFIED | NXP SLIX2 datasheet + Flipper + Proxmark (3 independent) |
| Boxine privacy password | uint32 **0x5B6EFD7F** → on-air pre-XOR bytes **5B 6E FD 7F**; fallback **0x0F0F0F0F** (NXP default) | HIGH | Flipper source (primary); tonies-wiki + NXP corroborate 0F0F0F0F |
| "0x7FFD6E5B" (your recollection) | Same four bytes **reversed** (little-endian reading). Canonical/on-air form is **5B 6E FD 7F** = 0x5B6EFD7F | VERIFIED | Flipper `slix_unlock.c` + Proxmark `-p` parsing |
| Wrong-password penalty | **None persistent.** Invalid pw → tag ignores commands only "until a Power-On Reset (RF reset)". No retry counter, no lockout, no brick | VERIFIED (SLIX2 datasheet; SLIX-L shares mechanism) | NXP SL2S2602 §9.5.3.2 |
| Auto re-lock on field removal? | **No.** SET PASSWORD takes the tag *out of* privacy persistently; it stays unlocked until a Toniebox (or an explicit ENABLE PRIVACY 0xBA) re-locks it | MED-HIGH | NXP datasheet §9.5.3.9 + tonies-wiki ("box puts every tag into privacy after reading") |
| Damage risk of GET RANDOM + SET PASSWORD + INVENTORY | **None** (no EEPROM/user writes, no counters touched, fully reversible) | HIGH | NXP datasheet, Flipper/Proxmark code |
| UID enough to tell 4 figures apart? | **Yes** — 64-bit UID is factory-unique per physical figurine | VERIFIED | NXP; ChameleonMini #265 ("UID is sufficient") |
| Magnet in figure base | Yes — magnet in the figure's socket **and** in the Toniebox top | VERIFIED | iFixit teardown |
| Magnet size (replica bench value) | ~**10 mm Ø × up to ~5.5 mm**, centre of base; tag inlay ≤ ~39 mm Ø, coil near bottom face | MED (DIY-derived) | MakerWorld custom-base specs, forum.revvox |
| Figure height / base | ~**10 cm** tall; flat magnetic foot; packaging boxes ~110×200×35–49 mm | LOW-MED | retailer listings (noisy; packaging not figure) |
| Four Pokémon Tonies on sale? | **Yes**, launched ~**20 Aug 2026**, **€16.99** each; yellow **Toniebox 2** starter w/ Pikachu | VERIFIED | mydealz, giga.de, familie.de |
| Article numbers | Pikachu **10001692 / 11001692** · Bisasam **11003815** · Schiggy **11003819** · Glumanda *(unconfirmed)* | MED | Heise Preisvergleich, Currys |
| New chip for 2024–26 / Toniebox 2? | No reported change; Toniebox 2 is backward-compatible with all prior Tonies. **Not directly verified on a 2026 Pokémon figure** | MED | tonies PR / heise (backward compat); no RE source reports a change |
| Read distance | No Tonie-specific figure found. ISO15693 vicinity ~up to 20 cm with a large tuned antenna (PN5180); small SLIX-L antenna → expect short range (~mm–few cm). Flipper: some tags need ≤1 cm | LOW | NXP PN5180 community, Flipper docs |
| Non-privacy Tonies? | Box-activated Tonies are all in privacy. A brand-new/unactivated tag may still be at factory default; Creative Tonies behave like content Tonies once boxed | MED | tonies-wiki, inference |

---

## Q1 — Chip, protocol, UID, memory

**Chip = NXP ICODE SLIX-L**, ISO/IEC 15693, 13.56 MHz. Verified across independent sources:

- Community wiki (teddycloud / revvox), [tonies-wiki custom-tags](https://tonies-wiki.revvox.de/docs/tools/teddycloud/usage/custom-tags/): required tag "Type: SLIX-L", "UID starts with: E0 04 03", 16-hex UID, Privacy-Mode.
- iFixit-based teardown mirror describes the figure chip as ISO 15693, "probably an ICODE SLIX-L".
- The Flipper Zero and Proxmark3 code both implement the Tonie unlock specifically under their **SLIX** (ISO15693) stacks (see Q2).
- Blank replacement tags are sold as "SLIX-L RFID-Tags, NXP Chip, kompatibel mit modifizierten Tonie Boxen" ([ebay.de 227024883343](https://www.ebay.de/itm/227024883343)).

**Ordering codes (SLIX-L):** **SL2S5002** (23.5 pF) and **SL2S5102** (97 pF, for small labels) — per [wakdev SLIX-L](https://www.wakdev.com/en/knowledge-base/nfc-chips/nxp-icode-slix-l.html). (Note: SLIX2 is the different part SL2S2602; SLIX is SL2S2002/2102. The "(SL2S5002)" in the brief is correct for SLIX-L.)

**UID:** 8 bytes (64-bit), factory-programmed and unique. Prefix **E0 04 03** = ISO/IEC 7816-6 RFID tag (E0) · NXP manufacturer (04) · ICODE product (03). Real example from teddycloud issue #378: `E0040350178864AE` ([github issue #378](https://github.com/toniebox-reverse-engineering/teddycloud/issues/378)). The stock Toniebox firmware checks this prefix — tonies-wiki: *"Usally the toniebox checks if the UID of the tag starts with E0:04:03."*

**Memory (SLIX-L, per wakdev + NXP family):** 64-byte EEPROM (512 bit) = 16 blocks × 4 bytes; only blocks 0–7 (32 bytes) are addressable with Read/Write. SLIX-L has **no** memory read/write password (unlike SLIX-S). For Tonies the meaningful identifier is the **UID**; the figure→content mapping lives in the box/cloud, not in the tag's user memory.

---

## Q2 — Privacy mode and the exact unlock sequence

### Is privacy mode used, and by whom?
Yes. tonies-wiki custom-tags: *"Once you place a new tag on the Toniebox, it will automatically activate privacy mode on this tag, making it unrecognizable by other NFC readers."* and *"Privacy mode must be deactivated beforehand."* The box both **sets** privacy (after reading) and **clears** it (to read), using passwords. tonies-wiki ofw-patches: *"Usally the toniebox puts every tag into privacy mode after reading it."* and *"doesn't allow tags without the boxine specific or the NXP specific privacy mode password 0f0f0f0f."* This applies to figures across the range (the behaviour is a tag property, not per-character).

### The unlock sequence — VERIFIED against 3 independent primary sources

**(a) NXP datasheet (SL2S2602 ICODE SLIX2, Rev 4.2, 2021 — same privacy engine as SLIX-L).** Local copy: `research/downloads/tonie_tag/nxp/SL2S2602_SLIX2.txt`. Source mirror: [docs.ampnuts.ru SL2S2602.pdf](https://docs.ampnuts.ru/nxp.com.datasheet/SL2S2602.pdf).
- GET RANDOM NUMBER `0xB2`, SET PASSWORD `0xB3`.
- §9.5.3.2: *"XOR_Password[31:0] = Password[31:0] XOR {Random_Number[15:0], Random_Number[15:0]}."* (password is XORed with the 16-bit random repeated twice).
- §9.5.3.2: *"The SET PASSWORD command can only be executed in Addressed or Selected mode except for the Privacy password"* → **privacy SET PASSWORD is sent unaddressed** (no UID needed).
- Password identifier table (one-hot): 01h Read · 02h Write · **04h Privacy** · 08h Destroy · 10h EAS/AFI.
- Delivery state: *"All password bytes are 0Fh for the Privacy and Destroy passwords"* and *"Password protected Privacy Mode is disabled"* → factory/default privacy password is **0F0F0F0F**.

**(b) Flipper Zero firmware** (`flipperdevices/flipperzero-firmware`, dev). Local copies under `research/downloads/tonie_tag/flipper/`.
- [`lib/nfc/protocols/slix/slix_i.h`](https://github.com/flipperdevices/flipperzero-firmware/blob/dev/lib/nfc/protocols/slix/slix_i.h): `SLIX_CMD_GET_RANDOM_NUMBER (0xB2U)`, `SLIX_CMD_SET_PASSWORD (0xB3U)`, `SLIX_NXP_MANUFACTURER_CODE (0x04U)`.
- [`applications/main/nfc/helpers/slix_unlock.c`](https://github.com/flipperdevices/flipperzero-firmware/blob/dev/applications/main/nfc/helpers/slix_unlock.c): the "TonieBox" method's password list — `static const SlixPassword tonie_box_pass_arr[] = {0x5B6EFD7F, 0x0F0F0F0F};`
- [`lib/nfc/protocols/slix/slix_poller_i.c`](https://github.com/flipperdevices/flipperzero-firmware/blob/dev/lib/nfc/protocols/slix/slix_poller_i.c), `slix_poller_set_password()`: builds the privacy request `skip_uid = (type == SlixPasswordTypePrivacy)` (unaddressed), `password_type = (0x01 << type)` → **0x04** for Privacy, then `double_rand_num = (rn_h<<24)|(rn_l<<16)|(rn_h<<8)|rn_l`, `xored_password = double_rand_num ^ password`, sent big-endian. GET RANDOM is also `skip_uid = true`.

**(c) Proxmark3 firmware** (`RfidResearchGroup/proxmark3`, master). Local copies under `research/downloads/tonie_tag/proxmark/`.
- [`include/protocols.h`](https://github.com/RfidResearchGroup/proxmark3/blob/master/include/protocols.h): `ISO15693_GET_RANDOM_NUMBER 0xB2`, `ISO15693_SET_PASSWORD 0xB3`, `ISO15693_WRITE_PASSWORD 0xB4`, `ISO15693_LOCK_PASSWORD 0xB5`, `ISO15693_DESTROY 0xB9`, `ISO15693_ENABLE_PRIVACY 0xBA`.
- [`armsrc/iso15693.c`](https://github.com/RfidResearchGroup/proxmark3/blob/master/armsrc/iso15693.c) `disable_privacy_15693_Slix()` sends GET RANDOM then `c[] = { ISO15_REQ_DATARATE_HIGH, ISO15693_SET_PASSWORD, 0x04, pass_id, …4 pw bytes… }` (flags = datarate-high only → **unaddressed**), with `init_password_15693_Slix()`:
  `buffer[0]^=rnd[0]; buffer[1]^=rnd[1]; buffer[2]^=rnd[0]; buffer[3]^=rnd[1];` (identical doubling to Flipper).
- [`client/src/cmdhf15.c`](https://github.com/RfidResearchGroup/proxmark3/blob/master/client/src/cmdhf15.c): CLI `hf 15 slixprivacydisable -p <4 hex bytes>` (example in help: `-p 0F0F0F0F`). `-p` bytes are taken in written order into `pwd[0..3]`. **Proxmark does not hard-code the Tonie secret — you supply it.**

### The exact on-air unlock (what the reader must transmit)

1. **GET RANDOM NUMBER** (unaddressed):
   `02 B2 04` + CRC16 → tag replies 2 random bytes `RN0 RN1`.
2. **SET PASSWORD** (privacy, unaddressed):
   `02 B3 04 04  P0 P1 P2 P3` + CRC16, where the pre-XOR password bytes are **5B 6E FD 7F** and
   `P0 = 5B^RN0, P1 = 6E^RN1, P2 = FD^RN0, P3 = 7F^RN1`.
   Flags `0x02` = high datarate, 1-subcarrier, **no address bit**; `04` = NXP mfg code; `04` = Privacy identifier.
3. If that password is rejected, repeat 1–2 with **0F0F0F0F** (`P = 0F 0F 0F 0F` before XOR).
4. **INVENTORY** (standard ISO15693) → tag now answers and returns its UID.

**Password byte-order, stated per source (important):**
- Flipper source: `0x5B6EFD7F` (a `uint32`, big-endian bytes **5B 6E FD 7F**) and `0x0F0F0F0F`.
- Proxmark CLI form for the same secret: `hf 15 slixprivacydisable -p 5B6EFD7F`.
- On the air (before the random XOR): **5B 6E FD 7F**.
- Your recalled "**0x7FFD6E5B**" is the *reversed* reading of these same four bytes (7F FD 6E 5B). It is the correct byte *set* but written little-endian; the canonical/transmitted order is **5B 6E FD 7F = 0x5B6EFD7F**. Use that.

The specific secret `0x5B6EFD7F` ("boxine specific" privacy password) is single-origin (Flipper firmware, the widely-used reference), but corroborated structurally: the box checks two passwords (boxine + NXP `0f0f0f0f`, per tonies-wiki) and Flipper tries exactly those two in that order.

---

## Q3 — Persistence, reversibility and damage risk

**Does the tag auto-return to privacy when the field is removed?**
No. Privacy is a stored (non-volatile) state. ENABLE PRIVACY (`0xBA`) sets it; SET PASSWORD (`0xB3`, privacy) takes it out of privacy. NXP SL2S2602 §9.5.3.9: *"To get out of the Privacy status, the valid Privacy password has to be transmitted to the IC with the SET PASSWORD command."* The Toniebox only needs to *"put every tag into privacy mode after reading it"* (tonies-wiki) **because** the unlock is persistent — it would be unnecessary if the tag auto-re-locked. (Contrast: Persistent-Quiet is explicitly reset at power-off in the datasheet; privacy carries no such caveat.)

**Consequence for this project:** after your reader does GET RANDOM + SET PASSWORD + INVENTORY, the Tonie is left **unlocked** (readable by any ISO15693 reader / phone) until it is placed back on a real Toniebox, or until your firmware explicitly re-locks it with ENABLE PRIVACY (`0xBA`) + the same password. This is harmless (no data changes), but worth a design decision: optionally re-lock after identifying, to keep the figures "normal" for a Toniebox owner. Confidence MED-HIGH (datasheet + inference; worth a bench check).

**Damage / brick risk of the identify sequence:** **None.** GET RANDOM + SET PASSWORD(privacy) + INVENTORY perform no EEPROM user writes and touch no counters; fully reversible.

**Wrong-password behaviour (no penalty counter):** NXP SL2S2602 §9.5.3.2: *"If the IC receives an invalid password, it will not execute any following command until a Power-On Reset (POR) (RF reset) is executed."* So a wrong guess just means: drop the RF field, re-power, try again. There is **no decrementing retry counter and no permanent lockout** on SLIX-L/SLIX2 privacy auth.

**Commands to NEVER send to a Tonie you want to keep:**
- `0xB4` **WRITE PASSWORD** — overwrites a password (could lock you out and break Toniebox compatibility).
- `0xB5` **LOCK PASSWORD** / 64-bit password protection — permanently locks a password.
- `0xB9` **DESTROY** — *permanent, irreversible* kill. NXP SL2S2602: *"That status is irreversible and the label will never respond … again."* (DESTROY needs GET RANDOM + the correct *destroy* password, so it cannot fire by accident, but never implement it.)
- `0xBA` **ENABLE PRIVACY** — only use deliberately, with the correct password, if you intend to re-lock; a wrong password just errors (needs RF reset), it does not damage the tag.
- Any WRITE SINGLE/MULTIPLE BLOCK, SET/LOCK EAS, LOCK BLOCK — unnecessary and risky; do not write to Tonies.

---

## Q4 — Is the UID enough to tell the four figures apart?
Yes. The SLIX-L UID is a factory-programmed, globally unique 64-bit value — unique per physical figurine, so the four Pokémon figures have four distinct UIDs. ChameleonMini discussion ([emsec/ChameleonMini #265](https://github.com/emsec/ChameleonMini/issues/265)): *"The UID is sufficient."* After the privacy unlock, a plain **INVENTORY** returns the UID; you simply whitelist the four UIDs. (You must read each of your four physical figures once to capture its UID — two "Pikachu" figures would have different UIDs.)

---

## Q5 — Physical facts about a Tonie figurine (for CAD)

> **Superseded:** `09_tonie_figure_dimensions.md` found that the values below describe replica bases. Genuine Tonies carry an upright ferrite-rod tag 20 to 50 mm above the underside and magnets of 6 x 6 mm, and the four Pokémon Tonies stand on a black foot of 45 mm. Use note 09.

- **Chip/coil location:** inside the figure's **base/foot**. The antenna is a small copper coil; keep the chip near the bottom face for best coupling (iFixit Q&A advice). Teardown: *"an NFC chip in his stomach"* for one figure, but for most figures the inlay sits in the magnetic foot. Confidence HIGH (qualitative), MED on exact depth — **measure your figures**.
- **Magnets:** iFixit Toniebox teardown — *"Magnets in the top of the Toniebox, and in the sockets of the Tonies."* So there is a magnet in the figure base **and** in the box; the figure is held by magnetic attraction over the box's read antenna. ([iFixit teardown 106148](https://www.ifixit.com/Teardown/Toniebox+Teardown/106148))
- **Magnet size/position (bench/replica values, MED):** replica "custom Tonie base" designs are built for a **circular magnet ≤ 10 mm Ø (≤ ~5.5 mm tall), centred**, and an NFC tag **≤ ~39 mm Ø** ([MakerWorld 200466](https://www.makerworld.com/en/models/200466) and similar). A forum test noted a 10×3 mm magnet ~1 cm above a chip blocked reads, while a centred magnet with a ~30 mm round coil still reads — i.e. a centre magnet is fine if the coil is annular around it. Replica tags commonly ~30 mm round.
- **Figure size:** standard Tonie figures are roughly **~10 cm** tall with a flat magnetic foot; the Pokémon figures are small characters. Retailer "dimensions" (e.g. 110×200×35–49 mm) are **packaging**, not the figure — treat as unreliable. Weight per figure ~20–70 g (packaging-listed). Confidence LOW-MED — **measure your actual figures** for the CAD cavity.
- **CAD takeaway:** design the Pokéball's read zone for a flat-footed figure whose coil + ~10 mm centre magnet sit in a ≤ ~40 mm base; present the reader antenna to the figure's bottom face with only thin (a few mm) plastic between.

---

## Q6 — The four Pokémon Tonies (existence, release, numbers, chip change)

- **They exist and are on sale.** Pikachu, Bisasam, Glumanda, Schiggy announced as the launch set; market start ~**20 Aug 2026**, **€16.99** each ([mydealz deal 2843972](https://www.mydealz.de/deals/pokemon-tonies-4er-bundle-pikachu-bisasam-glumanda-und-schiggy-pokemon-tonie-2843972), [giga.de](https://www.giga.de/games/pokemon-fuer-die-ohren-tonies-bringt-pikachu-co-als-exklusive-hoerfiguren--01KZV12M6K4Q4HJ34K1XQS9VYG), [familie.de](https://www.familie.de/testberichte/sommer-2026-wird-gelb-pikachu-bisasam-glumanda-und-schiggy-erobern-die-toniebox--01KGSKWVNYWY5BT19MQA7P7YNT)). A special-edition **yellow Toniebox 2** ships with a Pikachu Tonie.
- **Article numbers (MED):** Pikachu **10001692** (Boxine **11001692**; Currys code 547450) · Bisasam **11003815** · Schiggy **11003819** ([Heise Preisvergleich Pikachu](https://preisvergleich.heise.de/tonies-pok-mon-pikachu-10001692-a3908207.html), [Bisasam](https://preisvergleich.heise.de/tonies-pok-mon-bisasam-11003815-a3908200.html), [Schiggy](https://preisvergleich.heise.de/tonies-pok-mon-schiggy-11003819-a3908195.html)). **Glumanda number not confirmed** — check tonies.de.
- **Chip change for 2024–2026 / Toniebox 2?** No evidence of a tag-technology change. tonies states Toniebox 2 (launched Sep 2025) works with **all previously released Tonies**, and gen-1 boxes keep working ([heise](https://heise.de/-10623162) / tonies PR). New figures are still described simply as "NFC chip" figures. **No reverse-engineering source reports SLIX2/ICODE 3/NTAG 5 on current figures, but I could not directly verify the chip on a 2026 Pokémon figure** — the backward-compatibility requirement strongly implies the figures still present as ISO15693/SLIX-L in privacy mode (a Toniebox reads ISO15693 only). Confidence MED. **Bench-verify on an actual Pokémon figure before freezing the reader design** (see checklist).

---

## Q7 — Read distance

No Tonie-specific, through-plastic figure was found; treat this as the **least-verified** area.
- ISO15693 is a "vicinity" protocol; with a large, well-tuned antenna (e.g. PN5180 reference) reads of ~**20 cm** are typical for full-size tags ([playfultech PN5180](https://www.arduinolibraries.info/libraries/pn5180)); a mistuned antenna collapses to ~1 cm ([NXP community](https://community.nxp.com/t5/NFC/Assistance-in-Improving-ICODE-SLIX-Tag-Detection-Range-from-1-cm/td-p/2076050)).
- The Tonie's SLIX-L inlay is a **small** coil, and sits next to a magnet, so expect a **modest** practical range (order of millimetres to a few centimetres) through a few mm of plastic. Flipper docs note some cards need ≤ 1 cm.
- Practical design rule: put the figure's base essentially **on** the antenna; do not rely on cm-scale standoff. Verify with your actual reader + figures.

---

## Q8 — Alternatives to the unlock; are any Tonies not in privacy?

- **Without unlocking:** the only passive way to learn a boxed Tonie's UID is to **sniff** the reader↔tag traffic while a genuine Toniebox reads it (the box uses addressed mode, so the UID appears on air) — ChameleonMini #265: *"You can obtain the UID by sniffing the reader to tag communication."* That needs a sniffer and a Toniebox, so it is not practical for your device. For a standalone reader there is effectively **no alternative** to performing the privacy unlock (GET RANDOM + SET PASSWORD) before INVENTORY. Confidence HIGH.
- **Tonies not in privacy mode:** every box-activated figure is kept in privacy. A **brand-new/unactivated** tag may still be at the factory default (`0F0F0F0F`) and not yet in privacy — which is exactly why the reader should try the boxine password **and** `0F0F0F0F`. Creative Tonies behave like content Tonies once used with a box. (Community tooling: [nortakales/flipper-zero-tonies](https://github.com/nortakales/flipper-zero-tonies).) Confidence MED.

---

## Risks / open questions

1. **Exact secret `0x5B6EFD7F` is single-origin (Flipper).** Structurally corroborated (box checks boxine + `0F0F0F0F`), but confirm on a real Pokémon figure. Mitigation: try `0x5B6EFD7F` then `0x0F0F0F0F`.
2. **Byte-order confusion** between `0x5B6EFD7F` (on-air 5B 6E FD 7F) and the reversed `0x7FFD6E5B`. Standardise on **5B 6E FD 7F** and test both orderings on the bench if unsure.
3. **Chip identity on 2026 figures not directly verified.** Backward-compat implies SLIX-L/ISO15693, but a bench scan of an actual Pokémon figure is required before design freeze. If a figure ever came back as SLIX2 (SL2S2602) the *same* command set and identifiers (0xB2/0xB3, id 0x04) still apply — only confirm the password.
4. **Persistent unlock side-effect:** figures are left readable by phones after your reader touches them until re-locked by a Toniebox or ENABLE PRIVACY. Decide whether to auto re-lock.
5. **Read distance is unquantified for Tonies.** Must be measured with the chosen reader module and antenna, through the real Pokéball wall thickness, with the base magnet present.
6. **Physical dimensions (base Ø, coil depth, magnet) are community-derived, not official.** Measure the four actual figures.
7. **Glumanda article number unconfirmed.**
8. Do not auto-retry wrong passwords without an **RF reset** between attempts (tag ignores commands until POR).

---

## What to test on the bench first (checklist)

1. **Identify the chip:** scan each of the four Pokémon figures with a phone NFC app / Proxmark `hf 15 info` / `hf search`. Expect: no plain INVENTORY response (privacy), UID prefix `E0 04 03` once unlocked, type SLIX-L.
2. **Unlock with the boxine password:** Proxmark `hf 15 slixprivacydisable -p 5B6EFD7F`; if "not accepted", try `-p 0F0F0F0F` and the reversed `-p 7FFD6E5B`. Record which one works for *these* 2026 figures.
3. **Confirm the sequence on your own reader stack:** GET RANDOM (`02 B2 04`+CRC) → SET PASSWORD (`02 B3 04 04` + XORed pw) → INVENTORY. Log the returned UID.
4. **Capture the four UIDs** and hard-code them as the whitelist (one per physical figure).
5. **Verify re-lock behaviour:** after unlocking with the reader, re-scan with a phone to confirm the tag is now readable (persistent unlock), then confirm a genuine Toniebox re-locks it; optionally implement ENABLE PRIVACY (`0xBA`) re-lock and verify.
6. **Confirm no penalty:** send a deliberately wrong password, then cycle the RF field and show a correct unlock still works (no lockout).
7. **Measure read distance / orientation** through the intended Pokéball wall thickness, with the figure's base magnet in place; find the worst-case gap and antenna position.
8. **Measure the figures:** base diameter, foot thickness, coil depth from bottom face, magnet diameter/thickness/position — feed into the CAD cradle.
9. **Never** send WRITE PASSWORD / LOCK PASSWORD / DESTROY / block writes during any of this.

---

### Local evidence saved (untrusted; do not execute)
- `research/downloads/tonie_tag/flipper/` — Flipper SLIX source (`slix_unlock.c`, `slix_poller_i.c`, `slix_i.h`, etc.).
- `research/downloads/tonie_tag/proxmark/` — Proxmark `cmdhf15.c`, `armsrc/iso15693.c`, `include/protocols.h`.
- `research/downloads/tonie_tag/nxp/SL2S2602_SLIX2.pdf` + `.txt` — NXP ICODE SLIX2 datasheet Rev 4.2 (privacy engine shared with SLIX-L).
