# Font guidance — pick portable fonts, avoid tofu

A `.pptx` stores font *names*, not the fonts themselves (unless you embed them). If a
machine opening the deck lacks the named font, PowerPoint/Keynote silently substitutes
one — shifting metrics and spacing, and for non-Latin text producing **tofu** (□□□) when
the substitute lacks the glyphs. So choose fonts that are present *everywhere the deck
will be opened*, and flag the dependency at hand-off.

## Cross-platform-safe Latin fonts
Reliable on Windows + macOS (and close enough on Linux/LibreOffice via metric clones):
- **Sans:** Calibri, Arial, Verdana, Tahoma, Trebuchet MS. (Calibri ships with MS Office;
  on a Mac *without* Office it may substitute — Arial is the safest universal sans.)
- **Serif:** Georgia, Times New Roman, Cambria.
- **Mono (code):** Consolas, Courier New.
LibreOffice (what `render_deck.sh` uses) substitutes Calibri→Carlito, Cambria→Caladea,
etc. — metric-compatible, so the render is representative.

`deckkit` defaults: `FONT="Calibri"`, `MONO="Consolas"`, `EQFONT="Arial"`. Override them
right after import to match a brand or to maximise portability (`deckkit.FONT="Arial"`).

## Equations are font-independent
`equation_png` rasterises math with matplotlib's bundled math fonts, so **equations carry
no font dependency** — they render identically anywhere. Prefer it over `eq_par` when you
want zero font risk on the math (see `design-principles.md`).

## Non-Latin (CJK / etc.)
Set `deckkit.EAFONT` to a script-appropriate font so every run is tagged with a CJK
typeface (not an uncontrolled fallback): PingFang SC / Heiti SC / Noto Sans CJK SC
(Chinese), Hiragino / Noto Sans JP (Japanese), Apple SD Gothic / Noto Sans KR (Korean).
Noto fonts are the most portable (free, broad coverage). Full guidance + RTL limits in
`references/multilingual.md`.

## Brand fonts
If the user's brand uses a non-standard font (e.g. a foundry font), the recipient needs it
installed or the deck won't match. Options, in order: (1) use it but **flag** that viewers
need it installed; (2) **embed fonts** in the .pptx (PowerPoint: File → Options → Save →
"Embed fonts in the file" — note this is a manual step python-pptx can't do, and bloats
the file); (3) substitute a safe near-equivalent and tell the user. Default to a safe font
unless the brand font is essential.

## If you see tofu / wrong fonts in the render
1. The glyph is missing in the (substituted) font — for CJK, set `EAFONT`; for special
   symbols, prefer `equation_png` or a Unicode-complete font (Arial).
2. The font name isn't installed on the render machine — `bash scripts/check_env.sh`
   lists what's available; switch `FONT`/`MONO`/`EQFONT` to a present font and rebuild.
3. Re-render and confirm. At hand-off, tell the user which fonts the deck depends on.
