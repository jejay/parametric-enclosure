# 10 — Tall-grass look, printing rules for the grass base, small standard parts

Access date for all web sources: **2026-11-17**.

Evidence tags:

| Tag | Meaning |
| --- | --- |
| **[V2+]** | VERIFIED: two or more independent sources agree (or one source plus an independent drawing/calculation that reproduces it) |
| **[S1]** | Single source, read directly (PDF or page; pages read through the fetch tool arrive as an extract, not the raw page) |
| **[SNIP]** | Only seen as a search-result summary; page itself not opened or not reachable |
| **[MEAS]** | Measured by me on the stored pictures (Pillow), method in `reference_images/tall_grass/SOURCES.md` |
| **[INF]** | Inferred or calculated from sourced inputs — check before committing to CAD |
| **[MEM]** | From memory, not verified this session |

Material kept with this note (third-party, untrusted, read only):

- `research/reference_images/tall_grass/` — ten reference pictures `G01`…`G10` and `SOURCES.md` (file → URL, copyright note)
- `research/downloads/grass_base/` — one folder per file: `jst_ph/ePH.pdf`, `jst_sh/eSH.pdf`, `molex_51021_sd/510210600_sd.pdf`, `molex_51047_sd/510470600_sd.pdf`, `rs_doc_c439/` (Molex PicoBlade wire-to-wire product specification), `rs_doc_2f2c/` (Molex part page 51047-1000), `szlcsc_molex_94f7/` (Molex cable assembly 218112-0600 part page), `szlcsc_ph20_a/` (Xyeconn drawing of a PH-type housing), `boellhoff_iso10642/`, `boellhoff_din7991/`, `boellhoff_din7982/`, `prusament_petg_tds/`, `bambu_petg_hf_tds/`, `polymaker_polylite_petg_tds/`, `prusaslicer_printconfig/PrintConfig.cpp` (tag `version_2.8.1`), `bambustudio_printconfig/PrintConfig.cpp` (branch `master` on the access date)
- Already in the repo and only read: `research/downloads/mcu_audio/ti_drv5032.pdf` (TI SLVSDC7H)

---

## Part A — How "tall grass" is drawn

### A.1 Per source: tuft, proportion, arrangement

`G..` = stored picture. Proportions are of what is visible in the picture. "By eye" means read off an enlarged, gridded view, not fitted.

| id | source | tuft / blade shape | height : width | arrangement |
| --- | --- | --- | --- | --- |
| G01 | Red/Blue/Yellow tile, Game Boy | 8 × 8 px tuft: two pointed, straight blades in a lopsided V (right blade 8 px tall, left 6 px, each 2–3 px wide) joined at the base, plus one small fleck low on the left [MEAS] | tuft 1 : 1 | four identical tufts per 16 px tile (2 × 2), tiles tile seamlessly; on Route 1, 104 of 648 map cells are grass, in rectangular blocks 8 × 4, 4 × 4, 4 × 4, two stair-stepped pairs of 4 × 2, and 2 × 4 [MEAS on the Gen I and Gen II Route 1 maps] |
| G02 | Gold/Silver/Crystal Route 1 map, Game Boy Color | 7 × 7 px tuft in an 8 px cell: two leaf-shaped blades (3 px wide, pointed, one light pixel inside each) forming a V, merging into a 2 px base with flecks left and right [MEAS] | tuft 1 : 1 | as G01: 2 × 2 tufts per tile, rectangular blocks, straight block edges |
| G03 | Platinum screenshot, DS | one symmetric tuft per tile, 16 × 13 px, five to six pointed leaves in two tiers: a tall centre leaf flanked by two shorter ones, two broader leaves spreading below, one short leaf at the bottom [MEAS on the tile rips `Pt_Grass.png`, `DP_Grass.png`] | tuft 0.8 : 1 | strict grid, pitch 16–17 px across and 15 px down [MEAS, autocorrelation]; rows stay separate, the pale ground shows between them; one rectangular patch of about 9 × 9 tiles [by eye]; the character is hidden to the waist |
| G04 | X/Y screenshot, 3DS | one rosette per tile: 8–10 pointed, slightly curved leaves around a dark centre [by eye]; the isolated render (`XYORAS_Grass.png`) is 60 × 41 px | tuft 0.68 : 1 (seen from above at an angle) | still a grid: pitch 30–35 px across, about 20 px down in the 400 × 240 screenshot [MEAS]; one dense rectangular patch whose outline is a row of leaf tips |
| G05 | Let's Go render, Switch | about 20 visible blades in 4–5 clumps; every blade is broad, flat and lance-shaped: straight edges tapering to a sharp point, widest in the lower third, with a centre crease (two facets) and a thin lighter rim; a clump is 4–6 blades fanned about ±25–30° [by eye] | blade 3–4.5 : 1 [by eye]; whole tile 0.73 : 1 [MEAS, 1259 × 917 px]; one clump about 1–1.3 : 1 [by eye] | in the game (screenshot looked at, not stored): rectangular patches with straight edges, clumps in rows, about knee- to hip-high next to the player character [by eye] |
| G06 | Sword/Shield screenshot, Switch | no separate tufts: a dense brush of thin, straight, needle-like blades, bundled into small V's [by eye] | blade about 10–15 : 1 [by eye] | no grid; rounded patches with a sharp outline, about half the trainer's height; a vertical colour gradient (teal base, yellow-green tips) |
| G07 | Scarlet/Violet store screenshot, Switch | flat, narrow, straight-edged triangles ("spikes"), semi-transparent, standing singly or in loose groups of 2–4 that lean in different directions [by eye] | blade about 5–6 : 1 [by eye] | no grid, open fields with soft edges |
| G08 | Pokémon GO menu icon | flat silhouette of one tuft: 9–10 thin, sabre-shaped blades that curve outward and taper to points, the middle ones tallest [by eye] | tuft 1 : 1 [MEAS, 110 × 109 px]; blade about 12–15 : 1 [by eye] | a single tuft, used as a pictogram |
| G09 | animation frame, 2022 | long lance-shaped blades that arch over, overlapping in depth; a few backlit blades are pale [by eye] | blade 8 : 1 or more (cut off by the frame) | irregular, no grid; reaches the chest of a crouching child |
| G10 | trading card "Poké Kid", 2020 | painted, wind-blown blades, long, thin and curved, as brush strokes [by eye] | blade 10 : 1 or more | dense, irregular, diagonal |

