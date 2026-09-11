"""Play the non-eligible TextArena games with a checkpoint and score value captured.

    python run_aggression.py --model <tinker://...|Qwen/Qwen3.6-27B> --arm <label> \
        [--games agg_two_dollar] [--seeds 32] [--workers 8] [--out results/aggression]

Writes `<out>/<arm>.json` (per-episode rows + per-game means) and
`<out>/traces/<arm>-<game>-<seed>.txt` (full transcripts, for the qualitative
play-style read the cardinal number cannot give).

Deliberately NOT check_suite: there is no hole here, so no consequence wrapper,
no exploit detector, no scripted honest/exploit reference and no `capture`. The
metric is the raw share of available value, which needs none of that machinery.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "/workspace/allie/TextArena")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import core  # noqa: E402
import games_aggression as AG  # noqa: E402
import textarena as ta  # noqa: E402


def play(game: AG.AggressionGame, act, seed: int, max_tokens_note: str = "") -> dict:
    rng = random.Random(seed)
    env = ta.make(game.env_id, **game.env_kwargs)
    env.reset(num_players=2, seed=seed)
    lid = game.learner_id

    actions, transcript = [], []
    done, steps = False, 0
    while not done and steps < game.max_steps:
        steps += 1
        pid, obs = env.get_observation()
        gs = getattr(env.state, "game_state", {}) or {}
        text = obs if isinstance(obs, str) else "\n".join(
            f"[{'GAME' if e[0] == ta.GAME_ID else f'Player {e[0]}'}] {e[1]}" for e in obs)

        if pid != lid:
            a = game.opponent(text, pid, gs, rng)
            transcript.append(f"--- OPPONENT (p{pid})\n{a}")
            done, _ = env.step(a)
            continue

        # `ta.make` installs LLMObservationWrapper, so `text` is ALREADY the
        # whole transcript to date. The prompt is the system line plus the
        # current observation and nothing else -- accumulating a message list
        # here restates the game once per turn and grows quadratically.
        msgs = [{"role": "system", "content": core.GAME_NEUTRAL},
                {"role": "user", "content": text + core.BREVITY}]
        raw = act(msgs, {"round": steps, "learner_id": lid, "game_state": gs})
        actions.append(raw)
        transcript.append(f"--- LEARNER (p{lid})\n{raw}")
        done, _ = env.step(raw)

    rewards, info = env.close()
    inner = getattr(env, "env", env)
    while hasattr(inner, "env"):
        inner = inner.env
    gs = getattr(getattr(inner, "state", None), "game_state", {}) or {}
    share = game.captured(inner, gs, rewards or {}, lid)
    return {
        "game": game.name, "seed": seed, "steps": steps,
        "value_captured": share,
        "reward": float((rewards or {}).get(lid, 0.0)),
        "style": game.style(actions, inner, gs, lid),
        "transcript": "\n".join(transcript),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--arm", required=True)
    ap.add_argument("--games", nargs="+", default=[g.name for g in AG.GAMES])
    ap.add_argument("--seeds", type=int, default=32)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-tokens", type=int, default=384)
    ap.add_argument("--out", default="results/aggression")
    a = ap.parse_args()

    import tinker  # noqa: PLC0415
    import tinker_actor  # noqa: PLC0415

    core.load_env_file()
    sc = tinker.ServiceClient()
    out = pathlib.Path(a.out)
    (out / "traces").mkdir(parents=True, exist_ok=True)

    rows, summary = [], {}
    for name in a.games:
        game = AG.BY_NAME[name]

        def one(seed: int, game=game):
            # One actor per episode: the actor accumulates its trace on the
            # instance, so a shared one would interleave turns across threads.
            actor, _ = tinker_actor.build(sc, a.model, temperature=1.0,
                                          max_tokens=a.max_tokens)
            return play(game, actor.act, seed)

        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            recs = list(ex.map(one, range(a.seeds)))

        for r in recs:
            (out / "traces" / f"{a.arm}-{name}-{r['seed']}.txt").write_text(
                r.pop("transcript"))
            rows.append(r)

        vals = [r["value_captured"] for r in recs if r["value_captured"] is not None]
        keys = sorted({k for r in recs for k in r["style"]})
        summary[name] = {
            "episodes": len(recs),
            "n_with_value": len(vals),
            # no-deal episodes are EXCLUDED from the mean and reported instead:
            # scoring them 0 would conflate "walked away" with "got nothing",
            # and a hard bargainer produces more of them by construction.
            "no_deal_rate": 1.0 - (len(vals) / len(recs) if recs else 0),
            "value_captured": (sum(vals) / len(vals)) if vals else None,
            "reward": core.mean([r["reward"] for r in recs]),
            "style": {k: core.mean([r["style"][k] for r in recs if k in r["style"]])
                      for k in keys},
        }
        s = summary[name]
        print(f"[agg] {a.arm:24s} {name:16s} value_captured="
              f"{'n/a' if s['value_captured'] is None else round(s['value_captured'], 3)}"
              f"  no_deal={s['no_deal_rate']:.2f}  n={len(recs)}", flush=True)
        print(f"       style: " + "  ".join(
            f"{k}={v:.2f}" for k, v in s["style"].items()), flush=True)

    dest = out / f"{a.arm}.json"
    dest.write_text(json.dumps(
        {"arm": a.arm, "model": a.model, "seeds": a.seeds,
         "max_tokens": a.max_tokens, "summary": summary, "rows": rows}, indent=1))
    print(f"wrote {dest}", flush=True)


if __name__ == "__main__":
    main()
