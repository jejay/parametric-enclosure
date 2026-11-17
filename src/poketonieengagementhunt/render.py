"""Off-screen rendering of CadQuery shapes with VTK.

Produces shaded PNG images with true CAD edge lines, used for the building
manual and for visual checks.  No window is opened.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

import cadquery as cq
import vtk

# colour name -> (r, g, b, opacity)
PALETTE: dict[str, tuple[float, float, float, float]] = {
    "red": (0.86, 0.11, 0.12, 1.0),
    "white": (0.95, 0.95, 0.93, 1.0),
    "black": (0.13, 0.13, 0.14, 1.0),
    "clear": (0.80, 0.90, 0.98, 0.45),
    "stage": (0.20, 0.20, 0.23, 1.0),
    "chassis": (0.55, 0.58, 0.62, 1.0),
    "frame": (0.42, 0.47, 0.55, 1.0),
    "pawl": (0.98, 0.72, 0.10, 1.0),
    "slider": (0.98, 0.55, 0.10, 1.0),
    "cradle": (0.55, 0.05, 0.10, 1.0),
    "felt": (0.25, 0.02, 0.05, 1.0),
    "foam": (0.08, 0.08, 0.08, 1.0),
    "sleeve": (0.30, 0.75, 0.35, 1.0),
    "clamp": (0.30, 0.55, 0.85, 1.0),
    "pcb_blue": (0.08, 0.25, 0.60, 1.0),
    "pcb_black": (0.10, 0.12, 0.12, 1.0),
    "pcb_purple": (0.40, 0.12, 0.55, 1.0),
    "pcb_red": (0.70, 0.10, 0.10, 1.0),
    "copper": (0.80, 0.50, 0.20, 1.0),
    "gold": (0.90, 0.72, 0.25, 1.0),
    "brass": (0.80, 0.65, 0.30, 1.0),
    "ic": (0.15, 0.15, 0.15, 1.0),
    "connector": (0.92, 0.90, 0.82, 1.0),
    "metal": (0.75, 0.76, 0.78, 1.0),
    "metal_dark": (0.35, 0.36, 0.38, 1.0),
    "spring": (0.60, 0.70, 0.80, 1.0),
    "led_red": (0.95, 0.20, 0.20, 1.0),
    "led_glow": (1.00, 0.95, 0.60, 1.0),
    "speaker_cone": (0.18, 0.18, 0.20, 1.0),
    "cell_wrap": (0.25, 0.65, 0.35, 1.0),
    "servo_blue": (0.15, 0.40, 0.85, 1.0),
    "servo_clear": (0.55, 0.70, 0.95, 0.9),
    "cable": (0.60, 0.35, 0.15, 1.0),
    "diamond": (0.75, 0.92, 1.00, 0.85),
    "grass": (0.25, 0.70, 0.16, 1.0),          # #41B328, the main green measured in research/10
    "grass_dark": (0.11, 0.40, 0.26, 1.0),     # #1C6343
    "grass_light": (0.43, 0.90, 0.24, 1.0),    # #6EE53C
    "tonie_base": (0.17, 0.17, 0.18, 1.0),
    "tonie_body": (0.98, 0.85, 0.15, 1.0),
    "ghost": (0.80, 0.82, 0.85, 0.22),
    "highlight": (1.00, 0.55, 0.00, 1.0),
}


@dataclass
class Body:
    shape: cq.Shape
    colour: str
    opacity: float | None = None      # overrides the palette opacity
    edges: bool = True
    tag: str = ""                     # label id for call-outs


def _polydata(shape: cq.Shape, tol: float = 0.05, ang: float = 0.25) -> vtk.vtkPolyData:
    verts, tris = shape.tessellate(tol, ang)
    pts = vtk.vtkPoints()
    pts.SetNumberOfPoints(len(verts))
    for i, v in enumerate(verts):
        pts.SetPoint(i, v.x, v.y, v.z)
    cells = vtk.vtkCellArray()
    for t in tris:
        cells.InsertNextCell(3)
        cells.InsertCellPoint(t[0])
        cells.InsertCellPoint(t[1])
        cells.InsertCellPoint(t[2])
    pd = vtk.vtkPolyData()
    pd.SetPoints(pts)
    pd.SetPolys(cells)
    clean = vtk.vtkCleanPolyData()
    clean.SetInputData(pd)
    clean.SetTolerance(1e-6)
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputConnection(clean.GetOutputPort())
    normals.SetFeatureAngle(35.0)
    normals.SplittingOn()
    normals.ConsistencyOn()
    normals.Update()
    return normals.GetOutput()


def _edge_polydata(shape: cq.Shape, deflection: float = 0.08) -> vtk.vtkPolyData:
    """Discretise the true BRep edges into polylines."""
    from OCP.BRepAdaptor import BRepAdaptor_Curve
    from OCP.GCPnts import GCPnts_QuasiUniformDeflection

    from OCP.BRep import BRep_Tool
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopoDS import TopoDS

    # seam edges of spheres / cylinders are parametrisation artefacts: hide them
    seams: set[int] = set()
    fexp = TopExp_Explorer(shape.wrapped, TopAbs_FACE)
    while fexp.More():
        face = TopoDS.Face_s(fexp.Current())
        eexp = TopExp_Explorer(face, TopAbs_EDGE)
        while eexp.More():
            edge = TopoDS.Edge_s(eexp.Current())
            if BRep_Tool.IsClosed_s(edge, face):
                seams.add(cq.Edge(edge).hashCode())
            eexp.Next()
        fexp.Next()

    pts = vtk.vtkPoints()
    lines = vtk.vtkCellArray()
    for e in shape.Edges():
        if e.hashCode() in seams:
            continue
        try:
            curve = BRepAdaptor_Curve(e.wrapped)
            disc = GCPnts_QuasiUniformDeflection(curve, deflection)
            n = disc.NbPoints()
        except Exception:
            continue
        if n < 2:
            continue
        lines.InsertNextCell(n)
        for i in range(1, n + 1):
            p = disc.Value(i)
            lines.InsertCellPoint(pts.InsertNextPoint(p.X(), p.Y(), p.Z()))
    pd = vtk.vtkPolyData()
    pd.SetPoints(pts)
    pd.SetLines(lines)
    return pd


@dataclass
class Camera:
    """Camera described by a look direction (from the target towards the eye)."""

    azimuth: float = 35.0        # degrees around Z, 0 = looking from +X (front)
    elevation: float = 22.0      # degrees above the horizon
    target: Sequence[float] | None = None
    zoom: float = 1.0
    parallel: bool = True

    def direction(self) -> tuple[float, float, float]:
        a, e = math.radians(self.azimuth), math.radians(self.elevation)
        return (math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))


@dataclass
class Scene:
    bodies: list[Body] = field(default_factory=list)

    def add(self, shapes: Iterable[tuple[cq.Shape, str]], opacity: float | None = None, edges: bool = True, tag: str = "", colour: str | None = None) -> "Scene":
        for shape, col in shapes:
            self.bodies.append(Body(shape, colour or col, opacity, edges, tag))
        return self


def render(
    scene: Scene,
    path: str | Path,
    camera: Camera | None = None,
    size: tuple[int, int] = (1600, 1200),
    background: tuple[float, float, float] = (1.0, 1.0, 1.0),
    anchors: dict[str, Sequence[float]] | None = None,
) -> dict[str, tuple[float, float]]:
    """Render the scene to a PNG.

    ``anchors`` maps names to 3D points; the function returns their pixel
    coordinates (origin top-left) so that call-outs can be drawn afterwards.
    """
    camera = camera or Camera()
    ren = vtk.vtkRenderer()
    ren.SetBackground(*background)
    ren.SetUseDepthPeeling(1)
    ren.SetMaximumNumberOfPeels(12)
    ren.SetOcclusionRatio(0.0)

    for b in scene.bodies:
        r, gg, bl, op = PALETTE.get(b.colour, (0.6, 0.6, 0.6, 1.0))
        if b.opacity is not None:
            op = b.opacity
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(_polydata(b.shape))
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        prop = actor.GetProperty()
        prop.SetColor(r, gg, bl)
        prop.SetOpacity(op)
        prop.SetAmbient(0.32)
        prop.SetDiffuse(0.68)
        prop.SetSpecular(0.18)
        prop.SetSpecularPower(24)
        ren.AddActor(actor)
        if b.edges and op > 0.15:
            em = vtk.vtkPolyDataMapper()
            em.SetInputData(_edge_polydata(b.shape))
            ea = vtk.vtkActor()
            ea.SetMapper(em)
            ep = ea.GetProperty()
            shade = 0.05 if (r + gg + bl) > 0.9 else 0.55
            ep.SetColor(shade, shade, shade)
            ep.SetLineWidth(1.6)
            ep.SetOpacity(min(1.0, 0.35 + op))
            ep.LightingOff()
            ren.AddActor(ea)

    win = vtk.vtkRenderWindow()
    win.SetOffScreenRendering(1)
    win.SetMultiSamples(0)
    win.SetAlphaBitPlanes(1)
    win.AddRenderer(ren)
    win.SetSize(*size)

    cam = ren.GetActiveCamera()
    cam.SetParallelProjection(1 if camera.parallel else 0)
    ren.ResetCamera()
    bounds = ren.ComputeVisiblePropBounds()
    centre = camera.target or (
        (bounds[0] + bounds[1]) / 2,
        (bounds[2] + bounds[3]) / 2,
        (bounds[4] + bounds[5]) / 2,
    )
    d = camera.direction()
    diag = math.dist((bounds[0], bounds[2], bounds[4]), (bounds[1], bounds[3], bounds[5]))
    dist = max(diag, 1.0) * 2.2
    cam.SetFocalPoint(*centre)
    cam.SetPosition(centre[0] + d[0] * dist, centre[1] + d[1] * dist, centre[2] + d[2] * dist)
    cam.SetViewUp(0, 0, 1)
    ren.ResetCamera()
    cam.Zoom(camera.zoom * 1.15)
    ren.ResetCameraClippingRange()

    # one key light fixed to the camera plus a soft fill from above
    ren.RemoveAllLights()
    key = vtk.vtkLight()
    key.SetLightTypeToCameraLight()
    key.SetPosition(-0.6, 0.9, 1.0)
    key.SetIntensity(0.85)
    ren.AddLight(key)
    fill = vtk.vtkLight()
    fill.SetLightTypeToCameraLight()
    fill.SetPosition(0.8, -0.3, 0.6)
    fill.SetIntensity(0.35)
    ren.AddLight(fill)

    fxaa = ren.GetFXAAOptions()
    ren.SetUseFXAA(True)
    fxaa.SetSubpixelBlendLimit(0.75)

    win.Render()
    out: dict[str, tuple[float, float]] = {}
    if anchors:
        coord = vtk.vtkCoordinate()
        coord.SetCoordinateSystemToWorld()
        for name, p in anchors.items():
            coord.SetValue(float(p[0]), float(p[1]), float(p[2]))
            x, y = coord.GetComputedDisplayValue(ren)
            out[name] = (float(x), float(size[1] - y))

    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(win)
    w2i.SetInputBufferTypeToRGB()
    w2i.ReadFrontBufferOff()
    w2i.Update()
    writer = vtk.vtkPNGWriter()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    writer.SetFileName(str(path))
    writer.SetInputConnection(w2i.GetOutputPort())
    writer.Write()
    win.Finalize()
    return out


# --------------------------------------------------------------------------
# helpers for the manual
# --------------------------------------------------------------------------
def clip(bodies: Iterable[tuple[cq.Shape, str]], keep: cq.Shape) -> list[tuple[cq.Shape, str]]:
    """Intersect every body with ``keep`` (used for section views)."""
    out = []
    for shape, colour in bodies:
        try:
            cut = shape.intersect(keep)
        except Exception:
            continue
        if cut.isNull() or not list(cut.Solids()):
            continue
        out.append((cut, colour))
    return out


def _font(size: int):
    from PIL import ImageFont

    for name in ("arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def callouts(path: str | Path, anchors: dict[str, tuple[float, float]], numbers: dict[str, int], radius: int = 23) -> None:
    """Draw numbered balloons in two side columns with leader lines to the anchors."""
    from PIL import Image, ImageDraw

    img = Image.open(path).convert("RGB")
    w, h = img.size
    draw = ImageDraw.Draw(img)
    font = _font(int(radius * 1.05))
    keys = [k for k in numbers if k in anchors]
    left = sorted((k for k in keys if anchors[k][0] < w / 2), key=lambda k: anchors[k][1])
    right = sorted((k for k in keys if anchors[k][0] >= w / 2), key=lambda k: anchors[k][1])
    # keep the columns balanced
    while len(left) - len(right) > 1:
        k = max(left, key=lambda k: anchors[k][0])
        left.remove(k)
        right.append(k)
    while len(right) - len(left) > 1:
        k = min(right, key=lambda k: anchors[k][0])
        right.remove(k)
        left.append(k)
    left.sort(key=lambda k: anchors[k][1])
    right.sort(key=lambda k: anchors[k][1])
    gap = int(radius * 2.5)
    for column, x in ((left, radius + 14), (right, w - radius - 14)):
        n = len(column)
        if not n:
            continue
        # put every balloon at the height of its anchor, then push overlapping
        # balloons apart so that the leader lines stay short and do not cross
        ys = [min(max(anchors[k][1], radius + 8), h - radius - 8) for k in column]
        if n * gap > h - 2 * radius:
            ys = [(i + 0.5) * h / n for i in range(n)]
        else:
            for i in range(1, n):
                ys[i] = max(ys[i], ys[i - 1] + gap)
            for i in range(n - 1, -1, -1):
                limit = h - radius - 8 - (n - 1 - i) * gap
                ys[i] = min(ys[i], limit)
            for i in range(1, n):
                ys[i] = max(ys[i], ys[i - 1] + gap)
        for k, y in zip(column, ys):
            y = int(y)
            ax, ay = anchors[k]
            draw.line([(x, y), (ax, ay)], fill=(60, 60, 60), width=2)
            draw.ellipse([ax - 4, ay - 4, ax + 4, ay + 4], fill=(60, 60, 60))
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(255, 255, 255), outline=(20, 20, 20), width=3)
            text = str(numbers[k])
            box = draw.textbbox((0, 0), text, font=font)
            draw.text((x - (box[2] - box[0]) / 2 - box[0], y - (box[3] - box[1]) / 2 - box[1]), text, fill=(20, 20, 20), font=font)
    img.save(path)


def caption(path: str | Path, text: str, size: int = 34) -> None:
    """Write a caption into the lower left corner of an image."""
    from PIL import Image, ImageDraw

    img = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.text((24, img.size[1] - size - 24), text, fill=(40, 40, 40), font=_font(size))
    img.save(path)


def arrow(path: str | Path, p0: tuple[float, float], p1: tuple[float, float], colour=(230, 110, 0), width: int = 6) -> None:
    """Draw an arrow from pixel p0 to pixel p1."""
    from PIL import Image, ImageDraw

    img = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.line([p0, p1], fill=colour, width=width)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for s in (-1, 1):
        a = ang + math.pi + s * 0.45
        draw.line([p1, (p1[0] + 26 * math.cos(a), p1[1] + 26 * math.sin(a))], fill=colour, width=width)
    img.save(path)
