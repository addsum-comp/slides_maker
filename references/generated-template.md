# Generate a template with an image tool

The user picked Q1's **"generate a template with an image tool."** Instead of building on a
provided template or designing a clean default, you **create a bespoke visual identity with the
image tool** (a styled hero/divider illustration) and then **reproduce it natively** so every
content block fits it. Use it for a *vivid, designed* deck — a product launch, a festival/event,
a brand or culture deck, a playful pitch — where a clean default look isn't enough.

This branch **decides the look up front**, so after it's confirmed you **skip the 3-direction
gate** and run the rest of the interview (purpose, audience, source, language) normally.

## The construction model (this is the whole idea)
A good generated template is a **cohesive visual SYSTEM**, not one pretty picture — a palette, a
small **motif vocabulary** (the signature shapes/decorations), a type pairing, and **component
treatments** (how a card, a stat, an emphasis band, a title look). It is realised in **two
layers**, and the split is what keeps it editable *and* on-brand:

- **Hero + section-divider slides → a full-bleed GENERATED image.** A rich, styled, **text-free**
  illustration carries the mood; the title and badges sit on top as **native** editable shapes.
- **Content slides → built NATIVELY to match.** No big image — the background, the decorations,
  and the content cards/chips/bands are native python-pptx shapes that **reuse the template's
  palette, motifs, and component treatments**. This is why the inserted blocks *fit*: they are
  drawn in the same system, not pasted onto a foreign picture.

> Don't make every slide a generated image with text baked in — baked text isn't editable, wraps
> badly in other languages, and can't be critiqued/fixed. Images set the mood on heroes/dividers;
> native shapes carry the content.

## Workflow

### 1 — Mini-interview for the visual identity (before generating)
Run a short extra interview *now* — only what the *look* needs (purpose/audience/source come
later in the normal interview):
- **Scenario / topic** — what the deck is for (e.g. "summer music festival annual handbook").
- **Start from a known style (recommended) — don't generate from a cold prompt.** Seed the look
  with a *proven visual language* from the **Style library** at the end of this file (e.g. the
  **Memphis** style reverse-engineered from the Sugar Rush sample, or Swiss, Art Deco, Vaporwave,
  Editorial, Risograph, …). From the catalog, **propose the 3–4 best-fit styles for this
  scenario as selectable options**, plus **"describe your own look"** and **"I'll provide a
  reference image / brand."** A named style gives the image tool a strong, coherent target and
  gives you a ready palette + motif + type starting point for the native `style.py`.
- **Vibe / mood (if describing your own)** — the aesthetic in words: energy (calm↔loud), era,
  references. Use this to pick/blend a library style or to author a fresh one.
- **Brand colours / must-haves** — any fixed colours, a logo, words that must appear.
- **Reference material — invite drop-ins.** Explicitly offer: *"drop in any reference images, a
  logo, a mood board, screenshots of a look you like, or a brand guide and I'll steer the
  generation by them."* Use provided references to anchor the style (and, if a logo/photo is
  given, place it natively, not regenerated).

**Then TAILOR the chosen style to *this* deck before generating** — fold in the topic, the brand
colours, the energy, and anything from the reference materials. The library entry is the *starting
language, not a straitjacket*: customise its palette/motifs to fit, and blending two presets (or a
preset + a reference) is fine — just name what you're combining so the choice is legible to the user.

### 2 — Generate the template image(s)
Generate a **full-bleed, text-free** hero/divider illustration in the chosen style:
- **Tooling:** native imagegen in Codex; otherwise `scripts/generate_images_openai.py` with
  `OPENAI_API_KEY` (build the prompt with `scripts/image_prompts.py`). Render at the deck's
  aspect (16:9 → e.g. `1536x864` / `2048x1152`). In Codex, follow the imagegen skill's
  built-in save-path policy: generate first, then move/copy the selected output from
  `$CODEX_HOME/generated_images/...` into this deck's folder before referencing it in
  `style.py` or a build script.
