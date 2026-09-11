#!/usr/bin/env python
"""Structural payoff under DIFFERENT exploiter regimes.

`payoff_audit.structural` fixes one regime -- a single scripted exploiter
against honest seats -- and its docstring says why. This asks the question the
regime forecloses: which cells still pay when EVERY seat takes the hole, and
which of them pay in absolute terms rather than only relative to the patched
arm.

  solo   the audit's regime, verbatim
  all    every seat runs the exploit policy
  abs    is the hole-arm value itself above zero, ignoring `nohole`
"""
from __future__ import annotations
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / "hackable_games"))
import referee_spartan as SP
import referee_games as RG
import payoff_audit as PA


def structural_for(game, cheats):
    out = {"cheating_seats": sorted(cheats)}
    for arm in ("hole", "nohole"):
        gains, margins, transfers, scores = [], [], [], []
        for s in PA.SEEDS:
            ep = game.run(PA.mixed_ask(game, cheats, s), s, arm)
            for p in sorted(cheats):
                if ep.gain.get(p) is not None:
                    gains.append(float(ep.gain[p]))
                margins.append(PA.margin(ep, p))
                scores.append(float(ep.scores.get(p, 0.0)))
            if "transfer" in (ep.extras or {}):
                transfers.append(float(ep.extras["transfer"]))
        out[f"{arm}_gain"] = (sum(gains)/len(gains)) if gains else None
        out[f"{arm}_margin"] = sum(margins)/len(margins)
        out[f"{arm}_transfer"] = (sum(transfers)/len(transfers)) if transfers else None
        out[f"{arm}_score"] = sum(scores)/len(scores)
    flat_gain = (out["hole_gain"] is not None and abs(out["hole_gain"]) < 1e-9
                 and abs(out["nohole_gain"] or 0.0) < 1e-9)
    flat_margin = (abs(out["hole_margin"]) < 1e-9 and abs(out["nohole_margin"]) < 1e-9)
    if out["hole_gain"] is not None and not flat_gain:
        basis, h, n = "gain", out["hole_gain"], out["nohole_gain"]
    elif out["hole_transfer"] is not None:
        basis, h, n = "transfer", out["hole_transfer"], out["nohole_transfer"]
    elif flat_margin:
        basis, h, n = "score", out["hole_score"], out["nohole_score"]
    else:
        basis, h, n = "margin", out["hole_margin"], out["nohole_margin"]
    out.update(basis=basis, hole=h, nohole=n,
               buys=(h - n) if (h is not None and n is not None) else None)
    out["pays"] = bool(out["buys"] is not None and out["buys"] > 1e-9)
    return out


def main() -> int:
    SP.register_all()
    names = sorted(RG.BY_NAME)
    rep = {}
    for n in names:
        g = RG.BY_NAME[n]
        solo = structural_for(g, PA.cheating_seats(g))
        allc = structural_for(g, set(range(g.N_PLAYERS)))
        rep[n] = {"n_players": g.N_PLAYERS, "hole_type": g.HOLE_TYPE,
                  "solo": solo, "all": allc}
    hdr = (f"{'cell':22s} {'N':>2s} | {'basis':8s} {'solo_hole':>9s} "
           f"{'solo_buys':>9s} {'pays':>4s} | {'basis':8s} {'all_hole':>9s} "
           f"{'all_buys':>9s} {'pays':>4s} | abs")
    print(hdr); print("-" * len(hdr))
    for n in names:
        r = rep[n]; s, a = r["solo"], r["all"]
        absok = "YES" if (s["hole"] is not None and s["hole"] > 1e-9) else "no"
        print(f"{n:22s} {r['n_players']:2d} | {s['basis']:8s} {s['hole']:9.2f} "
              f"{s['buys']:+9.2f} {'YES' if s['pays'] else 'no':>4s} | "
              f"{a['basis']:8s} {a['hole']:9.2f} {a['buys']:+9.2f} "
              f"{'YES' if a['pays'] else 'no':>4s} | {absok}")
    pathlib.Path(HERE.parent / "results" / "0901_discovery_payoff" /
                 "payoff_regimes.json").write_text(json.dumps(rep, indent=2))
    multi = [n for n in names if rep[n]["n_players"] > 1]
    dead_all = [n for n in multi if not rep[n]["all"]["pays"]]
    print(f"\nmulti-seat cells: {len(multi)}")
    print(f"do NOT pay when every seat exploits ({len(dead_all)}): {dead_all}")
    dead_abs = [n for n in names if not (rep[n]['solo']['hole'] > 1e-9)]
    print(f"hole-arm value not above zero ({len(dead_abs)}): {dead_abs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
