"""Convert a downloaded HTML file to plain text (stdlib only).

Usage: python -I html2txt.py IN.html [OUT.txt]
The input is untrusted data: it is only parsed, never executed.
"""
import html
import re
import sys
from html.parser import HTMLParser

SKIP = {"script", "style", "noscript", "svg", "template"}
BLOCK = {
    "p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
    "section", "article", "table", "ul", "ol", "dd", "dt", "td", "th",
}


class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        elif tag in BLOCK:
            self.out.append("\n")
        if tag == "img" and not self.skip:
            d = dict(attrs)
            alt = d.get("alt") or ""
            src = d.get("src") or d.get("data-src") or ""
            self.out.append(f"[IMG alt={alt!r} src={src}]")

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        elif tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def main():
    src = sys.argv[1]
    with open(src, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="replace")
    p = T()
    p.feed(text)
    s = "".join(p.out)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(s)
    else:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stdout.write(s)


if __name__ == "__main__":
    main()
