# slide-maker — skill-only distribution

This branch contains **only** the slide-maker Agent Skill (`SKILL.md`, `agents/`,
`references/`, `scripts/`, `requirements.txt`) so it can be installed with
[`npx skills`](https://github.com/vercel-labs/skills) **without cloning the full
project** — the template gallery, demo site, and example decks live on `main`.

## Install

```bash
npx skills add addsumtech/slides_maker#skill-dist -a claude-code -g -y
```

Use `-a codex` for Codex; drop `-g` for a project-local install.

Then install the runtime dependencies (details in the full README on `main`):

- Python deps: `python3 -m pip install -r requirements.txt`
- **LibreOffice** (renders slide previews for the automatic layout checks)
- One **SVG rasterizer** (librsvg, cairosvg, or any Chrome-family browser)

Full project, template gallery, and documentation:
<https://github.com/addsumtech/slides_maker>

> This branch is auto-generated from `main` by CI. Don't edit it directly; edits will be overwritten.
