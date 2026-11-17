"""Merge Printables search result dumps and list unique models.

Usage: python -I printables_list.py DIR
Untrusted input: parsed with json only.
"""
import glob
import json
import os
import sys


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    seen = {}
    for fn in sorted(glob.glob(os.path.join(sys.argv[1], "search_*.json"))):
        try:
            d = json.load(open(fn, encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            print(fn, "ERR", e)
            continue
        sp = (d.get("data") or {}).get("searchPrints2") or {}
        items = sp.get("items") or []
        print(os.path.basename(fn), "total", sp.get("totalCount"), "got", len(items))
        for it in items:
            seen.setdefault(it["id"], it)
    print("unique", len(seen))
    for i, it in sorted(seen.items(), key=lambda kv: kv[1].get("datePublished") or ""):
        print(f"{i}\t{(it.get('datePublished') or '')[:10]}\t{it.get('name')}\t| {(it.get('summary') or '')[:140]}")


if __name__ == "__main__":
    main()
