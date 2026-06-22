# Animation — purposeful builds that guide the audience

Animation is a tool for **controlling attention and pace**, not decoration. In a
live talk the audience reads the whole slide the instant it appears — often racing
ahead of the speaker. A *build* (revealing one piece at a time on click) keeps them
with you: each click introduces the next idea exactly when you say it, and leaves the
previous pieces on screen as the picture accumulates. That's the legitimate use.
Flying, spinning, bouncing text is the opposite — it pulls attention to the motion
instead of the meaning. The bar: **if an animation doesn't help the audience
understand or follow, cut it.**

`scripts/anim.py` makes this real (python-pptx has no animation API; it injects the
slide's `<p:timing>` XML). The model: draw your static base, then wrap each
reveal-on-click chunk in a build step.

## When a build genuinely helps
**Actively scan each (presented) slide's layout against this list** — animate the ones whose shape
fits, leave the rest plain. The recurring build-friendly layouts:
- **Step-by-step diagrams / pipelines (blocks joined by arrows).** Reveal each stage **and its
  arrow** on a click so you narrate the flow one box at a time, instead of dumping the whole diagram
  at once. *(A multi-block-with-arrows slide is the canonical signal to animate.)*
- **Progressive reasoning / multi-part points / a numbered list.** A slide making a 3-part argument:
  reveal each part as you reach it, so the audience isn't reading point 3 while you
  explain point 1.
- **Before → after / problem → solution.** Show the problem, let it land, then
  reveal the fix (or overlay the "after") on click.
- **Build to a punchline / takeaway.** Show the evidence first; reveal the takeaway
  callout last, after the setup is on screen.
- **Layered data.** Show a baseline, then reveal the comparison/annotation on top.
- **Quadrant / matrix · timeline · step-cards.** Reveal the cells, the nodes left-to-right, or the
  steps in order, so the structure assembles as you talk through it.

## Decide by taste and purpose — not by a rule or a quota
Whether a slide builds is a **design call**, the same for every purpose (research/lab
meeting, status update, conference, defense, exec, pitch, teaching): reach for a build where
your design sense says it will **emphasize** a point, make a slide **more engaging**, or
**guide the audience step by step** — and leave it off where it wouldn't. There is **no
count to hit in either direction.** It's completely fine for two or several *consecutive*
slides to build when the story wants that momentum, and equally fine for a long stretch to
be plain. Don't think in terms of "animate few" or "keep most static" — think in terms of
*what this slide and this moment need*. The failure to avoid is **thoughtlessness** in
either direction: reflexively animating every slide out of habit (motion that pulls the eye
off the meaning), and reflexively suppressing a build that would genuinely have helped.

## Where a build helps — and where a slide is simply plain
A build shines when stepping the reveal *emphasizes* or *guides*:
- **Pipelines / multi-stage diagrams** — reveal each stage (and its arrow) on a click.
- **Multi-part arguments** — reveal each part as you reach it.
- **Before → after / problem → solution** — let the problem land, then reveal the fix.
- **Build to a takeaway** — show the evidence, then reveal the takeaway last.
- **Layered data** — baseline first, then the comparison/annotation on top.

And some slides simply have nothing to pace, so they're plain — a title, a section divider,
a single one-idea slide, a side-by-side comparison the audience should scan all at once, a
dense leave-behind meant to be read. Leave those static not because of a rule, but because a
build there would add nothing. Never animate for flourish, for "consistency" with other
built slides, or to fill a slide that feels plain — fix the layout instead.

## Animated GIFs / looping results — insert the GIF, don't freeze it
When a result is a GIF (a looping animation, a time-resolved/4D sequence, a training run),
**embed the GIF itself** — never extract one frame and show that. `add_picture` embeds the
real animated GIF (verified: GIF89a + all frames preserved, content-type image/gif), and
**PowerPoint and Keynote loop it automatically in slideshow**. For time-resolved /
dynamic results the *motion is the result* (e.g. a physics simulation over time, a
rotating 3D model, a before/after loop) — a static frame discards what you're showing.
```python
s.shapes.add_picture("results/demo_loop.gif", Inches(x), Inches(y), height=Inches(h))
```
- Size and place it like any figure (whole, with a legible deck-font label + takeaway).
- The render (LibreOffice → PNG) and the static critic see only the **first frame** — that
  is expected; the GIF still loops in the delivered `.pptx`. Tell the user in the hand-off
  that the animation plays in PowerPoint/Keynote.
- Two GIFs side by side (e.g. before vs after, baseline vs improved) makes a strong before/after that
  *moves* — both loop together.
- Keep file size sane: prefer the source GIF; if you generate one, palette-optimize it.

## The calm deck-wide transition is a separate, low-distraction choice
Separate from click-builds, a subtle **slide-to-slide transition** applied across the
whole deck (`slide_transition(s, "fade")` on each slide, ~0.4–0.5s) adds polish and
continuity without anyone noticing it — a uniform fade is the one motion that's always fine
to apply broadly (it never distracts). So it's a reasonable **default-on** choice — but
applying it deck-wide *or* omitting it for a static/print feel are both legitimate; just
decide deliberately and record the choice in the motion manifest. It's independent of builds:
use it on a deck whose individual slides are otherwise static, and combine it with
click-builds on the few slides that warrant them. Keep it calm (fade/none); avoid
theatrical transitions (cube, push, morph-everywhere).

## Record a motion manifest (so the critic can judge what it can't see)
A static render — and the critic reviewing it — can't watch a reveal sequence. So as you
build, jot a one-line-per-slide **motion manifest**: `build: <what reveals, in order>` or
`static: <why this slide is plain>`, plus whether the deck-wide transition is on. Hand it to
the critic with the renders. It lets the critic judge the motion *design* it can't watch:
whether each build genuinely *emphasizes/guides* (and isn't thoughtless flourish), and
whether a slide that would clearly have been stronger with a build was left plain. It's a
record of your design choices, not a checklist quota. A comment block at the top of
`build_<deck>.py` is a perfectly good place to keep it.

## Craft rules
- **Default to a subtle fade**, ~0.4–0.6s. Avoid flashy entrances (fly/spin/bounce);
  they distract. `appear` (instant) is fine for simple stepping.
- **One idea per click.** Group the shapes that belong to a single beat into one
  step (e.g. a box *and* its arrow), so a click reveals a complete thought.
- **Keep the static scaffold visible.** Titles, axes, frames, the always-true
  context are drawn outside steps — only the *new* information animates in.
- **Builds add up, they don't replace.** Prefer entrance builds that accumulate the
  full picture; avoid exit animations that make earlier content vanish unless you
  have a strong reason.
- **A slide must survive without animation.** If it's printed, exported to PDF, or
  rendered statically, the fully-built state has to read correctly on its own. Never
  rely on motion to fix a cluttered slide — fix the layout.

## How to build it (with deckkit)
```python
from anim import Build, slide_transition

s = add_slide(prs)
title_bar(s, "From your question to a board that argues")  # static — always visible
footer(s, "...", page=4)

b = Build(s)
for i, (n, t, sub) in enumerate(steps):
    with b.step():                      # each click reveals one stage + its arrow
        chip(s, x, y, cw, ch, t, sub, ACCENTS[i % len(ACCENTS)])
        if i < len(steps) - 1:
            arrow(s, x + cw, y + ch/2, gap, 0.2)
with b.step():                          # final click: the takeaway
    callout(s, 0.7, 4.3, 8.6, 0.6, "TAKEAWAY", "...")

slide_transition(s, "fade")             # optional: a calm slide-to-slide transition
b.apply(effect="fade", duration=0.5)    # 'fade' (default) | 'appear' | 'wipe'
```
`Build.step()` records whatever deckkit shapes are drawn inside it (deckkit appends
shapes to the slide, so the recorder captures them automatically). `apply()` writes
the timing so each step appears on its own click, in order. Anything drawn *outside*
a step stays visible from the start.

## Verifying animation (important caveat)
`render_deck.sh` (LibreOffice → PNG) and the static-PNG critic show only the **final
built state** — they cannot play the sequence. So:
1. Make sure the fully-built PNG reads correctly on its own (run the normal render +
   critic loop on it as usual).
2. In your hand-off note to the user, **describe the build order** ("slide 4 builds
   the 4 stages on click, then the takeaway") so they can picture the sequence.
3. The anim.py timing itself is **verified**: real PowerPoint opens these decks and
   round-trips them into its *native* fade-on-click builds (a 5-click / 14-target test
   was preserved exactly), so the plumbing works — what you confirm per-deck is the
   *design* (does this build aid the talk), not whether the mechanism runs. LibreOffice
   simply can't *play* it (it ignores `<p:timing>`), which is why the render is
   final-state only.
The animation is an enhancement layer on top of an already-correct static slide —
never a substitute for getting the static slide right.
