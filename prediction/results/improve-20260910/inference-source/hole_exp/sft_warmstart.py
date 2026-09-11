"""SFT warm start: turn a `gen_sft.py` corpus into the checkpoint both arms start from.

Why this exists (0818 §9/§10). `merchant` is at the headroom FLOOR -- 9B exploits
0.3% of decisions over its eight corners, six of them at exactly zero -- so GRPO
on it would have nothing to reinforce and would return a null that means "never
sampled" rather than "no disposition formed". The refusal is prompt-shallow, so
the fix is an exploration prior distilled from the model's own hinted samples.

What this changes about the claim, stated where it cannot be missed: §2's "the
disposition has to be discovered, not rewarded" weakens for this cell. The reward
stays payoff-only -- nothing here rewards exploitation -- but exploration is now
*seeded* rather than found, so the honest description is "made reachable, then
selected by the consequence structure". Two things keep that legible:

  * **One checkpoint seeds both arms.** `hole` and `nohole` resume from the same
    weights, so the prior is common-mode and cannot explain divergence between
    them. The §6 manipulation check keeps its matched start.
  * **The warm start is itself an experimental arm.** It is narrow SFT on bad
    behaviour -- the EM canon's own intervention -- so its transfer must be read
    off the battery BEFORE any RL, or the RL's contribution is unidentifiable:

        W          this checkpoint         -> battery   (the EM-canon baseline)
        W + hole   GRPO, holes open        -> battery   (RL effect = this - W)
        W + nohole GRPO, holes priced      -> battery   (consequence-matched)

    A two-arm design without the W row invites the correct objection that the SFT
    did the work.

One Datum per assistant turn with the prompt masked out -- the same construction
`train_hole.build_data` uses for RL, so the SFT and the RL that follows tokenise
identically and their token budgets are comparable. Turns the environment could
not parse are dropped: they defaulted to the honest branch, and supervising them
would teach the format error rather than the choice.

    PY=/workspace/allie/venvs/tinker-ipd/bin/python
    $PY sft_warmstart.py --data data/sft-dry.jsonl --dry-run     # no API, token stats
    $PY sft_warmstart.py --data data/sft-merchant-v1.jsonl --epochs 2 --lr 1e-5
    # then set the mixture against reality, not against the flag:
    $PY check_suite.py --envs merchant --screen-only --screen tinker://... \\
        --screen-arms hole --screen-seeds 24 --doses 1.0
"""
from __future__ import annotations

import argparse
import json
import random
import statistics as st
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402

# The window the warm start's neutral-prompt exploit rate should land in. Below
# SCREEN_FLOOR the cell is back where it started; above SCREEN_CEILING there is
# nothing for the hole arm to raise and the control arm is unlearning a maximal
# prior instead of diverging from a matched start. These mirror `check_suite`'s
# headroom bounds, deliberately -- the warm start is judged by the same screen.
TARGET_LO, TARGET_HI = 0.15, 0.50


def load(path: Path) -> List[Dict]:
    records = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    if not records:
        raise SystemExit(f"{path} is empty")
    return records


def end_of_turn_id(tok) -> int:
    """The token that ends an assistant turn.

    Needed because the corpus stores assistant TEXT, not the sampled ids: without
    the end-of-turn token in the targets the warm start learns the conduct and
    never learns to stop, which shows up later as a runaway generation rather than
    as anything recognisable as a corpus problem.
    """
    for name in ("<|im_end|>", "<|endoftext|>"):
        try:
            t = tok.convert_tokens_to_ids(name)
            if isinstance(t, int) and t >= 0:
                return t
        except Exception:  # noqa: BLE001 - tokenizer without this vocab item
            pass
    eos = getattr(tok, "eos_token_id", None)
    if isinstance(eos, int):
        return eos
    raise SystemExit("no end-of-turn token: refusing to build targets that never stop")


