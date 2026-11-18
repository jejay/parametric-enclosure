"""Single source of truth for every dimension of the Poké Ball device.

All values are millimetres / degrees.  Each block names the research file in
``research/`` that justifies the purchased-part dimensions.  Values marked
``MEASURE`` are tolerance-critical or were not verifiable from two sources:
measure the delivered part and adjust here, then re-run
``uv run poketonieengagementhunt all``.

Coordinate system: origin = ball centre, +X front (button), -X back (hinge),
+Z up (red lid), +Y left.
"""

from __future__ import annotations

import math

# ==========================================================================
# 1. Exterior (research/03_pokeball_proportions.md)
# ==========================================================================
D = 100.0                     # outer diameter of the ball
R = D / 2

# Ratios measured on seven reference sources; the official The Wand Company
# replica is the anchor (band 0.070 D, ring ~D/3, flat ring/collar pocket with
# the button top roughly flush with the sphere).
BAND_H = 0.070 * D            # height of the black equatorial band
HB = BAND_H / 2               # half band height; the lid seam is at z = +HB
BAND_RECESS = 0.012 * D       # band surface sits this far below the sphere
R_BAND = R - BAND_RECESS

BEZEL_R = 0.170 * D           # outer radius of the black ring around the button
LENS_R = 0.1125 * D           # radius of the white (translucent) flat rim
BTN_R = 0.070 * D             # radius of the central raised button
BEZEL_PROUD = 0.3             # ring face above the flat facet of the sphere
BTN_PROUD = 0.023 * D         # central button stands this far above the flat rim

T_LID = 2.0                   # red lid wall
T_BOWL = 2.2                  # white bowl wall
RI_LID = R - T_LID
RI_BOWL = R - T_BOWL
T_BAND = 1.6                  # black band wall thickness
RI_BAND = R_BAND - T_BAND     # inner radius of the band wall (cylindrical)

FLAT_CUT = 3.0                # the bottom pole is flattened by this much
Z_FLAT = -(R - FLAT_CUT)      # outer bottom plane: the foot the ball stands on by itself
FLOOR_T = 2.0                 # floor thickness above the flat
Z_FLOOR = Z_FLAT + FLOOR_T    # inner floor plane
R_FLAT = math.sqrt(R**2 - Z_FLAT**2)   # radius of the flat (17.1 for D=100)

# print/fit clearances (research/06_mechanics_printing_ring.md §5.1)
CL = 0.25                     # general sliding / mating clearance per side
CL_TIGHT = 0.15               # locating fits
CL_MOVE = 0.40                # clearance to moving parts
SEAM_GAP = 0.20               # nominal visible gap lid <-> bezel / band features

# ==========================================================================
# 2. Core stack-up along Z (all printed, see parts.py)
#
#   bowl bosses (inserts)  top at z = -HB
#   chassis flange         z = -HB .. 0      rests on the bosses
#   band lugs              z = 0 .. LUG_T    rest on the chassis flange
#   stage screw pads       sit on the lugs; M3 x 16 screws clamp the stack
# ==========================================================================
Z_BOWL_RIM = -HB              # white bowl ends here, black band starts
Z_CHASSIS_TOP = 0.0           # top of the chassis flange = bottom of the stage
R_FLANGE_IN = 40.0            # inner radius of the stacked flanges
R_CORE = RI_BAND - CL         # outer radius of the stage base inside the band
R_SPIGOT_OUT = 47.3           # band spigot: locates the band in the bowl rim
R_SPIGOT_IN = 45.9
R_CHASSIS_FLANGE = 45.6       # chassis flange radius (clears the band spigot)

