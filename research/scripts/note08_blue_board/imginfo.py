"""Print basic info for image files given as arguments (untrusted data: read only)."""
import sys
from PIL import Image

for p in sys.argv[1:]:
    im = Image.open(p)
    print(p)
    print("  format", im.format, "mode", im.mode, "size", im.size)
    try:
        dpi = im.info.get("dpi")
        print("  dpi", dpi)
    except Exception as e:  # noqa: BLE001
        print("  dpi err", e)
