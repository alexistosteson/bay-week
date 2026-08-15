# Content pipeline — where `events.json` comes from

The page fetches exactly one file. This is how that file is produced, and why
the config is the interesting part.

```
config/brief.yml            editorial + geographic config, hand-written
        │
        ├──────────────► prompts/weekly-research.md
        │                 an LLM reads both, researches the week
        │                          │
        │                          ▼
        │                data/YYYY-MM-DD.json      one file per week, committed
        │                          │
        │                scripts/validate.py       schema + vocabulary + window
        │                          │
        └──────────────► scripts/build.py          projects brief.yml over it
                                   │
                                   ▼
                          docs/events.json         what the page fetches
```

Run weekly:

```bash
python3 scripts/validate.py     # 67 events, 0 errors, 0 warnings
python3 scripts/build.py        # publishes newest data/ file to docs/
```

## The division of labour

**`config/brief.yml` owns WHERE and WHAT-COUNTS.** Origin, the five regions and
their order, colours, editorial priorities, exclusions, voice. It is prose and
lists, written to be argued with in a pull request — the `why:` fields are
addressed to a human reader and an LLM equally.

**`data/YYYY-MM-DD.json` owns WHAT HAPPENED.** The events themselves and the
window they cover. Nothing else.

**`scripts/build.py` merges them.** On every build it copies `origin` and
`regions` (id, label, rank, blurb, color) from the YAML onto the data file's
`meta`, and substitutes `{origin}` in the standfirst. So the geography the site
displays always comes from the config, never from whatever the LLM happened to
write into the data file.

This is why `index.html` contains no Bay Area geography. Repointing the whole
site at Portland is a `brief.yml` edit plus a rebuild — verified by test.

`pyyaml` is optional. Without it the config cannot be read and the data file
publishes unchanged, with a printed warning.

## Shape of the content file

```jsonc
{
  "meta": {
    "window_start": "2026-08-13", "window_end": "2026-08-16",
    "compiled": "2026-08-12",
    "origin": { "label": "Mountain View", "lat": 37.3861, "lng": -122.0839 },
    "standfirst": "Arts, music, and worthwhile oddities, ordered by remove from Mountain View.",
    "geos": [ { "id": "south-bay", "label": "South Bay", "rank": 1,
                "blurb": "San Jose, Saratoga, Sunnyvale, Mountain View",
                "color": "#FDE725" } ],
    "vocab": { "type": [...], "venue_type": [...], "cost": [...] }
  },
  "events": [
    {
      "id": "0813-paypal-sob",
      "date": "2026-08-13",
      "start": "18:00",                      // optional
      "title": "SOB x RBE, Plo, 310babii, Mistah F.A.B.",
      "venue": "Habbas Law Epicenter at PayPal Park",
      "city": "San Jose",
      "geo": "south-bay",                    // must match a meta.geos id
      "type": ["concert"],                   // must be in meta.vocab.type
      "venue_type": "amphitheater",
      "genre": ["hip-hop"],
      "cost": "ticketed",                    // free | free-ticketed | ticketed
      "outdoor": true,
      "featured": false,                     // renders a ◆ before the title
      "note": "Bay Area hip-hop — Vallejo's SOB x RBE headline a regional showcase."
    }
  ]
}
```

Full contract in `source/events.schema.json`. Design-relevant properties:

- **`note` is the editorial payload** and varies from one line to three. It is
  the reason a row is worth reading; do not design a layout that truncates it.
- **`title` runs long** — lineup listings like the example above are common and
  wrap to two lines even on desktop.
- **`venue` runs long too**, and the page shortens it for phone via a lookup
  table plus a noise-word stripper (`Habbas Law Epicenter at PayPal Park` →
  `PayPal Pk`). If you redesign the mobile meta line, that machinery is in
  `shortVenue` / `shortCity`.
- **`start` is often absent.** Roughly half the rows have no time.
- **`featured`** is rare — a handful per week, capped at 8 by config.
- `type` is an array and `venue_type` a single value; a row therefore has a
  variable number of tag chips, currently 3–5.

## Validation

`scripts/validate.py` checks more than the schema: vocabulary drift (a `type`
not declared in `meta.vocab`), regions that do not exist in `brief.yml`,
duplicate ids, and events falling outside the stated window. It exits non-zero
on error and runs in CI on every push (`.github/workflows/validate.yml`).

Warnings are not failures — notably, a data file whose regions disagree with
`brief.yml` warns rather than errors, because `build.py` will overwrite them
anyway.
