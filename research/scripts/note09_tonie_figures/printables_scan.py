"""Scan downloaded Printables model records for dimension statements.

Usage: python -I printables_scan.py DIR [REGEX]
Prints, per model that mentions Tonies, every sentence containing a number with mm/cm
(or matching REGEX). Untrusted input: parsed with json/re only.
"""
import glob
import html
import json
import os
import re
import sys


def strip(s):
    s = re.sub(r"<(br|/p|/li|/h\d|/div|/tr)[^>]*>", "\n", s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"[ \t]+", " ", s)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    d = sys.argv[1]
    rx = re.compile(sys.argv[2], re.I) if len(sys.argv) > 2 else re.compile(
        r"\d+(?:[.,]\d+)?\s*(?:mm|cm|inch|in\b|\")|durchmesser|diameter|\bØ", re.I)
    n = 0
    for fn in sorted(glob.glob(os.path.join(d, "print_*.json")), key=lambda p: int(re.findall(r"print_(\d+)", p)[0])):
        try:
            p = json.load(open(fn, encoding="utf-8"))["data"]["print"]
        except Exception:  # noqa: BLE001
            continue
        if not p:
            continue
        text = (p.get("name") or "") + "\n" + (p.get("summary") or "") + "\n" + strip(p.get("description"))
        if not re.search(r"toni", text, re.I):
            continue
        hits = []
        for sent in re.split(r"(?<=[.!?])\s+|\n+", text):
            if rx.search(sent) and len(sent.strip()) > 3:
                hits.append(sent.strip()[:400])
        if hits:
            n += 1
            user = (p.get("user") or {}).get("publicUsername")
            print(f"\n### {p['id']} | {(p.get('datePublished') or '')[:10]} | {p.get('name')} | by {user}")
            print(f"    https://www.printables.com/model/{p['id']}-{p.get('slug')}")
            seen = set()
            for h_ in hits:
                if h_ not in seen:
                    seen.add(h_)
                    print("   -", h_)
    print("\nmodels with hits:", n)


if __name__ == "__main__":
    main()
