# The King of Pop Template (English)

## Template File

`template.pptx`

## Summary

A 14-slide, 16:9 biography / tribute deck, built around Michael Jackson. The visual system is a dark spotlight + gold "King of Pop" theme: full-bleed cover, numbered content slides, a life timeline, stat cards, an album bar chart, a wall of honor, light & shadow, the final curtain and legacy. This is the English-only cut, split from a bilingual source (Chinese version: `zh/michael-jackson-king-of-pop`).

Use this when the user wants a ceremonial profile deck (celebrity biography, tribute, brand / person profile, cultural retrospective).

## Inspected Structure

- Slide size: 10.00 x 5.62 in (16:9). Slides: 14. Layouts: 11. One album bar chart.
- Fonts: Arial (body/display), Courier New (mono running header), Arial Black (accents).

## Use It For

- Celebrity biographies, tribute reels, person / brand profiles.
- Cultural retrospectives, life timelines, a subject's "highlights & controversy".

## Reuse Rules

- Keep the rhythm: full-bleed cover → numbered content → timeline → stats → honors → light & shadow → final curtain & legacy.
- Reuse the dark + gold spotlight visual; replace with the user's subject, data and imagery.

## Agent Notes

1. Run `scripts/inspect_template.py templates/decks/en/michael-jackson-king-of-pop/template.pptx` before building.
2. Use `deckkit.open_template()` when building on this preset; source build script in `_sources/michael-jackson-king-of-pop/` (`build_mj_mono.py`, driven by `MJLANG=zh|en`).
3. Treat the template as a visual system, not as source content.
