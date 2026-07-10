# Designed plots — pick the chart per argument, don't default to bars

A weak data deck reaches for the same bar chart (or a number table) every slide. A strong one
**chooses the chart TYPE that fits each argument**, themes it to the deck, **highlights the one
thing that matters**, and pairs it with a one-line "so-what". This file is the repertoire + the
rules. (For raw data with an *obvious* single comparison, a plain bar/line is still right — this
is for when the relationship is richer.)

## Pick by argument
| The point you're making | Chart | Helper (`scripts/designed_charts.py`) |
|---|---|---|
| Part-to-whole + one headline number | **donut + centre KPI** | `donut_kpi(...)` |
| Before→after / a gap per category | **dumbbell** | `dumbbell(rows, ...)` |
| Rank/level change between **two** dates | **slope / bump** | `slope(series, ...)` |
| Two trends on different scales (A↑ while B↓) | **dual-axis line** | `dual_axis(x, left, right, ...)` |
| x vs y with a 3rd (size) dimension + fair value | **bubble + trend line** | `bubble_trend(points, ...)` (raster) · **`deckkit.native_bubble`** (editable-native — prefer it for a non-Latin deck or when the user will edit) |
| The "vital few" that drive a total | **Pareto** (bars + cumulative %) | `pareto(items, ...)` |
| Current state in numbers (3-6 metrics) | **KPI scorecards** (native) | `deckkit.scorecard(...)` ×N |
| Ranked / part list keyed to a chart | **leaderboard** (native) | `deckkit.leaderboard(rows)` |
| One hub, many dependents | **hub-and-spoke** | native (`box`+connectors); radial layout |
| **How a total builds start→end / a variance walk** | **waterfall / bridge** | `waterfall(out, items, ...)` — floating rise/fall/total bars + connector steps; the one **semantic up/down colour** exception (not the single-highlight rule) |
| **A multivariate profile across 3+ axes** (compare shapes) | **radar / spider** | *no helper — hand-roll* matplotlib polar (≤3 overlaid polygons, transparent PNG in house style; PowerPoint's native radar is unthemeable) |
| A simple single comparison / one trend | **bar / line** | `matplotlib` (the existing path) |

The recipes render a themed PNG → place with `deckkit.picture(out, ..., fit="contain")`.

**Recipe patterns (no dedicated helper — compose in matplotlib / deckkit):**
- **Small multiples / trellis** — the same metric across many comparable slices (regions, products, cohorts): a `rows`/`columns` grid of identical mini charts with **shared x/y scales** (so shapes compare) + **one highlighted** slice, the rest greyed. Better than one spaghetti chart of N series.
- **Sparkline** — a tiny axis-less word-scale trend inside a KPI tile / table cell / sentence: a matplotlib line with axes/ticks/frame off, saved small and placed inline via `picture`, or a native mini `native_chart` stripped of chrome. Pairs with `big_numeral`/`stat_row` to show "the number AND its trend".
- **Chart annotation layer** — data-anchored overlays ON a designed chart: a **CAGR growth arrow** across columns, a **delta bracket** between two bars, a **reference/target line** (`ax.axhline`), a **convergence/target band** (`ax.axhspan`), or a labeled callout on the key point. The annotation carries the "so-what" *inside* the plot; keep it to the ONE thing that matters.
- **Football field / range bars** — a value RANGE per category (valuation, estimate, min–max) as floating horizontal bars on a shared `deckkit.axis_scale`, one row per category — a `dot_strip` cousin for ranges instead of points.

## Chart anti-patterns (each one has shipped an ugly or misleading chart — check by name)
- **Dual-axis abuse** — two unrelated series forced onto twin axes to fake correlation; use it only
  for one genuinely paired ↑/↓ story, and colour-key each axis to its series.
- **Too many series** — >4 lines/bars per chart turns evidence into spaghetti; split, or grey all
  but the ONE series the takeaway is about (single-highlight rule).
- **Composition without meaning** — a donut/stacked bar for parts that don't sum to a meaningful
  whole; if the audience won't ask "share of what?", use a bar.
- **Cropped-axis drama** — a bar chart whose y-axis starts above 0 inflates a small delta; bars
  start at 0 (lines may zoom, but then say so on the axis). This bites hardest on **clustered-high
  data** (scores 85/88/92, revenue 210/220/230): the renderer *auto-crops* the axis to ~200 and a
  bar reading ~3× taller is only 1.09× larger. `deckkit.native_chart`/`native_pareto` now force a
  zero baseline for column/bar with non-negative data (`zero_base=True` default) — don't pass
  `zero_base=False` unless a zoomed magnitude axis is deliberate *and* labelled; a **matplotlib /
  hand-rolled** bar chart has no such guard, so set `ax.set_ylim(bottom=0)` yourself.
- **Inflating floor on a proportional encoding** — a min-visible-size clamp that lifts small values
  to a fixed floor so a `10`-out-of-`200` tier is DRAWN at 20% width while its label reads 5%: the
  geometry now contradicts its own number, and the floor fires exactly where a funnel's story lives
  (the deep drop-off). A proportional encoding (funnel/pyramid band width, bubble area, bar length)
  must track `value/max` with at most a *hairline* floor; when a band gets too thin to hold its
  label, route the label OUT to a side leader — never widen the band. `deckkit.tier_stack` does this
  now; a hand-rolled proportional shape must too.
- **Off-zero neutral on a signed scale** — a diverging blue↔red (or +/−) encoding whose neutral is
  anchored at the DATA midpoint, not the value 0, so a true `0` renders blue ("negative") and
  all-positive deltas straddle neutral — the sign reading is simply wrong. Anchor neutral at the
  semantic zero. `deckkit.heat_matrix(scale='div')` zero-centres by default (pass explicit
  `vmin`/`vmax` only to fix a deliberate asymmetric range); a matplotlib diverging map needs
  `TwoSlopeNorm(vcenter=0)` (or a symmetric `vmin=-M, vmax=+M`).
- **Axis that misses a bar** — a baseline / value axis drawn to a hand-picked width that stops short of
  the last bar reads as a rendering bug; derive its extent from the data (`last_bar_x_end − axis_x`).
- **Waterfall that double-counts** — showing increments AND their sum as peer bars ("+8 / +8.3 / +16.3"
  where 16.3 = 8+8.3), or stacking two *different* quantity kinds into one total (take-home extras +
  employer pension = a "135%" bar). Show increments *or* the running total, use `designed_charts.waterfall`
  (correct running-total + connectors), and keep distinct quantities in separate stacks / a side note.
- **Hand-rolled where a component exists** — building `waterfall`/`gantt`/`dumbbell_board`/a chart from
  raw boxes re-introduces the geometry & grammar bugs the component already fixed; reach for the
  component, hand-roll only a form the library genuinely lacks.
- **Chart with no takeaway** — a plot dropped on the slide with no assertion title / takeaway rail
  is data, not an argument; every chart answers a named question.
- **Rainbow categorical palette** — hues with no semantic binding read as decoration; bind each hue
  (semantic-color-contract.md) or stay monochrome + one accent.

## The four rules every designed plot follows
1. **Single highlight (one-accent discipline).** Recolor only the ONE series/wedge/row/bar that
   carries the point in the accent; drop everything else to a neutral grey. The recipes take a
   `highlight` index and do this; for a multi-series categorical chart where every series matters,
   skip the highlight. Never let a chart use >2 saturated hues unless it's genuinely categorical.
   (On a **single-series** native bar/column chart, `highlight` selects a whole series and so can't
   pick one bar — use `native_chart(..., emphasize=<category index>)` to foreground ONE bar.)
2. **Theme it to the deck.** Pass the deck's palette (`palette=ACCENTS`, or pull from a generated
   template with `palette_from_image`) and `dark=True` for a dark deck, so the chart looks built-in,
   not pasted. Charts render on a transparent background, so they sit on any slide fill. **On a CJK
   (Chinese/Japanese/Korean) deck, pass `font="<your deckkit.EAFONT>"`** so chart labels render real
   glyphs, not tofu (matplotlib uses its first resolvable font for *all* text, so the CJK face must
   lead — the recipes handle this when you pass `font`). If no CJK font is installed, keep chart text
   Latin/numeric and label the categories with `deckkit.text()` around the chart (the `equation_png`
   fallback). This applies to **any-language** deck, not just English.
