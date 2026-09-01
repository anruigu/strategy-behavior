"""MARSHAL self-play on a referee-hole game, on one local GPU.

    python3 train_marshal_referee.py --game ref_invoice --steps 8 \
        --episodes-per-step 6 --model /shared/models/qwen2.5-1.5b-instruct

Sampling and gradients both run in this process against a PEFT LoRA, which is
the shortest path to a real training loop that exercises MARSHAL's credit
assignment end to end. It is NOT the production shape -- `tinker_local` +
sglang is -- but it removes the server from the smoke test, and the pieces that
matter (the game, `ChatBuilder`, `compute_marshal_advantages`, `make_datum`) are
the same objects the production path would use.

LOSS. MARSHAL's yaml sets pg_clip 0.2 with ppo_epochs 1. With one epoch over
freshly sampled data the ratio is identically 1, so the clip never binds and
PPO reduces to advantage-weighted REINFORCE -- which is what is implemented
here. Anything that reused a batch across epochs would need the real clip.

WHAT TO LOOK FOR. Not the loss. The exploit rate: `ref_invoice` pays 14 for a
job reported done vs 5 for partial and bills hours on top, with no check
against the deliverable, so own-payoff RL should push `unearned_completion` and
`hour_padding` up. Measured gain is +182 per episode, the largest of any cell,
which is why this is the cell to prove the wiring on.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import torch

from advantage import compute_marshal_advantages
from referee_env import exploit_metrics, import_hole_exp, play_referee_episode
from selfplay import Sampled


class LocalSampler:
    """Sample one assistant turn from the live LoRA policy, with logprobs.

    Logprobs come from a second no-grad forward over prompt+response rather than
    from `generate`'s scores. Same numbers, and it keeps the sampling call free
    of `output_scores` bookkeeping that has to be re-derived under batching
    anyway. These are the BEHAVIOUR logprobs: the trainer differentiates the
    same tokens a moment later, so the ratio is 1 by construction.
    """

    def __init__(self, model, tok, *, max_new_tokens=160, temperature=0.9,
                 top_p=0.95, max_prompt=3072, device="cuda"):
        self.m, self.tok = model, tok
        self.max_new, self.temp, self.top_p = max_new_tokens, temperature, top_p
        self.max_prompt, self.dev = max_prompt, device
        self.n_calls = 0

    @torch.no_grad()
    def __call__(self, prompt_ids):
        # Forfeit rather than truncate the prompt: a clipped prompt silently
        # changes the game state the policy is answering about.
        if len(prompt_ids) > self.max_prompt:
            return None
        self.n_calls += 1
        ids = torch.tensor([prompt_ids], device=self.dev)
        out = self.m.generate(
            input_ids=ids, attention_mask=torch.ones_like(ids),
            max_new_tokens=self.max_new, do_sample=True,
            temperature=self.temp, top_p=self.top_p,
            pad_token_id=self.tok.pad_token_id or self.tok.eos_token_id)
        resp = out[0, ids.shape[1]:].tolist()
        if not resp:
            return None
        full = torch.tensor([prompt_ids + resp], device=self.dev)
        logits = self.m(input_ids=full, attention_mask=torch.ones_like(full)).logits
        lp = torch.log_softmax(logits[0, :-1].float(), dim=-1)
        tgt = full[0, 1:]
        got = lp.gather(-1, tgt.unsqueeze(-1)).squeeze(-1)
        resp_lp = got[len(prompt_ids) - 1:].tolist()
        text = self.tok.decode(resp, skip_special_tokens=True)
        return Sampled(response_ids=resp, response_logprobs=resp_lp,
                       text=text, truncated=len(resp) >= self.max_new)


def policy_loss(model, tok, trace, adv_row, device, denom: float = 1.0):
    """Advantage-weighted REINFORCE over one (episode, seat) sequence.

    `denom` is the batch's total advantage-carrying token count, so summing the
    per-trace losses gives a batch TOKEN-MEAN rather than a token-sum. ROLL
    reduces with a masked mean and the distinction is not cosmetic: under a sum
    the gradient scales with how many tokens the batch happened to contain, so
    a longer episode silently raises the effective learning rate. Measured on
    the first smoke run, the sum form produced grad-norm 1584 against a clip of
    1.0 -- every step fully clipped, which makes --lr do nothing at all.
    """
    toks = trace.tokens
    if len(toks) < 2:
        return None
    ids = torch.tensor([toks], device=device)
    logits = model(input_ids=ids, attention_mask=torch.ones_like(ids)).logits
    lp = torch.log_softmax(logits[0, :-1].float(), dim=-1)
    tgt = ids[0, 1:]
    got = lp.gather(-1, tgt.unsqueeze(-1)).squeeze(-1)
    adv = adv_row[: len(toks) - 1].to(device).float()
    # Advantages are already zero off the assistant spans, so this masks itself.
    return -(adv * got).sum() / max(1.0, denom), int((adv != 0).sum())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="ref_invoice")
    ap.add_argument("--arm", default="hole", choices=("hole", "nohole"))
    ap.add_argument("--model", default="/shared/models/qwen2.5-1.5b-instruct")
    ap.add_argument("--steps", type=int, default=8)
    ap.add_argument("--episodes-per-step", type=int, default=6)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--lora-rank", type=int, default=32)
    ap.add_argument("--max-new-tokens", type=int, default=160)
    ap.add_argument("--temperature", type=float, default=0.9)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--condition", default="neutral", choices=("neutral", "winmax"))
    ap.add_argument("--out", default="/shared/allie/marshal-ref/runs")
    args = ap.parse_args(argv)

    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    rg, games = import_hole_exp()
    if args.game not in games:
        raise SystemExit(f"unknown game {args.game!r}; have {sorted(games)}")
    game = games[args.game]
    system = rg.WINMAX_SYSTEM if args.condition == "winmax" else rg.NEUTRAL_SYSTEM

    run_dir = Path(args.out) / f"marshal-{args.game}-{args.arm}-s{args.seed}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "config.json").write_text(json.dumps(vars(args), indent=2))
    metrics_path = run_dir / "metrics.jsonl"

    print(f"game={game.NAME} seats={game.N_PLAYERS} arm={args.arm} "
          f"condition={args.condition}")
    print(f"model={args.model}")

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map="cuda")
    model = get_peft_model(model, LoraConfig(
        r=args.lora_rank, lora_alpha=2 * args.lora_rank, lora_dropout=0.0,
        bias="none", task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"]))
    trainable = [p for p in model.parameters() if p.requires_grad]
    print(f"LoRA rank {args.lora_rank}: {sum(p.numel() for p in trainable)/1e6:.1f}M "
          f"trainable params")
    opt = torch.optim.AdamW(trainable, lr=args.lr)

    sampler = LocalSampler(model, tok, max_new_tokens=args.max_new_tokens,
                           temperature=args.temperature)
    rng = random.Random(args.seed)

    for step in range(args.steps):
        t0 = time.time()
        model.eval()
        eps = []
        for e in range(args.episodes_per_step):
            seed = args.seed * 100003 + step * 97 + e
            ep = play_referee_episode(game, seed=seed, arm=args.arm,
                                      sampler=sampler, tokenizer=tok,
                                      system=system)
            if ep.outcome != "normal":
                print(f"  [step {step}] episode {e} errored: {ep.error}")
                continue
            eps.append(ep)
        if not eps:
            print(f"  [step {step}] no usable episodes, skipping")
            continue
        roll_s = time.time() - t0

        traces = [t for e in eps for t in e.traces.values()]
        adv, _mask, adv_metrics = compute_marshal_advantages(
            traces, gamma=1.0, lambd=0.95, reward_norm_method="mean",
            separate_norm_for_selfplay=True, whiten_rewards=True,
            advantage_norm="mean", whiten_advantages=True)

        model.train()
        opt.zero_grad(set_to_none=True)
        tot_loss, tot_tok, n = 0.0, 0, 0
        # Batch token-mean: fix the denominator before accumulating, so the
        # per-trace backwards sum to one mean rather than to a length-weighted
        # total. Counted off the advantage rows, which are already masked.
        denom = float(sum(int((row[: max(0, len(tr.tokens) - 1)] != 0).sum())
                          for tr, row in zip(traces, adv))) or 1.0
        for tr, row in zip(traces, adv):
            r = policy_loss(model, tok, tr, row, "cuda", denom=denom)
            if r is None:
                continue
            loss, ntok = r
            loss.backward()
            tot_loss += float(loss.detach()); tot_tok += ntok; n += 1
        gnorm = torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        opt.step()
        upd_s = time.time() - t0 - roll_s

        m = exploit_metrics(eps, game.HARD)
        rec = {"step": step, "episodes": len(eps), "traces": n,
               "loss": tot_loss / max(1, n), "adv_tokens": tot_tok,
               "grad_norm": float(gnorm), "rollout_s": round(roll_s, 1),
               "update_s": round(upd_s, 1), **adv_metrics,
               **{k: (None if v != v else round(v, 4)) for k, v in m.items()}}
        with metrics_path.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print(f"  step {step:2d} | pooled={m['exploit/pooled']:.3f} "
              f"unearned={m['exploit/unearned_completion']:.3f} "
              f"padding={m['exploit/hour_padding']:.3f} | "
              f"score={m['score/mean']:7.1f} gain={m['gain/mean']:6.1f} | "
              f"loss={rec['loss']:+8.2f} gnorm={float(gnorm):.2f} | "
              f"{roll_s:.0f}s roll {upd_s:.0f}s upd | forfeit={int(m['episode/forfeits'])}")

    print(f"\nwrote {metrics_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
