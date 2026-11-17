"""Print product facts and image URLs from downloaded tonies.com product pages.

Usage: python -I pdp_info.py PAGE.html [PAGE.html ...]
"""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for path in sys.argv[1:]:
    t = open(path, "rb").read().decode("utf-8", errors="replace")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', t, re.S)
    if not m:
        print(path, "NO NEXT DATA"); continue
    pp = json.loads(m.group(1))["props"]["pageProps"]
    p = pp.get("product") or {}
    print("=====", path)
    for k in ("name", "subName", "sku", "salesId", "gtin", "ageMin", "runTime", "publicationDate", "productWarnings", "price", "rating", "soldLastMonth"):
        print(f"  {k}: {p.get(k)}")
    print("  commonAttributes:", json.dumps(p.get("commonAttributes"), ensure_ascii=False))
    for k in p:
        if re.search(r"dimen|weight|size|measure", k, re.I):
            print("  EXTRA", k, p[k])
    print("  image:", json.dumps(p.get("image"), ensure_ascii=False))
    for im in p.get("images") or []:
        print("  IMG", im.get("src"), "|", im.get("alt"))
