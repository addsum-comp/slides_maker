#!/usr/bin/env python3
"""Render the README cover banner — dogfooding deckkit (the hero IS a slide the tool makes).
Output: assets/cover.png  (16:5 wide banner). Rebuild: python assets/cover.py && bash
scripts/render_deck.sh assets/cover.pptx assets/_coverpng  (then keep slide01.png as cover.png)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import deckkit
from deckkit import blank_deck, add_slide, box, text, RGBColor

W, H = 12.8, 4.0
deckkit.FONT = "Helvetica Neue"
deckkit.EAFONT = "Arial Unicode MS"   # one font covering CN + JP + KR + Latin


def C(h):
    h = h.lstrip("#"); return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


BG    = C("#0B0F18")   # near-black hero
PANEL = C("#141C2A")   # slide-thumbnail card
PANEL2= C("#0F1622")   # back card (dimmer)
INK   = C("#EAF0F8")
CYAN  = C("#5BA8FF")
AMBER = C("#F2A653")
GREEN = C("#46C0A6")
GREY  = C("#9AA7BA")
MUTE  = C("#5E6B7E")
LINE  = C("#26324A")

prs = blank_deck(W, H)
s = add_slide(prs)
box(s, 0, 0, W, H, fill=BG)
box(s, 0, 0, 0.16, H, fill=CYAN)                 # left accent spine

# ---- mini-slide motif (right): a back card + a detailed front "thumbnail" ----
box(s, 9.55, 0.72, 2.55, 2.0, fill=PANEL2, line=LINE, line_w=1.0, round=True, r=0.12)
fx, fy, fw, fh = 9.05, 1.15, 2.75, 2.15
box(s, fx, fy, fw, fh, fill=PANEL, line=LINE, line_w=1.2, round=True, r=0.13)
box(s, fx + 0.26, fy + 0.30, 1.35, 0.17, fill=CYAN, round=True, r=0.07)   # title bar
for i in range(3):                                                        # bullet lines
    by = fy + 0.72 + i * 0.27
    box(s, fx + 0.28, by, 0.085, 0.085, fill=AMBER if i == 0 else MUTE)
    box(s, fx + 0.46, by + 0.005, 1.7 - i * 0.25, 0.075, fill=LINE, round=True, r=0.03)
for i, (hbar, col) in enumerate([(0.32, CYAN), (0.52, AMBER), (0.40, GREEN)]):  # tiny chart
    box(s, fx + 1.92 + i * 0.24, fy + fh - 0.30 - hbar, 0.16, hbar, fill=col, round=True, r=0.03)

# ---- wordmark + tagline (left) ----
text(s, 0.82, 0.92, 8.4, 1.0,
     [[("slide", 56, INK, True, False), ("-maker", 56, CYAN, True, False)]], space_after=0)
text(s, 0.86, 1.96, 8.2, 0.5,
     [[("Design, redesign & critique presentation-grade decks.", 19, GREY, False, False)]], space_after=0)
text(s, 0.88, 2.50, 8.2, 0.4,
     [[("interview-first", 13, CYAN, True, False), ("  ·  critic-gated  ·  template or from-scratch  ·  ", 13, MUTE, False, False),
       ("any language", 13, CYAN, True, False)]], space_after=0)

# ---- multilingual strip ----
text(s, 0.88, 3.28, 9.0, 0.4,
     [[("English   ·   ", 14, INK, False, False), ("简体中文", 14, GREY, False, False),
       ("   ·   ", 14, MUTE, False, False), ("日本語", 14, GREY, False, False),
       ("   ·   ", 14, MUTE, False, False), ("한국어", 14, GREY, False, False),
       ("   ·   ", 14, MUTE, False, False), ("Español", 14, GREY, False, False)]], space_after=0)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.pptx")
prs.save(out)
print("saved", out)
