"""Print the readable text of an Instructables showInstructableModel JSON dump.

Usage: python -I instructables_text.py FILE.json
Untrusted input: parsed with json only.
"""
import html
import json
import re
import sys


def strip(s):
    s = re.sub(r"<(br|/p|/li|/h\d|/div)[^>]*>", "\n", s or "")
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    with open(sys.argv[1], "rb") as f:
        d = json.loads(f.read().decode("utf-8", errors="replace"))
    print("TITLE:", d.get("title"))
    print("PUBLISHED:", d.get("publishDate"))
    print("SUPPLIES:", strip(d.get("supplies")))
    for i, st in enumerate(d.get("steps", [])):
        print(f"\n--- step {i}: {st.get('title')} ---")
        print(strip(st.get("body")))
        for fl in st.get("files", []):
            print("   FILE:", fl.get("name"), fl.get("downloadUrl"), fl.get("width"), fl.get("height"))


if __name__ == "__main__":
    main()