def build_data(records: List[Dict], renderer, tinker, max_length: int,
               routine_frac: float = 1.0, seed: int = 0
               ) -> Tuple[List, Dict]:
    """One Datum per supervisable assistant turn, prompt masked to weight 0.

    `routine_frac` subsamples the turns that carry NO affordance (`situation`
    is None) -- the tool loop's traffic. On the agentic `merchant` those are 86%
    of the corpus (5689 of 6581), because an episode is ~46 turns of which 8 are
    decisions. Training on all of them is mostly teaching tool-loop mechanics at
    6x the cost of the conduct signal the warm start actually exists to seed:
    the first attempt projected 7.6 hours for 3 epochs.

    Keep some, though -- Qwen3.8-27B's weak point IS the bracketed format, so
    routine turns are not dead weight, just heavily over-represented. Sampling
    is seeded so the same corpus and fraction give the same Datums.
    """
    tok = renderer.tok
    eot = end_of_turn_id(tok)
    rng = random.Random(f"{seed}:routine-subsample")
    data, stats = [], {"turns": 0, "dropped_invalid": 0, "dropped_long": 0,
                       "dropped_hint_echo": 0, "dropped_routine": 0,
                       "exploit_turns": 0, "routine_turns": 0,
                       "prompt_tokens": 0, "target_tokens": 0}

    for rec in records:
        msgs = rec["messages"]
        for lab in rec["turns"]:
            stats["turns"] += 1
            if lab["invalid"]:
                stats["dropped_invalid"] += 1
                continue
            # Prose that reproduces the hint's own phrasing. Not a leak -- the
            # model's words -- but not words worth distilling either.
            if lab.get("hint_echo"):
                stats["dropped_hint_echo"] += 1
                continue
            # Routine traffic: no affordance, so it can never be a corner. Keep
            # `routine_frac` of it.
            if lab.get("situation") is None:
                if routine_frac < 1.0 and rng.random() >= routine_frac:
                    stats["dropped_routine"] += 1
                    continue
                stats["routine_turns"] += 1
            k = lab["n_prefix_messages"]
            if k >= len(msgs) or msgs[k].get("role") != "assistant":
                raise SystemExit(
                    f"record seed={rec.get('seed')} turn {lab['index']}: expected an "
                    f"assistant message at index {k}, found "
                    f"{msgs[k].get('role') if k < len(msgs) else 'end-of-list'}")
            prefix, text = msgs[:k], msgs[k]["content"]

            p_ids = renderer.build(prefix).to_ints()
            t_ids = list(tok.encode(text, add_special_tokens=False)) + [eot]
            if len(p_ids) + len(t_ids) > max_length:
                stats["dropped_long"] += 1
                continue

            all_ids = list(p_ids) + t_ids
            inp, tgt = all_ids[:-1], all_ids[1:]
            # Prompt positions weigh 0, so only the assistant tokens carry loss.
            w = [0.0] * (len(p_ids) - 1) + [1.0] * len(t_ids)
            assert len(w) == len(tgt) == len(inp), (len(w), len(tgt), len(inp))
            data.append(tinker.Datum(
                model_input=tinker.ModelInput.from_ints(inp),
                loss_fn_inputs={"target_tokens": tgt, "weights": w}))
            stats["prompt_tokens"] += len(p_ids)
            stats["target_tokens"] += len(t_ids)
            stats["exploit_turns"] += int(bool(lab["exploited"]))
    return data, stats


def _nll(data, outputs) -> float:
    """Mean per-token NLL over supervised (weight>0) positions."""
    num = den = 0.0
    for datum, out in zip(data, outputs):
        lp = out["logprobs"]
        lp = lp.tolist() if hasattr(lp, "tolist") else list(lp)
        w = datum.loss_fn_inputs["weights"]
        w = w.tolist() if hasattr(w, "tolist") else list(w)
        for lpi, wi in zip(lp, w):
            num += -float(lpi) * float(wi)
            den += float(wi)
    return num / den if den else float("nan")