- **Prompt craft:** describe the *style + motif vocabulary + palette*, the subject/scene, **"no
  text, no lettering, no logos"**, and **leave a calm, lower-contrast zone** (a corner/band)
  where the title will sit. Ask for the **signature motifs** explicitly (e.g. "scattered Memphis
  geometric shapes — zigzags, dots, triangles, squiggles, checkerboard — bold black outlines")
  so you can reproduce them natively later.
- Generate **1–2 plates**: a **hero** (cover) and, if the look differs, a **divider** variant.
  A content-slide background is usually just the template's base colour + a few native motifs —
  you rarely need a third image.
- Keep assets in `~/Downloads/<deck>/assets/generated/`. Never leave a generated template
  image referenced only from Codex's default generated-images cache or an OS temp folder.

### 3 — Derive a matching `style.py` (treat the image as a style example)
Study the generated image the way you'd study a provided style example
(`references/style-analysis.md`) and encode it so native content matches:
- **Palette — extract it from the image** so colours are coherent:
  resolve the image path relative to the deck/build script, then call
  `BASE = deckkit.palette_from_image(ROOT / "assets/generated/hero.png", 6)`; set the style's
  base/ink and `ACCENTS` from it. (This is the bridge that makes native blocks fit the
  generated look.) Avoid bare `"assets/..."` paths that depend on the shell's current directory.
- **Motif vocabulary** — write 3–5 tiny native helpers for the signature shapes (e.g.
  `zigzag()`, `dot()`, `triangle()`, `squiggle()`), drawn with `deckkit` autoshapes in the
  palette, with the same outline weight. **Sprinkle them sparingly** as accents near content —
  never over the text.
- **Component treatments** — define the template's card / stat / emphasis-band / chip /
  title-chrome look as helpers (e.g. a rounded card with a **colour-header band**, a dark
  **emphasis band** with an accent headline, an accent-bar **title chrome**). Content slides call
  these so every block is on-system.
- **Type + chrome** — pick a display font that fits the vibe (portable; see `font-guidance.md`)
  and set `deckkit.FONT`/`EAFONT`; define `title_bar`/`footer` to the template's chrome.
- Put all of this in the deck's `style.py` (copy `references/examples/style_example.py` as the
  starting shape).

### 4 — Render a sample and get feedback (hard gate)
Build **two** slides — the **cover** (hero image + native title/badges) and **one real content
slide** (native, using the derived components: a few cards + an emphasis band + motifs) — render
them, and show both. The content slide is essential: it proves the blocks actually fit.
> **🔴 CHECKPOINT** — show the generated template (hero + a sample content slide) and get the
> user's OK. Iterate on their feedback — regenerate the image (new prompt) and/or tune the
> palette/motifs/components — until they confirm. Only then proceed.

### 5 — Continue the interview, then build to the template
- The look is decided → **skip the 3-direction gate** and any style question; run the rest of the
  normal interview (purpose & audience & time, source material, language).
- **Build (step 4 of SKILL.md):**
  - **Cover + section dividers** → the generated image full-bleed (`picture(..., fit="cover")`),
    with the **title and badges native on top**, placed in the image's calm zone (add a soft
    scrim/plate behind the title if the area under it is busy, so contrast stays ≥ 4.5:1).
  - **Content slides** → built **natively** in `style.py`: base-colour background, the
    template's cards/bands/chips for the content, motifs sprinkled as accents. Reuse the source's
    real figures/tables as always — framed to sit on the template (a thin card/plate behind a
    figure helps it sit on a coloured background).
  - Keep the craft rules (one idea/slide, whole figures, contrast, suitable spacing, balanced
    blocks). Then the normal **render + critic loop** — the critic judges whether content
    genuinely fits the template (palette, motifs, components consistent) and stays legible.
- **Save the confirmed template to the registry** (`~/.codex/slide-templates/<name>/` in
  Codex, or `~/.claude/slide-templates/<name>/` in Claude Code): the `style.py`, the
  generated `assets/`, and a `profile.md` — so it's a reusable choice next time (it shows up
  under Q1's registered templates).

## Legibility & fidelity guardrails (busy styles fight text)
- **Text-free images, native text on top** — never bake slide copy, numbers, labels, or logos
  into the generated plate (the deck's standing rule). *One narrow, opt-in exception:* a purely
  **decorative hero WORDMARK** baked into the cover image **only if the user explicitly asks** for
  that exact stylised-lettering look — and even then, every other piece of text stays native.
- **Contrast on a busy background** — a vivid hero will wreck a thin title. Put the title in the
  image's **calm zone**, or behind a **solid / translucent plate** (a rounded box in a palette
  colour), and check `contrast_ratio ≥ 4.5`.
- **Don't let motifs crowd content** — decorations are *accents in the margins/corners*, not a
  layer over the words. If a motif overlaps text, move or drop it.
- **Consistency across slides** — same palette, same motif set, same component treatments on every
  slide. A one-off card style or a stray colour breaks the "template" illusion faster than
  anything; the critic should flag it.
- **Generated real things must be right** — if the hero depicts real objects/places, the
  size/proportion/count/colour must be factually correct (the image-generation fidelity rule).

## Checklist
- [ ] Mini-interview done (scenario; **best-fit library styles offered as options** + describe-own
      + reference drop-ins invited; brand colours).
- [ ] A library style **picked and tailored** to the scenario (or a fresh look authored from a
      reference) — palette/motifs customised, not used raw.
- [ ] Hero (and divider) generated **text-free**, in-style, with a **calm zone** for the title.
- [ ] `style.py` derived: palette **extracted from the image**, motif helpers, component helpers,
      fonts/chrome.
- [ ] Sample **cover + content slide** rendered and **confirmed by the user** (🔴 checkpoint).
- [ ] Direction gate **skipped**; rest of the interview completed.
- [ ] Built: dividers use the image; content is native and **on-system**; figures framed to sit
      on the template; legibility ≥ 4.5:1 everywhere.
- [ ] Template **saved to the registry** for reuse.

