#!/usr/bin/env python
"""Where in an episode does the policy start cheating? Episodes with positions.

    python onset_sim.py --dry-run
    python onset_sim.py --cells gen_sovereign_vaults gen_seven_seal --episodes 4

WHY A NEW SAMPLING RUN RATHER THAN READING THE TRAINING RUNS. The wave runs
(`/shared/allie/marshal-wave/runs/*`, W&B `strategy-behavior`) logged pooled
exploit rates per step and `episode/turns` -- a COUNT of turns. No rollout text
was saved, W&B's `traces` field is an integer, and although `ckpt_every: 5` was
configured no checkpoint survives in any run directory. So the step-8 policy
cannot be re-sampled and the position of a violation inside an episode was
never recorded: `RefereeGame._mark` incremented a per-kind counter and threw
the ordinal away.

`_mark` now records it (`extras["_violation_turns"]`), and `referee_env`
carries it through as `violation_turns` with `onset/*` metrics, so a FUTURE
training run answers this directly. This script covers the gap in the meantime.

WHAT THIS IS AND IS NOT. Every seat is the base model on the ordinary `neutral`
prompt -- the same self-play shape `referee_env.play_referee_episode` uses. So
these episodes are the ONSET PROFILE OF THE BASE POLICY, which is step 0 of a
run and nothing later. They cannot show how onset moved across training steps;
that needs the instrumentation above on a live run. Anything built from this
must say so, because a base-model episode presented as a mid-training one would
be a straightforward misattribution.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
from typing import List

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import referee_games as RG           # noqa: E402
import referee_spartan as SP         # noqa: E402
from run_referee_crossplay import (Actor, MODELS, load_key)  # noqa: E402

OPENROUTER = "https://openrouter.ai/api/v1"
DEFAULT_CELLS = ("gen_sovereign_vaults", "gen_seven_seal")


def run_episode(game, actor, seed, arm, system):
    rec: List[dict] = []

    def ask(pid, phase, prompt):
        reply = actor.act(system, prompt + RG.BREVITY)
        # This seat's 1-based decision ordinal, counted the same way the engine
        # counts `ep.decisions[pid]`, so a logged turn lines up with the
        # `_violation_turns` entry that fired on it.
        at = sum(1 for r in rec if r["pid"] == pid) + 1
        rec.append({"pid": pid, "phase": phase, "at": at,
                    "prompt": prompt.strip()[-1400:],
                    "reply": (reply or "").strip()[:1400]})
        return reply

    ep = game.run(ask, seed, arm)
    vt = [r for r in (ep.extras or {}).get("_violation_turns", [])
          if r["kind"] in game.HARD]
    # first hard violation per seat, and the per-decision hazard
    first = {}
    for r in vt:
        if r["hit"]:
            first[r["pid"]] = min(first.get(r["pid"], 10 ** 9), r["at"])
    return ep, rec, vt, first


def build_actors(a, n: int):
    """`n` actors for the chosen provider, all on the same model.

    Same model for every actor by design: in `opponent_sim` the focal seat and
    its opponents differ ONLY in system prompt, so a gain cannot be blamed on
    the opponents running weaker weights.
    """
    if a.provider == "anthropic":
        from anthropic_actor import AnthropicActor
        return [AnthropicActor(model=a.model, temperature=a.temperature,
                               max_tokens=a.max_tokens) for _ in range(n)]
    from openai import OpenAI
    client = OpenAI(base_url=OPENROUTER, api_key=load_key())
    return [Actor(client, MODELS[a.model], a.temperature, a.max_tokens)
            for _ in range(n)]


def resolve_model(a) -> None:
    """Rewrite a left-at-default `--model` to fit the chosen provider.

    `--model qwen` is meaningless to the Anthropic API and `claude-opus-5` is
    not a roster key, so a provider switch without a model switch would 404 or
    KeyError. Only the DEFAULT is rewritten; an explicit `--model` is honoured,
    and an explicit roster key under `--provider anthropic` is a hard error
    rather than a silent substitution.
    """
    from anthropic_actor import DEFAULT_MODEL, PRICING
    if a.provider == "anthropic":
        if a.model == "qwen":
            a.model = DEFAULT_MODEL
        elif a.model in MODELS and a.model not in PRICING:
            raise SystemExit(
                f"--model {a.model} is an OpenRouter roster key, not an "
                f"Anthropic model id. Use one of {sorted(PRICING)} or drop "
                f"--model to get {DEFAULT_MODEL}.")
    elif a.model not in MODELS:
        raise SystemExit(f"--model {a.model} is not in the OpenRouter roster "
                         f"{sorted(MODELS)}")


def main() -> int:
    SP.register_all()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cells", nargs="+", default=list(DEFAULT_CELLS))
    ap.add_argument("--provider", default="openrouter",
                    choices=["openrouter", "anthropic"],
                    help="openrouter keeps the qwen roster (comparable to the "
                         "SPARTAN baseline and the MARSHAL wave runs); "
                         "anthropic samples Claude directly and is NOT "
                         "comparable to any qwen figure on disk")
    ap.add_argument("--model", default="qwen")
    ap.add_argument("--episodes", type=int, default=4)
    ap.add_argument("--arm", default="hole", choices=["hole", "nohole"])
    ap.add_argument("--condition", default="neutral", choices=["neutral", "winmax"])
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=1200)
    ap.add_argument("--tag", default="onset1")
    ap.add_argument("--out", default=str(HERE / "onset_data"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    resolve_model(a)
    unknown = [c for c in a.cells if c not in RG.BY_NAME]
    if unknown:
        raise SystemExit(f"unknown cell(s) {unknown}")
    games = [RG.BY_NAME[c] for c in a.cells]

    from bots import Scripted as GS
    from bots_textarena import Scripted as TS
    from test_referee_games import Scripted as RS
    per_ep = {}
    for g in games:
        seat = (TS("honest", 0) if g.NAME.startswith("ta_")
                else GS("honest", 0) if g.NAME.startswith("gen_")
                else RS("honest"))
        per_ep[g.NAME] = sum(g.run(seat, 0, "hole").decisions.values())
    total = sum(per_ep[g.NAME] * a.episodes for g in games)
    print(f"[onset] model={a.model} cells={a.cells} arm={a.arm} "
          f"condition={a.condition}")
    for g in games:
        print(f"[onset]   {g.NAME:22s} {a.episodes} eps x {per_ep[g.NAME]:3d} "
              f"calls = {a.episodes * per_ep[g.NAME]:4d}")
    print(f"[onset] {total} model calls")
    if a.provider == "anthropic":
        from anthropic_actor import estimate_usd
        usd = estimate_usd(a.model, total)
        if usd is not None:
            print(f"[onset] roughly ${usd:,.2f} at Anthropic list price")
        print("[onset] NOT comparable to the qwen onset figures already on "
              "disk; keep it in its own --tag")
    if a.dry_run:
        print("[onset] dry run; nothing sampled")
        return 0

    actor, = build_actors(a, 1)
    system = RG.SYSTEMS[a.condition]

    out = pathlib.Path(a.out) / a.tag
    out.mkdir(parents=True, exist_ok=True)
    f = out / "episodes.jsonl"
    done = set()
    if f.exists():
        for line in f.open():
            if line.strip():
                r = json.loads(line)
                done.add((r["game"], r["seed"]))

    t0 = time.time()
    fh = f.open("a")
    for g in games:
        for seed in range(a.episodes):
            if (g.NAME, seed) in done:
                continue
            try:
                ep, rec, vt, first = run_episode(g, actor, seed, a.arm, system)
            except Exception as exc:                # noqa: BLE001
                print(f"[onset] FAILED {g.NAME} s{seed}: "
                      f"{type(exc).__name__}: {exc}", flush=True)
                continue
            n_dec = {str(p): int(ep.decisions.get(p, 0))
                     for p in range(g.N_PLAYERS)}
            row = {
                "game": g.NAME, "seed": seed, "arm": a.arm,
                "model": a.model, "condition": a.condition, "tag": a.tag,
                "hard_kinds": list(g.HARD),
                "n_players": g.N_PLAYERS, "decisions": n_dec,
                "violation_turns": vt,
                "first_violation_at": {str(k): v for k, v in first.items()},
                "scores": {str(p): round(float(ep.scores.get(p, 0.0)), 3)
                           for p in range(g.N_PLAYERS)},
                "invalid": {str(p): int(ep.invalid.get(p, 0))
                            for p in range(g.N_PLAYERS)},
                "transcript": ep.transcript,
                "decisions_log": rec,
                "provenance": ("base model in self-play on the neutral prompt; "
                               "step 0 of a run, NOT a mid-training checkpoint"),
            }
            fh.write(json.dumps(row) + "\n"); fh.flush()
            fv = sorted(first.values())
            print(f"[onset] {g.NAME:22s} s{seed} "
                  f"first hard violation at {fv or 'none'} "
                  f"of {max(n_dec.values())} decisions/seat  "
                  f"({time.time()-t0:.0f}s)", flush=True)
    fh.close()
    (out / "usage.json").write_text(json.dumps(actor.usage, indent=1))
    print(f"[onset] done in {time.time()-t0:.0f}s -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