SCREW_R = 43.6                # radius of the four M3 stack screws
SCREW_AZ = (55.0, 100.0, 260.0, 305.0)   # azimuths (deg from +X) of the screws
M3_CLEAR = 3.4
M3_HEAD_D = 6.2               # ISO 4762 head Ø5.5 + clearance
M3_HEAD_H = 3.0
# Heat-set inserts M3 from the owner's stock: 5.0 mm over the knurl, 6 mm long at the rim and 5 mm long in
# the lower bosses.  Inserts of 4.6 mm (ruthex / CNC Kitchen M3 x 5.7) need M3_INSERT_HOLE = 4.0 instead.
M3_INSERT_D = 5.0
M3_INSERT_HOLE = 4.4          # hole for an insert of Ø5.0 (research/06 section 4.1)
M3_INSERT_WALL = 1.3          # least wall round that hole (same source)
M3_INSERT_L = 6.0             # inserts at the rim of the bowl, for the stack screws
M3_INSERT_DEPTH = M3_INSERT_L + 1.0
STACK_SCREW_L = 16.0          # M3 x 16 ISO 4762
BOSS_R = 4.2                  # radius of the insert bosses in the bowl
BOSS_DEPTH = 11.0             # boss height below the bowl rim
# M2 machine screws that form their own thread in a printed pilot hole (research/06 section 4.2).
# The right pilot depends on how the hole lies in the print:
M2_PILOT_FLAT = 1.95          # mouth of the hole parallel to the print bed (hole axis upright)
M2_PILOT_SIDE = 1.70          # mouth of the hole in an upright wall of the print (hole axis level)
M2_LEAD = 0.3                 # chamfer at the mouth of a pilot hole; it does not count as thread
M2_ENGAGE = 4.0               # thread that an M2 screw needs in the print
M2_CLEAR = 2.4
M2_HEAD_D, M2_HEAD_H = 4.0, 2.0   # room for the head of any M2 cap or pan head screw
                              # (ISO 4762: 3.8 x 2.0; ISO 7045: 4.0 x 1.6)
CLAMP_SCREW_L = 8.0           # M2 x 8: speaker clamp
PAWL_SCREW_L = 6.0            # M2 x 6: pawl pivot
LUG_T = 1.2                   # band lug thickness at its inner tip
LUG_R_IN = 40.6               # inner radius of the band lugs
LUG_HALF_DEG = 7.0            # angular half width of a lug
SPIGOT_H = 1.8                # band spigot reaching down into the bowl
STAGE_PAD_Z = 6.5             # screw head seat height on the stage

# stage (inner dome carrying ring, hinge and latch)
STAGE_GAP = 2.0               # radial gap between lid inner wall and stage dome
R_STAGE = RI_LID - STAGE_GAP  # outer radius of the stage dome
T_STAGE = 2.0
RI_STAGE = R_STAGE - T_STAGE
Z_DECK = 28.0                 # top of the ring deck
DECK_T = 2.4
BACK_RELIEF_R = 10.0          # stage is cleared within this radius of the hinge axis
BACK_RELIEF_Y = 30.0          # ... over this half width
LID_LIP_R = 47.4              # inner radius of the stiffening lip at the lid rim
LID_LIP_H = 2.5
R_COLLAR = LID_LIP_R - 0.35    # lid centring collar radius
COLLAR_H = 1.6                # collar height above the seam
COLLAR_AZ = 115.0             # the collar only exists within +-this azimuth of the front