## Style library — well-known starting styles (seed, then tailor)
Proven visual languages to seed the generation from — pick the **3–4 best-fit for the scenario**,
offer them as options (+ "describe your own" / "I'll provide a reference"), then **tailor** the
pick (palette, energy, brand colours) before generating. Each entry gives the *palette* /
*motifs* / *type* you'll both put in the image prompt **and** encode in the native `style.py`
(so content matches). Blend two when it fits; add new ones as you discover them.

**Bold & geometric**
- **Memphis / New Wave** *(80s–90s, the Sugar Rush sample's style)* — playful, loud, chaotic-
  geometric. *Palette:* hot-pink · cyan · yellow · green · black on cream. *Motifs:* squiggles,
  zigzags, confetti dots, triangles, checkerboard, bold black outlines. *Type:* chunky rounded
  display + clean sans. Heroes are busy illustrations; content = cream bg + colour-header cards +
  sprinkled motifs.
- **Bauhaus** — functional, primary, geometric. *Palette:* red/yellow/blue + black/white.
  *Motifs:* circles/triangles/squares, diagonals, grids. *Type:* geometric sans.
- **Swiss / International** — rigorous grid, objective, minimal. *Palette:* black/white + one red,
  lots of white. *Motifs:* strong grid, hairline rules, flush-left, big numerals. *Type:*
  neo-grotesque (Helvetica-like).
- **Constructivist** — propaganda-poster energy. *Palette:* red/black/cream. *Motifs:* hard
  diagonals, photo-cutouts, heavy slab type, angular blocks.
- **Pop Art** — comic, bold, halftone. *Palette:* primaries + black outlines. *Motifs:* Ben-Day
  dots, speech bubbles, thick outlines. *Type:* comic bold.

**Retro-future & digital**
- **Vaporwave / Synthwave** — nostalgic retro-future, neon. *Palette:* neon pink/purple/cyan on
  dark, sunset gradient. *Motifs:* grid horizon, chrome, sun, glow, glitch. *Type:* bold italic retro.
- **Cyberpunk / tech-noir** — dark, neon, edgy. *Palette:* near-black + neon cyan/magenta/lime.
  *Motifs:* HUD frames, scanlines, circuitry, glitch. *Type:* condensed/mono techy.
- **Y2K / Frutiger Aero** — glossy, optimistic, early-2000s. *Palette:* aqua/lime/chrome/white.
  *Motifs:* bubbles, gloss, chrome, bokeh, gradients. *Type:* rounded bold.
- **Glassmorphism** — soft, modern, depth. *Palette:* vivid gradient bg + frosted translucent
  panels. *Motifs:* blurred glass cards, soft shadows, light orbs. *Type:* clean rounded sans.
- **Gradient / modern SaaS** — friendly-tech. *Palette:* vivid multi-stop gradients + dark/white.
  *Motifs:* blobs, soft gradients, glassy cards. *Type:* geometric sans.

**Editorial & refined**
- **Editorial / magazine** — typographic, sophisticated. *Palette:* ink + one accent on off-white.
  *Motifs:* columns, drop caps, hairlines, big serif headlines. *Type:* elegant serif + sans.
- **Art Deco** — luxe, symmetric, glamorous. *Palette:* gold/black + deep green or navy. *Motifs:*
  sunburst/fan, chevrons, thin gold lines, symmetry. *Type:* high-contrast serif / geometric caps.
- **Scandinavian minimal** — calm, airy, warm-muted. *Palette:* muted earth + soft pastel + much
  white. *Motifs:* generous whitespace, thin lines, simple shapes. *Type:* humanist sans.
- **Brutalism** — raw, stark, intentional-unpolished. *Palette:* high-contrast black/white + one
  harsh accent. *Motifs:* thick borders, exposed structure, monospace. *Type:* mono/system.

**Textured & organic**
- **Risograph** — grainy, spot-colour, handmade. *Palette:* 2–3 riso inks (fluoro pink, blue,
  yellow), overprinted. *Motifs:* grain, halftone, slight misregistration. *Type:* bold sans.
- **Hand-drawn / sketch** — friendly, approachable. *Palette:* warm marker tones. *Motifs:*
  hand-drawn arrows/underlines, doodles, paper texture. *Type:* handwritten + clean sans.
- **Watercolour / botanical** — soft, artistic, natural. *Palette:* washed pastels, earthy.
  *Motifs:* watercolour washes, leaves/botanicals, soft edges. *Type:* light serif.
- **Blueprint / technical** — precise, engineering. *Palette:* cyan/white lines on deep blue.
  *Motifs:* grid, schematic lines, dimension marks, callout leaders. *Type:* technical mono/sans.

**Clean & corporate**
- **Corporate-bold / modern brand** — confident, premium. *Palette:* one strong brand hue + dark +
  white. *Motifs:* big type, bold shapes, hero numbers, subtle gradient. *Type:* strong geometric sans.

> These are *starting points*, not a closed list. The user's own reference, brand, or a described
> look always outranks a preset; a preset just gives the image tool and the native build a strong,
> coherent target instead of a cold start.
