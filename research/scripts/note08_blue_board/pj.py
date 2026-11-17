"""Pretty-print selected fields from a JSON file (untrusted data; parse only).

usage: pj.py FILE [maxlen]
Prints printables search items: id | name | user | date | summary
"""
import sys
import json

p = sys.argv[1]
maxlen = int(sys.argv[2]) if len(sys.argv) > 2 else 160
with open(p, "r", encoding="utf-8", errors="replace") as fh:
    data = json.load(fh)


def walk(o):
    if isinstance(o, dict):
        if "id" in o and "name" in o and "slug" in o:
            yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


for it in walk(data):
    user = (it.get("user") or {}).get("publicUsername", "")
    s = (it.get("summary") or "").replace("\n", " ")[:maxlen]
    line = f'{it["id"]} | {it["name"]} | {user} | {str(it.get("datePublished"))[:10]} | {s}'
    sys.stdout.buffer.write((line + "\n").encode("utf-8", "replace"))