# ==========================================================================
# 3. Hinge (research/06 §2.1, §3)
# ==========================================================================
HINGE_E = 7.0                 # hinge axis height above the seam plane
HINGE_Z = HB + HINGE_E
# The hinge axis lies inside the lid, and the lid's wall closes it at both ends: beside each hinge tower a
# Ø2 pin has only 4 mm of room, so one long pin cannot be put in.  Two short pins are used.  Each is pressed
# into its tower from outside until it is flush with the tower's inner face and waits there, standing out of
# the tower, while the lid is put on; then both are pressed in the rest of the way.
HINGE_PIN_D = 2.0             # two steel dowel pins Ø2 x 8 (ISO 2338)
HINGE_W = 20.0                # width over the two hinge towers; it sets how far back the hinge can sit
HINGE_PIN_L = 8.0
HINGE_PIN_Y1 = HINGE_W / 2 - 0.2            # outer end of a mounted pin: flush with the outer face of its tower
HINGE_PIN_Y0 = HINGE_PIN_Y1 - HINGE_PIN_L   # inner end, inside the spring sleeve
HINGE_BORE = 2.3              # rotating bore for the Ø2 pin (ribs of the lid, spring sleeve)
HINGE_PRESS = 1.95            # press-fit bore for the Ø2 pin (hinge towers)
HINGE_RECESS_Y = 16.5         # the inside of the lid wall is relieved up to this distance from the middle ...
HINGE_RECESS_WALL = 1.3       # ... down to this wall thickness: room for the two waiting pins
HINGE_RECESS_TOP = 2.5        # the relief ends this far above the hinge axis; below, it runs out through the rim
HINGE_MOUNT_DEG = 65.0        # the lid is held about this far open while it is slid onto the hinge
KNUCKLE_R = 2.7               # outer radius of the printed knuckles
LID_WALL_AT_HINGE = 1.0       # the lid wall is locally thinned behind the hinge
SPRING_OD = 6.7               # Gutekunst T-16324: d 0.7, Di 5.3, De 6.7, 7 coils
SPRING_ID = 5.3
SPRING_WIRE = 0.7
SPRING_BODY = 5.6
SPRING_LEG = 14.0             # legs trimmed from 35 mm
SPRING_SLOT = 6.6             # axial room for the coil
SLEEVE_OD = 4.5               # mandrel sleeve on the pin (catalogue 4.3-4.7)
LID_RIB_T = 3.4               # each lid knuckle rib
LID_TAB_LEN = 8.5             # stop tab on each rib
LID_TAB_DEG = -60.0           # tab direction when the lid is closed
STAGE_KNUCKLE_T = 3.0         # each stage knuckle
LID_OPEN_DEG = 95.0           # opening angle at the end stop
SPRING_DEFL_CLOSED = 115.0    # spring wind-up with the lid closed (<= 80 % Mn)

# Hinge axis x: as far back as possible.  Two limits apply inside the locally
# thinned lid wall: the knuckles at the pin ends and the spring coil at the
# centre must both keep clear of the wall.  The smaller distance wins.
_r_wall = math.sqrt((R - LID_WALL_AT_HINGE) ** 2 - HINGE_Z**2)
_w_half = HINGE_W / 2
HINGE_X = -min(
    math.sqrt((_r_wall - KNUCKLE_R - 0.35) ** 2 - _w_half**2),
    _r_wall - SPRING_OD / 2 - 0.5,
)

# ==========================================================================
# 4. Latch (servo-released pawl) and SG90 servo (research/05 §1, §8.1)
# ==========================================================================
SG90_L, SG90_W = 22.7, 11.8           # body (spread 22.0-23.2 x 11.5-12.5)
SG90_POCKET_L, SG90_POCKET_W = 23.8, 12.9
SG90_SHAFT_OFF = 5.9                  # shaft axis from the near body end
SG90_FLANGE_SPAN = 32.1               # (spread 31.9-32.6)
SG90_FLANGE_T = 2.5
SG90_FLANGE_Z = 15.9                  # flange underside above the body base
SG90_CASE_Z = 22.7                    # top of main case
SG90_GEAR_Z = 26.7                    # top of gear case (spread to 27.3)
SG90_SPLINE_Z = 29.9                  # tip of output spline (spread 29.0-30.3)
SG90_HORN_TOP_Z = 32.0                # with stock horn and screw
SG90_HOLE_PITCH = 27.4                # mounting holes (spread 27.0-27.4)
SG90_ARM_Z0, SG90_ARM_Z1 = 27.6, 30.3  # height band swept by the stock horn arm
SG90_ARM_LEN = 13.0                   # the stock single arm (~19-21 mm) is TRIMMED to this radius
SG90_ARM_W = 5.0                      # arm width near r = 9 mm                    MEASURE

SERVO_X, SERVO_Y = 11.0, 0.0          # output-shaft axis position
SERVO_BASE_Z = -9.5                   # bottom of the servo body
HORN_REST_DEG = -35.0                 # horn arm direction, lid latched (from +X, CCW)
HORN_RELEASE_DEG = -5.0               # horn arm direction that frees the lid

