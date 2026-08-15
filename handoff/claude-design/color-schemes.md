# Colour schemes

Three states exist. The site shipped as **A**, was converted to **B**, then
re-coloured to **C**, which is current. B is included because it is the honest
"light version of the original palette" — it kept the original hues and only
changed the ground. C changed the hues for a specific, measured reason.

---

## A — original dark (historical, commit `22612aa`)

Not in use. Included only so the original hue intent is legible.

```
--ink     #0E1216   page ground        --text   #F4F8FB
--surface #171D24   insets             --muted  #AEBDC9
--raised  #212A33   pressed states     --dim    #7A8B99
--line    #2C3742   borders
```

Regions: `#F2B138` amber · `#6BCB9B` green · `#5AA9E6` blue · `#E0719E` pink ·
`#9B8AC4` purple. Bright saturated hues on a near-black ground, dark text
sitting on each fill.

---

## B — light, original hues (commit `d76b62a`)

The straight light conversion. Same five hues, re-derived ground.

```
--ink       #FAF9F7   page ground (warm paper)
--surface   #F1EEE9   insets
--raised    #E6E1D9   pressed chips
--line      #D9D3C9   borders
--hairline  #EAE6DF   row dividers
--text      #16191C   16.77:1
--text-soft #2F363D   11.63:1   event notes
--muted     #4E565E    7.09:1   meta, standfirst
--dim       #6B737C    4.57:1   labels, tags
--on-accent #1A1408   dark text on a region fill
```

Two things the inversion could not carry over, and how they were solved:

- Rail labels were `var(--ink)` — dark text on a bright fill. Flipping `--ink`
  to a light ground would have made them white-on-yellow. A dedicated
  `--on-accent` token holds the dark, in any theme.
- The region hues are tuned for a dark ground. As *text* on white, amber landed
  at ~1.9:1. So each region gained a second token: a **fill** for backgrounds
  and a darkened **ink** for text and borders.

| region | fill | ink | ink on page |
|---|---|---|---|
| south-bay | `#F2B138` | `#8A5A00` | 5.63 |
| peninsula | `#6BCB9B` | `#0F6B47` | 6.21 |
| sf | `#5AA9E6` | `#1063A6` | 5.94 |
| east-bay | `#E0719E` | `#A32C63` | 6.44 |
| outer | `#9B8AC4` | `#5B4A93` | 7.01 |

**Why this was not the end state:** every one of these five hues sits at
roughly the same lightness. That is fine for normal colour vision and fails for
red-green colour blindness, which flattens hue and leaves lightness as the only
remaining cue.

---

## C — current, viridis ramp (commit `a1e7b0f`)

The ground, text and structural tokens are **identical to B**. Only the five
region colours changed, plus the label-on-fill rule.

| rank | region | fill | ink (derived) | label on fill |
|---|---|---|---|---|
| 1 | south-bay | `#FDE725` | `#796E12` | dark |
| 2 | peninsula | `#5EC962` | `#37773A` | dark |
| 3 | sf | `#21918C` | `#1B7571` | dark |
| 4 | east-bay | `#3B528B` | `#3B528B` | white |
| 5 | outer | `#440154` | `#440154` | white |

### Rationale

Regions are ranked by remove from home. A palette that ramps light→dark with
that rank makes lightness *carry the meaning* rather than decorate it — which
is also exactly what survives when hue perception is reduced.

Measured by simulating each palette under protanopia, deuteranopia and
tritanopia (Viénot 1999 LMS projection), then taking the minimum CIE76 ΔE
across all ten region pairs. Lower = two regions look more alike.

| palette | normal | protan | deutan | tritan | worst |
|---|---|---|---|---|---|
| B (original hues) | 27.3 | 11.0 | **10.2** | 11.0 | 10.2 |
| Okabe-Ito | 26.4 | 23.2 | 16.6 | **10.9** | 10.9 |
| **C (viridis)** | 37.7 | 23.5 | 19.4 | 19.3 | **19.3** |
| cividis | 24.0 | 23.9 | 25.6 | 19.6 | 19.6 |

Reading the table:

- **B's failure is concrete, not theoretical.** Under deuteranopia — the most
  common profile, ~6% of men — peninsula and east-bay collapse to ΔE 10.2,
  which is "these are the same colour" territory. Two further pairs collapse
  under protanopia and tritanopia.
- **Okabe-Ito**, the usual accessible-qualitative default, fixes red-green
  handily but still collapses under tritanopia, and its dark blue `#0072B2`
  fails text contrast at 3.53:1 against the page. Rejected.
- **cividis** scores marginally best but its midtones go grey-olive
  (`#7C7B78`, `#BCAF6F`), which reads as *absence of colour* in a 6px tick.
  Rejected on legibility, not on numbers.
- **viridis** roughly doubles B's worst case, collapses nowhere, and improves
  normal-vision separation too (27.3 → 37.7).

The simulation script is not shipped here; it is straightforward to regenerate
(sRGB → linear → LMS, apply the dichromat projection plane, back to sRGB, then
CIE76 in CIELAB).

### Consequences to preserve

1. **The ramp spans light yellow to dark purple**, so no single label colour
   works on all five fills. The page picks dark or white per fill by contrast.
   Any redesign that puts text on a region fill needs the same rule.
2. **Region inks are derived, not authored.** The page darkens a fill until it
   clears 4.5:1 on the ground. This is what lets a forked config supply
   arbitrary hexes and still get readable region-coloured text.
3. **The free tag** (`#A9DCAC` border, peninsula ink) is tied to the green end
   of the ramp. If the ramp changes, it needs re-picking.

### If you want the original character back

The constraint to preserve is the **lightness ramp**, not the specific hues.
Warmer, more editorial colours that still ramp monotonically light→dark by rank
would satisfy every requirement here. Picking five pretty hues at similar
lightness is precisely what B did, and it is the thing that failed.
