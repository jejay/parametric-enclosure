"""Print step text and image URLs of an iFixit API guide JSON dump.

Usage: python -I ifixit_guide_text.py FILE.json
Untrusted input: parsed with json only.
"""
import json
import sys


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    with open(sys.argv[1], "rb") as f:
        d = json.loads(f.read().decode("utf-8", errors="replace"))
    print("TITLE:", d.get("title"))
    print("PUBLISHED:", d.get("published_date"), "MODIFIED:", d.get("modified_date"))
    print("INTRO:", d.get("introduction_raw"))
    for st in d.get("steps", []):
        print(f"\n--- step {st.get('orderby')}: {st.get('title')} ---")
        for ln in st.get("lines", []):
            print("  *", ln.get("text_raw"))
        for im in (st.get("media") or {}).get("data", []) or []:
            if isinstance(im, dict):
                print("   IMG:", im.get("original") or im.get("large"))
    print("\nCONCLUSION:", d.get("conclusion_raw"))


if __name__ == "__main__":
    main()