PAWL_PIVOT = (27.0, 0.0)              # vertical pivot of the pawl
PAWL_Z1 = Z_DECK - DECK_T - 0.8       # pawl plate top (just under the deck)
PAWL_Z0 = PAWL_Z1 - 2.8               # pawl plate bottom = latch face
PAWL_NOSE_X = 9.2                     # nose reach in front of the pivot
PAWL_TAIL_X = 7.0                     # tail post distance behind the pivot
PAWL_POST_R = 1.5
PAWL_POST_Z0 = SERVO_BASE_Z + SG90_ARM_Z0 - 0.5   # post spans the horn arm band
PAWL_RELEASE_DEG = 24.0               # pawl rotation that frees the lid hook
PAWL_BOSS_D = 5.0                     # printed pivot boss under the deck
PAWL_BORE = 5.3
PAWL_CAP_D, PAWL_CAP_T = 7.0, 0.6     # printed pivot washer: its flange keeps the pawl on the boss ...
PAWL_CAP_HUB_D, PAWL_CAP_HUB_T = 4.4, 0.9   # ... and its hub takes up the rest of the screw's length
TOOTH_H = 3.0                         # lid hook tooth height at the stem
TOOTH_REACH = 2.8                     # tooth overlap under the pawl nose (in -Y)
HOOK_X0, HOOK_X1 = 33.9, 36.9         # lid hook stem, x range
HOOK_W = 3.0                          # stem thickness in y
HOOK_Y = 1.7                          # stem centre y (tooth points to -y)
LATCH_GAP = 0.15                      # vertical play between tooth and pawl

# ==========================================================================
# 5. Ring (research/06 §1) and its lock
# ==========================================================================
RING_ID = 15.6                # EU size 49: 49 mm circumference / pi
RING_BAND = 2.5               # owner: "diameter 2.5 mm" = band width / wire  MEASURE
RING_THICK = 1.8              # radial band thickness (typ. 1.2-2.0)          MEASURE
RING_HEAD_H = 6.5             # setting height above the band outside (typ.)   MEASURE
RING_STONE_D = 5.2            # 0.5 ct round brilliant ~5.0-5.2 mm             MEASURE
RING_X = -3.0                 # the ring plane (y-z) sits slightly behind centre
RING_SLOT_W = RING_BAND + 1.2 # slot width incl. 2 x 0.5 mm felt + clearance
CRADLE_X0, CRADLE_X1 = RING_X - 6.0, RING_X + 6.0
CRADLE_Y = 13.0               # cradle half length (y)
CRADLE_DEPTH = 12.0           # cradle body below the deck top
LOCK_PIN_D = 3.0              # steel dowel pin through the ring
LOCK_PIN_DEPTH = 5.0          # pin axis below the deck top
# The ring is sunk so far that the lock pin passes 0.3 mm above the inside of
# the band: locked, the ring cannot be lifted more than that.
RING_SINK = LOCK_PIN_DEPTH + LOCK_PIN_D / 2 + 0.3 + RING_THICK
LOCK_TRAVEL = 7.0             # slider travel between locked and released
LOCK_PIN_L = 25.0             # Ø3 x 25 dowel pin (ISO 2338) pressed into the slider; 25 is a stock length, 24 is not.
                              # The extra millimetre lies at the rear end; the tip positions are unchanged
LOCK_TIP_X = RING_X + 4.0     # pin tip when locked (inside the cradle front wall)
LOCK_STEM_X = (-21.5, -16.5)  # slider stem when locked
LOCK_Z = Z_DECK - LOCK_PIN_DEPTH

