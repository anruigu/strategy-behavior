# Training: SPIRAL self-play on Tinker

The same self-play loop as `../`, with [Tinker](https://tinker-docs.thinkingmachines.ai/)
doing sampling and gradients remotely instead of oat + vLLM + DeepSpeed on an
8xGPU node. Only the TextArena game loop runs locally, and that is pure-Python
and CPU-only — this arm launches from a laptop.

Structured after [Guanghan/JustTinker](https://github.com/Guanghan/JustTinker),
which is the same shape of thing for JustRL math: a local rollout/reward loop
driving `sampling_client.sample` → `tinker.Datum` → `forward_backward` →
`optim_step`. The differences are that a SPIRAL rollout is a multi-turn game
rather than one prompt, and the reward is a game outcome rather than a verified
answer. Where we diverge from JustTinker's actual code, it's called out in
`make_datum` (token alignment) and below.

```
config.py       arm/scale presets; every default maps to a flag in ../run_*.sh
selfplay.py     game loop, action parsing, RAE — no Tinker imports, so it runs offline
train_tinker.py Tinker clients, Datum assembly, training loop, eval, checkpoints
export_lora.py  tinker:// checkpoint -> PEFT adapter, for ../../evals/
run_*_tinker.sh one launcher per arm, mirroring ../run_kuhn.sh / ../run_multi.sh / ../run_pigdice.sh
```

## Read this before you use a checkpoint from here

**The Tinker arm is not another point on the `results/` curve.** Two things
change at once relative to the oat arms:

| | oat arms (`../`) | this arm |
|---|---|---|
| base model | `Qwen/Qwen3-4B-Base` | `Qwen/Qwen3.5-9B-Base` |
| what is trained | every parameter | a LoRA adapter (rank 32 by default) |

Tinker does not host Qwen3-4B-Base and does not do full finetuning, so neither
is optional. `results/README.md` compares `spiral-kuhn-step256` against a
`base-redo` MASK arm on the *same* base model; a Tinker checkpoint has no such
partner until you run one. **Serve `Qwen/Qwen3.5-9B-Base` untrained and run
MASK on it first** — otherwise any honesty delta you measure is confounded with
"different model, different finetuning method", which is two changes more than
the experiment is trying to isolate.

Check the live model list before assuming a base is available:
<https://tinker-docs.thinkingmachines.ai/tinker/models.json>, or ask your own
account with `ServiceClient().get_server_capabilities()` — the account list is
not identical to the docs list. It changes, and a model that has been removed
fails at client creation.

**If you want a Tinker-vs-local matched pair, the model is `Qwen/Qwen3-8B`.**
It is the only entry on Tinker's list that `$SAT_VENV` can also load: oat 0.2.1
hard-pins `vllm==0.8.4`, which knows `Qwen3ForCausalLM` / `Qwen3MoeForCausalLM`
only, so every `Qwen3.5-*` checkpoint (`model_type: qwen3_5`, arch
`Qwen3_5ForConditionalGeneration`) is rejected by transformers 4.51.3 before
vLLM sees it. `../run_kuhn_qwen3_8b.sh` is the local half of that pair. Note the
trade: Qwen3-8B is an instruct/hybrid-thinking model, so it needs `/no_think`
(see gotchas) — no *base* model exists on both sides.

Everything downstream of the base model — the games, the prompt template, the
action parser, the invalid-action penalty, RAE, the reward shaping — is imported
from or ported line-for-line out of `train_spiral.py`, so the *training signal*
is the same one the oat arms use. `test_parity.py` proves it: it binds spiral's
own `SelfPlayActor.extract_action` and `.prepare_trajectories` to a stub and
diffs them against this port's versions on identical inputs.

```bash
# needs $SAT_VENV, since importing train_spiral pulls oat + vllm
"$SAT_VENV/bin/python" test_parity.py --arm kuhn --games 24
# PASS: 64/64 matched   (also passes for --arm multi / --arm pigdice)
```

It has already earned its keep twice: `ignore_no_eos` sets a *loss mask* in
spiral and does not drop the turn (dropping it lets a live turn take the slot in
the `turns_per_step` subsample, so the batch carries more gradient than oat's
does), and the RAE baseline updates for a seat that never moved — which happens
constantly, because an invalid action on turn 0 ends the game before the
opponent acts.

## Setup

```bash
# spiral, for the envs/template/parsers. NOT pip install -e: that pulls
# oat + vllm + deepspeed, which is exactly what this arm avoids.
git clone https://github.com/spiral-rl/spiral "$SPIRAL_DIR"
# only if you will run the pigdice arm:
git -C "$SPIRAL_DIR" apply "$SAT_HOME/training/patches/action-parsers.patch"

python3.11 -m venv "$SAT_TINKER_VENV"      # defaults to training/tinker/.venv
"$SAT_TINKER_VENV/bin/pip" install -r requirements.txt

echo 'TINKER_API_KEY=...' >> "$SAT_ENV_FILE"   # ../../.env, see ../../env.example
```

`../patches/components-timeout.patch` is **not** needed here — it fixes an oat
learner deadlock in `spiral/components.py`, and this arm never imports that
module.

You do **not** need `OPENROUTER_API_KEY`: like the oat runs, eval opponents are
`random` (upstream's default LLM opponent is retired and 404s).

## Running

```bash
# free, offline, ~1 minute: plays real games with a random-action stub sampler.
# Verifies template + action parser + reward overrides + Datum alignment.
./run_kuhn_tinker.sh --scale smoke --dry-run

# real runs
./run_kuhn_tinker.sh                       # KuhnPoker only,  400 steps
./run_multi_tinker.sh                      # TicTacToe + KuhnPoker + SimpleNegotiation
./run_pigdice_tinker.sh                    # PigDice control
./run_kuhn_tinker.sh --scale short         # 64 steps, for finding out it works

# resume from a saved training state
./run_kuhn_tinker.sh --resume tinker://.../state/spiral-tinker-kp-self-play-step128
```

**Always dry-run a new arm or model first.** A mismatched prompt template or
action parser makes every game a one-turn invalid-action forfeit; the run does
not crash, it just burns sampled tokens — which you are billed for — and the win
rate sits at chance. The dry run catches that for nothing.

Each run writes `$SAT_TINKER_OUT/<run-name>-<timestamp>/`:

- `config.json` — the resolved config, including the seed
- `history.jsonl` — one record per policy step (metrics + eval)
- `checkpoints.jsonl` — `tinker://` paths. **Keep this.** A `tinker://` path is
  not reconstructible from anything on your disk.

## Getting a checkpoint into the MASK pipeline

`../../evals/` runs MASK against a local vLLM server, which cannot open a
`tinker://` path. Two hops:

```bash
python export_lora.py \
    --checkpoints "$SAT_TINKER_OUT/spiral-tinker-kp-self-play-.../checkpoints.jsonl" \
    --step 256 --out "$SAT_CKPT_DIR/spiral-tinker-kuhn-step256"

../../evals/serve_tinker_ckpt.sh "$SAT_CKPT_DIR/spiral-tinker-kuhn-step256" \
    spiral-tinker-kuhn-step256 8000 0
```

The PEFT adapter is two small files; the base weights stay separate, so
`serve_tinker_ckpt.sh` needs the base model name to match what the run trained
on (it is in each `checkpoints.jsonl` record, and `export_lora.py` prints it).
From there the rest of the pipeline is unchanged — it only ever sees the served
model name:

```bash
./run_mask.sh spiral-tinker-kuhn-step256
python compare_mask_arms.py <tinker-base-arm> spiral-tinker-kuhn-step256
```

## How the oat flags map

`config.py` carries the full table in its docstring. The parts worth knowing
without opening it:

- **`--rollout_batch_size 128` counts turns, not games.** `SelfPlayActor.step`
  plays whole games until it has at least that many model turns, then
  subsamples to exactly that many. `turns_per_step` does the same, so a 128-turn
  batch is ~8-13 KuhnPoker games and ~2-3 PigDice games.
- **`--num_ppo_epochs 2` with `--train_batch_size 128`** = two optimizer steps
  per collected batch. Here that is two (`forward_backward` × N chunks →
  `optim_step`) passes; chunking is a request-size knob only, since
  `forward_backward` accumulates and `optim_step` applies.
- **`--beta 0`** — no KL term. Tinker's `ppo` loss has no `kl_coef` anyway.
- **`--gamma 1`** — every turn of a game carries the same advantage.
  `use_intermediate_rewards` still discounts by `gamma**turns_from_end`, so it
  is a no-op at the default and is the first knob to reach for if credit
  assignment across a 50-turn PigDice game looks like the problem.
- **RAE (`use_role_baseline`)** is SPIRAL's actual contribution to the
  optimization and is on by default. A GRPO-style group baseline does not work
  here: the two seats of a zero-sum game have systematically different expected
  returns, so pooling them subtracts a baseline that is wrong for both.

## Gotchas

- **A thinking model needs `/no_think`, and it is not optional.** spiral's
  `qwen3` template was written for a base model. Point it at a hybrid-thinking
  instruct model (any `Qwen/Qwen3-*`, `Qwen3.5-*`, `Qwen3.6-*` that is not
  `-Base`) and it opens a `<think>` block that does not close inside
  `generate_max_length`, so no `\boxed{}` is emitted, `extract_action` falls
  through to the raw response, and every game is a turn-1 forfeit. Measured on
  `Qwen/Qwen3-8B`, KuhnPoker, identical prompt:

  | | games/step | invalid actions | game length | resp tokens | step time |
  |---|---:|---:|---:|---:|---:|
  | stock template | 512 (hit the cap) | **99.8%** | 1.00 | 837 | 1378 s |
  | `+ /no_think` | 8 | **6.7%** | 9.4 | 663 | 114 s |

  `--thinking-mode auto` (the default) turns it on for those models and off for
  `-Base` ones. The local arm needs the same marker or the pair is not matched —
  `../patches/qwen3-no-think-template.patch` adds an `SPIRAL_NO_THINK=1` switch
  to `spiral/template.py` (a no-op when unset). The marker is appended to the
  *rendered prompt* only; the per-env action parsers read the last line of the
  observation, so they must keep seeing it untouched.
- **Concurrency is where all the throughput is.** An episode is sequential —
  turn *t+1*'s observation depends on turn *t*'s action — so each game is one
  thread blocking on one `sample()` future. With `--max-concurrent-games 32` and
  ~12 turns per KuhnPoker game, a 128-turn batch costs ~12 sequential round
  trips instead of ~128. Raise it if collection dominates `step_time` in the log
  line (which prints the roll/train split); lower it if you are rate-limited.
- **The stop sequence is load-bearing.** spiral's `qwen3` template is ChatML and
  the prompt ends at `<|im_start|>assistant\n`, but on a *base* model nothing
  guarantees an EOS. Without an explicit `<|im_end|>` stop, every turn runs to
  `generate_max_length`, every turn is then dropped by `ignore_no_eos`, and the
  batch is empty — with no error. `TinkerSampler` refuses to start if the
  tokenizer has no `<|im_end|>`.
- **PigDice needs `use_llm_obs_wrappers=True`** (the arm preset sets it) and
  fails silently without it, exactly as in `../README.md`. It is also ~5x longer
  per episode than the other arms, so at equal `--turns-per-step` it costs
  several times as much, and it is the arm most likely to hit `--max-turns 50`
  and score draws — watch `outcome/turn_limit` in the step log.
- **`context_limit` is a Tinker-only outcome.** oat let vLLM's `--max_model_len`
  handle an overlong prompt; a Tinker `sample()` whose prompt exceeds the window
  raises instead, which would take down every game sharing the thread pool. We
  score it as a draw and count it, so it shows up as a metric rather than a
  crash. If `outcome/context_limit` is non-zero, raise `--max-model-len` (up to
  the model's window) or lower `--generate-max-length`.
- **Token alignment differs from JustTinker on purpose.** JustTinker builds
  `target_tokens` and `logprobs` one position further right than
  `tokens[1:]`, which trains against a target already visible in the model's own
  input. We follow the tinker-cookbook convention; the derivation is in the
  `make_datum` docstring, and `--dry-run` asserts it.
- **No math/general-reasoning eval.** `train_spiral.py` also evaluates on math
  benchmarks via `--eval_data`; that path is not ported, since this repo's eval
  battery is MASK/MACHIAVELLI (`../../evals/`, `../../docs/methodology.md`).
  Eval here is win rate vs a uniform-random legal-move opponent, which answers
  "did the policy learn the game at all" and nothing stronger.
