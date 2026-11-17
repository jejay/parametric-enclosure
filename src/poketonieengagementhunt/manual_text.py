"""Text of the building manual: assembly steps, BOM notes and the Markdown layout."""

from __future__ import annotations

from . import params as P

BOARDS = ["contacts", "mcu", "amp", "charger", "boost"]
SERVO = ["servo", "horn", "servo_screws"]
FRONT = ["speaker", "spk_clamp", "clamp_screws", "led", "cone", "lens", "bezel"]
CORE = ["chassis"] + BOARDS + SERVO + FRONT
BOWL = ["bowl", "inserts"]
GRASS_IN = ["reader", "hall", "harness"]
TURF = ["grass_top"]
GRASS = ["grass_base"] + GRASS_IN + TURF + ["turf_screws"]
FOOT = BOWL + GRASS + ["base_screws"]          # everything below the core
STAGE = ["stage", "pawl", "pawl_screw", "pawl_spring", "cradle", "lock_pin", "slider"]
LID = ["lid", "hinge_pin", "sleeve", "spring"]

ANTENNA_MM = P.Z_TURF - P.Z_PCB_BOT            # antenna copper below the standing surface, at most
FRONT_MM = P.X_TIP - (P.SPOT_X + P.TONIE_BASE_D / 2)   # from the foot of a centred figure to the front edge of the tongue
HALL_MM = P.Z_TURF - (P.Z_TRAY_FLOOR + P.HALL_T)   # face of the hall switch below the standing surface
TABLE_MM = P.Z_PCB_BOT - P.Z_SOLE              # antenna copper above the table


def _lift(keys, v):
    return {k: v for k in keys}


