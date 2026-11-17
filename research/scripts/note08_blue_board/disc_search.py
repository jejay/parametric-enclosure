"""Print Discourse search.json results (untrusted data; parse only).
usage: disc_search.py FILE... [--max N]
"""
import sys
import json
import re

args = [a for a in sys.argv[1:] if not a.startswith("--")]
mx = 12
if "--max" in sys.argv:
    mx = int(sys.argv[sys.argv.index("--max") + 1])
    args = [a for a in args if a != str(mx)]
for p in args:
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as fh:
            data = json.load(fh)
    except Exception as e:  # noqa: BLE001
        print("=====", p, "ERR", e)
        continue
    topics = {t["id"]: t for t in data.get("topics", [])}
    posts = data.get("posts", [])
    out = [f"===== {p}: {len(posts)} posts"]
    for po in posts[:mx]:
        t = topics.get(po.get("topic_id"), {})
        blurb = re.sub(r"\s+", " ", po.get("blurb", ""))[:230]
        out.append(f't/{po.get("topic_id")}/{po.get("post_number")} [{str(po.get("created_at"))[:10]}] "{t.get("title", "")[:70]}" @{po.get("username")}: {blurb}')
    sys.stdout.buffer.write(("\n".join(out) + "\n").encode("utf-8", "replace"))
