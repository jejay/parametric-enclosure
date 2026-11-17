# Tonie figure reference pictures — sources

All files were downloaded on **2026-11-17** with `curl` and a browser User-Agent. They are third-party,
copyrighted pictures (© tonies GmbH; Pokémon © Nintendo / Creatures Inc. / GAME FREAK inc.) kept only as
private measurement references — do not redistribute them with the project. They are untrusted downloads:
they were only decoded (Pillow; the video with Blender's sequencer), never executed.

Results and discussion: `../../09_tonie_figure_dimensions.md`.

Image host for all stills: `https://images.cdn.europe-west1.gcp.commercetools.com/cffb5678-47af-495c-9f19-1c2ccfc5910c/`
(file name given per row). The file lists come from the product data embedded in the shop pages
(`__NEXT_DATA__`), saved under `../../downloads/tonie_figures/tonies_de/`.

## Measured pictures

| file | what it is | source (file name on the image host · shop page) | what was measured |
|---|---|---|---|
| `T6_toniebox2_top_blue.png` | Toniebox 2, official top view (render, 1200×900, transparent background) | `Tonies_Box_Top_blau_-MvvFb--w.png` · https://tonies.com/de-de/toniebox-2/toniebox-2-hellblau/ | Scale: outer width 694.0 px = 130 mm (official size). White panel 106.7 mm wide, corner radius ≈ 19.7 mm; light ring inner Ø 68.0 mm, outer Ø 76.0 mm, centre 6.5 mm from the panel centre away from the ears. This is the metric model for every other picture. |
| `T2_toniebox2_frontal_b.png` | Toniebox 2, official frontal view | `Tonies_Box_Frontal_b-WYTK1jPx.png` · same page | Width / height of the body = 591 / 585 px = 1.010 (official 130 / 126 = 1.032; the difference is explained by a camera about 1° above the horizon). Check only. |
| `P1_pikachu_front.png`, `B1_bisasam_front.png`, `G1_glumanda_front.png`, `S1_schiggy_front.png` | Official "Vorderansicht" of the four Pokémon Tonies (1200×900, transparent background, soft shadow) | `50005354-Tonie_Shado-Cw3EvupV.png`, `51020902-Tonie_Shado-pkPK_-JW.png`, `51020910-Tonie_Shado-2AEOeGeW.png`, `51020918-Tonie_Shado-Y92mrUcF.png` · https://tonies.com/de-de/tonies/pokemon/{pikachu,bisasam,glumanda,schiggy}/ | Base width (397–401 px, identical base on all four), total height and lateral extent of the figure in units of the base diameter, straight height of the base's side wall, deviation of the nameplate edge from the base circle. |
| `P2_pikachu_on_toniebox.png`, `B2_bisasam_on_toniebox.png`, `G2_glumanda_on_toniebox.png`, `S2_schiggy_on_toniebox.png` | Official "Vorderansicht auf Toniebox": the figure composited onto a red Toniebox 2 (1200×900) | `50005354-Tonie_Tonie-kH82PxNy.png`, `51020902-Tonie_Tonie-MKu89WmM.png`, `51020910-Tonie_Tonie-yHqVan9F.png`, `51020918-Tonie_Tonie-l7t5rKV-.png` · same pages | Ellipses fitted to the outer and inner edge of the light ring (a = 292.9 / 261.3 px, view elevation 13.1°); base width 344.3–347.9 px → base Ø 44.7–45.3 mm. |
| `X3_starterset_pikachu_on_yellow_box.png` | Official picture of the Pikachu starter set, 3/4 view from above (render, 1200×900) | `PDP_DE-q4XTk54A.png` · https://tonies.com/de-de/toniebox-2/pikachu-toniebox-2-starter-set-blitzgelb/ | Plane homography of the box top from the white-panel outline (319 points, rms 0.14 mm; light ring lands 0.2 mm from its predicted radius). Cylinder fitted to the base silhouette: Ø 45.9 mm, height 15.0 mm. |
| `P4_pikachu_lifestyle_toniebox2.png` | Official lifestyle **photograph**: child holding a red Toniebox 2 with the Pikachu Tonie (2000×2000) | `SKU_Square_2%20%281%29-BCiSG0XV.png` · https://tonies.com/de-de/tonies/pokemon/pikachu/ | Same method on a real photo: homography from 222 outline points (rms 0.12 mm; lit ring 0.14 mm from its predicted radius). Cylinder fit of the base: Ø 44.7 mm (44.3–45.2 depending on the assumed optical centre). Base centre 5.6 mm away from the ring centre. |
| `V057_video_empty_box_top.jpg` | Frame 57 of the official 5-second clip (3840×2160): yellow Toniebox 2, top empty, ring lit | https://videos.ctfassets.net/l6vo76cztcax/7gSdweg8zyIA50AP0yLtvw/ca8238f98820ff01cc2053de63461619/5Sek_All_Pokemon_16x9.mp4 (hero video of https://tonies.com/de-de/pokemon/) | Homography of the box top (201 outline points, rms 0.38 mm); ellipse through the middle of the lit ring: a = 211.1 px, b = 50.0 px (elevation 13.7°). |
| `V033_video_pikachu_on_box.jpg`, `V053_video_bisasam_on_box.jpg`, `V081_video_glumanda_on_box.jpg`, `V121_video_schiggy_on_box.jpg` | Frames 33, 53, 81, 121 of the same clip: each figure standing on the box, hand out of the way (real footage, fixed camera) | same video | Base silhouette width 268.4 / 259.7 / 270.8 / 268.8 px; cylinder fit with the homography of frame 57: Ø 44.2 / (42.3) / 44.3 / 44.2 mm; height of the highest point of each figure. Frame 53 is unreliable: red reflections on both flanks of the base pull the detected edges inwards. |
| `X1_bundle_box_and_four_tonies.png` | Official picture of the bundle: three figures standing next to the box (render, 1200×900) | `51009656-DACH-110022-APftpBVm.png` · https://tonies.com/de-de/bundles/pokemon-toniebox-2-starter-set-blitzgelb/ | Lateral extent of Bisasam, Glumanda and Schiggy against the vertical edges of their own base, seen about 40° off the front: all inside. |
| `X2_bundle_lifestyle.png` | Official lifestyle **photograph** of the bundle on a shelf (1200×900) | `PDP_DE%20%282%29-2FFOUv7m.png` · same page | Same comparison for Bisasam and Schiggy on a real photo: both inside the base width. |

`overlays/` holds the check pictures written by the measuring scripts (JPEG): fitted ring ellipses and base
width (`*_onbox_overlay`), panel outline in cyan and predicted ring in yellow (`*_rectify_overlay`), fitted
cylinder in magenta with its footprint in cyan (`*_puck3d_overlay`), front-view extents (`*_front_overlay`; the
yellow ellipse there marks the upper end of the straight side wall, not the top rim). All were looked at.

## How the video frames were obtained

There is no ffmpeg on this machine. The clip was decoded with the installed Blender 4.5 in background mode
(`blender --background --factory-startup --python blender_frames.py -- VIDEO OUTDIR STEP`), which loads the
file as a movie strip and writes numbered JPEGs (quality 92). Frame numbers are 1-based, 25 frames per second.
A 4:5 version of the same footage exists on the same page (`Tonies_Pokemon_5s_Collectability_4x5_…mp4`); it
shows more of the scene above and below, so the 16:9 file is a re-framed crop and its optical centre is not
the picture centre.

## Pictures that were only looked at

Kept in `../../downloads/tonie_figures/`:

* `tonies_product_images/` — the remaining official stills of the four figures and of the Toniebox 2
  (in-hand photos, booklet pictures, other box views). The in-hand photos show a child's hand and give no scale.
* `tonies_landing_media/` — the video itself and three stills from https://tonies.com/de-de/pokemon/.
* `ifixit_teardown/` — photos of the iFixit Toniebox teardown (lion figure opened, top of the first Toniebox,
  antenna board). `gtblog_inside_tonie/` — photos of an opened Creative Tonie and its tag.

## Not obtained

* Any picture of the **underside** of a Pokémon Tonie, a pure side view, or a picture with a ruler.
* MakerWorld, Cults3D, Galaxus, Kohl's, John Lewis and us.tonies.com product pages (HTTP 403 / 429 for curl
  and for the fetch tool). Thingiverse (API needs a token). The "Daruma Magic Tonie" blog post is offline and
  not in the Wayback Machine.