STEPS = [
    {
        "n": 1,
        "title": "Prepare the bowl",
        "parts": ["bowl", "inserts"],
        "text": [
            "Press eight M3 heat-set inserts into the bowl with a soldering iron (about 230 °C for PETG): four into the bosses at the rim, four into the bosses low on the front wall, below the notch for the button. Push straight down and stop when the insert is flush with the top of its boss; let it cool before you touch it.",
            "The four lower bosses take the screws of the grass tongue. Check from outside that an M3 screw passes freely through the hole below each of them.",
        ],
        "views": [
            {"file": "step_01.png", "show": ["bowl"], "new": ["inserts"], "lift": {"inserts": (0, 0, 18)}, "az": 40, "el": 52},
        ],
    },
    {
        "n": 2,
        "title": "Build the grass tongue",
        "parts": ["grass_base", "reader", "hall", "harness"] + TURF + ["turf_screws"],
        "text": [
            "Wire the reader. Take the plug halves of the two 6-pin pairs with about 12 cm of wire. Solder ten wires to the reader's header row, coming from the component side: the first nine pads, +5V, +3.3V, RST, NSS, MOSI, MISO, SCK, BUSY, GND, and the pad IRQ. The pads GPIO, AUX and REQ stay empty. Cut flush whatever sticks out on the plain side. The header that comes with the board is not fitted: the plain side has to be flat.",
            "Wire the hall switch. Its supply leg goes to the reader's +3.3V pad and its ground leg to GND, each with a short wire; its output leg takes the eleventh wire of the plugs. The twelfth wire stays free (table in `docs/electronics.md`). Insulate each joint with thin heat-shrink tube.",
            "Glue the hall switch flat onto the floor of the pocket between the three small walls under the middle of the antenna, printed face up, legs pointing towards the ball. If the bench test of section 2 found the magnets of your figures elsewhere, glue it there instead; the floor is flat all over. Lay its wires along the floor.",
            "Lay the reader into the pocket, components down, with the antenna at the tip of the tongue and the header end against the two stops at the rear. It rests on the ledge all round. Lead the wires side by side through the channel towards the ball and fix them there with a drop of hot glue. Two more drops at the corners keep the board from rattling.",
            "Fit the grass top into its frame: hold it level, a little behind its place, and push it forwards and down, so that its bevelled front edge slips under the rim at the tip and the plate lies flush in the frame all round. Turn the tongue over and fasten the four 2.2 x 6 screws from below; their heads sit deep in the holes of the sole. They end inside the roots of grass tufts in the two rear corners, so stop as soon as they are snug.",
        ],
        "views": [
            {"file": "step_02a.png", "show": ["grass_base"], "new": GRASS_IN, "lift": {"hall": (0, 0, 9), "reader": (0, 0, 22), "harness": (0, 0, 36)}, "az": -55, "el": 44},
            {"file": "step_02b.png", "show": ["grass_base"] + GRASS_IN, "new": TURF + ["turf_screws"], "lift": {**_lift(TURF, (0, 0, 26)), "turf_screws": (0, 0, -20)}, "az": -55, "el": 16},
        ],
    },
    {
        "n": 3,
        "title": "Screw the tongue under the bowl",
        "parts": ["base_screws"],
        "text": [
            "Push the two plugs of the reader harness from outside through the window low on the front of the bowl, one after the other, and pull the wires in after them.",
            f"Set the bowl onto the hollow rear end of the tongue, with the U-shaped notch for the button above the tongue. The bowl rests on four small pads round the screw holes; everywhere else a gap of {P.CUP_GAP} mm remains. No part of the tongue reaches round the ball. With the bowl in place the grass top can no longer slide back out of its frame.",
            f"Hold both together, turn them over and fasten the four countersunk M3 x {P.BASE_SCREW_L:.0f} screws into the lower inserts. Tighten gently and in turn.",
            "Stand the device on a flat table. The underside of the tongue lies in the plane of the ball's flat foot, so both stand on the table together and the device must not rock. Printed parts differ by a tenth of a millimetre or two: if it rocks, a strip of adhesive tape on the four pads lowers the tongue and a few strokes of sandpaper on them raise it. Three thin felt dots, one under the flat of the ball and two under the tongue, hide whatever remains.",
            "Look into the gap between grass and ball at the front: no wire may be pinched under the bowl.",
            "The other order works as well: finish and test the whole ball first, then pull the two sockets of the core out through the window, plug them in, push the pairs back and screw the tongue on. The window lets a mated pair pass.",
        ],
        "views": [
            {"file": "step_03.png", "show": GRASS, "new": ["bowl", "inserts", "base_screws"], "lift": {"bowl": (0, 0, 40), "inserts": (0, 0, 40), "base_screws": (0, 0, -24)}, "label": ["bowl", "harness", "base_screws"], "az": 36, "el": 16},
        ],
    },
    {
        "n": 4,
        "title": "Fit the boards and the battery contacts",
        "parts": ["chassis"] + BOARDS,
        "text": [
            "Wire the electronics on the bench first, following `docs/electronics.md`, and test them before anything goes into the chassis.",
            "Slide the two contact plates into the slots at the ends of the battery cradle: the spring at the right-hand end (-Y, cell minus), the dimple at the left-hand end (+Y, cell plus). Their solder tabs point up.",
            "Lay the charger on its shelf at the back left, between the two lips, with the USB-C socket pointing outwards and the inner end of the board against the stop block. The stop takes the push of the plug; a bed of epoxy or hot glue under the board holds it against the pull when unplugging. Check with the band held in place that the face of the socket ends just behind the band's surface; adjust `TP_L` in `params.py` if your module is longer or shorter than 28 mm.",
            "Stand the XIAO upright in its pocket on the right (USB-C up) and the amplifier upright in the pocket on the left (pin row up). Lay the boost converter on its small shelf behind the battery. A drop of hot glue per board is enough.",
            "Plug the XIAO's flexible antenna into its U.FL socket and stick it to the inside of the chassis wall on the right, as far from the cell as the lead allows.",
            "Lead the two 6-pin sockets for the reader harness down through the rectangular window in the floor plate, with about 8 cm of wire below the plate.",
        ],
        "views": [
            {"file": "step_04.png", "show": ["chassis"], "new": BOARDS, "lift": {"contacts": (0, 0, 22), "mcu": (0, 0, 26), "amp": (0, 0, 26), "charger": (-10, 4, 20), "boost": (0, 0, 24)}, "az": 150, "el": 48},
        ],
    },
    {
        "n": 5,
        "title": "Fit the servo",
        "parts": SERVO,
        "text": [
            "Shorten the single-arm servo horn to 13 mm from the centre of the shaft with side cutters. A longer arm would hit the latch pivot.",
            "Lower the servo into its bay with the output shaft towards the left (+Y) and the cable in the slot. Fix it with the two screws that came with it.",
            "Do not fit the horn yet: its angle is set during commissioning (section 6).",
        ],
        "views": [
            {"file": "step_05.png", "show": ["chassis"] + BOARDS, "new": SERVO, "lift": {"servo": (0, 0, 30), "horn": (0, 0, 40), "servo_screws": (0, 0, 46)}, "az": 60, "el": 42},
        ],
    },
    {
        "n": 6,
        "title": "Build the front module: speaker, light and bezel",
        "parts": FRONT,
        "text": [
            "Solder two wires to the speaker. Seat the speaker against the back of the baffle (cone to the front) and clamp it with the clamp ring and two 2.2 x 8 screws. The solder tags sit in the notch of the ring. A thin bead of glue around the rim makes the front chamber airtight.",
            "Push the lens into the bezel from behind until its flange sits on the step. Push the white light cone in behind it; it holds the lens in place.",
            "Solder three wires to the LED board, press it into the cup at the narrow end of the cone (LED facing the lens) and lead the wires out through the notch.",
            "Glue the bezel into the socket of the baffle. The key under the tube fits only one way; the four slits then lie on the diagonals. Lead the LED wires out of the front chamber through the socket key notch and seal the notch with a drop of glue.",
        ],
        "views": [
            {
                "file": "step_06.png",
                "show": ["chassis"] + BOARDS + SERVO,
                "new": FRONT,
                "lift": {"speaker": (-11, 0, 0), "spk_clamp": (-21, 0, 0), "clamp_screws": (-33, 0, 0), "led": (22, 0, 34), "cone": (30, 0, 34), "lens": (44, 0, 34), "bezel": (20, 0, 0)},
                "az": -52,
                "el": 26,
            },
        ],
    },
    {
        "n": 7,
        "title": "Lower the core into the bowl and insert the cell",
        "parts": ["cell"],
        "text": [
            "Hold the finished core over the bowl and join the two 6-pin plugs of the reader harness to the two sockets hanging under the chassis. Mark the pairs A and B so that they cannot be swapped.",
            "Lower the core. The plugs and the spare wire fold into the space between the floor of the bowl and the chassis plate; the bezel slides into the U-shaped notch and the chassis flange comes to rest on the four bosses at the rim.",
            "Snap the 18650 cell into the cradle, plus pole to the left (+Y), until the two side walls click over it.",
            "If the charger's protection circuit stays off after a cell has been inserted, connect USB-C power once to wake it.",
        ],
        "views": [
            {"file": "step_07.png", "show": FOOT, "new": CORE + ["cell"], "lift": {**_lift(CORE, (0, 0, 58)), "cell": (0, 0, 100)}, "label": ["chassis", "cell", "harness"], "az": 38, "el": 20},
        ],
    },
    {
        "n": 8,
        "title": "Fit the band",
        "parts": ["band"],
        "text": [
            "Lower the black band over the core. Its notch slips over the USB-C socket, its gap over the bezel, and its skirt drops inside the rim of the bowl. The four lugs lie on the chassis flange, over the screw holes.",
            "Optional: glue a 6 mm wide strip of black felt or fabric tape to the inside of the band below the shallow pocket at the back, standing 2 mm proud of the pocket. It closes the view into the hinge and bends away when the lid opens.",
        ],
        "views": [
            {"file": "step_08.png", "show": FOOT + CORE + ["cell"], "new": ["band"], "lift": {"band": (0, 0, 30)}, "az": 150, "el": 28},
        ],
    },
    {
        "n": 9,
        "title": "Assemble the stage: latch and ring lock",
        "parts": STAGE,
        "text": [
            "Turn the stage upside down. Put the pawl on the pivot boss (post pointing away from the deck) and hold it with the 2.2 x 6 screw and washer. The pawl must swing freely; do not clamp it.",
            "Put the short compression spring between the nub on the pawl's tail and the nub on the stage. It pushes the tail against the stop pin.",
            "Turn the stage over. Line the ring slot of the cradle with self-adhesive felt on both sides until the ring slides in with light friction, then drop the cradle into its pocket in the deck.",
            "Press the 3 x 24 mm dowel pin into the stem of the slider. Put the slider into its slot behind the cradle and push the pin forwards through the guide and the cradle. In the rear position the pin clears the ring slot, in the front position it crosses it; in both positions it keeps the cradle captive.",
        ],
        "views": [
            {"file": "step_09a.png", "show": ["stage"], "new": ["pawl", "pawl_screw", "pawl_spring"], "lift": {"pawl": (0, 0, -16), "pawl_screw": (0, 0, -30), "pawl_spring": (0, 0, -16)}, "az": 25, "el": -42},
            {"file": "step_09b.png", "show": ["stage", "pawl", "pawl_screw", "pawl_spring"], "new": ["cradle", "lock_pin", "slider"], "lift": {"cradle": (0, 0, 18), "slider": (0, 0, 26), "lock_pin": (-34, 0, 0)}, "az": 150, "el": 40},
        ],
    },
    {
        "n": 10,
        "title": "Hinge the lid to the stage",
        "parts": LID,
        "text": [
            "Slip the printed sleeve into the torsion spring. Hold the spring between the two ribs of the lid so that one leg lies up along the inside of the lid's back wall and the other points forwards.",
            "Hold the lid about 90° open behind the stage, bring its ribs between the two hinge towers and push the 2 x 20 mm pin through tower, rib, sleeve, rib and tower. It is a press fit in the ribs.",
            "Lift the forward-pointing spring leg onto the yoke between the towers. The coil must tighten when you close the lid; if it opens instead, take the spring out and use the one with the other winding direction (order both L and R).",
            "Close and open the lid by hand a few times. It must swing freely from closed to the end stop at about 95° and the spring must throw it open.",
        ],
        "views": [
            {"file": "step_10.png", "pose": "open", "show": STAGE, "new": LID, "lift": {"lid": (-34, 0, 6), "hinge_pin": (0, 36, 0), "sleeve": (0, 0, 22), "spring": (0, 0, 36)}, "az": 62, "el": 32},
        ],
    },
    {
        "n": 11,
        "title": "Screw the stage onto the core",
        "parts": ["stack_screws"],
        "text": [
            "Open the lid. Lower the stage onto the core: its notch goes over the bezel, the pawl post drops in beside the servo, and the four screw wells line up with the band lugs.",
            "Fasten the four M3 x 16 screws through the wells. They pass through stage, band lug and chassis flange into the inserts at the rim of the bowl and clamp the whole stack. Tighten gently.",
        ],
        "views": [
            {"file": "step_11.png", "pose": "open", "show": FOOT + CORE + ["cell", "band"], "new": STAGE + LID + ["stack_screws"], "lift": {**_lift(STAGE + LID, (0, 0, 46)), "stack_screws": (0, 0, 84)}, "label": ["stage", "lid", "stack_screws"], "az": 38, "el": 24},
        ],
    },
    {
        "n": 12,
        "title": "Seat and lock the ring, close the lid",
        "parts": ["ring"],
        "text": [
            "Pull the slider back, push the ring into the felt-lined slot until it sits on the bottom, and push the slider forwards until it clicks. The pin now passes through the ring below the deck: the ring cannot come out, however the ball is shaken or dropped.",
            "Check that the servo is in its rest position, then press the lid down until the latch clicks.",
        ],
        "views": [
            {"file": "step_12.png", "pose": "unlocked", "show": FOOT + CORE + ["cell", "band", "stack_screws"] + STAGE + LID, "new": ["ring"], "lift": {"ring": (0, 0, 24)}, "az": 22, "el": 34},
        ],
    },
]


