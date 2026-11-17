# 03 — Classic Poké Ball proportions, measured from reference images

Research date / access date for every URL: **2026-11-17**.
Images, scripts, raw numbers and check overlays: `research/reference_images/` (index: `reference_images/SOURCES.md`).

All ratios are fractions of the ball's outer diameter **D**.

## 1. Result in one table

Recommended canonical set for a faithful-looking print (true geometry, i.e. what to model in CAD):

| quantity | ratio of D | plausible range | D = 90 mm | D = 100 mm | D = 110 mm |
|---|---|---|---|---|---|
| black band height (gap between red and white shell) | **0.070** | 0.058 – 0.075 "thin" look; 0.10 – 0.12 "chunky" look | 6.3 | 7.0 | 7.7 |
| black ring, outer diameter | **0.340** | 0.32 – 0.355 | 30.6 | 34.0 | 37.4 |
| white disc inside the ring (= ring inner diameter) | **0.225** | 0.21 – 0.24 | 20.2 | 22.5 | 24.8 |
| → radial width of the black ring | 0.0575 | 0.05 – 0.06 | 5.2 | 5.8 | 6.3 |
| central button diameter | **0.140** | 0.13 – 0.15 | 12.6 | 14.0 | 15.4 |
| band centre | on the equator | ±0.3 % of D | — | — | — |
| band surface recessed below the shells | 0.012 | 0.010 – 0.015 (replica); 0 is also "canon" | 1.1 | 1.2 | 1.3 |
| button face above the white collar | 0.023 | 0.02 – 0.03 | 2.1 | 2.3 | 2.5 |
| ring + collar plane below the sphere apex (flat ring face) | 0.030 | geometry: ½·(1 − √(1 − 0.34²)) | 2.7 | 3.0 | 3.3 |

Red and white shells are equal: each spans (D − band)/2 of the height.

How sure: ring / disc / button agree within about ±5 % across the trustworthy sources. The **band height is the
one feature the sources do not agree on** (0.056 … 0.123, a factor of two) — it is a style choice; 0.07 matches
the official replica, the Sugimori artwork and Pokémon GO. Details and caveats in §6.

## 2. Method

* 13 front-ish images from independent sources were measured (`F01`–`F13`), plus two three-quarter photos of the
  official replica for depth (`S01`, `S03`). See `reference_images/SOURCES.md` for file → URL.
* `measure_front_views.py` fits, per image: the silhouette circle (→ D); the outer edge of the black ring; the
  inner edge of the ring (→ white disc); the button edge; and the band thickness on lines perpendicular to the
  band at centre ± f·R. f = 0.5 is the "25 % / 75 % of the width" position; where the button ring or a finger
  covers that spot another f is used and named in the table. Edges are located at the steepest point of a
  smoothed profile (sub-pixel), circles/ellipses are least-squares fits with outlier rejection.
* Every fit was drawn back onto the image (`reference_images/overlays/*_overlay.png`) and looked at; several
  first attempts were wrong (band edge inside a highlight, silhouette locked onto a glossy rim) and were fixed.
* **Oblique views.** A circle seen obliquely is an ellipse whose major axis is the true diameter. Ring, disc and
  button are fitted with an ellipse constrained by the sphere geometry (minor axis along the radius through the
  ball centre, axis ratio from the centre offset), which stays stable where the band hides part of the ring; an
  unconstrained ellipse was fitted as well and agrees within ~1 % (both are in `measurements_front.json`). Band
  thickness in a view tilted by t is multiplied by 1/cos t.
* **Outlines in artwork.** Drawn black outlines are not part of the object. Object edges are taken at the
  outline centre line: for the clip-art vector, the anime frame and the silhouettes the centre of the line is
  located directly; for the Sugimori artwork (6.4 px outlines on a 656 px ball) one outline width is subtracted
  from the dark features (band, ring outer diameter) and added to the white disc. Without that correction the
  Sugimori band would read 0.068 instead of 0.058.
* **Camera perspective.** In a photo or render the front of the ball is closer to the camera than the
  silhouette, so band, ring, disc and button look 5–25 % too big relative to D. `measure_side_views.py` fits the
  camera distance d from how the band appears thinner towards the limb (T ∝ 1/(d − z)) and
  `measure_summary.py` removes it. This worked for the replica photos; for small game renders it is not possible
  (those rows are marked *apparent*).

