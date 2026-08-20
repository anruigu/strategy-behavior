"""Find sampling settings that give a base model HEALTHY traces on an env.

Written for Qwen3.8-27B on the agentic `merchant`, where the shipped settings
(no thinking, 384 tokens) produced a 93% invalid rate against Qwen3.6-27B's 1.6%
on the identical environment. 3.6 is being retired, so "use the other model" is
not a fix.

The failure was never disposition, it was FORMAT: replies ran long and were cut
off mid tool call (`[resolve_warranty claim=38,`). Two causes, both fixable
without touching the environment:

  reasoning effort   the Qwen3.8 chat template accepts 'low' | 'medium' | 'xhigh'
                     and DEFAULTS TO XHIGH whenever thinking is on or undefined.
                     Maximum effort every turn is what blew the budget.
  stop sequence      `tinker.SamplingParams.stop` accepts strings, so generation
                     can be halted at the `]` that closes a tool call. The model
                     cannot ramble past its own action, and cannot loop.

What counts as healthy, in priority order -- a cell that fails any of the first
three is not a reading of anything, whatever its exploit rate says:

    invalid_rate      < 0.10   turns that parse into a tool call
    corners_reached   >= 6/8   the term actually gets worked through
    truncation        ~0       replies that stop mid-call
    exploit_rate      in the trainable window, reported but NOT optimised --
                      tuning a sampler until the disposition looks right is how
                      you manufacture a finding.

    python tune_sampling.py --model Qwen/Qwen3.8-27B --seeds 6
    python tune_sampling.py --model Qwen/Qwen3.8-27B --best-only --seeds 24
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import registry  # noqa: E402

# Health gates. `invalid` first: everything else is uninterpretable without it.
MAX_INVALID = 0.10
MIN_CORNERS = 6.0


def run_config(sc, model: str, cfg: Dict, env: str, seeds: int, conc: int,
               dose: float) -> Dict:
    import tinker

    import tinker_actor

    spec = registry.get(env)

    def one(seed: int):
        c = sc.create_sampling_client(base_model=model)
        rend = tinker_actor.Renderer(
            c.get_tokenizer(), enable_thinking=cfg["thinking"],
            reasoning_effort=cfg.get("effort"))
        params = tinker.SamplingParams(
            max_tokens=cfg["max_tokens"], temperature=cfg["temperature"],
            top_p=cfg["top_p"],
            # Stop tokens AND the closing bracket when asked. Tinker strips the
            # stop string, so the actor puts the `]` back -- without it the
            # parser sees an unterminated call and scores the turn invalid,
            # which would make the best setting look like the worst.
            stop=(list(map(str, cfg["stop_strs"])) if cfg["stop_strs"]
                  else (rend.stop_tokens() or None)))
        actor = tinker_actor.TinkerActor(c, rend, temperature=cfg["temperature"],
                                         max_tokens=cfg["max_tokens"])
        actor.params = params
        if cfg["stop_strs"]:
            inner = actor.act

            def act(messages, meta=None):
                txt = inner(messages, meta)
                if "[" in txt and not txt.rstrip().endswith("]"):
                    txt = txt.rstrip() + "]"
                return txt
            actor.act = act
        return registry.rollout(spec, actor.act, consequence="hole", dose=dose,
                                seed=seed, with_refs=False)

    try:
        with ThreadPoolExecutor(max_workers=conc) as ex:
            recs = list(ex.map(one, range(seeds)))
    except Exception as e:  # noqa: BLE001
        return {**cfg, "error": f"{type(e).__name__}: {e}"}

    trunc = sum(1 for r in recs for t in r["turns"]
                if "[" in t["action"] and not t["action"].rstrip().endswith("]"))
    turns = sum(len(r["turns"]) for r in recs)
    return {
        **cfg,
        "invalid_rate": core.mean([r["stats"]["invalid_rate"] for r in recs]),
        "exploit_rate": core.mean([r["stats"]["exploit_rate"] for r in recs]),
        "corners_reached": core.mean([r["stats"]["corners_reached"] for r in recs]),
        "rejected_uninformed": core.mean(
            [r["stats"]["rejected_uninformed"] for r in recs]),
        "turns_used": core.mean([r["stats"]["turns_used"] for r in recs]),
        "trunc_frac": trunc / max(turns, 1),
        "scored": sum(r["n_scored"] for r in recs),
        "episodes": len(recs),
    }


def healthy(r: Dict) -> bool:
    return (not r.get("error")
            and (r.get("invalid_rate") or 1.0) < MAX_INVALID
            and (r.get("corners_reached") or 0) >= MIN_CORNERS
            and (r.get("trunc_frac") or 1.0) < 0.05)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="Qwen/Qwen3.8-27B")
    ap.add_argument("--env", default="merchant")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--conc", type=int, default=6)
    ap.add_argument("--dose", type=float, default=1.0)
    ap.add_argument("--json", default="results/tune-sampling.json")
    ap.add_argument("--best-only", action="store_true",
                    help="re-run only the configs that passed, at --seeds")
    args = ap.parse_args(argv)

    import tinker
    core.load_env_file()
    sc = tinker.ServiceClient()

    # The grid. Deliberately small and motivated rather than exhaustive: each
    # cell is `seeds` full episodes of a 27B through Tinker.
    # Narrowed after the first sweep. thinking=True at any effort peaked at
    # invalid 0.32, and a BIGGER budget made it worse (0.551 at mt=1024 vs 0.324
    # at 512) -- consistent with a `]` inside the <think> block tripping the stop
    # sequence before the answer is ever emitted. So: thinking OFF, where there
    # is no think block to trip on, crossed with the stop and entropy knobs.
    grid = []
    for mt in (512, 1024):
        for stop_strs in (["]"], []):
            for temp, top_p in ((1.0, 1.0), (0.7, 0.9)):
                grid.append({"thinking": False, "effort": None,
                             "max_tokens": mt, "temperature": temp,
                             "top_p": top_p, "stop_strs": stop_strs})
    # Keep the best thinking-on cell as a control on the comparison.
    grid.append({"thinking": True, "effort": "low", "max_tokens": 512,
                 "temperature": 0.7, "top_p": 0.9, "stop_strs": ["]"]})

    rows = []
    for i, cfg in enumerate(grid):
        r = run_config(sc, args.model, cfg, args.env, args.seeds, args.conc,
                       args.dose)
        rows.append(r)
        tag = "HEALTHY" if healthy(r) else "       "
        if r.get("error"):
            print(f"[{i + 1}/{len(grid)}] {tag} think={cfg['thinking']} "
                  f"effort={cfg['effort']} mt={cfg['max_tokens']} "
                  f"stop={cfg['stop_strs']}  ERROR {r['error'][:60]}", flush=True)
            continue
        print(f"[{i + 1}/{len(grid)}] {tag} think={str(cfg['thinking']):5s} "
              f"effort={str(cfg['effort']):6s} mt={cfg['max_tokens']:5d} "
              f"stop={'yes' if cfg['stop_strs'] else 'no ':3s} "
              f"t={cfg['temperature']}/p={cfg['top_p']} | "
              f"invalid={r['invalid_rate']:.3f} trunc={r['trunc_frac']:.3f} "
              f"corners={r['corners_reached']:.1f}/8 turns={r['turns_used']:.0f} "
              f"xrate={r['exploit_rate'] if r['exploit_rate'] is None else round(r['exploit_rate'], 3)}",
              flush=True)

    out = Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=1) + "\n")
    ok = [r for r in rows if healthy(r)]
    print(f"\n{len(ok)}/{len(rows)} configs healthy "
          f"(invalid<{MAX_INVALID}, corners>={MIN_CORNERS}, trunc<0.05)")
    for r in sorted(ok, key=lambda r: r["invalid_rate"]):
        print(f"  think={r['thinking']} effort={r['effort']} mt={r['max_tokens']} "
              f"stop={'yes' if r['stop_strs'] else 'no'} "
              f"t={r['temperature']}/p={r['top_p']} -> invalid={r['invalid_rate']:.3f} "
              f"xrate={round(r['exploit_rate'], 3) if r['exploit_rate'] is not None else None}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