# key -> (what to buy / what it is, reference into research/)
BOM_NOTES = {
    "reader": ("The common blue PN5180 module, about 70 x 39 mm, silkscreen \"PN5180-NFC\" (AliExpress, Amazon, eBay, AZ-Delivery). Prefer a listing whose pin header is supplied loose. The bag usually holds two test tags as well.", "research/02 §1A, 08"),
    "hall": ("TI DRV5032FB hall switch in TO-92 (4.0 x 3.15 x 1.52 mm). Buy two: the second can go on the spare wire if one does not catch the magnets.", "research/04 §5, 09 §7, 10 C5"),
    "harness": ("Two pre-wired 6-pin wire-to-wire pairs with 1.25 mm pitch and at least 15 cm of 28 AWG wire on each half. Sold as \"Micro JST 1.25 mm 6-pin male and female with wire\"; the original parts are Molex PicoBlade 51021-0600 and 51047-0600. One half goes to reader and hall switch, the other to the core.", "research/10 C1"),
    "turf_screws": ("Self-tapping screws 2.2 x 6 with pan head, ISO 7049 (head 4.0 x 1.6 mm).", "research/06 §4.2, 10 C4"),
    "base_screws": ("M3 x 16 countersunk screws with hexagon socket, ISO 10642 or DIN 7991.", "research/10 C2"),
    "mcu": ("Seeed XIAO ESP32-S3 Plus (16 MB flash, 8 MB PSRAM) with its U.FL antenna. Fallback: Unexpected Maker TinyS3 (needs a longer pocket).", "research/04 §1, 07 §11"),
    "amp": ("MAX98357A I2S class-D amplifier breakout (Adafruit #3006 or clone), terminal block not fitted.", "research/04 §2"),
    "speaker": ("Visaton K 40, 8 ohm, art. no. 2840 (Ø40 x 4.3 mm, 83 dB).", "research/04 §3"),
    "led": ("One WS2812B or SK6812 on a round Ø10 mm mini PCB.", "research/04 §4"),
    "servo": ("Any SG90-class 9 g micro servo with its horns and screws.", "research/05 §1"),
    "horn": ("The single-arm horn from the servo bag, trimmed to 13 mm.", "research/05 §1.3"),
    "cell": ("Unprotected flat-top 18650, e.g. Samsung INR18650-35E or Molicel M35A.", "research/05 §2"),
    "contacts": ("One spring and one button contact plate for AA/18650 holders, about 10 x 10 mm.", "research/05 §3.2"),
    "charger": ("TP4056 USB-C charger module with DW01A protection, 28 x 17 mm. Change R_PROG to 2.0-2.4 kOhm for about 0.5 A.", "research/05 §4.1"),
    "boost": ("Adafruit MiniBoost 5V @ 1A (TPS61023), #4654, with enable pin.", "research/05 §4.3"),
    "spring": ("Gutekunst T-16324L and T-16324R (order one of each).", "research/06 §2.1"),
    "inserts": ("M3 heat-set inserts, Ø4.6 x 5.7 mm (ruthex / CNC Kitchen).", "research/06 §4.1"),
    "stack_screws": ("M3 x 16 socket head cap screws, ISO 4762.", "research/06 §4.3"),
    "servo_screws": ("Supplied with the servo.", "research/05 §8.1"),
    "clamp_screws": ("Self-tapping screws 2.2 x 8.", "research/06 §4.2"),
    "pawl_screw": ("Self-tapping screw 2.2 x 6 and an M2 washer.", "research/06 §4.2"),
    "pawl_spring": ("Soft compression spring about Ø3.5-4.5 x 8 mm, for example a piece of a ball-pen spring.", "research/06 §2.2"),
    "hinge_pin": ("Stainless pin Ø2 x 20 mm: dowel pin ISO 2338, or a cut bicycle spoke.", "research/06 §3"),
    "lock_pin": ("Hardened dowel pin Ø3 x 24 mm, ISO 2338.", "research/06 §3"),
    "ring": ("The engagement ring. Measure it and adjust the RING_* values in `params.py`, then reprint the cradle.", "research/06 §1"),
}