## 3. Per-image measurements

### 3a. As measured (tilt and outline corrected, camera perspective NOT removed)

| id | image | D [px] | yaw / tilt | band/D (where) | band centre below ball centre | ring OD/D | white disc/D | button/D |
|---|---|---|---|---|---|---|---|---|
| F01 | Sugimori official artwork | 656 | −11° / 25° | 0.058 (0.064 at f=−0.62, 0.052 at f=+0.5) | (tilted) | 0.321 | 0.208 – 0.221 | 0.140 |
| F02 | Pokémon GO item sprite | 180 | 16° / 20° | 0.056 (f=−0.5: 0.060, −0.7: 0.055, +0.8: 0.054) | (tilted) | 0.359 | 0.257 | 0.133 |
| F03 | Let's Go in-game model, screenshot | 212 | 0° / 5° | 0.101 (25 %: 0.101, 75 %: 0.100) | +0.048 (= 5° tilt) | 0.354 | glow | glow |
| F04 | TWC die-cast replica (Dusk Ball), front photo | 1876 | 1° / 1° | 0.078 (25 %: 0.078, 75 %: 0.079) | +0.006 | 0.374 | 0.253 | 0.165 |
| F05 | TWC die-cast replica (Poké Ball) in hand | 1881 | 17° / 6° | 0.071 (25 %: 0.073, f=+0.8: 0.070) | (tilted) | 0.376 | 0.251 | 0.165 |
| F06 | TWC Mini replica 40 mm, render | 1566 | −1° / 1° | 0.084 (f=±0.6) | +0.003 | 0.421 | 0.279 | 0.182 |
| F08 | Vector art, official clip-art style | 1135 | 14° / −7° | 0.123 (f=−0.66: 0.120, +0.74: 0.126) | (tilted) | 0.346 | 0.238 | 0.168 |
| F09 | Fan 3D model (Sketchfab) | 585 | −14° / 5° | 0.108 (f=−0.78: 0.105, 75 %: 0.112) | (tilted) | 0.367 | 0.266 | 0.141 |
| F10 | Fan 3D print (Printables), phone photo | 1569 | −2° / 1° | 0.110 (f=±0.62) | +0.005 | 0.367 | 0.269 (whole white button) | — |
| F11 | TV anime EP001 frame | 160 | −10° / 11° | 0.076 (f=−0.7 only) | (tilted) | 0.341 | 0.183 | 0.117 |
| F12 | Smash Bros. Wii U trophy render | 236 | 22° / −16° | 0.061 (f=−0.55, +0.8) | (tilted) | 0.393 | 0.290 | stub |
| F07 | Fan vector "Poké Ball.svg" (numbers from the SVG) | — | 0 / 0 | 0.111 | 0 | 0.289 | 0.234 | 0.141 |
| F13 | Fan icon "Poké Ball icon.svg" (numbers from the SVG) | — | 0 / 0 | 0.073 | 0 | 0.356 | 0.210 | none |

### 3b. Best estimates of the true ratios (perspective removed where it could be fitted)

