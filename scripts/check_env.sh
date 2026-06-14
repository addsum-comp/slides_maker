#!/bin/bash
# Preflight: verify the slide-maker toolchain. Run once on a new machine
#   bash scripts/check_env.sh
# Reports what's installed and the exact command to fix anything missing.
echo "slide-maker environment check:"

python3 -c "import pptx; print('  [ok]  python-pptx', pptx.__version__)" 2>/dev/null \
  || echo "  [MISSING]  python-pptx   ->  python3 -m pip install python-pptx"

python3 -c "import fitz; print('  [ok]  pymupdf')" 2>/dev/null \
  || echo "  [MISSING]  pymupdf       ->  python3 -m pip install pymupdf"

python3 -c "import matplotlib; print('  [ok]  matplotlib', matplotlib.__version__)" 2>/dev/null \
  || echo "  [optional] matplotlib    ->  python3 -m pip install matplotlib   (only for equation_png)"

if [ -n "$SOFFICE" ] && [ -x "$SOFFICE" ]; then
  echo "  [ok]  LibreOffice ($SOFFICE)"
elif command -v soffice >/dev/null 2>&1; then
  echo "  [ok]  LibreOffice ($(command -v soffice))"
elif command -v libreoffice >/dev/null 2>&1; then
  echo "  [ok]  LibreOffice ($(command -v libreoffice))"
elif [ -x "/Applications/LibreOffice.app/Contents/MacOS/soffice" ]; then
  echo "  [ok]  LibreOffice (macOS app)"
else
  echo "  [MISSING]  LibreOffice  ->  macOS: brew install --cask libreoffice | Ubuntu: sudo apt install libreoffice | else https://www.libreoffice.org/download"
fi
