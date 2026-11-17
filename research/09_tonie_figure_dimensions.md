# 09 — Tonie figure dimensions (the four Pokémon Tonies, and Tonies in general)

Access date of every web source: **2026-11-17**.
Pictures that were measured, with their URLs: `research/reference_images/tonie_figures/` (index: `SOURCES.md`, check overlays in `overlays/`). Other saved pages and files: `research/downloads/tonie_figures/`.
Confidence tags: **VERIFIED** = two or more independent sources agree · **single source** · **inferred** = derived here (picture measurement, calculation or reasoning), no source states it.

No source publishes the size of a Tonie figure. tonies.com lists material and "magnethaftend, handbemalt" for the Pokémon Tonies and nothing else; retailers repeat one packaging size for every Tonie. All figure dimensions below were therefore measured on official pictures against the Toniebox 2, whose size is published.

## 1. Values to use in CAD

| Quantity | Value | Tolerance | Confidence | Where |
|---|---|---|---|---|
| Foot (black base) of all four Pokémon Tonies: diameter | **45 mm** | +2 / −1.5 mm | inferred — four measuring routes give 44.2 … 46.2 | §3 |
| Foot: height | **15 mm** | ±1 mm | inferred | §3 |
| Foot: shape | round puck, the same on all four; top edge rounded (≈2 mm); flat name plate at the front that stays inside the circle (≤1.7 mm) | — | inferred | §3 |
| Overall height incl. foot | Pikachu **70**, Glumanda **63**, Bisasam **61**, Schiggy **60** mm | ±3 mm each | inferred | §4 |
| Largest width of the figure above the foot | Pikachu 37, Bisasam 35, Schiggy 33, Glumanda 32 mm (front view) | ±2 mm | inferred | §4 |
| Overhang beyond the foot | ≤ 1.2 mm (Pikachu's ear tip, Schiggy's arm); nothing else | +2 mm for the unseen side view | inferred | §4 |
| **Safe envelope for all four** | cylinder **Ø 52 mm × 78 mm**, on the axis of the foot | tolerances of the rows above are already inside it | inferred | §4 |
| Seat on the platform | flat, at least Ø 52 mm clear; no tight recess. A locating ring, if wanted: Ø 48 mm, at most 1 mm deep, only after measuring a figure | — | design consequence | §3 |
| Where a figure ends up on a real Toniebox 2 | 2 … 6 mm off the centre of the light ring | — | inferred (one photo, three video frames) | §7 |
| Mass | 40 … 50 g | — | single sources that disagree (40 g, 48 g) | §6 |
| Magnet (classic Tonies) | cylinder **Ø 6 × 6 mm**, one or two; in a Creative Tonie one in each foot | ±0.5 mm | VERIFIED for the Creative Tonie; **not verified for the Pokémon foot** | §7 |
| Magnet depth | pole face 1 … 2 mm above the underside | — | inferred (replica practice only) | §7 |
| Magnet position in the Pokémon foot | **unknown — do not assume the centre** | — | not verified | §7 |
| Tag | upright ferrite-rod transponder, ≈ 10 mm long, < 4 mm thick — not a flat inlay | — | VERIFIED (classic Tonies) | §8 |
| Tag height above the underside | classic figures: ≈ 20 mm above the magnet, up to ≈ 50 mm; Pokémon figures: unknown. Plan the reader for **3 … 55 mm**, near the axis | — | VERIFIED for classic figures, not verified for Pokémon | §8 |

## 2. The four figures — official data

| | Pikachu | Bisasam | Glumanda | Schiggy |
|---|---|---|---|---|
| Article number (SKU) | 10001692 | 11003815 | **11003817** | 11003819 |
| GTIN | 4251192129161 | 4251192175571 | 4251192175595 | 4251192175618 |
| Running time | 78 min | 79 min | 77 min | 67 min |

Source: product data embedded in https://tonies.com/de-de/tonies/pokemon/pikachu/ (and `/bisasam/`, `/glumanda/`, `/schiggy/`). Single source (the maker). This also settles the Glumanda number that note 01 left open.