| id | source | group | band/D | ring OD/D | white disc/D | button/D | grade |
|---|---|---|---|---|---|---|---|
| F01 | Sugimori official artwork | official 2D art | 0.058 | 0.321 | 0.214 | 0.140 | A |
| F08 | Vector art, official clip-art style | official-style 2D art | 0.123 | 0.346 | 0.238 | 0.168 | A |
| F11 | TV anime EP001 frame | official 2D art | 0.076 | 0.341 | 0.183 | 0.117 | B |
| F04c | TWC replica, F04, camera at 7.2 R removed | official replica | 0.069 | 0.329 | 0.222 | 0.144 | – |
| F05c | TWC replica, F05, camera at 6.7 R removed | official replica | 0.063 | 0.329 | 0.219 | 0.143 | – |
| S01c | TWC replica, S01, camera at 10.7 R removed | official replica | 0.067 | 0.345 | 0.227 | – | – |
| **TWC** | **The Wand Company die-cast replica 75 mm (mean of the three)** | official replica | **0.066** | **0.334** | **0.223** | **0.144** | A |
| F06 | The Wand Company Mini 40 mm, camera at 5.2 R removed | official replica | 0.071 | 0.352 | 0.234 | 0.150 | A |
| F02 | Pokémon GO item sprite — apparent | official 3D render | 0.056 | 0.359 | 0.257 | 0.133 | C |
| F03 | Let's Go in-game model — apparent | official 3D render | 0.101 | 0.354 | – | – | C |
| F12 | Smash Bros. Wii U trophy — apparent | official 3D render | 0.061 | 0.393 | 0.290 | – | C |
| F09 / F09c | Fan 3D model — apparent / camera at 3.4 R removed | fan | 0.108 / 0.084 | 0.367 / 0.278 | 0.266 / 0.202 | 0.141 / 0.104 | C |
| F10 / F10c | Fan 3D print — apparent / camera at 2.9 R removed | fan | 0.110 / 0.081 | 0.367 / 0.261 | 0.269 / 0.192 | – | C |
| F07 | Fan vector (Wikipedia icon) | fan | 0.111 | 0.289 | 0.234 | 0.141 | A |
| F13 | Fan icon | fan | 0.073 | 0.356 | 0.210 | – | B |

Grade = how far the number can be trusted as geometry: A good, B low resolution or stylised, C perspective
unknown or poorly constrained. On the replica at its real size (75 mm) the TWC row means: band 5.0 mm,
ring 25.0 mm (= D/3), white collar 16.7 mm, button 10.8 mm.

### 3c. Statistics

Geometry-grade sources only (F01, F08, F11, TWC, F06, F07, F13 — each source counted once):

| quantity | n | mean | median | min | max |
|---|---|---|---|---|---|
| band/D | 7 | 0.083 | 0.073 | 0.058 | 0.123 |
| ring OD/D | 7 | 0.334 | 0.341 | 0.289 | 0.356 |
| white disc/D | 7 | 0.219 | 0.223 | 0.183 | 0.238 |
| button/D | 6 | 0.143 | 0.142 | 0.117 | 0.168 |

Official sources among those (F01, F08, F11, TWC, F06):

| quantity | n | mean | median | min | max |
|---|---|---|---|---|---|
| band/D | 5 | 0.079 | 0.071 | 0.058 | 0.123 |
| ring OD/D | 5 | 0.339 | 0.341 | 0.321 | 0.352 |
| white disc/D | 5 | 0.218 | 0.223 | 0.183 | 0.238 |
| button/D | 5 | 0.144 | 0.144 | 0.117 | 0.168 |

All 12 independent sources, using apparent values where perspective is unknown (so ring and disc are biased high):

| quantity | n | mean | median | min | max |
|---|---|---|---|---|---|
| band/D | 12 | 0.085 | 0.075 | 0.056 | 0.123 |
| ring OD/D | 12 | 0.348 | 0.353 | 0.289 | 0.393 |
| white disc/D | 11 | 0.238 | 0.234 | 0.183 | 0.290 |
| button/D | 8 | 0.142 | 0.141 | 0.117 | 0.168 |

Reading the spread:

* **Ring OD ≈ D/3** is robust: 0.32–0.355 in every official geometry-grade source; the replica is 0.334.
* **White disc ≈ 0.22–0.24**, **button ≈ 0.14–0.15**; only the low-resolution anime frame is smaller.
* **Band**: two clusters. Thin, 0.056–0.076: Sugimori, Pokémon GO, Smash, the replica, the anime frame.
  Thick, 0.10–0.12: the Let's Go model, the clip-art vector, both fan vectors/models. The black ring's radial
  width (0.05–0.06 D) is about 0.85–0.9 × the band height in the thin-band sources (replica 0.84, Sugimori 0.92).
* **Band position**: in the three straight-on images (F04, F06, F10) the band mid-line is 0.003–0.006 D below
  the fitted ball centre and the button centre has the same offset. That is within measurement error of the
  equator (a camera elevation of under 1° produces it): the band is on the equator and the button is centred on
  the band.

## 4. Depth: does the button protrude, is the band recessed?

Measured on The Wand Company replica (`measure_side_views.py`, `S01` and `S03`, both ~42–44° off-axis):

