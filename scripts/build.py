#!/usr/bin/env python3
"""
build.py — publish a data file to the site.

Copies the chosen week to docs/events.json. The page fetches that file at
runtime, so this is the only step needed to publish.

    python3 scripts/build.py                 # newest file in data/
    python3 scripts/build.py data/2026-08-13.json

Note: docs/index.html fetches events.json, so opening it directly from disk
(file://) will not work. Serve the folder instead:

    cd docs && python3 -m http.server
"""
import sys, json, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if src is None:
        files = sorted(glob.glob(str(ROOT / "data" / "*.json")))
        if not files:
            print("no data files in data/")
            return 1
        src = Path(files[-1])

    data = json.loads(src.read_text())

    out = DOCS / "events.json"
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))

    print(f"published {src.name}: {len(data['events'])} events")
    print(f"  -> {out.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
