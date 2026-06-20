# Non-Latin languages (Chinese / Japanese / Korean / …)

The pipeline is Unicode-clean — python-pptx, the LibreOffice renderer, and PowerPoint
all handle non-Latin text. The deck won't break. The things that make it look *good*
(not just render) are **font glyph coverage**, **PowerPoint portability**, and a few
**script-specific typography** habits.

## One language, consistently (the default)

**A deck is written in ONE language throughout** — every title, bullet, callout, label,
axis, footer, and the closing slide. The most common failure when building from source
material in another language (e.g. an English-speaking user + a Chinese codebase, or a
Chinese paper presented to an English user) is a deck that drifts: English headings over
Chinese bullets, one slide in the wrong language, a stray translated-vs-untranslated mix.
Pick the **target language** (step 0) and hold it across the whole deck.

- **Decide the target language explicitly.** Default to the language the *user* is
  writing in. **When the source material's language differs from the user's**, or it's
  otherwise ambiguous, **ask** which language the slides should be in — don't assume the
  source's language.
- **Translate the content into the target language** — don't paste source text verbatim
  in the other language just because that's how the source had it (faithfulness is to the
  *facts*, not the source's language).
- **Legitimate exceptions (not "mixing"):** established technical terms, proper nouns,
  brand/product names, acronyms, units, math symbols, and code/identifiers may stay in
  their original form — e.g. a Chinese deck can say "基于 Transformer 的重建" or "DeepSeek
  API"; that's normal, not a language violation.
- **Mixed / bilingual only on request.** Only produce a deck that mixes languages (e.g.
  EN + 中文 lines together, or a bilingual conference deck) if the user explicitly asks.
  Then do it *systematically* — the same pairing on every slide (e.g. English title with
  a 中文 subtitle throughout), not ad-hoc drift.

## The one required change: set a script-appropriate font

deckkit's default `FONT` (Calibri) has **no CJK glyphs**. It still *renders* here only
because LibreOffice silently substitutes a CJK font — but in the user's PowerPoint that
substitution is uncontrolled (wrong/inconsistent font, possibly tofu □□□ on a machine
without a good fallback). So for a CJK deck, set the East-Asian font explicitly:

```python
import deckkit
deckkit.FONT   = "Calibri"      # Latin letters + numbers
deckkit.EAFONT = "PingFang SC"  # CJK glyphs  (or "Heiti SC" / "Microsoft YaHei" / "Noto Sans CJK SC")
```

`EAFONT` makes every run carry **both** `<a:latin>` (for Latin/numbers) **and** `<a:ea>`
(for CJK) — so PowerPoint/Keynote render Chinese with *your* chosen font while English
and numbers stay on `FONT`. Mixed "中文 + English 28%" text then looks intentional and
travels correctly. (Without `EAFONT`, CJK falls back to an uncontrolled default.)

### Font choices
| Role | Portable (recommended) | macOS | Windows |
|---|---|---|---|
| CJK sans (default) | Noto Sans CJK SC / Source Han Sans | PingFang SC, Heiti SC | Microsoft YaHei |
| CJK serif (formal) | Noto Serif CJK SC / Source Han Serif | Songti SC | SimSun |
| CJK brush/handwritten | — | Kaiti SC | KaiTi |
| Japanese / Korean | Noto Sans JP / KR | Hiragino Sans / Apple SD Gothic | Yu Gothic / Malgun Gothic |

Pick the CJK font to match the *purpose* the same way as Latin (`design-by-purpose.md`):
sans (Heiti/PingFang) for modern/corporate/talks, serif (Songti) for formal/defense.

### Portability caveat (say this in step 6)
PowerPoint can embed fonts, but python-pptx can't, so the recipient's machine needs the
CJK font installed — or PowerPoint substitutes. Prefer a widely-installed font (PingFang
on macOS, Microsoft YaHei on Windows) or **Noto Sans/Serif CJK** for maximum portability,
and tell the user which font the deck expects.

## CJK typography habits (so it reads like a native deck, not translated)
- **No true italic.** CJK fonts fake italic by slanting — it looks wrong. Emphasize with
  **weight, colour, or size**, never italic, for CJK runs. (Latin runs can still italic.)
- **Full-width punctuation.** Use 。，、：；（）「」 — don't add Latin spaces around them,
  and don't end CJK sentences with a Latin period. **But for a lone, centred large mark** (a
  "?" in a box, a standalone "!"), use the **ASCII** form: a full-width `？！` sits
  left-of-centre within its advance and won't optically centre. Full-width is for *running*
  CJK text, not a centred single glyph.
- **Line-breaking.** CJK wraps at any character (no spaces needed) — fine, but give text
  boxes a little more room and consider `line_spacing` ~1.1–1.2; dense CJK at tight
  leading is hard to read.
- **Density.** A CJK character carries more meaning per glyph, so terse points matter even
  more — resist the temptation to fill the line just because it fits.
- **Numbers / Latin terms** inside CJK text render in `FONT` (the latin font) — choose a
  Latin font that pairs cleanly with the CJK one (Calibri/Arial with most sans CJK).

## Equations & figures
- `eq_par` / `equation_png` use ASCII + Greek (`EQFONT`) — unaffected by language. Don't
  put CJK *inside* `equation_png` (matplotlib's math font may lack the glyphs); label CJK
  around the equation with normal `text()` instead.
- Reuse the source's figures whole as always; if a figure has burned-in text in another
  language, that's the source's, not yours.

## Right-to-left scripts (Arabic / Hebrew) — limited
deckkit lays out left-to-right and doesn't handle RTL reordering or right alignment of
flow. You can set an Arabic/Hebrew font, but bidi layout, RTL bullet/indent direction,
and mirrored chrome are **not** supported well — treat RTL as a known limitation, flag it
to the user, and keep such decks very simple (or build RTL-critical slides by hand).

## Verify
The critic already flags tofu/missing glyphs — so render and **look**: every glyph is a
real character (no □), the CJK font is the one you chose, and emphasis isn't faux-italic.
