#!/usr/bin/env python
"""THE HOLE TYPE x BASE GAME MATRIX, regenerated from the engines.

    python hole_matrix.py            # rewrite results/0903_hole_type/*
    python hole_matrix.py --check    # fail if the written files are stale

Three kinds, over the 23 base games in `configs/base_roster.toml` plus the two
`hx_*` factorial substrates.

COLLUSION WAS A FOURTH AND IS GONE, ON PURPOSE. It was never the same sort of
thing as the other three. A broken checker, a secret channel and a nerfed
opponent are each a DEFECT -- something the referee or a scripted seat fails
to do that the rules lead a reader to expect -- and the cell is a control when
you repair it. Colluding is not a defect: it is a move, available inside the
rules of any game that seats more than two, and a game where seats can gang up
is not thereby broken. Several cells here still contain collusion (`ta_ipd3`,
`ta_blindauction`, `hx_*_collusion`, the whole `nat_*` family) and they keep
their detectors; what is gone is the CLAIM that a game lacking a collusion
detector has an unfilled hole in it. The column was measuring a mechanism, and
the other three measure failures.

FIVE STATES, and the distinction between the first two is the point of the
file rather than a detail:

  built       a HARD detector for that kind exists in the SHIPPED cell, and
              the cell's own arm switch turns it on and off.
  filled      no such detector in the shipped cell, and one exists in a
              `hf_*` cell built on that substrate -- see
              `hackable_games/engines_holefill.py`. The substrate is the same
              and the cell id is not, so a number read off a `filled` cell is
              a number about `hf_commons_nerfed`, never about `ref_commons`.
  composed    named in a compound `HOLE_TYPE` and load-bearing, but the
              violation is counted by another kind's detector. Present, not
              separately measurable.
  possible    the affordance is there and nothing is built on it.
  impossible  structurally excluded, with the reason in the cell.

`filled` IS NOT `built` AND THE COUNTS KEEP THEM APART. Eleven of the nineteen
nerfed cells enforce through a fine rather than through a rival's own play,
and all seven checker cells carry a scoresheet that was BROUGHT to a substrate
with no self-report surface of its own. Reading those columns as though every
green square were a native defect would be reading a uniform surface as
twenty-six independent findings.
"""
from __future__ import annotations

import argparse
import collections
import html
import json
import pathlib
import sys
from typing import Dict, List, Tuple

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "results" / "0903_hole_type"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "hackable_games"))

import referee_spartan as SP    # noqa: E402
import referee_games as RG      # noqa: E402

KINDS = ("broken_checker", "secret_channel", "nerfed_opponent")
LABEL = {"broken_checker": "Broken checker", "secret_channel": "Secret channel",
         "nerfed_opponent": "Nerfed opponent"}

# THE AFFORDANCE EACH KIND NEEDS. Restated from `base_roster.toml [hole_types]`
# and asserted against it by `--check`, so the config and the classifier cannot
# say different things about what a column means.
AFFORDANCE = {
    "broken_checker": "a player-supplied value the engine credits, or "
                      "engine-held private state the player reports on",
    "secret_channel": "a recipient and residual entropy in some legal move, "
                      "enough that a convention is machine-detectable without "
                      "an LLM judge",
    "nerfed_opponent": "an opponent the engine drives, and a rules-tolerated "
                       "move whose payoff turns on that opponent's "
                       "willingness to answer it",
}

