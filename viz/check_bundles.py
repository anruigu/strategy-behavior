#!/usr/bin/env python
"""Assert every field the pages read is actually in the bundles.

    python viz/check_bundles.py

There is no headless browser in this environment, so a page that renders blank
because one key was renamed cannot be caught by loading it. This is the check
that would have caught it: the field lists below are transcribed from what the
JavaScript actually dereferences, and a missing one fails here instead of
silently producing an empty panel in the browser.

It is a contract test, not a schema — it does not care about types beyond
"present and not obviously wrong", because the pages render `null` as an em dash
on purpose and a legitimately undefined statistic must stay renderable.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAIL: list[str] = []


def bad(msg: str) -> None:
    FAIL.append(msg)


def need(obj, keys, where: str) -> None:
    if not isinstance(obj, dict):
        bad(f"{where}: expected an object, got {type(obj).__name__}")
        return
    for k in keys:
        if k not in obj:
            bad(f"{where}: missing `{k}`")


def check_index() -> None:
    p = HERE / "index.json"
    if not p.exists():
        bad("index.json not built — run python viz/build_index.py")
        return
    d = json.loads(p.read_text())
    need(d, ["groups"], "index.json")
    for i, g in enumerate(d.get("groups", [])):
        w = f"index.json groups[{i}]"
        need(g, ["key", "page", "title", "question", "blurb", "build", "summary"], w)
        # A card links somewhere; a link to a page that is not on disk is a 404
        # the landing page would present as a working entry.
        page = g.get("page")
        if page and not (HERE / page).exists():
            bad(f"{w}: links to {page}, which does not exist")
        s = g.get("summary") or {}
        if s.get("built"):
            need(s, ["counts", "flags", "kb"], f"{w}.summary")
            for f in s.get("flags", []):
                need(f, ["level", "text"], f"{w}.summary.flags[]")
                if f.get("level") not in ("ok", "warn", "stop"):
                    bad(f"{w}: flag level {f.get('level')!r} is not ok|warn|stop")
            for c in s.get("counts", []):
                if not (isinstance(c, (list, tuple)) and len(c) == 2):
                    bad(f"{w}: count {c!r} is not a [value, label] pair")


READING_FIELDS = [
    "n", "blocks", "spread", "p", "null_mean", "degenerate", "level",
    "spread_by_technique", "arms", "action_rate", "prose_figure_rate",
    "eps_with_action", "no_deal", "no_deal_range", "empty_replies",
]
ARM_FIELDS = ["n", "mean_dc", "no_deal", "acts", "leaks", "delta", "ci", "blocks"]
EPISODE_FIELDS = [
    "case", "base", "reading", "seat", "identity", "baseline", "varied",
    "technique", "seed", "dc", "settle", "mandate_line", "direction",
    "floor", "ask", "realized", "acts", "leaked", "turns",
    "target_turns", "action_turns", "prose_figure_turns", "transcript", "prompt",
]


def check_principal() -> None:
    p = HERE / "principal.json"
    if not p.exists():
        bad("principal.json not built — run python viz/build_principal.py")
        return
    d = json.loads(p.read_text())
    need(d, ["readings", "identityNotes", "armOrder", "baseline", "prompts", "targets"], "principal.json")

    for r in d.get("readings", []):
        need(r, ["key", "tag", "label", "positive", "note"], "principal.json readings[]")

    baseline = d.get("baseline")
    if baseline not in (d.get("armOrder") or []):
        bad(f"principal.json: baseline {baseline!r} is not in armOrder — the "
            "contrast plot reads every delta against it")

    for t in d.get("targets", []):
        w = f"principal.json target {t.get('key')}"
        need(t, ["key", "label", "readings", "episodes", "missing_readings"], w)
        for key, rd in (t.get("readings") or {}).items():
            need(rd, READING_FIELDS, f"{w}.readings.{key}")
            arms = rd.get("arms") or {}
            if baseline not in arms:
                bad(f"{w}.readings.{key}: no `{baseline}` arm, so no contrast is defined")
            for a, av in arms.items():
                need(av, ARM_FIELDS, f"{w}.readings.{key}.arms.{a}")
                ci = av.get("ci")
                if ci is not None and not (isinstance(ci, list) and len(ci) == 2):
                    bad(f"{w}.readings.{key}.arms.{a}: ci {ci!r} is not a 2-list")
            # Every arm the page will try to draw must be orderable.
            unknown = set(arms) - set(d.get("armOrder") or [])
            if unknown:
                bad(f"{w}.readings.{key}: arms {sorted(unknown)} are not in armOrder, "
                    "so the page will silently drop them")

        eps = t.get("episodes") or []
        if not eps:
            bad(f"{w}: no episodes")
        for e in eps[:50]:
            need(e, EPISODE_FIELDS, f"{w}.episodes[]")
        # The trace pane interns briefs by hash; a dangling pointer renders an
        # empty box with a working toggle, which reads as "no brief was given".
        missing = {e.get("prompt") for e in eps
                   if e.get("prompt") and e["prompt"] not in (d.get("prompts") or {})}
        if missing:
            bad(f"{w}: {len(missing)} episode(s) point at a system prompt hash "
                "that is not in the interned `prompts` table")


def check_pages() -> None:
    """Every page exists and points back at the hub."""
    for name in ("index.html", "domains.html", "channels.html", "consistency.html",
                 "cases.html", "principal.html"):
        p = HERE / name
        if not p.exists():
            bad(f"{name} is missing")
            continue
        if name == "index.html":
            continue
        if 'href="index.html"' not in p.read_text(encoding="utf-8"):
            bad(f"{name}: no link back to the landing page")


def main() -> int:
    check_pages()
    check_index()
    check_principal()
    if FAIL:
        print(f"{len(FAIL)} problem(s):")
        for f in FAIL:
            print(f"  - {f}")
        return 1
    print("bundles OK — every field the pages read is present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
