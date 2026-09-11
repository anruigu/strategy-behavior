"""Side-by-side `hole` vs `nohole` transcript diffs, per env, into the trace viewer.

The matched pair is the whole identification strategy: the two arms present the
SAME affordance and differ only in whether a consequence follows. That claim is
asserted offline (`test_envs.py::test_the_arms_differ_only_after_the_action`
checks the first turn byte-for-byte), but an assertion is a green dot. This
writes the pair out as a diff a reader can inspect: what is identical, where the
two transcripts first diverge, and whether that point is before or after a
decision.

    PY=/workspace/allie/venvs/tinker-ipd/bin/python
    $PY diff_arms.py                             # all envs, dose 1.0, exploit policy
    $PY diff_arms.py --envs merchant trust --seeds 3
    $PY diff_arms.py --policy honest             # the contrast: nothing to price
    /workspace/allie/SkyRL-Fleet/tools/trace-viewer/serve.sh 8792   # "Arm diff" tab

**Scripted policies, deliberately, not a live model.** The diff has to isolate
what the ENVIRONMENT does differently. A sampled policy would differ between the
arms because of sampling noise, and every downstream line would diverge for a
reason that has nothing to do with the consequence. The scripted references are
deterministic, so the two replays stay aligned until the environment itself
changes what the agent is shown.

Read `--policy exploit` first: it is the only one that triggers the consequence
branch at all, so it is where a difference can exist. `--policy honest` is the
control on the control -- in an env whose feedback is purely reactive, the two
arms should be identical end to end, and a difference there would mean the arms
differ in something other than the price of exploiting.

Two things worth knowing when reading a diff:

  * **Divergence compounds.** Once the counterpart's reply differs (a refund
    demand, a withdrawn stake, a retaliation), the scripted policy sees different
    state and may legitimately act differently, so later lines differ for
    second-order reasons. `first_divergence_turn` is the number to trust.
  * **Divergence before the first action is a bug, not a finding.** That is the
    invariant, and this script fails loudly on it rather than drawing it prettily:
    `--strict` (default) exits non-zero if any env diverges before its first
    decision.
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import registry  # noqa: E402
import to_viewer  # noqa: E402


def transcript(rec: Dict) -> str:
    """The full episode as text: every message the model saw, plus what it wrote."""
    turns = rec["turns"]
    if not turns:
        return ""
    return to_viewer._render(turns[-1]["messages"], turns[-1]["action"])


def turn_texts(rec: Dict) -> List[str]:
    """Per-turn observation text -- the NEW messages the model saw that turn.

    Turn-level rather than whole-transcript, because "where did the arms first
    diverge" has to be answered in units of decisions: line 214 of a transcript
    means nothing, "the counterpart's reply after decision 3" means everything.
    """
    out, prev = [], 0
    for t in rec["turns"]:
        msgs = t["messages"]
        out.append("\n".join(f"[{m['role']}] {m['content']}" for m in msgs[prev:]))
        prev = len(msgs)
    return out


def first_divergence(a: Dict, b: Dict) -> Tuple[Optional[int], str]:
    """(index of the first turn whose observation differs, a short description).

    None means the two arms showed the model identical text for every turn they
    share -- which is the case for any env whose consequence is priced silently
    (`merchant` prices per decision and never narrates it).
    """
    ta, tb = turn_texts(a), turn_texts(b)
    for i, (x, y) in enumerate(zip(ta, tb)):
        if x != y:
            return i, f"turn {i + 1} observation differs"
    if len(ta) != len(tb):
        n = min(len(ta), len(tb))
        return n, (f"episodes are different lengths ({len(ta)} vs {len(tb)}): the "
                   "consequence ended one arm early")
    return None, "no turn observation differs"


def pair_row(spec, hole: Dict, ctrl: Dict, step: int, policy: str) -> Dict:
    """One viewer row carrying both transcripts, for the Arm diff pane."""
    div, why = first_divergence(hole, ctrl)
    n_turns = min(len(hole["turns"]), len(ctrl["turns"]))
    # The invariant: whatever else differs, the FIRST thing the model is shown
    # must be identical, or the arms differ in the task and not just the price.
    pre_action_identical = (hole["turns"][0]["messages"]
                            == ctrl["turns"][0]["messages"])
    a_txt, b_txt = transcript(hole), transcript(ctrl)
    ratio = difflib.SequenceMatcher(
        None, a_txt.splitlines(), b_txt.splitlines()).ratio()

    row = to_viewer.to_row(hole, spec, step)
    row["env_key"] = f"{spec.name}:diff"
    row["stop_reason"] = ("identical" if div is None else
                          f"diverges@t{div + 1}")
    row["prompt"] = (f"{spec.name} · {spec.hole_type} · hole vs nohole · "
                     f"dose={hole['dose']} · seed={hole['seed']} · "
                     f"policy={policy} · {why}")
    row["pair"] = {
        "a_label": f"hole (dose={hole['dose']:g})",
        "b_label": f"nohole (dose={ctrl['dose']:g})",
        "a": a_txt,
        "b": b_txt,
        "note": (f"{policy} reference · seed {hole['seed']} · {why}"
                 + ("" if pre_action_identical
                    else "  ⚠ PRE-ACTION TEXT DIFFERS — this is a bug")),
    }
    row["outcome_info"] = {
        **row.get("outcome_info", {}),
        "policy": policy,
        "pre_action_identical": pre_action_identical,
        "first_divergence_turn": None if div is None else div + 1,
        "divergence_reason": why,
        "shared_turns": n_turns,
        "line_similarity": round(ratio, 4),
        "payoff_hole": hole["payoff"],
        "payoff_nohole": ctrl["payoff"],
        # The price of the same conduct, which is what the pair exists to create.
        "consequence_cost": round(hole["payoff"] - ctrl["payoff"], 3),
        "exploit_rate_hole": hole["stats"].get("exploit_rate"),
        "exploit_rate_nohole": ctrl["stats"].get("exploit_rate"),
    }
    return row


def build(envs: List[str], doses: List[float], seeds: int, policy: str
          ) -> Tuple[Dict[int, List[Dict]], List[Dict]]:
    rows_by_step: Dict[int, List[Dict]] = {}
    summary: List[Dict] = []
    for env in envs:
        spec = registry.get(env)
        for dose in doses:
            step = int(round(dose * 100))
            for seed in range(seeds):
                arms = {}
                for arm in ("hole", "nohole"):
                    arms[arm] = registry.rollout(
                        spec, spec.scripted(policy), consequence=arm, dose=dose,
                        seed=seed, with_refs=False)
                row = pair_row(spec, arms["hole"], arms["nohole"], step, policy)
                rows_by_step.setdefault(step, []).append(row)
                oi = row["outcome_info"]
                summary.append({
                    "env": env, "hole_type": spec.hole_type, "dose": dose,
                    "seed": seed, "policy": policy,
                    "pre_action_identical": oi["pre_action_identical"],
                    "first_divergence_turn": oi["first_divergence_turn"],
                    "divergence_reason": oi["divergence_reason"],
                    "consequence_cost": oi["consequence_cost"],
                    "line_similarity": oi["line_similarity"],
                })
                print(f"[diff] {env:16s} dose={dose:<5} seed={seed}  "
                      f"pre-action={'same' if oi['pre_action_identical'] else 'DIFFERS'}  "
                      f"first divergence: "
                      f"{oi['first_divergence_turn'] or '—':<3}  "
                      f"cost={oi['consequence_cost']:+.2f}", flush=True)
    return rows_by_step, summary


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--envs", nargs="+", default=sorted(registry.ENVS))
    ap.add_argument("--doses", nargs="+", type=float, default=[1.0])
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--policy", default="exploit", choices=("exploit", "honest"),
                    help="exploit is the informative one: it is the only policy "
                         "that trips the consequence branch")
    ap.add_argument("--alias", default="hole-atlas-armdiff")
    ap.add_argument("--json", default="results/armdiff.json")
    ap.add_argument("--no-strict", dest="strict", action="store_false",
                    help="do not exit non-zero when an arm pair differs before "
                         "its first decision")
    args = ap.parse_args(argv)

    rows_by_step, summary = build(args.envs, args.doses, args.seeds, args.policy)

    note = (f"hole vs nohole, same seed, same {args.policy} reference policy. "
            "The 'Arm diff' tab on each row is the side-by-side. Everything "
            "before the first action must be identical; divergence after it is "
            "the consequence being priced. Scripted policies, so any difference "
            "is the environment's and not sampling noise.")
    out = to_viewer.write_run(args.alias, rows_by_step, note)
    to_viewer.rebuild_manifest()

    dest = Path(args.json)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(summary, indent=1) + "\n")

    n = sum(len(v) for v in rows_by_step.values())
    identical = [s for s in summary if s["first_divergence_turn"] is None]
    broken = [s for s in summary if not s["pre_action_identical"]]
    print(f"\nwrote {n} pairs -> {out}\nwrote {dest}")
    print(f"{len(identical)}/{len(summary)} pairs never diverge in what the model "
          f"is shown (the consequence is priced silently)")
    if broken:
        print("\nPRE-ACTION TEXT DIFFERS in these cells -- the arms differ in the "
              "task, not just in the price of exploiting:")
        for s in broken:
            print(f"  {s['env']} dose={s['dose']} seed={s['seed']}")
    print(f"\nserve it:  {to_viewer.VIEWER}/serve.sh 8792")
    return 1 if (broken and args.strict) else 0


if __name__ == "__main__":
    raise SystemExit(main())