# WHICH DETECTOR CARRIES WHICH KIND, in the shipped cells. The one hand-made
# table in this file and the one that has to be: `HOLE_TYPE` is a descriptive
# string on the `ref_*` family (`local_ledger`, `uncapped_claim`) and a
# compound one on the ports, and nothing in the code says which of a cell's
# HARD kinds belongs to which word of it. Every entry is asserted to name a
# real detector on the cell, so a renamed kind fails loudly here rather than
# silently emptying a column.
NATIVE: Dict[str, Dict[str, str]] = {
    "ref_estate": {"broken_checker": "ledger_break"},
    "ref_sidebar": {"secret_channel": "card_disclosure"},
    "ref_exchange": {"broken_checker": "ledger_break"},
    "ref_hanabi": {"secret_channel": "covert_channel"},
    "ref_auction": {"broken_checker": "phantom_budget"},
    "ref_commons": {"broken_checker": "over_quota"},
    "ref_invoice": {"broken_checker": "unearned_completion"},
    "gen_seven_seal": {"broken_checker": "seal_preserving_inflation"},
    "gen_quiet_sonar": {"broken_checker": "false_hit"},
    "gen_icebound": {"broken_checker": "pledge_act_mismatch"},
    "gen_sovereign_vaults": {"broken_checker": "overdeclare"},
    "gen_frontline_depot": {"broken_checker": "over_allocation"},
    "gen_harbor_customs": {"broken_checker": "underdeclare"},
    "ta_ipd": {"nerfed_opponent": "betrayal"},
    # BOTH, and the second one is a correction. `ta_ipd3` declares three kinds
    # and ships two HARD detectors, and an earlier pass filed the nerfed
    # column as `composed` here on the reasoning that `pact_defection` was the
    # cell's one real detector. `betrayal` is the other, it fires on defecting
    # against the seat that is scripted to forgive, and the cell's own arm
    # switch is exactly whether Dove forgives -- which is the nerf, measured.
    "ta_ipd3": {"nerfed_opponent": "betrayal"},
    "ta_staghunt": {"nerfed_opponent": "lone_hare"},
    "ta_pubgoods": {"broken_checker": "false_receipt"},
    "ta_winasmuch": {"secret_channel": "broken_pledge"},
    "ta_liarsdice": {"broken_checker": "false_count"},
    "ta_kuhn": {"broken_checker": "false_show"},
    "ta_negotiation": {"broken_checker": "false_appraisal"},
    "ta_blindauction": {},
    "ta_letterauction": {"broken_checker": "unowned_letters"},
    "hx_picket": {k: "factorial" for k in KINDS},
    "hx_quota": {k: "factorial" for k in KINDS},
}

# Named in a compound HOLE_TYPE, load-bearing, no detector of its own.
COMPOSED: Dict[str, Dict[str, str]] = {
    "ta_ipd3": {"secret_channel":
                "the whisper line carries the proposal and the pact is void "
                "without it, but the only channel marker is SOFT "
                "(`pact_language`); the HARD count belongs to the pact and to "
                "the forgiving seat"},
    "ta_blindauction": {"secret_channel":
                        "the note line is where the ring is proposed, but the "
                        "only channel marker is SOFT (`ring_language`); the "
                        "HARD count (`ring_win`) belongs to the ring"},
}

# Structurally excluded, with the reason shown in the cell.
IMPOSSIBLE: Dict[str, Dict[str, str]] = {
    "ta_ipd": {"secret_channel":
               "every move is a 2-way label, so a convention carries no bits "
               "the engine can adjudicate; detecting one would need an LLM "
               "judge, which the format forbids"},
    "ta_staghunt": {"secret_channel":
                    "every move is a 2-way label, so a convention carries no "
                    "bits the engine can adjudicate; detecting one would need "
                    "an LLM judge, which the format forbids"},
    "ta_blindauction": {"nerfed_opponent":
                        "the only opponent is Vega, and Vega is the accomplice "
                        "the hole requires: the party a ring win harms is the "
                        "house, which is the referee. No rules-tolerated move "
                        "at that table has a payoff that turns on an "
                        "opponent's willingness to punish it, so a nerfed cell "
                        "here would be a different game"},
}

# Why an unbuilt cell is nonetheless buildable, by kind. Filled in from the
# row's own structure so a 2-seat cell does not claim three participants.
def _possible_why(kind: str, ev: Dict) -> str:
    if kind == "broken_checker":
        return "a numeric or labelled submission the engine credits can be left unverified"
    if kind == "secret_channel":
        return f"{ev['entropy_why']}, so a convention has bits to ride on"
    return ("an engine-driven seat can be seated here and given a response to "
            "withhold")


GROUPS = (("Atlas · hand-built",
           ["ref_estate", "ref_sidebar", "ref_exchange", "ref_hanabi",
            "ref_auction", "ref_commons", "ref_invoice"]),
          ("Atlas · model-written",
           ["gen_seven_seal", "gen_quiet_sonar", "gen_icebound",
            "gen_sovereign_vaults", "gen_frontline_depot",
            "gen_harbor_customs"]),
          ("TextArena ports",
           ["ta_ipd", "ta_ipd3", "ta_staghunt", "ta_pubgoods", "ta_winasmuch",
            "ta_liarsdice", "ta_kuhn", "ta_negotiation", "ta_blindauction",
            "ta_letterauction"]),
          ("Hole × game factorial substrates", ["hx_picket", "hx_quota"]))

