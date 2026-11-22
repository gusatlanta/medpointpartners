"""List HTML pages missing the Google Analytics 4 tag.

    python tools/check_ga.py            # check the site folder
    python tools/check_ga.py <folder>   # check somewhere else

Prints every page whose <head> does not contain the standard gtag.js snippet
for G-PP39BB32PP. Exits 0 when every page has it, 1 when any page does not.
"""
import sys
from pathlib import Path

GA_ID = "G-PP39BB32PP"
SRC = f"https://www.googletagmanager.com/gtag/js?id={GA_ID}"
CONFIG = f"gtag('config', '{GA_ID}')"

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent


def head_has_tag(text):
    end = text.lower().find("</head>")
    if end == -1:
        return False
    head = text[:end]
    return SRC in head and CONFIG in head


def main():
    pages = sorted(
        p for p in ROOT.rglob("*.html")
        if ".git" not in p.parts and "__pycache__" not in p.parts
    )
    missing = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if not head_has_tag(text):
            missing.append(page.relative_to(ROOT).as_posix())

    print(f"{len(pages)} HTML pages")
    if missing:
        print(f"{len(missing)} missing the GA4 tag ({GA_ID}):")
        for name in missing:
            print(name)
        return 1
    print(f"every page has the GA4 tag ({GA_ID})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