# ==========================================================================
# 6. Front module: bezel, lens, light cone, LED, speaker (research/04 §3, §4)
# ==========================================================================
SPK_D = 40.0                  # Visaton K 40: Ø40 ±0.2, depth 4.3 ±0.3
SPK_DEPTH = 4.3
SPK_RIM_T = 1.3
SPK_BASKET_D = 36.0
SPK_CUP_D = 16.0
SPK_X_FRONT = 33.0            # x of the speaker front (rim) face
SPK_Z = -4.0                  # speaker axis height (lowered to clear the latch)
SPK_OPEN_D = 34.0             # front chamber bore in front of the cone
BAFFLE_X1 = SPK_X_FRONT + 5.2 # front face of the chassis baffle block
CHAMBER_X1 = SPK_X_FRONT + 2.0   # front chamber: SPK_X_FRONT .. CHAMBER_X1
BEZEL_X_FACE = math.sqrt(R**2 - BEZEL_R**2) + BEZEL_PROUD   # flat face of the black ring
BEZEL_X_BACK = CHAMBER_X1 + 0.4                     # rear end of the bezel tube
BEZEL_WALL = 1.6              # bezel tube wall
BEZEL_FACE_T = 2.2            # thickness of the slotted face plate
SLIT_W = 2.0                  # sound slit width in the black ring
SEAT_R0 = LENS_R + 0.75       # lens seat tube: inner radius (lens flange pocket)
SEAT_R1 = SEAT_R0 + 0.9       # ... outer radius
SLIT_R = (SEAT_R1 + BEZEL_R - BEZEL_WALL) / 2   # mid radius of the slits
SLIT_ARC = 68.0               # each of the four slit arcs spans this angle
LED_PCB_D = 10.0              # single WS2812B/SK6812 mini PCB Ø10 x 3.2
LED_PCB_T = 3.2
LENS_T = 1.6                  # translucent flat rim thickness
LENS_FLANGE_R = LENS_R + 0.62 # lens retaining flange behind the face plate
LENS_SEAT_X = BEZEL_X_FACE - 1.9   # flat seat for the lens flange
LED_X = SPK_X_FRONT + 5.8     # x of the LED emitting face
EMERGENCY_YZ = (-6.2, 12.55)  # where the paper clip enters the upper slit (on SLIT_R)
EMERGENCY_SLOPE_DEG = 22.0    # the clip is pushed in rising by this angle

# ==========================================================================
# 7. Electronics (research/02, 04, 05)
# ==========================================================================
# Blue "PN5180-NFC" reader board, R1.1-170710 (research/08 section 0; no
# manufacturer drawing exists: the values come from two community models and
# from photos of two to three boards, scaled by the header pitch).
# Local board frame: x along the long side, measured from the header-end edge;
# y across, measured from the long edge next to pin 1.  The board lies in the
# grass tongue (section 9), component side down, plain side against the turf.
BLUE_L, BLUE_W, BLUE_T = 69.6, 38.6, 1.6           # +-0.4 / +-0.2 / +-0.15          MEASURE
BLUE_ANT_X = 48.8             # antenna centre from the header-end edge, +-0.5      MEASURE
BLUE_ANT = (28.3, 69.2, 0.4, 38.1)                  # antenna copper, outer extent: x0, x1, y0, y1
BLUE_HOLES = ((25.9, 2.3), (25.9, 36.3), (62.9, 6.8), (62.9, 31.8))   # not used for mounting
BLUE_HOLE_D = 3.3
BLUE_HDR_X = 2.6              # row of the 13 header holes, from the edge (2.3-2.6)
BLUE_PIN1_Y = 4.05            # pin 1 (+5V); 13 holes at 2.54 pitch
BLUE_COMP_X = (4.0, 28.5)     # every component lies in this strip of the component side
BLUE_COMP_H = 1.3             # tallest of them (inferred from photos)             MEASURE
BLUE_CL_X, BLUE_CL_Y = 0.5, 0.35                    # pocket clearance per side: takes a board up to 70.0 x 39.0
BLUE_LEDGE = 1.0              # the board rests on a ledge this wide beside its components ...
BLUE_LEDGE_ANT = 2.5          # ... and this wide under its antenna half, which is bare on both sides

# 18650 cell, unprotected flat top (research/05 §2)
CELL_D, CELL_L = 18.6, 65.3
CELL_AXIS = (-5.0, -15.0)     # (x, z) of the cell axis; the cell lies along Y
CELL_CONTACT = 2.25           # mean room per end for the contact plates
CELL_SPRING_LEN = 3.5         # compressed length of the negative spring contact
CELL_Y = 1.25                 # the spring pushes the cell towards the + contact (+Y)
CRADLE_WALL = 1.6
CELL_BORE = CELL_D + 0.4      # cradle bore
CELL_SNAP = 3.0               # snap walls rise this far above the cell axis

