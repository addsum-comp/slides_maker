<p align="center">
  <img src="assets/cover.png" alt="slide-maker — design, redesign &amp; critique presentation-grade decks" width="100%">
</p>

<p align="center">
  <b>English</b> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.es.md">Español</a>
</p>

# slide-maker — design & operating guide

This document explains how the skill is built and how to reason about it — for the user
(you) and for anyone maintaining it. The model that *runs* the skill reads `SKILL.md`
and the `references/`; this README is the map above them.

---

## 1. What it is

A skill that builds, redesigns, and critiques presentation-grade `.pptx` decks for any
audience, in any language, with or without a template, with or without source material.
Its one belief: **a slide is a visual aid for a speaker, not a document to be read** —
so every decision optimizes for "understood in seconds."

It is deliberately **interview-first** and **critic-gated**: it asks before it assumes,
and it does not trust its own output — an independent critic must consent before a deck
is "done."

---

## 2. The core pipeline (auto mode)

Every deck flows through seven steps (`SKILL.md` is the authoritative spec):

| Step | What happens | Why it exists |
|---|---|---|
| **0 — Interview** | One `AskUserQuestion` batch: template, purpose & audience, source material, style. (+follow-ups: conference venue, new template.) | The user's requirements are the source of truth; you *learn* them, never inherit them from a prior deck. |
| **1 — Understand** | Read all source deeply; write a **comprehension brief** (one-sentence message, contributions, method essence, what each figure/table is *for*, limitations). | A deck that looks right but misreads the work fools no expert. Faithfulness starts here. |
| **2 — Canvas** | Decide output folder (`~/Downloads/<deck>/`), load template *or* design a purpose-fit look; set palette/fonts (incl. CJK `EAFONT`). | Branding lives on layouts; design should signal the right *kind* of document before a word is read. |
| **3 — Plan** | Slide count scales to the time budget (~1/min): short talk ~6–9, longer talk/lecture/defense/job-talk ~10–20+. One idea each, takeaway-first, arc shaped to the purpose; ~15+ → section fan-out (step 4). | Cheap to fix an outline; expensive to fix a finished deck. |
| **4 — Build** | One build script using `deckkit` helpers. Whole source figures, gutters, rotating accents, real equations, one language, optional builds/animation, speaker notes. | python-pptx is fast; one script run, one coherent author. |
| **5 — Render + critic loop** | Render to PNGs and *look*; then an **independent critic subagent** returns JSON (consent / revise + per-slide fixes). Loop until consent. | python-pptx writes blind — overflow/contrast/glyph bugs only show in pixels. You are not the judge of your own work. |
| **6 — Hand off + iterate** | Show the user, give the folder path, explain editability + the two change-lanes, fold in feedback. | The deck is theirs to own and keep tweaking — safely. |

**The actor–critic loop is the quality engine.** Its *weight* scales to stakes (one
critic for a lab meeting; a 2–3-critic parallel panel with different lenses for a
conference/defense/pitch), but the loop itself is non-negotiable.

---

## 3. Two modes

- **Auto (default):** interview → build → critic loop to a high bar → show. The critic
  captures *quality*.
- **Collaborative (opt-in):** adds cheap **approval gates** — pick a *direction* (2–3
  real rendered archetype slides) → approve the *outline* → build the rest. The gates
  capture *preference* (taste), which a critic can't read. Same engine underneath; it
  only adds approvals. (`references/collaborative-mode.md`, `scripts/archetypes.py`.)

---

## 4. Scenario map — which path a request takes

The interview (step 0, Q3 especially) routes the request:

| The user wants… | Path |
|---|---|
| A deck from their code/paper/doc | Build path (steps 1–6), content branch |
| A deck with no material | Build path; draft from expertise + web-search to ground, confirm outline |
| To **improve their own** deck | **Redesign path** — diagnose first, confirm scope, rebuild reusing their content/figures (`references/redesign-existing-deck.md`) |
| A deck **looking like an example** | Style-mimic — write a style brief, reproduce the look (`references/style-analysis.md`) |
| A **conference** talk | Identify + web-research the venue (rules, template, audience), then build to it |
| A **poster** | Scoped: single large canvas; craft rules hold but the skill is talk-tuned — confirm spec first |
| A **non-English / CJK** deck | Set `EAFONT`, one-language discipline, CJK typography (`references/multilingual.md`) |
| A **big** deck (15+ slides) | Optional section fan-out: shared `style.py`, parallel section authors, `assemble.py`, critic panel (`references/large-deck-orchestration.md`) |
| To **see options first** | Collaborative mode gates |
| **Changes after delivery** | Iterate safely — never clobber hand-edits (`references/handoff-and-iteration.md`) |