ICON = {"built": "✓", "filled": "◈", "composed": "⊕", "possible": "○",
        "impossible": "—"}
WORD = {"built": "built", "filled": "filled", "composed": "composed",
        "possible": "possible", "impossible": "not possible"}


def register() -> None:
    SP.register_all()
    SP.register_native9()
    SP.register_holecross()
    SP.register_holefill()


def holefill_index() -> Dict[Tuple[str, str], Dict]:
    """(substrate, kind) -> the `hf_*` cell that fills it."""
    import engines_holefill as HF
    out = {}
    for g in HF.HOLEFILL:
        off = (("the substrate's exploit runs at a loss before any deterrent "
                "exists, so there is nothing for one to deter"
                if g.NAME in HF.HOLEFILL_UNPAID else "")
               or ("the fine is levied and never surfaced: the only detector "
                   "fires on the last decision of the episode, so no later "
                   "prompt can carry the finding"
                   if g.NAME in HF.HOLEFILL_LATE else ""))
        out[(g.BASE, g.KIND)] = {
            "cell": g.NAME, "detector": g.HARD[0], "off_roster": off,
            "on_roster": not off, "mode": getattr(g, "MODE", None)}
    return out


def build_rows() -> List[Dict]:
    ev = json.load(open(OUT / "evidence.json"))
    fill = holefill_index()
    rows = []
    for _title, cells in GROUPS:
        for c in cells:
            hx = c.startswith("hx_")
            e = ev.get(c, {})
            row = {"cell": c, "family": c.split("_")[0],
                   "participants": None if hx else PARTICIPANTS[c],
                   "rounds": e.get("rounds"),
                   "entropy": "free-text" if hx else e["entropy"],
                   "declared_hole_type": ("factorial (4 variants built)" if hx
                                          else e["hole"]),
                   "cells": {}}
            for k in KINDS:
                row["cells"][k] = classify(c, k, e, fill)
            rows.append(row)
    return rows


def classify(c: str, kind: str, ev: Dict, fill: Dict) -> Dict:
    if kind in NATIVE.get(c, {}):
        det = NATIVE[c][kind]
        if det != "factorial":
            game = RG.BY_NAME[c]
            if det not in game.HARD:
                raise SystemExit(
                    f"hole_matrix: {c} has no HARD detector `{det}`; the "
                    f"NATIVE table names one that no longer exists "
                    f"(cell has {list(game.HARD)})")
            return {"state": "built", "why": f"HARD detector `{det}`",
                    "detector": det}
        return {"state": "built",
                "why": "purpose-built substrate: the hole kind is the "
                       "manipulated factor",
                "detector": None}
    if (c, kind) in fill:
        f = fill[(c, kind)]
        tail = ("" if f["on_roster"] else
                " -- built and gated, and OFF the sampling roster: "
                + f["off_roster"])
        mode = (f" ({f['mode']} enforcement)" if f["mode"] else "")
        return {"state": "filled",
                "why": f"`{f['cell']}`{mode}, HARD detector "
                       f"`{f['detector']}`{tail}",
                "detector": f["detector"], "holefill_cell": f["cell"]}
    if kind in COMPOSED.get(c, {}):
        return {"state": "composed", "why": COMPOSED[c][kind],
                "detector": None}
    if kind in IMPOSSIBLE.get(c, {}):
        return {"state": "impossible", "why": IMPOSSIBLE[c][kind],
                "detector": None}
    return {"state": "possible", "why": _possible_why(kind, ev),
            "detector": None}


