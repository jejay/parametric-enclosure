# 06 — Mechanics, printing, ring: research for CAD

Access date for all web sources: **2026-11-17**. Prices are list prices seen on that date.

Evidence tags used throughout:

| Tag | Meaning |
| --- | --- |
| **[V2+]** | Confirmed by two or more independent sources (or one source plus an independent calculation that reproduces it) |
| **[S1]** | Single source, read directly |
| **[SNIP]** | Only seen as a search-result snippet or summary; page itself could not be opened (403/402/timeout) |
| **[INF]** | My inference or calculation from sourced inputs — check before committing to CAD |
| **[MEM]** | From memory of a standard or textbook, **not** verified this session |

Raw data kept in `research/downloads/mechanics/` (untrusted, data only):

- `gutekunst_torsion/torsion_list_sorted_by_d.csv` — 564 stock torsion springs, wire 0.4–1.4 mm, scraped from the federnshop.com listing
- `gutekunst_torsion/detail_candidates.txt`, `detail_candidates_2.txt` — full detail-page data for 12 candidates
- `gutekunst_torsion/datenblatt_t-18436l.pdf`, `datenblatt_t-16244l.pdf` — manufacturer datasheets (drawing defines the leg-angle convention)
- `gutekunst_compression/*.csv` — two filtered compression-spring searches
- `papers/dogan_2022_short-term_creep_AM_polymers_svjme.pdf` — peer-reviewed creep study

---

## 1. Ring

### 1.1 Size 49

| Quantity | Value | Status | Source |
| --- | --- | --- | --- |
| Definition | ISO 8653:2016 ring size = inner circumference in mm | [V2+] | https://en.wikipedia.org/wiki/Ring_size , https://www.baur.de/magazin/ringgroessentabellen |
| Inner circumference | 49 mm | [V2+] | same |
| Inner diameter | 49 / π = 15.597 mm → **15.6 mm** | [V2+] | Wikipedia ISO table (49 → 15.6), Baur table (49 → 15,6), arithmetic |
| Neighbours | 48 → 15.3 mm, 50 → 15.9 mm | [V2+] | same two tables |
| UK / FR equivalents | UK J, FR 9 | [S1] | Baur |
| US equivalent | ≈ 4.9 (from C = 2.55·s + 36.5) | [INF] | formula on Wikipedia |