| feature | value | from |
|---|---|---|
| band surface below the shell surface, seen in profile at the limb | 0.011, 0.011 and 0.015 D (≈ 0.8–1.2 mm on the 75 mm ball) | F04 left/right limb, S01 |
| black ring + white collar | one flat face lying in the chord plane of the ring's outer edge (collar plane at 0.94 R ≈ √(1 − 0.334²) R); the shell's cut-out wall is visible on the far side | S01 |
| button face above the white collar | 0.023 D (S01), 0.025 D (S03) ≈ 1.7–1.9 mm at 75 mm | wall width / sin(view angle) |
| button face relative to the sphere envelope | 0.97–0.99 R, i.e. flush to ~1.5 % of D **below** the sphere; it does not stick out | S01, S03 (±1.5 % of D) |

So the official replica is a ball with a shallow groove (band) and a flat-bottomed circular pocket (ring) from
which the button rises back to about the sphere surface. Other sources, qualitatively:

* Sugimori artwork and the clip-art: no relief drawn except a highlight on the button (reads as a low dome).
* Smash Bros. Brawl / Wii U models (`S10`, `F12`): raised black ring, button stub clearly proud of the sphere
  (by eye roughly 3–5 % of D; not measured).
* 1999 Burger King container (`S06`): ring and button moulded as a raised boss on the white half, band flush.
* Poké Ball Plus (`S15`): band flush (colour inlay), control stick protrudes.
* Fan models: band visibly recessed with lips (`F09`, `F10`) and buttons that stand proud of the sphere
  (`S11`, `S13`) — by eye a few percent of D each; not measured.