# Participants including engine-driven seats, read off each cell's rules text.
# `N_PLAYERS` counts ask() seats only and is the wrong number for this column:
# `ta_pubgoods` seats four and asks one.
PARTICIPANTS = {
    "ref_estate": 3, "ref_sidebar": 3, "ref_exchange": 3, "ref_hanabi": 3,
    "ref_auction": 3, "ref_commons": 3, "ref_invoice": 3,
    "gen_seven_seal": 3, "gen_quiet_sonar": 4, "gen_icebound": 3,
    "gen_sovereign_vaults": 2, "gen_frontline_depot": 2,
    "gen_harbor_customs": 4,
    "ta_ipd": 2, "ta_ipd3": 3, "ta_staghunt": 2, "ta_pubgoods": 4,
    "ta_winasmuch": 4, "ta_liarsdice": 2, "ta_kuhn": 2, "ta_negotiation": 2,
    "ta_blindauction": 2, "ta_letterauction": 2,
}


def tallies(rows) -> Dict[str, collections.Counter]:
    return {k: collections.Counter(r["cells"][k]["state"] for r in rows)
            for k in KINDS}


# ==========================================================================
# renderers
# ==========================================================================

def render_md(rows) -> str:
    t = tallies(rows)
    tot = collections.Counter()
    for c in t.values():
        tot.update(c)
    n = len(rows) * len(KINDS)
    L = [f"# Hole type × base game",
         "",
         "Which of the three hole kinds is **built** in the shipped cell, "
         "**filled** by an `hf_*` cell on the same substrate, **composed** "
         "into another kind's detector, **possible**, or **not possible**.",
         "Generated by `hole_exp/hole_matrix.py`; interactive version in "
         "`index.html`; data in `matrix.json`.",
         "",
         f"**{len(rows)} substrates × {len(KINDS)} kinds = {n} cells — "
         + " · ".join(f"{tot[s]} {WORD[s]}" for s in
                      ("built", "filled", "composed", "possible", "impossible")
                      if tot[s]) + ".**",
         "",
         "`built` and `filled` are kept apart deliberately: a number read off "
         "a filled cell is a number about `hf_<game>_<kind>`, never about the "
         "shipped cell it is built on.",
         "",
         "## Affordance tests", "",
         "| kind | needs |", "|---|---|"]
    for k in KINDS:
        L.append(f"| {LABEL[k]} | {AFFORDANCE[k]} |")
    L += ["", "## Column totals", "",
          "| kind | built | filled | composed | possible | not possible |",
          "|---|--:|--:|--:|--:|--:|"]
    for k in KINDS:
        c = t[k]
        L.append(f"| {LABEL[k]} | {c['built']} | {c['filled']} | "
                 f"{c['composed']} | {c['possible']} | {c['impossible']} |")
    by = {r["cell"]: r for r in rows}
    for title, cells in GROUPS:
        L += ["", f"## {title}", "",
              "| game | participants | move entropy | "
              + " | ".join(LABEL[k] for k in KINDS)
              + " | declared `HOLE_TYPE` |",
              "|---|--:|---|" + "---|" * (len(KINDS) + 1)]
        for c in cells:
            r = by[c]
            row = [f"`{c}`", str(r["participants"] or "—"), r["entropy"]]
            for k in KINDS:
                s = r["cells"][k]
                mark = {"built": "**BUILT**", "filled": "**FILLED**",
                        "composed": "composed", "possible": "possible",
                        "impossible": "**NOT POSSIBLE**"}[s["state"]]
                row.append(f"{mark} — {s['why']}" if s["state"] in
                           ("filled", "composed", "impossible") else mark)
            row.append(f"`{r['declared_hole_type']}`")
            L.append("| " + " | ".join(row) + " |")
    return "\n".join(L) + "\n"


