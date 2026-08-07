# Training: SPIRAL self-play

Trains the base model on [SPIRAL](https://github.com/spiral-rl/spiral) self-play
(oat-based zero-sum RL), producing the checkpoints that `../evals/` then probes for
alignment/deception transfer (MASK honesty, MACHIAVELLI).

- **Base model:** `Qwen/Qwen3-4B-Base`.
- **Algorithm:** SPIRAL — the model plays both sides of a zero-sum game against
  itself; oat runs the PPO-style policy update over the resulting rollouts.
- **Curriculum:**
  - `run_kuhn.sh` — single-env: **KuhnPoker-v1** only (imperfect-information
    bluffing game). Eval'd throughout training on TicTacToe-v0 + KuhnPoker-v1.
  - `run_multi.sh` — multi-env: **TicTacToe-v0 + KuhnPoker-v1 +
    SimpleNegotiation-v1**, trained concurrently, to test whether transfer
    effects are specific to zero-sum bluffing or generalize across a broader
    game mix (including a natural-language negotiation game).
  - `run_pigdice.sh` — control: **PigDice-v1** only. Pig is two-player and
    zero-sum like KuhnPoker, but its uncertainty is *stochastic* (a die) rather
    than *informational* (a hidden card), and there is no opponent model to
    misrepresent. It therefore separates "trained on a risky zero-sum game"
    from "trained on a game where bluffing pays" — a separation a TicTacToe
    control cannot make, since TicTacToe has no uncertainty at all.
  - `run_multigame_social.sh` — the 0806 multigame **social arm**:
    **TruthAndDeception-v1 + KuhnPoker-v1 + SimpleNegotiation-v1 +
    LiarsDice-v1-2d**, trained concurrently. Four two-player games in which
    misrepresenting your private state pays, to concentrate the deception
    signal rather than dilute it with a neutral game as `run_multi.sh` does.
    Needs `patches/multigame-social-envs.patch` as well as
    `patches/action-parsers.patch`.

All eval against a `random` opponent — see the "gotchas" section below for why.

## Two ways to run it

- **oat + vLLM + DeepSpeed on 8x GPU** — everything in this directory. This is
  what produced the checkpoints in `../results/`.
- **[Tinker](https://tinker-docs.thinkingmachines.ai/)** — [`tinker/`](tinker/README.md).
  Same self-play loop, same games, same reward shaping; sampling and gradients
  happen remotely, so only the (CPU-only) TextArena game loop runs locally and
  the whole arm launches from a laptop. It trades away the base model —
  Tinker does not host `Qwen3-4B-Base` and does LoRA rather than full
  finetuning — so its checkpoints need their own base-model MASK arm and are
  **not** comparable to the numbers in `../results/`. Read
  [`tinker/README.md`](tinker/README.md) before using one.

The rest of this file is the oat path.

## Setup

1. **Clone spiral** and apply the timeout patch:

   ```bash
   git clone https://github.com/spiral-rl/spiral "$SPIRAL_DIR"
   cd "$SPIRAL_DIR"
   git apply /path/to/spiral-alignment-transfer/training/patches/components-timeout.patch
   ```

   The patch fixes `spiral/components.py`: it imports `Pool` from
   `multiprocessing` but catches the builtin `TimeoutError` in
   `MATHOracle.get_reward`. `multiprocessing.Pool.apply_async(...).get(timeout=...)`
   actually raises `multiprocessing.context.TimeoutError` (a `ProcessError`),
   which the builtin `TimeoutError` (an `OSError`) does **not** match — so the
   `except TimeoutError` clause is dead code. A slow reward grade kills learner
   rank 0 outright instead of being caught, and every other rank then hangs
   forever on its next collective op. The patch imports `TimeoutError` from
   `multiprocessing` alongside `Pool` so the except clause actually catches it.

   **For `run_pigdice.sh` or `run_multigame_social.sh`**, also apply:

   ```bash
   git apply /path/to/spiral-alignment-transfer/training/patches/action-parsers.patch
   # multigame social arm only:
   git apply /path/to/spiral-alignment-transfer/training/patches/multigame-social-envs.patch
   ```

   Upstream spiral vendors several envs it never finished wiring into the
   trainer — the ports stop at `spiral/envs/` and skip
   `_VALID_ACTION_PARSER` in `spiral/agents/utils.py`. Each one fails only when
   the first rollout reaches it, with `NotImplementedError: valid action parser
   not implemented for <env>` out of `agent_act()` (and `RandomAgent(<env>)`
   fails identically at eval). `action-parsers.patch` adds the two we need:

   - **`PigDice-v1`** — constant action space, `[roll]` / `[hold]`.
   - **`LiarsDice-v1`** (and the round-capped `LiarsDice-v1-2d`) — *parametric*
     action space, so the parser has to enumerate every legal `[Bid: Q, F]`
     rather than describe it, because `extract_action()` rejects anything not
     literally in the list. Two things make that harder than it looks, and both
     produce silent invalid-move losses rather than errors: the standing bid
     resets between rounds while `LLMObservationWrapper` keeps the previous
     round's `Current bid:` line in the text (so the parser anchors on the last
     `Your new dice are:` re-roll marker), and the per-seat dice counts are
     printed once at the start and go stale as dice are lost (so it re-reads
     the latest `Remaining dice:` block).

   `multigame-social-envs.patch` registers `LiarsDice-v1-2d` and adds
   `TruthAndDeception-v1` to `agent_act`'s free-form-action list — T&D's
   persuasion turns are open text and only its final `[Fact 1]`/`[Fact 2]`
   guess is constrained, so it has no single action space to enumerate and
   routes through `extract_chat_action` the way SimpleNegotiation already does.

   `sbatch_pigdice.sh` and `sbatch_multigame_social.sh` both check their wiring
   up front, so a job on an unpatched checkout dies in seconds rather than
   after the fused_adam build.

2. **Create the training venv outside the checkout** (python 3.10; see
   [gotchas](#gotchas) for why it can't live inside `$SPIRAL_DIR`):

   ```bash
   python3.10 -m venv "$SAT_VENV"
   source "$SAT_VENV/bin/activate"
   pip install -e "$SPIRAL_DIR"   # oat, vllm, textarena, deepspeed, ...
   ```

3. **Copy the run scripts into the checkout** (they invoke `train_spiral.py`,
   which only exists there):

   ```bash
   cp training/run_kuhn.sh training/run_multi.sh training/run_pigdice.sh \
      training/run_multigame_social.sh training/launch_run.sh "$SPIRAL_DIR/"
   ```

4. Copy `env.example` to `.env` at the repo root (or wherever `$SAT_ENV_FILE`
   points) and fill in `WANDB_API_KEY` (required — every run script passes
   `--use-wb`). `OPENROUTER_API_KEY` is not needed for training; see gotchas.

5. Review `../config.sh` and override any of the `SAT_*` variables you need
   (venv location, save path, HF cache, etc.) by exporting them before running.

## Running

### Single node

```bash
export SAT_HOME=/path/to/spiral-alignment-transfer   # if not auto-detected
cd "$SPIRAL_DIR"
SAT_RUN_SCRIPT=run_kuhn.sh ./launch_run.sh    # KuhnPoker only (default)
SAT_RUN_SCRIPT=run_multi.sh ./launch_run.sh   # TicTacToe + KuhnPoker + SimpleNegotiation
SAT_RUN_SCRIPT=run_pigdice.sh ./launch_run.sh # PigDice control
SAT_RUN_SCRIPT=run_multigame_social.sh ./launch_run.sh  # 0806 social arm
```

`launch_run.sh` activates `$SAT_VENV`, sources `$SAT_ENV_FILE`, points caches at
`$SAT_HF_HOME`, clears stale PyTorch JIT-extension locks, and then execs
whichever run script you asked for (`run_kuhn.sh` by default).

### Slurm (single node, 8x GPU)

```bash
SAT_HOME=/path/to/spiral-alignment-transfer sbatch training/sbatch_multi.sh
SAT_HOME=/path/to/spiral-alignment-transfer sbatch training/sbatch_pigdice.sh
SAT_HOME=/path/to/spiral-alignment-transfer sbatch training/sbatch_multigame_social.sh
```

`sbatch_multi.sh` runs the multi-env curriculum, `sbatch_pigdice.sh` the
PigDice control, `sbatch_multigame_social.sh` the 0806 social arm. Because slurm copies the
submitted script to a spool directory before executing it, `SAT_HOME` cannot be
auto-detected from the script's own path — it **must** be exported (or passed
via `sbatch --export=SAT_HOME=...`) or the job fails fast with a clear error.
The job's `#SBATCH --output`/`--error` use `%j` only (job ID); slurm writes
them relative to the submission directory, so no path needs hardcoding.

## Gotchas

These are distilled from the comments in the scripts themselves — read the
scripts for the full detail.

- **Venv must live outside the spiral checkout.** `textarena` pulls in `nltk`,
  whose import guard rejects any site-packages module whose origin resolves
  under the current working directory. `train_spiral.py` runs from the repo
  root, so an in-repo `.venv` makes every site-packages import look like a cwd
  import and `import textarena` dies trying to import `regex`. Always create
  `$SAT_VENV` outside `$SPIRAL_DIR`.
- **`$HOME` is node-local on slurm compute nodes**, and may not even resolve to
  a valid user. `node_env.sh` (repo root) redirects `$HOME` and every
  torch/triton cache to `/tmp`, while keeping `$SAT_HF_HOME` on shared storage
  so the ~8GB model weights are downloaded once and reused across nodes.
  `sbatch_multi.sh` sources it; `launch_run.sh` (single-node) does the
  equivalent inline.
- **PigDice requires `--use_llm_obs_wrappers True`.** This is the one place
  `run_pigdice.sh` diverges from a TicTacToe-style control, which used `False`.
  TicTacToe redraws the entire board in its latest message, so
  `FirstLastObservationWrapper` (first observation + last) loses nothing.
  PigDice does not: the running scores arrive in a turn-rotation message and
  the turn total in a per-roll message, and First+Last drops both. Under
  `False` the player sees only the static rules prompt and "Available actions:
  '[roll]' or '[hold]'" — it cannot see its own turn total, so every roll/hold
  decision is blind and the run is worthless. It fails *silently*: nothing
  errors, the win rate just sits at chance.
- **PigDice episodes are ~5x longer than the other arms'.** At
  `winning_score=50` a game is ~50–60 model calls (measured over 300 self-play
  games: mean 57.6 random, 48.0 for a hold-at-20 policy), against ~9 for
  TicTacToe and ~10–20 for KuhnPoker. Same `rollout_batch_size`, several times
  the generated tokens per policy step — budget wall-clock accordingly.
- **`run_pigdice.sh` uses `--save_steps 64`, not 16.** 25 checkpoints x 7.6GB
  is ~190GB per run and `/workspace` is shared; 64 gives the
  64/128/192/256/320/384 ladder plus the forced end-of-run save (oat calls
  `eval_and_log(save=True)` after the training loop, so the final step is
  always checkpointed whatever the cadence) — 7 checkpoints, ~53GB. See
  `../evals/README.md` for when to bound disk here vs. in `sync_checkpoints.sh`.
- **Checkpoints land under `$SAT_SAVE_PATH`**, which itself may be node-local
  or ephemeral depending on your cluster. Mirror them to durable storage with
  `../evals/sync_checkpoints.sh "$SAT_SAVE_PATH" <run-label>` running
  alongside training (it polls for completed checkpoint dirs and copies them
  out, optionally to S3 — see that script's header for the tiering logic).
- **`fused_adam` must be pre-built single-process.** DeepSpeed JIT-builds its
  `FusedAdam` CUDA extension on first use, guarded by a `torch` `FileBaton`
  lock file. With 8 learner ranks starting simultaneously on a fresh node, one
  rank's build can be imported half-written by the others, or a killed rank
  can leave the lock file behind so every later rank blocks on it forever.
  `sbatch_multi.sh` builds it once, serially, before launching; `launch_run.sh`
  additionally clears any stale lock left over from a previous killed run.
  `node_env.sh` also seeds a prebuilt `fused_adam.so` from `$SAT_PREBUILT_DIR`
  onto fresh nodes that can't compile it themselves (no dev headers).
- **`--eval_opponent_names random`, not the upstream default.** Upstream
  defaults to `google/gemini-2.0-flash-lite-001` as the eval opponent, which is
  retired and now 404s on OpenRouter — that aborts the whole job at the
  step-0 eval. Self-play training never calls an external opponent, so
  `OPENROUTER_API_KEY` is not required for these run scripts (only for the
  MASK judge in `../evals/`).
