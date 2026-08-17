# Project guidance for Claude Code

**This is not the `new-swe-project` scaffold, and does not owe one.** That skill
refuses to retrofit a repo that already contains code, and this one arrived as a
tarball with its own git history. There is no CONSTITUTION, no `docs/HANDOFF.md`
and no ritual docs — do not follow references to them.

That is a deliberate position, not a gap. **Tier is declared per spec, not per
project** (`delivery-tiers`), so most work here declares `probe` — short-form
spec, worktree, build, behavioural check, evidence — which owes no plan, no
NASA audit, no tier registry and no merge ritual. The build-tier tree becomes
owed only when a spec here is declared `build`; see the parked row in
[BACKLOG.md](BACKLOG.md) for the layout constraint that applies when it does.

**Two things never relax, at any tier:**

- **Short-form specs go in a root-level `specs/`, never `docs/`** — see below.
- **`delivery-tiers`' floor:** a written spec, the owner's behavioural check, no
  claim without command output proving it, and work never on `main`.

This file plus the backlog are the whole process surface.

## The one thing that will bite you

**`docs/` is the GitHub Pages web root**, not a documentation folder. Pages
serves `main` + `/docs`. Anything written there is published at
`alexistosteson.github.io/culture-vulture/…`. Process docs, specs, plans and
notes must not go in `docs/`.

## What the project is

A weekly Bay Area arts digest: one HTML file, one JSON file, no framework, no
backend, no build step beyond copying a file. `docs/index.html` fetches
`events.json` beside it and renders.

```
config/brief.yml     editorial + geographic config — the source of truth for WHERE
prompts/             the research prompt an LLM runs against brief.yml
data/YYYY-MM-DD.json one file per week — the events and their window
scripts/validate.py  schema + vocabulary + window checks (runs in CI)
scripts/build.py     projects brief.yml over the data file -> docs/events.json
docs/                THE PUBLISHED SITE — index.html + events.json only
handoff/             design port package (not published; root-level, not docs/)
```

Weekly run:

```bash
python3 scripts/validate.py     # expect: 0 errors, 0 warnings (exit 0)
python3 scripts/build.py        # publishes newest data/ file to docs/
```

`validate.py` checks **every** file in `data/`, so the file and event counts it
prints grow each week and are not an expectation to match — `0 errors, 0
warnings` is. Don't pin a count here; the previous version of this line said 67
and was two weeks stale.

CI runs everything unattended on every push: `validate.py`, a
`brief.yml`/`sources.yml` parse check, a check that `docs/events.json` is
current, and — since 2026-08-17 — both halves of the tooling floor, a
`select`-coverage assertion over `ruff.toml` followed by `ruff check .`. The
push path filter includes `ruff.toml` and `.github/workflows/**`, so narrowing
the floor or editing the gate cannot slip through unwatched.

## Conventions that are load-bearing

- **`config/brief.yml` drives the site's geography.** Origin, region names,
  order and colours are copied into `docs/events.json` by `build.py` on every
  build. `index.html` contains no Bay Area geography — repointing the site at
  another city is a config edit plus a rebuild. Do not hardcode geography into
  the page; it is the project's whole premise.
- **`docs/events.json` is derived.** Editing it directly is overwritten by the
  next build. Region changes belong in `brief.yml`.
- **Light theme only, and no `prefers-color-scheme` block.** Per the global
  rule in `~/.claude/CLAUDE.md`.
- **Region colour must not be the only encoding, and must keep its lightness
  ramp.** The palette is viridis, ordered light-to-dark by distance from origin,
  so it survives red-green colour blindness; the rationale and the measurements
  are in `handoff/claude-design/color-schemes.md` and in the comment above
  `regions:` in `brief.yml`. Re-colouring is fine — flattening the ramp is not.
- **Region inks and label colours are derived at runtime** from whatever hex the
  config supplies, so a fork with arbitrary colours still gets readable text.

## Tooling floor

Run it locally before any merge, and any time `ruff.toml` is edited. CI enforces
the same floor, but by an assertion that duplicates the required rule families —
this script is the authority, so if you add a family here, mirror it into
`.github/workflows/validate.yml`:

```bash
python3 ~/.claude/bin/tool-floor.py
```

Exit `0` met · `1` findings · **`2` not enforceable** — tool missing, config
missing, or a required rule family removed. Treat exit 2 as a hard failure, not
a skip: it means nothing is checking. Never resolve it by narrowing `ruff.toml`.

## Testing

There is no test suite. Verification is `scripts/validate.py`, the tooling floor
above, plus looking at the page. To view it locally — `index.html` fetches `events.json`, so `file://`
does not work:

```bash
cd docs && python3 -m http.server
```

Serve on a fresh port when re-checking a change; `events.json` caches hard
enough to show you the previous build. The published page fetches
`events.json?v=<timestamp>` so a warm browser cannot serve stale data, but
`index.html` itself still sits behind the Pages CDN — **hard-reload after a
deploy**, or you will diagnose a build that actually worked.

**Screenshots of the page at a named viewport need care.** Headless Chrome does
not honour the mobile layout viewport — `--window-size=390,1500` yields a PNG
that is exactly 390px wide but laid out at desktop width and cropped, and the
file's dimensions look right, so nothing catches it but opening the image. Load
the page in a fixed-width `<iframe>` and screenshot the wrapper.
