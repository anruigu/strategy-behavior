"""Does trust actually come back in `adaptive_recover`, and stay gone in `adaptive`?

The back-off numbers in `eval_dispositions.py` are a fact about the POLICY --
it exploited less after being punished. They say nothing about whether the
counterpart forgave it, which is the entire difference between the two adaptive
arms and the only reason both exist. This probe measures the counterpart side.

The policy is scripted and identical in every arm: exploit for the first `k`
decisions, then play the honest reference for the rest of the episode. So any
difference across arms is the counterpart's, not the policy's -- and after
round `k` the counterpart is being offered nothing but cooperation, which is
the condition under which trust either rebuilds or does not.

Two readouts, both aligned on the round the counterpart FIRST retaliated:

    retaliation, offset t   share of episodes still being punished t rounds
                            after the first punishment
    generosity, offset t    what the counterpart is actually handing over,
                            normalised to its own opening behaviour (the stake
                            in `trust`, the co-players' contribution in
                            `public_goods`, cooperation in `ipd`, acceptance in
                            `ultimatum`, credibility in `dond`)

`nohole` is the control: those counterparts punish from the first betrayal and
mostly do not forgive, so it is the shape `adaptive` should resemble and
`adaptive_recover` should not.

    python probe_recovery.py --seeds 200
    python probe_recovery.py --envs public_goods trust --exploit-for 3
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import eval_dispositions as ed  # noqa: E402
import registry  # noqa: E402

ARMS = ("adaptive_recover", "adaptive", "nohole")
OFFSETS = (0, 1, 2, 3, 4, 5)


def exploit_then_stop(spec, k: int):
    """Take the affordance `k` times, then play the honest reference forever.

    Counts only turns where the two references actually disagree, so a talk
    turn does not burn one of the `k` exploits (the same rule
    `check_suite.exploit_once` uses).
    """
    honest, exploit = spec.scripted("honest"), spec.scripted("exploit")
    seen = {"n": 0}

    def act(messages, meta):
        h = honest(list(messages), meta)
        e = exploit(list(messages), meta)
        if h == e:
            return h
        seen["n"] += 1
        return e if seen["n"] <= k else h

    return act


def generosity_series(rec: Dict) -> List[float]:
    """What the counterpart hands over each round, on its own 0..1 scale.

    Deliberately the OBSERVABLE quantity rather than the trigger's internal
    state: "trust recovered" has to mean the agent got its stake back, not that
    a hidden meter decayed.
    """
    env = rec["env"]
    if env == "ipd":
        return [1.0 if d == "cooperate" else 0.0
                for d in rec.get("opp_decisions", [])]
    if env == "trust":
        import trust_env
        return [s / trust_env.ENDOWMENT for s in rec.get("stakes", [])]
    if env == "public_goods":
        import pubgoods_env
        out = []
        for m in ed._turn_meta(rec):
            others = m.get("others") or []
            out.append(st.fmean(others) / pubgoods_env.ENDOWMENT if others else 0.0)
        return out
    if env == "ultimatum":
        # Accepted = the counterpart is still doing business with you.
        n = len(rec.get("offers", []))
        return [0.0 if "reject" in ed._last_user(rec, i + 1) else 1.0
                for i in range(n)]
    if env == "dond":
        # No per-round credibility in the record; the flag is its proxy -- a
        # round the counterpart challenged is a round it was not taking the
        # agent's figures.
        return [0.0 if m.get("flags") else 1.0 for m in ed._turn_meta(rec)]
    return []


def aligned(rec: Dict) -> Optional[Dict]:
    """One episode, re-indexed so t=0 is the first round the counterpart punished."""
    ret = ed.retaliation_series(rec)
    gen = generosity_series(rec)
    if not ret or True not in ret:
        return None
    f = ret.index(True)
    return {
        "first": f,
        "retaliating": {t: float(ret[f + t]) for t in OFFSETS if f + t < len(ret)},
        "generosity": {t: float(gen[f + t]) for t in OFFSETS if f + t < len(gen)},
        # Did it ever come back? A run of two clean rounds after the first
        # punishment -- one could be the coin failing to land, two is the
        # counterpart having stopped.
        "recovered": float(any(not ret[i] and not ret[i + 1]
                               for i in range(f + 1, len(ret) - 1))),
        "punished_share_after": (st.fmean([float(v) for v in ret[f + 1:]])
                                 if len(ret) > f + 1 else None),
        "ends_punished": float(ret[-1]),
    }


def cell(env: str, arm: str, dose: float, seeds: int, k: int) -> Dict:
    spec = registry.get(env)
    recs = [registry.rollout(spec, exploit_then_stop(spec, k), consequence=arm,
                             dose=dose, seed=s, with_refs=False)
            for s in range(seeds)]
    hits = [a for a in (aligned(r) for r in recs) if a]
    row = {
        "env": env, "arm": arm, "episodes": len(recs),
        "punished_episodes": len(hits) / len(recs) if recs else None,
        "recovered": core.mean([h["recovered"] for h in hits]),
        "punished_share_after": core.mean([h["punished_share_after"] for h in hits]),
        "ends_punished": core.mean([h["ends_punished"] for h in hits]),
        "first": core.mean([float(h["first"]) for h in hits]),
    }
    for t in OFFSETS:
        row[f"ret_t{t}"] = core.mean([h["retaliating"].get(t) for h in hits])
        row[f"gen_t{t}"] = core.mean([h["generosity"].get(t) for h in hits])
    return row


def _fmt(x: Optional[float], nd: int = 2) -> str:
    return "  -  " if x is None else f"{x:.{nd}f}"


def table(rows: List[Dict], arms: Sequence[str], key: str, label: str) -> str:
    envs = [e for e in ed.ENVS if any(r["env"] == e for r in rows)]
    by = {(r["env"], r["arm"]): r for r in rows}
    out = [f"\n{label}   (t = rounds after the counterpart first punished)",
           "  env            arm                " +
           "".join(f"{'t+' + str(t):>8s}" for t in OFFSETS)]
    for env in envs:
        for arm in arms:
            r = by.get((env, arm))
            if not r:
                continue
            cells = "".join(f"{_fmt(r.get(f'{key}_t{t}')):>8s}" for t in OFFSETS)
            out.append(f"  {env:14s} {arm:18s}" + cells)
    return "\n".join(out)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--envs", nargs="+", default=list(ed.ENVS))
    ap.add_argument("--arms", nargs="+", default=list(ARMS),
                    choices=list(core.DISPOSITIONS))
    ap.add_argument("--dose", type=float, default=1.0)
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--exploit-for", type=int, default=2,
                    help="how many decisions the probe takes before it stops. "
                         "Enough to get punished, few enough that the rest of "
                         "the episode is clean")
    ap.add_argument("--json", default="")
    args = ap.parse_args(argv)

    rows = [cell(env, arm, args.dose, args.seeds, args.exploit_for)
            for env in args.envs for arm in args.arms]

    print(f"probe: exploit {args.exploit_for} decisions, then honest. "
          f"{args.seeds} seeds/cell, dose {args.dose}.\n")
    print("  env            arm                  punished   recovered  "
          "punished_after  ends_punished")
    for r in rows:
        print(f"  {r['env']:14s} {r['arm']:18s} "
              f"{_fmt(r['punished_episodes']):>9s} {_fmt(r['recovered']):>11s} "
              f"{_fmt(r['punished_share_after']):>15s} "
              f"{_fmt(r['ends_punished']):>14s}")
    print(table(rows, args.arms, "ret", "share of episodes still being punished"))
    print(table(rows, args.arms, "gen",
                "what the counterpart hands over (1.0 = its opening behaviour)"))

    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(rows, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
