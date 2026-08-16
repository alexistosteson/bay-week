---
state: active
next: Decide where process docs live before scaffolding — `docs/` is the GitHub Pages web root, so the `new-swe-project` template's `docs/HANDOFF.md` + `docs/handoff/` + `docs/superpowers/` would be published to the public site. See the first row below.
tool: claude-code
updated: 2026-08-15
---

# Backlog — culture-vulture

Weekly Bay Area arts digest. One HTML file, one JSON file, no framework or
backend. Live at https://alexistosteson.github.io/culture-vulture/ · released
`v0.1.0` 2026-08-15.

**This project is only partially scaffolded.** It arrived as a downloaded
tarball with its own git history rather than through `new-swe-project`, so it
has no CONSTITUTION, no ritual docs and no tooling floor. The first row below
is the blocker on fixing that. Until it is resolved, treat this file plus
[CLAUDE.md](CLAUDE.md) as the whole of the project's process surface.

## Index

- small · **Resolve the `docs/`-is-web-root conflict, then finish scaffolding** — blocks CONSTITUTION, HANDOFF and the ritual docs
- one-liner · Design port package is stale — chip already spawned 2026-08-15
- one-liner · Establish the tooling floor (`tool-floor.py --init python`)
- one-liner · `docs/events.json` caches aggressively — no cache-busting on the fetch

---

| Item | Context | Do it when |
|---|---|---|
| Resolve the `docs/`-is-web-root conflict, then finish scaffolding | **`new-swe-project` refuses this repo** — its step 1 stops on a directory that already contains code, and the refusal is correct for a second reason it does not know about: **GitHub Pages serves this repo from `main` + `/docs`**, so every file the template would write to `docs/HANDOFF.md`, `docs/handoff/` and `docs/superpowers/{specs,plans}` becomes publicly served at `alexistosteson.github.io/culture-vulture/…`. Specs, plans, gotchas and shipped-state would all be published.<br><br>**Three ways out, none yet chosen (owner's call).** (a) Put the process tree somewhere other than `docs/` — cleanest, but every path in the template's CLAUDE.md and in `spec-item-check.py --items` has to be repointed, and it diverges from every other project here. (b) Keep the template layout and add `docs/_config.yml` with an `exclude:` list — Pages is on the legacy Jekyll build (`build_type: legacy`, confirmed via the API 2026-08-15), so Jekyll would honour it; fragile if anyone later adds `.nojekyll`. (c) Move the site to a `gh-pages` branch or the repo root and free `docs/` for its conventional use — biggest change, and it breaks the published URL if done carelessly.<br><br>**Do not copy the template piecemeal in the meantime.** The template's `CLAUDE.md` references `CONSTITUTION.md`, `docs/HANDOFF.md`, `docs/handoff/*` and `docs/superpowers/specs/_SPEC-SECTIONS.md` throughout; copying it without the tree it points at yields a router whose every link is dead. | Before any spec is written against this repo. Nothing here is urgent while the project is a personal weekly digest, but the first real feature is the wrong moment to discover the rituals were never loaded — that exact failure is on record in the harness backlog ("portfolio-scan should flag project dirs with content but no CLAUDE.md"), where this project is now the second recorded instance. |
| Design port package is stale | `handoff/claude-design/` snapshots the site **before** the Culture Vulture rename and before the outdoor-chip fix — its `source/index.html` is two commits behind, its README cites commit `a1e7b0f`, and all five screenshots show the old masthead. A chip was spawned 2026-08-15 with the full instructions, including the headless-Chrome capture method (`--window-size` alone silently produces desktop-layout images at mobile pixel widths; the working method is a fixed-width iframe wrapper). | Before handing the package to anyone. Harmless while it sits unread. |
| Establish the tooling floor | `new-swe-project` step 5 — `python3 ~/.claude/bin/tool-floor.py --init python`, then confirm it runs. Never done, because the scaffold never ran. The repo is Python (`scripts/build.py`, `scripts/validate.py`) plus one HTML file, so the floor is small but real: `validate.py` is the only thing standing between a malformed data file and the published site. | With the scaffolding row above, or independently — it does not depend on the `docs/` decision. |
| `docs/events.json` caches aggressively | A stale copy survives a rebuild in a warm browser; hit twice during development 2026-08-15, once producing a page that rendered the previous palette while the file on disk was current. Not a site defect — a devloop trap and a plausible source of a false "the build didn't work" report. Candidate fix: cache-bust the fetch in `docs/index.html`. | Next time `index.html` is touched. |