SMALL_PARTS = [
    ("Electrolytic capacitor 470-1000 µF / 10 V", "1", "across the 5 V output of the boost converter, close to the servo"),
    ("Resistors 2 MOhm and 1 MOhm, capacitor 100 nF", "1 each", "battery voltage divider at the ADC pin"),
    ("Resistors 100 kOhm", "3", "pull-downs on boost enable, amplifier SD and reader RST"),
    ("Diode 1N4148", "1", "in series with the LED's 5 V supply, so that 3.3 V data is in spec"),
    ("Silicone wire 26-28 AWG, heat-shrink tube", "", "all point-to-point wiring"),
    ("Self-adhesive felt or velour, 0.5-1 mm", "", "ring slot lining; optional curtain behind the band pocket; optional dots under the ball's flat and the tongue"),
    ("Hot glue or epoxy; cyanoacrylate", "", "boards, bezel, hall switch, reader"),
    ("Flexible ferrite sheet 0.1-0.2 mm, about 45 x 42 mm (Würth WE-FSFS 364004 or 364005)", "1, only if needed", "on the floor of the pocket under the antenna, if the bench test fails on a metal surface"),
    ("Schottky diodes BAT43 or 1N5817", "2, only if needed", "supply of the reader in sleep, if the ball is woken by card detection instead of the hall switch"),
]

