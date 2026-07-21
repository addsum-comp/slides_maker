# Form selection — content shape → the candidate FORMS (generate a set, then pick)

The single content-indexed map for "what visual form should this slide take?" — used by the
**slide-design** agent (designs to it, Step 2), the **builder** (SKILL.md step 4), and the **critic** (judges form
fit) so all three resolve to one surface. Each row is a **candidate SET + a tie-breaker**, never a
single answer.

> **Design is choosing, not matching.** NEVER record the first matching form. For each content slide,
> generate the **2–3 forms the content could take**, then pick with the tie-breaker and record *why the
> winner beat the runner-up* (the planner's Form ledger). The reflex form — a rounded-card / panel grid
> — is the right answer for **parallel, unordered, equal-weight** items only; the moment the content has
> **order, magnitude, a relationship, time, or two axes**, a non-card form almost always says it better.

## Concept → visualization (the FIRST move — before the content-shape map)

**Reason from the concept's *shape* to a visual language, THEN pick the concrete form/component below.**
Before opening the content-shape map, read the idea's underlying shape and reach for its visual
metaphor. The **`slide-design` agent owns this move** (step 2 of `agents/slide-design.md`); the concrete
form / component is chosen in the map below (and `design-gallery.md`).

**The single authoritative dictionary is the Concept → Visualization decision table in
`references/design-intelligence-addendum.md` §3** — with the full **Use when / Avoid when / Common AI
failure** detail for every concept. The compact reminder below is a *pointer into it*, not a second
source: reach for the visual language here, then resolve the use / avoid / failure-mode call — and any
concept not listed below — in the addendum before picking the concrete form.

| Concept | Visual language | Concept | Visual language |
|---|---|---|---|
| **Flow** | pipeline / river / conveyor | **Decision** | decision-tree |
| **Journey** | timeline / road / metro | **Process** | assembly-line |
| **Growth** | mountain / rocket / curve | **Relationship** | network |
| **Loop** | flywheel / orbit | **Dependency** | sankey |
| **Comparison** | split-screen | **Scale** | stairs |
| **Hierarchy** | pyramid → `tier_stack` | **Prioritization** | quadrant |
| **Strategy** | compass | **Evolution** | timeline |
| **Ecosystem** | galaxy / network | **Risk** | heatmap → `heat_matrix` |
| **System** | circuit / layer | **Performance** | dashboard |
| **Transformation** | morphing | **Progress** | progress-bar |
| **Geography / where** | map → `choropleth` (shade a RATE) | **Spatial spread** | map → `choropleth` |

## By communicative intent

| The content is… | Candidate forms (deckkit, in rough preference order) | Tie-breaker |
|---|---|---|
| **A comparison** (A vs B; before→after) | `table`(highlight row) · `dumbbell` · **`dumbbell_board`** (a WHOLE results scoreboard — one collision-free dumbbell row per metric, per-row scales, hero row + threshold tick; an optional **8th row element `v_mid`** draws an intermediate mid-dot on the track, and value labels **flip OUTWARD on lower-is-better rows**, so leftward rows can't collide) · **`kpi_card`** grid (layered result cards with DELTA CHIPS — the change foregrounded as +51%/−72% pills; pick it when the *delta* is the story, `dumbbell_board` when the *magnitude* should be seen spatially) · **`flow_compare`** (old-vs-new PROCEDURE — two parallel stage-chip rows, bottleneck highlighted, per-row result chips; THE form for a process-rebuild / redefined-pipeline story; row labels default to OLD/NEW — CJK decks pass `old_label="旧流程", new_label="新流程"` explicitly) · `slope` · `before_after` · `change_stat` · `quadrant` | table for >2 dimensions; **dumbbell** for one before→after gap *per item*; slope for a 2-point rank change; change_stat for a single baseline→after; quadrant when **two axes** carry the point |
| **A process / sequence / steps** | `step_list` · `flow_chain` · `timeline` · `node`+`connector` · **`cycle_diagram`** (a CIRCULAR process — lifecycle / feedback loop / flywheel, with the optional dashed reinforcing arrow) · `repeat_row`(if N identical stages) | timeline if the steps are **dated**; flow_chain if **linear** with stroke semantics (+ shape semantics, elbow for loops); step_list if linear & numbered; **any branching** → the **decision-flowchart recipe** (`design-gallery.md`: happy path on ONE spine, branches to one consistent side, elbow merges); **~8–10+ steps → group into phase lanes (region boundaries + phase headers), convert to an appear-build (only if builds are opted in), or split into two slides — never shrink the nodes** |
| **Parts of a whole / composition** | `native_donut` · `segmented_bar` · `stat_row` · `leaderboard` | donut for 2–4 shares; **segmented_bar** for cumulative 100%; leaderboard for a *ranked* breakdown |
| **A relationship / structure / architecture** | `hub_spoke` · `node`+`connector` · `concentric_rings` · `quadrant` | hub_spoke for one centre + spokes; concentric_rings for **nested** layers; node+connector for a general graph (one `hub`); a multi-layer SYSTEM → the **system-architecture recipe** (`design-gallery.md`: role layers as columns/rows — LTR for pipelines, TTB for stacks — adjacent-layer connectors only, ONE bus bar for shared middleware); **8+ edges or time-ordered messages → number them with small badge chips so the narration can index them** |
| **A trend over time** | `native_chart`(line) · `slope` · `native_dual_axis` · `native_pareto` | line for many points; **slope** for two points; dual-axis for two scales (A↑ vs B↓) |
| **A total AND its component MIX over time** (composition) | `native_chart(kind='column_stacked'` / `'…_stacked_100'` / `'area_stacked'`) | stacked when the TOTAL matters too; `…_100` when the SHARE is the story (mix shift); area for many periods. Omit `highlight` so the mix reads |
| **A few standout numbers / KPIs** | `scorecard`(3–6 tiles) · `stat_row` · `big_numeral`(one hero) · `change_stat` · `meter_bar` · **`bullet_graph`** (actual vs TARGET with poor/ok/good bands — a status dashboard) · **`dot_strip`** (3–6 NAMED values positioned on ONE shared value axis — e.g. postdoc / academic / industry pay, with anti-collision labels + an optional highlighted dot) | big_numeral when **one** number is the whole point; scorecard for 3–6; meter_bar for a single share/percentile; **bullet_graph** when each KPI has a *target* and a good/ok/poor context (per-row scale, so mixed units are fine); **dot_strip** when several values must be *seen against each other on a common scale* (it and `dumbbell_board` / value-spaced `timeline` / `bullet_graph` / `range_bars` share one `axis_scale` mapper, so value geometry never drifts between forms) |
| **A set of distinct attributes / features** | **first ask:** is there magnitude (`stat_row`) or two axes (`quadrant`) or a comparison (`table`)? → use those. Only if the items are **truly parallel, unordered, equal-weight** → `icon_card` row / `columns` cards | cards are the *considered* choice for parallel-equal items, **not** the default for anything list-shaped |
| **Score / rate N options against M criteria** (a decision / vendor / trade-off grid) | **`eval_matrix`** (options×criteria grid; `mark="ball"` = Harvey balls 0–4 via `harvey_ball`, `mark="mark"` = semantic ✓/◐/✕; `recommend=<col>` tints the winner + a RECOMMENDED tab) | a *qualitative* scoring grid — the glyph cells are the value `table` can't give; use `table` when the cells are plain text/numbers, `eval_matrix` when they're ratings/pass-fail |
| **A category×category grid coloured by value** (risk matrix, prioritization, correlation, cohort) | **`heat_matrix`** (`scale="seq"|"div"|"risk"`, contrast-aware cell text, optional legend) | the designed risk/prioritization/small-correlation grid; a LARGE statistical heatmap (big correlation/confusion + continuous colorbar) stays on the matplotlib "compute the real artifact" path (`data-viz.md`/paper-figures) |
| **A value PER GEOGRAPHIC REGION** (per country / per province — unemployment, revenue, adoption, share) | **`choropleth`** (maps: `europe` · `world` · `china` provinces; real public-domain geometry, light→`accent` ramp, neutral no-data, NATIVE title + gradient legend so units/titles are CJK-safe; key by ISO alpha-2/3 or name, or province name/adcode) | reach for it when the categories ARE places and *where* is part of the story — a `dot_strip`/bar throws the geography away. **Shade a RATE/share/per-capita, not a raw count** (a total just re-draws population/area — see data-viz.md). NOT for a handful of regions where names suffice (use `dot_strip`), nor sub-national detail the three base maps don't cover |
| **A dated PLAN / roadmap / schedule** (durations, overlap, parallel workstreams) | **`gantt`** (task bars on a shared `axis_scale`; `lanes=` swimlanes, `today=` marker, `ticks/tick_labels=` a quarter/month grid) · a Now/Next/Later board = `columns(3)` bucket recipe | `gantt` when tasks have **durations / overlap / lanes**; a **dated point-sequence** (milestones, no durations) stays `timeline`; a simple linear list stays `step_list` |
| **A total that builds from start→end** (a variance walk, revenue bridge, cost buildup) | **`waterfall`** (raster recipe, `scripts/designed_charts.py`; floating rise/fall/total bars + connector steps; the documented **semantic up/down colour** exception) | when the *composition of a change* is the point, not just the endpoints (`change_stat`/`dumbbell` show endpoints; waterfall shows the walk) |
| **A narrowing pipeline / a stacked hierarchy of tiers** | **`tier_stack`** (`mode="funnel"` = conversion/drop-off narrowing · `mode="pyramid"` = Maslow / strategy tiers / foundation→apex; proportional tiers + semantic colour ramp; `values=` conversion %/counts) + thin `funnel()`/`pyramid()` wrappers | funnel for **stage drop-off**, pyramid for **proportional layers** — the taper the deck's Hierarchy/Bottleneck metaphors point at |
| **A real product / UI screenshot to showcase** | **`device_frame`** (`chrome="browser"` = window + traffic-lights + URL pill · `chrome="phone"` = bezel + notch; clips the real screenshot to the inner rounded rect) | for a product/pitch/teaching deck showing an actual app/site — frames the shot so it reads as the product, not a floating rectangle |
| **One idea / a claim / a quote** | `pull_quote` · `big_numeral`+caption · a whole figure + assertion title · `insight_banner` | pull_quote for a verbatim line; big_numeral for a single statistic; figure when the artifact *is* the point |
| **Dense reference / many fields** | `table` · `spec_card` · `wireframe_grid`+`spec_list` · `sources_page` (the references/citations bookend) | table for rows×cols; spec_card for a mono key→value placard; wireframe for a UI/layout spec |
| **Code / a config / a command** | `code_block` (mono, syntax-tint, keep it SHORT — the 5 lines that matter, not a whole file) | show the *snippet that makes the point*, not a scroll; annotate the key line |
| **A formula / equation** | **`equation_native`** (EDITABLE LaTeX-subset — the default) · `equation_png` (2-D: fractions/matrices/stacked) · `eq_par` (one inline symbol/variable) · **`concept_equation`** (a *word*-equation headline, e.g. ZINE = MAGAZINE) | typeset it, never ASCII/screenshot; size to body text; `concept_equation` when the "equation" is rhetorical, not mathematical |
| **Photos / an image set / a gallery** | `picture`(one hero) · `before_after` (2-up A/B) · `image_tab` (labeled A/B/C tabs) · `photo_triptych` (3-up band) · `photo_card` (framed with caption) | one strong image beats a grid of small ones; duotone to the palette (`image_fx`) so photos don't fight the accent |
| **A call to action / a next step / the ask** | `cta_button` (one primary action) · `cta_pair` (primary + secondary) | for a pitch/inspire/decision close — one clear ask, not a wall of links |
| **A concept that needs the real thing** | a **computed/generated domain artifact** (image-generation.md) · a **whole source figure** | compute/extract the real artifact (FFT, a real plot, a patch) — never a box-and-dot cartoon |
| **A principle / mechanism / experiment / definition you're EXPLAINING** (physics · chemistry · biology · engineering · econ · *any* subject — how/why it works, an apparatus/setup, a defined concept) | a **labelled schematic diagram ALONGSIDE a short text description** (forces · signal-path · reaction · apparatus · geometry · cause→effect) · a generated/computed domain artifact · `node`+`connector` · an annotated whole figure | **default to a diagram + text, not text-alone** — and **build the schematic CORRECTLY**: components / connections / geometry / reaction / apparatus must be **domain-accurate & faithful to the source** (a wrong or generic box-and-dot cartoon is worse than none). Schematic when spatial/causal/procedural; **extract/compute the real artifact** when it must look real (a specific molecule, a real plot); an equation (mathfont) when the law *is* the relation. Text-only for something a diagram could show is a miss. **HOW to build a physical/spatial schematic (force · ray · circuit · apparatus · vector · wave) → `references/schematic-diagrams.md` — matplotlib/domain-lib for precise/label-critical ones, or the image tool for complex/stylized/template-matched ones (labels overlaid native, geometry verified) + the fidelity gate;** the deckkit node/connector kit is for conceptual box-flow only. |
| **An algorithm / method / training-or-optimization procedure** (ANY field — ML, but also a derivation, optimizer, lab/comp protocol) | `algorithm_block` (numbered pseudocode — Input/Output, for/if, indentation) · `flow_chain` / `node`+`connector` (the data-flow/architecture) · `step_list` | **`algorithm_block`** when the *exact steps, loops, Input→Output* matter (a training loop, an optimizer, a derivation); a **flow/architecture diagram** when the *data path between modules* is the point; **often BOTH** — the block for precision + a small diagram for intuition. Don't bury a precise procedure in prose. |

**Compose-from-primitives recipes (no dedicated component — build from existing helpers; recipes in `design-gallery.md`/`data-viz.md`):**
- **A team / founders / people roster** → circular headshots `picture(fit="cover", round=…)` on a `columns(n)` grid + name/role/bio `text()` — one avatar diameter, one accent, one alignment across all cards (CRAP Repetition), like `icon_card` siblings.
- **An org chart / issue tree / driver tree** (parent→children decomposition) → `node` + `elbow_connector` as a branch-bus (parent drop → horizontal bus → evenly-spaced child drops); MECE, left-to-right for a driver/issue tree. (Watch the "org chart as decoration" anti-pattern — prefer it only when the branching IS the point.)
- **Shared attributes / a "sweet spot"** → a Venn of 2–3 translucent `glass_card`/`box` circles with labeled overlaps.
- **The same metric across many comparable slices** (regions/products/cohorts) → **small multiples**: a `rows`/`columns` grid of identical mini `native_chart`s with **shared scales** + one highlighted slice (`data-viz.md`).
- **A value RANGE per category** (a "football field" — valuation/estimate ranges) → **`range_bars`** (floating min–max bars on a shared `axis_scale`, one row per category, optional base-case tick — a `dot_strip` cousin for ranges). Use `dot_strip` instead when each row is a single best-estimate POINT, not a genuine min–max range.
- **A persistent agenda / section tracker** → a thin nav rail listing sections with the current one accented, repeated as quiet chrome (or `step_list(active_idx=…)` on a dedicated agenda page).

**Micro-viz & furniture (accents ON a form, not the form itself):** a **rating / qualitative level** →
`dot_meter` (●●○) or `harvey_ball`; a **pros/cons or +/− tradeoff list** → `tradeoff_list`; a **single
share/percentile/progress row** → `meter_bar`; the **"so-what" beside a chart/figure** → `takeaway_rail`
or `insight_banner` (the so-what bar); a **status/confidential stamp** → `status_stamp`, a **RECOMMENDED
corner** → `corner_tab`. **East-Asian register** (ink/traditional decks) — `seal` (vermilion chop),
`cjk_numeral` (壹贰叁), `bilingual_lockup` (CJK + tracked-Latin headline) — see `east-asian-aesthetic.md`.

**Cross-links:** pick the **chart type** in `data-viz.md` (editable-native vs raster); draw a
**science schematic** (force/ray/circuit/apparatus) per `schematic-diagrams.md`; reach for the
exact **component** in `design-gallery.md`; place safely with the `deckkit` helpers in SKILL.md step 4.

## New forms (quick index)
- **Small multiples** → `deckkit.small_multiples` — build them through the ONE call (hand-composing
  native_chart per panel silently loses the shared scale that IS the form).
- **Labelled 2-D position** → `deckkit.position_map` (quadrant() discards within-cell position).
- **Figure walkthrough** → `deckkit.annotated_figure` (numbered markers + caption rail + inset).
- **Hierarchy** → `deckkit.org_tree` (tidy centroid layout; auto-raises when unfittable).


## How the slide-design agent uses this (the Form ledger)
For every **content** slide, the plan records one Form-ledger row — `slide | visual protagonist |
format-family (card / chart / diagram / quote / big-number / timeline / table / photo) | build?` — plus,
in the per-slide Layout cell, the winner **and** the alternative it beat: e.g. *"dumbbell — beats
bar+table because the per-item before→after gap IS the point; a bar hides the pairing."* The **diversity
gate** then runs against the ledger: if any one format-family exceeds **~40–50%** of the content slides,
the plan is **not ready** — rework the weakest into the form its content actually wants. (Taste, not a
quota: a genuinely card-shaped run is allowed *with a one-clause justification in the ledger* — the gate
is auditable, never silent.)
