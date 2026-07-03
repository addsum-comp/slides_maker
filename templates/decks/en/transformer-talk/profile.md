# Attention Is All You Need Paper Talk Template

## Template File

`template.pptx`

## Summary

A 15-slide, 16:9 paper-reading and lab-meeting deck built around Vaswani et al.'s `Attention Is All You Need`. It is the main template for the "Lab Meeting / Paper Talk" category: background problem, core claim, architecture, attention equations, multi-head attention, positional encoding, results, limitations, and takeaways.

This is a real-content example deck, not an empty placeholder. Reuse its visual system, rhythm, and paper-talk structure, but replace the Transformer-specific content with the user's own paper.

## Structure

- Slide size: 10 x 5.625 in.
- Slides: 15.
- Language: English, with paper title, institution names, metrics, and equations preserved.
- Example content: `Attention Is All You Need`, NIPS 2017 / arXiv:1706.03762.

## Use It For

- Paper reading, lab meetings, method overviews, and experiment reports.
- Classic-paper walkthroughs or new-paper presentations.
- Technical decks that need to explain paper figures, formulas, experimental results, limitations, and implications.

## Reuse Rules

- Keep the narrative rhythm: background problem → central claim → architecture → mechanism → results → limitations and takeaways.
- Reuse the visual system and slide types, not the Transformer facts. Unless the user's topic is Transformer itself, replace all claims, numbers, figures, and equations.
- Paper figures, tables, and formulas must come from the user's material or be re-typeset; do not leak Transformer example content into a new topic.
- This is the default academic/research presentation starting point for English users.

## Agent Notes

1. Run `scripts/inspect_template.py templates/decks/en/transformer-talk/template.pptx` before building.
2. Use `deckkit.open_template()` when building on this preset.
3. Preserve the density, numbered rhythm, and organization of formula / figure / result slides.
4. For presented decks, continue adding speaker notes so the user can present directly.
