"""Print GitHub repository search results JSON (untrusted data; parse only).
usage: ghrepos.py FILE...
"""
import sys
import json

for p in sys.argv[1:]:
    with open(p, "r", encoding="utf-8", errors="replace") as fh:
        try:
            data = json.load(fh)
        except Exception as e:  # noqa: BLE001
            print(p, "not json", e)
            continue
    print("=====", p, "total", data.get("total_count"), data.get("message", ""))
    for it in data.get("items", []):
        line = "{full_name} | stars {stargazers_count} | pushed {pushed} | {desc}".format(
            full_name=it.get("full_name"), stargazers_count=it.get("stargazers_count"),
            pushed=str(it.get("pushed_at"))[:10], desc=(it.get("description") or "")[:140])
        sys.stdout.buffer.write((line + "\n").encode("utf-8", "replace"))
