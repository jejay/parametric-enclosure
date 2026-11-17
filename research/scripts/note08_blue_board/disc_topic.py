"""Print posts of a Discourse topic JSON (untrusted data; parse only).
usage: disc_topic.py FILE [--grep REGEX] [--posts a-b] [--maxlen N]
Shows post_number, username, date, text (HTML stripped), and attachment/link URLs.
"""
import sys
import json
import re
import html

p = sys.argv[1]
rx = None
if "--grep" in sys.argv:
    rx = re.compile(sys.argv[sys.argv.index("--grep") + 1], re.I)
lo, hi = 0, 10**9
if "--posts" in sys.argv:
    a, b = sys.argv[sys.argv.index("--posts") + 1].split("-")
    lo, hi = int(a), int(b)
maxlen = 4000
if "--maxlen" in sys.argv:
    maxlen = int(sys.argv[sys.argv.index("--maxlen") + 1])

with open(p, "r", encoding="utf-8", errors="replace") as fh:
    data = json.load(fh)
posts = (data.get("post_stream") or {}).get("posts") or data.get("posts") or []
stream = (data.get("post_stream") or {}).get("stream") or []
out = [f"TOPIC {data.get('id')} \"{data.get('title')}\" posts_count={data.get('posts_count')} loaded={len(posts)} stream={len(stream)}"]
for po in posts:
    n = po.get("post_number", 0)
    if not (lo <= n <= hi):
        continue
    cooked = po.get("cooked", "")
    links = re.findall(r'href="([^"]+)"', cooked)
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', cooked)
    txt = re.sub(r"<(br|/p|/h\d|/li|/blockquote|/div)[^>]*>", "\n", cooked)
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = html.unescape(txt)
    txt = re.sub(r"\n\s*\n+", "\n", txt).strip()
    if rx and not rx.search(txt):
        continue
    out.append(f"--- #{n} @{po.get('username')} {str(po.get('created_at'))[:10]} (id {po.get('id')})")
    out.append(txt[:maxlen])
    keep = [l for l in links if not l.startswith("/u/") and "user_avatar" not in l]
    if keep:
        out.append("   LINKS: " + " | ".join(keep[:25]))
    keepi = [i for i in imgs if "emoji" not in i and "user_avatar" not in i]
    if keepi:
        out.append("   IMGS: " + " | ".join(keepi[:12]))
sys.stdout.buffer.write(("\n".join(out) + "\n").encode("utf-8", "replace"))
