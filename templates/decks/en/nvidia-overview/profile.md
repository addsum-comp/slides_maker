# Company Overview Template

## Template File

`template.pptx`

## Summary

A 16-slide, 16:9 corporate company-overview deck, built around a single company's story (NVIDIA in the source). The visual system is confident and modern: a strong cover, an identity statement, an origin story, product pillars, a metrics page, and a forward-looking close. It is paced to introduce a company to investors, partners, recruits, or customers.

Use this as a preset when the user wants a polished "who we are / what we build / why it matters" deck: a company overview, a pitch backbone, an investor intro, a product-portfolio tour, or a recruiting brand deck.

## Inspected Structure

- Slide size: 10.00 x 5.62 in (16:9).
- Slides: 16.
- Layouts: 11.
- Built-in layouts include `Title Slide`, `Title and Content`, `Section Header`, `Two Content`, `Comparison`, `Title Only`, `Blank`, `Content with Caption`, `Picture with Caption`, `Title and Vertical Text`, and `Vertical Title and Text`.

## Existing Content Pattern

The source deck runs:

- `COMPANY OVERVIEW 2026`
- `WHO WE ARE` / `OUR STORY` / `WHAT WE BUILD`
- `BY THE NUMBERS`
- `DATA CENTER · THE CORE`
- `ANNUAL CADENCE` / `ADOPTION` / `THE MOAT` / `NETWORKING`
- `GAMING · WHERE IT BEGAN` / `SIMULATION · DIGITAL TWINS` / `PHYSICAL AI`
- `THE VALUE` / `TRAJECTORY` / `GET STARTED`

These are content examples only. Do not preserve NVIDIA facts unless the user's new deck is actually about NVIDIA.

## Use It For

- Company / startup overviews and corporate intros.
- Investor and partner pitch backbones.
- Product-portfolio and platform tours.
- Recruiting and employer-brand decks.

## Reuse Rules

- Keep the arc: strong cover → identity → story → what you build → numbers → product pillars → value → trajectory → call to action.
- Reuse the confident, modern visual feel and slide rhythm, not the original NVIDIA content.
- Replace all company names, products, metrics, and claims with the user's actual material.
- Works well for a mix of statement slides and metric slides; keep copy tight so each slide lands one idea.
- For a deep technical review prefer an analytical preset (e.g. the MRI Reconstruction Trends template); for atmosphere-led storytelling prefer an editorial preset (e.g. the Chengdu template).

## Agent Notes

1. Run `scripts/inspect_template.py templates/decks/en/nvidia-overview/template.pptx` before building.
2. Use `deckkit.open_template()` when building on this preset.
3. Extract palette, fonts, and any recurring chrome from the source deck instead of hardcoding new colours.
4. Treat the template as a visual system, not as source content.