# boards
XIAO_L, XIAO_W, XIAO_H = 21.0, 17.8, 5.0          # Seeed XIAO ESP32-S3 Plus   MEASURE height
AMP_L, AMP_W, AMP_H = 19.05, 17.78, 3.0           # MAX98357A breakout
TP_L, TP_W, TP_H = 28.0, 17.0, 4.0                # TP4056 USB-C + DW01A module
BOOST_L, BOOST_W, BOOST_H = 17.8, 11.3, 5.6       # Adafruit MiniBoost 5V #4654
USB_W, USB_H = 8.94, 3.26                         # USB-C receptacle shell
USB_OPEN_W = 9.4                                  # notch width in the band
USB_PLUG_W, USB_PLUG_H = 12.6, 6.6                # body (overmold) of a USB-C plug, with margin
USB_Z = Z_BOWL_RIM + USB_H / 2 + 0.2              # receptacle centre: sits on the bowl rim
USB_AZ = 160.0                                    # azimuth of the port (back, 20 deg left of the hinge)
HALL_W, HALL_H, HALL_T = 4.0, 3.2, 1.52           # DRV5032FB in TO-92; the AH3661UA has the same body

# chassis
Z_PLATE_TOP = -26.5           # top of the chassis floor plate
PLATE_T = 2.0
CHASSIS_WALL = 1.4
R_BUCKET = RI_BOWL - 0.5      # chassis bucket outer sphere radius
BAFFLE_R = 21.0               # radius of the speaker baffle block
TP_TIP_R = R_BAND - 0.3       # USB-C receptacle face sits 0.3 mm behind the band
BOOST_POS = (-27.5, -14.5, -18.0)  # boost board centre (x, y) and underside z
MCU_POS = (14.0, -26.4, -13.5)     # XIAO centre
AMP_POS = (14.0, 25.4, -14.5)      # amplifier centre
R_BUCKET_CYL = R_CHASSIS_FLANGE   # ... capped to this radius near the top (band spigot)

# ==========================================================================
# 8. The four Pokémon Tonies (research/09 section 1).  No source publishes
#    their size: every value was measured on official pictures against the
#    Toniebox 2.  Measure a figure before printing.                     MEASURE
# ==========================================================================
TONIE_BASE_D = 45.0           # the black round foot, the same on all four (+2 / -1.5)
TONIE_BASE_H = 15.0           # its height (+-1)
TONIE_H = 70.0                # overall height of the tallest, Pikachu (+-3); the others 60-63
TONIE_ENVELOPE_D = 52.0       # cylinder that contains all four with their tolerances ...
TONIE_ENVELOPE_H = 78.0       # ... nothing overhangs the foot by more than about 1 mm
TONIE_MAGNET_D = 6.0          # classic Tonies: one or two magnets of 6 x 6 mm.  Their number and
TONIE_MAGNET_H = 6.0          # position in the Pokémon foot are NOT known (research/09 section 7)
TONIE_MASS_G = 50.0           # 40-50 g

