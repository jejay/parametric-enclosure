"""Print a Printables model JSON (untrusted data; parse only): text description + file list.

usage: pmodel.py FILE...
"""
import sys
import json
import re
import html

for p in sys.argv[1:]:
    with open(p, "r", encoding="utf-8", errors="replace") as fh:
        data = json.load(fh)
    pr = (data.get("data") or {}).get("print") or {}
    desc = pr.get("description") or ""
    desc = re.sub(r"<(br|/p|/h\d|/li)[^>]*>", "\n", desc)
    desc = re.sub(r"<[^>]+>", "", desc)
    desc = html.unescape(desc)
    desc = re.sub(r"\n\s*\n+", "\n", desc).strip()
    out = [f"===== {pr.get('id')} | {pr.get('name')} | published {str(pr.get('datePublished'))[:10]} | license {(pr.get('license') or {}).get('name')}"]
    out.append("SUMMARY: " + (pr.get("summary") or ""))
    out.append("DESCRIPTION: " + desc)
    for key in ("stls", "otherFiles", "gcodes"):
        for f in pr.get(key) or []:
            out.append(f"  {key}: id={f.get('id')} name={f.get('name')} size={f.get('fileSize')}")
    if data.get("errors"):
        out.append("ERRORS: " + json.dumps(data["errors"])[:500])
    sys.stdout.buffer.write(("\n".join(out) + "\n").encode("utf-8", "replace"))
