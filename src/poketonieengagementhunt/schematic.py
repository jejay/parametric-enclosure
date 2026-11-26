"""Electronics schematic of the device, drawn as an SVG.

    uv run poketonieengagementhunt schematic   -> docs/img/schematic.svg, and schematic.png if resvg is installed

Every pad of every board is drawn, the ones that stay empty included. The
sheet is laid out by hand in ``build``; pin map and values are those of
``docs/electronics.md``. ``Sheet.verify`` only makes sure that no pad was
forgotten: every pad that is declared has to end in a wire or in a cross.
"""

from __future__ import annotations

import shutil
import subprocess
from html import escape
from pathlib import Path

W, H = 1720, 1230
FONT = "Arial, Helvetica, 'DejaVu Sans', sans-serif"
PNG_WIDTH = 2580

# colour of a net class: wires, junctions and tags
NET = {
    "sig": "#22364d",
    "vbat": "#c0392b",
    "v5": "#b36b00",
    "v33": "#1e7b4f",
    "gnd": "#111111",
}
TINT = {"vbat": "#fbe9e7", "v5": "#fdf1dc", "v33": "#e3f4ea"}
INK = "#16202b"
GREY = "#6b7480"
BOX = "#f5f7fa"
STUB = 20.0


class Sheet:
    def __init__(self) -> None:
        self.el: list[str] = []
        self.boxes: dict[str, tuple[float, float, float, float]] = {}
        self.pins: dict[tuple[str, str], tuple[float, float]] = {}
        self.uses: dict[tuple[str, str], int] = {}

    # ---- primitives -------------------------------------------------
    def raw(self, s: str) -> None:
        self.el.append(s)

    def wire(self, pts, net: str = "sig", width: float = 1.6) -> None:
        d = " ".join(f"{x:g},{y:g}" for x, y in pts)
        self.raw(f'<polyline points="{d}" fill="none" stroke="{NET[net]}" stroke-width="{width:g}" stroke-linejoin="round" stroke-linecap="round"/>')

    def dot(self, x: float, y: float, net: str = "sig") -> None:
        self.raw(f'<circle cx="{x:g}" cy="{y:g}" r="3.3" fill="{NET[net]}"/>')

    def text(self, x, y, s, size=12.0, anchor="start", fill=INK, bold=False, italic=False) -> None:
        a = "" if anchor == "start" else f' text-anchor="{anchor}"'
        b = ' font-weight="bold"' if bold else ""
        i = ' font-style="italic"' if italic else ""
        self.raw(f'<text x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{fill}"{a}{b}{i}>{escape(s)}</text>')

    def lines(self, x, y, rows, size=11.0, step=14.0, **kw) -> None:
        for k, s in enumerate(rows):
            self.text(x, y + k * step, s, size=size, **kw)

    def rect(self, x0, y0, x1, y1, fill="none", stroke=INK, width=1.4, rx=6.0, dash="") -> None:
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<rect x="{x0:g}" y="{y0:g}" width="{x1 - x0:g}" height="{y1 - y0:g}" rx="{rx:g}" fill="{fill}" stroke="{stroke}" stroke-width="{width:g}"{d}/>')

    # ---- symbols ----------------------------------------------------
    def gnd(self, x: float, y: float) -> None:
        """Ground symbol hanging below (x, y)."""
        c = NET["gnd"]
        self.raw(f'<path d="M{x:g},{y:g} v6 M{x - 9:g},{y + 6:g} h18 M{x - 6:g},{y + 10:g} h12 M{x - 3:g},{y + 14:g} h6" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round"/>')

    def nc(self, x: float, y: float) -> None:
        self.raw(f'<path d="M{x - 4:g},{y - 4:g} l8,8 M{x - 4:g},{y + 4:g} l8,-8" fill="none" stroke="{GREY}" stroke-width="1.6" stroke-linecap="round"/>')

    def resistor_v(self, x, y0, y1, net0="sig", net1="gnd", body=34.0) -> None:
        m = (y0 + y1) / 2
        self.wire([(x, y0), (x, m - body / 2)], net0)
        self.wire([(x, m + body / 2), (x, y1)], net1)
        self.rect(x - 5.5, m - body / 2, x + 5.5, m + body / 2, fill="#ffffff", stroke=INK, width=1.5, rx=1.5)

    def resistor_h(self, x0, x1, y, net0="sig", net1="sig", body=34.0) -> None:
        m = (x0 + x1) / 2
        self.wire([(x0, y), (m - body / 2, y)], net0)
        self.wire([(m + body / 2, y), (x1, y)], net1)
        self.rect(m - body / 2, y - 5.5, m + body / 2, y + 5.5, fill="#ffffff", stroke=INK, width=1.5, rx=1.5)

    def cap_v(self, x, y0, y1, net0="sig", net1="gnd", polar=False) -> None:
        m = (y0 + y1) / 2
        self.wire([(x, y0), (x, m - 3.5)], net0)
        self.wire([(x, m + 3.5), (x, y1)], net1)
        self.raw(f'<path d="M{x - 10:g},{m - 3.5:g} h20 M{x - 10:g},{m + 3.5:g} h20" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')
        if polar:
            self.text(x + 13, m - 6, "+", size=12, bold=True)

    def cap_h(self, x0, x1, y, net0="sig", net1="sig") -> None:
        m = (x0 + x1) / 2
        self.wire([(x0, y), (m - 3.5, y)], net0)
        self.wire([(m + 3.5, y), (x1, y)], net1)
        self.raw(f'<path d="M{m - 3.5:g},{y - 10:g} v20 M{m + 3.5:g},{y - 10:g} v20" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')

    def diode_h(self, x0, x1, y, net0="sig", net1="sig") -> None:
        """Diode that conducts from x0 to x1."""
        m = (x0 + x1) / 2
        self.wire([(x0, y), (m - 8, y)], net0)
        self.wire([(m + 8, y), (x1, y)], net1)
        self.raw(f'<path d="M{m - 8:g},{y - 8:g} L{m + 8:g},{y:g} L{m - 8:g},{y + 8:g} Z" fill="#ffffff" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
        self.raw(f'<path d="M{m + 8:g},{y - 8:g} v16" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')

    def terminal(self, x, y, net="sig") -> None:
        self.raw(f'<circle cx="{x:g}" cy="{y:g}" r="3.4" fill="#ffffff" stroke="{NET[net]}" stroke-width="1.6"/>')

    def tag(self, x, y, name, net, side="left") -> None:
        """Rail tag whose point touches (x, y); the body lies to the given side."""
        w = 7.2 * len(name) + 12
        c, f = NET[net], TINT[net]
        if side == "left":
            pts = [(x, y), (x - 9, y - 10), (x - 9 - w, y - 10), (x - 9 - w, y + 10), (x - 9, y + 10)]
            tx, ty = x - 9 - w / 2, y + 4
        elif side == "right":
            pts = [(x, y), (x + 9, y - 10), (x + 9 + w, y - 10), (x + 9 + w, y + 10), (x + 9, y + 10)]
            tx, ty = x + 9 + w / 2, y + 4
        else:  # up
            pts = [(x, y), (x + 7, y - 9), (x + w / 2, y - 9), (x + w / 2, y - 29), (x - w / 2, y - 29), (x - w / 2, y - 9), (x - 7, y - 9)]
            tx, ty = x, y - 15
        d = " ".join(f"{px:g},{py:g}" for px, py in pts)
        self.raw(f'<polygon points="{d}" fill="{f}" stroke="{c}" stroke-width="1.5" stroke-linejoin="round"/>')
        self.text(tx, ty, name, size=11.5, anchor="middle", fill=c, bold=True)

    # ---- boards and their pads --------------------------------------
    def module(self, ref, name, x0, y0, x1, y1, detail="") -> None:
        self.boxes[ref] = (x0, y0, x1, y1)
        self.rect(x0, y0, x1, y1, fill=BOX)
        ty = y0 - (22 if detail else 8)
        self.raw(f'<text x="{x0:g}" y="{ty:g}" font-size="13" fill="{INK}"><tspan font-weight="bold">{escape(ref)}</tspan><tspan dx="7">{escape(name)}</tspan></text>')
        if detail:
            self.text(x0, y0 - 8, detail, size=11, fill=GREY)

    def pin(self, ref, name, side, y, sub="", back=False, num="", net="sig", label="") -> None:
        x0, _, x1, _ = self.boxes[ref]
        key, name = name, label or name
        if side == "L":
            xe, xb, anchor = x0 - STUB, x0, "start"
            spans = f'<tspan font-weight="bold">{escape(name)}</tspan>' + (f'<tspan dx="6" fill="{GREY}" font-size="10.5">{escape(sub)}</tspan>' if sub else "")
            tx = x0 + (11 if back else 7)
        else:
            xe, xb, anchor = x1 + STUB, x1, "end"
            spans = (f'<tspan fill="{GREY}" font-size="10.5">{escape(sub)}</tspan>' if sub else "") + f'<tspan dx="{6 if sub else 0}" font-weight="bold">{escape(name)}</tspan>'
            tx = x1 - (11 if back else 7)
        self.wire([(xe, y), (xb, y)], net)
        if back:
            self.raw(f'<rect x="{xb - 3.5:g}" y="{y - 3.5:g}" width="7" height="7" fill="{INK}"/>')
        a = "" if anchor == "start" else ' text-anchor="end"'
        self.raw(f'<text x="{tx:g}" y="{y + 4:g}" font-size="12" fill="{INK}"{a}>{spans}</text>')
        if num:
            self.text(xb - 4 if side == "L" else xb + 4, y - 4, num, size=9.5, anchor="end" if side == "L" else "start", fill=GREY)
        self.pins[(ref, key)] = (xe, y)
        self.uses[(ref, key)] = 0

    def at(self, ref, name) -> tuple[float, float]:
        self.uses[(ref, name)] += 1
        return self.pins[(ref, name)]

    def empty(self, ref, name, note="") -> None:
        """Pad that stays empty: a cross at its end, the reason beside it."""
        x, y = self.at(ref, name)
        x0, _, x1, _ = self.boxes[ref]
        left = x < x0
        cx = x + (-4 if left else 4)
        self.nc(cx, y)
        if note:
            self.text(cx - 11 if left else cx + 11, y + 4, note, size=10.5, anchor="end" if left else "start", fill=GREY)

    def verify(self) -> None:
        unused = [f"{r}.{n}" for (r, n), k in self.uses.items() if k == 0]
        if unused:
            raise AssertionError("pads without a wire or a cross: " + ", ".join(unused))

    def svg(self) -> str:
        head = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">\n'
            "<title>Electronics schematic</title>\n"
            f'<rect width="{W}" height="{H}" fill="#ffffff"/>\n'
        )
        return head + "\n".join(self.el) + "\n</svg>\n"