Recommendation: recess the band 1.0–1.5 % of D, sink ring and collar as a flat face, let the button end
between flush and +1.5 % of D proud of the sphere (proud reads better at arm's length and prints as a button).

## 5. Colours

Median colour of each class inside the ball (`measure_colors.py`); photos and shaded art depend on lighting.

| source | red | black / band | white |
|---|---|---|---|
| Vector art, official clip-art style (exact flat swatches) | #EF4036 | fill #58585A, outline #231F20 | #FFFFFF (shadow #A19E9E) |
| Pokémon GO item sprite | #FF2322 | #141A22 | #E7F3F7 |
| Smash Bros. Wii U trophy | #FE3118 | #020200 | #EEEDE9 |
| Sugimori artwork (watercolour) | #ED5E64 | #393A39 | #D5D6DC |
| Let's Go screenshot (bloom-lit) | #FD7F7A | #525B4F | #D4DCD6 |
| TV anime EP001 (1997 cel colours) | #C63655 | #47374C | #BDC4DC |
| TWC replica photo / Mini render | #D24040 / #E04848 | #2A2A2A / #282727 | #B9B9B9 / #D5D5D5 |
| Fan vector (Wikipedia icon), from SVG | maroon (#800000) | black | #F2F2F2, button #999999 |
| Fan icon, from SVG | #FF1C1C (shade #DF1818) | black | #FFFFFF (shade #DFDFDF) |

Commonly cited palettes: Eggradients "Pokéball Colors" lists #F08080, #FF0000, #B22222, #000000, #DCDCDC and
white; a derived Pokémon GO brand red of #E21C25 is quoted by brandcolorcode.com (not a Poké Ball value). Both
are taken from the search engine's summary of those pages (the hex values are in images / scripts there and
were not parsed directly). No official colour specification was found. Practical target: a saturated, slightly warm signal red around
**#EE2A2A–#F03A30** (not crimson, not maroon), near-black **#1A1A1A–#231F20**, clean white **#F5F5F5–#FFFFFF**;
the button is the same white or marginally greyer.

## 6. Real-world sizes

| object | diameter | notes | source |
|---|---|---|---|
| The Wand Company die-cast Poké Ball replica | 75 mm (~2.95″) | 297 g (the page also says 291 g); die-cast zinc shells, ABS band and button; lit, touch-sensing button; **does not open**; display case 90 × 95 × 95 mm | thewandcompany.com/pokeball/ |
| The Wand Company Mini Poké Ball | 40 mm | 80 g; does not open; "dimensions, colour, size and weight" approved by Pokémon | thewandcompany.com/?p=12408 |
| Nintendo Poké Ball Plus | 48 mm (without protruding parts) | ~65 g | Nintendo support |
| Burger King 1999 promotional container | 70–76 mm (2.75–3″) | two halves pull apart | Wikipedia, "Burger King Pokémon container recall" |
| Jazwares Clip 'N' Go Poké Ball | not published | holds one 2-inch / 5 cm figure; one eBay title says "(3 inch)"; ~70–75 mm is unverified | retailer listings |
| in-universe "canon" | no official figure found | fan wiki: "exact dimensions … not known … probably around 4–6 cm"; retailer copy for the TWC replicas: ~75 mm "based on its actual size within the world of Pokémon" (both quoted from web-search snippets, pages not fetched) | see §9 |

The de-facto life size is therefore ~75 mm (baseball-sized). A 100 mm print is 1.33× that (90 mm: 1.2×, 110 mm: 1.47×).

## 7. Hinge, button and seam conventions

| object | opens? | hinge | button and band belong to | parting line |
|---|---|---|---|---|
| Jazwares Clip 'N' Go (`S08`, `S09`) | yes ("open the clasp on the back") | at the back, opposite the button | the **red lid** carries the whole black band and the button; the white bowl has a U-notch at the front | lower edge of the band |
| Burger King 1999 (`S06`, `S07`) | yes, halves pull apart, no hinge | – (belt clip at the back of the white half) | the **white half** carries band and button (unpainted white); the red half has a semicircular notch | upper edge of the band |
| The Wand Company replicas | no | – | band + ring are a separate black part between two shells; both shells are notched around the ring | both band edges are visible joints |
| TV anime EP001 (`S16`) | yes | at the back; red lid swings up ~90° | not resolvable in the frame | not resolvable |
| Fan print, Gonz Heredia (`S11`) | yes | at the back | button on the **red** half; each half has half the band | middle of the band (equator) |
| Fan model "Lifesize Pokeball!" (`S12`) | yes | at the back | button on the **white** half; each half has half the band | middle of the band (equator) |
| Fan print, 3D Gene Designs (`S13`) | yes | at the back | button on the **red** half | not resolvable in the photo |

Common ground: hinge at the back, exactly opposite the button; red half is the lid. Which half carries the
button is not fixed (official toy: red lid; official 1999 promo: white half; fan models: both). The seam runs
either along one edge of the band (injection-moulded toys, band entirely on one half) or through the middle of
the band on the equator (fan prints) — both hide well because the seam coincides with a colour change or sits
inside the black.

## 8. What is solid and what is shaky

Solid

* Official replica, apparent proportions: two independent photos (different ball, different camera) give ring
  0.374 / 0.376, disc 0.253 / 0.251, button 0.165 / 0.165 of D.
* Ring OD ≈ D/3, disc ≈ 0.22–0.24, button ≈ 0.14–0.15 across official geometry-grade sources.
* Band on the equator; button centred on the band.
* Replica band recess 1.1–1.5 % of D (three limb measurements) and button 2.3–2.5 % of D above its collar (two photos).

Medium

* Perspective-corrected replica values: they depend on the fitted camera distance (7.2 R [5.9–9.3], 6.7 R
  [6.3–7.0], 10.7 R [8.9–13.2]); the three photos then give ring 0.329 / 0.329 / 0.345 and band 0.069 / 0.063 /
  0.067, i.e. ±3–5 %.
* Sugimori artwork: hand-drawn, its three ellipses are not mutually consistent (disc model fit 0.208 vs free fit
  0.221); ±5 %.
* Mini replica: a single wide-angle render, −15 % perspective correction on the ring.

Shaky

* Pokémon GO sprite, Let's Go screenshot, Smash trophy: 180–240 px balls (±0.5 px is ±5 % on the band) and
  unknown perspective — their ring and disc values are probably 5–15 % too large.
* Fan-model corrections (F09c, F10c): the recessed band biases the camera fit; true values lie between the
  apparent and the corrected column.
* Anime frame (160 px, blurry); one frame cannot represent 25 years of anime drawings.
* Button top versus sphere envelope (±1.5 % of D): no dead-on side profile of an official replica was found.
* Colours (lighting, rendering, JPEG) and the unpublished Jazwares diameter.
* Attribution of F01 to Ken Sugimori and the provenance of F08 rest on the hosting wikis; Bulbapedia could not
  be reached (Cloudflare).

## 9. Source URLs (all accessed 2026-11-17)

Image files: one URL per file in `reference_images/SOURCES.md`. Facts quoted above:

* The Wand Company, full-size Poké Ball replica (75 mm, 297 g / 291 g, materials, "does not open", case 90 × 95 × 95 mm): https://www.thewandcompany.com/pokeball/
* The Wand Company, Mini Poké Ball (40 mm, 80 g, "does not open up", approval statement): https://www.thewandcompany.com/?p=12408
* Nintendo support, Poké Ball Plus ("48mm diameter (not including protruding parts)", "Approx. 65g"): https://en-americas-support.nintendo.com/app/answers/detail/a_id/42359/p/897/c/715
* Wikipedia, Burger King Pokémon container recall (2.75–3 in, halves pull apart): https://en.wikipedia.org/wiki/Burger_King_Pok%C3%A9mon_container_recall
* Target, Jazwares Clip 'N' Go ("Simply open the latch to reveal the figure inside"; 2-inch figure): https://www.target.com/p/-/A-85717622
* Maziply, Jazwares Clip 'N' Go ("open the clasp on the back of the Pokéball"; fits any 5 cm figure): https://www.maziply.com/products/pokemon-clip-n-go-fennenin-pokeball-figure-set
* eBay listing title "Jazwares - Pokemon Clip 'N' Go Poke Ball & Figure … (3 inch)": https://ebay.com/itm/364299246388
* Retailer copy "nearly 3 inches (75 mm) in diameter — based on its actual size within the world of Pokémon" (TWC Premier Ball): https://www.theswordandboardtoronto.com/products/pokemon-premier-ball-replica
* Fan wiki on the in-universe size ("probably around 4-6 centimeters in diameter"): https://pokemon.gamepedia.com/Poke_Ball
* Eggradients "Pokeball Colors" palette: https://www.eggradients.com/palette/pokeball-colors
* Pokémon GO brand red #E21C25 (derived): https://www.brandcolorcode.com/pokemon-go
* Wikimedia Commons, fan vectors and Burger King photos: https://commons.wikimedia.org/wiki/File:Pok%C3%A9_Ball.svg , https://commons.wikimedia.org/wiki/File:Pok%C3%A9_Ball_icon.svg , https://commons.wikimedia.org/wiki/File:Pokebola-pokeball-png-0.png , https://commons.wikimedia.org/wiki/File:Burger_King_Pok%C3%A9_Ball_-_closed.jpg , https://commons.wikimedia.org/wiki/File:Burger_King_Pok%C3%A9_Ball_-_opened.jpg
* WikiDex image categories (artwork and anime frames): https://www.wikidex.net/wiki/Categor%C3%ADa:Ilustraciones_de_Pok%C3%A9_Balls , https://www.wikidex.net/wiki/Categor%C3%ADa:Im%C3%A1genes_de_Pok%C3%A9_Balls_en_el_anime
* SmashWiki files (Let's Go screenshot, trophies): https://www.ssbwiki.com/File:PokeballLetsGoPikachuEevee.jpg , https://www.ssbwiki.com/File:PokeBallTrophyWiiU.png , https://www.ssbwiki.com/File:Poke_Ball_-_Brawl_Trophy.png
* PokeMiners Pokémon GO asset dump: https://github.com/PokeMiners/pogo_assets
* Printables models: https://www.printables.com/model/374028-pokeball , https://www.printables.com/model/990970-lifesize-pokeball , https://www.printables.com/model/1310276-functional-pokeball-fully-detailed
* Sketchfab model (JMGameDev, "Pokemon Basic Pokeball"): https://sketchfab.com/3d-models/none-9b29539199c14ddea4de7776c4d758df
* Not reachable: https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9_Ball and archives.bulbagarden.net (HTTP 403 / Cloudflare challenge).

## 10. Reproduce

```sh
uv run python -I -B research/reference_images/measure_front_views.py
uv run python -I -B research/reference_images/measure_side_views.py
uv run python -I -B research/reference_images/measure_colors.py
uv run python -I -B research/reference_images/measure_summary.py
```

Needs numpy and Pillow, both importable in the project environment as it is (nothing was added to the project).
