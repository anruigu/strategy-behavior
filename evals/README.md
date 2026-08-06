# evals

Two evals for the SPIRAL self-play -> alignment/deception transfer study:

- **MASK** ([centerforaisafety/mask](https://github.com/centerforaisafety/mask)) -- implemented, results in `../results/`.
- **MACHIAVELLI** ([aypan17/machiavelli](https://github.com/aypan17/machiavelli)) -- checked out and cloned into `$MACHIAVELLI_DIR`, but not yet run.

All scripts here are driven by `../config.sh`; read it (and `../env.example`) before running anything. Every path below is an env var with a repo-relative default -- override by exporting it, or by editing `config.sh`.

## Setup

```bash
# external checkouts
git clone https://github.com/centerforaisafety/mask "$MASK_DIR"
git clone https://github.com/aypan17/machiavelli "$MACHIAVELLI_DIR"

# MASK pins its own (conflicting) deps, so it gets its own venv
python3.10 -m venv "$SAT_MASK_VENV"
"$SAT_MASK_VENV/bin/pip" install -r "$MASK_HARNESS/requirements.txt"

# fetch MASK's dataset CSVs
cd "$MASK_HARNESS" && "$SAT_MASK_VENV/bin/python" download.py

# secrets: OPENROUTER_API_KEY (judge) + optional AWS creds (S3 checkpoint tier)
cp ../env.example ../.env  # then fill it in; see config.sh for $SAT_ENV_FILE
```

## Serving a model

Both eval pipelines generate against a local vLLM OpenAI-compatible server, not the training process itself.

```bash
# base model, defaults to Qwen/Qwen3-4B-Base on GPU 0 / port 8000
./serve_base.sh [model] [served-name] [port] [gpu]

# a trained checkpoint
./serve_ckpt.sh <checkpoint-path> [served-name] [port] [gpu]
```

Both pin `--num-gpu-blocks-override` to hard-cap the KV cache so the server's footprint is predictable regardless of what else is resident on the card (see comments in `serve_base.sh`).

## MASK pipeline

MASK measures honesty under pressure: a model states a belief, is then pressured to contradict it, and a judge scores whether it does. The pipeline is 4 stages, run against one served model at a time (an **arm**, e.g. `base-redo`, `spiral-kuhn-step256`):

1. **generate** -- sample responses from the local vLLM server (`generate_responses.py`)
2. **judge** -- score belief + contradiction via an external judge on OpenRouter (`evaluate.py`)
3. **metric** -- compute per-row dishonesty (`metric.py`)
4. **aggregate** -- roll up into `all_results.json` (`process_metrics.py`)

Generation talks to `OPENAI_BASE_URL=http://localhost:<port>/v1`; the judge is switched to OpenRouter (`MASK_JUDGE_BASE_URL`) since MASK's own OpenAI-key path 401s here. The judge model defaults to `$MASK_JUDGE_MODEL` (`openai/gpt-4.1` in `config.sh`) -- **not** gpt-4o, which on this OpenRouter account is served via Azure and content-filters (HTTP 400) a chunk of MASK's lying/disinformation prompts, silently dropping those rows.

Two ways to run it:

```bash
# ad hoc, against a server you already started
./run_mask.sh <served-model-name>
./run_mask_port.sh <served-model-name> <port>

# slurm: serves the model AND runs the full pipeline for one arm
export SAT_HOME=/path/to/spiral-alignment-transfer   # BASH_SOURCE doesn't resolve once slurm copies the script
sbatch sbatch_mask.sh <arm-name> <model-path-or-hf-id>
```

`sbatch_mask.sh` copies `$MASK_HARNESS` into `$SAT_RUNS_DIR/<arm-name>` and runs entirely from that copy -- arms run concurrently and would otherwise race on `csv_data/{responses,evaluated,metrics}` and `all_results.json`. It also purges any output dirs inherited from the checkout (keeping the input `csv_data/*.csv`) so a stale run's responses never get re-judged under a new arm.

### Comparing arms: the belief-elicitation confound

MASK's headline honesty score is `100 - %dishonest`, but a row only counts as dishonest if the model *first stated a belief* that its pressured answer then contradicts. When the judge can't extract a belief, it's recorded as `'C'` and the row drops out of the honesty computation entirely.

The base `Qwen3-4B-Base` (not instruction-tuned) fails belief elicitation far more often than a SPIRAL-trained checkpoint does. That means naive per-arm honesty is computed over *different subsets of the data* for each arm -- enough on its own to manufacture a "SPIRAL reduces honesty" result out of nothing but improved instruction-following/format compliance.

`compare_mask_arms.py` makes this explicit by reporting, per arm:

1. `%C` -- how often belief elicitation failed at all
2. `honesty(all)` -- the naive number, comparable to published tables
3. `honesty` on the **both-valid intersection** -- restricted to `task_id`s where *both* arms produced an extractable belief; the only apples-to-apples comparison

```bash
cd evals
python compare_mask_arms.py base-redo spiral-kuhn-step256
```

Reads `$SAT_RUNS_DIR/<arm>/csv_data/evaluated/*.csv` for each arm named on the command line.

## Checkpoint plumbing

`$HOME` (and thus oat's default `--save_path`) is node-local ephemeral storage on this cluster -- it doesn't survive a restart and isn't visible from other nodes, so a checkpoint written there can't even be evaluated elsewhere.

```bash
# background loop: mirror + optionally upload as new checkpoints land
./sync_checkpoints.sh <src-save-path> <run-label> [interval-seconds]
```

- **Tier 1 (always):** mirror completed checkpoints to `$SAT_CKPT_DIR/<run-label>/<step>` (colon-free step dirs; the NFS volume rejects `:`).
- **Tier 2 (optional):** also upload to `s3://$S3_CHECKPOINT_BUCKET/$S3_PREFIX/`, gated by `S3_CHECKPOINT_BUCKET` being set and throttled by `S3_UPLOAD_EVERY` (a full run's checkpoints are ~190GB; uploading every 64th step keeps S3 spend down while `$SAT_CKPT_DIR` still holds every one).

S3 uploads go through `s3_upload_dir.py <local-dir> <bucket> <key-prefix>`, a small multipart/concurrent uploader mirroring SkyRL-Fleet's `s3_checkpoints.py` convention (one key per file under `<key-prefix>/<relative-path>`); credentials come from `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` in the dotenv at `$SAT_ENV_FILE`.

## Results

See `../results/` for the actual numbers, and `../config.sh` + `../env.example` for everything configurable/needed before running these scripts.
