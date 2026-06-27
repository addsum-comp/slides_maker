# Icons — one coherent family, recolored to the deck, used with restraint

Icons can lift a deck (label categories, mark sections, give a card a focal point) — but used
badly they make it look *worse* (a mismatched zoo, decorative clutter, the same junk as emoji
in titles). The whole value is **consistency**: a coherent icon family is an *identity system*
(CRAP "Repetition"), and a single icon gives a block a focal point (CRAP "Contrast"). Get those
two right and icons read as "designed"; get them wrong and they read as AI-slop.

## Design them yourself, or fetch them? — FETCH, from one open-licensed family
**Do not hand-draw an icon set.** Hand-/AI-drawn icons come out inconsistent — varying stroke
weight, optical size, corner radius, metaphor — which is exactly the inconsistency that looks
amateur. A curated library is a *system*: hundreds of icons on one grid, one stroke weight, one
visual language. That coherence is the point. (The only acceptable "self-drawn" mark is a trivial
geometric primitive deckkit already draws — a dot, arrow, plus, check — or a case where literally
no library icon fits; even then match the deck's stroke language.)

**Pick ONE family per deck**, to the deck's mood (all permissive licenses — no attribution needed):

| family (`spec` prefix) | look | license | best for |
|---|---|---|---|
| `tabler:` (+ `tabler-filled:`) | crisp, minimal line | MIT | default; corporate / product / clean |
| `lucide:` | clean, neutral line | ISC | minimal / editorial |
| `phosphor:` (+ `phosphor-bold:`) | friendly, rounded line | MIT | approachable / teaching / playful |
| `feather:` | spare, thin line | MIT | very minimal |
| `heroicons:` (+ `-solid`) | corporate line/solid | MIT | enterprise / stakeholder |
| `simple:` | **brand / tech logos** (GitHub, Python, AWS…) | CC0 | representing actual products/tech |

Mixing two *content* families on one deck is a consistency tell — don't. (Exception: a `simple:`
brand logo can sit alongside your one content family, since logos are their own category.)
**SVG Repo** has **mixed per-icon licenses** — prefer the curated sets above; if you must use it,
check that icon's license and attribute when the license requires it.

## Mechanism — fetch → recolor → rasterize → place
python-pptx can't reliably embed SVG, so rasterize to a **transparent high-DPI PNG** (renders
identically in PowerPoint / Keynote / the LibreOffice render / the critic) and recolor to the deck
palette first. `scripts/icons.py` does it; `deckkit.icon()` / `icon_card()` place it.

```python
from icons import icon_png            # scripts/icons.py
import deckkit as dk
ACC = "#1F5FA8"                        # the deck accent
p = icon_png("tabler:chart-bar", "assets/icons/chart.png", color=ACC, px=160)  # fetch+recolor+raster
dk.icon(s, p, x, y, 0.42, disc="#E8F0FA")        # a single icon (optional tinted tile behind it)
dk.icon_card(s, *col, p, "Analytics", "Track what matters", accent=dk.ACCENT, disc="#E8F0FA")
```
- Keep recolored PNGs in `~/Downloads/<deck>/assets/icons/` (reproducible from the build).
- **Rasterizer:** `icons.py` tries cairosvg → rsvg-convert → headless Chrome (the last is usually
  present). If none exists it errors clearly — `pip install cairosvg`, or install Chrome/Chromium.
- **Offline / exact-name unknown:** pass a **local `.svg` path** to `icon_png()` instead of a spec
  (the user can drop an SVG in), or check the library's site for the exact kebab-case name.

## When icons HELP vs HURT
**Help** (use): a **row of feature/category/section cards** each marked by an icon; a **section
divider** or wayfinding mark reused per section; a **brand/tech logo** (`simple:`) to name a real
product; a single focal icon in a callout/stat tile. The test: the icon **aids recognition or
labels a category** the audience scans.