# ==========================================================================
# 9. Grass tongue (revision 5): a tongue in front of the ball on which a Tonie
#    stands to be read (research/08, 09, 10).  No part of it reaches round
#    the ball, and its underside lies in the plane of the ball's flat.
#    Tray and grass top are printed in one light green.
#
#   z = Z_TURF        top of the grass top and of the rim round it = surface a Tonie stands on
#   turf plate        TURF_T thick, one flat sheet that carries the tufts; it lies in a frame
#   reader board      plain side up against the turf, component side down, on a ledge
#   well below it     WELL_DEPTH: wires, and the hall switch lying on its floor
#   tray floor        solid from there down to the sole
#   z = Z_SOLE        = Z_FLAT: tongue and ball stand on the table together
# ==========================================================================
Z_SOLE = Z_FLAT               # flush: the tongue's underside lies in the plane of the ball's flat
BASE_T = 15.0                 # height of the tongue without the blades (owner: keep, revision 4)
Z_TURF = Z_SOLE + BASE_T
TURF_T = 1.6                  # turf plate; its underside is flat, so it prints on the bed
Z_RAIL = Z_TURF - TURF_T      # bed of the turf plate in the tray = underside of the plate
PCB_PLAY = 0.1
Z_PCB_TOP = Z_RAIL - PCB_PLAY                 # plain side of the reader board
Z_PCB_BOT = Z_PCB_TOP - BLUE_T                # component side with the antenna copper
SOLDER_RELIEF = 0.7           # recess in the turf above the solder joints of the header row
WELL_DEPTH = 5.0              # free depth under the board.  The hall switch lies on its floor, which puts
                              # its element 8-9 mm below the pole face of a magnet in a figure's foot:
                              # deep enough to catch magnets that are not on the axis (research/09 section 7)
Z_TRAY_FLOOR = Z_PCB_BOT - WELL_DEPTH
TRAY_FLOOR = Z_TRAY_FLOOR - Z_SOLE            # solid tray under the pocket

# outline: rear end under the ball's belly, two straight sides, a blunt front end just in front of
# the reader board.  The spot is not marked (owner, revision 4); the front end is the cue.
X_REAR = 10.0                 # the tongue begins this far in front of the ball's axis, under its belly
REAR_CHAMFER = 12.0           # its rear corners are cut off at 45 degrees
TONGUE_W = 36.0               # half width at the rear corners; from there the sides run straight to the tip
SPOT_X = 87.0                 # where a figure belongs = centre of the antenna.  Set by the reader
                              # board: its rear edge has to stay in front of the ball's belly
SIDE_MARGIN = 10.5            # ground that shows beside the foot of a centred figure
R_SIDE = TONIE_BASE_D / 2 + SIDE_MARGIN       # the sides touch a circle of this radius round the figure: 33 mm
TIP_WALL = 3.2                # tray in front of the reader pocket: 2 mm of rim, the joint, 1 mm of bed for the grass top
X_TIP = SPOT_X - BLUE_ANT_X + BLUE_L + BLUE_CL_X + TIP_WALL   # front end of the tongue: 111.5 mm.  The reader board
                              # sets it, not the figure, whose foot ends 2 mm short of it (owner: shorter, revision 5)
TIP_R = 15.0                  # radius of the two front corners; a larger one leaves less than 3 mm of wall
                              # round the front corners of the reader pocket
GRASS_GAP = 8.0               # least distance between the foot of a centred figure and any grass
SPOT_CLEAR_R = TONIE_BASE_D / 2 + GRASS_GAP   # no grass inside this radius
GRASS_X_MAX = SPOT_X - 10.0   # and none in front of this line: the sides and the front of a figure stay open
EDGE_CHAMFER = 0.5

# the grass top lies in a frame: a rim of the tray round its sides and its tip
RIM = 2.0                     # width of that rim at the level of the bed
RIM_GAP = 0.15                # clearance between plate and rim, all round
TURF_HOOK = 1.2               # the walls of the frame lean forwards by this much over the turf thickness:
                              # at the tip the rim overhangs the plate and holds its front edge down
TURF_FOOT = 0.3               # the lowest 0.3 mm of the plate stand back by another 0.3 mm (first layer squeezed wide)

CUP_GAP = 0.25                # gap between ball and tongue everywhere except on the seat pads
R_CUP_HOLE = math.sqrt((R + CUP_GAP) ** 2 - (Z_SOLE + 1.0) ** 2)   # the rear edge is cut off where it gets thinner than 1 mm
BASE_SCREW_RHO = 30.5         # four M3 x 16 countersunk screws from below into the bowl, on this radius
BASE_SCREW_AZ = (32.0, 52.0, -32.0, -52.0)
BASE_SCREW_L = 16.0
BASE_PAD_R = 4.5              # seat pads round the screws: the only contact with the ball
CSK_D, CSK_H = 6.0, 1.7       # M3 countersunk head ISO 10642 / DIN 7991 (research/10 C2)
CSK_RECESS = 0.3              # head sits this far below the sole
BASE_BOSS_R = 4.2             # bosses for the four inserts inside the bowl
Z_BASE_BOSS = -29.5           # top of those bosses, 1 mm under the chassis plate
BASE_INSERT_L = 5.0           # inserts in the lower bosses, for the screws of the tongue
BASE_INSERT_DEPTH = 6.2       # that insert + 1.2 mm; the screw comes from below and ends 1.2 mm under the top of the boss

