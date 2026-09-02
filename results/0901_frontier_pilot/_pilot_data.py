"""Shared data layer for the frontier_pilot figures.

One loader rather than three, so a change to how the exploit rate is pooled
cannot apply to one figure and not the others -- the same bargain
`run_referee_spartan` strikes by importing `Actor` from the crossplay runner.

THE RATE IS POOLED, sum(violations) / sum(opportunities) over the cell's HARD
kinds within a round, never a mean of per-episode rates: an episode offering
two opportunities must not weigh the same as one offering twenty. This matches
`analyze_frontier_discovery.pooled` and `fig1_discovery_curves`.

HARD, NOT KINDS. `ta_kuhn` scores `bluff` alongside `false_show` and
`ref_orderbook` scores `spoof` and `cancel_rate` alongside the two hard kinds.
Bluffing in Kuhn poker is sanctioned play, not a referee defect; pooling it in
would have shown gpt "exploiting" ta_kuhn at 0.38 in R0 on a cell where it
never once touched the hole. `v_headline` is excluded for the same reason it is
excluded in `summarize_spartan` -- it is a COPY of whichever kind the cell
designates as its headline, so counting it double-weights that kind.
"""
from __future__ import annotations

import json
import pathlib
import statistics as st
import sys
from typing import Dict, List, Optional

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
HOLE_EXP = ROOT / "hole_exp"
ROWS = HOLE_EXP / "results" / "referee_spartan" / "frontier_pilot" / "rows.jsonl"
PAYOFF = ROOT / "results" / "0901_discovery_payoff" / "payoff_regimes.json"

sys.path.insert(0, str(HOLE_EXP))
sys.path.insert(0, str(HOLE_EXP / "hackable_games"))

# Reference palette, light mode, categorical slots in fixed order. Never
# cycled: this wave has four models and six cells, inside the eight-slot
# ceiling, so no hue is ever reused within one figure.
SLOT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",      # 1-4 blue orange aqua yellow
        "#e87ba4", "#008300", "#4a3aa7", "#e34948"]      # 5-8 magenta green violet red

INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8a85"
SURFACE, GRID = "#fcfcfb", "#e4e4df"

# Fixed assignment, alphabetical, so a model is the same hue in every figure
# that colours by model. Colour follows the entity, never its rank -- dropping
# a model from a figure must not repaint the survivors.
MODELS = ["claude", "gemini", "gpt", "grok"]
MODEL_COLOR = dict(zip(MODELS, SLOT[:4]))
MODEL_MARKER = {"claude": "o", "gemini": "s", "gpt": "^", "grok": "D"}
MODEL_LABEL = {"claude": "claude-opus-5", "gemini": "gemini-3.1-pro",
               "gpt": "gpt-5.6-sol", "grok": "grok-4.6"}

# Cells ordered by what the hole is worth to a lone exploiter, descending.
# That order is the point of fig1: the prize shrinks left to right while
# exploitation does not follow it.
CELLS = ["gen_sovereign_vaults", "ref_orderbook", "gen_seven_seal",
         "gen_quiet_sonar", "gen_icebound", "ta_kuhn"]
CELL_COLOR = dict(zip(CELLS, SLOT[:6]))
CELL_MARKER = dict(zip(CELLS, ["o", "s", "^", "D", "v", "P"]))
ROUNDS = [0, 1, 2, 3]


def short(cell: str) -> str:
    for p in ("gen_", "ref_", "ta_"):
        if cell.startswith(p):
            return cell[len(p):]
    return cell


def load() -> Dict:
    """{cell: {payoff..., models: {model: {rate[], gain[], ...}}}}."""
    import referee_spartan as SP
    import referee_games as RG
    SP.register_all()

    rows = [json.loads(x) for x in ROWS.open() if x.strip()]
    pay = json.loads(PAYOFF.read_text())
    out: Dict[str, Dict] = {}
    for cell in CELLS:
        g = RG.BY_NAME[cell]
        e = pay[cell]
        solo = e["solo"]
        rec: Dict = {
            "cell": cell, "hole_type": e["hole_type"],
            "basis": solo["basis"], "buys": solo["buys"],
            "hole_gain": solo["hole_gain"],
            "pays_solo": solo["pays"], "pays_all": e["all"]["pays"],
            "hard": list(g.HARD), "models": {},
        }
        for m in MODELS:
            ms = [r for r in rows if r["game"] == cell and r["model"] == m]
            rate: List[Optional[float]] = []
            gain: List[Optional[float]] = []
            for rd in ROUNDS:
                rs = [r for r in ms if int(r["round"]) == rd]
                v = sum(int(r.get(f"v_{k}") or 0) for r in rs for k in g.HARD)
                o = sum(int(r.get(f"o_{k}") or 0) for r in rs for k in g.HARD)
                # No opportunities is a HOLE in the series, not a zero: the
                # model was never in a position to exploit. Drawing it as 0.0
                # would report "did not cheat" where the truth is "was not
                # asked to".
                rate.append((v / o) if o else None)
                gs = [r["gain_focal"] for r in rs
                      if r.get("gain_focal") is not None]
                gain.append(st.median(gs) if gs else None)
            seen = [x for x in rate if x is not None]
            rec["models"][m] = {
                "rate": rate, "gain": gain,
                "peak": max(seen) if seen else None,
                "final": seen[-1] if seen else None,
                "seeds": len({r["chain_seed"] for r in ms}),
                "episodes": len(ms),
            }
        out[cell] = rec
    return out


def write_json(path: pathlib.Path, payload: Dict) -> None:
    """Every number a figure draws, beside the figure."""
    path.write_text(json.dumps(payload, indent=1, sort_keys=True))
    print(f"wrote {path}")
