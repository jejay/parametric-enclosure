"""Extract and explore the __NEXT_DATA__ JSON of a downloaded Next.js page.

Usage:
  python -I nextdata.py dump  PAGE.html OUT.json        # write pretty JSON
  python -I nextdata.py grep  PAGE.html REGEX [CTX]     # print JSON paths whose key or string value matches
  python -I nextdata.py path  PAGE.html a.b.0.c         # print the value at a path
Untrusted input: parsed with json/re only.
"""
import json
import re
import sys


def load(path):
    with open(path, "rb") as f:
        t = f.read().decode("utf-8", errors="replace")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', t, re.S)
    if not m:
        raise SystemExit("no __NEXT_DATA__")
    return json.loads(m.group(1))


def walk(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{p}.{k}" if p else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{p}.{i}")
    else:
        yield p, o


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cmd, page = sys.argv[1], sys.argv[2]
    d = load(page)
    if cmd == "dump":
        with open(sys.argv[3], "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        print("written", sys.argv[3])
    elif cmd == "grep":
        rx = re.compile(sys.argv[3], re.I)
        ctx = int(sys.argv[4]) if len(sys.argv) > 4 else 300
        seen = set()
        for p, v in walk(d):
            s = v if isinstance(v, str) else json.dumps(v)
            if rx.search(p) or rx.search(s):
                key = (p.rsplit(".", 1)[-1], s[:ctx])
                if key in seen:
                    continue
                seen.add(key)
                print(f"{p} = {s[:ctx]!r}")
    elif cmd == "path":
        cur = d
        for part in sys.argv[3].split("."):
            cur = cur[int(part)] if isinstance(cur, list) else cur[part]
        print(json.dumps(cur, ensure_ascii=False, indent=1)[:20000])


if __name__ == "__main__":
    main()