3. **Carry a "so-what".** Split the slide ~**65% chart / ~35% narrative rail** and add a
   `deckkit.takeaway_rail(label, hero_stat, body)` — a small caps label, the one restated number,
   and a 2-3 line interpretation. A chart without a stated conclusion makes the audience guess.
4. **Label directly, don't rely on colour alone.** End-of-line value labels, a legend keyed by
   the SAME colours as a paired `leaderboard`, markers as well as hue — so it survives a projector
   and colour-blind viewers (the deck-wide accessibility rule).
5. **It must LOOK right — render it and check.** Applies to **every plot you generate with code**
   (matplotlib, a designed_charts recipe, any domain plot), not one chart type. Two recurring failures:
   **(a) undersampled curves** — a continuous/high-frequency function plotted at coarse or integer `x`
   *aliases* into jagged zigzags (the "sine looks weird" bug); sample with a dense `np.linspace` (a few
   hundred points, ≥~10× the highest frequency) so smooth functions look smooth — plot the curve on a
   fine grid even if the *data/markers* sit on integers. **(b) A legend (or annotation) sitting ON the
   data** — when the plot is full, put the legend **outside the axes** or in the truly empty corner;
   `loc='best'` is not enough on a busy plot. The general pattern:
   ```python
   xs = np.linspace(x0, x1, 600)            # dense grid — NOT np.arange(0, 50) for a smooth curve
   for k in series: ax.plot(xs, f(xs, k), label=...)
   ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False)  # legend OUTSIDE the axes
   fig.savefig(out, bbox_inches="tight")    # so the outside legend isn't clipped
   ```
   For a **dual-axis / twin-axis** plot, never draw two separate `legend()`s (they collide with each
   other and the twin-axis ticks) — collect both handle lists and draw **one combined legend above** the
   axes: `lns = l1 + l2; ax.legend(lns, [h.get_label() for h in lns], loc="lower center",
   bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False)`. Overlap can't always be perfectly avoided on a
   dense plot — when there's no empty region, going **outside** (right or above) is the answer; never ship
   a legend sitting on the data. (In a very small plot cell an outside legend can shrink the axes too far —
   then omit the in-figure legend and label the series in the native slide caption instead.)
   Always **view the rendered PNG** and fix aliasing / an occluding legend / clipped labels before
   placing it — a wrong-*looking* plot misleads even when the numbers are right.