**Disagreement:** a Swarovski size guide reportedly pairs 15.3 mm with size 49 and 15.6 mm with size 50 [SNIP] (https://asset.swarovski.com/files/SWA_SIZE-GUIDE_RINGS_DE/SWA_SIZE-GUIDE_RINGS_DE.pdf). 15.3 mm × π = 48.1 mm, so that table is shifted by one size relative to ISO 8653; not used.

Size steps are 1 mm of circumference = 0.32 mm of diameter, so a CAD value of 15.6 mm is good to about ±0.15 mm of what "49" can mean.

### 1.2 "Diameter 2.5 mm"

Interpreted as the **band (shank) width, 2.5 mm**. This is at the wide end of the normal solitaire range below, so it is plausible, but it is an interpretation — the alternatives (wire thickness of a round-section band, or a 2.5 mm stone) change the slot. **Measure the real ring with calipers before finalising the slot.** Needed measurements: band width at the bottom, band radial thickness at the bottom, overall height bottom-of-band to top-of-stone, head width across the prongs.

### 1.3 Typical solitaire geometry

| Dimension | Typical range | Status | Source |
| --- | --- | --- | --- |
| Shank width | 1.8–2.0 mm "sturdy" norm; thin styles 1.2–1.65 mm; heavier settings to 3.0 mm | [V2+] | https://www.briangavindiamonds.com/news/buyers-guide-thin-band-engagement-ring/ , https://ritani.com/blogs/news/how-thick-or-thin-should-my-engagement-ring-be , https://www.baunatjewellery.cn/en/thin-engagement-ring |
| Shank (radial) thickness | 1.2–2.0 mm; one classic 6-prong lists 2.0–2.6 mm (retailer wording does not always separate width from thickness) | [S1] each | Baunat, https://www.jewlr.com/products/JLUX32-O3/classic-6-prong-solitaire-diamond-engagement-ring |
| Setting height above finger (inner bore top → stone table) | low profile 5.5–6.5 mm; high/cathedral 7.5–8+ mm | [SNIP] | Frank Darling listings (5.5 mm, 6.1 mm), PriceScope thread (8 mm, 8.3 mm) — https://frankdarling.com/engagement-rings/the-single-scoop-round , https://www.pricescope.com/community/threads/how-high-are-center-stones-generally-set.258975 |
| Round brilliant Ø, 0.25 ct | 4.0–4.1 mm | [V2+] | https://whiteflash.com/diamond-education/mm-to-carat-weight-conversion-diamonds-guide , https://www.brilliantearth.com/news/mm-to-carat/ |
| Round brilliant Ø, 0.50 ct | 5.0–5.2 mm | [V2+] | same |
| Round brilliant Ø, 0.75 ct | 5.75–5.8 mm | [S1] | Whiteflash |
| Round brilliant Ø, 1.00 ct | 6.3–6.5 mm | [V2+] | Brilliant Earth 6.3, Whiteflash 6.5 (disagree by 0.2 mm) |
| Stone total depth | 59–62.5 % of Ø (≈ 4.0 mm for 1 ct) | [S1] | https://www.bluenile.com/blog/diamonds-jewelry/ideal-diamond-proportions |

Derived envelope for a size-49 solitaire [INF]:

- Outer Ø at the band = 15.6 + 2 × (1.3…2.0) = **18.2–19.6 mm**
- Overall height, bottom of band to top of stone = band thickness + 15.6 + setting height = (1.3…2.0) + 15.6 + (5.5…8.5) = **22.5–26 mm**
- Head width ≈ stone Ø + 1…1.5 mm for prongs → 5.5–8 mm for 0.25–1 ct
- **CAD envelope to reserve: Ø 21 mm × 28 mm tall × 9 mm thick at the head**, with the head on top. Lid inner clearance above the platform must exceed the standing ring by ≥ 3 mm.

### 1.4 How commercial ring boxes hold a ring

| Product | Holding feature | Numbers | Status | Source |
| --- | --- | --- | --- | --- |
| Westpack ring box insert | slit foam pad | pad 44 × 44 × 15 mm in a 45 × 45 × 30 mm interior; low-profile variant 10 mm foam in 45 × 45 × 18 mm | [SNIP] | https://www.westpack.com/eur_eu_eng/additional-foam-insert-for-ring-box-00272000100.html |
| INCA ring box | removable foam with an "H"-shaped slit for the shank | foam 18 mm thick | [SNIP] | https://www.incauk.com/0761.html |
| Amadesa ring tray | die-cut foam, velour-covered; roll-style inserts | foam 5/8 in (16 mm); slots 1¼ in (32 mm) deep; ½ in (13 mm) clearance to lid for tall heads | [SNIP] | https://amadesa.com/products/black-72-slot-ring-case |

No source gives a slit *width*: commercial boxes rely on compressed foam, so the slit is a cut of ~zero width and the foam grips by elastic recovery. The ring typically sits one third to one half of its height into 10–18 mm of foam. That is a friction hold only.

### 1.5 Positive locking — existing designs and what a drop needs

Existing printable designs (all [SNIP]):

- TPU 95A insert that grips the band — https://www.printables.com/model/924240-insert-for-engagement-ring-box-cryptex
- Slot that tapers toward the top so the ring "gently locks" — Printables listing via 3dgo.app
- Separate printed spring pressing against the ring — Thangs "Rose Ring Box"
- Snap ring through the ring, "impossible to fall out" — keychain-style holder on Printables
- Pokéball references: https://www.printables.com/model/51817-pokeball-ring-stand (hinged top, latch, button with printed leaf spring), https://www.printables.com/model/1165943-pokeball-ring-holder , MakerWorld "Pokeball Cone Ring Box" (central cone through the ring)

None of these is a rated lock. Order-of-magnitude drop load [INF]: ring mass 2–4 g; a rigid ≈ 250 g plastic ball dropped 1 m onto a hard floor decelerates at roughly 500–2000 g, so the ring pulls on its holder with **15–60 N** for a few milliseconds. Foam or velvet friction (well under 1 N) will not hold that; a form lock is required.

Design directions that give a form lock [INF]:

1. **Deep saddle + keeper through the bore.** Slot depth ≥ 10 mm (more than half the ring is not needed if a keeper is used); a tongue or pin 4–6 mm wide passes through the 15.6 mm bore just above the slot floor and is carried on both sides. The ring cannot leave without the keeper moving. The keeper can be a manual slide the recipient pulls, or be withdrawn by the lid linkage near full open.
2. **Slot closed over the band from above** by two spring fingers that meet above the bottom arc of the band (band 2.5 mm → fingers leave a 1.5 mm throat and must deflect ≥ 0.5 mm each). Holding force is then set by finger stiffness, not friction; size for ≥ 60 N pull-out.
3. **TPU liner** only as rattle damping in addition to 1 or 2, not as the lock.

Slot numbers for a 2.5 mm band [INF]: bare printed slot **2.8 mm** wide (0.15 mm clearance per side); if lined with self-adhesive velour (≈ 0.5 mm per side) open the printed slot to ≈ 3.5 mm so the lining is lightly compressed; or a **TPU 95A liner with a 2.3 mm slot** (0.1 mm interference per side). Slot depth 10–12 mm. All to be re-set from caliper measurements.

---

## 2. Springs

### 2.1 Torsion springs — Gutekunst Federn (federnshop.com)

Catalogue: 1,600 stock torsion springs (800 sizes × left/right), all stainless **1.4310**, tangential straight legs, tolerances to DIN 2194 grade 2. Source: https://www.federnshop.com/de/produkte/schenkelfedern.html [S1, manufacturer]. Detail page pattern: `https://www.federnshop.com/de/produkte/schenkelfedern/t-18460l.html`; datasheet pattern: `https://www.federnshop.com/de/datenblatt/federnshop-datenblatt-schenkelfeder_t-18460l.pdf`. STEP models: https://cad.federnshop.com (not downloaded).

Article suffix **L** = left-wound, **R** = right-wound (mirror images; same data and price).

#### Leg-angle convention — read this before placing legs in CAD

Established from the datasheet drawing plus the coil-count pattern in the catalogue [V2+ within the manufacturer's own data, geometry check INF]:

- The catalogue value "Schenkelstellung α" is the angle between the lever leg and the **extension** of the resting leg. Included angle between the two legs when free = **180° − α**.
- α = 0° → integer number of coils → legs collinear, pointing opposite ways (straight line).
- α = 90° → x.25 coils → legs form an L.
- α = 180° → x.5 coils → legs parallel, pointing the same way (hairpin).
- α = 270° → x.75 coils → legs crossed 90° past parallel.
- Loading is only permitted in the winding (coil-closing) direction, and **increases** α: lever-leg position = α + deflection. Source for "only in winding direction": https://www.ingenieur.de/fachmedien/konstruktion/maschinenelemente/metallfedern-richtig-auslegen/ [S1].

This differs from the common US catalogue convention where "180°" means straight legs. **Download the STEP of the chosen article and check it before modelling the leg seats.**

#### Candidates (all data from the detail pages; torques at intermediate angles are M = Mn·α/αn)

| Article | d | Di / De | nt | Lk0 | Ls | α free | Mn ± tol | αn | Rate | M @ 20° | M @ 110° | M @ 130° (% of Mn) | Mandrel Ø min–max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **T-18460L / R** | 0.8 | 7.2 / 8.8 | 6.5 | 6.0 | 45 | 180° | 61.92 ± 12.09 | 155.88° | 0.397 | 7.9 | 43.7 | **51.6 (83 %)** | 5.8–6.5 |
| T-18436L / R | 0.8 | 6.0 / 7.6 | 7.75 | 7.0 | 40 | 270° | 60.96 ± 12.57 | 155.54° | 0.392 | 7.8 | 43.1 | 51.0 (84 %) | 4.8–5.4 |
| T-18461L / R | 0.8 | 7.2 / 8.8 | 7.75 | 7.0 | 45 | 270° | 61.92 ± 11.59 | 185.83° | 0.333 | 6.7 | 36.7 | 43.3 (70 %) | 5.8–6.5 |
| T-18459L / R | 0.8 | 7.2 / 8.8 | 5.25 | 5.0 | 45 | 90° | 61.92 ± 12.72 | 125.94° | 0.492 | 9.8 | 54.1 | exceeds αn | 5.8–6.5 |
| **T-16324L / R** | 0.7 | 5.3 / 6.7 | 7 | 5.6 | 35 | 0° | 41.48 ± 8.59 | 143.91° | 0.288 | 5.8 | 31.7 | **37.5 (90 %)** | 4.3–4.7 |
| T-16305L / R | 0.7 | 4.3 / 5.7 | 8.25 | 6.48 | 35 | 90° | 40.62 ± 9.05 | 138.44° | 0.293 | 5.9 | 32.3 | 38.1 (94 %) | 3.5–3.8 |
| T-16325L / R | 0.7 | 5.3 / 6.7 | 8.25 | 6.48 | 35 | 90° | 41.48 ± 8.26 | 169.62° | 0.245 | 4.9 | 26.9 | 31.8 (77 %) | 4.3–4.7 |
| T-16343L / R | 0.7 | 6.3 / 7.7 | 5.75 | 4.73 | 35 | 270° | 42.10 ± 8.34 | 139.99° | 0.301 | 6.0 | 33.1 | 39.1 (93 %) | 5.0–5.6 |
| T-16363L / R | 0.7 | 7.3 / 8.7 | 5.75 | 4.73 | 35 | 270° | 42.56 ± 7.80 | 161.68° | 0.263 | 5.3 | 29.0 | 34.2 (80 %) | 5.9–6.5 |
| **T-16244L + R (pair)** | 0.63 | 5.37 / 6.63 | 7 | 5.04 | 30 | 0° | 30.87 ± 5.94 each | 163.52° | 0.189 each | 3.8 each / 7.6 pair | 20.8 / 41.5 | **24.5 each / 49.1 pair (79 %)** | 4.3–4.8 |

Units: mm, N·mm, N·mm/°. De = Di + 2d [INF]. Price for every article above: **5.11 € @ 1, 3.60 € each @ 2, 3.43 € @ 3, 2.22 € @ 7** (price group H). Whether these are net of VAT and what shipping costs was **not** visible on the pages — assume net B2B prices plus shipping until checked.

Three things in this table matter for the design:

1. **Mn tolerance is about ±20 %.** Size the latch and servo for 1.25 × nominal torque and make sure the lid still opens at 0.8 × nominal.
2. **Catalogue rates ignore leg bending.** With 0.8 mm wire, loading the legs 15 mm from the coil adds about 8° of deflection at 50 N·mm (≈ 6 % softer); loading at the full 45 mm leg length adds about 23° (≈ 18 % softer) [INF]. Seat the legs close to the coil and trim them; 15–20 mm is enough.
3. **Sustained preload:** Mn is the static limit. For weeks of preload stay at ≤ 80–85 % of Mn [INF — standard spring practice, not sourced]. T-18460, T-18436, T-18461, T-16325, T-16363 and the T-16244 pair meet that at 130°; T-16324 meets it only up to ≈ 115°.

Under 130° of wind-up the coil inner Ø shrinks (T-18460: 7.2 → 6.8 mm; T-16324: 5.3 → 5.0 mm) and the body grows by d·α/360 ≈ 0.25–0.3 mm [INF from the formulas in 2.3]. The mandrel must stay within the catalogue Ddmin–Ddmax; a bare 3 mm hinge pin is too small for every spring above and needs a printed or metal sleeve.

#### Which free angle fits which hinge layout [INF]

A thin hemispherical lid has its centre of gravity R/2 above the rim plane, i.e. 26.6° above horizontal seen from a rim hinge. Gravity torque about the hinge is m·g·R when closed (35 g, R = 50 mm → 17.2 N·mm, matching the 13–18 N·mm brief) and **falls to zero at 63° of opening**; beyond that gravity holds the lid open. The spring therefore only has to drive the first ≈ 65–90°, and a spring that runs free at 90° of lid angle is acceptable.

| Layout when lid is closed | Needed free angle α | Stock choice | Deflection closed / at 110° open | Torque closed |
| --- | --- | --- | --- | --- |
| A — legs folded together, both pointing forward (one under the platform, one in the lid rim plane) | 180° − deflection | α = 90°: **T-18459** | 90° / spring free from 90° lid angle | 44 N·mm (71 % Mn) |
| B — legs in line, one down the base wall and one up the lid wall | 360° − deflection | α = 270°: **T-18436** | 90° / free from 90° | 35 N·mm (58 % Mn) |
| C — legs in a 50° V closed, opening to 160° | 0° | **T-16324**, or **T-16244 L+R pair** | 130° / 20° | 37.5 N·mm; pair 49 N·mm |
| D — legs 130° apart closed, swinging toward parallel (20° apart) as the lid opens | 180° | **T-18460** | 130° / 20° | 51.6 N·mm |

Simulated opening (35 g lid, I = 5/3·m·R² = 1.46 × 10⁻⁴ kg·m² about the hinge, no friction or damping) [INF]: 0.13–0.19 s to reach 110°, arriving at 18–27 rad/s (lid front edge 1.8–2.7 m/s) with 0.02–0.05 J to absorb at the end stop. That is a visible "jump". It is also enough angular momentum to rock an unrestrained ball backwards — see open risks.

#### Other suppliers

Febrotec and Lesjöfors (https://shop.lesjofors.com/) stock torsion springs, but no torsion catalogue data could be retrieved this session; Hennlich lists 1.4310 torsion springs in a PDF catalogue (https://www.hennlich.at/fileadmin/user_upload/HAT/Produktkategorien/Federn_Maschinenelemente/Federn/Federnkatalog.pdf) not opened. MISUMI not checked. **Only Gutekunst is verified.**

#### Cheap assortments (Amazon.de / AliExpress / eBay)

Amazon and AliExpress pages could not be opened; the description below is from eBay and reseller listings that carry the same import goods [SNIP].

| Listing | Content | Source |
| --- | --- | --- |
| 10-pack, 0.8 mm wire | OD 5–10 mm, 3–6 coils, right-wound | https://www.ebay.de/itm/388684855790 |
| 10-pack, 0.5 / 0.6 mm wire | OD 2.5–8 mm, 3 / 6 / 9 coils, 60° / 90° / 120° / 180° | https://www.ebay.de/itm/266790377855 |
| 10-pack, 0.5 mm wire | OD 3–6 mm | https://www.ebay.de/itm/267372288534 |
| Swpeet 45-piece kit | 15 sizes, "304 stainless", 45° / 90° / 120° | desertcart mirror of an Amazon listing |
| VXB 10-pack | 0.5 mm wire, 5 mm OD, 9 turns, 180° | https://vxb.com/products/10-pack-stainless-steel-torsion-springs-for-tools |
| Bambu Lab Maker's Supply | 0.8 × 5 × 3 coils, 120°; 0.5 mm, 4.5 mm OD, 5 coils, 90° | https://eu.store.bambulab.com/en/products/torsion-spring |

None publishes torque, permissible angle, tolerance or a verified material. Estimates with the formulas in 2.3, assuming 1.4310-like wire (E = 185 GPa, 1350 MPa allowable) [INF]:

| Spring | Rate | Est. Mn | Est. αn | Verdict |
| --- | --- | --- | --- | --- |
| 0.8 mm, OD 5, 3 coils | 1.64 N·mm/° | 57 N·mm | **35°** | Unusable — yields long before 110° |
| 0.8 mm, OD 8, 6 coils | 0.48 | 62 | 129° | Borderline; at its limit at 130°, no margin |
| 0.6 mm, OD 6, 9 coils | 0.135 | 26 | 194° | Usable as a pair: 2 × 17.5 = 35 N·mm at 130° |
| 0.5 mm, OD 4.5, 5 coils | 0.158 | 15 | 94° | Too weak and too little angle |
| 0.5 mm, OD 5, 9 coils | 0.078 | 15 | 194° | Too weak (10 N·mm at 130°) |

Rule that falls out: with few coils the permissible angle is small. For ≥ 130° at these diameters you need roughly ≥ 6.5 coils in 0.8 mm, ≥ 7 in 0.7 mm. Most assortment springs have 3–6 coils. They are fine for prototyping the mechanism, not for the final part that sits preloaded for weeks with unknown wire.

### 2.2 Compression springs

**Ball-point-pen spring.** No published measurement of a pen spring was found (searched in English and German). Characterised instead by the Gutekunst stock springs of pen-like size [S1 for each row, "pen-like" is INF]:

| Article | Material | d | De | L0 | n | Rate N/mm | Fn N | sn mm | 1-off € |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D-026R-04 | EN 10270-1 | 0.30 | 4.0 | 25.0 | 12.5 | 0.130 | 2.47 | 18.97 | 4.61 |
| VD-026R-04 | 1.4310 | 0.30 | 4.0 | 25.0 | 12.5 | 0.112 | 2.12 | 18.97 | 4.85 |
| D-030 | EN 10270-1 | 0.32 | 4.32 | 19.2 | 8.5 | 0.196 | 2.84 | 14.45 | 4.72 |
| D-030B | EN 10270-1 | 0.32 | 4.32 | 28.6 | 12.5 | 0.134 | 2.96 | 22.14 | 4.72 |

So a pen spring is about **0.3–0.35 mm wire, 4–4.5 mm OD, 20–30 mm free length, 0.1–0.2 N/mm, 2–3 N at solid**. Treat as an estimate; measure any salvaged spring (hang a known weight).

**Stock alternatives in the requested window** (De 4–6 mm, L0 20–30 mm, 0.2–0.6 N/mm). Source: filtered search on https://www.federnshop.com/de/produkte/druckfedern.html , 41 hits saved in the CSV.

| Article | Material | d | De | L0 | n | Rate N/mm | Fn N | sn mm | 1-off € |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **VD-051B** | 1.4310 | 0.4 | 4.4 | 25.1 | 12.5 | 0.280 | 4.89 | 17.45 | 4.90 |
| D-051B | EN 10270-1 | 0.4 | 4.4 | 25.1 | 12.5 | 0.326 | 5.69 | 17.45 | 4.72 |
| **VD-045** | 1.4310 | 0.4 | 5.4 | 23.7 | 8.5 | 0.211 | 3.75 | 17.76 | 4.90 |
| D-045 | EN 10270-1 | 0.4 | 5.4 | 23.7 | 8.5 | 0.245 | 4.36 | 17.76 | 4.72 |
| VD-073A | 1.4310 | 0.5 | 5.5 | 30.0 | 18.5 | 0.236 | 4.12 | 17.44 | 4.94 |
| D-073 | EN 10270-1 | 0.5 | 5.5 | 30.0 | 12.5 | 0.408 | 8.63 | 21.19 | 4.72 |
| VD-073 | 1.4310 | 0.5 | 5.5 | 30.0 | 12.5 | 0.350 | 7.42 | 21.19 | 4.94 |

Fn/sn are the maximum force and travel. Ends: 0.4 mm wire "angelegt" (closed, not ground); 0.5 mm wire closed and ground.

**Fallback concept** [INF]: a plunger near the hinge pushing the lid up. VD-051B compressed 12–15 mm gives 3.4–4.2 N; acting 15 mm from the hinge axis that is 50–63 N·mm at closed, falling to nearly zero by ≈ 60–90° of lid angle — sufficient because gravity takes over at 63° (see 2.1). Cheaper to tune than a torsion spring (swap spring or shim), no leg-angle question, but needs a guided plunger and puts a point load on the lid.

### 2.3 Formulas for sanity checks

Symbols: d wire Ø, D = Di + d mean coil Ø, n active coils, E Young's modulus, M torque, α angle in degrees, w = D/d.

| Quantity | Formula | Status |
| --- | --- | --- |
| Torque rate | R_M = M/α = **E·d⁴ / (3667·D·n)** [N·mm/°]; equivalently E·d⁴/(64·D·n) per radian | [V2+] Shigley via https://www.webpages.uidaho.edu/mindworks/machine_design/posters/pdf/springs.pdf (θ = 64·M·D·N/(d⁴·E)); reproduces six Gutekunst catalogue rates to within 0.25 % with **E = 185,000 MPa** |
| Bending stress | σ = 32·M / (π·d³) | [V2+] same |
| Curvature correction (Shigley) | K_i = (4C² − C − 1) / (4C·(C − 1)), C = D/d | [S1] same poster |
| Curvature correction (EN 13906-3) | q = (w + 0.07) / (w − 0.75); σ_q = q·σ | [MEM] — standard is paywalled (https://www.din.de/en/wdc-beuth:din21:198895053); see check below |
| Allowable static stress | σ_zul = 0.7·Rm | [MEM], same caveat |
| Coil inner Ø under load | Di(α) = D·n / (n + α/360) − d | [INF] constant wire length |
| Body length under load | Lk(α) = (n + 1 + α/360)·d | [INF]; matches catalogue Lk0 = (n + 1)·d |
| Force at a lever arm | F = M / R_H | [S1] Gutekunst catalogue text |

Check of the two [MEM] items against catalogue data [INF]: applying q to Mn gives σ_q = **1341 MPa** for all three 0.8 mm series regardless of coil diameter, 1361 MPa for 0.7 mm and 1375 MPa for 0.63 mm. A single stress per wire size, rising as wire gets thinner, is exactly what "q-corrected stress = 0.7·Rm" predicts (implied Rm ≈ 1915 / 1945 / 1965 MPa, plausible for 1.4310). So the catalogue is consistent with those formulas, but the formulas themselves were not read from the standard.

For K_i versus q at C = 8.5: 1.096 versus 1.106 — interchangeable for a sanity check.

Usable allowables for hand checks: **1.4310 stainless ≈ 1340–1375 MPa** (back-calculated above) with E = 185 GPa; patented carbon spring wire EN 10270-1 SH/DH is higher (roughly 1500–1650 MPa at 0.8 mm) with E = 206 GPa [MEM].

---

## 3. Hinge pins and small hardware

| Item | Data | Status | Source |
| --- | --- | --- | --- |
| Parallel pin standard | ISO 2338 replaces DIN 7; nominal lengths differ from DIN; unhardened steel or austenitic stainless | [V2+] | https://fasten.it/en/norms/norm/din_en_iso_2338 , Keller & Kalmbach listings |
| ISO 2338 length series | …16, 18, 20, 22, 24, 26, 28, 30, 32, 35, 40, 45, 50… | [S1] | fasten.it |
| End chamfer | ≈ 0.35 mm (Ø2), 0.4 mm (Ø2.5), 0.5 mm (Ø3) | [S1] | fasten.it |
| Common stock tolerance | **m6** (A2, 1.4305); h8 exists but is less stocked ("on request" at some dealers) | [V2+] | https://www.ehorst.de/en/Zylinderstifte-ISO-2338-1-4305-A2-3-0x10-mm-Passung-m6-Kuppe-Fase-aehnl-DIN-7-1150207.html , Keller & Kalmbach, SFS |
| Ø3 lengths seen in stock | 3 × 10, 3 × 14, **3 × 36**; the owner can get 3 × 20 and 3 × 25 (2026-11-18), which is why the ring lock uses 25 mm and not the 24 mm of the ISO series | [SNIP] | https://www.keller-kalmbach.de/produkte/verbindungselemente/stifte/zylinderstifte/iso-2338-zylinderstift/ |
| Tolerance values | Ø3 m6 = 3.002–3.008; Ø3 h8 = 2.986–3.000; Ø2 m6 = 2.002–2.008; Ø2 h8 = 1.986–2.000 | [MEM] ISO 286 | — |
| Standard length range per diameter | Ø2: 6–20 mm; Ø3: 8–30 mm | [MEM] — **not confirmed**; dealers do list longer (3 × 36) | — |
| Stainless round bar | 1.4301, Ø2 and Ø3, bright, **h9** (Ø3 = 2.975–3.000), sold by the metre / 0.5 m / 3 m | [SNIP] | https://www.voss-edelstahl.com/online/en/Stainless-steel/round-bars/8/?lang=1 , eBay metal dealers (≈ 2–4 €/m) |

Practical reading: a **Ø3 × 30–40 mm** pin is easy (ISO 2338 A2 m6, or cut from h9 bar). A **Ø2 × 30–40 mm** dowel pin is probably outside the standard length range; cut it from Ø2 h9 bar and deburr/chamfer the ends.

**The concealed hinge cannot take one long pin (found 2026-11-18)** [INF, measured in the CAD model; `checks.py`, section "Pins"]. The hinge axis lies inside the lid, 7 mm above its rim. The lid's wall therefore closes the axis at both ends, whatever the opening angle, because the axis does not move in the lid: the wall begins 16.8 mm from the middle, and a Ø2 pin touches it already 14.0 mm from the middle, since the wall crosses the axis at 64° to its normal. Beside each hinge tower (outer face 10 mm from the middle) a pin has 4.0 mm of room, beside each rib of the lid 7.3 mm. A pin that passes through both ribs of the lid (13.4 mm over the ribs) can therefore not be put in at any length, neither with the lid on the stage nor into the lid alone. Revisions 1 to 5 specified one pin of 2 × 20 mm "pushed through tower, rib, sleeve, rib and tower"; that could not have been done. No check had covered the path of a pin.

Ways out that were examined:

| Way | Result |
| --- | --- |
| **Two short pins 2 × 8, one in each tower** (chosen by the owner) | Each pin is pressed into its tower from outside until it is flush with the tower's inner face and waits there, standing 4.9 mm out, while the lid is slid on; then both are pressed in with long-nose pliers. Press fit in the towers (2.9 mm), the ribs of the lid turn on the pins (3.4 mm each), the tips carry the spring sleeve (1.35 mm each). The inside of the lid wall is relieved to 1.3 mm beside the knuckles so that the waiting pins have room; nothing shows outside. To take the lid off, the printed sleeve has to be cut. |
| One 2 × 18 pin through a hole in each flank of the lid | Simple and removable, but each hole of 2.2 mm meets the surface at 64° and shows as an oval of about 2.2 × 5.0 mm, 7 mm above the band and 27° from the middle of the back. Against "nothing betrays that the ball can open". |
| Pin mounted in the towers, ribs of the lid open on one side and clipped on | Nothing shows and the lid comes off without tools. Rejected: an open knuckle is a hook, and the blow of the lid on its end stop (0.02 to 0.05 J, section 2.1) and the stop tab on the same rib would load that hook where it is thinnest; the lid prints with its rim on the bed, so the hook would also be loaded across the layers. A lid that comes off while it jumps open is the worst failure this device can have. |
| Two pins 2 × 10 | They would meet in the middle and support the sleeve over its whole length, but a waiting pin would need a relief that leaves less than 0.8 mm of wall. |
| Three pins (2 × 8 in the sleeve, 2 × 6 in each tower) | Needs no relief in the lid, but two lengths to buy, and the middle pin is held in each rib by 0.7 mm only. |

The same review found that the bore for the Ø3 lock pin stopped 0.9 mm short of the outside of the stage's rear wall at its lower edge, leaving a sliver in the pin's path; the bore now runs out through the wall.

**Long M2 / M3 screws as hinge pins** [INF; thread lengths from section 4, diameters MEM]: ISO 4762 screws have a thread length b = 16 mm (M2), 17 mm (M2.5), 18 mm (M3); only screws longer than that have a plain shank (an M3 × 40 has ≈ 22 mm of shank, Ø ≈ 2.86–3.00). A thread running inside a printed knuckle acts as a file and the fit is sloppy (thread major Ø ≈ 2.87–2.98). If a screw is used: let the moving knuckles ride on the plain shank, put the threaded end into a heat-set insert in the fixed part, and do not rely on it for alignment.

**Shoulder screws:** ISO 7379 officially starts at 6.5 mm shoulder / M5; 4 mm-M3 and 5 mm-M4 are dealer extras outside the standard; nothing with a 3 mm shoulder was found in German retail [SNIP] (https://ehorst.de/en/Pass-Schulterschraube-mit-Bund-ISO-7379-6-M5-12-Passung-f9-1162680.html and RS listings). Too large for this hinge. Miniature shoulder screws (MISUMI and similar) not checked.

---

## 4. Fasteners in printed parts

### 4.1 Heat-set inserts

CNC Kitchen and ruthex publish the same geometry family; the two tables agree line for line except for the M2 and M2.5 lengths.

| Thread | Brand / type | L | Insert Ø D1 | Pilot tip Ø D2 | **Hole Ø D3** | Min wall W | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M2 | CNC Kitchen standard | 3.0 | 3.6 | 3.1 | **3.2** | 1.3 | [V2+] |
| M2 | ruthex RX-M2x4 | 4.0 | 3.6 | 3.1 | **3.2** | 1.3 | [V2+] |
| M2.5 | CNC Kitchen standard | 4.0 | 4.6 | 3.9 | **4.0** | 1.6 | [V2+] |
| M2.5 | ruthex RX-M2,5x5.7 | 5.7 | 4.6 | 3.9 | **4.0** | 1.6 | [V2+] |
| M3 | CNC Kitchen standard / ruthex RX-M3x5.7 | 5.7 | 4.6 | 3.9 | **4.0** | 1.6 | [V2+] |
| M3 | CNC Kitchen short | 3.0 | 4.6 | 3.9 | **4.0** | 1.6 | [S1] |
| M3 | CNC Kitchen "Voron" | 4.0 | 5.0 | 4.25 | 4.4 | 1.3 | [S1] |

Sources: https://www.3djake.com/cnc-kitchen/threaded-inserts-set-standard (column headings there: length, insert diameter, centre tip, hole diameter, wall thickness min.), https://www.3djake.ch/de-CH/ruthex/m2-m3-m4-m5-gewindeeinsatz-sortimentskasten , https://www.3djake.ch/de-CH/ruthex/gewindeeinsatz-m25-70-stueck . The ruthex pages label the columns only D1/D2/D3/L/W; mapping them to the CNC Kitchen headings is safe because the numbers are identical, and ruthex's own drill set is 3.2 mm for M2 and 4.0 mm for M2.5.

Derived for CAD:

| Thread | Hole Ø | Hole depth | Min boss Ø (= hole + 2·W) | Recommended boss Ø |
| --- | --- | --- | --- | --- |
| M2 | 3.2 | L + 1 → 4.0 (CNC K) / 5.0 (ruthex) | 5.8 | 6.5 |
| M2.5 | 4.0 | 5.0 / 6.7 | 7.2 | 8.0 |
| M3 | 4.0 | 6.7 (std) / 4.0 (short) | 7.2 | 8.0 |

- Depth = insert length + 1 mm, straight (not tapered) hole [V2+]: https://www.cnckitchen.com/blog/tipps-amp-tricks-fr-gewindeeinstze-im-3d-druck-3awey , https://make.epfl.ch/wiki/public/spot_-_3d_printing/how_to_use_threaded_inserts . Hackaday suggests +50 % of insert length instead — more generous, also fine.
- Chamfer: CNC Kitchen says none needed; EPFL says 0.3–0.5 mm. Disagreement; a 0.3 mm lead-in does no harm.
- Install at print temperature + 10…20 °C; melt in ≈ 90 % with the iron and seat the rest flat with a cold tool [S1] 3DJake / Prusa listing.
- Holes print 0.1–0.2 mm undersize; the tabulated values are *design* values used by both brands, so do not add compensation on top unless a test hole says so.

### 4.2 Self-tapping screws into printed plastic

Bambu Lab's published hole table for its BT-series self-tapping screws [S1, forum copy of the Bambu wiki]: https://forum.bambulab.com/t/how-to-design-screw-holes-for-3d-printing/217352

| Screw | Material | "Vertical" hole: mouth in an upright wall of the print | "Horizontal" hole: mouth parallel to the bed | Wall loops | Engagement | Torque |
| --- | --- | --- | --- | --- | --- | --- |
| BT2 | PLA Basic | 1.80 | 2.00 | 2 | 4.0 mm | 0.15 N·m |
| BT2 | PETG Basic / HF | 1.65 / 1.60 | 2.00 / 1.95 | 2 | 4.0 | 0.15 |
| BT2.5 | PLA Basic | 2.20 | 2.35 | 2 | 5.0 | 0.20 |
| BT2.5 | PETG Basic / HF | 2.05 / 2.00 | 2.35 | 2 | 5.0 | 0.20 |
| BT3 | PLA Basic | 2.55 | 3.00 | 3 | 6.0 | 0.30 |
| BT3 | PETG Basic / HF | 2.40 | 2.95 / 2.80 | 3 | 6.0 | 0.30 |

**Correction (2026-11-18).** Until revision 5 this note took the source's "horizontal" and "vertical" to mean the direction of the hole axis. The source defines them by the surface in which the hole opens, which is the opposite: "When the screw hole opening surface is parallel to the print bed, we call it a horizontal screw hole", and "When the screw hole opening surface is at a right angle to the print bed, we call it a vertical screw hole". A hole that stands upright in the print is therefore a *horizontal* hole and needs the *larger* diameter, because such small closed loops shrink ("Material cooling and the seam affect the size of horizontal screw holes"). The column heads of the table above have been corrected. The 1.8 mm pilot that revisions 1 to 5 used for 2.2 mm screws in upright holes was tighter than this source advises.

Same source, **machine screws threaded directly into the print** [S1, read again on 2026-11-18]:

| Filament | Thread | Pitch Ø of the thread | "Horizontal" hole: mouth parallel to the bed | "Vertical" hole: mouth in an upright wall |
| --- | --- | --- | --- | --- |
| PLA | M2 / M2.5 / M3 | 1.740 / 2.208 / 2.675 | 2.10 / 2.50 / 2.90 | 1.84 / 2.30 / 2.72 |
| PETG HF | M2 / M2.5 / M3 | 1.740 / 2.208 / 2.675 | **1.95** / 2.45 / 2.90 | **1.70** / 2.15 / 2.60 |
| PETG Basic | M2 / M2.5 / M3 | 1.740 / 2.208 / 2.675 | 2.10 / 2.50 / 2.90 | 1.74 / 2.20 / 2.72 |

Thread engagement 4.0 / 5.0 / 5.0 mm and tightening torque 0.13 / 0.20 / 0.25 N·m for M2 / M2.5 / M3; "For BT2 and M2 screws, we suggest setting the engagement length to at least 4 mm". The source suggests machine screws "when you don't need to take the screw out often", and a 45° chamfer at the mouth of the hole that "shall not be counted toward the thread engagement length".

Second sources for M2 in an actual hole of about 1.6 to 1.75 mm: a MakerWorld post that gives 1.70 mm for PETG [SNIP] https://makerworld.com/en/community/post/1182854 , and the rules "outer Ø − 0.4 mm" and "80 % of the screw Ø" in the table below, which both give 1.6 mm. The two hole directions were not found in a second source: how much a small upright hole shrinks is a property of printer, slicer and filament, which is why the model exports a test piece.

Other guidance, for sizes not in that table:

| Rule | Gives | Status | Source |
| --- | --- | --- | --- |
| Pilot = screw outer Ø − 0.4 mm | 2.2 → 1.8; 2.6 → 2.2; 3.0 → 2.6 | [S1] | https://rigid-prints.pages.dev/design-guide/holes-bosses-threads |
| Pilot ≈ 80 % of screw Ø | 2.2 → 1.75; 2.6 → 2.1; 3.0 → 2.4 | [S1] | https://www.albanycountyfasteners.com/blog/fasteners-for-3d-printing/ |
| Accu "Polyfix" chart | M2.5: 1.85 (PETG/ABS) / 2.05 (PLA/nylon); M3: 2.30 / 2.50 | [SNIP] | https://accu-components.com/p/488-threaded-insert-hole-size-charts-for-3d-printing-pla-petg-resin |

Working values since revision 6, for **M2 machine screws that form their own thread in PETG**: **1.95 mm where the mouth of the hole lies parallel to the bed, 1.70 mm where it lies in an upright wall**, at least 4 mm of thread not counting a 0.3 mm lead-in, and a blind hole 0.3 mm deeper than the screw reaches, because a machine screw has a blunt end. These are the smaller of the source's two PETG figures in each direction: a hole that prints too tight can be opened with a drill, one that prints too loose cannot be mended. The owner asked for M2 because 2.2 mm self-tapping screws are hard to come by in Germany.

Working values for self-tapping screws, used until revision 5: **Ø2.2 screw → 1.8 mm; Ø2.6 → 2.1–2.2 mm; Ø3.0 → 2.4 (PETG) – 2.55 (PLA)**, boss outer Ø ≥ 2 × screw Ø, engagement ≥ 2 × screw Ø. The sources warn that PLA bosses split with self-tappers; print bosses with ≥ 3 wall loops and avoid repeated re-assembly — use inserts wherever the joint will be opened more than a few times.

### 4.3 Screw head dimensions

ISO 4762 socket head cap screws [V2+ for M2: fasten.it and Engineers Edge; S1 for the rest]: https://fasten.it/norms/norm/din_en_iso_4762

| Thread | Pitch | Head Ø dk max / min | Head height k max | Hex key | Thread length b |
| --- | --- | --- | --- | --- | --- |
| M2 | 0.4 | 3.80 / 3.62 | 2.0 | 1.5 | 16 |
| M2.5 | 0.45 | 4.50 / 4.32 | 2.5 | 2.0 | 17 |
| M3 | 0.5 | 5.50 / 5.32 | 3.0 | 2.5 | 18 |

(The source prints k min = 2.66 for M2.5, larger than k max — a typo on that page.)

ISO 7380-1 button heads: the standard **starts at M3** [S1] https://fasten.it/en/norms/norm/din_en_iso_7380-1

| Thread | Head Ø dk max / min | Head height k max / min | Hex key | Status |
| --- | --- | --- | --- | --- |
| M3 (ISO 7380-1) | 5.70 / 5.40 | 1.65 / 1.40 | 2.0 | [V2+] fasten.it, Fastenright |
| M2 (vendor, "similar to ISO 7380") | 3.5 (one listing 3.7) | 1.3 | 1.3 [MEM] | [SNIP] https://www.fastenright.com/general-fixings/socket-button-head-screw-to-iso-7380/sk07 |
| M2.5 (vendor) | 4.5 or 4.7 — **sources disagree** | 1.5 | 1.5 [MEM] | [SNIP] Westfield 4.5, Accu 4.7 |

For M2 / M2.5 button heads, counterbore for the larger figure (M2 Ø4.2, M2.5 Ø5.2) or measure the purchased screws.

ISO 7045 (DIN 7985) pan head with cross recess, M2: head Ø4.0, height 1.6, recess size 1 [SNIP] https://westfieldfasteners.co.uk/Standards/ScrewBolt-PhilRaPan-M.pdf ; another vendor table prints 1.75 for the height [SNIP] https://tfc.eu.com/?p=2043 . The model keeps room for a head of Ø4.0 x 2.0 mm, which takes this head and the ISO 4762 cap head. The two screws of the speaker clamp must have the hex socket all the same [INF, measured in the model; `checks.py`, section "Small screws"]: they lie deep in the core, a screwdriver in line with them meets the chassis, and only the long arm of a 1.5 mm hex key (or a ball-end driver held 10 to 20° off the axis) reaches them. The parts list therefore names ISO 4762 / DIN 912 for all seven screws.

Plain washers ISO 7089 (DIN 125 A): M2 is 2.2 x 5.0 x 0.3 (0.2–0.4), M2.5 is 2.7 x 6.0 x 0.5 [SNIP] https://mcmaster.com/products/washers/specifications-met~iso-7089 , https://accu-components.com/de/metrische-flachwaschmaschinen/72476-HPW-M2-A2 . A 5 mm washer cannot keep the pawl (bore 5.3 mm) on its pivot, which the parts list of revisions 1 to 5 overlooked; the pivot washer is printed since revision 6.

Clearance holes, ISO 273 medium: M2 2.4, M2.5 2.9, M3 3.4 [MEM]. Counterbores for cap heads in printed parts: head Ø + 0.5 mm, depth = k + 0.3 mm [INF].

---

## 5. FDM design rules (PLA / PETG, 0.4 mm nozzle, 0.2 mm layers)

### 5.1 Clearances

| Fit | Published values | Source |
| --- | --- | --- |
| Sliding fit | 0.2–0.3 mm per side generic; PLA 0.15–0.25; PETG 0.2–0.3; ASA 0.25–0.35 | https://www.sovol3d.com/blogs/news/fdm-3d-printing-tolerances-clearances-how-to-design-parts-that-fit |
| Clearance fit (moving, lids, print-in-place) | 0.3–0.5 mm | https://blog.snapmaker.com/blog/3d-printing-tolerances/ |
| Transition / snug | 0.1–0.2 mm | Snapmaker |
| Press fit | 0.0 to −0.05 mm (Snapmaker); "0.05–0.15 mm per side" clearance (Sovol); −0.05 to −0.15 mm for a static pin, bosses split beyond ≈ 0.20 mm interference (QIDI, [SNIP]) | Snapmaker, Sovol, https://qidi3d.com/blogs/print-lab/3d-printed-snap-fit-joints-clearance-guide |
| Print-in-place hinge | 0.3–0.4 mm (QIDI [SNIP]); 0.3–0.5 mm (3dprintcalcs [SNIP]); "≈ 0.3–0.4 mm total" (Sovol) | as named, https://3dprintcalcs.pages.dev/reference/common-tolerances |
| Pin inserted after printing | 0.15–0.25 mm on radius | QIDI [SNIP] |
| Printed holes | undersize, worse for small holes; drill to size if critical | https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/ |

The sources agree on sliding and clearance fits and **disagree on press fits** (they do not even agree on the sign). All are vendor blogs; none is a controlled study. Treat as starting values for a coupon.

**Recommended CAD values** [INF from the table]:

| Feature | Value |
| --- | --- |
| Printed part sliding in printed guide (latch bolt, keeper) | 0.20 mm per side PLA, 0.25 mm per side PETG |
| Ø3.00 steel pin, **rotating** in printed knuckle | bore Ø3.30 as designed (0.15 mm per side); or print Ø2.9 and drill/ream 3.1 for a quieter hinge |
| Ø3.00 steel pin, **fixed** end | bore Ø2.90–2.95 as designed, press in warm; or Ø3.0 plus a drop of CA |
| Ø2.00 pin, rotating / fixed | Ø2.25–2.30 / Ø1.90–1.95 |
| Printed-to-printed press fit | 0.00 to −0.05 mm per side, with a lead-in chamfer |
| Lid-to-base rim (lip and groove) | 0.25 mm per side radially; 0.2–0.3 mm designed gap at the visible seam |
| Knuckle axial gaps along the hinge | 0.2–0.3 mm each |
| Spring coil to mandrel sleeve | sleeve Ø inside catalogue Ddmin–Ddmax; ≥ 1 wire Ø + 0.5 mm axial room for body growth |
| Horizontal bores | teardrop or flat-roof profile; bridges ≤ 5 mm print unsupported (Hubs) |

Print one coupon carrying the pin bores, the latch slide, and the M2/M3 insert holes before committing; adjust once.

### 5.2 Wall thickness and stiffness of the 100 mm dome

2.2 mm equals 5 perimeters at Bambu defaults (0.42 outer + 4 × 0.45) → solid wall, no infill gaps [INF]. Loads on the lid are tiny (latch force well under 1 N at the front edge, see 7.2), and a doubly curved shell this thick is very stiff; 2.2 mm is ample structurally. Thickness matters more for **opacity** (5.5) and for the rim: add a local rim rib or lip of 3–4 mm so the open edge does not ovalise and the seam gap stays even. No published minimum-wall figure specific to domes was found; Hubs gives no number.

### 5.3 Overhangs

Up to 45° from vertical prints without support; steeper needs support; bridges up to 5 mm [S1] https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/

### 5.4 Printing the hemispherical shells

| Point | Guidance | Status |
| --- | --- | --- |
| Orientation | **Rim (flat cut) on the bed, dome up.** Never rest a curved surface on the plate | [V2+] https://all3dp.com/2/3d-printing-spheres-tutorial/ , https://forum.bambulab.com/t/inconsistent-gaps-and-edge-refinement/234251 |
| Consequence | Outer surface is entirely upward-facing (no supports touch it). The *inside* overhangs progressively: 45° at 71 % of the height, horizontal at the pole → the inner cap needs support | [INF geometry] |
| Supports | Inside only. Users report a rough inner surface where supports were (a Pokéball print, Prusa forum) — acceptable because it is hidden; widen the support Z-gap or use a support-interface material | [S1] https://forum.prusa3d.com/forum/how-do-i-print-this-printing-help/sphere-supports |
| Alternative | Flatten or thicken the inner pole so the last layers bridge instead of overhang (also gives a place for a boss) | [S1] All3DP |
| Layer height | Stair-stepping is worst near the pole. Use variable layer height: 0.2 mm on the lower two thirds, 0.08–0.12 mm on the cap | [S1] MakerWorld / Bambu forum reports of 0.12 mm |
| Seam | Paint the seam to the back, where the hinge is; on the base, hide it in the hinge line too | [S1, weak] one Bambu forum report |
| First layer | Add a 0.4–0.5 mm × 45° chamfer on the rim or enable elephant-foot compensation, otherwise the seam between halves shows a flare | [S1] Hubs |

### 5.5 Multi-colour (AMS)

| Point | Finding | Status / source |
| --- | --- | --- |
| Flush volume | Bambu Studio auto-calculates per colour pair; a global multiplier scales it (1.0 default; Bambu suggests trying 0.8–0.9) | [SNIP] https://wiki.bambulab.com/en/software/bambu-studio/reduce-wasting-during-filament-change (page returned 402), third-party summary |
| Costly direction | Anything **into white / light**, and anything **from black or red** needs the most flushing | [V2+] https://forum.bambulab.com/t/ams-flushing-volumes-calibration-purge-reduction/37062 , https://dreaming3d.net/blogs/news/how-to-reduce-multicolor-purge-waste-the-settings-that-actually-work |
| Tuning | Raise only the problem cells (red→white, black→white) rather than the whole table | [S1] dreaming3d |
| Bleed that is not a purge problem | White is translucent: red or black *behind* a thin white wall shows through as pink/grey. One user still saw red through six white walls; matte white hides better; "red covers white, white does not cover red" | [SNIP] https://forum.bambulab.com/t/multi-color-bleed-through/3980 , https://forum.bambulab.com/t/colour-showing-through-white-pla/45303 , https://forum.bambulab.com/t/black-to-white-outer-wall-bleed-i-dont-think-its-a-purging-issue/96483 |
| Fixes reported | One body per colour; keep coloured regions deep (full wall thickness) rather than painted skins; print light before dark within a layer; order infill first | [SNIP] same threads |
| Mixed polymers | PLA and PETG do not bond to each other (they are used as support interface for one another) — every colour in one printed part must be the same polymer | [MEM] |

**Black band: inlaid colour or separate part?** [INF] Recommend a **separate black part** (band ring plus button bezel), with white and red shells printed single-colour:

- An inlaid band means two to three filament changes on every layer that crosses the band; at 0.2 mm layers an 8 mm band is ≈ 40 layers, so on the order of 100 changes with black→white among them — the worst pair — for a long, wasteful print and the highest bleed risk exactly at the most visible line.
- Single-colour shells remove the red-behind-white problem entirely and let each shell be printed with its best settings.
- A separate band doubles as a functional part: it can carry the seam lip, hide the hinge and latch, and be printed in a tougher or matte material.
- If the band must be inlaid for looks, make the black a full-depth body (not a painted skin), keep it off the white shell's layers where possible, and raise the black→white flush cell.

Actual flush volumes per change were not verified this session; read them from the Bambu Studio flushing table for the specific filaments.

### 5.6 Translucent material for LED diffusion

| Finding | Status / source |
| --- | --- |
| Milky (white/natural) PLA diffuses better than colourless PLA; thicker walls lower transmission and raise haze; the relation is not simple Beer–Lambert | [SNIP] integrating-sphere study, https://iieta.org/download/file/fid/193673 |
| Clear PETG changes LED colour least; natural PLA shifts colour temperature; cold-white PLA blocks too much; "transparent" PLA is barely transparent; clear PETG haze varies by brand | [S1] maker reports, https://forum.bambulab.com/t/led-diffuser-using-transparent-pc/185469 |
| For RGB LEDs start with **white PLA, 2 layers × 0.2 mm (0.4 mm)** and thicken if still too bright; lamp diffusers are offered at 0.6 mm and 0.8 mm | [S1] same thread; MakerWorld diffuser models |

Reading for this device [INF]: two different jobs. A **light pipe / window** (button, status ring) wants clear PETG, 1–2 mm, with the LED 10+ mm behind it or a white cavity around it. A **glowing surface** wants white/natural material 0.4–0.8 mm thick with the LED ≥ 10–15 mm behind to avoid a hot spot. The 2.2 mm white shell will glow dimly and show internal shadows; decide deliberately whether that is wanted and thin the wall locally where light should come through. Print a swatch with 0.4 / 0.6 / 0.8 / 1.2 mm steps in the actual filament (https://makerworld.com/models/1922544 is a ready-made test).

### 5.7 Creep and heat — what to use for a spring-loaded latch and hinge

| Evidence | Finding | Status / source |
| --- | --- | --- |
| Creep, peer-reviewed | Six printed materials at 25 / 40 / 60 °C and 10 / 20 MPa for 3 h. **PLA has the worst creep resistance** ("use at room temperature with no load or very low static loads"); tough PLA slightly better; CPE (Ultimaker co-polyester, PETG family) **better than ABS, PLA and tough PLA**; PC best; load matters more than temperature | [S1] Dogan 2022, Strojniški vestnik 68(7-8) 451–460, https://www.sv-jme.eu/article/short-term-creep-behavior-of-different-polymers-used-in-additive-manufacturing-under-different-thermal-and-loading-conditions/ (PDF saved). The paper expands CPE as "chlorinated polyethylene" but cites the Ultimaker CPE datasheet, which is a co-polyester |
| Creep, practitioners | PLA clips lose tension and deform permanently; PETG "creeps only slightly and usually keeps its tension", default choice for parts under continuous tension; PC possibly better | [S1, anecdotal] https://forum.bambulab.com/t/pla-vs-petg-hf-deformation-under-load/212834 |
| Creep, dissent | One site rates PLA creep "good" and warns against PETG, quoting unsourced figures at 50 % of ultimate strength | [S1, unsourced] http://kanrog.com/printed_frame_material.html — far above the stresses here; not followed |
| Stiffness (3-point bending) | PLA 3300 MPa, ASA 2300 MPa, PETG 1900 MPa | [S1] https://cnckitchen.com/blog/comparing-pla-petg-amp-asa-feat-prusament |
| Heat, loaded sample in oven | PLA starts to give at 60 °C, fails ≈ 65 °C; PETG 80 / ≈ 85 °C; ASA softens 110 °C, fails 120 °C | [S1] same CNC Kitchen test |
| Heat deflection temperature (0.45 MPa) | Prusament PLA 55 °C; Prusament PETG 68 °C; an ASA datasheet 92 °C (other brand, ASTM D648) | [V2+ for PLA/PETG ordering] https://cdn.shopify.com/s/files/1/1745/6181/files/PRUSA_PLA_TechSheet_ENG.pdf , https://cdn.shopify.com/s/files/1/1745/6181/files/PETG_TechSheet_ENG.pdf , https://cdn.shopify.com/s/files/1/0919/6571/8867/files/purefil_ASA_Material_data_sheet.pdf |
| Car interior | Dashboard ≈ 69 °C after an hour in direct sun; a test on an 80–85 °C dashboard deformed PLA in under a minute | [SNIP] https://jlc3dp.com/blog/pla-temperature-resistance , https://makers101.com/heat-resistant-3d-printing-filament/ |
| Layer adhesion | ASA printed without enclosure reached only 29 % of its flat strength across layers (PLA 55 %, PETG 46 %); a ≈ 30 °C enclosure helped ASA by ≈ 20 % | [S1] CNC Kitchen |

No source was found that tests a printed spring latch held for weeks, and no measured PETG-versus-ASA creep comparison. The recommendation below rests on the evidence above plus a stress estimate.

Stress estimate for this device [INF]: a 50 N·mm spring loaded 15 mm from the coil presses each leg seat with ≈ 3.3 N; the latch at the front edge (100 mm from the hinge) carries only ≈ 0.2–0.7 N. Over a seat 0.8 mm × 8 mm that is ≈ 0.5 MPa; over a Ø3 × 5 mm knuckle ≈ 0.2 MPa. These are 20–50 times below the 10 MPa at which the study saw creep, so **at room temperature creep is controllable in any of the three materials if the contacts are generous**. A leg tip digging into plastic on a point contact is the exception — that will indent over weeks in PLA.

**Recommendation:**

1. **PETG for everything that carries spring load** — hinge knuckles, spring seats, latch pawl and strike, servo mount, ring keeper. Best creep behaviour of the three with evidence behind it, HDT 68 °C, tough rather than brittle, no enclosure needed.
2. **PLA only for cosmetic shells, and only if the device is certain to stay below ≈ 45–50 °C.** PLA prints the cleanest dome, but it is the worst for sustained load and softens at 55–60 °C; in a sun-heated car the preloaded lid would deform permanently. If shells are PLA, put the hinge and latch on a PETG chassis that the shells screw to.
3. **ASA if a hot car or direct sun is a realistic scenario** and an enclosed printer is available: ≈ 25–40 K more heat margin than PETG. Costs: enclosure, fumes, weaker layer bonds, more warping on a 100 mm dome. PETG's own margin over a 69 °C dashboard is zero — for that scenario PETG is not enough either.
4. Whatever the polymer: run spring forces into **metal** where possible (legs bearing on the hinge pin, a screw shank or an insert), give every plastic seat ≥ 8 mm of line contact, and let the lid sit on a hard stop at closed so the preload goes through the latch only.
5. Simple check before the event: assemble, latch, leave it at ≈ 40 °C (on a radiator shelf) for 48 h, and confirm the seam gap and latch engagement are unchanged.

---

## 6. Magnets and RF materials

### 6.1 Small disc magnets

Holding force = straight pull from a thick, flat steel plate in direct contact (manufacturer's convention). Source: supermagnete.de product pages [S1 each], e.g. https://www.supermagnete.de/eng/disc-magnets-neodymium/disc-magnet-8mm-3mm_S-08-03-N

| Size Ø × h | Article | Grade | Holding force | Shear ("displacement") | Max temp | Mass | Price @ 10 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 × 2 | S-05-02-N52N | N52 | ≈ 680 g (6.67 N) | ≈ 140 g (1.33 N) | 65 °C | 0.3 g | 0.31 € |
| 6 × 2 | S-06-02-N | N45 | ≈ 740 g (7.26 N) | — | 80 °C | 0.43 g | 0.31 € |
| 6 × 3 | S-06-03-N | N45 | ≈ 990 g (9.71 N) | ≈ 200 g (1.93 N) | 80 °C | 0.64 g | 0.36 € |
| 8 × 3 | S-08-03-N | N45 | ≈ 1.5 kg (14.7 N) | ≈ 290 g (2.88 N) | 80 °C | 1.1 g | 0.43 € |

Cross-checks and disagreements:

- 8 × 3 N45: an eBay seller table gives 1.52 kg — agrees [V2+]. An older supermagnete catalogue said 1.3 kg.
- 6 × 2 N45: the same eBay table gives 644 g against supermagnete's 740 g — 13 % apart.
- 5 × 2: only N35 at 395 g (eBay) and N52 at 680 g (supermagnete) were found; the plain S-05-02-N (reported as N40) force was not retrieved. The N52/N35 ratio here (1.72) is larger than the grade ratio 52/35 = 1.49, so the two vendors do not measure alike.
- Grade scaling at equal size is roughly proportional to the grade number: N35 ≈ 0.78 ×, N42 ≈ 0.93 ×, N52 ≈ 1.16 × the N45 value [INF].

Design notes [INF unless marked]:

- Shear force is ≈ 20 % of pull (ratios in the table: 19–21 %) [S1 arithmetic on source data]. A magnet resists sliding poorly.
- Force collapses with gap; a magnet behind 0.6–1 mm of plastic delivers a fraction of the catalogue value. Gap curves were not retrieved — test the actual stack.
- As closure assist the magnet acts **against** the opening spring. At the front edge (100 mm from the hinge) even 1 N adds 100 N·mm of holding torque — more than the spring. Use magnets as detents (lid-open hold, keeper position) rather than at the latch, or keep them far weaker than the spring margin.
- N52 is rated to 65 °C only; N45 to 80 °C.
- Keep magnets away from the NFC antenna and the speaker's own magnet path.

### 6.2 NFC ferrite sheets (13.56 MHz)

Würth Elektronik WE-FSFS flexible sintered ferrite sheet, self-adhesive [S1, manufacturer]: https://www.we-online.com/en/components/products/WE-FSFS

| Order code | Size | Thickness | µ′ / µ″ at 13.56 MHz |
| --- | --- | --- | --- |
| **364004** | 60 × 60 mm | 0.1 mm | 120 / 2 |
| **364005** | 60 × 60 mm | 0.2 mm | 120 / 2 |
| **364006** | 60 × 60 mm | 0.3 mm | 120 / 2 |
| 364001 / 364002 / 364003 | 120 × 120 mm | 0.1 / 0.2 / 0.3 mm | 120 / 2 |
| 3641014, 364103, 364104, 364105 | 60 × 60 mm | 0.14 / 0.3 / 0.4 / 0.5 mm | 150 / 3 |
| 354xxx, 374xxx | 60 × 60 and 120 × 120 | 0.1–0.3 mm | 150–170 / **90** — lossy at 13.56 MHz, wrong family for NFC |

- The **364** family is the one Würth's application note names for 13.56 MHz (µ″ stays below 2, µ′ above 100) [SNIP] https://www.we-online.com/components/media/o109011v410%20ANP016a%20DE.pdf
- Operating range −40…+85 °C [SNIP, RS listing].
- EU sources: RS Components (e.g. https://benl.rs-online.com/web/p/shielding-sheets/8235386 for 60 × 60 × 0.3), Würth direct, Mouser, DigiKey. Prices varied between regional RS pages and were not pinned down.
- **Disagreement:** an RS listing associates Würth number 364003 with a 60 × 60 × 0.2 mm sheet; Würth's own page says 364003 is 120 × 120 × 0.3 mm. Order by the Würth code from Würth's table.
- Thicker sheet shields better; 0.2–0.3 mm is the usual choice when metal (servo, speaker magnet, battery) sits behind the antenna [INF].

---

## 7. Servo-released spring latches

### 7.1 Reference designs

| Design | What it shows | Source |
| --- | --- | --- |
| PokeBall Ring Stand | Hinged top that latches shut; front button with a printed leaf spring releases the latch; PLA | [SNIP] https://www.printables.com/model/51817-pokeball-ring-stand |
| Geocache box servo latch | SG90/MG90 **cam pushes a spring-returned latch lever**; in the latched position the cam does not touch the lever, so the latch can still be pushed aside from outside (manual override). Cam and latch printed at ≥ 75 % infill | [SNIP] https://www.stlfinder.com/model/servo-latch-geocache-box-servo-latch-FJzqm6RA/4700264 |
| Arduino forum thread | Servo pulls a locking pin through a wire link so the pin can retract independently of the servo; angled pin that the closing lid pushes aside, returned by spring or magnet; a small servo draws only milliamps when not holding load; power both needed to lock and unlock unless the latch is spring-loaded | [S1] https://forum.arduino.cc/t/design-question-best-way-to-lock-and-unlock-a-lid-box-3d-printed/657878 |
| Printable latch mechanisms | Spring-loaded latch whose spring is at rest when latched and only loaded while being pushed in | [SNIP] https://www.printables.com/model/130253-spring-loaded-latching-mechanism , https://www.printables.com/model/950899-automatic-latching-mechanism-for-opening-lids-heav |

No formal design guide for servo-released latches was found; the practices below are engineering inference consistent with those examples.

### 7.2 Practices and numbers [INF]

- **Latch at the front, opposite the hinge.** Latch force = (spring torque ∓ lid gravity torque) / 100 mm: ≈ **0.15–0.4 N upright**, up to ≈ 0.7 N when the ball is held upside-down and gravity adds to the spring. With the +20 % spring tolerance, **design for 1 N**. Placing the latch near the hinge multiplies the force by the lever ratio.
- **Load path perpendicular to the release motion.** The pawl or bolt takes the lid force in shear/compression against a fixed strike; the servo only slides or rotates it sideways. Release force is then friction only: µ ≈ 0.3 × 1 N ≈ 0.3 N.
- **Servo margin:** SG90 stall torque is quoted as 1.8 kgf·cm in most copies of the datasheet and 1.2 kgf·cm (4.8 V) on a TowerPro-branded sheet [V2+ that the range is 1.2–1.8; sources disagree on the value] — e.g. https://tams.informatik.uni-hamburg.de/lehre/2023ss/vorlesung/es/doc/sg90.pdf . At a 10 mm horn radius that is 12–18 N, i.e. about 40× the release force. Speed ≈ 0.1–0.12 s per 60°.
- **Rotating pawl versus sliding bolt.** A pawl on a pin is preferable in print: one pivot with a steel pin, no long sliding surfaces to bind after weeks of preload or a little warping. Give the hook face a neutral to slightly positive angle (0–5° undercut) so the lid force neither back-drives the pawl open nor wedges it; a sliding bolt needs 0.2–0.25 mm per-side guides and is more sensitive to dirt and creep.
- **Lost motion between servo and pawl** (slot, pushrod with free travel, or cam that stands clear when latched): the pawl can snap over on closing without back-driving the servo, a drop does not hammer the servo gears, and the servo can be unpowered while latched.
- **Closing ramp:** 30–45° lead-in on pawl and strike so pushing the lid down snaps it shut; pawl return spring ≈ 0.2–0.5 N at the hook (a pen-type compression spring or a printed PETG leaf).
- **Engagement and travel:** hook overlap 1.5–2.0 mm; release travel = overlap + 1 mm ≈ **2.5–3 mm**; with a 10 mm horn that is ≈ 15–20° of servo rotation.
- **Hard stop at closed** so the latch is not what defines the seam gap, and a mechanical or hidden manual release in case electronics fail on the day.

### 7.3 End stop and damping for the sprung lid

| Option | Data | Source |
| --- | --- | --- |
| 3M Bumpon SJ5302, clear polyurethane hemisphere, self-adhesive | Ø7.9 mm × 2.2 mm | [V2+] https://multimedia.3m.com/mws/media/175691O/3mtm-bumpontm-protective-products.pdf , https://ie.farnell.com/3m/sj5302trans/feet-polyurethane-2-2x7-9mm-pk144/dp/1165067 |
| 3M Bumpon SJ5303 | Ø11.1 mm × 5.0 mm | [SNIP] Mouser catalogue |
| Soft-close lid hinges with rotary damper (Häfele, Sugatsune HG-JH) | exist, but furniture-sized | [SNIP] https://www.sugatsune.com/product/soft-close-dampening-hinge/ |

Energy to absorb is only 0.02–0.05 J (section 2.1), so a 2 mm polyurethane or silicone bumper on the hinge-side stop, or an O-ring on a stop pin, is sufficient; the lid will bounce once or twice. A grease-damped hinge pin (damping grease in the knuckles) slows the opening if the "jump" turns out too violent — not sourced, try on the prototype. No miniature rotary damper of suitable size was identified.

---

## 8. Speaker grille and enclosure

### 8.1 Open area and geometry

| Guidance | Value | Status / source |
| --- | --- | --- |
| Minimum open area of the outlet, relative to diaphragm area | **≥ 20 %** to avoid noticeable loss | [V2+] https://www.digikey.com/en/articles/why-rear-enclosures-are-crucial-for-miniature-speakers , https://www.electronicspecifier.com/blog/how-to-design-with-mini-speakers-for-the-best-sound-and-reliability , Same Sky guide [SNIP] |
| Preferred open area | **40 % or more** (DigiKey); 40–60 % "more optimal" (Same Sky/CUI) | [V2+] DigiKey; https://sameskydevices.com/blog/how-to-design-a-micro-speaker-enclosure [SNIP, page 403] |
| Hi-fi forum opinion | never below 50 %; commercial perforated grilles span 25–65 % | [SNIP] diyaudio, https://www.prosoundtraining.com/?p=9962 |
| Extent of the hole pattern | about the same size and shape as the cone | [S1] Electronic Specifier |
| Gap cone → grille | **1–2 mm** | [V2+] Electronic Specifier, Same Sky [SNIP] |
| Rear and front must be sealed from each other | gasket, tight frame seat or adhesive; leaks cut output and change the response | [V2+] DigiKey, Electronic Specifier |

Worked numbers [INF]:

| Speaker | Approx. cone Ø / area | 20 % | 40 % | Example slot set for ≈ 40 % |
| --- | --- | --- | --- | --- |
| 28 mm | 24 mm / 450 mm² | 90 mm² | 180 mm² | 8 slots 1.5 × 15 mm |
| 40 mm | 34 mm / 910 mm² | 180 mm² | 365 mm² | 12 slots 1.5 × 20 mm |

Slot width versus printability and dust [INF]: with a 0.4 mm nozzle keep slots **≥ 1.2 mm, preferably 1.5 mm** wide and the bars between them ≥ 1.2 mm (three extrusion lines); narrower slots close up or string, especially in PETG. Slots up to ≈ 1.5 mm keep fingers and most debris out; back them with acoustic mesh or thin speaker cloth for dust. On the lower hemisphere, orient slots so they print as vertical walls rather than as bridges, or accept ≤ 5 mm bridges.

### 8.2 Front chamber and duct effects on speech

The cavity between cone and grille plus the grille openings form a Helmholtz resonator, f0 = (c / 2π)·√(S / (V·(l + 1.7·r))), with S opening area, V front volume, l opening depth, r opening radius. A smaller front volume and a larger, shorter opening push the resonance up; the front-chamber resonance produces a mid-frequency peak and tube resonance a high-frequency peak; front volume and porting control the high-frequency end of the response [SNIP: patents, https://www.mdpi.com/2076-3417/13/2/1018 , https://comsol.fr/paper/download/678001/sinelnikov_paper.pdf ].

Applied here [INF], front cavity 2 mm deep, wall 2.2 mm, 1.5 mm slots:

| Speaker | Open area | Resonance |
| --- | --- | --- |
| 40 mm | 40 mm² (4 %) | ≈ 3.7 kHz — inside the speech band; honky, coloured |
| 40 mm | 180 mm² (20 %) | ≈ 7.8 kHz |
| 40 mm | 360 mm² (40 %) | ≈ 11 kHz |
| 28 mm | 25 mm² (6 %) | ≈ 4.2 kHz |
| 28 mm | 90 mm² (20 %) | ≈ 7.9 kHz |
| 28 mm | 180 mm² (40 %) | ≈ 11 kHz |

Speech intelligibility lives mainly in 300 Hz–4 kHz. Keeping the open area at ≥ 20 % with a ≤ 2 mm front gap puts the resonance above that band; a few small holes or a long duct pulls it into the band and makes speech boxy. Avoid ducting the sound around a corner; if the speaker cannot face the grille directly, keep the duct short, wide, and of constant cross-section.

### 8.3 Sealed back volume

| Guidance | Status / source |
| --- | --- |
| Use the volume on the speaker datasheet (given in cc as a test condition); ±10 % is acceptable. If none is stated the speaker does not strictly need one | [S1] DigiKey |
| Starting point without a datasheet figure: rear cavity depth ≈ speaker diameter; if depth is short, extend the area behind the speaker | [S1] Electronic Specifier |
| Alternative rule: rear volume ≈ 3 × the physical volume of the speaker | [SNIP] https://www.mouser.lt/pdfDocs/New-Speakers_How-to-Improve-Performance.pdf (timeout) |
| Airtight; rigid walls so they do not radiate; absorbent lining helps and stuffing can act like 15–25 % more volume | [S1] DigiKey, Electronic Specifier; stuffing figure [SNIP] |

Rough targets [INF]: 28 mm speaker ≈ 15–20 cm³; 40 mm speaker ≈ 40–50 cm³ (depth ≈ diameter over the speaker footprint). The base hemisphere of a 100 mm ball holds ≈ 230 cm³ inside a 2.2 mm wall, so this is affordable if a sealed pocket is planned from the start. Printed walls leak at layer lines and seams: ≥ 3 perimeters, a gasket or bead of sealant at the joint, and cable exits sealed with hot glue. No Thiele–Small based sizing was done because no speaker has been selected.

---

## 9. Recommended hardware list

| # | Item | Article / spec | Qty | Supplier | Note |
| --- | --- | --- | --- | --- | --- |
| 1 | Torsion spring, primary | **Gutekunst T-18460L and T-18460R** — 0.8 mm 1.4310, Di 7.2 / De 8.8, 6.5 coils, free α 180°, Mn 61.92 N·mm, αn 155.9° | 2 + 2 | federnshop.com | 51.6 N·mm at 130° (83 % Mn), 7.9 N·mm at 20°. Use one; second hand lets the spring sit on either side. 3.43 € each at 3+ |
| 2 | Torsion spring, softer alternative | **Gutekunst T-16324L / R** — 0.7 mm, Di 5.3 / De 6.7, 7 coils, α 0°, Mn 41.48, αn 143.9° | 2 | federnshop.com | 31.7 N·mm at 110°; keep ≤ 115° for long preload |
| 3 | Torsion spring pair | **Gutekunst T-16244L + T-16244R** — 0.63 mm, Di 5.37 / De 6.63, 7 coils, α 0°, Mn 30.87 each, αn 163.5° | 2 + 2 | federnshop.com | Symmetric pair, 49 N·mm at 130° at 79 % Mn; remove one to halve the force |
| 4 | Torsion springs for a 90°-drive layout | **T-18459L/R** (α 90°) or **T-18436L/R** (α 270°) | 2 | federnshop.com | Only if CAD ends up with layout A or B in 2.1 |
| 5 | Compression springs | **Gutekunst VD-051B** (0.4 × 4.4 × 25.1, 0.28 N/mm) and **VD-045** (0.4 × 5.4 × 23.7, 0.21 N/mm) | 2 each | federnshop.com | Plunger fallback, pawl return, button return |
| 6 | Hinge pin | ISO 2338 A2 **Ø3 m6 × 30/32/36**, or Ø3 h9 1.4301 bar cut to length | 2 + 0.5 m | Keller & Kalmbach, ehorst, metal dealers | Ø3 preferred over Ø2: stiffer, standard lengths exist |
| 7 | Small pins | Ø2 h9 1.4301 bar | 0.5 m | metal dealers | Pawl pivot, keeper pin; cut and chamfer |
| 8 | Heat-set inserts | ruthex **RX-M3x5.7** and **RX-M2x4** (or CNC Kitchen M3 standard/short, M2 standard) | 1 pack each | 3DJake, ruthex, Prusa | Holes Ø4.0 and Ø3.2 |
| 9 | Screws | ISO 4762 A2 M3 × 6/8/10, M2 × 5/6/8; ISO 7380-1 M3 where a low head is needed | assortment | any | Heads: M3 Ø5.5 × 3.0, M2 Ø3.8 × 2.0 |
| 10 | Self-tapping screws (not used since revision 6: hard to get in Germany; M2 machine screws take their place) | Ø2.2 and Ø2.6 for plastic (or Bambu BT2 / BT2.5) | few | Bambu store, hardware dealers | Holes 1.8 / 2.1–2.2 mm |
| 11 | Bumpers | 3M Bumpon **SJ5302** (Ø7.9 × 2.2) | 1 card | Farnell, RS | Lid end stop, feet |
| 12 | Magnets (detents only) | supermagnete **S-06-02-N** (6 × 2, N45, ≈ 7.3 N) and **S-05-02-N52N** | 10 each | supermagnete.de | Not at the main latch |
| 13 | NFC ferrite | Würth **364005** (60 × 60 × 0.2 mm) or **364006** (0.3 mm) | 1–2 | Würth, RS, Mouser | 364 family only |
| 14 | Filament | PETG for load-bearing parts; shell material per 5.7; clear PETG for light windows; TPU 95A for ring liner | — | — | — |

L and R are separate articles for the quantity price. Items 1–3 in the quantities listed come to about 36 € (ten springs at 3.60 € each) plus shipping, VAT status unverified, and cover layouts C and D in 2.1; add item 4 for layouts A or B. Ordering everything in one go is cheaper than a second shipment.

---

## 10. Rejected / not chosen candidates

| Candidate | Why not |
| --- | --- |
| Gutekunst **T-18435** (0.8 mm, Di 6.0, α 180°, αn 130.5°) | Exactly at its limit at 130° — no margin for weeks of preload or the ±20 % tolerance |
| Gutekunst **T-16243** (0.63 mm, α 270°, αn 134°) | 97 % of Mn at 130° |
| Gutekunst **T-18486 / T-18487** (0.8 mm, Di 9.2) | Good margin (55–66 % Mn) but De 10.8 mm exceeds the 9 mm envelope |
| Gutekunst 1.0 mm wire (T-185xx, Mn ≈ 115–119 N·mm) | 68–119 N·mm at 130° — four to seven times the lid's gravity torque; violent opening, high latch and hinge loads |
| Gutekunst 0.5 mm wire (T-161xx, Mn ≈ 15–16 N·mm) | Below the lid's own gravity torque |
| All stock springs with ≤ 5 coils in 0.7–0.8 mm | Permissible angle 30–100°, cannot reach 110–130° |
| Bambu 0.8 × 5 × 3 torsion spring | Estimated permissible angle ≈ 35° |
| Generic Amazon / AliExpress / eBay assortments | No torque, angle, tolerance or material data; most have 3–6 coils. Fine for mock-ups only |
| Febrotec, Lesjöfors, Hennlich, MISUMI torsion springs | Not rejected on merit — data could not be retrieved; unverified |
| Ø2 mm ISO 2338 dowel pin as the main hinge pin | 30–40 mm lengths probably outside the standard range; about one fifth of the bending stiffness of Ø3 |
| M3 screw as the hinge pin | Thread inside printed knuckles wears and rattles; acceptable only with the knuckles on the plain shank |
| ISO 7379 shoulder screws | Smallest standard shoulder 6.5 mm / M5 — too big |
| Würth WE-FSFS **354 / 374** families | µ″ ≈ 90 at 13.56 MHz — lossy, wrong for NFC |
| Magnet as primary lid closure | Fights the opening spring with a 100 mm lever; force varies steeply with gap |
| Foam or velvet slit as the only ring retention | Friction hold; estimated drop load 15–60 N |
| PLA for hinge, latch and spring seats | Worst creep of the common filaments; softens at 55–60 °C |
| Inlaid black band printed with the shells | ≈ 100 extra filament changes including black→white, bleed risk on the most visible line |
| Printing the dome rim-up (bowl orientation) | Supports on the visible outer surface |
| Furniture soft-close hinges / rotary dampers | Far too large |

---

## 11. Open risks and unverified items

**Must be resolved before CAD freeze**

1. **The ring has not been measured.** Band width 2.5 mm is an interpretation of "diameter 2.5 mm"; band thickness, setting height and head width are assumed ranges. Setting-height figures are snippet-level only.
2. **Gutekunst leg-angle convention** was derived from the datasheet drawing and coil counts, not from a written definition. Check the STEP model of the chosen article.
3. **Hinge layout decides the spring.** The four layouts in 2.1 need different free angles; the springs are not interchangeable between layouts.
4. **Spring torque tolerance ±20 %** and leg-bending compliance (6–18 %) both move the real torque; prototype with the actual spring before fixing latch geometry.
5. **Lid momentum can roll the ball.** ≈ 0.003–0.004 kg·m²/s of angular momentum stops against the end stop within milliseconds; an unrestrained 100 mm ball will rock or roll backwards and could throw the ring side toward the floor. Needs a flat or weighted base, a stand, or a softer opening. Calculated, not sourced.
6. **Drop load on the ring holder (15–60 N)** is an order-of-magnitude estimate; the lock needs a physical drop test with a dummy ring.

**Unverified numbers used above**

- EN 13906-3 stress correction q and σ_zul = 0.7·Rm — from memory; consistent with catalogue back-calculation but not read from the standard.
- ISO 2338 length ranges per diameter and ISO 286 tolerance values — from memory.
- ISO 273 clearance holes; hex key sizes for M2 / M2.5 button heads — from memory.
- M2 / M2.5 button-head diameters — vendor data, and vendors disagree (M2.5: 4.5 versus 4.7 mm).
- Gutekunst prices: VAT and shipping status not shown on the pages read.
- Pen-spring dimensions and rate — inferred from similar catalogue springs; no measurement found.
- Contents of Amazon.de / AliExpress assortments — inferred from eBay and reseller listings; Amazon itself not readable.
- Bambu flush volumes per colour change — not read; the Bambu wiki page returned HTTP 402.
- Magnet force through a plastic gap; the plain N40/N45 5 × 2 mm value.
- Same Sky/CUI grille guidance (40–60 %) and the "3 × speaker volume" rule — snippets only.
- Car-interior temperatures — snippets only.
- "≤ 80–85 % of Mn for long preload" and relaxation of 1.4310 over weeks — engineering practice, not sourced.
- ASA heat deflection — from a non-Prusament datasheet; no ASA creep data found at all.

**Recorded disagreements between sources**

| Topic | Disagreement |
| --- | --- |
| Ring size 49 | ISO/Wikipedia/Baur 15.6 mm versus Swarovski chart (snippet) 15.3 mm |
| 1 ct round diamond | 6.3 mm (Brilliant Earth) versus 6.5 mm (Whiteflash) |
| Press-fit allowance | 0 to −0.05 mm (Snapmaker) versus +0.05 to +0.15 mm per side (Sovol) versus −0.05 to −0.15 mm (QIDI) |
| Insert hole chamfer | none (CNC Kitchen) versus 0.3–0.5 mm (EPFL) |
| Insert hole depth | +1 mm (CNC Kitchen, EPFL) versus +50 % of length (Hackaday) |
| PETG creep | better than PLA (Dogan 2022 for co-polyester; forum consensus) versus "avoid PETG" (kanrog.com, unsourced) |
| SG90 stall torque | 1.8 kgf·cm (generic sheets) versus 1.2 kgf·cm at 4.8 V (TowerPro sheet) |
| 6 × 2 mm N45 magnet | 740 g (supermagnete) versus 644 g (eBay seller) |
| Würth 364003 | 120 × 120 × 0.3 mm (Würth) versus 60 × 60 × 0.2 mm (an RS listing) |
| Grille open area | ≥ 20 % / ≥ 40 % (component vendors) versus ≥ 50 % (hi-fi forum) |

**Sources that could not be opened** (HTTP 403/402/429/timeout): supermagnete S-05-02-N plain variant (served the N52 page), Same Sky/CUI enclosure guide, Mouser PDFs, Bambu wiki and EU store, eBay listings, PriceScope, Printables, Accu, ruthex.de, cnckitchen.store, MyTechFun, Fabbaloo. DuckDuckGo's HTML endpoint returned a bot challenge, so the German-language fallback search was not available.