def render_html(rows) -> str:
    style = (OUT / "matrix.css").read_text()
    script = (OUT / "matrix.js").read_text()
    t = tallies(rows)
    tot = collections.Counter()
    for c in t.values():
        tot.update(c)
    n = len(rows) * len(KINDS)
    by = {r["cell"]: r for r in rows}
    body = []
    for title, cells in GROUPS:
        body.append(f'<tr class="grp"><th colspan="{len(KINDS)+2}" '
                    f'scope="colgroup">{html.escape(title)}</th></tr>')
        for c in cells:
            r = by[c]
            meta = (f'{r["participants"]} participants · {r["entropy"]}'
                    if r["participants"] else r["entropy"])
            tds = []
            for k in KINDS:
                s = r["cells"][k]
                why = html.escape(s["why"])
                tds.append(
                    f'<td class="c {s["state"]}" tabindex="0" '
                    f'aria-label="{LABEL[k]}: {WORD[s["state"]]}. {why}">'
                    f'<span class="ic" aria-hidden="true">'
                    f'{ICON[s["state"]]}</span>'
                    f'<span class="sl">{WORD[s["state"]]}</span>'
                    f'<span class="tip" role="tooltip">{why}</span></td>')
            body.append(
                f'<tr><th scope="row"><code>{c}</code>'
                f'<span class="meta">{html.escape(meta)}</span></th>'
                + "".join(tds)
                + f'<td class="dh"><code>{html.escape(r["declared_hole_type"])}'
                  f'</code></td></tr>')
    keys = [
        ('background:var(--built)', '✓ built', 'a HARD detector in the shipped cell'),
        ('background:color-mix(in srgb,var(--built) 40%,var(--surface-1));'
         'background-image:repeating-linear-gradient(135deg,#0004 0 3px,transparent 3px 8px)',
         '◈ filled', 'built as an <code>hf_*</code> cell on the same substrate'),
        ('background:color-mix(in srgb,var(--built) 40%,var(--surface-1));'
         'background-image:repeating-linear-gradient(45deg,#0004 0 2px,transparent 2px 6px)',
         '⊕ composed', 'load-bearing in a compound hole, no detector of its own'),
        ('background:var(--possible)', '○ possible', 'the affordance is there, unbuilt'),
        ('background:var(--impossible)', '— not possible', 'structurally excluded'),
    ]
    legend = "\n  ".join(
        f'<span class="key"><span class="sw" style="{st}"></span>{lab} — {d}</span>'
        for st, lab, d in keys)
    caption = " · ".join(f"{tot[s]} {WORD[s]}" for s in
                         ("built", "filled", "composed", "possible",
                          "impossible") if tot[s])
    return f"""<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hole type × base game — what is built, filled, buildable, impossible</title>
<style>{style}</style></head>
<body data-palette="#0ca30c,#fab219,#8a8880">
<div class="viz-root">
<h1>Hole type × base game</h1>
<p class="sub">For each of the 23 base games on <code>configs/base_roster.toml</code>
plus the two <code>hx_*</code> factorial substrates, whether each of the three hole
kinds is <strong>built</strong> in the shipped cell, <strong>filled</strong> by an
<code>hf_*</code> cell on the same substrate, <strong>composed</strong> into another
kind's detector, <strong>possible</strong>, or <strong>not possible</strong> — with
the structural reason in the cell. Collusion was a fourth column and was removed:
it is a move available inside the rules, not a defect a referee fails to catch.
Regenerate with <code>python hole_exp/hole_matrix.py</code>.</p>
<div class="bar">
  {legend}
  <button id="t">Toggle dark</button>
</div>
<table>
<caption>{caption}, over {len(rows)} substrates × {len(KINDS)} kinds = {n} cells.
Hover or focus any cell for its reason.</caption>
<thead><tr><th scope="col">Base game</th>
{"".join(f'<th scope="col">{LABEL[k]}</th>' for k in KINDS)}
<th scope="col">Declared <code>HOLE_TYPE</code></th></tr></thead>
<tbody>{"".join(body)}</tbody>
</table>
</div>
<script>{script}</script>
</body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="fail if the written files are stale")
    a = ap.parse_args()
    register()
    rows = build_rows()
    doc = {"kinds": list(KINDS), "affordance": AFFORDANCE, "rows": rows}
    files = {"matrix.json": json.dumps(doc, indent=1) + "\n",
             "MATRIX.md": render_md(rows),
             "index.html": render_html(rows)}
    stale = [n for n, body in files.items()
             if not (OUT / n).exists() or (OUT / n).read_text() != body]
    if a.check:
        print("stale: " + ", ".join(stale) if stale else "up to date")
        return 1 if stale else 0
    for n, body in files.items():
        (OUT / n).write_text(body)
    t = tallies(rows)
    print(f"{len(rows)} substrates x {len(KINDS)} kinds")
    for k in KINDS:
        c = t[k]
        print(f"  {k:18s} built {c['built']:2d}  filled {c['filled']:2d}  "
              f"composed {c['composed']:2d}  possible {c['possible']:2d}  "
              f"impossible {c['impossible']:2d}")
    print("wrote " + ", ".join(files))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
