#!/usr/bin/env python3
"""
build.py — publish a data file to the site.

Copies the chosen week to docs/events.json, projecting the geography from
config/brief.yml over it on the way. The page fetches that file at runtime, so
this is the only step needed to publish.

    python3 scripts/build.py                 # newest file in data/
    python3 scripts/build.py data/2026-08-13.json

brief.yml is the source of truth for WHERE. `origin` and `regions` there decide
the site's starting point, its region order, and its colours — change them and
the next build follows, with no edit to the data file or to index.html. The
data file keeps what only it knows: the events and the window they cover.

If `standfirst` contains {origin}, the origin label is substituted in, so the
masthead line stays true after a fork.

pyyaml is optional. Without it the config cannot be read and the data file is
published unchanged, which is the pre-existing behaviour.

Note: docs/index.html fetches events.json, so opening it directly from disk
(file://) will not work. Serve the folder instead:

    cd docs && python3 -m http.server
"""
import sys, json, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BRIEF = ROOT / "config" / "brief.yml"

# Keys copied from a brief.yml region onto a site geo. Anything else in the
# region entry (`includes`, for instance) is research input, not site data.
GEO_KEYS = ("id", "label", "rank", "blurb", "color")


def load_brief(path):
    """Read brief.yml. Returns None if pyyaml is absent or the file is unreadable."""
    try:
        import yaml
    except ImportError:
        return None
    try:
        return yaml.safe_load(path.read_text())
    except (OSError, ValueError):
        return None


def apply_brief(data, brief):
    """Project brief.yml's geography onto a data file's meta. Returns a note list."""
    meta = data.setdefault("meta", {})
    notes = []

    origin = brief.get("origin")
    if isinstance(origin, dict) and "label" in origin:
        if meta.get("origin") != origin:
            notes.append(f"origin -> {origin['label']}")
        meta["origin"] = origin

    regions = brief.get("regions")
    if isinstance(regions, list) and regions:
        geos = [{k: r[k] for k in GEO_KEYS if k in r} for r in regions]
        geos.sort(key=lambda g: g.get("rank", 99))
        if meta.get("geos") != geos:
            notes.append(f"geos -> {len(geos)} regions from brief.yml")
        meta["geos"] = geos

    # The travel tables (venues, city centroids, corridors) are geography too, and
    # index.html holds none of its own — so they ride along exactly like regions.
    travel = brief.get("travel")
    if isinstance(travel, dict) and travel:
        if meta.get("travel") != travel:
            notes.append(
                f"travel -> {len(travel.get('venues') or {})} venues, "
                f"{len(travel.get('corridors') or [])} corridors from brief.yml"
            )
        meta["travel"] = travel

    standfirst = (brief.get("meta") or {}).get("standfirst")
    if standfirst:
        label = (meta.get("origin") or {}).get("label", "")
        meta["standfirst"] = standfirst.strip().replace("{origin}", label)

    return notes

def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if src is None:
        files = sorted(glob.glob(str(ROOT / "data" / "*.json")))
        if not files:
            print("no data files in data/")
            return 1
        src = Path(files[-1])

    data = json.loads(src.read_text())

    brief = load_brief(BRIEF)
    if brief is None:
        notes = ["config/brief.yml not read (install pyyaml to apply it) — data published as-is"]
    else:
        notes = apply_brief(data, brief) or ["config/brief.yml applied, no change"]

    out = DOCS / "events.json"
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))

    print(f"published {src.name}: {len(data['events'])} events")
    for n in notes:
        print(f"  {n}")
    print(f"  -> {out.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
