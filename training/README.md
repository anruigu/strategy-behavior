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

Both eval against a `random` opponent — see the "gotchas" section below for why.

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
   cp training/run_kuhn.sh training/run_multi.sh training/launch_run.sh "$SPIRAL_DIR/"
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
```

`launch_run.sh` activates `$SAT_VENV`, sources `$SAT_ENV_FILE`, points caches at
`$SAT_HF_HOME`, clears stale PyTorch JIT-extension locks, and then execs
whichever run script you asked for (`run_kuhn.sh` by default).

### Slurm (single node, 8x GPU)

```bash
SAT_HOME=/path/to/spiral-alignment-transfer sbatch training/sbatch_multi.sh
```

`sbatch_multi.sh` runs the multi-env curriculum only. Because slurm copies the
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
