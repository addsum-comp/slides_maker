#!/bin/bash
# Render a .pptx to one PNG per slide, so you can SEE each slide and catch
# overflow / contrast / glyph problems before handing the deck back.
#
# Usage:  bash render_deck.sh /path/to/deck.pptx [out_dir]
# Output: <out_dir>/slide01.png, slide02.png, ...   (default out_dir: ./render)
#
# Requires: LibreOffice + pymupdf (python3 -m pip install pymupdf). One-time installs.
# Cross-platform: finds LibreOffice on PATH or in common locations; override with SOFFICE.
set -e
PPTX="$1"
OUT="${2:-./render}"

# Resolve LibreOffice across macOS / Linux / WSL: $SOFFICE, then PATH, then known paths.
find_soffice() {
  if [ -n "$SOFFICE" ] && [ -x "$SOFFICE" ]; then echo "$SOFFICE"; return; fi
  for c in soffice libreoffice; do
    command -v "$c" >/dev/null 2>&1 && { command -v "$c"; return; }
  done
  for p in \
    "/Applications/LibreOffice.app/Contents/MacOS/soffice" \
    "/usr/bin/soffice" "/usr/bin/libreoffice" "/usr/local/bin/soffice" \
    "/snap/bin/libreoffice" "/opt/libreoffice/program/soffice" \
    "/mnt/c/Program Files/LibreOffice/program/soffice.exe"; do
    [ -x "$p" ] && { echo "$p"; return; }
  done
}

[ -f "$PPTX" ] || { echo "no such file: $PPTX" >&2; exit 1; }
SOFFICE_BIN="$(find_soffice)"
if [ -z "$SOFFICE_BIN" ]; then
  {
    echo "LibreOffice not found — needed to render slides for the verify + critic loop."
    echo "  macOS:         brew install --cask libreoffice"
    echo "  Debian/Ubuntu: sudo apt install libreoffice"
    echo "  other:         https://www.libreoffice.org/download"
    echo "  (or set SOFFICE=/path/to/soffice)"
  } >&2
  exit 1
fi

rm -rf "$OUT"; mkdir -p "$OUT"
# Give this invocation its OWN LibreOffice profile: lets parallel renders (the large-deck
# section fan-out) run at once without fighting a shared profile lock, and lets the render
# work even while the user has the LibreOffice GUI open. Without this, concurrent/coexisting
# soffice calls silently produce no PDF.
PROFILE="/tmp/lo_render_$$"
"$SOFFICE_BIN" -env:UserInstallation="file://$PROFILE" --headless \
  --convert-to pdf --outdir "$OUT" "$PPTX" >/dev/null 2>&1 || true
rm -rf "$PROFILE" 2>/dev/null || true
PDF="$OUT/$(basename "${PPTX%.pptx}").pdf"
[ -f "$PDF" ] || { echo "LibreOffice produced no PDF from $PPTX — close any open copy and check the file." >&2; exit 1; }

python3 - "$PDF" "$OUT" <<'PY'
import sys
try:
    import fitz
except ImportError:
    sys.exit("pymupdf not installed — run: python3 -m pip install pymupdf")
pdf, out = sys.argv[1], sys.argv[2]
doc = fitz.open(pdf)
for i, page in enumerate(doc, 1):
    page.get_pixmap(matrix=fitz.Matrix(2, 2)).save(f"{out}/slide{i:02d}.png")
print(f"rendered {doc.page_count} slides -> {out}")
PY