- Published for each: material "Kunststoff", "Magnethaftend, handbemalt", "Kompatibel mit allen Tonieboxen", warnings `choking-hazard` and `interfering-magnet`. **No dimension, no weight.** Same pages.
- All four stand on the same black round base. Maker: "The black base was designed to keep the focus on the Pokémon itself" (https://support.tonies.com/hc/en-gb/articles/37955468581906-tonies-x-Pok%C3%A9mon-FAQ). Press: "Die Figuren sind jeweils auf einem schwarzen Sockel befestigt" (https://www.gameswelt.ch/toniebox/special/pokemon-erobern-jetzt-auch-akustisch-das-kinderzimmer-335479). VERIFIED.
- Scale reference: Toniebox 2 = **130 × 130 × 126 mm, 815 g** (https://tonies.com/de-de/toniebox-2/toniebox-2-hellblau/). Single source (the maker); retailers repeat it.

## 3. The foot: diameter, height, shape

### Method

1. **Model of the box top.** The official top view of the Toniebox 2 was scaled to its 130 mm width. It gives: white panel 106.7 mm wide with corner radius ≈ 19.7 mm; light ring inner Ø 68.0 mm, outer Ø 76.0 mm; ring centre 6.5 mm from the panel centre, away from the ears.
2. **Ring ratio.** In the official "figure on a Toniebox" pictures the foot stands inside the ring on the same plane. Ellipses were fitted to the ring's edges; foot Ø = ring Ø × foot width / ring major axis.
3. **Homography and cylinder.** In oblique pictures the outline of the white panel was located and a plane homography fitted to the model outline (rms 0.12–0.38 mm). The lit ring, not used in the fit, lands within 0.1–1.0 mm of its predicted radius. The camera was then recovered from the homography and an upright cylinder fitted to the left, right and lower silhouette of the foot. The optical centre is not the picture centre in cropped pictures; it was scanned and the solution with orthonormal rotation columns kept.
4. The same was done on a real photograph and on frames of a real video, to check that the composites and renders are to scale.

### Results

| Route | Pictures | Foot Ø [mm] |
|---|---|---|
| Ring ratio, official composites | Pikachu, Bisasam, Glumanda, Schiggy on a red box | 44.9, 45.1, 45.2, 44.7 (outer ring edge) · 45.0, 45.1, 45.3, 44.8 (inner edge) |
| Homography + cylinder, official render | Pikachu starter set, 3/4 view | **45.9** (45.5–46.3 over the optical-centre scan) |
| Homography + cylinder, official photograph | child holding a red box with Pikachu | **44.7** (44.3–45.2) |
| Homography + cylinder, official video (real footage, 4K) | Pikachu, Glumanda, Schiggy | **44.2, 44.3, 44.2** (Bisasam frame 42.3: rejected, red reflections on both flanks) |
| Ring ratio, same video frames | same three | 45.8, 46.2, 45.8 |

- **Diameter 45 mm, +2 / −1.5.** The routes differ by about ±1 mm; the scale itself (130 mm width, proportions of the top view) adds about ±2 %.
- Sensitivity: with the picture centre taken as the optical centre the video frames give 48.1–48.3 mm and the render 47.3 mm. Those camera solutions are inconsistent (rotation columns 9–21 % off orthonormal) and, for the video, fit the silhouette worse (rms 0.7–1.0 px against 0.26–0.37 px). The 16:9 clip is a re-framed crop: a 4:5 version of the same take shows more above and below. For the photograph the consistent solution lies at the picture centre.
- **The four feet are identical:** 397.5–401.0 px wide in the four front views, 344.3–347.9 px in the four composites.
- **Height 15 mm ±1.** Fitted height in the render 15.0 mm; a 15 mm cylinder also matches the back rim of the foot in the video frames; the straight part of the side wall is 11.8–12.7 mm, the rest is the rounded top edge.
- **Shape.** Cylinder with a groove around the middle and a rounded top edge. The name plate ("PIKACHU #0025") is a flat field at the front, about 24 mm wide at the top and 32 mm at the bottom (read off an enlarged front view); its lower edge lies 1.0–1.7 mm **inside** the 45 mm circle. A round seat therefore fits; the footprint is not a perfect circle.
- **Underside:** never shown in any picture found. In the photo and the video the foot sits flush on the box, no gap, no feet visible. "Flat" is inferred.

## 4. Height, width, overhang of each figure

Heights include the foot. H/D is the height in units of the foot diameter, so the values scale with §3.

| | Front view: H/D → mm at D = 45 | Video, simple projection at D = 45 | Video, camera model (own scale) | Use |
|---|---|---|---|---|
| Pikachu (ear tip) | 1.557 → 70.1 | 72.5 | 70.1 | **70 ±3** |
| Glumanda (head) | 1.392 → 62.6 | 64.6 | 63.2 | **63 ±3** |
| Bisasam (bulb tip) | 1.378 → 62.0 | 62.8 | (58.5, unreliable frame) | **61 ±3** |
| Schiggy (head) | 1.316 → 59.2 | 61.3 | 59.9 | **60 ±3** |

- The ±3 mm covers the unknown position of the highest point in front of or behind the axis (0.25–0.4 mm of height per mm) and the scale. The front-view result changes by about 0.5 mm over camera elevations from 13° to 25°; the elevation of those pictures could only be narrowed down to that range.
- **Width of the figure above the foot, front view:** Pikachu 36.7, Bisasam 35.4, Schiggy 33.4, Glumanda 31.8 mm.
- **Overhang, front view:** Pikachu's lowered ear tip reaches 1.2 mm beyond the foot's edge, 44 mm above the underside. Schiggy's raised arm reaches 1.0 mm beyond it, 40 mm up. Bisasam and Glumanda stay at least 4.7 mm inside.
- **Overhang, views about 40° off the front** (bundle render, starter-set render, shelf photo): Bisasam, Glumanda and Schiggy inside the foot's silhouette; Pikachu's ear tip about 0.9 mm outside.
- No pure side view exists in the material. Pikachu's tail and Glumanda's tail flame point backwards; in the 40° views they stay inside. A rear overhang of more than about 2 mm is unlikely but not excluded.
- **Envelope Ø 52 mm × 78 mm:** largest radius seen 23.7 mm, plus 2 mm for the unseen direction, on a foot that may be 47 mm; height 70 + 3 mm plus scale.

## 5. Ordinary Tonies: base and size

| Claim | Confidence | Source |
|---|---|---|
| There is no common base. The lion figure stands on a rectangular stack of letters, the Creative Tonie on its two feet. | VERIFIED | photos in https://www.ifixit.com/Teardown/Toniebox+Teardown/106148 (step 10) and https://gt-blog.de/inside-tonie-figurine/ |
| No official size statement for Tonie figures. | — | tonies.com product data, support site searched |
| "The standard Tonie figure is between 6cm and 7cm" | single source | https://www.instructables.com/Custom-Tonie-Audio-Figure/ (step 3) |
| A shelf cell 90 mm high "passt für 90% der Figuren" | single source | https://www.printables.com/model/355564 |
| Holders are built for a footprint of 40–50 mm: 40 mm of shelf per figure; a 50 × 50 mm plate for "standard-sized Tonies", 100 × 50 mm for "wide Tonies"; a double holder for "the bigger tonies like the ones from Disneys 'Cars'" | single sources that agree | https://www.printables.com/model/963244 · https://www.printables.com/model/711414 · https://www.printables.com/model/487455 |
| Counter-plates used under a figure: steel disc Ø 35 × 2 mm, washers Ø 20–25 mm | VERIFIED | https://www.printables.com/model/487455 · https://www.printables.com/model/355564 |
| Retail "dimensions" 200 × 115 × 35 mm (also 19.99 × 10.79 × 3.5 cm) are identical for every Tonie: packaging, not the figure. A 45 mm foot would not even fit the 35 mm. | VERIFIED as packaging | https://www.currys.co.uk/products/tonies-pok%C3%A9mon-audio-figure-squirtle-10307783.html · https://www.bestbuy.ca/en-ca/product/tonies-pokemon-pikachu-tonie-english/20209089 |

Replica bases (not genuine parts): coin Ø 40 mm with a 10 × 3 mm magnet (https://www.printables.com/model/718026); sticker tags Ø 38 mm (https://www.printables.com/model/1197605).

## 6. Mass

| Figure | Listed | Source | Confidence |
|---|---|---|---|
| Pokémon Pikachu, Charmander, Squirtle, Bulbasaur | 40 g each | Best Buy Canada product data, `https://www.bestbuy.ca/api/v2/json/product/<id>?lang=en-CA` for 20209089, 20206753, 20206751, 20206756 (shop page of the first: https://www.bestbuy.ca/en-ca/product/tonies-pokemon-pikachu-tonie-english/20209089) | single source |
| Pokémon Squirtle | 48 g | https://www.currys.co.uk/products/tonies-pok%C3%A9mon-audio-figure-squirtle-10307783.html (the Charmander page shows the same in a search snippet; the page itself was blocked) | single source |
| Four ordinary Tonies | 38, 39, 41, 52 g | alternate.de product pages 1625099, 1584688, 1871918, 1635221 | single source |
| Outliers in the same shop | 100 g, 220 g | alternate.de 1370831, 1883634 | probably with packaging |

Neither retailer says whether the weight includes packaging. Use 40–50 g. "Tonie figures tend to be quite hefty for their size" (Instructables, step 4).

## 7. The magnet, and the Toniebox side

| Claim | Confidence | Source |
|---|---|---|
| Every Tonie contains magnets: "All Tonies contain inaccessible, strong magnets"; "small built-in magnets" | VERIFIED | https://support.tonies.com/hc/en-gb/articles/33106780286866-Magnets-and-the-Toniebox-2 · https://support.tonies.com/hc/en-au/articles/29036575611794 |
| Creative Tonie: **two cylinder magnets, about Ø 6 × 6 mm, one in each foot** | VERIFIED | "Durchmesser und eine Länge von ca. 6 mm", "aus den Füßen" (familie.de, URL below) · "magnets are down in the feet (ø6 x 6mm)" (https://www.printables.com/model/1440336) · "the diameter of the magnets in a Creative Tonie was 6mm" (https://www.printables.com/model/1763980) · pushed out "von unten durch die Füße … rechts und links" (https://www.echtemamas.de/zaubertonies-herstellen/) |
| Other figures: one hollow "right at the bottom of the figurine to hold a small magnet" | single source | https://gt-blog.de/inside-tonie-figurine/ |
| The magnet only holds the figure; the box has no reed or hall sensor for it | VERIFIED | https://www.ifixit.com/Answers/View/595663/ · https://www.mikrocontroller.net/topic/566157 |
| Polarity differs between figures: "it is not guaranteed that the same magnetic pole points downward on all figures" | single source | https://www.supermagnete.de/eng/Magnet-applications/DIY-Tonie-shelf-with-magnets |
| Depth: replica builders put the magnet about 1.5 mm above the underside, or "closer to the surface so the magnets will stick slightly better" | inferred for genuine figures | Instructables (step 3) · https://www.printables.com/model/1763980 |
| Field or holding force of a Tonie magnet | **nothing measured anywhere** | — |
| Number and position of magnets in the Pokémon foot | **not verified** | — |

familie.de: https://www.familie.de/diy/zaubertonie-selber-machen-material-schritt-fuer-schritt-anleitung--01JPW67XN4C3KGAPTCPA3B93S0

**Calculated field of an ideal Ø 6 × 6 mm magnet (Br 1.25 T), vertical component in mT.** Inferred; z = distance below the pole face, ρ = sideways offset of the sensor.

| z | ρ = 0 | 5 mm | 8 mm | 10 mm |
|---|---|---|---|---|
| 3 mm | 151 | 27 | 0.6 | −2.5 |
| 5 mm | 67 | 24 | 5.5 | 1.2 |
| 8 mm | 26 | 14 | 6.4 | 3.2 |
| 10 mm | 16 | 10 | 5.6 | 3.4 |

The DRV5032FB switches at 4.8 mT at the latest (note 04). Directly under a magnet there is a large margin. Ten millimetres to the side there is none at any depth, and at 3–5 mm depth the field passes through zero there. If the Pokémon foot carries two magnets about 20 mm apart, like the Creative Tonie, a single sensor on the axis 2–4 mm below the foot sits in that dead zone. A sensor 6–10 mm below the pole face catches a magnet up to about 8 mm off its axis.

**Toniebox side**

| Claim | Confidence | Source |
|---|---|---|
| Toniebox 1: "Magnets in the top of the Toniebox, and in the sockets of the Tonies, to keep them stuck together while you tilt and turn the box" | single source | iFixit teardown, step 1 |
| Toniebox 1: the figure stands on a coloured **rounded-square** pad in the white top plate, not on a round spot. The pad is about 0.6 of the plate wide and shifted away from the ears; roughly 55–65 mm if the plate is about 108 mm. Flush or recessed could not be decided. | inferred from one oblique photo | iFixit teardown, step 2 photo |
| Toniebox 1: the antenna is a frame along the edge of the top, not a small coil under the figure (about 100 mm across, estimated from the photo) | single source | iFixit teardown, step 8 photos |
| Toniebox 2: flat white top, 106.7 mm wide; light ring inner Ø 68 mm, outer Ø 76 mm, 6.5 mm off-centre away from the ears; no recess visible | inferred from the official top view | https://tonies.com/de-de/toniebox-2/toniebox-2-hellblau/ |
| Toniebox 2 also holds by magnets; NFC at 13.56 MHz | single source (maker) | support article above · https://tonies.com/ecodesign/ |
| On a real Toniebox 2 the foot sits 5.6 mm (photo) and 1.8, 1.8 and 4.0 mm (video frames) from the ring centre. The magnets hold the figure where it is put down; they do not centre it. | inferred | pictures P4, V033, V081, V121 |
| Builders of replica figures use two 10 × 3 mm N52 magnets, otherwise "the figure will slide away from the toniebox" | single source | https://www.printables.com/model/931388 |

No teardown of a Toniebox 2 was found.

## 8. Where the RFID tag sits

| Claim | Confidence | Source |
|---|---|---|
| The tag is a small **ferrite rod with a wound coil** and the chip at one end; "looks a bit like an glas transponder … but without the glas tube" | VERIFIED | photos in iFixit teardown step 10 and in https://gt-blog.de/inside-tonie-figurine/ · "Ferritkern mit Spule" (https://www.mikrocontroller.net/topic/566157) · rebuilt from a 5.6 µH drum inductor (Bourns RLB0608-5R6KL) and an SL2S5002 chip "more like the original Tonies" (https://forum.revvox.de/t/selfmade-slix-l-tags/477) |
| Size: "1 cm lang und weniger als 4 mm dick"; holes of Ø 4.6 mm (bare) and Ø 6.4 mm (with rubber) take it | VERIFIED | familie.de · https://www.printables.com/model/1440336 |
| It stands **upright** and must stay upright: "Der Chip muss senkrecht eingebaut werden" | VERIFIED | familie.de · https://ganzschoenlaut.de/zaubertonies-herstellen/ · https://www.isteshaltbar.de/frage-und-antwort/wo-ist-der-chip-im-tonie |
| Position: a second hollow "at about 20mm higher location" than the magnet; in the lion "just beneath the neck" | single source with photo | https://gt-blog.de/inside-tonie-figurine/ |
| Creative Tonie: behind the face plate or in the head, about 50 mm above the base | VERIFIED | Instructables (steps 1, 4) · https://www.printables.com/model/1440336 · familie.de |
| One source places it lower: "Fuß der Figur, in dem sich deren Chip befindet" | single source, contradicts the teardowns | https://help.oclc.org/Library_Management/BIBLIOTHECAnext/Troubleshooting/Tonies_und_RFID-Verbuchung_Besonderheiten |
| A Toniebox reads such a rod tag from **2 mm to 75 mm** above its top; lying directly on the box it fails ("min. 2 - 3mm") | VERIFIED for the lower limit, single source for 75 mm | forum.revvox.de/t/477 (post 19) · mikrocontroller.net topic 566157 |
| A magnet close under the rod stops it: about 1 cm above a 10 × 3 mm magnet "the chip is not recognized"; keep it "1-2 cm … von den Magneten entfernt", offset sideways | VERIFIED | forum.revvox.de/t/477 (post 10) · familie.de |
| The tags are "Sonderformen … Der Empfang … ist sehr begrenzt und rein für die Toniebox abgestimmt" | single source | comment by the author of gt-blog.de, 16 July 2021 |
| **Pokémon Tonies carry UIDs beginning `E0:04:03:50`** (NXP ICODE SLIX-L, as every Tonie), shown for Bisasam, Glumanda and Schiggy in a TeddyCloud screenshot | single source | https://forum.revvox.de/t/4381 (7 Nov 2026) |
| Where the rod sits in a Pokémon Tonie | **not verified.** The 15 mm foot is tall enough for an upright 10 mm rod; whether it is there or up in the figure is unknown. | — |

## 9. Do Tonies overhang their base, and what envelope is safe?

- **The four Pokémon Tonies:** no, within 1.2 mm (§4). Envelope **Ø 52 mm × 78 mm**.
- **Ordinary Tonies:** they have no common base to overhang; the figure is the footprint. Most fit a 40–50 mm square and 90 mm of height; "wide" figures such as the Disney Cars need about 100 × 50 mm (§5). A cylinder of about Ø 65 mm × 100 mm holds the usual figure. No cylinder is known to hold every one, and no list of sizes exists.

## 10. What this changes elsewhere (other files were not edited)

1. `params.py` assumes `TONIE_BASE_D = 36` and `TONIE_H = 75`. For the Pokémon figures the foot is 45 mm and the tallest figure 70 mm.
2. Note 01 §5 and README open point 3 describe a flat tag inlay of up to 39 mm with a centred 10 mm magnet in the base. That is the layout of replica bases. Genuine Tonies carry an upright rod tag and Ø 6 mm magnets.
3. README open point 2 counts 10.6 mm from antenna to figure. The tag may sit 20–50 mm higher than the underside, and it is a rod that couples to the vertical field on the axis.
4. README open point 1 (tag type of the 2026 figures): the UID prefix `E0:04:03:50` in the forum screenshot is the first direct evidence for SLIX-L. Still a single source.
5. Hall switch at the dock (note 04 §5): its position has to follow the magnets, which are not located yet (§7).

## 11. Not verified

1. The **underside** of a Pokémon Tonie: flat or not, any marking, any opening. No picture found.
2. **Number, size, position and polarity of the magnets in the Pokémon foot.** Everything in §7 comes from Creative Tonies and older figures.
3. **Height of the tag** in a Pokémon Tonie, and whether a 40 mm reader antenna reaches it.
4. The absolute scale: every length rests on the 130 mm width of the Toniebox 2 and on the proportions of one official top view. Nobody has put a calliper on a Pokémon Tonie in any source found.
5. Overhang seen exactly from the side, in particular Pikachu's tail and Glumanda's tail flame.
6. Bisasam's height from the video (one frame, disturbed by reflections); it rests on the front view.
7. Mass: 40 g or 48 g, with or without packaging.
8. Field and holding force of the magnets; the table in §7 is a calculation for an ideal magnet.
9. Size of the pad on the first Toniebox and whether it is recessed; the inside of a Toniebox 2.
10. Statements seen only as search-result snippets, pages not opened: Etsy replica bases "35 mm × 14.5 mm" and "2 in × 7/8 in"; MakerWorld base "Ø 50 mm"; a chip test distance of "3 to 4 cm" in a blog post that is offline.

## 12. Local evidence (third-party material, untrusted; do not execute)

- `research/reference_images/tonie_figures/` — 19 measured pictures and video frames, `SOURCES.md`, `overlays/`.
- `research/downloads/tonie_figures/tonies_de/` — the tonies.com product pages with their embedded data.
- `…/tonies_landing_media/` — the official clip the video frames come from; `…/tonies_product_images/` — further official stills, looked at only.
- `…/ifixit_teardown/`, `…/gtblog_inside_tonie/` — teardown text and photos of the rod tag.
- `…/familie_zaubertonie/`, `…/zaubertonie_guides/`, `…/instructables_custom_tonie/`, `…/printables_api/` — conversion guides and model descriptions quoted above.
- `…/revvox_forum_477/`, `…/revvox_forum_4381/`, `…/revvox_forum_342/`, `…/mikrocontroller_566157/`, `…/oclc_help/`, `…/supermagnete/`, `…/tonies_support/` — forum threads and support pages.
- `…/retail_currys/`, `…/retail_bestbuy_ca/`, `…/retail_alternate/` — retailer listings used for mass and packaging size.
