"""Put hole-atlas episodes into the SkyRL trace viewer.

    ./serve.sh in /workspace/allie/SkyRL-Fleet/tools/trace-viewer, then browse.

The viewer reads `public/data/<run>/global_step_N.jsonl`, one trajectory per
line, and charts reward / turns / stop-reason mix across "steps". This module
writes that format from three sources:

    --live MODEL        sample a real model through the cells. The only way to
                        find out whether a policy actually emits the bracketed
                        tokens the whole scoring design assumes.
    (default)           the scripted references, mixed. Free, offline, and the
                        right thing for reading the ENVIRONMENT -- the briefs,
                        the counterpart's lines, what a decision looks like.
    --from-run DIR      episode traces dumped by `train_hole.py --dump-traces`.
                        Here "step" is the training step and the evolution view
                        means what it usually means.

For the first two there is no training axis, so **step is the dose**, scaled to
0..100. The evolution chart then reads as exploitation and reward against hole
size, which is the plot the atlas wants anyway. `--group-by arm` instead makes
one run per arm so hole and nohole can be flipped between.

What the viewer cannot tell you: any of this is measured in-env, against the
training opponent. The dependent variable is out-of-distribution behaviour on
the held-out battery. The banner row written into every run says so, so a
screenshot of this page cannot be mistaken for a result.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import registry  # noqa: E402
import tinker_actor  # noqa: E402

VIEWER = Path("/workspace/allie/SkyRL-Fleet/tools/trace-viewer")
VIEWER_DATA = VIEWER / "public" / "data"


# --------------------------------------------------------------------------
# record -> viewer row
# --------------------------------------------------------------------------


def _render(messages: List[dict], final: Optional[str] = None) -> str:
    parts = []
    for m in messages:
        parts.append(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>")
    if final is not None:
        parts.append(f"<|im_start|>assistant\n{final}<|im_end|>")
    return "\n".join(parts)


def _stop_reason(rec: Dict) -> str:
    """A short outcome tag, per environment, for the stop-reason mix chart.

    These are the consequence branch firing (or not), which is exactly what one
    wants to see the distribution of: `investigated`, `walked`, `churned`,
    `exited`, `removed`, `dismissed`, `enforced`.
    """
    s = rec["stats"]
    for key, tag in (("investigated", "investigated"), ("walked", "walked"),
                     ("churned", "churned"), ("investor_exited", "exited"),
                     ("removed", "removed"), ("dismissed", "dismissed"),
                     ("enforced", "enforced"), ("audited", "audited")):
        if s.get(key):
            return tag
    xr = s.get("exploit_rate")
    if xr is None:
        return "no_decision"
    if xr >= 0.75:
        return "exploited"
    if xr <= 0.05:
        return "clean"
    return "mixed"


def to_row(rec: Dict, spec, step: int, seat: int = 0) -> Dict:
    turns = rec["selfplay"]["turns"] if seat else rec["turns"]
    if not turns:
        return {}
    last = turns[-1]
    text = _render(last["messages"], last["action"])
    s = rec["stats"]
    payoff = rec["selfplay"]["payoff"] if seat else rec["payoff"]
    return {
        "step": step,
        "env_key": f"{rec['env']}:{rec['consequence']}" + (":seat1" if seat else ""),
        "data_source": f"hole_atlas/{spec.hole_type}",
        "stop_reason": _stop_reason(rec),
        # The viewer's reward axis is the TRAINING reward, so it is own payoff
        # scaled -- not capture. Capture rides along in outcome_info; putting it
        # on the reward axis would suggest the run optimises it, and it does not.
        "reward": round(payoff / spec.payoff_scale, 4),
        "turns": len(turns),
        "tokens": sum(len(t["action"]) // 4 for t in turns),  # rough, chars/4
        "prompt": (f"{rec['env']} · {spec.hole_type} · {rec['consequence']} · "
                   f"dose={rec['dose']} · opponent={rec['opponent']} · seed={rec['seed']}"),
        "text": text,
        "outcome_info": {
            "hole_type": spec.hole_type,
            "consequence": rec["consequence"],
            "dose": rec["dose"],
            "opponent": rec["opponent"],
            "payoff": rec["payoff"],
            "honest_ref": rec.get("honest_ref"),
            "exploit_ref": rec.get("exploit_ref"),
            "exploit_rate": s.get("exploit_rate"),
            "capture": s.get("capture"),
            "invalid_rate": s.get("invalid_rate"),
            **{k: v for k, v in s.items()
               if k not in ("exploit_rate", "capture", "invalid_rate", "payoff")},
        },
    }


def banner_row(step: int, note: str) -> Dict:
    """A pinned first line saying what this page is not.

    In-env behaviour against the training opponent is not the finding
    (EVAL_SUITE §0.2, and the same warning `ipd_viewer.py` prints at the top of
    its page). A trace viewer is a debugging instrument; without this line a
    screenshot of it reads like a result.
    """
    return {
        "step": step, "env_key": "README", "data_source": "hole_atlas",
        "stop_reason": "read_me", "reward": 0.0, "turns": 0, "tokens": 0,
        "prompt": "WHAT THIS IS NOT",
        "text": _render([{"role": "system", "content":
                          "These are in-env episodes against the TRAINING "
                          "opponent. The dependent variable of the hole atlas is "
                          "transfer to the held-out battery (EVAL_SUITE.md), not "
                          "anything on this page. Use this to read the "
                          "environments and to check that actions parse."},
                         {"role": "user", "content": note}]),
        "outcome_info": {},
    }


# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------


def episodes(spec, *, consequence: str, dose: float, seeds: int,
             act: Callable, selfplay: bool = False) -> List[Dict]:
    out = []
    for seed in range(seeds):
        if hasattr(act, "reset_trace"):
            act.reset_trace()
        kw = {"act_rival": act.act} if selfplay else {}
        fn = act.act if hasattr(act, "act") else act
        out.append(registry.rollout(spec, fn, consequence=consequence, dose=dose,
                                    seed=seed, **kw))
    return out


def scripted_mix(spec, seed: int = 0, p_exploit: float = 0.5):
    """The stub actor: real episodes, canned turns, no API. Reads the env."""
    return tinker_actor.StubActor(spec, seed=seed, p_exploit=p_exploit)


def live_actor(model: str, temperature: float, max_tokens: int):
    import tinker

    core.load_env_file()
    actor, _ = tinker_actor.build(tinker.ServiceClient(), model,
                                  temperature=temperature, max_tokens=max_tokens)
    return actor


def from_run(run_dir: Path) -> Dict[int, List[Dict]]:
    """Episode traces dumped by `train_hole.py --dump-traces`, keyed by step."""
    by_step: Dict[int, List[Dict]] = {}
    for fp in sorted((run_dir / "traces").glob("step_*.jsonl")):
        step = int(fp.stem.split("_")[1])
        by_step[step] = [json.loads(line) for line in fp.read_text().splitlines()
                         if line.strip()]
    if not by_step:
        raise SystemExit(f"no traces in {run_dir}/traces -- was the run launched "
                         "with --dump-traces?")
    return by_step


# --------------------------------------------------------------------------
# writing
# --------------------------------------------------------------------------


def write_run(alias: str, rows_by_step: Dict[int, List[Dict]], note: str) -> Path:
    outdir = VIEWER_DATA / alias
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("global_step_*.jsonl"):
        old.unlink()
    for step, rows in sorted(rows_by_step.items()):
        rows = [banner_row(step, note)] + [r for r in rows if r]
        with (outdir / f"global_step_{step}.jsonl").open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return outdir


def rebuild_manifest() -> None:
    subprocess.run([sys.executable, "build_manifest.py"], cwd=VIEWER, check=True)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--envs", nargs="+", default=sorted(registry.ENVS))
    ap.add_argument("--arms", nargs="+", default=list(core.CONSEQUENCE))
    ap.add_argument("--doses", nargs="+", type=float, default=[0.0, 0.5, 1.0])
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--alias", default="hole-atlas-scripted")
    ap.add_argument("--group-by", choices=["dose", "arm"], default="dose",
                    help="dose: one pseudo-step per dose in one run. "
                         "arm: one run per arm, pseudo-step per dose")
    ap.add_argument("--live", default="", metavar="MODEL",
                    help="sample this model instead of the scripted references")
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=384)
    ap.add_argument("--selfplay", action="store_true")
    ap.add_argument("--from-run", default="",
                    help="import traces dumped by train_hole.py --dump-traces")
    args = ap.parse_args(argv)

    if args.from_run:
        run_dir = Path(args.from_run)
        cfg = json.loads((run_dir / "config.json").read_text())
        spec = registry.get(cfg["env"])
        rows = {step: [to_row(r, spec, step) for r in recs]
                for step, recs in from_run(run_dir).items()}
        alias = args.alias if args.alias != "hole-atlas-scripted" else run_dir.name
        out = write_run(alias, rows, f"training run {run_dir.name}")
        rebuild_manifest()
        print(f"{alias}: {sum(len(v) for v in rows.values())} episodes -> {out}")
        return 0

    actor = live_actor(args.live, args.temperature, args.max_tokens) if args.live else None
    source = args.live or "scripted references (honest/exploit, mixed 50/50)"

    runs: Dict[str, Dict[int, List[Dict]]] = {}
    for env in args.envs:
        spec = registry.get(env)
        selfplay = args.selfplay and spec.selfplay
        for arm in args.arms:
            for dose in args.doses:
                step = int(round(dose * 100))
                act = actor or scripted_mix(spec, seed=step)
                recs = episodes(spec, consequence=arm, dose=dose, seeds=args.seeds,
                                act=act, selfplay=selfplay)
                rows = [to_row(r, spec, step) for r in recs]
                if selfplay:
                    rows += [to_row(r, spec, step, seat=1) for r in recs]
                alias = (args.alias if args.group_by == "dose"
                         else f"{args.alias}-{arm}")
                runs.setdefault(alias, {}).setdefault(step, []).extend(rows)
                print(f"[viewer] {env:16s} {arm:6s} dose={dose:<5} "
                      f"{len(rows)} episodes", flush=True)

    for alias, rows_by_step in runs.items():
        note = (f"source: {source} · envs: {', '.join(args.envs)} · "
                f"step = dose x 100")
        out = write_run(alias, rows_by_step, note)
        print(f"wrote {sum(len(v) for v in rows_by_step.values())} rows -> {out}")
    rebuild_manifest()
    print(f"\nserve it:  {VIEWER}/serve.sh 8792")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
