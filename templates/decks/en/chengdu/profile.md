# Chengdu Traveller Guide Template

## Template File

`template.pptx`

## Summary

A 12-slide, 16:9 travel and city-guide deck built around Chengdu. The visual system is warm, editorial, image-forward, and paced like a guided story: cover, reasons to care, section breaks, feature pages, and a closing mood.

Use this as a preset when the user wants a vivid but calm deck about a place, culture, event, destination, lifestyle topic, or public-facing explainer.

## Inspected Structure

- Slide size: 13.33 x 7.50 in.
- Slides: 12.
- Slide masters: 1.
- Layouts: 11.
- Built-in layouts include `Title Slide`, `Title and Content`, `Section Header`, `Two Content`, `Comparison`, `Title Only`, `Blank`, `Content with Caption`, and `Picture with Caption`.

## Existing Content Pattern

The source deck begins with:

- `A TRAVELLER'S GUIDE / Chengdu / 成都`
- `WHY CHENGDU`
- `THE PANDAS`
- `GIANT PANDAS`
- `THE FLAVOUR`

These are content examples only. Do not preserve Chengdu facts unless the user's new deck is actually about Chengdu.

## Use It For

- City or destination guides.
- Culture, food, travel, tourism, and lifestyle explainers.
- Public-facing decks where atmosphere matters but readability still has to stay high.
- Lightweight narrative decks with section rhythm.

## Reuse Rules

- Keep the pacing: strong cover, short section breaks, image-led feature slides, restrained explanatory copy.
- Reuse the visual feel and slide rhythm, not the original Chengdu content.
- Replace all destination names, facts, captions, and imagery with the user's actual source material.
- Keep text brief. This template works best when one large image or scene carries each slide.
- If the new deck is data-heavy or corporate, use this only for opening/section mood; prefer a more analytical preset for dense evidence.

## Agent Notes

1. Run `scripts/inspect_template.py templates/decks/en/chengdu/template.pptx` before building.
2. Use `deckkit.open_template()` when building on this preset.
3. Extract palette, fonts, and any recurring chrome from the source deck instead of hardcoding new colours.
4. Treat the template as a visual system, not as source content.