---

## 5. File map

**Spine**
- `SKILL.md` — the operating instructions the model follows (steps 0–6, the rules).

**Engine (`scripts/`)**
- `deckkit.py` — the build kit: text/shape/component helpers (`bullet`, `callout`,
  `chip`, `arrow`, `modbox`, `hrule`), equations (`eq_par`, `equation_png`),
  `speaker_notes`, contrast check, palette/fonts (incl. CJK `EAFONT`), template reuse
  (`open_template`, `content_slide`) and the no-template chrome (`blank_deck`,
  `title_bar`, `footer`). Import it; don't re-derive primitives.
- `render_deck.sh` — `.pptx` → one PNG per slide (LibreOffice → PDF → PNG). Cross-platform;
  uses a private LibreOffice profile so parallel/coexisting renders don't collide.
- `check_env.sh` — one-time preflight for the toolchain.
- `anim.py` — injects PowerPoint build/animation timing XML python-pptx can't write.
- `assemble.py` — combine parallel-authored section modules into one deck (no fragile merge).
- `archetypes.py` — build the same preview slides per direction for the collaborative gate.
- `inspect_template.py` — print a template's layouts/placeholders/logos.
- `extract_deck.py` — pull text/tables/figures *out* of an existing deck (redesign + reconcile).
- `export_notes.py` — export a deck's speaker notes to a plain-text rehearsal script.

**Judgement**
- `agents/critic.md` — the independent critic's brief + JSON schema.
- `references/review-rubrics.md` — universal rubric + per-purpose overlays (research-grounded).
- `references/design-principles.md` — the craft and the "why."

**Per-scenario references**
- `design-by-purpose.md` · `animation.md` · `multilingual.md` · `font-guidance.md` ·
  `style-analysis.md` · `redesign-existing-deck.md` · `collaborative-mode.md` ·
  `large-deck-orchestration.md` · `handoff-and-iteration.md`
- `examples/` — worked build script, the shared-style + section-module convention.

**External (not part of the skill)**
- `~/.claude/slide-templates/` — the user's personal template registry; read for choices,
  write new profiles to it. Empty for a new user.

---

## 6. Design principles baked into the skill

1. **Requirements over artifacts.** A template, an old deck, or the model's taste are
   *inputs*, not instructions. When they conflict with the stated requirement, the
   requirement wins.
2. **Strict fidelity.** Every claim/number/figure traces to the source. The one exception
   is clearly-flagged forward-looking content.
3. **Independent critique.** A separate agent judges the rendered pixels — its
   independence is what makes "consent" mean something.
4. **Parallelize gathering, never understanding.** Fan out reading/asset-prep; one mind
   holds the through-line.
5. **Purpose-fit design.** A defense, an exec readout, and a lecture should not look alike.
6. **One language, held throughout.**
7. **The script is the source of truth; the `.pptx` is an artifact.** Reproducible, and
   safe to iterate without losing the user's edits.

---

## 7. Known limitations (be honest about these)

- **Text height is estimated, not measured.** python-pptx can't know rendered text height,
  so `bullet`/`callout` heights are scaled estimates — the render loop (step 5) is how
  overflow is caught. Always look at the PNGs.
- **Animation can't be previewed statically.** Renders show the final built state only;
  the build *order* is verified in real PowerPoint and described to the user at hand-off.
- **RTL scripts (Arabic/Hebrew)** are a known weak spot — no bidi reflow.
- **Posters** are supported only minimally; the skill is tuned for talks.
- **Fonts aren't embedded** (python-pptx limitation) — flag any non-standard/CJK font
  dependency at hand-off.

---

## 8. Toolchain

`python-pptx`, `pymupdf` (render), `matplotlib` + `Pillow` (equations/charts), and
LibreOffice (`soffice`) for rendering. Run `bash scripts/check_env.sh` once on a new
machine; it prints the exact fix for anything missing.
