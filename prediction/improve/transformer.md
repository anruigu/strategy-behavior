The transformer workers are separate from the first study. All real extraction, head fitting, adaptation, and checkpoint forecasting run inside Fleet API jobs. Importing the module and running its synthetic tests never downloads or calls a real model.

The fixed protocol is `prediction/results/improve-20260910/transformer-protocol.json`, pinned to Qwen/Qwen3-4B revision `1cfa9a7208912126459214e8b04321603b3df60c`. It was encoded before improvement comparisons. Qwen's [model card](https://huggingface.co/Qwen/Qwen3-4B) documents its decoder and Transformers support; implementation uses the official [Qwen3 model](https://huggingface.co/docs/transformers/model_doc/qwen3) and [PEFT LoRA](https://huggingface.co/docs/peft/developer_guides/lora) interfaces. A technical amendment requires an explicit source/protocol change before comparative scores; the worker does not silently change precision, truncate prompts, or select another checkpoint.

Inputs are data.py's shared outcome-free text: payoffs, fixed protocol, and ordered identities, without family labels, game IDs, or outcomes. One user-message chat template disables thinking and adds the assistant prefix. No tokens are generated. The final hidden state at the last non-padding token feeds a three-output probability head. Inputs longer than 512 tokens fail preflight. Frozen BF16 embeddings can be shared across folds because their cache contains only input text and model/tokenization identity. The cache never contains training targets, masks, family labels, or counts.

Each fold fits its own training-example mean and standard deviation; constant embedding dimensions use scale one. No PCA or other dimensionality reduction is fitted. A linear sigmoid head minimizes fractional-binomial cross-entropy with fixed L2=.01, using full-batch LBFGS (at most 200 iterations). Intercepts are unpenalized. For each target, event weights sum to one within each supported canonical shape; the objective then averages supported shapes and targets. All normalization is recomputed on training rows. Missing targets have zero loss mass, and an entirely unsupported training target yields null forecasts.

The adapted model starts from that same fold's fitted head and scaler. The frozen decoder receives rank-8 LoRA adapters (alpha16, dropout.05) on every q_proj and v_proj. Adapter and head optimization uses two fixed epochs, microbatch4 accumulated to32, AdamW adapter LR2e-4/head LR1e-4, adapter decay.01, head L2=.01, cosine schedule with10% warmup, and gradient clipping at1. Gradient checkpointing is enabled. The final epoch is always selected; no outer labels, validation scores, or best-checkpoint search are used. Seed20260910 is fixed. One seed and fixed-forecast bootstrap intervals do not quantify unrestricted training variability.

The ten fits are seven leave-family-out folds, within-family interpolation, within-family extrapolation, and full72-shape training. The full fit's saved test forecasts are for the already-inspected21-shape development cohort; they are not fresh prospective results.

Typical Fleet commands, with project root as working directory:

```bash
PREDICTION_FLEET_TRAINING_RUN=1 python -B -m prediction.improve.transformer preflight \
  --fleet-run-id RUN_ID --data DATA/data.json --protocol transformer-protocol.json \
  --model-path MODEL_SNAPSHOT --model-manifest MODEL_MANIFEST --out preflight.json

PREDICTION_FLEET_TRAINING_RUN=1 python -B -m prediction.improve.transformer run \
  --fleet-run-id RUN_ID --data DATA/data.json --folds DATA/folds.json \
  --protocol transformer-protocol.json --model-path MODEL_SNAPSHOT \
  --model-manifest MODEL_MANIFEST --embedding-cache EMBEDDING_CACHE \
  --out TRANSFORMER_OUTPUT --methods both --max-runtime-seconds 18000
```

All paths must resolve under `/shared/allie` or its cluster alias `/mnt/sfs/allie`. Root supplies the Fleet run identity and launches jobs through the API. The local model manifest must contain `model_id`, `revision`, and `files: {relative_path: sha256}`. Model files are verified before use and loaded locally with remote code disabled. Runtime package versions, GPU model, token lengths, and checkpoint/source hashes are recorded.

`--methods frozen` runs just frozen heads; `--methods lora` requires the completed same-fold frozen artifacts in the same output root. `--fold-ids full` or explicit fold IDs bound a submission. `--resume` validates existing source/data/protocol contracts and completed file hashes. LoRA optimizer, adapter/head weights, scheduler, and RNG states are checkpointed every20 optimizer steps and at epoch ends. A runtime limit pauses at an optimizer boundary and leaves a checkpoint; completed fits are reused without overwriting. `progress.jsonl` exposes fold starts, optimization loss/gradient diagnostics, checkpointed progress, and completion. Root must enforce the aggregate six GPU-hour limit across submissions/retries.

Each `TRANSFORMER_OUTPUT/{frozen,lora}/FOLD/` contains the reusable `head.npz`, `artifact.json`, `contract.json`, `complete.json`, `forecasts.jsonl`, and `forecast-manifest.json`; adapted fits also have `adapter/` and checkpoints. The forecast rows use the shared keys row_id, group_id, game_id, model, opponent, method, split, fold_id, target, prediction. Structurally undefined targets and missing training support are explicitly null with distinct statuses. Original episode-level scoring happens separately; the worker never reports held-out scores.

Forecast new outcome-free metadata with the completed fit:

```bash
PREDICTION_FLEET_TRAINING_RUN=1 python -B -m prediction.improve.transformer forecast \
  --fleet-run-id RUN_ID --fit TRANSFORMER_OUTPUT/lora/full --metadata fresh-examples.json \
  --model-path MODEL_SNAPSHOT --model-manifest MODEL_MANIFEST \
  --embedding-cache EMBEDDING_CACHE --out NEW_IMMUTABLE_FORECAST_DIR --split fresh
```

Metadata accepts a list of examples or `examples`/`metadata_examples` lists. It needs input_text, IDs/identities, and structural applicability; no outcomes are read. Existing forecast output directories are refused. Freeze every required full/family-excluded forecast before player collection.

Run focused synthetic tests with `python -B -m unittest prediction.improve.test_transformer -v`. The standard NumPy tests run locally. Torch pooling, fractional-loss gradients, and microbatch accumulation tests are marked skipped when Torch is absent and must also run in the Fleet runtime. They use synthetic tensors only and perform no actual study training.
