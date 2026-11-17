"""Print posts of a Discourse topic JSON dump (untrusted input, json only).

Usage: python -I discourse_text.py TOPIC.json [REGEX]
With REGEX only posts matching it are printed in full; others as one line.
"""
import html
import json
import re
import sys


def strip(s):
    s = re.sub(r"<img[^>]*src=\"([^\"]+)\"[^>]*>", r"[IMG \1]", s or "")
    s = re.sub(r"<(br|/p|/li|/h\d|/div|/blockquote)[^>]*>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    with open(sys.argv[1], "rb") as f:
        d = json.loads(f.read().decode("utf-8", errors="replace"))
    rx = re.compile(sys.argv[2], re.I) if len(sys.argv) > 2 else None
    print("TITLE:", d.get("title"), "| posts:", d.get("posts_count"))
    posts = d.get("post_stream", {}).get("posts", [])
    print("posts in dump:", len(posts))
    for p in posts:
        txt = strip(p.get("cooked"))
        head = f"--- #{p.get('post_number')} {p.get('created_at', '')[:10]} user#{p.get('user_id')}"
        if rx is None or rx.search(txt):
            print(head)
            print(txt)
        else:
            print(head, "|", txt[:100].replace("\n", " "))


if __name__ == "__main__":
    main()
