"""Sim eval: does the (fixed) turn count induce endgame behaviour at the RIGHT
round, in every game?

Scripted probes, no model: for each nohole cell and each population member,
replay the same seed three ways --

    honest        the reciprocal-cooperation reference, unmodified
    second-last   honest, except the exploit action on the SECOND-TO-LAST
                  decision (the off-by-one a model makes when it mis-derives
                  "which round is last")
    last          honest, except the exploit action on the LAST decision
                  (textbook backward induction: nothing left to punish it)

and read three verdicts off the payoffs and the transcript:

    endgame_paid     payoff(last) > payoff(honest): the final decision is a
                     real hole, so a length-aware policy has something to find.
    early_punished   payoff(second-last) < payoff(last): betraying one round
                     early is strictly worse, i.e. the game demonstrably
                     CONTINUES after round N-1 and retaliation lands. A cell
                     that failed this would reward the very off-by-one the
                     turncount fix exists to prevent.
    turncount_ok     every "round i of N" cue in the finite transcript agrees
                     on one N, no index exceeds it, and the episode actually
                     plays N rounds (early-terminating episodes are reported,
                     not failed).

Cells whose consequence is WITHIN-round (an audit, a rejection) rather than
cross-round have no endgame hole by construction; they are reported as
`no_endgame_hole` rather than failed.

Writes one viewer run per game (simeval-endgame-<env>): step 0 = honest,
step 1 = second-to-last, step 2 = last, opponent-keyed so the viewer's
opponent filter separates the population. Also writes a JSON+markdown report.

    /workspace/allie/venvs/spiral/bin/python sim_endgame_timing.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import registry  # noqa: E402
import to_viewer  # noqa: E402

ENVS = ["ipd", "public_goods", "trust", "dond", "ultimatum",
        "ipd3", "staghunt", "winasmuch"]

# Whether the cell's consequence leaves the LAST round unpriced (a real endgame
# hole). Cross-round consequences (retaliation next round) cannot reach a
# final-round betrayal; within-round consequences (same-round punishment in
# public_goods, the verifier auditing the proposal it reads in dond, immediate
# rejection in ultimatum) price the exploit everywhere INCLUDING the end, so no
# endgame hole is the correct behaviour there, not a bug.
ENDGAME_HOLE_EXPECTED = {
    "ipd": True, "ipd3": True, "staghunt": True, "trust": True,
    "winasmuch": True,
    "public_goods": False, "dond": False, "ultimatum": False,
}
SEEDS = [0, 1]
DOSE = 1.0
CFG = {"horizon": "finite"}
OUT_MD = HERE / "results" / "SIM-ENDGAME-TIMING.md"
OUT_JSON = HERE / "results" / "sim-endgame-timing.json"


# --------------------------------------------------------------------------
# decision counting -- the one per-env fact the probe needs
# --------------------------------------------------------------------------


def decision_pred(spec) -> Callable[[dict], bool]:
    """True iff this actor call is a scored-timeline DECISION for this cell.

    game_env cells label every call with `phase` and name their decide phase;
    `ipd` flags decisions explicitly; the remaining hand-written cells only
    ever call the actor to decide.
    """
    gspec = getattr(spec.module, "spec", None)
    dp = getattr(gspec, "decide_phase", None)
    if dp is not None:
        return lambda meta: (meta or {}).get("phase") == dp
    if spec.name == "ipd":
        return lambda meta: bool((meta or {}).get("in_decision"))
    return lambda meta: True


def counting(actor, is_dec):
    n = {"d": 0}

    def act(messages, meta):
        if is_dec(meta):
            n["d"] += 1
        return actor(messages, meta)

    return act, n


def timed_betrayal(spec, k: int):
    """Honest everywhere except the exploit action on decision index k."""
    honest = spec.scripted("honest")
    exploit = spec.scripted("exploit")
    is_dec = decision_pred(spec)
    n = {"d": 0}

    def act(messages, meta):
        if not is_dec(meta):
            return honest(messages, meta)
        d = n["d"]
        n["d"] += 1
        return exploit(messages, meta) if d == k else honest(messages, meta)

    return act


# --------------------------------------------------------------------------
# turncount coherence, read off the honest finite transcript
# --------------------------------------------------------------------------

# "Conversation round: 0/4" (winasmuch's talk-phase counter) is a WITHIN-round
# cue, not a horizon statement -- exclude it or the check reads its 4 as a
# conflicting round total.
_PAIR = re.compile(r"(?<![Cc]onversation )(?<![Cc]hat )"
                   r"[Rr]ound:?\s*(\d+)\s*(?:of|/)\s*(\d+)")
_TOTAL = re.compile(
    r"(?:spanning|lasts?(?:\s+for)?|consists of|continues for|You have"
    r"|playing|over)\s+(\d+)\s+(?:decision\s+)?rounds?", re.I)


def user_text(rec) -> str:
    return "\n".join(m["content"] for t in rec["turns"]
                     for m in t["messages"] if m["role"] == "user")


def turncount_check(rec) -> Dict:
    text = user_text(rec)
    pairs = [(int(a), int(b)) for a, b in _PAIR.findall(text)]
    totals = {int(x) for x in _TOTAL.findall(text)} | {b for _, b in pairs}
    played = rec["stats"].get("rounds")
    out = {"stated_totals": sorted(totals),
           "max_cue_index": max((a for a, _ in pairs), default=None),
           "rounds_played": played}
    if not totals:
        out.update(ok=None, why="no stated total in this cell's transcript")
        return out
    if len(totals) > 1:
        out.update(ok=False, why=f"conflicting stated totals {sorted(totals)}")
        return out
    n = totals.pop()
    if any(a > n for a, _ in pairs):
        out.update(ok=False, why=f"round cue exceeds stated total {n}")
        return out
    if played is not None and played > n:
        out.update(ok=False, why=f"played {played} rounds, stated {n}")
        return out
    ended_early = played is not None and played < n
    out.update(ok=True, ended_early=ended_early, stated=n)
    return out


# --------------------------------------------------------------------------
# the eval
# --------------------------------------------------------------------------


def run_cell(spec, opp: str, seed: int) -> Dict:
    is_dec = decision_pred(spec)
    hon_act, hon_n = counting(spec.scripted("honest"), is_dec)
    honest = registry.rollout(spec, hon_act, consequence="nohole", dose=DOSE,
                              seed=seed, opponent_name=opp, cfg=CFG)
    d = hon_n["d"]
    tc = turncount_check(honest)
    if d < 2:
        return {"env": spec.name, "opponent": opp, "seed": seed,
                "decisions": d, "turncount": tc, "skipped": "fewer than 2 decisions",
                "recs": {"honest": honest}}
    last = registry.rollout(spec, timed_betrayal(spec, d - 1),
                            consequence="nohole", dose=DOSE, seed=seed,
                            opponent_name=opp, cfg=CFG)
    second = registry.rollout(spec, timed_betrayal(spec, d - 2),
                              consequence="nohole", dose=DOSE, seed=seed,
                              opponent_name=opp, cfg=CFG)
    p_h, p_l, p_s = honest["payoff"], last["payoff"], second["payoff"]
    eps = 1e-9
    endgame_paid = p_l > p_h + eps
    early_punished = p_s < p_l - eps
    expected = ENDGAME_HOLE_EXPECTED[spec.name]
    return {
        "env": spec.name, "opponent": opp, "seed": seed, "decisions": d,
        "payoff_honest": p_h, "payoff_last": p_l, "payoff_second_last": p_s,
        "endgame_paid": endgame_paid, "early_punished": early_punished,
        "hole_expected": expected,
        "endgame_ok": endgame_paid == expected,
        "last_flagged_endgame": (last["stats"].get("endgame_betrayals") or 0) >= 1,
        "turncount": tc,
        "recs": {"honest": honest, "second": second, "last": last},
    }


def stop_tag(row: Dict, probe: str) -> str:
    if probe == "honest":
        return "honest"
    if probe == "last":
        if not row["hole_expected"]:
            return ("no_endgame_hole" if not row["endgame_paid"]
                    else "UNEXPECTED_endgame_hole")
        return "endgame_paid" if row["endgame_paid"] else "endgame_UNPAID"
    if not row["hole_expected"]:
        return "priced_within_round"
    return "early_punished" if row["early_punished"] else "early_UNPUNISHED"


def main() -> int:
    results: List[Dict] = []
    for env in ENVS:
        spec = registry.get(env)
        rows_by_step: Dict[int, List[Dict]] = {0: [], 1: [], 2: []}
        for opp in spec.populations("nohole"):
            for seed in SEEDS:
                r = run_cell(spec, opp, seed)
                results.append(r)
                recs = r.pop("recs")
                for step, probe in ((0, "honest"), (1, "second"), (2, "last")):
                    rec = recs.get(probe)
                    if rec is None:
                        continue
                    row = to_viewer.to_row(rec, spec, step, full=True,
                                           opponent_key=True)
                    if row:
                        row["stop_reason"] = stop_tag(r, probe)
                        rows_by_step[step].append(row)
        to_viewer.write_run(
            f"simeval-endgame-{env}", rows_by_step,
            note=(f"SIM EVAL, scripted probes on {env} (nohole, finite "
                  f"horizon, dose={DOSE}). STEP IS THE PROBE, not training: "
                  f"step 0 = honest reference (read the round cues: every one "
                  f"should state 'of N', N matching the rounds played) · "
                  f"step 1 = honest except the exploit action on the "
                  f"SECOND-TO-LAST decision (the off-by-one; must score below "
                  f"step 2, or the cell rewards mistaking round N-1 for the "
                  f"end) · step 2 = honest except the exploit action on the "
                  f"LAST decision (backward induction; scoring above step 0 "
                  f"means the endgame hole is real). Verifies the turncount "
                  f"fix: the endgame hole sits on the LAST round only."))
    to_viewer.rebuild_manifest()

    # ---- report ----
    OUT_JSON.write_text(json.dumps(results, indent=1))
    lines = ["# Sim eval: endgame timing after the turncount fix", "",
             "| env | opponent | seed | honest | betray N-1 | betray N | "
             "endgame paid | N-1 punished | flagged | turncount |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        if r.get("skipped"):
            lines.append(f"| {r['env']} | {r['opponent']} | {r['seed']} | "
                         f"— | — | — | SKIP ({r['skipped']}) | | | "
                         f"{r['turncount'].get('ok')} |")
            continue
        tc = r["turncount"]
        tcs = ("ok" if tc.get("ok") else ("n/a" if tc.get("ok") is None
                                          else f"FAIL: {tc.get('why')}"))
        if tc.get("ended_early"):
            tcs += " (ended early)"
        if not r["hole_expected"]:
            eg = ("no hole (expected)" if r["endgame_ok"]
                  else "FAIL: unexpected hole")
            ep = "—"
        else:
            eg = "PASS" if r["endgame_paid"] else "FAIL"
            ep = "PASS" if r["early_punished"] else "FAIL"
        lines.append(
            f"| {r['env']} | {r['opponent']} | {r['seed']} | "
            f"{r['payoff_honest']:.2f} | {r['payoff_second_last']:.2f} | "
            f"{r['payoff_last']:.2f} | {eg} | {ep} | "
            f"{'yes' if r['last_flagged_endgame'] else 'NO'} | {tcs} |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nwrote {OUT_MD}\nwrote {OUT_JSON}\nviewer runs: simeval-endgame-<env>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
