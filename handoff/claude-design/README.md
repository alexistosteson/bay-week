# bay-week — design port package

A self-contained brief for redesigning **Bay Area Week**, a weekly Bay Area
arts-and-culture digest. Everything here is current as of commit `a1e7b0f`
(2026-08-15). Live site: https://alexistosteson.github.io/bay-week/

Read this file first. It says what the thing is, what constraints are real,
and where the other files are.

---

## 1. What it is

One page. It lists every worthwhile cultural event in the Bay Area for a
seven-day window, ordered by how far it is from home (Mountain View). There is
no backend, no build step beyond copying a JSON file, no framework, and no
external runtime dependency. `docs/index.html` is 430 lines: markup, one
`<style>` block, one `<script>` block. It fetches `events.json` next to it and
renders.

The editorial premise matters for design decisions: this is a digest for a
person deciding what to do this week, not a search tool. Scanning beats
filtering. The default view is grouped by region, nearest first, because the
question is usually "what's near me" and only sometimes "what's on Friday".

**Current data volume:** 67 events across 4 days and 5 regions. A busy week is
~100. Design for 100 rows in one scroll, not for pagination.

## 2. Files in this package

```
README.md               this file
color-schemes.md        all three palettes, measured, with rationale
content-pipeline.md     where events.json comes from
assets/
  desktop-geo-date.png  1280px, default view (grouped by region)
  desktop-date-geo.png  1280px, alternate view (grouped by day)
  tablet-geo-date.png    800px
  mobile-geo-date.png    390px, default view
  mobile-date-geo.png    390px, alternate view
source/
  index.html            the entire front end, verbatim
  brief.yml             the config that drives the site's geography
  events.schema.json    the contract every data file must satisfy
content/
  events.json           the live content file, exactly as the page fetches it
```

## 3. Layout: three tiers, not a fluid grid

Breakpoints are deliberate and the tiers differ in *what is shown*, not just
how it wraps.

| tier | width | controls | notes |
|---|---|---|---|
| phone | < 620px | sort toggle only | search and facet chips hidden; meta line goes telegraphic (`Thu 13 / PayPal Pk / San Jose`); tags capped at 3 |
| tablet | 620–1023px | toggle + search + collapsible filters | filter panel behind a **Filters** button |
| desktop | ≥ 1024px | persistent left sidebar | filters always visible, content column beside them |

Below 1024px the controls bar is sticky at the top of the viewport, and group
headers pin beneath it. Above 1024px the controls are static in the sidebar and
the sidebar itself is sticky.

**Not shown in the screenshots:** the sticky group header. On phone and tablet,
scrolling into a region pins that region's name (`PENINSULA`) directly below the
controls bar, underlined in the region's colour, until the next region takes
over. This is load-bearing — see §5.

## 4. The two views

A single toggle switches the grouping axis, and it changes what each row needs
to say:

- **Geo → Date** (default): groups are regions. Each row shows its date, because
  the region is implied by the group. There is *no* region label on the row —
  region is carried by the coloured left tick and the group header.
- **Date → Geo**: groups are days. Each row gains a region tag chip
  (`SAN FRANCISCO`) because the region is no longer implied.

State lives in the URL hash (`#axis=date&geo=sf&cost=free`), so any view is
linkable. Preserve that if you restructure.

## 5. Constraints that are not negotiable

These were arrived at by measurement, not preference. Changing them is fine;
changing them *unknowingly* would regress real accessibility.

1. **Light only.** No dark theme, and no `prefers-color-scheme` block — a page
   whose only theme switch is the OS setting renders dark on a dark-set OS,
   which is the thing being ruled out. `<meta name="color-scheme" content="light">`
   is set explicitly.
2. **Region must not be encoded by hue alone.** The five region colours ramp
   light→dark with distance, so the encoding survives red-green colour
   blindness. Full measurements in `color-schemes.md`. If you re-colour, keep
   the lightness ramp.
3. **Region must be readable as text somewhere on screen at all times.** On
   phone this is what the sticky header buys. Colour alone failed here — a 3px
   tick is not a legible colour target at arm's length.
4. **4.5:1 minimum** for all text, including the region-coloured text and the
   labels sitting on region fills. Everything currently passes; the weakest is
   4.57 (`--dim` on the page ground).
5. **No external runtime requests.** Fonts are the sole exception (Google Fonts:
   Barlow Condensed, Inter, JetBrains Mono). If you add anything, it must still
   work as one file plus one JSON.

## 6. Typography

- **Display** — Barlow Condensed 400/500/600/700. Masthead, group titles,
  buttons, rail labels. Uppercase, tight.
- **Body** — Inter 400/500/600. Event titles, notes, standfirst.
- **Mono** — JetBrains Mono 400/700. Metadata, tags, counts, eyebrow. Carries
  most of the "listing" texture; the meta line and every tag is mono.

Base 15px / 1.5, dropping to 14.5px on phone.

## 7. Known issues, not yet fixed

- **Duplicate `outdoor` tag.** A row whose `type` array contains `outdoor` and
  which also has `outdoor: true` renders the chip twice (visible in the desktop
  screenshots). Rendering bug in the tag list, not a data problem.
- **`events.json` caches aggressively.** A stale copy can survive a rebuild in
  a warm browser. Worth a cache-busting query param if you touch the fetch.
- The region `color` in the data is trusted as a hex string; a malformed value
  silently falls back to the CSS variable for that region id.

## 8. Where the real coupling is

If you rebuild the front end, these are the seams that matter:

- The page is **driven by `config/brief.yml`**, not by hardcoded values. Origin,
  region names, region order and region colours all arrive inside
  `events.json`. `index.html` contains no Bay Area geography — a fork pointed at
  Portland works without touching it. Preserve this; it is the project's whole
  premise (see `content-pipeline.md`).
- **Region inks are derived at runtime.** The page takes each region's fill
  colour and darkens it until it clears 4.5:1 on the page ground, so an
  arbitrary hex from a forked config still yields readable region-coloured text.
  Same for label colour on a fill: dark or white, whichever reads.
- `--controls-h` is measured from the live controls bar and written to the root
  element, because opening the Filters panel changes its height and the sticky
  group header offsets from it.
