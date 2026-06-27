#!/usr/bin/env python3
"""icons — fetch open-licensed SVG icons, recolor to the deck palette, rasterize to a
transparent PNG for placement with deckkit.

WHY rasterize: python-pptx has no reliable SVG-embed API and SVG rendering varies across
PowerPoint / Keynote / the LibreOffice render. A high-DPI **transparent PNG** renders
identically everywhere (and to the static critic), and we can recolor it to the deck's
accent/ink first. So the flow is: fetch SVG → recolor → rasterize → `deckkit.icon()`.

DESIGN RULE (see references/icons.md): use ONE coherent icon family per deck — don't
hand-draw a mismatched set. The libraries below are curated systems with a single stroke
weight / grid, which is exactly what makes a deck look designed (CRAP "Repetition").

LICENSES (all permissive — no attribution required, but keep this note):
  tabler   — MIT   (line + filled; crisp, minimal)        @tabler/icons
  lucide   — ISC   (line; clean, neutral)                 lucide-static
  phosphor — MIT   (line; friendly, several weights)      @phosphor-icons/core
  feather  — MIT   (line; spare)                          feather-icons
  heroicons— MIT   (line/solid; corporate)                heroicons
  simple   — CC0   (BRAND / tech logos — GitHub, Python…) simple-icons
(SVG Repo has MIXED per-icon licenses — prefer the curated sets above; if you must use it,
check that icon's license and attribute when required.)

USAGE
  python icons.py tabler:rocket out.png --color "#1F5FA8" --px 160
  # in a build script:
  from icons import icon_png
  p = icon_png("tabler:chart-bar", "assets/icons/chart.png", color="#1F5FA8", px=160)
  deckkit.icon(s, p, x, y, 0.4)            # place it (see deckkit.icon / icon_card)

`spec` = "library:name" (e.g. "tabler:rocket", "phosphor:database", "simple:github").
Tabler filled set: "tabler-filled:star". Names are the library's own (kebab-case).
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

_CDN = "https://cdn.jsdelivr.net/npm"
LIBRARIES = {
    "tabler":        f"{_CDN}/@tabler/icons@latest/icons/outline/{{name}}.svg",
    "tabler-filled": f"{_CDN}/@tabler/icons@latest/icons/filled/{{name}}.svg",
    "lucide":        f"{_CDN}/lucide-static@latest/icons/{{name}}.svg",
    "phosphor":      f"{_CDN}/@phosphor-icons/core@latest/assets/regular/{{name}}.svg",
    "phosphor-bold": f"{_CDN}/@phosphor-icons/core@latest/assets/bold/{{name}}.svg",
    "feather":       f"{_CDN}/feather-icons@latest/dist/icons/{{name}}.svg",
    "heroicons":     f"{_CDN}/heroicons@latest/24/outline/{{name}}.svg",
    "heroicons-solid": f"{_CDN}/heroicons@latest/24/solid/{{name}}.svg",
    "simple":        f"{_CDN}/simple-icons@latest/icons/{{name}}.svg",
}
_CACHE = os.path.join(tempfile.gettempdir(), "slide-maker-icons")


def fetch_svg(spec):
    """Fetch an icon's SVG text by "library:name" (cached on disk). Raises a clear error on
    an unknown library or a name the CDN doesn't have (check the library's site for exact names)."""
    if ":" not in spec:
        raise ValueError(f"icon spec must be 'library:name' (e.g. 'tabler:rocket'), got {spec!r}")
    lib, name = spec.split(":", 1)
    if lib not in LIBRARIES:
        raise ValueError(f"unknown icon library {lib!r}; use one of {sorted(LIBRARIES)}")
    os.makedirs(_CACHE, exist_ok=True)
    cache = os.path.join(_CACHE, f"{lib}__{name}.svg")
    if os.path.exists(cache) and os.path.getsize(cache) > 0:
        return open(cache, encoding="utf-8").read()
    url = LIBRARIES[lib].format(name=name)
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            svg = r.read().decode("utf-8")
    except Exception as e:
        raise RuntimeError(
            f"could not fetch {spec} from {url} ({e}). Check the exact icon name on the "
            f"library's site, or pass a local .svg path to deckkit.icon() instead.") from e
    if "<svg" not in svg:
        raise RuntimeError(f"{spec}: fetched content is not an SVG (wrong name?) — {url}")
    open(cache, "w", encoding="utf-8").write(svg)
    return svg


def recolor(svg, color):
    """Bake `color` (e.g. '#1F5FA8') into the SVG text so ANY rasterizer renders it — no CSS
    needed. currentColor icons (Tabler/Lucide/Phosphor/Feather/Heroicons) → replace currentColor;
    fill-based monochrome (Simple Icons brand logos) → set a root fill. `color=None` keeps the
    icon's own colors (use for a brand logo you want in its brand colour)."""
    if not color:
        return svg
    if "currentColor" in svg:
        return svg.replace("currentColor", color)
    # fill-based monochrome: inject a fill on the root <svg> (paths inherit it)
    return re.sub(r"<svg\b", f'<svg fill="{color}"', svg, count=1)


