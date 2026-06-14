# Analysing a style example — understand it fully, then reproduce it

When the user gives a deck to **mimic the style of** (Q4), the goal is to reproduce
its *look and feel* in your own build — without building on it or taking its logos.
A glance at one slide is not enough: a style lives in the **system** (how the same
choices repeat across slides) and in the **details** (the small decorations that give
it character). Study it properly, write the brief below, then build to the brief.

## First, look at the whole thing
**Render and view EVERY slide** (`render_deck.sh` for .pptx, pymupdf for .pdf, or read
the image files). Zoom in to read fonts, measure spacing, and pick exact colours
(sample hex from the rendered pixels). Notice what is *consistent* across slides —
that consistency IS the style.

## Write a STYLE BRIEF (before building)
Capture each of these concretely (with hex codes, sizes, and "where/how used"):

1. **Overall structure & rhythm.** What slide archetypes recur (title, section
   divider, content, full-bleed figure, two-column, results, closing)? How is the
   deck sectioned — are there divider slides, an agenda, running section labels,
   progress dots? What's the typical information density per slide?
2. **Grid & layout.** Margins and safe area; is content left-aligned to a column or
   centred? Where does the title sit (band? top-left? over a shape?) and the footer?
   How is whitespace used — airy or packed? Is there a consistent two/three-column grid?
3. **Colour system.** The base background; the primary text colour; 1–3 accent colours
   and **exactly where each is used** (titles? rules? highlights? backgrounds?). Light
   or dark theme? Any gradients?
4. **Typography.** Heading font vs body font; sizes and weights for title / section /
   body / caption; sentence case vs Title Case; any all-caps labels.
5. **Decorations & motifs** — the character. Header/footer **bands or bars**; **rules
   / dividers** (thickness, colour); **shapes** (rounded vs sharp corners, circles,
   chevrons, ribbons); **icons or bullets** (style, colour); **shadows / borders**;
   page-number treatment; logo placement; any **signature touch** that makes it
   recognisable (a corner accent, a coloured side-strip, a consistent dotted leader).
6. **How recurring elements are styled** (match these, since they appear on every
   slide): titles, bullet markers, **callout/emphasis boxes**, figure framing &
   captions, **tables** (ruled? shaded header? zebra?), **equations**, pipeline/▢→▢
   diagrams, "takeaway" treatments, quotes.
7. **Tone.** Formal/academic · corporate · playful · editorial — and what makes it so.

## Reproduce, don't copy blindly
Build with `deckkit` but **override the defaults to match the brief** — set the
palette to the example's hex colours, the fonts to its fonts, the title/footer
treatment, the corner style (rounded vs sharp), the bullet/rule/band motifs, and the
table/figure/equation styling. Re-create the *system and the decorations*, applied to
the **user's** content and purpose. Keep the craft rules (whole figures, gutters,
margins, legible results) — a style preference never overrides those.

Then **verify by render**: put a slide of your deck next to the example and check they
read as the same family (same palette, same title treatment, same motifs, same density).
If a template (Q1) is also in play, the template's branding wins where they conflict;
the style example governs the rest.