Looked at but not stored (URLs in `SOURCES.md`): the Gen III tile is a bushy star of pointed leaves, the HeartGold/SoulSilver and Black/White tiles are round bushes of many small leaves (one per tile); the Sun/Moon render is an upright clump of thin blades (44 × 55 px, 1.25 : 1); a second Pokémon GO asset is a white crown-shaped silhouette with 7–9 points (54 × 40 px); the Sword/Shield town map marks grass with small crown-shaped pictograms; the 2026 *Pokopia* item sprite "Tall grass" is a low dome of many short pointed leaves (81 × 59 px); TV-anime frames from 1997–2000 show dark blue-green, sword-like blades with a light centre stripe. A Spanish fan wiki notes that in the TV anime tall grass "as such does not exist" as a mechanic; grass with small Pokémon in it appears mainly in episode 1 [S1] https://www.wikidex.net/wiki/Hierba_alta .

The two Game Boy tufts, pixel for pixel (`#` dark, `+` middle, `-` light, `.` empty) [MEAS]:

```
Red/Blue/Yellow (8 x 8)      Gold/Silver/Crystal, Kanto tile (8 x 8)
......#+                     ........
.....#-#                     .#...#..
##..#++#                     #-#.#-#.
#-#.#+#+                     #++#++#.
#-+####.                     .#++#+#.
.#-+##+.                     +#++#+#+
++#+##..                     ++#+##++
.++##+..                     .++##++.
```

### A.2 Colours measured from the pictures

Pixel art: exact palette entries. Everything else: k-means cluster centres (dark / middle / light) of the green pixels inside hand-picked boxes; the share of each cluster is in brackets. All [MEAS]; screenshots and scans carry lighting, bloom and JPEG error, so read the 3D values as ±10 per channel.

| id | source | main green | dark green | highlight | remark |
| --- | --- | --- | --- | --- | --- |
| G01 | Red/Blue/Yellow tile | — | — | — | grey-scale rip: #808080, #C0C7C0, #FFF8FF; no green information |
| G02 | Gold/Silver/Crystal | #63CE08 (33 %) | #297300 (31 %) | #B5FF52 (36 %) | exact palette of a grass block; the light colour is also the ground between the tufts |
| G03 | Platinum | #28AC00 / #30BC08 | #188428 | #58CC20 / #68DC38 | exact palette; the ground between rows is #50FC90 |
| G04 | X/Y | #41B328 (43 %) | #17860F (26 %) | #69DB4A (32 %) | |
| G05 | Let's Go | #0E9B51 (44 %) | #1C6343 (32 %) | #42BE57 (24 %) | mean of all opaque pixels #1F914E |
| G06 | Sword/Shield | #76D76E (34 %) | #3AA968 (24 %) | #ACF877 (42 %) | gradient base → tip; mean #7EDA70 |
| G07 | Scarlet/Violet | #54AF6F (47 %) | #246247 (23 %) | #78CD8B (30 %) | foreground blades alone: #49A866, #3A6E5B, #5FBC78 |
| G08 | Pokémon GO icon | #86D728 | — | — | one flat colour with an alpha gradient |
| G09 | animation frame 2022 | #327748 (41 %) | #144828 (44 %) | #5EB072 (16 %) | |
| G10 | trading card | #427341 (44 %) | #264929 (14 %) | #6A8A50 (42 %) | olive, painted |

Tile rips of the other generations, exact palettes, dark → light [MEAS on the not-stored Bulbapedia files]: Ruby/Sapphire/Emerald #385000, #18A068, #70C0A0, #A0D0C0 · FireRed/LeafGreen #385810, #389030, #40B088, #70C8A0, #A0E0C0 · Diamond/Pearl #187030, #189000, #28B000, #60D030 · HeartGold/SoulSilver #106040 … #50C078 (most pixels #207050, #288850, #389858) · Black/White (spring) about #326731, #369045, #6EBC57.

