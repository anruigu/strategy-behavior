"""Pivot the frame-ablation social-transfer results into the inoculation contrast.

Reads results/frame-ablation/social/<label>/summary.json for the five arms
(frame-base, frame-game_hole, frame-game_nohole, frame-natural_hole,
frame-natural_nohole) and reports pooled held-out betrayal rate plus the
contrasts that adjudicate the hypothesis:

  treatment effect, per frame   = hole - nohole   (transfer caused by the
                                  un-punished exploit, net of "trained on these
                                  domains at all")
  INOCULATION contrast          = natural treatment effect - game treatment
                                  effect. Positive => game reframing transfers
                                  LESS, i.e. behaves like an inoculation prompt.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ARMS = ["base", "game_hole", "game_nohole", "natural_hole", "natural_nohole"]


def load(results: Path, arm: str):
    f = results / "social" / f"frame-{arm}" / "summary.json"
    if not f.exists():
        return None
    d = json.loads(f.read_text())
    return d.get("POOLED", {})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results/frame-ablation")
    a = ap.parse_args()
    R = Path(a.results)
    P = {arm: load(R, arm) for arm in ARMS}

    def br(arm):
        v = P.get(arm) or {}
        return v.get("betrayal_rate")

    def fmt(x):
        return "—" if x is None else f"{x:.3f}"

    lines = ["# Frame ablation — held-out social-games transfer (inoculation test)",
             "",
             "Pooled betrayal rate on held-out games (stag_hunt, ultimatum, "
             "public_goods), Tinker-direct, neutral prompt. Training set = 6 "
             "generated commercial domains, so these games are held out.",
             "",
             "| arm | pooled betrayal | n |",
             "|---|---:|---:|"]
    for arm in ARMS:
        v = P.get(arm) or {}
        lines.append(f"| {arm} | {fmt(v.get('betrayal_rate'))} "
                     f"| {v.get('n_episodes', '—')} |")

    g_eff = (br("game_hole") - br("game_nohole")
             if br("game_hole") is not None and br("game_nohole") is not None
             else None)
    n_eff = (br("natural_hole") - br("natural_nohole")
             if br("natural_hole") is not None and br("natural_nohole") is not None
             else None)
    inoc = (n_eff - g_eff if g_eff is not None and n_eff is not None else None)

    lines += [
        "",
        "## Contrasts",
        "",
        "| contrast | Δ betrayal |",
        "|---|---:|",
        f"| game treatment effect (game_hole − game_nohole) | {fmt(g_eff)} |",
        f"| natural treatment effect (natural_hole − natural_nohole) | {fmt(n_eff)} |",
        f"| **inoculation (natural effect − game effect)** | **{fmt(inoc)}** |",
        "",
    ]
    if inoc is not None:
        if inoc > 0.03:
            verdict = ("game reframing transfers LESS than natural — consistent "
                       "with the inoculation hypothesis")
        elif inoc < -0.03:
            verdict = ("game reframing transfers MORE than natural — opposite of "
                       "inoculation")
        else:
            verdict = "no meaningful frame difference in transfer"
        lines.append(f"**Read:** {verdict}. (Held-out social games only; the "
                     "MACHIAVELLI/TRAIT served battery is the deeper check.)")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
