"""Print a GitHub git-tree JSON listing (untrusted data; parse only).
usage: ghtree.py FILE [substring-filter ...]
"""
import sys
import json

p = sys.argv[1]
filters = [f.lower() for f in sys.argv[2:]]
with open(p, "r", encoding="utf-8", errors="replace") as fh:
    data = json.load(fh)
if "tree" not in data:
    print("no tree:", str(data)[:300])
    sys.exit(0)
print("truncated:", data.get("truncated"), "entries:", len(data["tree"]))
for e in data["tree"]:
    path = e.get("path", "")
    if filters and not any(f in path.lower() for f in filters):
        continue
    if e.get("type") == "blob":
        sys.stdout.buffer.write(f'{e.get("size", 0):>10} {path}\n'.encode("utf-8", "replace"))
