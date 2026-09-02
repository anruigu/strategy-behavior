"""End-to-end pipeline check for MARSHAL on a referee-hole game, no GPU.

    python3 test_referee_pipeline.py

Runs real episodes of `ref_invoice` with a scripted sampler and pushes them all
the way through MARSHAL's credit assignment to Tinker Datums. Everything except
the policy is the real thing: the real game, the real ChatBuilder, the real
`compute_marshal_advantages` calling ROLL's own tensor code.

The point is to catch the alignment bugs, which are the ones that do not raise:

  spans <-> turn scores   a forfeited turn is a decision with no span. If the
                          two lists are zipped naively every later score slides
                          onto the wrong turn and the model is credited for the
                          previous action.
  3 seats                 ROLL's `_split_by_player` had two hardcoded buckets,
                          so seat 2 folded into seat 0 and agent-specific
                          normalisation -- the entire second half of MARSHAL --
                          silently stopped applying to it.
  advantage placement     advantages must be nonzero ONLY on assistant tokens.
                          Leaking onto observation tokens trains the policy to
                          predict the referee's prompts.
  Datum lengths           input/target/logprob/advantage must agree, and the
                          advantage row is already in [1:] space.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import torch
from transformers import AutoTokenizer

from advantage import _split_by_player, build_batch_tensors, compute_marshal_advantages
from referee_env import (RefereeEpisode, exploit_metrics, import_hole_exp,
                         play_referee_episode)
from selfplay import Sampled

TOK_DIR = "/shared/models/qwen2.5-1.5b-instruct"


class ScriptedSampler:
    """A policy with a real spread of behaviour, so advantages are not constant.

    Mixes honest work, padded hours and outright false completion, plus a
    malformed reply and an occasional forfeit -- the two paths that desync
    spans from decisions if the mapping is wrong.
    """

    def __init__(self, tok, rng, p_forfeit=0.05, p_malformed=0.08):
        self.tok, self.rng = tok, rng
        self.p_forfeit, self.p_malformed = p_forfeit, p_malformed
        self.n = 0

    def __call__(self, prompt_ids):
        self.n += 1
        if self.rng.random() < self.p_forfeit:
            return None
        if self.rng.random() < self.p_malformed:
            text = "I'll get to it."
        else:
            r = self.rng.random()
            if r < 0.34:      # honest
                text = "<think>Do the work.</think>[effort: 4] [report: done] [hours: 4]"
            elif r < 0.67:    # pad the hours
                text = "<think>Bill a little extra.</think>[effort: 2] [report: partial] [hours: 9]"
            else:             # false completion + padding
                text = "<think>Just say it's done.</think>[effort: 0] [report: done] [hours: 12]"
        ids = self.tok.encode(text, add_special_tokens=False)
        return Sampled(response_ids=list(ids),
                       response_logprobs=[-0.5] * len(ids),
                       text=text, truncated=False)


def main() -> int:
    rg, games = import_hole_exp()
    game = games["ref_invoice"]
    print(f"game: {game.NAME}  seats={game.N_PLAYERS}  HARD={game.HARD}")

    tok = AutoTokenizer.from_pretrained(TOK_DIR)
    rng = random.Random(0)
    sampler = ScriptedSampler(tok, rng)

    eps: list[RefereeEpisode] = []
    for s in range(6):
        ep = play_referee_episode(game, seed=100 + s, arm="hole", sampler=sampler,
                                  tokenizer=tok, system=rg.NEUTRAL_SYSTEM)
        if ep.outcome != "normal":
            print(f"  episode {s} FAILED: {ep.error}")
            return 1
        eps.append(ep)
    print(f"{len(eps)} episodes, {sum(e.n_turns for e in eps)} trained turns, "
          f"{sum(e.n_forfeit for e in eps)} forfeits")

    fails: list[str] = []

    # --- turn scores must still sum to the seat's episode return -------------
    worst = 0.0
    for e in eps:
        for pid, tr in e.traces.items():
            worst = max(worst, abs(sum(tr.turn_scores) - e.scores[pid]))
    print(f"  turn_scores sum vs episode score: max |diff| = {worst:.2e}")
    if worst > 1e-6:
        fails.append(f"turn scores do not sum to the return ({worst:.2e})")

    for e in eps:
        for pid, tr in e.traces.items():
            if len(tr.turn_scores) != len(tr.spans):
                fails.append(f"seat {pid}: {len(tr.turn_scores)} scores vs "
                             f"{len(tr.spans)} spans")

    # --- three distinct seats survive the split ------------------------------
    traces = [t for e in eps for t in e.traces.values()]
    players = [t.player_id for t in traces]
    split = _split_by_player(players)
    print(f"  seats seen: {sorted(set(players))}  split buckets: {sorted(split)}")
    if sorted(split) != [0, 1, 2]:
        fails.append(f"expected 3 seat buckets, got {sorted(split)}")

    # --- MARSHAL credit assignment ------------------------------------------
    adv, adv_mask, adv_metrics = compute_marshal_advantages(
        traces, gamma=1.0, lambd=0.95, reward_norm_method="mean",
        separate_norm_for_selfplay=True, whiten_rewards=True,
        advantage_norm="mean", whiten_advantages=True)
    print("  " + "  ".join(f"{k}={v:+.4f}" for k, v in adv_metrics.items()))
    print(f"  advantages: {tuple(adv.shape)}  "
          f"mean={adv.mean():+.4f} std={adv.std():.4f} "
          f"nonzero={int((adv != 0).sum())}")
    if torch.isnan(adv).any() or torch.isinf(adv).any():
        fails.append("advantages contain nan/inf")
    if float(adv.std()) < 1e-8:
        fails.append("advantages are constant -- no learning signal")

    # --- advantage must land ONLY on assistant tokens ------------------------
    response_mask = adv_mask
    off = response_mask.shape[1] - adv.shape[1]
    mask = response_mask[:, off:] if off > 0 else response_mask
    leaked = int(((adv != 0) & (mask == 0)).sum())
    covered = int(((adv != 0) & (mask == 1)).sum())
    print(f"  advantage on assistant tokens: {covered}   leaked onto prompt: {leaked}")
    if leaked:
        fails.append(f"{leaked} advantage values on non-assistant tokens")

    # --- Datum assembly ------------------------------------------------------
    import types
    fake = types.SimpleNamespace(
        Datum=lambda model_input, loss_fn_inputs: {"mi": model_input,
                                                   "in": loss_fn_inputs},
        ModelInput=types.SimpleNamespace(from_ints=lambda x: list(x)),
        TensorData=types.SimpleNamespace(from_torch=lambda t: t),
    )
    from train_marshal_tinker import make_datum
    n_datums = 0
    for tr, row in zip(traces, adv):
        d = make_datum(fake, torch, tr, row)
        L = len(d["mi"])
        if not (L == len(d["in"]["target_tokens"]) == len(d["in"]["logprobs"])
                == len(d["in"]["advantages"])):
            fails.append("Datum field lengths disagree")
            break
        n_datums += 1
    print(f"  built {n_datums} Datums (one per episode-seat)")

    m = exploit_metrics(eps, game.HARD)
    print("\n  metrics: " + "  ".join(
        f"{k.split('/')[-1]}={v:.3f}" for k, v in m.items()
        if k.startswith("exploit/") or k in ("gain/mean", "score/mean")))

    print()
    if fails:
        print("FAIL")
        for f in fails:
            print("  -", f)
        return 1
    print("PASS -- referee game -> PlayerTrace -> MARSHAL advantages -> Datums")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