def build() -> Sheet:
    S = Sheet()
    XL, XR = 766.0, 1026.0          # ends of the pads on the two sides of the controller
    PX = 1220.0                     # ends of the pads of amplifier, servo and LED
    PLUG0, MATE, PLUG1 = 1140.0, 1170.0, 1200.0
    RX = 1320.0                     # ends of the reader's pads

    # rows of the harness: plug A, plug B, and the reader's pads 1..13
    ROW_A = [740.0, 766.0, 792.0, 878.0, 904.0, 930.0]
    ROW_B = [956.0, 982.0, 1008.0, 1034.0, 1060.0, 1086.0]
    PAD = ROW_A + ROW_B[:3] + [1034.0, 1060.0, 1086.0, 1112.0]
    UNDER = 1156.0

    S.text(30, 44, "Electronics schematic", size=24, bold=True)
    S.text(30, 66, "Poké Ball in the tall grass: every pad of every board, the empty ones included. Pin map and values as in docs/electronics.md.", size=12.5, fill=GREY)

    # ---- the grass tongue and the two plugs (drawn first, below the wires)
    S.rect(MATE, 690, 1690, 1192, fill="#f3f8f1", stroke="#5f8f55", width=1.3, rx=10, dash="7 5")
    S.text(1678, 712, "Grass tongue", size=13, anchor="end", fill="#3f6f37", bold=True, italic=True)
    for rows, tagname in ((ROW_A, "A"), (ROW_B, "B")):
        S.rect(PLUG0, rows[0] - 16, PLUG1, rows[-1] + 8, fill="#ffffff", stroke=INK, width=1.3, rx=5)
        S.raw(f'<path d="M{MATE:g},{rows[0] - 16:g} V{rows[-1] + 8:g}" stroke="{INK}" stroke-width="1.1" stroke-dasharray="3 3"/>')
    S.text(MATE, 668, "Harness plugs A and B", size=12, anchor="middle", bold=True)
    S.text(MATE, 681, "6-pin, 1.25 mm pitch", size=10.5, anchor="middle", fill=GREY)
    S.text(MATE - 4, 1118, "socket half", size=10, anchor="end", fill=GREY)
    S.text(MATE + 4, 1118, "plug half", size=10, fill=GREY)
    S.text(MATE - 4, 1130, "on the core", size=10, anchor="end", fill=GREY)
    S.text(MATE + 4, 1130, "on the tongue", size=10, fill=GREY)

    # ---- boards -----------------------------------------------------
    S.module("U2", "TP4056 USB-C charger", 150, 120, 300, 335, "with DW01A protection")
    S.pin("U2", "IN+", "L", 196)
    S.pin("U2", "IN−", "L", 222)
    S.pin("U2", "B+", "L", 262, net="vbat")
    S.pin("U2", "B−", "L", 304, net="gnd")
    S.pin("U2", "OUT+", "R", 150, net="vbat")
    S.pin("U2", "OUT−", "R", 200, net="gnd")

    S.module("U3", "Adafruit MiniBoost 5 V", 450, 415, 610, 540, "TPS61023")
    S.pin("U3", "Vin", "L", 445, net="vbat")
    S.pin("U3", "GND", "L", 505, net="gnd")
    S.pin("U3", "5V", "R", 445, net="v5")
    S.pin("U3", "En", "R", 475)

    S.module("U1", "Seeed XIAO ESP32-S3 Plus", 786, 120, 1006, 1116)
    for name, y, sub, back, net in (
        ("BAT+", 150, "underside", False, "vbat"), ("BAT−", 176, "underside", False, "gnd"), ("GND", 202, "", False, "gnd"),
        ("D1", 240, "GPIO2", False, "sig"), ("D18", 475, "GPIO12", True, "sig"),
        ("5V", 600, "", False, "sig"), ("D2", 626, "GPIO3", False, "sig"), ("D6", 652, "GPIO43", False, "sig"), ("D7", 678, "GPIO44", False, "sig"),
    ):
        S.pin("U1", name, "L", y, sub=sub, back=back, net=net)
    for name, y, sub, back, net in (
        ("D13", 150, "GPIO40", True, "sig"), ("D12", 176, "GPIO39", True, "sig"), ("D11", 202, "GPIO38", True, "sig"), ("D17", 254, "GPIO13", True, "sig"),
        ("D15", 400, "GPIO42", True, "sig"), ("D14", 560, "GPIO41", True, "sig"),
        ("3V3", ROW_A[1], "", False, "v33"), ("D4", ROW_A[2], "GPIO5", False, "sig"), ("D5", ROW_A[3], "GPIO6", False, "sig"),
        ("D10", ROW_A[4], "GPIO9", False, "sig"), ("D9", ROW_A[5], "GPIO8", False, "sig"), ("D8", ROW_B[0], "GPIO7", False, "sig"),
        ("D3", ROW_B[1], "GPIO4", False, "sig"), ("D19", ROW_B[3], "GPIO11", True, "sig"), ("D0", ROW_B[4], "GPIO1", False, "sig"),
        ("D16", ROW_B[5], "GPIO10", True, "sig"),
    ):
        S.pin("U1", name, "R", y, sub=sub, back=back, net=net)

    S.module("U4", "MAX98357A amplifier", 1240, 125, 1380, 331, "Adafruit 3006 or a copy of it")
    for k, name in enumerate(("LRC", "BCLK", "DIN", "GAIN", "SD", "GND", "Vin")):
        S.pin("U4", name, "L", 150 + 26 * k, net={"GND": "gnd", "Vin": "vbat"}.get(name, "sig"))
    S.pin("U4", "+", "R", 190)
    S.pin("U4", "−", "R", 242)

    S.module("M1", "Servo SG90", 1240, 378, 1380, 505)
    S.pin("M1", "signal", "L", 400, sub="orange")
    S.pin("M1", "+", "L", 430, sub="red", net="v5")
    S.pin("M1", "−", "L", 480, sub="brown", net="gnd")

    S.module("LED1", "WS2812B on a 10 mm board", 1240, 538, 1380, 655)
    S.pin("LED1", "DIN", "L", 560)
    S.pin("LED1", "5V", "L", 590, net="v5")
    S.pin("LED1", "GND", "L", 630, net="gnd")
    S.pin("LED1", "DOUT", "R", 560)

    S.module("U5", "PN5180 reader, blue board", 1340, 715, 1460, 1137)
    names = ("+5V", "+3.3V", "RST", "NSS", "MOSI", "MISO", "SCK", "BUSY", "GND", "GPIO", "IRQ", "AUX", "REQ")
    for k, name in enumerate(names):
        S.pin("U5", name, "L", PAD[k], num=str(k + 1), net={"+5V": "v5", "+3.3V": "v33", "GND": "gnd"}.get(name, "sig"))
    # second ends of the two supply pads, for the legs of the hall switch
    S.pin("U5", "+3.3V'", "R", PAD[1], net="v33", label="+3.3V")
    S.pin("U5", "GND'", "R", PAD[8], net="gnd", label="GND")

    S.module("U6", "Hall switch, TO-92", 1540, 957, 1660, 1059, "DRV5032FB or AH3661UA")
    S.pin("U6", "VCC", "L", 982, num="1", net="v33")
    S.pin("U6", "GND", "L", 1008, num="2", net="gnd")
    S.pin("U6", "OUT", "L", 1034, num="3")

    # ---- power: cell, charger, battery rail -------------------------
    bx = 80.0
    x, y = S.at("U2", "B+")
    S.wire([(x, y), (bx, y), (bx, 276)], "vbat")
    x, y = S.at("U2", "B−")
    S.wire([(x, y), (bx, y), (bx, 290)], "gnd")
    S.raw(f'<path d="M{bx - 13:g},276 h26" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')
    S.raw(f'<path d="M{bx - 7:g},290 h14" stroke="{INK}" stroke-width="4.2" stroke-linecap="round"/>')
    S.text(bx - 22, 272, "+", size=13, anchor="middle", bold=True)
    S.raw(f'<text x="30" y="330" font-size="13" fill="{INK}"><tspan font-weight="bold">BT1</tspan><tspan dx="6">18650 cell</tspan></text>')
    S.lines(30, 345, ["unprotected, flat top", "plus at the dimple (+Y),", "minus at the spring (−Y)"], size=10.5, step=13, fill=GREY)
    S.empty("U2", "IN+")
    S.empty("U2", "IN−", "both stay empty")
    S.rect(100, 139, 150, 161, fill="#ffffff", stroke=INK, width=1.4, rx=9)
    S.text(125, 154, "USB-C", size=10.5, anchor="middle", bold=True)
    S.lines(30, 110, ["charging socket,", "in the black band"], size=10.5, step=13, fill=GREY)
    S.lines(150, 353, ["On the board: replace R_PROG, 1.2 kΩ,", "by 2.0 to 2.4 kΩ (charges with about 0.5 A)."], size=10.5, step=13, fill=GREY)

    x, y = S.at("U2", "OUT+")
    bx, by = S.at("U1", "BAT+")
    S.wire([(x, y), (bx, by)], "vbat", width=2.0)
    S.wire([(520, 150), (520, 139)], "vbat")
    S.dot(520, 150, "vbat")
    S.tag(520, 139, "VBAT", "vbat", "up")
    S.text(430, 143, "3.0 to 4.2 V, always on", size=10.5, anchor="end", fill=NET["vbat"])
    x, y = S.at("U2", "OUT−")
    S.wire([(x, y), (345, y)], "gnd")
    S.gnd(345, y)
    S.text(345, y + 30, "star point", size=10.5, anchor="middle", bold=True)

    # boost converter with C2 at its input
    vx, vy = S.at("U3", "Vin")
    gx, gy = S.at("U3", "GND")
    S.wire([(400, 150), (400, vy), (vx, vy)], "vbat")
    S.dot(400, 150, "vbat")
    S.dot(400, vy, "vbat")
    S.cap_v(400, vy, gy, "vbat", "gnd", polar=True)
    S.wire([(gx, gy), (400, gy)], "gnd")
    S.dot(400, gy, "gnd")
    S.gnd(400, gy)
    S.text(386, 471, "C2", size=12, anchor="end", bold=True)
    S.text(386, 485, "220 to 470 µF", size=10.5, anchor="end")
    x, y = S.at("U3", "5V")
    S.wire([(x, y), (648, y), (648, 405)], "v5")
    S.tag(648, 405, "+5V", "v5", "up")
    S.lines(530, 512, ["on the board:", "100 kΩ En to Vin"], size=10, step=12, anchor="middle", fill=GREY)
    x, y = S.at("U3", "En")
    bx, by = S.at("U1", "D18")
    S.wire([(x, y), (bx, by)])
    S.dot(700, y)
    S.resistor_v(700, y, 541)
    S.gnd(700, 541)
    S.text(688, 505, "R4", size=12, anchor="end", bold=True)
    S.text(688, 519, "4.7 kΩ", size=10.5, anchor="end")
    S.text(733, y - 5, "5 V on", size=10, anchor="middle", fill=GREY)

    # battery sense divider
    bx, by = S.at("U1", "D1")
    S.dot(640, 150, "vbat")
    S.resistor_v(640, 150, by, "vbat", "sig")
    S.wire([(640, by), (bx, by)])
    S.dot(640, by)
    S.dot(700, by)
    S.resistor_v(640, by, 320)
    S.cap_v(700, by, 320)
    S.wire([(640, 320), (700, 320)], "gnd")
    S.gnd(670, 320)
    S.text(628, 191, "R1", size=12, anchor="end", bold=True)
    S.text(628, 205, "2 MΩ", size=10.5, anchor="end")
    S.text(628, 276, "R2", size=12, anchor="end", bold=True)
    S.text(628, 290, "1 MΩ", size=10.5, anchor="end")
    S.text(714, 276, "C1", size=12, bold=True)
    S.text(714, 290, "100 nF", size=10.5)
    x, y = S.at("U1", "BAT−")
    gx, gy = S.at("U1", "GND")
    S.wire([(x, y), (746, y), (746, gy), (gx, gy)], "gnd")
    S.dot(746, gy, "gnd")
    S.gnd(746, gy)

    S.empty("U1", "5V", "USB 5 V, live only while the XIAO's own USB-C is plugged in")
    S.empty("U1", "D2", "strapping pin of the chip, leave open")
    S.empty("U1", "D6", "debug TX; the chip prints its boot text here at every wake")
    S.empty("U1", "D7", "debug RX")

    # USB-C and antenna of the controller
    S.wire([(830, 1116), (830, 1134)])
    S.rect(805, 1134, 855, 1156, fill="#ffffff", stroke=INK, width=1.4, rx=9)
    S.text(830, 1149, "USB-C", size=10.5, anchor="middle", bold=True)
    S.lines(830, 1172, ["for flashing only; never together", "with the charger's USB-C"], size=10.5, step=13, anchor="middle", fill=GREY)
    S.wire([(966, 1116), (966, 1156)])
    S.raw(f'<path d="M966,1138 l-10,-12 M966,1138 l10,-12" fill="none" stroke="{NET["sig"]}" stroke-width="1.6" stroke-linecap="round"/>')
    S.lines(966, 1172, ["U.FL socket:", "flexible antenna"], size=10.5, step=13, anchor="middle", fill=GREY)

    # ---- amplifier and speaker --------------------------------------
    for pad, pin_, label in (("D13", "LRC", "I2S word clock"), ("D12", "BCLK", "I2S bit clock"), ("D11", "DIN", "I2S data"), ("D17", "SD", "amplifier on")):
        x, y = S.at("U1", pad)
        S.wire([(x, y), S.at("U4", pin_)])
        S.text(x + 8, y - 5, label, size=10, fill=GREY)
    y = S.pins[("U1", "D17")][1]
    S.dot(1080, y)
    S.resistor_v(1080, y, 318)
    S.gnd(1080, 318)
    S.text(1093, 283, "R5", size=12, bold=True)
    S.text(1093, 297, "4.7 kΩ", size=10.5)
    S.empty("U4", "GAIN", "open: 9 dB")
    x, y = S.at("U4", "GND")
    S.wire([(x, y), (1152, y)], "gnd")
    S.gnd(1152, y)
    x, y = S.at("U4", "Vin")
    S.tag(x, y, "VBAT", "vbat", "left")
    S.lines(1336, 286, ["on the board:", "1 MΩ SD to Vin"], size=10, step=12, anchor="middle", fill=GREY)
    px, py = S.at("U4", "+")
    mx, my = S.at("U4", "−")
    S.wire([(px, py), (1462, py), (1462, 203)])
    S.wire([(mx, my), (1462, my), (1462, 229)])
    S.raw(f'<path d="M1454,203 h16 v26 h-16 Z M1470,203 l20,-16 v58 l-20,-16" fill="#ffffff" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    S.raw(f'<text x="1502" y="212" font-size="13" fill="{INK}"><tspan font-weight="bold">LS1</tspan><tspan dx="6">Speaker</tspan></text>')
    S.text(1502, 227, "Visaton K 40, 8 Ω", size=10.5, fill=GREY)

    # ---- servo with C3 ----------------------------------------------
    x, y = S.at("U1", "D15")
    S.wire([(x, y), S.at("M1", "signal")])
    S.text(x + 8, y - 5, "servo pulse", size=10, fill=GREY)
    px, py = S.at("M1", "+")
    mx, my = S.at("M1", "−")
    S.wire([(1150, py), (px, py)], "v5")
    S.tag(1150, py, "+5V", "v5", "left")
    S.dot(1195, py, "v5")
    S.cap_v(1195, py, my, "v5", "gnd", polar=True)
    S.wire([(mx, my), (1195, my)], "gnd")
    S.dot(1195, my, "gnd")
    S.gnd(1195, my)
    S.text(1180, 453, "C3", size=12, anchor="end", bold=True)
    S.text(1180, 467, "470 to 1000 µF", size=10.5, anchor="end")

    # ---- LED with D1 ------------------------------------------------
    x, y = S.at("U1", "D14")
    S.wire([(x, y), S.at("LED1", "DIN")])
    S.text(x + 8, y - 5, "LED data", size=10, fill=GREY)
    px, py = S.at("LED1", "5V")
    S.tag(1110, py, "+5V", "v5", "left")
    S.wire([(1110, py), (1140, py)], "v5")
    S.diode_h(1140, 1184, py, "v5", "v5")
    S.wire([(1184, py), (px, py)], "v5")
    S.raw(f'<text x="1162" y="{py + 23:g}" font-size="12" fill="{INK}" text-anchor="middle"><tspan font-weight="bold">D1</tspan><tspan dx="5" font-size="10.5">1N4148</tspan></text>')
    x, y = S.at("LED1", "GND")
    S.wire([(x, y), (1202, y)], "gnd")
    S.gnd(1202, y)
    S.empty("LED1", "DOUT", "DOUT and the 5V and GND pads beside it stay empty")

    # ---- harness to the tongue --------------------------------------
    for k, r in enumerate(ROW_A):
        S.text(MATE - 15, r - 5, f"A{k + 1}", size=9.5, anchor="middle", fill=GREY)
    for k, r in enumerate(ROW_B):
        S.text(MATE - 15, r - 5, f"B{k + 1}", size=9.5, anchor="middle", fill=GREY)
    # A1: switched 5 V for the transmitter
    x, y = S.at("U5", "+5V")
    S.tag(1110, y, "+5V", "v5", "left")
    S.wire([(1110, y), (x, y)], "v5")
    # A2: 3.3 V
    x, y = S.at("U1", "3V3")
    S.wire([(x, y), S.at("U5", "+3.3V")], "v33")
    S.text(x + 8, y - 5, "3.3 V, always on", size=10, fill=NET["v33"])
    # A3..B2: reset and SPI
    for pad, pin_, label in (("D4", "RST", "reset"), ("D5", "NSS", "chip select"), ("D10", "MOSI", "data out"), ("D9", "MISO", "data in"), ("D8", "SCK", "clock"), ("D3", "BUSY", "busy")):
        x, y = S.at("U1", pad)
        S.wire([(x, y), S.at("U5", pin_)])
        S.text(x + 8, y - 5, label, size=10, fill=GREY)
    y = ROW_A[2]
    S.dot(1080, y)
    S.resistor_v(1080, y, y + 54)
    S.gnd(1080, y + 54)
    S.text(1093, y + 24, "R3", size=12, bold=True)
    S.text(1093, y + 38, "100 kΩ", size=10.5)
    # B3: ground
    x, y = S.at("U5", "GND")
    S.wire([(1110, y), (x, y)], "gnd")
    S.gnd(1110, y)
    # B4: interrupt, to pad 11
    x, y = S.at("U1", "D19")
    ix, iy = S.at("U5", "IRQ")
    S.wire([(x, y), (1275, y), (1275, iy), (ix, iy)])
    S.text(x + 8, y - 5, "interrupt", size=10, fill=GREY)
    # B5: hall output, led below the reader
    x, y = S.at("U1", "D0")
    hx, hy = S.at("U6", "OUT")
    S.wire([(x, y), (1250, y), (1250, UNDER), (1508, UNDER), (1508, hy), (hx, hy)])
    S.text(x + 8, y - 5, "wake", size=10, fill=GREY)
    # B6: spare
    x, y = S.at("U1", "D16")
    S.wire([(x, y), (1222, y)])
    S.terminal(1226, y)
    S.text(x + 8, y - 5, "spare", size=10, fill=GREY)
    S.text(1226, y + 17, "free end", size=10, anchor="middle", fill=GREY)
    for name in ("GPIO", "AUX", "REQ"):
        S.empty("U5", name)
    # hall switch: supply and ground from the reader's own pads
    x, y = S.at("U5", "+3.3V'")
    hx, hy = S.at("U6", "VCC")
    S.wire([(x, y), (1496, y), (1496, hy), (hx, hy)], "v33")
    x, y = S.at("U5", "GND'")
    S.wire([(x, y), S.at("U6", "GND")], "gnd")
    S.lines(1524, 1078, ["Marked face towards you,", "legs down, from the left:", "1 VCC, 2 GND, 3 OUT."], size=10.5, step=13, fill=GREY)
    S.lines(1506, 812, ["The supply and ground legs", "of the hall switch are soldered", "to these two pads of the reader."], size=10.5, step=13, fill=GREY)

    # ---- variants ---------------------------------------------------
    S.rect(30, 745, 372, 905, fill="#fbfbfc", stroke=GREY, width=1.1, rx=8)
    S.text(44, 767, "Only with the AH3661UA hall switch", size=12.5, bold=True)
    S.terminal(120, 805, "v33")
    S.text(111, 809, "3V3 pad", size=11, anchor="end")
    S.resistor_h(124, 246, 805, "v33", "sig")
    S.terminal(250, 805)
    S.text(259, 809, "D0 pad", size=11)
    S.raw(f'<text x="185" y="792" font-size="12" fill="{INK}" text-anchor="middle"><tspan font-weight="bold">R6</tspan><tspan dx="5" font-size="10.5">1 MΩ</tspan></text>')
    S.text(44, 829, "at the controller: its output only pulls low", size=10.5, fill=GREY)
    S.terminal(120, 866, "v33")
    S.text(111, 870, "VCC leg", size=11, anchor="end")
    S.cap_h(124, 246, 866, "v33", "gnd")
    S.terminal(250, 866, "gnd")
    S.text(259, 870, "GND leg", size=11)
    S.raw(f'<text x="185" y="849" font-size="12" fill="{INK}" text-anchor="middle"><tspan font-weight="bold">C4</tspan><tspan dx="5" font-size="10.5">100 nF</tspan></text>')
    S.text(44, 893, "at the switch, across its supply legs", size=10.5, fill=GREY)

    S.rect(392, 745, 740, 905, fill="#fbfbfc", stroke=GREY, width=1.1, rx=8)
    S.text(406, 767, "Only if card detection has to wake the ball", size=12.5, bold=True)
    S.tag(470, 805, "+5V", "v5", "left")
    S.wire([(470, 805), (490, 805)], "v5")
    S.diode_h(490, 540, 805, "v5", "v5")
    S.wire([(540, 805), (634, 805)], "v5")
    S.dot(580, 805, "v5")
    S.terminal(638, 805, "v5")
    S.text(647, 802, "to plug A1", size=11)
    S.text(647, 815, "(reader +5V)", size=10.5, fill=GREY)
    S.terminal(466, 856, "v33")
    S.text(457, 860, "3V3 pad", size=11, anchor="end")
    S.diode_h(470, 560, 856, "v33", "v5")
    S.wire([(560, 856), (580, 856), (580, 805)], "v5")
    S.text(515, 790, "D2", size=12, anchor="middle", bold=True)
    S.text(515, 841, "D3", size=12, anchor="middle", bold=True)
    S.text(406, 893, "D2, D3: BAT43 or 1N5817, in place of the plain wire to A1", size=10.5, fill=GREY)

    # ---- notes ------------------------------------------------------
    S.text(30, 944, "Notes", size=13, bold=True)
    notes = [
        (0, "1. Every ground symbol is one net. Each ground wire ends at OUT− of the charger, the star point."),
        (15, "Nothing but the cell is connected to B+ and B−."),
        (0, "2. Tags of one name, VBAT or +5V, are one net. +5V is live only while the controller holds En high."),
        (0, "3. R4 and R5 keep the 5 V rail and the amplifier switched off whenever the controller does not drive them:"),
        (15, "at reset, while it is flashed, and asleep. Both boards carry a pull-up to the battery, so the two"),
        (15, "resistors have to be this small."),
        (0, "4. R3 keeps the reader in power-down while the controller sleeps."),
        (0, "5. C2 is soldered at the Vin pad of the boost converter, C3 at the servo, R1, R2 and C1 at pad D1."),
    ]
    for k, (dx, line) in enumerate(notes):
        S.text(30 + dx, 964 + 16 * k, line, size=11.5)
    S.raw(f'<path d="M30,1100 l8,8 M30,1108 l8,-8" fill="none" stroke="{GREY}" stroke-width="1.6" stroke-linecap="round"/>')
    S.text(46, 1108, "a pad that stays empty", size=11.5)
    S.raw(f'<rect x="210" y="1100" width="8" height="8" fill="{INK}"/>')
    S.text(226, 1108, "one of the nine small pads (1.27 mm) on the underside of the XIAO", size=11.5)
    S.dot(34, 1128)
    S.text(46, 1132, "wires that are joined; wires that only cross have no dot", size=11.5)

    S.verify()
    return S


def write(root: Path) -> list[Path]:
    img = root / "docs" / "img"
    img.mkdir(parents=True, exist_ok=True)
    svg = img / "schematic.svg"
    svg.write_text(build().svg(), encoding="utf-8", newline="\n")
    files = [svg]
    resvg = shutil.which("resvg")
    if resvg:
        png = img / "schematic.png"
        subprocess.run([resvg, "-w", str(PNG_WIDTH), str(svg), str(png)], check=True)
        files.append(png)
    else:
        print("resvg not found: docs/img/schematic.png was not rendered")
    return files