TOOLS = [
    "FDM printer with a 0.4 mm nozzle; PETG in red, white, black, natural (clear) and a light green, and any colour for the inner parts",
    "Soldering iron with a fine tip (also used to set the heat-set inserts)",
    "Hex keys 2 and 2.5 mm, small cross-head screwdriver, side cutters, tweezers",
    "Multimeter; a USB-C cable and charger",
    "Calipers, to measure the ring, the reader board and the other delivered boards",
]


def manual_markdown(items, nums, printed) -> str:
    from . import geom as g

    by = {it.key: it for it in items}
    L: list[str] = []
    a = L.append
    a("# Building manual: Poké Ball in the tall grass, for the Tonie hunt")
    a("")
    a("This manual is generated by `uv run poketonieengagementhunt manual` from the CAD model in `src/poketonieengagementhunt/`. Pictures, part numbers and dimensions therefore always match the model. The balloons in every picture carry the position numbers of the bill of materials in section 1.")
    a("")
    a("| Closed | With a Tonie | Open |")
    a("| --- | --- | --- |")
    a("| ![closed](img/hero_closed.png) | ![with a Tonie](img/hero_tonie.png) | ![open](img/hero_open.png) |")
    a("")
    a("## What you are building")
    a("")
    a(f"A {P.D:.0f} mm Poké Ball with a tongue of tall grass in front of it. The tongue is a block screwed under the lower front of the ball: {2 * P.TONGUE_W:.0f} mm wide at the ball, {2 * P.R_SIDE:.0f} mm beside a figure, {P.BASE_T:.0f} mm high without the blades, and it reaches {P.X_TIP - P.R:.1f} mm beyond the ball, just past the reader board inside it. Tongue and grass are one light green. Nothing of the tongue lies beside or behind the ball, and its underside lies in the plane of the ball's flat foot, so ball and tongue stand on the table together. A Tonie is stood at the front end of the tongue, in front of the ball. That wakes the ball, which reads the figure's RFID tag and plays that figure's recorded message from its own flash memory. Because the figure stands on the grass, the ball always stays upright.")
    a("")
    a("The ball's black front ring carries the sound slits and its button is a lens lit by an RGB LED. The red half is a spring-loaded lid on a concealed hinge. A servo releases its latch on command from the phone, and the lid jumps open to present the ring, which is locked into its seat by a steel pin.")
    a("")
    a("![section](img/section.png)")
    a("")
    a("*Section through the centre plane, seen from the right-hand side. Front (button and tongue) is on the right.*")
    a("")
    a("Before you start: read `research/README.md` for why each part was chosen, `docs/electronics.md` for the wiring, and `docs/verification.md` for what has and has not been verified. The firmware and the phone app are not part of this manual.")
    a("")
    a("**Safety.** A bare 18650 cell can deliver dangerous currents: never short it, never solder on it, and do not leave the ball in a hot car (PETG softens near 70 °C). The heat-set inserts are pressed in at about 230 °C. No magnets are used in the device. The only magnets involved are those inside the Tonies.")
    a("")

    # ------------------------------------------------------------------ BOM
    a("## 1. Bill of materials")
    a("")
    a("### Purchased components")
    a("")
    a("| Pos. | Qty | Part | What to buy | Research |")
    a("| --- | --- | --- | --- | --- |")
    for it in items:
        if it.kind == "purchased" and it.key in nums:
            note, ref = BOM_NOTES.get(it.key, ("", ""))
            a(f"| {nums[it.key]} | {it.qty} | {it.label} | {note} | {ref} |")
    a("")
    a("### Hardware")
    a("")
    a("| Pos. | Qty | Part | Note | Research |")
    a("| --- | --- | --- | --- | --- |")
    for it in items:
        if it.kind == "hardware":
            note, ref = BOM_NOTES.get(it.key, ("", ""))
            a(f"| {nums[it.key]} | {it.qty} | {it.label} | {note} | {ref} |")
    a("")
    a("### Small parts without a position number")
    a("")
    a("| Part | Qty | Used for |")
    a("| --- | --- | --- |")
    for name, qty, use in SMALL_PARTS:
        a(f"| {name} | {qty} | {use} |")
    a("")
    a("### Printed parts")
    a("")
    a("| Pos. | Part | File | Filament | Mass | Print orientation |")
    a("| --- | --- | --- | --- | --- | --- |")
    for it in items:
        if it.kind == "printed":
            shape, filament, note = printed[it.key]
            mass = g.volume(shape) * 1.27e-3
            shown = f"{mass:.0f} g" if mass >= 10 else f"{mass:.1f} g"
            a(f"| {nums[it.key]} | {it.label} | `export/stl/{it.key}.stl` | {filament} | {shown} | {note} |")
    a("")
    a("### Tools")
    a("")
    for t in TOOLS:
        a(f"- {t}")
    a("")

    # ------------------------------------------------------------ bench test
    a("## 2. Test on the bench before you print")
    a("")
    a("Five things decide whether the design works, and none of them can be proven by CAD. Test them with loose parts and the real figures first:")
    a("")
    a(f"1. **Tonie reading.** Wire the PN5180 board to the XIAO and flash any firmware that performs the SLIX-L privacy unlock (see `research/01` and `research/07`). Lay the board on a wooden table with the components down, on two strips of cardboard about 2 mm thick, as it will lie in the tray. Cover it with a sheet of plastic {P.TURF_T:.1f} mm thick and stand each of the four figures on the middle of the antenna. All four must read. The tag is a small upright rod somewhere inside the figure, perhaps several centimetres up, so find the reserve: raise each figure on books or coasters until it stops reading, and slide it sideways until it stops reading. Note both distances and which privacy password each figure needs.")
    a(f"2. **Metal under the tongue.** Repeat test 1 with a baking tray {TABLE_MM:.0f} mm under the board: that is a metal table under the tongue. The distance is a little more than the 10 mm that the antenna guides ask for [research/08 §8], so the figures should still read. If they do not, lay the ferrite sheet from the list of small parts 5 mm under the board, where the floor of the pocket will be, and repeat on both surfaces.")
    a(f"3. **The magnets.** The pocket is laid out for the magnets of the classic Tonies, which the Pokémon figures should share because they work on the first Toniebox: cylinders of {P.TONIE_MAGNET_D:.0f} x {P.TONIE_MAGNET_H:.0f} mm, one in the middle of the foot or one in each of two feet [research/09 §7]. Find them with a steel pin or a compass needle. Then fix the hall switch under the middle of the antenna with its printed face {HALL_MM - P.TURF_T:.0f} mm below the plastic sheet (a stack of cardboard does it): that is where it lies in the tongue. It must switch when a figure stands on the sheet, in every rotation of the figure, and release when the figure is lifted away. Then slide the figure off the middle and note how far it can stand off before the switch lets go and before the read fails. Nothing marks the place on the tongue, so this distance is the reserve for a figure that is put down by eye; about {P.GRASS_GAP:.0f} mm is what the layout counts on. If the switch does not answer at all, read \"Wake, if the magnet is not where the switch is\" in `docs/electronics.md` before you go on.")
    a("4. **Servo and supply.** Run the servo from the boost converter on the real cell while the amplifier plays. The board must not reset. Measure the stall current.")
    a("5. **Lid spring.** Print the lid, the stage and the band first, hinge them and check that the spring throws the lid open and that it rests on the end stop.")
    a("")
    a(f"Also measure the delivered parts against the values marked `MEASURE` in `params.py`: outline of the reader board ({P.BLUE_L} x {P.BLUE_W} mm assumed; it sets the length of the tongue) and position of its antenna, the foot of a figure ({P.TONIE_BASE_D:.0f} mm assumed; the width of the tongue follows it), height of the XIAO, length of the charger and position of its USB-C socket, and the ring itself.")
    a("")

    # ---------------------------------------------------------------- print
    a("## 3. Print the parts")
    a("")
    a("![print orientation](img/print_orientation.png)")
    a("")
    a("*All printed parts in their print orientation. The STL files in `export/stl/` are already turned this way.*")
    a("")
    a("- Material: PETG for every part. The hinge, the latch and the spring seats stay under load for weeks, and PLA creeps and softens at 55-60 °C.")
    a("- 0.2 mm layers, 5 perimeters for the shells (they print solid), 4 perimeters and 30 % infill for the inner parts, 100 % for pawl, slider, sleeve and lens.")
    a("- Bowl, lid: rim on the bed, tree supports inside only. Put the layer seam at the back. A variable layer height (0.1 mm near the pole) hides the stair-stepping on the cap.")
    a("- Band, stage: upside down. Their 45° surfaces are designed to print without support in this orientation.")
    a("- Lens: natural (uncoloured) PETG. Print one first and check the glow with the LED; 1.6 mm front thickness is `LENS_T` in `params.py`.")
    a("- Bowl: the four bosses low on its front wall hang from the dome in print orientation. The tree supports that the floor needs anyway carry them.")
    a("- Grass tongue (tray): light green, sole on the bed, no supports, 4 perimeters, 40 % infill. The rim round its top overhangs inwards at the tip by less than 40°; it prints without support.")
    a(f"- Grass top: the same light green, one file (`grass_top.stl`): underside on the bed, tufts up, no supports, 5 perimeters so that the blades print solid. Slow down above the turf surface and keep a minimum layer time of about 8 s, so that the blunt tips do not melt. Its edge leans like the walls of its frame, and its lowest {P.TURF_FOOT} mm stand back a little for a first layer that is squeezed wide. If it still does not drop into the frame, scrape its bottom edge with a knife.")
    a("- A green that comes close to the grass of the games: Bambu PETG HF Green [research/10 A.4]. Tray and grass top should come from the same spool.")
    a("- Print pawl, slider, sleeve and cradle first. They are small and show whether your printer's clearances suit: the slider must move in the stage with light friction and the pawl must turn freely on its boss.")
    a("")

    # --------------------------------------------------------------- wiring
    a("## 4. Wire the electronics")
    a("")
    a("Wire and test everything on the bench, outside the ball, following the net list and the pin map in `docs/electronics.md`. Keep every lead just long enough to reach its place in the chassis plus 3 cm, and lead no wire across the top of the cell, which must lift out. Twelve wires connect the core to the reader and the hall switch in the grass tongue. They run through two 6-pin plugs, so that core and tongue can be separated.")
    a("")

    # ---------------------------------------------------------------- steps
    a("## 5. Assembly")
    a("")
    for st in STEPS:
        a(f"### Step {st['n']}: {st['title']}")
        a("")
        parts = [k for k in st["parts"] if k in nums]
        if parts:
            a("Parts: " + ", ".join(f"**{nums[k]}** {by[k].label}" for k in parts))
            a("")
        for v in st["views"]:
            a(f"![step {st['n']}](img/{v['file']})")
            a("")
        for i, line in enumerate(st["text"], 1):
            a(f"{i}. {line}")
        a("")

    # --------------------------------------------------------- commissioning
    a("## 6. Commissioning")
    a("")
    a("![latch locked](img/latch_locked.png)")
    a("")
    a("*The latch seen from above with the deck removed, locked. The pawl (yellow) lies over the tooth of the lid hook (red). The servo arm rests clear of the pawl's post.*")
    a("")
    a("![latch released](img/latch_released.png)")
    a("")
    a("*Released: the servo arm has pushed the post, the pawl has turned and its nose has left the tooth.*")
    a("")
    a(f"1. **Set the horn.** With the stage off and the servo commanded to its rest pulse, push the trimmed horn onto the shaft pointing about {abs(P.HORN_REST_DEG):.0f}° to the right of straight ahead (towards -Y), and fit its screw. At the release pulse it should point about {abs(P.HORN_RELEASE_DEG):.0f}° to the right of straight ahead. Store both pulse widths in the firmware; never command a position beyond them.")
    a("2. **Test the latch with the stage on and the lid open.** Command release: the pawl nose must swing clear of the hook slot. Command rest: the pawl must return against its stop pin by its own spring.")
    a("3. **Test the opening.** Close the lid (press until it clicks) and command release. The lid must open fully. Repeat twenty times.")
    a("4. **Test the emergency opening** described below, so that you know the feel of it.")
    a(f"5. **Test the tongue.** Stand each figure at the front end, its foot about {FRONT_MM:.0f} mm short of the front edge: the ball must wake and read it, also when the figure stands {P.GRASS_GAP:.0f} mm further back or to one side. Leave a figure standing: the ball must go back to sleep and stay asleep.")
    a("6. **Register the four Tonies and upload the messages** once the firmware exists.")
    a("")

    # ------------------------------------------------------------------ use
    a("## 7. Using the ball")
    a("")
    a("### Presenting a Tonie")
    a("")
    a("| | |")
    a("| --- | --- |")
    a("| ![a Tonie on the grass](img/grass.png) | ![section through the tongue](img/grass_section.png) |")
    a("")
    a(f"Stand the device on a table or on the ground and stand the Tonie at the front end of the tongue, in the middle between its two sides: its foot then ends about {FRONT_MM:.0f} mm short of the front edge and leaves about {P.SIDE_MARGIN:.0f} mm on each side. That wakes the ball. No mark shows the place; the front end is the cue. The reader's antenna lies {P.Z_TURF - P.Z_PCB_TOP:.1f} to {ANTENNA_MM:.1f} mm below the surface, centred under that place; the tag itself is a small rod further up inside the figure.")
    a("")
    a("Nothing holds the figure. It stands on a plain, level surface without recess or catch. The thin line that runs round the front end is the joint between the grass top and the rim of the tray; both are level, and the front edge of the foot stands on the rim. The grass stands only in the two corners beside the ball, in tufts of different sizes thrown at random; the sides and the front of the figure are open. Whoever carries the device has to hold the figure separately, as on any tray. On a shelf the figure simply stands on the tongue; the firmware lets the ball sleep while a figure stays there.")
    a("")
    a("### Charging")
    a("")
    a("![back](img/back_closed.png)")
    a("")
    a(f"The USB-C socket sits in the black band at the back, {180 - P.USB_AZ:.0f}° to the left of the hinge. The shallow scoop in the white rim below it makes room for the body of the plug. A charge at 0.5 A takes about 7 hours. Do not run the hunt from the charger: the charger has no power path and will not terminate while the ball is active.")
    a("")
    a("### Emergency opening")
    a("")
    a("![emergency](img/emergency.png)")
    a("")
    a("*Section along the path of the paper clip (orange).*")
    a("")
    a(f"If the electronics fail, the lid can still be opened without leaving a mark. Straighten a paper clip (wire up to 1.2 mm). Looking at the button, insert it into the **upper left slit**, near the upper end of that slit, about {abs(P.EMERGENCY_YZ[0]):.0f} mm left of the vertical centre line. Aim {P.EMERGENCY_SLOPE_DEG:.0f}° upwards. After about 17 mm the clip meets resistance; push 3 mm further. The clip leaves the bezel through a slot in its wall and pushes the pawl aside; the lid springs open. Nothing on the outside shows that this is possible.")
    a("")
    a("### Closing the lid")
    a("")
    a("Press the lid down until the latch clicks. The tooth of the hook pushes the pawl aside by itself; the servo is not needed.")
    a("")
    a("### Releasing the ring")
    a("")
    a("| Locked | Released |")
    a("| --- | --- |")
    a("| ![locked](img/ring_locked.png) | ![released](img/ring_released.png) |")
    a("")
    a(f"Pull the slider behind the ring back by {P.LOCK_TRAVEL:.0f} mm. The pin leaves the ring and the ring lifts out.")
    a("")
    a("### The hinge")
    a("")
    a("| Closed | Open |")
    a("| --- | --- |")
    a("| ![hinge closed](img/hinge_closed.png) | ![hinge open](img/hinge_open.png) |")
    a("")
    a("The hinge pin sits inside the lid. While the lid opens, its rear rim dips into a shallow pocket in the top edge of the black band. That pocket is the only trace of the hinge on the outside; it is black, lies under the overhanging lid and can be closed with the felt strip from step 8.")
    a("")

    # -------------------------------------------------------------- service
    a("## 8. Service")
    a("")
    a("**Swapping the cell**")
    a("")
    a("1. Open the lid (by command or with the paper clip) and unlock and remove the ring.")
    a("2. Undo the four M3 screws in the wells of the stage and lift the stage with the lid straight up.")
    a("3. Lever the cell out of its cradle and snap in a charged one, plus pole to the left.")
    a("4. Put the stage back and fasten the four screws.")
    a("")
    a("To take out the whole core, also lift off the band and separate the two 6-pin plugs under the chassis.")
    a("")
    a("**Opening the grass tongue**")
    a("")
    a("1. Undo the four countersunk screws under the rear end of the tongue and lift the ball a few centimetres off it.")
    a("2. Pull the two plug pairs out through the window in the bowl and separate them. The ball is now free.")
    a("3. Undo the four small screws, lift the rear of the grass top a little and draw it backwards out from under the rim at the tip; the reader lies open.")
    a("")

    # ------------------------------------------------------------- exploded
    a("## 9. Exploded view")
    a("")
    a("![exploded](img/exploded.png)")
    a("")
    a("| Pos. | Part | Qty | Kind |")
    a("| --- | --- | --- | --- |")
    for it in items:
        if it.key in nums:
            a(f"| {nums[it.key]} | {it.label} | {it.qty} | {it.kind} |")
    a("")
    return "\n".join(L) + "\n"