Reading the table: the games keep one recipe for 25 years — a **saturated mid green** (#28AC00 … #41B328 … #0E9B51), a **dark green that leans to teal** in the 3D games (#1C6343, #246247; pure dark green #17860F–#297300 in the 2D games) and a **yellow-green highlight** (#58CC20 … #69DB4A … #ACF877; the lime of the Game Boy Color tile, #63CE08, and of the Pokémon GO icon, #86D728, sits in the same range). Olive and grey-green only occur in painted art (G10).

### A.3 What changed over time

1. **Tile era, 1996–2012 (G01–G03):** countable tufts on a strict square grid, in rectangular blocks with straight edges. Generations I–II draw four small two-blade V tufts per tile; generations III–V draw one rosette or bush per tile.
2. **Clump era, 2013–2018 (G04, G05):** one 3D clump of broad pointed leaves per grid cell; still rectangular patches. Let's Go is the clearest model: few, large, flat, lance-shaped blades.
3. **Field era, 2019– (G06, G07):** dense fields of thin blades without a grid, shaded by a colour gradient.
4. Icons and illustration (G08–G10) use thin curved blades and no pattern.

### A.4 Recommendation

**Stylisation for blades 8–20 mm tall** [INF from A.1–A.3 and Part B.1]: build the **Let's Go clump (G05) on the tile-era grid** — per tuft 4–6 broad, flat, lance-shaped blades with straight edges and a pointed (blunted) tip, length : width 3–4 : 1, fanned ±25°, the middle blades tallest; tufts in straight rows at a pitch equal to the tuft width; the patch outline straight or following the plate edge. Reasons:

- It is the 3D form of what the 2D games showed for twenty years: a few large leaves per tuft, repeated on a grid. The repetition and the straight patch edge are what separate "tall grass" from a lawn.
- Broad flat blades are the only variant a 0.4 mm nozzle prints at this size: a 16 mm blade is 4–5 mm wide and can be 2.4–3 mm thick at the root (B.1). The needle styles (G06, G08, G09: 10–15 : 1) would be 1–1.6 mm wide at 16 mm height — fragile in PETG and not distinctive.
- For a flat mark (the two-colour inlay of B.2) the Generation II V tuft above is the clearest pictogram: two leaves and a base, readable at 8 px.

**Colour:** two greens — a saturated mid green for the blades and a darker, slightly teal green for the plate (or the reverse for the inlaid disc). Nominal hex codes of filaments against the measured game colours, as CIE76 colour difference ΔE*ab averaged over the generations in A.2 (smaller is closer; below about 25 the colours read as the same family) [INF, calculated from the makers' hex codes]:

| PETG filament (maker's hex) | as main green | as dark green | as highlight | source of the hex |
| --- | --- | --- | --- | --- |
| Bambu Lab PETG HF **Green** (#00AE42) | **24** (X/Y 14, Let's Go 18, Platinum 23) | 36 | 28 | [S1] a retailer's copy of Bambu's "PETG HF Hex Code Table", https://www.gigaparts.com/bambu-lab-petg-hf-3d-printer-filament.html ; the same values in a second retailer's listing [SNIP] |
| Bambu Lab PETG HF **Lime Green** (#6EE53C) | 26 (Gold/Silver 9, GO icon 13, Platinum 15) | 61 | **22** (Platinum 4, X/Y 10) | same |
| Bambu Lab PETG HF **Forest Green** (#39541A) | 56 | 29 (olive, darker than the games) | 64 | same |
| Prusament PETG **Jungle Green** (#007248, HueForge TD 0.5) | 49 | **23** (Let's Go 10, Scarlet/Violet 14) | 57 | [S1] https://help.prusa3d.com/article/hueforge-filament-transparency-values-and-hexcodes_762314 |
| Prusament PETG Pistachio Green (#93A682, TD 0.9) | 55 | 41 | 56 | same; a grey sage, not a game colour |
| Prusament PETG Neon Green Transparent (#A6EC5E, TD 75) | 28 | 56 | 20 | same; transparent, unsuitable for an opaque inlay |

So: **Bambu PETG HF Green** for the main green, **Bambu PETG HF Lime Green** for highlights or the lighter disc, **Prusament PETG Jungle Green** (or Bambu PETG HF Forest Green if one brand is wanted) for the dark green. Other PETG greens that are sold in the EU but for which no hex code was found: eSUN "PETG Green" and "PETG Solid Green", SUNLU "PETG Green", Elegoo "PETG Green", Polymaker "PolyLite PETG Green" and "Dark Green", AzureFilm "PETG Hyper Speed Grass Green" [SNIP] https://www.3djake.com/3d-printer-filaments/petg-green-1 . Hex codes are nominal; a printed surface looks darker and, for translucent PETG, depends on what lies beneath (B.2).

---

## Part B — Printing rules (PETG, 0.4 mm nozzle)

### B.1 Thin upright features: what prints and what survives

**What the slicer will print**

| Rule | Value at a 0.4 mm nozzle | Status / source |
| --- | --- | --- |
| Arachne "minimum feature size": thinner model features "will not be printed" | 25 % of the nozzle = **0.10 mm** (default) | [V2+] the same default in PrusaSlicer 2.8.1 and Bambu Studio: `downloads/grass_base/prusaslicer_printconfig/PrintConfig.cpp` (`min_feature_size`), `…/bambustudio_printconfig/PrintConfig.cpp` |
| Arachne "minimum perimeter / wall width": features between the two limits are "widened" to it | 85 % of the nozzle = **0.34 mm** (default) | [V2+] same two files (`min_bead_width`) |
| Consequence for a blade tip | a tip never comes out sharper than one bead (about 0.34–0.45 mm); anything modelled finer is widened or dropped | [INF] |
| Classic perimeter generator | walls thinner than one extrusion width "will likely still be ignored" [SNIP] https://help.prusa3d.com/article/layers-and-perimeters_1748 ; with Arachne "detect thin walls" is disabled because Arachne adapts the extrusion width itself | [S1] https://help.prusa3d.com/article/arachne-perimeter-generator_352769 |
| Small vertical pins | "smaller diameter pins (less than 5 mm diameter) can be made up of only perimeter prints with no infill" — weak | [S1] https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/ |
| Generic FDM minimums from design guides | walls 2 × nozzle Ø up to 1 mm; protruding features 2 mm; pins 1.5–3 mm Ø | [SNIP] FACFOX, Core77, a University of Zurich guideline, a University of Cincinnati lab page — vendor and teaching material, the numbers differ |
| PETG in particular | Prusa lists as cons: "possibility of stringing", "poor bridging and overhangs", "not great for printing detailed parts"; the Prusament data sheet says "not suitable for tiny parts" | [V2+ within one maker] https://help.prusa3d.com/article/petg_2059 , `downloads/grass_base/prusament_petg_tds/PETG_TechSheet_ENG.pdf` |
| Cooling trade-off | cooling "helps to keep the model detailed and prevents stringing", but "if you want the model to be as tough as possible, try to turn off the print fan"; otherwise fan at half power after the first layers | [S1] Prusa PETG article |

Working values [INF]: no wall of a blade under **0.9 mm** (two beads), **1.2–1.6 mm** where it has to survive handling; tip modelled as a flat or round end **≥ 1.2 mm wide and ≥ 0.9 mm thick** (blunt, also so that it does not prick a finger); a root fillet of ≥ 1 mm. Print several tufts in one job or raise the minimum layer time so that the tips cool between layers [MEM].

**Strength across the layers (Z) compared with in the layer plane (XY)**

| Source | XY tensile | Z tensile | Z / XY | What else changes in Z | Print settings of the specimens |
| --- | --- | --- | --- | --- | --- |
| Prusament PETG data sheet [S1] | 47 ± 2 MPa (flat), 50 ± 1 (on edge), yield | 30 ± 5 MPa | 0.60–0.64 | elongation at yield 5.1 % → 2.5 %; Charpy unnotched "no break" → 5 ± 1 kJ/m² | 0.2 mm layers, 260 °C, 100 % infill, i3 MK3 |
| Bambu PETG HF data sheet V1.0 [S1, retailer copy] | 34 ± 4 MPa | 23 ± 4 MPa | 0.68 | bending strength 64 ± 3 → 48 ± 4 MPa (0.75); elongation at break 8.6 % → 5.1 %; impact 31.5 → 10.6 kJ/m² | 255 °C, 200 mm/s, 100 % infill, annealed 8 h at 75 °C |
| Polymaker PolyLite PETG data sheet V5.2 [S1] | 31.9 ± 1.1 MPa | 13.4 ± 2.0 MPa | 0.42 | elongation at break 6.8 % → 1.3 % | 240 °C, fan off, 100 % infill |
| Polymaker wiki, current sheet [S1, fetch extract] | 50.8 ± 0.9 MPa | 42.8 ± 2.8 MPa | 0.84 | elongation at break 8.4 % → 3.3 % | 240 °C, fan off |
| CNC Kitchen hook test, Prusament PETG [S1, fetch extract] | 55 kg (lying) | 25 kg (standing) | 0.46 | — | 250 °C, fan 30–50 % |

Sources: `downloads/grass_base/prusament_petg_tds/`, `…/bambu_petg_hf_tds/` (from https://botland.com.pl/img/art/inne/25540_karta_produktu.pdf), `…/polymaker_polylite_petg_tds/` (https://cdn.shopify.com/s/files/1/0789/2979/files/PolyLite_PETG_TDS_V5.2.pdf), https://wiki.polymaker.com/polymaker-products/more-about-our-products/documents/technical-data-sheets/petg-pet/polylite-tm-petg , https://www.cnckitchen.com/blog/comparing-pla-petg-amp-asa-feat-prusament .

Reading [V2+ for the direction, the numbers scatter]: across the layers PETG reaches **0.42–0.84 of its in-plane strength, typically 0.5–0.7 (13–43 MPa against 32–51 MPa), and breaks at half the strain or less**, i.e. an upright blade snaps at a layer line near the root instead of bending. All data-sheet specimens are solid; nobody was found who tested 1–3 mm thin upright PETG walls.

**Sizing a blade** [INF]. Blade as a cantilever, finger force F at the tip, height h, rectangular root b × t (t = thin direction): F = σ·b·t² / (6·h). A "careless finger" is taken as the 10 N of the standard jointed test finger of IEC 61032 [SNIP, test-equipment vendors, e.g. https://www.lisungroup.com/products/standard-test-probes-fingers/iec-61032-standard-articulated-test-probe-with-10n-thrust.html ]; a deliberate push is several times more. Design stress 10 MPa upright (about a third of 23–30 MPa, to cover layer notches and the 13 MPa outlier) and 20 MPa for a blade printed lying flat; "breaks at" uses 25 MPa and 45 MPa.

| h | root b × t | upright: safe F / breaks at | printed flat: safe F / breaks at |
| --- | --- | --- | --- |
| 8 mm | 4 × 1.6 | 2 N / 5 N | 4 N / 10 N |
| 8 mm | 5 × 2.4 | 6 N / 15 N | 12 N / 27 N |
| 12 mm | 5 × 2.0 | 3 N / 7 N | 6 N / 13 N |
| 12 mm | 6 × 3.0 | 8 N / 19 N | 15 N / 34 N |
| 16 mm | 6 × 2.4 | 4 N / 9 N | 7 N / 16 N |
| 16 mm | 6 × 3.0 | 6 N / 14 N | 11 N / 25 N |
| 16 mm | 8 × 4.0 | 13 N / 33 N | 27 N / 60 N |
| 20 mm | 6 × 3.0 | 4.5 N / 11 N | 9 N / 20 N |
| 20 mm | 8 × 4.0 | 11 N / 27 N | 21 N / 48 N |
| 20 mm | 10 × 5.0 | 21 N / 52 N | 42 N / 94 N |

What follows for the design [INF]:

1. A single free-standing upright blade that is still blade-like (t ≤ 3 mm) does **not** survive 10 N at 12–20 mm height. For 10 N at a design stress of 10 MPa the root has to be 6 × 3.5 mm at 12 mm, 8 × 3.5 mm at 16 mm, 8 × 3.9 mm at 20 mm.
2. Therefore merge the 4–6 blades of a tuft into **one solid clump** up to 40–50 % of the height (common root at least 8 × 5 mm) and let only the top 5–8 mm be separate tips; a 6 mm free tip with a 4 × 2.0 mm root is safe for 4 N and breaks at about 11 N, and a finger rests on several tips at once.
3. Taper every blade in thickness as well as in width (thickest at the root), add the root fillet, blunt the tip.
4. Stronger alternative: print the tufts **lying flat** as separate fan-shaped pieces (layers run along the blades: about twice the load and a ductile failure) and plug or glue them into slots of the plate. That also frees the plate to be printed top-face-down (B.2).

### B.2 Flush two-colour mark in the top surface

**How deep must the inlaid colour be?**

| Finding | Status / source |
| --- | --- |
| HueForge "transmission distance" TD = roughly the thickness in mm at which a filament stops showing what is beneath it: "a TD of 2 would mean that after printing a part roughly 2 mm thick … deeper colors contribute very little" | [S1] https://wiki.polymaker.com/the-basics/applications/hueforge-painting |
| Measured TD and hex of Prusament PETG: Jungle Green 0.5 · Anthracite Grey 0.3 · Pistachio Green 0.9 · Mango Yellow 2.6 · Signal White 3.4 · Prusa Orange 6.2 · Neon Green Transparent 75 · Clear 100 | [S1] https://help.prusa3d.com/article/hueforge-filament-transparency-values-and-hexcodes_762314 |
| Model used by HueForge-style tools: transmission T = 10^(−d/TD) for a layer of thickness d | [SNIP] an engrXiv preprint, not opened |
| A one-layer inlay (0.4 mm in the example) can be seen through; "two layers of red make it just opaque enough"; a chamfer or draft on the pocket "will allow you to print multiple layers of the top inlay, so you can't see through it" | [S1, quotes checked in the page text] https://www.matterhackers.com/articles/how-to-print-two-colors-with-one-nozzle |

With that model [INF]: an opaque green (TD 0.5) lets 16 % through at 0.4 mm, 6 % at 0.6 mm, 1 % at 1.0 mm; a TD of 0.9 needs 1.0–1.2 mm for 5–8 %; a pale or translucent filament (TD 2–6) still passes 25–63 % at 1.2 mm. **Rule: inlay depth ≥ the TD of the inlaid filament, and at least 1.0–1.2 mm (5–6 layers of 0.2 mm) for a lighter green over a darker one.** If the lighter green is translucent, make the disc a plug through the full 6.5 mm or lay two white layers under it. Ask the maker for the TD or print a step wedge; only Prusa publishes the values.

**Purge and bleed**

| Point | Status / source |
| --- | --- |
| Every colour change costs a purge; the volume per colour pair is scaled by the "flush multiplier" (default 1.0); purging "inside objects' infills" is an option (default off) | [S1] Bambu Studio source, `flush_multiplier`, `flush_into_infill` |
| Dark → light needs the most flushing; a light, translucent colour shows a dark neighbour through thin walls | see note 06 §5.5 (forum sources there); not re-checked |
| "Interface shells": "force the generation of solid shells between adjacent materials/volumes" (default off); painted regions can be limited in depth with "maximum width of a segmented region" (default 0 = through the body) and keyed with "interlocking depth" | [V2+] both slicer sources |
| Two greens are a mild pair, and a 1.0–1.2 mm deep disc means only 5–6 layers with two changes each | [INF] |

Working values [INF]: every inlaid feature ≥ 0.9 mm wide (two beads; finer strokes are widened or dropped, B.1); model the disc and the plate as two bodies that share the pocket surface exactly (no gap, no overlap); print the lighter colour after the darker one in each layer if the slicer allows it.

**In the first layers (face down) or in the top layers?**

| | Face down (mark in layers 1–5) | Face up (mark in the last 5–6 layers) |
| --- | --- | --- |
| Surface | "glass-smooth" on a smooth plate; a textured PEI plate "leaves a matte texture"; no layer lines on the face | shows the top infill lines; "fine color details may be less sharp" |
| Colour boundary | sharper | follows the bead paths |
| Risks | thin first-layer colour areas are "finicky" to get to stick; the plate texture is copied; first-layer squish moves the boundary by a bead fraction [INF] | ironing can smooth it (Bambu Studio: "using small flow to print on same height of surface again"), which is delicate with PETG [MEM] |
| Works with blades printed in one piece on top | no — the top face has to lie on the bed | yes |
| Sources | [S1] https://color-layer.vercel.app/blog/print-orientation-color-up-vs-down (a vendor blog; it recommends colour-down for small, hand-held prints); Prusa forum users note that text on a textured sheet takes the sheet's grain [SNIP] | same; Bambu Studio source for ironing |

Decision rule [INF]: if the blades are printed in one piece with the plate, the mark has to go into the **top** 1.0–1.2 mm; print it with monotonic top lines and decide about ironing on a coupon. If the tufts become separate plug-in parts (B.1, option 4), print the plate **face down on a textured PEI plate** with the mark in the first 5–6 layers: it gives the cleaner, flatter, more uniform surface and needs no ironing. PETG "bonds strongly to the print surface" and Prusa advises against bare smooth PEI [S1, Prusa PETG article], which is one more reason for the textured plate.

### B.3 Bridging the 16 mm window

| Source | Statement | Status |
| --- | --- | --- |
| Hubs design guide | "If a bridge exceeds 5 mm, sagging or marks from support material can occur" | [S1] https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/ (same figure as note 06 §5.3) |
| Bambu Studio default | "max length of bridges that don't need support" = 10 mm (`max_bridge_length`) | [S1] slicer source |
| Bambu PETG HF data sheet | "max bridging length ~ 30 mm", max overhang angle about 70° | [S1] `downloads/grass_base/bambu_petg_hf_tds/` |
| Prusa | PETG: "poor bridging and overhangs"; bridges work "only over short distances"; reduce the bridge flow and speed, cool; for very long bridges put a support island half-way | [S1] https://help.prusa3d.com/article/petg_2059 , https://help.prusa3d.com/article/poor-bridging_1802 |
| Slicer options | bridge flow: "decrease this value slightly (for example 0.9) … to improve sag"; thick bridges "are more reliable, can bridge longer distances, but may look worse" | [S1] Bambu Studio source |
| User reports | PETG bridges of 65 mm and 92 mm succeeded with visible sag; a vendor blog puts visible sag above about 50 mm | [SNIP] Prusa and Bambu forums, a QIDI blog |

No controlled PETG bridging test was found. Reading [INF]: **16 mm is three times the cautious rule and half of Bambu's own figure — it bridges without support, but the first bridge layer will hang 0.2–0.5 mm and look rough underneath.** Design for that: give the window 0.5 mm extra height, or cut 3 mm × 45° chamfers into the two upper corners (flat span 10 mm), or make the lintel a shallow arch; let the bridge run across the short span, full fan on the bridge layers, bridge flow 0.9–1.0. If the window is cut into the 6.5 mm plate itself, the lintel above it is thin: keep at least 1.2 mm (6 layers) of material above the bridge so that the sag does not print through to the top surface.

---

## Part C — Small standard parts

### C.1 Six-pin wire connectors

**JST PH, 2.0 mm** — manufacturer data sheet `downloads/grass_base/jst_ph/ePH.pdf` (https://www.jst-mfg.com/product/pdf/eng/ePH.pdf). The sheet is titled "2.0 mm pitch / Wire-to-Board connectors"; the series consists of the contact, the receptacle housing PHR and board headers only.

| Part | Width | Thickness | Length / height | Status |
| --- | --- | --- | --- | --- |
| PHR-6 receptacle housing (A = 10.0 over the six contacts) | **13.8** | **4.5** | **6.85** | [V2+] JST drawing; a second maker's drawing of the same housing type gives 13.70 × 4.50 × 6.95 (`…/szlcsc_ph20_a/`, Xyeconn XY-PHR-6PJK); distributor attributes 13.8 × 4.5 [SNIP] RS, Bürklin |
| B6B-PH-K-S shrouded header, top entry | 13.9 | 4.5 | 6.0 above the board (+ 3.4 pins) | [S1] JST |
| S6B-PH-K-S shrouded header, side entry | 13.9 | 4.8 high | 7.6 deep (+ 3.4 pins) | [S1] JST |
| Mated, top entry | 13.9 | 4.5 | 8 above the board | [S1] JST assembly layout |
| Mated, side entry | 13.9 | 4.8 high | 9.6 from the back of the header to the end of the housing | [S1] JST assembly layout |
| Wire | AWG 32–24; standard contact SPH-002T-P0.5S AWG 30–24, insulation Ø0.8–1.5 mm; 2 A at AWG 24 | | | [S1] JST |

- **There is no JST PH wire-to-wire pair** [S1 for "not in the series", INF for "none exists"]. The housing sits 4.85 mm deep in the header's shroud and stands 2.0 mm proud (8 − 6 mm) [INF from the JST dimensions].
- The "JST PH 2.0 male/female cable pairs" are third-party parts: a cable-mounted copy of the header shroud with pins ("plug") plus an ordinary PHR-type receptacle. A reputable seller words it as "2.0 mm pitch 6-pin cable matching pair — JST PH compatible … an inline socket and plug connector", 26 AWG stranded, 20 cm each [S1] https://www.adafruit.com/product/5090 . One kit seller describes HY2.0 (Yeonho SMH200) as the 2.0 mm wire-to-wire family and PH as the one that mates with board headers, "not cross-compatible", while labelling its own PH kits "wire-to-wire" as well [SNIP] keszoox.com (page returned HTTP 429) — so a "2.0 mm male/female pair" can be either family; check the photo for the PH shape. Kits advertised with 22 AWG leads are outside JST's wire range for PH contacts [INF].
- Mated envelope of such an in-line pair: **no drawing found.** Estimate [INF]: 14–15 mm wide × 5–6 mm thick × 12–15 mm long (shroud ≥ 4.85 mm deep plus a rear body for the pins, plus the 2.0 mm of housing that stays outside). Measure the parts.

**Molex PicoBlade, 1.25 mm (sold as "Micro JST 1.25")** — a genuine wire-to-wire system: Molex product specification "PicoBlade 1.25 wire to wire connector system" (`…/rs_doc_c439/`), receptacle housing 51021, plug housing 51047 ("1.25 W/W conn. plg hsg.", application "Signal, Wire-to-Wire", `…/rs_doc_2f2c/`).

| Part | Width | Thickness | Length | Status |
| --- | --- | --- | --- | --- |
| 51021-0600 receptacle housing | **9.25** | **3.2** (2.3 at the nose) | **3.95** | [S1] Molex drawing `…/molex_51021_sd/` (archived copy of molex.com); distributor attributes 9.25 × 3.2 [SNIP] RS |
| 51047-0600 plug housing, wire-to-wire | **9.25** | **3.2** (2.8 at the rear) | **8.0** | [S1] Molex drawing SD-51047 `…/molex_51047_sd/` (archived copy); a distributor lists "depth 8 mm" [SNIP]. The two Molex drawings agree on the 9.25 mm width |
| Mated pair | 9.25 | 3.2 | about 9–9.5 | [INF] 8.0 plus the flange of the receptacle that stays outside; the drawings give no mated length |
| Wire | terminals for AWG 26–28 or AWG 28–32, insulation Ø0.5–1.04 mm; 2.0 A (AWG 26), 1.5 A (AWG 28), 1.0 A (AWG 30/32); 125 V | | | [S1] Molex product specification |

Pre-wired: Molex's own off-the-shelf assembly 218112-0600 (6 circuits, receptacle to pigtail, AWG 28, 75 mm) [S1] `…/szlcsc_molex_94f7/`; "1.25 mm pitch 6-pin cable matching pair, 10 cm" with in-line socket and plug, "Molex PicoBlade compatible" [S1] https://www.adafruit.com/product/4986 (wire gauge not stated there; the single 6-pin cable 4926 is 28 AWG). The generic "Micro JST 1.25" sets are copies of this system [INF]; their envelope should match the Molex drawings within a few tenths, unverified.

**JST SH, 1.0 mm** — `downloads/grass_base/jst_sh/eSH.pdf`, titled "1.0 mm pitch / Wire-to-Board connectors".

| Part | Width | Thickness | Length / height | Status |
| --- | --- | --- | --- | --- |
| SHR-06V-S-B housing (with side protrusions) / SHR-06V-S (without) | **9.0** / 7.0 | **2.8** | **5.0** | [S1] JST |
| BM06B-SRSS-TB header, top entry (SMT) | 8.0 | 2.9 (+ 0.7 solder tab) | 4.25 high | [S1] JST |
| SM06B-SRSS-TB header, side entry (SMT) | 8.0 | 2.9 high (2.95 mounted) | 4.25 deep (+ 0.7) | [S1] JST |
| Mated, top entry / side entry | 8.0–9.0 | 2.9 / 2.95 high | 6.3 high / 6.25 long | [S1] JST assembly layout |
| Wire | AWG 32–28, insulation Ø0.4–0.8 mm; 1.0 A; ready-made cables are 28 AWG, 1 A, 50 V | | | [V2+] JST; https://www.pololu.com/product/5541 |

No wire-to-wire SH part exists in the JST sheet [S1]; pre-wired "SH 1.0 male/female" sets are sold by marketplace brands [SNIP], no dimensions found. Estimate for such a pair [INF]: about 8–10 × 3–3.5 × 8–9 mm.

**Which pre-wired 6-pin plug-and-socket pair is easiest to buy in the EU?**

| Candidate | Evidence of EU supply | Mated envelope | Wire |
| --- | --- | --- | --- |
| 2.0 mm "PH-compatible" pair | Adafruit 5090 at DigiKey's EU sites (1528-5090-ND, "2MM PH 6PIN PAIR 20CM 26AWG") and at a Dutch shop [SNIP]; several eBay.de offers of 6-pin PH plug/socket sets, one from a German seller [SNIP] | about 14–15 × 5–6 × 12–15 mm [INF] | 26 AWG |
| 1.25 mm PicoBlade-compatible pair | product exists (Adafruit 4986); an EU listing was not confirmed | 9.25 × 3.2 [S1, genuine Molex parts] × about 9.5 mm [INF] | 28 AWG |
| 2.5 mm XH-compatible pair, for comparison | "2.5 mm pitch 6-pin cable matching pair — JST XH compatible", € 1.42, Netherlands [S1] https://www.kiwi-electronics.com/en/search?search=matching%20pair | larger than PH (XH is 2.5 mm pitch) — not measured | — |
| JST SM 6-pin plug + receptacle set, for comparison | Adafruit 1665, 22 AWG, 162 mm [S1] https://www.adafruit.com/product/1665 | not looked up | 22 AWG |

Answer [INF from the table]: the **2.0 mm PH-compatible pair** is the one with confirmed EU distribution; plan for about **15 × 6 × 15 mm** per mated pair and measure before fixing the pocket. For 11–12 wires two pairs are needed; each passes a 16 mm window on its own if the window is at least 6.5 mm high. The 1.25 mm pair is half the size (two stacked: 9.25 × 6.4 mm) and has a real manufacturer drawing; it is the better fit if 28 AWG and 1–1.5 A per wire are enough.

### C.2 Countersunk hexagon-socket screws M3

| Dimension | ISO 10642 | DIN 7991 (withdrawn, still sold) | Status / source |
| --- | --- | --- | --- |
| Head Ø dk, nominal = max | **6.72** (theoretical, sharp edge) | **6.00** | [V2+] https://www.fasten.it/en/norms/norm/din_en_iso_10642 , https://www.fasten.it/en/norms/norm/din_7991 ; Böllhoff data sheets `downloads/grass_base/boellhoff_iso10642/`, `…/boellhoff_din7991/` |
| Head Ø dk, min | **5.54** | **5.70** | [V2+] same |
| Head height k, max (min) | **1.86** (1.52) | **1.70** | [V2+] same; k min from Böllhoff and Westfield |
| Hexagon socket s | **2** (2.02–2.08) | 2 (2.02–2.10) | [V2+] same |
| Socket depth t | min 1.10 | 0.95–1.2 | [V2+] same |
| Thread length b | 18 | 12 | [V2+] same |
| Countersink (head) angle | **90°** (tolerance +2°; Böllhoff draws 90°–92°) | 90° | [V2+] same |

One distributor table gives dk max 5.81 instead of 6.72 for ISO 10642 M3 [S1] https://www.westfieldfasteners.co.uk/Bolts-Screws-Metric/Socket-Head-Countersunk-Screw-M3x8-A2-Stainless.html — its other values agree. Geometry check [INF]: a 90° cone from the 3.0 mm shank to Ø6.72 is exactly 1.86 mm high, so 6.72 is the diameter of the theoretical sharp-edged head and k max belongs to it; real heads have a small cylindrical rim and measure 5.5–6.0 mm.

For CAD [INF]: clearance hole Ø3.4; a 90° countersink of **Ø6.8 at the surface** takes any head of either standard flush or up to 0.6 mm below the surface; for an exactly flush head measure the screws and use head Ø + 0.2 mm. The cone is 1.7 mm deep; leave at least 1.5 mm of plastic under it. Countersink dimensions to DIN 74 form F were not found.

### C.3 Heat-set inserts M3 (ruthex, CNC Kitchen)

| Insert | Outer Ø D1 | Guide tip Ø D2 | Hole Ø D3 | Length L | Min. wall W | Status / source |
| --- | --- | --- | --- | --- | --- | --- |
| ruthex RX-M3x5.7 | **4.6** | 3.9 | **4.0** | **5.7** | **1.6** | [V2+ with the next row] https://www.3djake.com/ruthex/threaded-insert-m3-100-pieces (and the German page of the same shop) |
| CNC Kitchen M3 standard | 4.6 | 3.9 | 4.0 | 5.7 | 1.6 | https://www.3djake.com/cnc-kitchen/threaded-inserts-set-standard |
| CNC Kitchen M3 short | 4.6 | 3.9 | 4.0 | 3.0 | 1.6 | same |
| CNC Kitchen M3 "Voron" | 5.0 | 4.25 | 4.4 | 4.0 | 1.3 | same |

**Confirmed: Ø4.6 × 5.7 in a Ø4.0 hole, minimum wall 1.6 mm** (boss Ø ≥ 7.2 mm; hole depth L + 1 mm = 6.7 mm as in note 06 §4.1). Both rows come from one reseller's listings of two brands; the makers' own shops answered HTTP 403 and 429. With a plate of 6.5 mm the standard insert plus 1 mm does not fit blind (6.7 mm): use the 3.0 mm short insert, a through hole, or a local boss [INF].

### C.4 Small self-tapping screws around Ø2.2 mm

| Screw | Head Ø dk max / min | Head height k max | Recess | Status / source |
| --- | --- | --- | --- | --- |
| DIN 7981 pan head, 2.2 (withdrawn, still the usual shop article) | **4.2** / 3.9 | 1.8 (min 1.55) | PH1 | [S1] https://www.fasten.it/en/norms/norm/din_7981 ; a second table with the same values [SNIP] Westfield |
| ISO 7049 pan head, ST2.2 | **4.0** / 3.7 | 1.6 (min 1.4) | PH0 | [S1] https://www.fasten.it/en/norms/norm/din_en_iso_7049 |
| DIN 7982 countersunk, 2.2 (withdrawn) | **4.3** / 4.0 | 1.3 | PH1 | [V2+] https://www.fasten.it/en/norms/norm/din_7982 ; Böllhoff `downloads/grass_base/boellhoff_din7982/` |
| ISO 7050 countersunk, ST2.2 | **3.8** / 3.5 | 1.1 | PH0 | [S1] https://www.fasten.it/en/norms/norm/din_en_iso_7050 |
| "M2 × 6 self-tapping" (not a standard designation) | pan about 4.0, countersunk about 3.8 | 1.6 / about 1.0 | — | [SNIP] shop listings (SKD, McMaster) |

Thread pitch of the 2.2 mm size 0.8 mm [V2+, both sources]; nominal lengths in the Böllhoff sheet 6.5, 9.5, 13, 16 mm and longer (6.5 means 5.7–7.3) [S1]. The head angle of the countersunk types is 90° [INF: (4.3 − 2.2)/2 = 1.05 mm cone plus a rim gives k = 1.3; not printed in the tables read].

Pilot hole in PETG:

| Screw | Hole, axis vertical | Hole, axis horizontal | Engagement | Torque | Status / source |
| --- | --- | --- | --- | --- | --- |
| Bambu BT2 (pitch Ø 1.62 mm), PETG HF | 1.60 | 1.95 | 4.0 mm | 0.15 N·m | [S1, fetch extract] https://forum.bambulab.com/t/how-to-design-screw-holes-for-3d-printing/217352 (same table as note 06 §4.2, read again) |
| Bambu BT2, PETG Basic | 1.65 | 2.00 | 4.0 mm | 0.15 N·m | same |
| Bambu BT2.5 (pitch Ø 2.01 mm), PETG HF / Basic | 2.00 / 2.05 | 2.35 | 5.0 mm | 0.20 N·m | same |

Working values [INF]: Ø2.2 tapping screw (DIN 7981/7982) → **Ø1.8 mm** vertical hole in PETG (between BT2 and BT2.5, and equal to "outer Ø − 0.4 mm"), 5 mm engagement, two wall loops around the hole, boss Ø ≥ 4.5 mm; a 2.0 mm "M2" self-tapper → Ø1.6–1.65 mm. Counterbore for the pan head Ø4.6; 90° countersink Ø4.5 for DIN 7982.

### C.5 TI DRV5032 in TO-92 (package LPG)

From `research/downloads/mcu_audio/ti_drv5032.pdf` (SLVSDC7H, revised December 2024), package drawing LPG0003A (4221343/C) on PDF page 33 and Figure 7-8 on page 15. All [S1] (manufacturer); nominal = middle of the tolerance band.

| Quantity | Value |
| --- | --- |
| Body width | **4.0 mm** (3.9–4.1) |
| Body height (along the leads) | **3.15 mm** (3.05–3.25) |
| Body thickness | **1.52 mm** (1.42–1.62) |
| Front face | flat 2.28–2.68 mm wide between two 45° bevels; the bevels start 0.66–0.86 mm above the back face. The back face is flat over the full width |
| Body top to the end of the lead shoulders | 5.05 mm max |
| Leads | three, pitch **1.27 ± 0.05 mm** (outer leads 2.44–2.64 apart); 0.35–0.48 wide (0.40–0.55 at the shoulder) × 0.36–0.51 thick; 15.1–15.5 mm long below the body; lead centre line 0.54 mm (reference) in front of the back face |
| Pins, seen on the bevelled face with the leads down, left to right (FA, FB, FC, AJ, ZE versions) | 1 VCC · 2 GND · 3 OUT |
| Example board layout | holes on 1.27 mm pitch, 2.54 between the outer ones |
| Sensing element, in the face | centred across the width (2.0 mm from each side, ±50 µm); **1.54 mm below the top edge** of the body, 1.61 mm above the lead-side edge |
| Sensing element, in depth | **1030 µm ± 115 µm above the flat back face**, i.e. **0.49 mm below the bevelled front face** at nominal thickness (0.28–0.71 mm with all tolerances stacked [INF]) |
| Sensitive direction | the field component perpendicular to the "top of the package"; Figure 7-1 draws it through the TO-92 from the flat back to the bevelled front face. The FB version is omnipolar ("responds to north and south magnetic poles") |

The data sheet does not say in words which face carries the marking; for TO-92 Hall sensors that is by convention the bevelled front face [MEM]. Read "depth below the marked face" as **0.49 mm below the bevelled face**, and check on the part that the marking is there. For the dock: put the bevelled face toward the magnet, with the magnet's axis through a point 1.5 mm below the top edge of the body and on its centre line.

---

## D. What could not be verified

1. **In-line "PH-compatible" and "SH-style" plugs:** no drawing; their size and the mated envelope are estimates. Measure the pair before the pocket and the window are fixed.
2. **Mated length of the genuine PicoBlade pair** (9–9.5 mm): derived from two separate housing drawings.
3. **EU supply** of the pairs: search summaries only (DigiKey, one Dutch shop, eBay.de); the 1.25 mm pair was not confirmed at an EU shop. Marketplace listings were not opened.
4. **Marked face of the DRV5032 in TO-92** — not stated in the data sheet text that was read.
5. **Filament colours:** Bambu's hex codes come from retailer copies of its table; no hex codes for eSUN, SUNLU, Elegoo, Polymaker, AzureFilm PETG greens; transmission distances only for Prusament. The colour differences in A.4 compare nominal hex codes, not printed samples.
6. **HueForge transmission formula** — search summary of a preprint.
7. **Z strength of thin PETG walls:** all figures are from solid test bars; no test of 1–3 mm upright walls was found. The blade table is a first-order beam estimate.
8. **Finger force:** 10 N is the IEC 61032 test-finger force as quoted by test-equipment vendors; the standard was not read.
9. **PETG bridging at 16 mm:** no controlled test found; the conclusion rests on a design guide, a slicer default, one maker's data sheet and forum reports.
10. **Heat-set inserts:** makers' own pages not reachable (HTTP 403 / 429); values from one reseller.
11. **Tapping screws:** head angle (90°) inferred; "M2 × 6 self-tapping" head sizes from shop listings; DIN 74 form F countersink values not found.
12. **Pictures:** provenance of G06 as a press screenshot, G08 as the "Sightings" tuft and G09's episode are taken from the hosting wikis or from appearance. No merchandise that shows tall grass as blades was found. Bulbapedia has no pictures for Sword/Shield, Brilliant Diamond/Shining Pearl or Scarlet/Violet.
13. **Polymaker's current data sheet** (50.8 / 42.8 MPa) was read through the fetch tool's extract of the wiki page; the V5.4 PDF link returned 404. The V5.2 PDF with very different values is stored.
14. Statements marked [MEM]: ironing behaviour of PETG, minimum layer time for small tips, the marking convention of TO-92 Hall sensors.

**Disagreements between sources**

| Topic | Disagreement |
| --- | --- |
| ISO 10642 M3 head Ø max | 6.72 (fasten.it, Böllhoff: theoretical sharp edge) versus 5.81 (Westfield) |
| PETG Z / XY strength | 0.42 (PolyLite V5.2) · 0.46 (CNC Kitchen) · 0.60–0.75 (Prusament, Bambu) · 0.84 (PolyLite wiki) |
| Unsupported bridge | 5 mm (Hubs) · 10 mm (Bambu Studio default) · about 30 mm (Bambu PETG HF sheet) · 65–92 mm with sag (forum reports) |
| Ø2.2 tapping screw heads | DIN 7981 4.2 × 1.8, PH1 versus ISO 7049 4.0 × 1.6, PH0; DIN 7982 4.3 × 1.3 versus ISO 7050 3.8 × 1.1 — shops mostly stock the DIN geometry |
| PH receptacle housing, 6-way | 13.8 × 4.5 × 6.85 (JST) versus 13.70 × 4.50 × 6.95 (Xyeconn copy) |
| Adafruit 4986 cable length | 10 cm in the text, "20 cm" in the picture captions |
| FDM minimum pin / wall | 1 mm, 1.5 mm, 3 mm pins and 0.8–2 mm walls, depending on the guide |

**Sources that could not be opened:** bulbapedia.bulbagarden.net and archives.bulbagarden.net (HTTP 403; archived copies used), molex.com (time-out; archived drawings used), ruthex.de and cnckitchen.store (403 / 429), keszoox.com (429), uk.rs-online.com product pages (403), eu.store.bambulab.com PETG HF page (404), the Böllhoff DIN 7981 data sheet (404), several pokemon.fandom.com image URLs (403), polymaker.com V5.4 PDF (404), TI's HTML viewer for a sister data sheet (table of contents only). The JST PDFs have a text layer in a shifted encoding and fonts the usual renderers could not draw; their pages were rendered to images with Ghostscript in `-dSAFER` mode and read from those. The Prusament PDF was likewise read from rendered pages.

## E. Reproduce

Colour and geometry numbers of Part A: Pillow and numpy from the project environment, run as `uv run python -I <script> <image>` from the repo root, image paths as arguments. The scripts lived in a temporary folder and are not part of the repository; the method and the pixel boxes are written down in `research/reference_images/tall_grass/SOURCES.md` (exact palette for pixel art, k-means with k = 3 on hue-filtered pixels otherwise, bounding boxes of opaque pixels, autocorrelation for the grid pitch, exact tile matching on a 16 px grid for the block layout, CIE76 for the filament comparison).