**Hurt** (cut): an icon on **every bullet** (clutter, not information); a **decorative** icon that
labels nothing; **mismatched families** on one deck; an **oversized** icon competing with the title;
an icon **carrying meaning with no text label** (fails accessibility + ambiguous); a literal/cheesy
metaphor (a lightbulb for "idea" on every slide). Icons are seasoning — a few, consistent, purposeful.
**Never** substitute emoji or ✅/🚀/🔥 for real icons (that's an AI-slop tell, see design-principles).

## What makes icons look GOOD — five qualities (from real well-iconned decks)
A good icon slide gets ALL of these right; getting one wrong is what makes icons look tacked-on.

1. **Semantic fit — the metaphor matches the content it labels.** Pick the icon whose meaning *is*
   the thing: an **eye** for "perception", a **brain** for "reasoning", a **bolt** for "action", a
   **database** for "memory"; a **magnifier** for "parse", a **target** for "select", a **plug** for
   "execute", a **check** for "validate", a **retry/refresh** for "recover", **layers** for "deliver".
   A generic or mismatched icon (a gear on every card) is worse than none — it mislabels.
2. **Colour-coded by category — each category its OWN hue, and the icon carries it.** In a multi-
   category layout (layers, sections, steps, problem areas) give each category a distinct accent and
   make the **icon, its label, its card tint, and any pill/number all share that one hue** — so colour
   itself encodes "which group". Derive the N hues from `deckkit.palette(n)` (distinct, contrast-
   checked) and apply one per category, consistently. (This is the single biggest "looks designed"
   move — NOT one global accent on every icon when the layout has real categories.)
3. **Contrast against the background.** On a **dark deck**, icons are **bright/saturated** accent
   colours, often in a **disc/tile** that lifts them off the card (a deep-tinted disc on a dark card
   with a bright icon, or a dark disc on a colour-banded header with a light icon). On a **light deck**,
   a saturated accent icon (never pale-grey, never pure black). Aim ≥3:1 icon-vs-its-immediate-
   background so the shape reads. The `disc=` tile is the easy way to guarantee contrast.
4. **Consistent position & size across siblings.** Pick ONE placement and repeat it: **upper-left of
   the card** (`icon_card`, the default) or **centred at the top** of a step/pipeline card — every
   sibling the **same family, size, colour-treatment, and position**. Size small, to ~heading scale
   (**≈0.32–0.5 in**), and **never larger than the title** (font-hierarchy). One odd icon breaks it.
5. **Design style matches the deck.** Outline icons for a clean/minimal/technical deck (the dark
   "glowing line" look pairs thin line icons), filled/solid for a bold or corporate deck — and the
   icon weight should echo the deck's type/stroke. Don't mix outline and filled across siblings.

## Placement patterns + the craft
- **Upper-left corner of a card** (`icon_card`) — default and strongest: icon top-left (bare or in a
  `disc=` tile), title under it, body below; the eye lands on the icon then reads down.
- **Centred at the top of a step card** — for a pipeline/numbered sequence (often a number circle
  above + icon + label + an output line + a bottom pill), the icon centred, recolored to that step's
  hue; consider highlighting the terminal/success step.
- **In a colour-banded header** — icon in a circular disc inside a per-card accent band, with the
  category label beside it (good for a 3-up problem/feature panel).
- **Other:** above a centred big-number/stat; inline just before a chip/section label (vertically
  centred with the text); a light icon inside a solid accent bar.
  Whatever you pick, apply it the **same way everywhere**.
- **Accessibility:** an icon is *support* — the **text label always carries the meaning**, never an
  icon alone. Set `alt=` when informative; keep the icon legible against its background.

## Build checklist
One family · **semantic fit** (metaphor matches the content) · **colour-coded per category** (each
category its own hue from `palette(n)`, carried by the icon + label + tint) · **contrast** against the
background (bright on dark / saturated on light, disc if needed) · small (≤ title) · **consistent
size/position/treatment** across siblings · style matches the deck (outline vs filled) · labels
something (not decoration) · text always present · assets cached in the deck folder.
