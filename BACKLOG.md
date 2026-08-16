---
state: active
next: Nothing blocking. To publish a week: run the research prompt in `prompts/weekly-research.md` against `config/brief.yml`, save the result as `data/<monday>.json`, then in this repo run `python3 scripts/validate.py && python3 scripts/build.py` and commit — see [CLAUDE.md](CLAUDE.md) for the pipeline. Specs go in a root-level `specs/`, never `docs/` (the Pages web root); each declares its own tier per `delivery-tiers`.
tool: claude-code
updated: 2026-08-15
---

# Backlog — culture-vulture

Weekly Bay Area arts digest. One HTML file, one JSON file, no framework or
backend. Live at https://alexistosteson.github.io/culture-vulture/ · released
`v0.1.0` 2026-08-15.

**Deliberately light on process, not unfinished.** It arrived as a downloaded
tarball with its own git history rather than through `new-swe-project`, so it
has no CONSTITUTION and no ritual docs — and per `delivery-tiers` it does not
owe them, because tier is declared per spec and most work here is `probe`. The
one gate that never relaxes, the tooling floor, is established (`ruff.toml`,
2026-08-15). This file plus [CLAUDE.md](CLAUDE.md) are the whole process
surface.

## Index

- one-liner · Design port package is stale — chip already spawned 2026-08-15
- small · Full build-tier scaffold, only if a spec ever needs it — parked, see the row below for why it is not owed now
- one-liner · `docs/events.json` caches aggressively — no cache-busting on the fetch

---

| Item | Context | Do it when |
|---|---|---|
| Full build-tier scaffold — parked, not owed | **Resolved 2026-08-15 by reading `delivery-tiers` rather than scaffolding on reflex. Tier is declared per spec, not per project**, so this repo does not need a project-level tier and most work here will declare `probe` on its own — which owes no plan, no NASA audit, no tier registry and no merge ritual. That is most of what the template's `docs/` tree exists to hold, so the tree is not owed until a build-tier spec appears.<br><br>**The project-scope probe declaration was considered and does not apply.** `delivery-tiers` allows one project-wide probe declaration — the *probe run* — for a project whose entire output is a real-world state change and whose every line of code is deletable at the end. `build.py`, `validate.py` and `index.html` are the product and survive, and the skill is explicit that a tool expected to survive the project is a build spec, not part of a probe run. Declaring it anyway would be tier-laundering, and the honest framing is simply that no project-level tier is required.<br><br>**What still constrains the layout when a build spec does arrive:** GitHub Pages serves this repo from `main` + `/docs`, so anything the template writes to `docs/HANDOFF.md`, `docs/handoff/` or `docs/superpowers/{specs,plans}` is publicly served. Short-form probe specs therefore go in a **root-level `specs/`**, never `docs/`. The three options weighed for a full scaffold, if it is ever needed: relocate the process tree out of `docs/`; keep the template layout and exclude it via `docs/_config.yml` (Pages is on the legacy Jekyll build — `build_type: legacy`, confirmed via the API 2026-08-15 — so Jekyll would honour it, but it breaks if anyone adds `.nojekyll`); or move the site to a `gh-pages` branch and free `docs/`.<br><br>**Do not copy the template piecemeal in the meantime** — its `CLAUDE.md` references `CONSTITUTION.md`, `docs/HANDOFF.md`, `docs/handoff/*` and `docs/superpowers/specs/_SPEC-SECTIONS.md` throughout, so copying it without the tree yields a router whose every link is dead. | Only when a spec here is declared **build** tier. Nothing triggers it before that. The floor that *was* owed regardless of tier is done — `ruff.toml` written 2026-08-15, `F/ARG/B/RUF`, exit 0 against the existing scripts. `delivery-tiers`' own floor (spec, behavioural check, evidence rule, worktree isolation) still applies to every spec here whatever its tier. |
| Design port package is stale | `handoff/claude-design/` snapshots the site **before** the Culture Vulture rename and before the outdoor-chip fix — its `source/index.html` is two commits behind, its README cites commit `a1e7b0f`, and all five screenshots show the old masthead. A chip was spawned 2026-08-15 with the full instructions, including the headless-Chrome capture method (`--window-size` alone silently produces desktop-layout images at mobile pixel widths; the working method is a fixed-width iframe wrapper). | Before handing the package to anyone. Harmless while it sits unread. |
| `docs/events.json` caches aggressively | A stale copy survives a rebuild in a warm browser; hit twice during development 2026-08-15, once producing a page that rendered the previous palette while the file on disk was current. Not a site defect — a devloop trap and a plausible source of a false "the build didn't work" report. Candidate fix: cache-bust the fetch in `docs/index.html`. | Next time `index.html` is touched. |
