#!/usr/bin/env python3
"""
validate.py — check an events file against the schema and against brief.yml.

The schema catches shape errors. This script also catches the errors that
matter more in practice: vocabulary drift, regions that don't exist, duplicate
ids, and events outside the stated window.

    python3 scripts/validate.py data/2026-08-13.json
    python3 scripts/validate.py            # validates every file in data/
"""
import sys, json, glob, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path):
    """Minimal YAML reader so the repo has no install step for validation."""
    try:
        import yaml
        return yaml.safe_load(path.read_text())
    except ImportError:
        return None


def check(path, brief):
    errs, warns = [], []
    try:
        doc = json.loads(Path(path).read_text())
    except json.JSONDecodeError as e:
        return [f"{path}: invalid JSON — {e}"], []

    meta = doc.get("meta", {})
    events = doc.get("events", [])
    if not events:
        errs.append(f"{path}: no events")
        return errs, warns

    geos = {g["id"] for g in meta.get("geos", [])}
    vocab = meta.get("vocab", {})
    v_type = set(vocab.get("type", []))
    v_venue = set(vocab.get("venue_type", []))
    v_cost = set(vocab.get("cost", []))

    # brief.yml is the source of truth for regions when it's readable
    if brief:
        brief_geos = {r["id"] for r in brief.get("regions", [])}
        if brief_geos and brief_geos != geos:
            warns.append(
                f"{path}: regions differ from brief.yml — "
                f"only in data: {sorted(geos - brief_geos) or '—'}; "
                f"only in brief: {sorted(brief_geos - geos) or '—'}"
            )

    try:
        w0 = datetime.date.fromisoformat(meta["window_start"])
        w1 = datetime.date.fromisoformat(meta["window_end"])
    except Exception:
        errs.append(f"{path}: meta.window_start / window_end missing or malformed")
        w0 = w1 = None

    seen = set()
    required = ("id", "date", "title", "venue", "city", "geo", "type", "venue_type", "cost")

    for i, e in enumerate(events):
        tag = e.get("id") or f"index {i}"

        for k in required:
            if k not in e:
                errs.append(f"{path}: [{tag}] missing required field '{k}'")

        if e.get("id") in seen:
            errs.append(f"{path}: duplicate id '{e['id']}'")
        seen.add(e.get("id"))

        if e.get("geo") and e["geo"] not in geos:
            errs.append(f"{path}: [{tag}] unknown region '{e['geo']}'")

        for t in e.get("type", []):
            if v_type and t not in v_type:
                errs.append(f"{path}: [{tag}] type '{t}' not in vocabulary")

        if v_venue and e.get("venue_type") not in v_venue:
            errs.append(f"{path}: [{tag}] venue_type '{e.get('venue_type')}' not in vocabulary")

        if v_cost and e.get("cost") not in v_cost:
            errs.append(f"{path}: [{tag}] cost '{e.get('cost')}' not in vocabulary")

        if w0 and e.get("date"):
            try:
                d = datetime.date.fromisoformat(e["date"])
                if not (w0 <= d <= w1):
                    errs.append(f"{path}: [{tag}] date {e['date']} outside window {w0}..{w1}")
            except ValueError:
                errs.append(f"{path}: [{tag}] malformed date '{e['date']}'")

        if e.get("start") and not (
            len(e["start"]) == 5 and e["start"][2] == ":" and e["start"].replace(":", "").isdigit()
        ):
            errs.append(f"{path}: [{tag}] start '{e['start']}' should be HH:MM")

        note = e.get("note", "")
        if note and len(note) > 400:
            warns.append(f"{path}: [{tag}] note is {len(note)} chars — trim toward 400")
        if not note:
            warns.append(f"{path}: [{tag}] no note; every listing should say something")

    featured = [e for e in events if e.get("featured")]
    cap = (brief or {}).get("output", {}).get("featured_max", 8)
    if len(featured) > cap:
        warns.append(f"{path}: {len(featured)} featured events, cap is {cap}")

    return errs, warns


def main():
    brief = load_yaml(ROOT / "config" / "brief.yml")
    if brief is None:
        print("note: PyYAML not installed — skipping brief.yml cross-checks\n")

    targets = sys.argv[1:] or sorted(glob.glob(str(ROOT / "data" / "*.json")))
    if not targets:
        print("no data files found")
        return 1

    all_err, all_warn, total = [], [], 0
    for t in targets:
        e, w = check(t, brief)
        all_err += e
        all_warn += w
        try:
            total += len(json.loads(Path(t).read_text()).get("events", []))
        except Exception:
            pass

    for w in all_warn:
        print(f"  warn  {w}")
    for e in all_err:
        print(f" ERROR  {e}")

    print(f"\n{len(targets)} file(s), {total} events, "
          f"{len(all_err)} error(s), {len(all_warn)} warning(s)")
    return 1 if all_err else 0


if __name__ == "__main__":
    sys.exit(main())