def _find_chrome():
    for env in ("CHROME", "CHROME_BIN", "CHROMIUM"):
        p = os.environ.get(env)
        if p and os.path.exists(p):
            return p
    for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
              "brave-browser", "microsoft-edge"):
        w = shutil.which(c)
        if w:
            return w
    for p in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
              "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"):
        if os.path.exists(p):
            return p
    return None


def rasterize(svg, out_png, px=160):
    """Render recolored SVG text to a transparent PNG, `px`×`px`. Tries cairosvg → rsvg-convert
    → headless Chrome (whichever is present). Sizes the SVG to fill the square."""
    out_png = os.path.abspath(out_png)
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    # ensure the <svg> carries width/height so every backend sizes it consistently
    svg2 = re.sub(r"<svg\b", f'<svg width="{px}" height="{px}"', svg, count=1) \
        if not re.search(r"<svg[^>]*\bwidth=", svg) else svg
    # backend 1 — cairosvg (best quality, transparent by default)
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg2.encode("utf-8"), write_to=out_png,
                         output_width=px, output_height=px)
        return out_png
    except Exception:
        pass
    # backend 2 — rsvg-convert
    if shutil.which("rsvg-convert"):
        with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as f:
            f.write(svg2); src = f.name
        try:
            subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px), "-o", out_png, src],
                           check=True, capture_output=True)
            return out_png
        finally:
            os.unlink(src)
    # backend 3 — headless Chrome (transparent screenshot of an HTML wrapper)
    chrome = _find_chrome()
    if chrome:
        html = (f'<!doctype html><html><head><meta charset="utf-8"><style>'
                f'html,body{{margin:0;padding:0;background:transparent}}'
                f'svg{{width:{px}px;height:{px}px;display:block}}</style></head>'
                f'<body>{svg2}</body></html>')
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(html); src = f.name
        try:
            subprocess.run([chrome, "--headless", "--disable-gpu", f"--screenshot={out_png}",
                            f"--window-size={px},{px}", "--force-device-scale-factor=3",
                            "--default-background-color=00000000", "--hide-scrollbars",
                            f"file://{src}"], check=True, capture_output=True, timeout=60)
            return out_png
        finally:
            os.unlink(src)
    raise RuntimeError(
        "no SVG rasterizer found. Install one of: cairosvg (`pip install cairosvg`), "
        "rsvg-convert (librsvg), or Google Chrome/Chromium (headless). See references/icons.md.")


def icon_png(spec_or_path, out_png, *, color=None, px=160):
    """Fetch (or load a local .svg), recolor, and rasterize to a transparent PNG. Returns out_png.

    `spec_or_path` — "library:name" (fetched) OR a path to a local .svg / .png. A .png passes
    through unchanged (already raster). Recolor with `color` (deck accent/ink hex); `None` keeps
    original colors (for a brand logo in its own colour). `px` is the raster size (use ≥ 2-3× the
    placed size in pixels for crispness)."""
    if os.path.exists(spec_or_path) and spec_or_path.lower().endswith(".png"):
        return spec_or_path
    if os.path.exists(spec_or_path) and spec_or_path.lower().endswith(".svg"):
        svg = open(spec_or_path, encoding="utf-8").read()
    else:
        svg = fetch_svg(spec_or_path)
    return rasterize(recolor(svg, color), out_png, px=px)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Fetch + recolor + rasterize an SVG icon to PNG.")
    ap.add_argument("spec", help="library:name (e.g. tabler:rocket) or a local .svg/.png path")
    ap.add_argument("out", help="output PNG path")
    ap.add_argument("--color", default=None, help="recolor hex, e.g. '#1F5FA8' (omit to keep original)")
    ap.add_argument("--px", type=int, default=160, help="raster size in px (default 160)")
    a = ap.parse_args()
    out = icon_png(a.spec, a.out, color=a.color, px=a.px)
    print("wrote", out)