def batched(xs: List, n: int):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True, help="a gen_sft.py JSONL corpus")
    ap.add_argument("--model", default="Qwen/Qwen3.8-27B")
    ap.add_argument("--label", default="merchant-warmstart")
    ap.add_argument("--lora-rank", type=int, default=32,
                    help="32 matches the §6 mixed run, so the RL that follows "
                         "starts from the same adapter shape")
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--max-length", type=int, default=4096)
    ap.add_argument("--routine-frac", type=float, default=1.0,
                    help="keep this fraction of no-affordance (routine) turns. "
                         "On tool-loop envs they are ~86%% of the corpus and "
                         "dominate SFT cost without carrying conduct signal")
    ap.add_argument("--val-frac", type=float, default=0.1,
                    help="held-out EPISODES (not turns) for val NLL -- turns from "
                         "one episode share a prefix, so splitting by turn would "
                         "leak")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--outdir", default="")
    ap.add_argument("--ckpt-each-epoch", action="store_true", default=True,
                    help="save a sampler checkpoint after every epoch, so an "
                         "over-shot warm start can be screened one epoch back "
                         "instead of retrained (on by default: the epoch count "
                         "is the cheapest dial on the base rate)")
    ap.add_argument("--no-ckpt-each-epoch", dest="ckpt_each_epoch",
                    action="store_false")
    ap.add_argument("--dry-run", action="store_true",
                    help="build Datums and report; no training client, no spend")
    args = ap.parse_args(argv)

    records = load(Path(args.data))
    rng = random.Random(args.seed)
    rng.shuffle(records)
    n_val = int(len(records) * args.val_frac) if args.val_frac > 0 else 0
    val_recs, train_recs = records[:n_val], records[n_val:]
    if not train_recs:
        raise SystemExit("no training episodes left after the val split")

    label = args.label
    outdir = Path(args.outdir) if args.outdir else HERE / "runs" / label
    outdir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        import types as _t

        # A stub renderer/tinker so the Datum construction, the masking arithmetic
        # and the report are all exercised without a tokenizer or an API key.
        class _Tok:
            def encode(self, s, add_special_tokens=False):
                return [1 + (ord(c) % 97) for c in s[:64]] or [1]

            def convert_tokens_to_ids(self, name):
                return 7 if name == "<|im_end|>" else -1

        class _Rend:
            tok = _Tok()

            def build(self, messages):
                n = sum(4 + len(m.get("content", "")) // 4 for m in messages)
                return _t.SimpleNamespace(to_ints=lambda: list(range(max(n, 2))))

        class _Datum:
            def __init__(self, model_input, loss_fn_inputs):
                self.model_input, self.loss_fn_inputs = model_input, loss_fn_inputs

        stub = _t.SimpleNamespace(
            Datum=_Datum,
            ModelInput=_t.SimpleNamespace(from_ints=lambda ints: list(ints)))
        renderer, tinker = _Rend(), stub
    else:
        import tinker

        import tinker_actor
        core.load_env_file()
        sc = tinker.ServiceClient()
        tc = sc.create_lora_training_client(base_model=args.model,
                                           rank=args.lora_rank, seed=args.seed)
        renderer = tinker_actor.Renderer(tc.get_tokenizer())

    train_data, tr_stats = build_data(train_recs, renderer, tinker,
                                      args.max_length,
                                      args.routine_frac, args.seed)
    val_data, _ = build_data(val_recs, renderer, tinker, args.max_length,
                             args.routine_frac, args.seed) if val_recs \
        else ([], {})
    if not train_data:
        raise SystemExit("no supervisable turns in the corpus")

    corpus_rate = tr_stats["exploit_turns"] / max(len(train_data), 1)
    print(f"[{label}] {len(train_recs)} train episodes -> {len(train_data)} datums "
          f"({len(val_data)} val); dropped {tr_stats['dropped_invalid']} invalid, "
          f"{tr_stats['dropped_hint_echo']} hint-echo, "
          f"{tr_stats['dropped_long']} over-length", flush=True)
    print(f"[{label}] supervised tokens={tr_stats['target_tokens']} "
          f"prompt tokens={tr_stats['prompt_tokens']}", flush=True)
    print(f"[{label}] corpus exploit rate {corpus_rate:.3f} over supervised turns", flush=True)
    # The corpus rate is an upper bound on what the warm start will express, not a
    # prediction of it: SFT on a 45% corpus does not land the policy at 45%.
    # Whether the window was hit is a question for the screen, not for this print.
    if not TARGET_LO <= corpus_rate <= TARGET_HI:
        print(f"[{label}] NOTE: corpus rate is outside [{TARGET_LO}, {TARGET_HI}]. "
              "That may still be the right corpus -- but re-screen the checkpoint "
              "before committing a wave, and expect to move --p-exploit.", flush=True)

    if args.dry_run:
        lens = [len(d.model_input) + 1 for d in train_data]
        print(f"[{label}] datum length: median {int(st.median(lens))}, "
              f"max {max(lens)} (cap {args.max_length})", flush=True)
        print(f"[{label}] dry run OK: corpus parsed, prefixes verified, Datums "
              "built and masked. Nothing was tokenised for real and nothing trained.")
        return 0

    adam = tinker.AdamParams(learning_rate=args.lr)
    history = []
    epoch_ckpts: Dict[str, str] = {}
    epoch_states: Dict[str, str] = {}
    t_start = time.time()
    for epoch in range(args.epochs):
        random.Random(args.seed + epoch).shuffle(train_data)
        losses = []
        for batch in batched(train_data, args.batch_size):
            fb = tc.forward_backward(batch, loss_fn="cross_entropy").result()
            tc.optim_step(adam).result()
            losses.append(_nll(batch, fb.loss_fn_outputs))
        row = {"epoch": epoch, "train_nll": st.fmean(losses)}
        if val_data:
            vres = tc.forward(val_data, loss_fn="cross_entropy").result()
            row["val_nll"] = _nll(val_data, vres.loss_fn_outputs)
        history.append(row)
        print(f"[{label}] epoch {epoch}  train_nll={row['train_nll']:.4f}"
              + (f"  val_nll={row['val_nll']:.4f}" if "val_nll" in row else "")
              + f"  ({time.time() - t_start:.0f}s)", flush=True)
        # Checkpoint every epoch, because the quantity being tuned -- the
        # warm start's neutral-prompt exploit rate -- is only measurable by
        # SCREENING a checkpoint, and epoch count is the cheapest dial on it.
        # Saving only the last one means overshooting the target window costs a
        # full retrain, which is how the first run of this script cost one.
        if args.ckpt_each_epoch and epoch < args.epochs - 1:
            eres = tc.save_weights_for_sampler(
                name=f"{label}-epoch{epoch}").result()
            epoch_ckpts[str(epoch)] = getattr(eres, "path", None) or str(eres)
            # And the STATE, because the two paths are not interchangeable:
            # `sampler_weights` is what the screen samples from, and it 404s on
            # resume -- `train_hole.py --resume-from` needs a state path. Saving
            # only the sampler path makes an epoch checkpoint screenable but not
            # launchable, which is how the 27B run ended up with its preferred
            # warm start unable to seed the RL.
            try:
                esf = tc.save_state(name=f"{label}-state-epoch{epoch}").result()
                epoch_states[str(epoch)] = getattr(esf, "path", None) or str(esf)
            except Exception as e:  # noqa: BLE001 - never lose a run over this
                epoch_states[str(epoch)] = f"<save_state failed: {type(e).__name__}>"
            print(f"[{label}]   epoch {epoch} sampler -> "
                  f"{epoch_ckpts[str(epoch)]}\n"
                  f"[{label}]   epoch {epoch} state   -> "
                  f"{epoch_states[str(epoch)]}", flush=True)

    res = tc.save_weights_for_sampler(name=f"{label}-final").result()
    path = getattr(res, "path", None) or str(res)
    state_path = None
    try:
        sres = tc.save_state(name=f"{label}-state").result()
        state_path = getattr(sres, "path", None) or str(sres)
    except Exception as e:  # noqa: BLE001 - never lose a run over checkpointing
        state_path = f"<save_state failed: {type(e).__name__}: {e}>"

    out = {"checkpoint": path, "state": state_path,
           "epoch_checkpoints": epoch_ckpts,
           "epoch_states": epoch_states, "history": history,
           "corpus_exploit_rate": corpus_rate, "datums": len(train_data),
           "args": vars(args)}
    (outdir / "warmstart.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"\n[{label}] checkpoint -> {path}")
    print(f"[{label}] state      -> {state_path}")
    print(f"[{label}] wrote {outdir / 'warmstart.json'}")
    print(f"\nnext: screen it, then set --p-exploit against what comes back.\n"
          f"  $PY check_suite.py --envs merchant --screen-only --screen {path} \\\n"
          f"      --screen-arms hole --screen-seeds 24 --doses 1.0\n"
          f"then both arms resume from this checkpoint, and the battery is read "
          f"here FIRST (the W row).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
