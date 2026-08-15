# Culture Vulture

A weekly digest of arts, music, and worthwhile oddities across the Bay Area,
ordered by remove from Mountain View.

**Live site:** `https://<your-username>.github.io/bay-week/`

---

## What this is

A weekly research run produces a structured dataset. A static page renders it,
sortable by geography or by date and filterable by event type, venue type, and
cost. The research itself is driven by a config file, not by a prompt buried in
someone's chat history — which means the taste is versioned, reviewable, and
forkable.

The interesting file is [`config/brief.yml`](config/brief.yml). It defines what
counts as worth listing. Everything else is plumbing.

---

## Repository layout

```
config/
  brief.yml            what to look for — regions, interests, exclusions, voice
  sources.yml          where to look — venue calendars, aggregators, feeds
prompts/
  weekly-research.md   the instruction that reads the configs
schema/
  events.schema.json   JSON Schema for the data
data/
  YYYY-MM-DD.json      one file per week, named for the window start
digests/
  YYYY-MM-DD.md        the human-readable digest for that week
docs/                  GitHub Pages root
  index.html           the site
  events.json          the week currently published
scripts/
  validate.py          schema + vocabulary + brief consistency checks
  build.py             publish a week to docs/
```

---

## Weekly run

1. Open a new Claude session. Attach `prompts/weekly-research.md`,
   `config/brief.yml`, and `config/sources.yml`.
2. Claude researches and writes `data/YYYY-MM-DD.json` and
   `digests/YYYY-MM-DD.md`.
3. Publish and check:

   ```bash
   python3 scripts/build.py          # copies newest week into docs/
   python3 scripts/validate.py       # 0 errors required
   git add -A && git commit -m "Week of YYYY-MM-DD" && git push
   ```

Pages redeploys on push. Git history gives you a versioned archive of every
week for free.

---

## Setup

1. Fork or clone.
2. Settings → Pages → Source: **Deploy from a branch**, branch `main`, folder
   `/docs`.
3. Wait about a minute. Site is at
   `https://<your-username>.github.io/<repo>/`.

Validation needs Python 3.9+. `pyyaml` is optional — without it, `validate.py`
skips the brief cross-checks and still runs the schema and vocabulary checks.

```bash
pip install pyyaml        # optional
```

---

## Making it yours

Everything that encodes taste or place lives in `config/brief.yml`:

| Change | Edit |
|---|---|
| Where you live | `origin` |
| Which areas, and their order | `regions` — `rank: 1` is home |
| What kinds of events | `interests.priorities` |
| Which music you want surfaced | `interests.music.emphasis` |
| What to never list | `exclusions.hard` |
| What to list but rank low | `exclusions.soft` |
| Everything vs. a curated cap | `coverage.mode` |
| How it should read | `voice` |

Swap `config/sources.yml` wholesale for a different metro. The tier structure
transfers; only the venue names change.

The colors in `regions[].color` drive the site's region coding — the rail
across the top, the tick on every row. Change them there, not in the CSS.

---

## Contributing

**Taste changes are PRs against `config/brief.yml`.** That's the point of the
file. If you think the digest over-indexes on club shows and under-covers dance,
change the `priorities` order and argue for it in the PR description. The `why`
fields are prose precisely so they can be argued with.

**Adding a venue** is a one-line addition to `sources.yml` under the right tier
and region.

**Adding a vocabulary term** means editing both `meta.vocab` in the data files
and the schema. Prefer reusing an existing term — the vocabularies are closed on
purpose, because open tag sets fragment into near-duplicates within a month.

CI runs `validate.py` on every push and PR, and checks that `docs/` isn't stale.

---

## Design notes

Region color coding is informational, not decorative: a warm gold at home
cooling through green and blue to rose across the bay. The rail under the
masthead is legend and filter at once.

Three responsive tiers:

- **Phone** (`<620px`) — sort toggle only; metadata goes telegraphic
  (`Fri 14/PURE/Sunnyv.`)
- **Tablet** (`620–1023px`) — toggle, search, and filters behind a disclosure
- **Desktop** (`≥1024px`) — persistent sidebar, content column beside it

Filter state lives in the URL hash, so any view is a shareable link:
`#geo=south-bay,peninsula&cost=free`

No build step, no dependencies, no framework. One HTML file and one JSON file.

The page fetches `events.json` at runtime, so opening `index.html` directly
from disk won't work. To preview locally:

```bash
cd docs && python3 -m http.server
```

---

## Caveats

Genre descriptions are editorial shorthand, not official billing. Where a
lineup was unannounced, the note describes the room's typical booking and says
so. Lineups shift and shows move — verify with the venue before travelling.