* A teardown of a Toniebox 2 or of a Pokémon Tonie.

## Scripts

The scripts are kept in `research/scripts/note09_tonie_figures/`. They were written for a scratch directory, so the
picture paths have to be given anew. They read the pictures with Pillow only and were run as `uv run python -I -B SCRIPT ARGS`
from the repo root. What each one does, so that it can be rebuilt:

* `topmodel.py` — top view → metric model: panel outline as radius over angle, ring centre and radii.
* `measure_onbox.py` — axis-aligned ellipse fits to the ring edges; base width from the rows where the dark run
  through a seed column has constant width. Seeds / rows used: P2 576 / 545–590, B2 565 / 562–582,
  G2 570 / 546–586, S2 566 / 554–582.
* `rectify_top.py` — locates the white-panel outline (and the lit ring as a check) near a predicted position and
  fits a plane homography (8 parameters, soft-L1) so that the points fall on the model outline. Start corners:
  X3 `368,345 690,435 805,300 505,232`; P4 `840,1313 1467,1203 1343,1023 933,1053`;
  V057 `1565,1115 1780,1265 2410,1165 2150,1050`.
* `puck3d.py` — recovers the camera from the homography (square pixels; the optical centre is scanned and the
  solution with orthonormal rotation columns is kept), then fits an upright cylinder so that the convex hull of
  its projected bottom and top circles passes through the left, right and lower silhouette points of the base.
  Silhouette boxes (x0,x1,y0,y1): X3 left `505,540,272,312`, right `665,700,272,300`, bottom `526,578,300,362`,
  optical centre `310,450`; P4 left `955,1010,1140,1154`, right `1190,1250,1112,1152`, bottom
  `1046,1116,1180,1245`, optical centre `1000,1000`; video frames: optical centre `1400,1080`, boxes around
  x = 1804 / 2073 (left / right edge) and y = 1175 (front of the footprint).
* `measure_front.py`, `puck_profile.py` — front views: base width, top of the figure, lateral extent, lower
  silhouette against the footprint ellipse.
* `ring_ellipse.py`, `video_measure.py`, `bbox_overhang.py` — ring ellipse in the video frame, weak-perspective
  heights, figure width against base width in the 3/4 views.
* `magnet_field.py` — field of an ideal cylinder magnet (surface-charge model); no picture involved.