WINDOW_R0, WINDOW_R1 = 26.0, 36.0     # cable window in the bowl wall, hidden behind the tongue
WINDOW_HALF_DEG = 19.0
CHANNEL_W = 8.25              # half width of the cable channel

TURF_SCREW_HEAD_D, TURF_SCREW_HEAD_H = M2_HEAD_D, M2_HEAD_H
TURF_SCREW_L = 6.0            # M2 x 6
TURF_SEAT = 1.7               # tray left under the head: the screw then has M2_ENGAGE of thread beyond the lead-in
TURF_SCREW_CB = (Z_RAIL - Z_SOLE) - TURF_SEAT       # depth of the counterbore in the sole
TURF_PILOT_DEPTH = TURF_SCREW_L - TURF_SEAT + 0.3   # pilot hole from the turf underside: 0.3 mm deeper than the
                              # screw reaches; it ends inside a blade root
# four screws hold the rear half of the grass top (the rim holds its tip); each is hidden in the
# root of a tuft in one of the two corners beside the ball.  Deliberately not mirrored.
TURF_SCREW_XY = ((37.5, 29.0), (52.0, 24.5), (43.0, -25.0), (55.5, -28.0))

# the lawn: thin, and gathered in the two corners between the ball and the sides of the tongue
LAWN_SEED = 20261119          # another seed gives another lawn
LAWN_TUFTS = 10               # tufts thrown at random, besides the four on the screws (fewer if they do not fit)
LAWN_CORNER = (37.0, 28.0)    # where the grass is densest: x, |y|
LAWN_SPREAD = 11.0            # how far it scatters from there (standard deviation, mm)
LAWN_CENTRE_BAND = 20.0       # within this distance of the centre line the grass thins out ...
LAWN_CENTRE_FREE = 8.0        # ... and within this distance no tuft is rooted at all
BLADE_H = (7.0, 21.0, 13.0)   # height of the main leaf of a tuft: least, most, most frequent
BLADE_GAP = 0.8               # least distance between a blade and the ball
BLADE_ROOT_SINK = 0.3         # blades start this far below the turf surface
BLADE_TIP = (0.6, 0.5)        # half axes of the blunt tip: 1.2 x 1.0 mm (research/10 B1)
MOUND_H = 2.4                 # every tuft grows out of a low solid mound that ties its blades together

HARNESS_W = 12.5              # twelve 28 AWG wires side by side
HARNESS_T = 1.1
# one mated 6-pin wire-to-wire pair, 1.25 mm pitch (Molex PicoBlade 51021 / 51047
# and its clones, research/10 C1).  PLUG_PASS is the largest plug section the
# cable window is designed to let through.
PLUG_L, PLUG_W, PLUG_H = 12.0, 9.25, 3.2
PLUG_PASS = (15.5, 6.5)


def summary() -> dict[str, float]:
    """Key derived numbers, used by the checks and the manual."""
    return {
        "outer_diameter": D,
        "band_height": BAND_H,
        "bezel_diameter": 2 * BEZEL_R,
        "lens_diameter": 2 * LENS_R,
        "button_diameter": 2 * BTN_R,
        "flat_diameter": 2 * R_FLAT,
        "hinge_axis_x": HINGE_X,
        "hinge_axis_z": HINGE_Z,
        "deck_height": Z_DECK,
        "antenna_to_figure_base": Z_TURF - Z_PCB_BOT,
        "figure_spot_x": SPOT_X,
        "base_length": X_TIP - X_REAR,
    }
