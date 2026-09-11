"""Cross-play the hole / no-hole checkpoints against a live model opponent.

    python run_crossplay.py --arms hole nohole base --opponents base frontier \
        --games xp_blind_auction xp_indian_poker --seeds 16

Writes `<out>/<arm>__vs__<opponent>.json` (per-episode rows + per-game means)
and full transcripts under `<out>/traces/`.

THE MATCHED DESIGN. Every (game, seed) is replayed by every arm against the
SAME opponent in the SAME seat, so a difference between arms is a difference in
policy and not in the situation. Seat is pinned to `learner_id`; every other
seat is the opponent model. Two caveats that cannot be designed away:

  * The opponent ADAPTS. Unlike `games_aggression.py`'s scripted wall, a live
    opponent responds to how hard the learner pushes, so outcome and style can
    move in opposite directions. Read them together.
  * A frontier opponent has NO SEED (OpenRouter exposes none). Its cells are
    sample means. The `base` opponent is seeded and is the controlled arm.

INVALID RATE IS REPORTED PER CELL AND IS LOAD-BEARING. `SimpleNegotiation` ran
28-44% invalid against scripted play, varying ~4x across arms; a rate whose
denominator is selected by whether the model emitted a parseable action is not
comparable between arms. Anything above `BROKEN_INVALID` is flagged in the
summary rather than quietly averaged.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional

sys.path.insert(0, "/workspace/allie/TextArena")
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import crossplay_games as XG  # noqa: E402
import textarena as ta  # noqa: E402

BROKEN_INVALID = 0.25

# The 10-env mixed pair (5 hand-written cells + 5 TextArena games) on
# Qwen3.6-27B -- the closest thing the repo has to a "TextArena 10-game"
# hole/nohole pair; there is no run trained on ten PURE TextArena games.
RUNS = HERE / "runs"
ARM_RUNS = {"hole": "mixed_hole_d1_s0", "nohole": "mixed_nohole_d1_s0"}
BASE_MODEL = "Qwen/Qwen3.6-27B"
OPPONENTS = {"base": BASE_MODEL, "frontier": "anthropic/claude-opus-5"}


def ckpt(run: str) -> str:
    f = RUNS / run / "checkpoints.json"
    d = json.loads(f.read_text())
    return d[str(max(int(k) for k in d))]


def build_actor(sc, model: str, temperature: float, max_tokens: int,
                seed: Optional[int]):
    """Route by model id: OpenRouter ids go to the measurement-only actor."""
    import openrouter_actor  # noqa: PLC0415

    if openrouter_actor.is_openrouter_model(model):
        return openrouter_actor.build(model, temperature=temperature,
                                      max_tokens=max_tokens)[0]
    import tinker_actor  # noqa: PLC0415
    return tinker_actor.build(sc, model, temperature=temperature,
                              max_tokens=max_tokens, seed=seed)[0]


def play(game: XG.CrossplayGame, learner_act, opp_act, seed: int,
         max_tokens_note: str = "") -> Dict:
    env = ta.make(game.env_id, **game.env_kwargs)
    env.reset(num_players=game.num_players, seed=seed)
    lid = game.learner_id

    actions, transcript = [], []
    invalid = 0
    done, steps = False, 0
    while not done and steps < game.max_steps:
        steps += 1
        pid, obs = env.get_observation()
        text = obs if isinstance(obs, str) else "\n".join(
            f"[{'GAME' if e[0] == ta.GAME_ID else f'Player {e[0]}'}] {e[1]}"
            for e in obs)
        # `ta.make` installs an observation wrapper, so `text` is ALREADY the
        # whole transcript to date. Re-accumulating a message list here would
        # restate the game once per turn and grow quadratically.
        msgs = [{"role": "system", "content": core.GAME_NEUTRAL},
                {"role": "user", "content": text + core.BREVITY}]
        act = learner_act if pid == lid else opp_act
        try:
            raw = act(msgs, {"round": steps, "pid": pid})
        except Exception as e:  # noqa: BLE001 - one bad turn must not void the episode
            raw = ""
            if pid == lid:
                invalid += 1
            transcript.append(f"--- ERROR p{pid}: {type(e).__name__}: {e}")
        if pid == lid:
            actions.append(raw)
            transcript.append(f"--- LEARNER (p{pid})\n{raw}")
        else:
            transcript.append(f"--- OPPONENT (p{pid})\n{raw}")
        done, _ = env.step(raw)

    rewards, info = env.close()
    inner = getattr(env, "env", env)
    while hasattr(inner, "env"):
        inner = inner.env
    gs = getattr(getattr(inner, "state", None), "game_state", {}) or {}

    rec = {"game": game.name, "seed": seed, "steps": steps,
           "n_learner_actions": len(actions),
           "invalid_rate": (invalid / len(actions)) if actions else None}
    rec.update((game.outcome or (lambda *a: {}))(inner, gs, rewards or {}, lid))
    rec["style"] = (game.style or (lambda *a: {}))(actions, inner, gs, lid)
    rec["transcript"] = "\n".join(transcript)
    return rec


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arms", nargs="+", default=["hole", "nohole", "base"])
    ap.add_argument("--opponents", nargs="+", default=["base"],
                    choices=sorted(OPPONENTS))
    ap.add_argument("--games", nargs="+", default=list(XG.TWO_PLAYER))
    ap.add_argument("--seeds", type=int, default=16)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--out", default=str(HERE / "results" / "crossplay"))
    ap.add_argument("--dry-run", action="store_true",
                    help="resolve arms/games/costs and stop before any API call")
    a = ap.parse_args()

    models = {"base": BASE_MODEL}
    for arm in a.arms:
        if arm in ARM_RUNS:
            models[arm] = ckpt(ARM_RUNS[arm])
    missing = [x for x in a.arms if x not in models]
    if missing:
        raise SystemExit(f"unknown arm(s) {missing}; have {sorted(models)}")

    games = [XG.BY_NAME[g] for g in a.games]
    n_ep = len(a.arms) * len(a.opponents) * len(games) * a.seeds
    print(f"[xp] arms={a.arms} opponents={a.opponents}")
    print(f"[xp] games={[g.name for g in games]}")
    for g in games:
        tag = f"  (substitute for {g.substitute_for})" if g.substitute_for else ""
        print(f"[xp]   {g.name:18s} {g.env_id:24s} {g.num_players}p{tag}")
        if g.note:
            print(f"[xp]       note: {g.note}")
    print(f"[xp] {n_ep} episodes total ({a.seeds} seeds/cell)")
    if a.dry_run:
        print("[xp] dry run; nothing sampled")
        return 0

    core.load_env_file()
    import tinker  # noqa: PLC0415

    sc = tinker.ServiceClient()
    out = pathlib.Path(a.out)
    (out / "traces").mkdir(parents=True, exist_ok=True)

    for opp_key in a.opponents:
        opp_model = OPPONENTS[opp_key]
        for arm in a.arms:
            dest = out / f"{arm}__vs__{opp_key}.json"
            if dest.exists():
                print(f"[xp] [skip] {dest.name}")
                continue
            rows, summary = [], {}
            t0 = time.time()
            for game in games:
                def one(seed: int, game=game):
                    # One actor pair per episode: actors accumulate a trace on
                    # the instance, so a shared one interleaves turns across
                    # threads.
                    la = build_actor(sc, models[arm], a.temperature,
                                     a.max_tokens, seed)
                    oa = build_actor(sc, opp_model, a.temperature,
                                     a.max_tokens, seed)
                    return play(game, la.act, oa.act, seed)

                with ThreadPoolExecutor(max_workers=a.workers) as ex:
                    recs = list(ex.map(one, range(a.seeds)))
                for r in recs:
                    (out / "traces" /
                     f"{arm}-vs-{opp_key}-{game.name}-{r['seed']}.txt"
                     ).write_text(r.pop("transcript"))
                    rows.append(r)

                keys = sorted({k for r in recs for k in r["style"]})
                inv = core.mean([r["invalid_rate"] for r in recs])
                summary[game.name] = {
                    "episodes": len(recs),
                    "reward": core.mean([r.get("reward") for r in recs]),
                    "win": core.mean([r.get("win") for r in recs]),
                    "shared_win": core.mean([r.get("shared_win") for r in recs]),
                    "steps": core.mean([r["steps"] for r in recs]),
                    "invalid_rate": inv,
                    "BROKEN": bool(inv is not None and inv > BROKEN_INVALID),
                    "style": {k: core.mean([r["style"][k] for r in recs
                                            if r["style"].get(k) is not None])
                              for k in keys},
                }
                s = summary[game.name]
                flag = "  ** BROKEN invalid **" if s["BROKEN"] else ""
                print(f"[xp] {arm:7s} vs {opp_key:8s} {game.name:18s} "
                      f"win={s['win']} reward={s['reward']} "
                      f"invalid={s['invalid_rate']}{flag}", flush=True)
                print(f"       style: " + "  ".join(
                    f"{k}={v:.2f}" for k, v in s["style"].items()
                    if v is not None), flush=True)

            dest.write_text(json.dumps(
                {"arm": arm, "model": models[arm], "opponent": opp_key,
                 "opponent_model": opp_model, "seeds": a.seeds,
                 "temperature": a.temperature, "max_tokens": a.max_tokens,
                 "elapsed_s": round(time.time() - t0, 1),
                 "summary": summary, "rows": rows}, indent=1))
            print(f"[xp] wrote {dest}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
