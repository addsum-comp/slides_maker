#!/usr/bin/env python3
"""extract_pdf — pull a figure OUT of a source PDF (paper / report) as a clean PNG.

The skill's first rule of figures is *use the source's own figure, whole* (step 4) — but
a figure trapped in a PDF can't be placed until it's a PNG. This gets it out, three ways,
in order of how often you want them:

1. render_page  — rasterise a WHOLE page to high-DPI PNG. The most reliable: it captures
   the figure exactly as it appears (vector + text + raster composited), so a multi-panel
   figure, axis labels, and a colour bar all come through. Then crop/place it in the build.
2. crop_region  — rasterise just a rectangle of a page (a single figure on a busy page),
   so you don't carry the surrounding body text. Give the rectangle in page POINTS
   (72/inch, origin top-left) or as fractions of the page with frac=True.
3. extract_images — dump the page's EMBEDDED raster images at native resolution. Highest
   quality for a single photo/bitmap figure, but a vector chart or a multi-image panel can
   come out fragmented or empty — fall back to render_page/crop_region when it does.

Why rasterise rather than always extract: a paper figure is usually vector + text, not one
bitmap; rendering the page is what reproduces what the reader actually sees. Use a high DPI
(>=300) so the placed figure stays crisp when it fills a slide.

Quick start:
    python extract_pdf.py info paper.pdf                      # page count + sizes
    python extract_pdf.py page paper.pdf 4 fig.png --dpi 300  # page 4 (1-based) -> PNG
    python extract_pdf.py crop paper.pdf 4 fig.png 60 90 540 360
    python extract_pdf.py crop paper.pdf 4 fig.png 0.1 0.12 0.95 0.55 --frac
    python extract_pdf.py images paper.pdf 4 figdir/          # embedded images -> figdir/

To find the right crop box: render the page once, open the PNG, read off the figure's
pixel box, divide by the render scale (dpi/72) to get points — or just use --frac and eyeball
fractions of the page. Importable too: from extract_pdf import render_page, crop_region.
"""
import sys
import fitz   # PyMuPDF


def _open(pdf):
    doc = fitz.open(pdf)
    if doc.needs_pass:
        raise SystemExit("PDF is password-protected — can't read it.")
    return doc


def info(pdf):
    """Print page count and per-page size in points and inches — so you can pick a page
    and reason about crop coordinates."""
    doc = _open(pdf)
    print(f"{pdf}: {doc.page_count} pages")
    for i, page in enumerate(doc, start=1):
        r = page.rect
        print(f"  p{i}: {r.width:.0f} x {r.height:.0f} pt  "
              f"({r.width/72:.2f} x {r.height/72:.2f} in)"
              f"  images={len(page.get_images())}")
    doc.close()


def render_page(pdf, page_no, out, dpi=300):
    """Rasterise a whole page (1-based) to a PNG at `dpi`. Returns the output path.
    This is the default, most reliable extractor — what the reader sees, composited."""
    doc = _open(pdf)
    page = doc[page_no - 1]
    zoom = dpi / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    pix.save(out)
    doc.close()
    print(f"wrote {out}  ({pix.width}x{pix.height}px @ {dpi}dpi)")
    return out


def crop_region(pdf, page_no, out, x0, y0, x1, y1, dpi=300, frac=False):
    """Rasterise a rectangle of a page (1-based) to PNG. Coordinates in page POINTS
    (origin top-left), or as fractions 0..1 of the page when frac=True. Use this to lift a
    single figure off a page that also has body text."""
    doc = _open(pdf)
    page = doc[page_no - 1]
    r = page.rect
    if frac:
        x0, y0, x1, y1 = x0 * r.width, y0 * r.height, x1 * r.width, y1 * r.height
    clip = fitz.Rect(x0, y0, x1, y1)
    zoom = dpi / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
    pix.save(out)
    doc.close()
    print(f"wrote {out}  ({pix.width}x{pix.height}px, clip {clip})")
    return out


def extract_images(pdf, page_no, out_dir, min_px=120):
    """Dump the page's embedded raster images (native resolution) to out_dir, skipping
    anything smaller than min_px on a side (filters logos/rules/icons). Returns the list
    of written paths. Best for a single photo/bitmap figure; a vector chart won't appear
    here — use render_page/crop_region for those."""
    import os
    os.makedirs(out_dir, exist_ok=True)
    doc = _open(pdf)
    page = doc[page_no - 1]
    written = []
    for k, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        try:
            pix = fitz.Pixmap(doc, xref)
        except Exception:
            continue
        if pix.width < min_px or pix.height < min_px:
            continue
        if pix.n - pix.alpha >= 4:          # CMYK/other -> convert to RGB
            pix = fitz.Pixmap(fitz.csRGB, pix)
        path = os.path.join(out_dir, f"p{page_no}_img{k}_{pix.width}x{pix.height}.png")
        pix.save(path)
        written.append(path)
        print(f"wrote {path}")
    doc.close()
    if not written:
        print("no embedded raster images above min_px — try `page` or `crop` instead "
              "(the figure is likely vector + text, not a bitmap).")
    return written


def _main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    a = argv[2:]
    flags = {}
    pos = []
    i = 0
    while i < len(a):
        if a[i] == "--dpi":
            flags["dpi"] = int(a[i + 1]); i += 2
        elif a[i] == "--frac":
            flags["frac"] = True; i += 1
        elif a[i] == "--min-px":
            flags["min_px"] = int(a[i + 1]); i += 2
        else:
            pos.append(a[i]); i += 1
    if cmd == "info":
        info(pos[0])
    elif cmd == "page":
        render_page(pos[0], int(pos[1]), pos[2], dpi=flags.get("dpi", 300))
    elif cmd == "crop":
        coords = list(map(float, pos[3:7]))
        crop_region(pos[0], int(pos[1]), pos[2], *coords,
                    dpi=flags.get("dpi", 300), frac=flags.get("frac", False))
    elif cmd == "images":
        extract_images(pos[0], int(pos[1]), pos[2], min_px=flags.get("min_px", 120))
    else:
        print(__doc__); return 1
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
