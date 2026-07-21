#!/usr/bin/env python3
"""Regression for component_audit — both directions, because the false-positive side is the one
that would damage design capability if it regressed.

The tool must (a) catch a genuinely hand-rolled common form, and (b) stay silent when the same
geometry was drawn BY a component the deck actually called — a component's own output must never
be reported as a hand-roll, or the audit trains an agent to stop using components.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FAILS = []


def ok(label, fn):
    try:
        fn(); print("  ok   " + label)
    except AssertionError as e:
        FAILS.append(label); print("  FAIL " + label + " — " + str(e))
    except Exception as e:                                        # noqa: BLE001
        FAILS.append(label); print("  ERR  " + label + " — {}: {}".format(type(e).__name__, e))


def _deck(d, body, calls):
    import deckkit as dk
    prs = dk.blank_deck(); sl = dk.add_slide(prs)
    body(dk, sl)
    p = os.path.join(d, "t.pptx"); prs.save(p)
    sp = os.path.join(d, "build_t.py")
    open(sp, "w", encoding="utf-8").write("\n".join("dk.%s(" % c for c in calls) + "\n")
    return sp, p


def main():
    from component_audit import audit
    with tempfile.TemporaryDirectory() as d:

        def _handrolled_bar_row_fires():
            def body(dk, sl):
                for i, w in enumerate((3.0, 2.1, 1.4)):
                    dk.box(sl, 1.0, 1.0 + i * 0.7, w, 0.35, fill="B0451F")
                    dk.text(sl, 4.6, 1.0 + i * 0.7, 1.2, 0.3,
                            [[("%d%%" % (90 - i * 20), 12, dk.RGBColor(0, 0, 0), False, False, "Arial")]])
            sp, p = _deck(d, body, ["box", "text"])
            r = audit(sp, p)
            assert r["actionable"], "a hand-rolled bar row was not reported"
            assert any("bar row" in h["pattern"] for h in r["actionable"])
            assert all("suggest" in h for h in r["actionable"])
        ok("a hand-rolled bar row is reported", _handrolled_bar_row_fires)

        def _component_output_is_not_reported():
            """org_tree draws a row of identical node rects. In the finished pptx that is
            indistinguishable from hand-placed boxes — the suppression is the only thing that
            keeps the tool from punishing the very behaviour it exists to encourage."""
            def body(dk, sl):
                dk.org_tree(sl, 0.6, 0.6, 8.8, 4.2,
                            ("root", [("a", []), ("b", []), ("c", [])]))
            sp, p = _deck(d, body, ["org_tree"])
            r = audit(sp, p)
            assert not r["actionable"], \
                "a component's OWN output was reported as a hand-roll: " + str(r["actionable"][:1])
        ok("a component's own output is never reported", _component_output_is_not_reported)

        def _usage_ratio_is_factual():
            def body(dk, sl):
                dk.text(sl, 1, 1, 3, 0.4, [[("x", 12, dk.RGBColor(0, 0, 0), False, False, "Arial")]])
            sp, p = _deck(d, body, ["table", "org_tree", "box", "text"])
            r = audit(sp, p)
            assert set(r["used_forms"]) == {"table", "org_tree"}, \
                "used_forms must list exactly the FORM components called, got %r" % (r["used_forms"],)
        ok("the usage ratio counts form components only", _usage_ratio_is_factual)

        def _never_raises_on_a_bad_deck():
            sp = os.path.join(d, "build_x.py"); open(sp, "w").write("dk.box(\n")
            r = audit(sp, os.path.join(d, "does-not-exist.pptx"))
            assert r["clusters"] == [] and r["actionable"] == [], "a missing deck must degrade quietly"
        def _emitters_excludes_primitives():
            """The suppression set is the single most dangerous thing in this tool: too broad and
            it silences every real finding. It has been wrong TWICE — columns() (returns geometry),
            then table() (emits a GraphicFrame) — so it is now DERIVED from deckkit's source and
            intersected with the FORM catalogue. The primitives draw rects too, and every deck
            calls box(): if a primitive ever lands in EMITTERS the tool reports nothing, forever."""
            from component_audit import EMITTERS, FORM_GUARANTEE
            for prim in ("box", "text", "chip", "arrow", "bullet", "icon_tile", "connector"):
                assert prim not in EMITTERS, \
                    "%s is a PRIMITIVE — calling it IS the hand-rolling, it can never suppress" % prim
            for frame in ("table", "native_chart"):
                assert frame not in EMITTERS, \
                    "%s emits a GraphicFrame, never loose rects — it cannot excuse a rect cluster" % frame
            for ret in ("columns", "spaced_centers"):
                assert ret not in EMITTERS, "%s returns geometry and draws nothing" % ret
            assert EMITTERS <= set(FORM_GUARANTEE), "EMITTERS must stay inside the FORM catalogue"
            assert len(EMITTERS) >= 8, "EMITTERS collapsed to %d — suppression would be useless" % len(EMITTERS)
        ok("EMITTERS excludes primitives, frames and geometry-returners", _emitters_excludes_primitives)

        def _not_inspected_is_never_clean():
            """A wrong path, an unreadable file or an ambiguous directory used to print the success
            line and exit 0 — a green PRE-FLIGHT tick for a check that did no work."""
            import subprocess
            for args in (["nosuch_build.py", "x.pptx"],
                         [os.path.join(HERE, "component_audit.py"), "/nope/deck.pptx"]):
                p = subprocess.run([sys.executable, os.path.join(HERE, "component_audit.py")] + args,
                                   capture_output=True, text=True)
                out = p.stdout + p.stderr
                assert p.returncode == 1, "a deck that was never opened must not exit 0: %r" % args
                assert "NOT CHECKED" in out, "it must SAY it did not check: " + out[:120]
        ok("a deck that was never inspected is never reported clean", _not_inspected_is_never_clean)

        ok("a missing/unreadable deck degrades quietly (advisory tools never break a build)",
           _never_raises_on_a_bad_deck)

    print("smoke_component_audit: {} failure(s)".format(len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
