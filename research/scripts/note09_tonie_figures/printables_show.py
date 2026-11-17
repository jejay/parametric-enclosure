"""Print the full text of selected Printables model records.

Usage: python -I printables_show.py DIR ID [ID ...]
Untrusted input: parsed with json/re only.
"""
import html
import json
import os
import re
import sys


def strip(s):
    s = re.sub(r"<(br|/p|/li|/h\d|/div|/tr)[^>]*>", "\n", s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    d = sys.argv[1]
    for i in sys.argv[2:]:
        p = json.load(open(os.path.join(d, f"print_{i}.json"), encoding="utf-8"))["data"]["print"]
        print(f"\n===== {p['id']} | {(p.get('datePublished') or '')[:10]} | {p.get('name')} | by {(p.get('user') or {}).get('publicUsername')}")
        print("SUMMARY:", p.get("summary"))
        print(strip(p.get("description"))[:3500])
        print("FILES:", ", ".join(f"{s.get('name')}" for s in (p.get("stls") or []))[:600])
        imgs = [im.get("filePath") for im in (p.get("images") or [])][:6]
        print("IMAGES:", imgs)


if __name__ == "__main__":
    main()