## Editable native charts vs matplotlib rasters — pick by need
Three ways to put a chart on a slide; choose by what the deck needs:
- **Editable native PowerPoint chart — `deckkit.native_chart` / `deckkit.native_dual_axis`.** A *real*
  chart object: the user can **click to edit data/labels** in PowerPoint, and **any non-Latin labels —
  CJK (中文/日本語/한국어), Cyrillic, Greek, … — render via PowerPoint's own fonts, no tofu** (matplotlib
  often can't find the script's font for a rotated axis title and renders □). **Prefer this whenever
  (a) the deck is in ANY non-Latin language, or (b) the user wants to edit the chart.** Pass `font=`
  your deck's text font for the script (your `EAFONT` for CJK; a Cyrillic/Greek deck's `FONT` already
  covers those). **Covers nearly the whole roster:** `native_chart` (`line`/`line_markers`/`column`/
  `bar`, and **slope** = a 2-point line), `native_dual_axis` (two-scale 'A↑ vs B↓', e.g. 占比% vs
  成本指数), `native_donut` (part-to-whole + a KPI in the hole), `native_pareto` (columns + cumulative-%
  line on a secondary axis), `native_bubble` (x·y·size). Themed (`palette`, `dark`, `font`,
  `highlight`). **Data from a spreadsheet?** `deckkit.series_from_csv(path, x_col, y_cols)` → `(categories,
  series)` feeds `native_chart`/`native_dual_axis` directly (stdlib csv — no pandas; auto-sniffs the
  delimiter; strips thousands-commas / `%` / a currency symbol; non-numeric → 0). *(RTL scripts —
  Arabic/Hebrew — remain a known layout limitation, see `multilingual.md`.)*
- **`designed_charts` (matplotlib raster).** Use only when (a) you specifically want the matplotlib
  styling, or (b) for the **dumbbell** (before→after gap), which has no native chart type — otherwise
  prefer the native editable equivalents above. A transparent PNG; **not editable**, and on a
  non-Latin deck you must pass `font="<the script's font>"` — still raster.
- **Freeform native (`deckkit` shapes)** for diagram-like "charts" (hub-and-spoke, a flow/Sankey, an
  annotated timeline) that are really layout — and for an editable **dumbbell** (rows of dot——dot).
  Keep them measure-then-place inside a `content_band`.

Rule of thumb: **default to the native editable charts** (`native_chart` / `native_dual_axis` /
`native_donut` / `native_pareto` / `native_bubble` — pass the script's `font=`); reach for
`designed_charts` (raster) only for dumbbell or a deliberate matplotlib look; a diagram → freeform.
- Either way: **whole chart, legible at the deck's read distance, one message, one highlight, a
  takeaway.** ("From the back of the room" is the floor for a *presented* deck; for a **read-alone /
  reference** chart, size to arm's-length reading and it's fine to keep more series labelled — there's
  no narrator to point at the rest. Direct labels + colour-blind safety are universal regardless.)

## Native data furniture (deckkit)
- `scorecard(slide, x,y,w,h, label, value, delta=, caption=, good_up=, glass_tint=)` — a KPI tile
  (big value + auto-coloured ▲/▼ delta). Lay out 3-6 with `columns()`/a 2×2 grid; pass
  `glass_tint=` on a dark deck to make them glass.
- `leaderboard(slide, x,y,w, rows=[(color,name,value[,sub])])` — ranked rows with a colour swatch
  that **keys back to a paired chart** (use the chart's colour list so legend ↔ chart stay in sync).
- `takeaway_rail(slide, x,y,w, label, hero, body)` — the narrative rail beside a chart.

## Example
```python
import designed_charts as dc, deckkit as dk
band = dk.content_band(s)                       # the safe region
dc.dumbbell("assets/gap.png", rows, palette=ACCENTS, highlight=1, a_label="2024", b_label="2026")
dk.picture(s, "assets/gap.png", band[0], band[1], band[2]*0.62, band[3], fit="contain")
dk.takeaway_rail(s, band[0]+band[2]*0.66, band[1]+0.3, band[2]*0.34,
                 "Key shift", "+5 dB", "Model B closes most of the gap by 2026 — the one to back.")
```

## When NOT to use this
Short status updates, qualitative talks, or a slide with a single obvious number (use a hero stat /
`scorecard`, not a chart). Reserve the richer roster for data/report/market/strategy decks that have
many distinct quantitative relationships to show.
