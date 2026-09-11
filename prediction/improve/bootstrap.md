# Technical dependency repair

Fleet entrypoint (never launch locally):

```bash
python -B -u prediction/improve/bootstrap.py --run-root /mnt/sfs/allie/strategy-behavior/prediction/results/improve-20260910 --runtime-dir /mnt/sfs/allie/strategy-behavior/prediction/results/improve-20260910/fleet-runtime/retry-1
```

The job must supply `FLEET_RUN_NAME`, `PREDICTION_FLEET_TRAINING_RUN=1`, the original absolute `PREDICTION_EXPERIMENT_DEADLINE`, and writable shared paths for TMPDIR and all six checked cache/config locations. The bootstrap does not submit jobs. It extracts only the exact staged SciPy1.15.3 CPython3.12 Linux x86_64 wheel, validates its pinned SHA256 against the dependency manifest, rejects unsafe archive members and packages that could shadow Torch, and uses a new `scipy-overlay` directory. It never invokes pip, resolves dependencies, downloads packages, or installs the staged PEFT/Accelerate wheels.

Before the unchanged archived `train_job.py --resume`, it checks SciPy arithmetic and the existing image's Qwen3/PEFT stack with a tiny random CUDA BF16 model: native SDPA, the specified q_proj/v_proj LoRA modules, nonreentrant checkpointing, finite nonzero backward gradients, and adapter save/reload. The tiny check reads no study outcomes or pretrained weights and performs no optimizer step. Failures retain package versions/origins in `bootstrap-status.json` and tracebacks in `bootstrap.log`; unsupported existing dependencies stop the attempt. The worker inherits only overlay + frozen-source PYTHONPATH, and Torch's origin/version must stay unchanged.

Existing attempt reports are never overwritten by a later invocation: use a new runtime directory for another attempt. Original failed worker reports remain the root supervisor's responsibility to archive; the unchanged worker's explicit resume records its previous status. The original experiment deadline bounds the child process, with the parent job's outer timeout as the external limit. Local verification is `python -B -m unittest prediction.improve.test_bootstrap` and only exercises synthetic archive/guard logic.

## cuDNN SDPA compatibility amendment

Retry2 reached the tiny CUDA forward but failed with `cuDNN Frontend ... No valid execution plans built` under the actual Torch2.11.0+cu128 image. Retry3 disables only cuDNN SDPA through `torch.backends.cuda.enable_cudnn_sdp(False)`. Native Flash, memory-efficient, and math SDPA flags remain exactly as supplied by the image; the worker still requests `attn_implementation='sdpa'`, with unchanged precision/model/protocol/hyperparameters. Bootstrap status and log record all four flags before and after the amendment.

The tiny model now exercises head dimension128 and a4:1 query/key-value head ratio, two layers, and unequal right-padded sequence lengths; the backward check masks padding. A generated, hashed `worker_entry.py` applies and verifies the same backend policy in the child interpreter before `runpy.run_path` executes the archived worker with its original `--run-root ... --resume` arguments. It checks frozen worker bytes and unchanged Torch origin/version, and writes `worker-backend.json` with backend flags and source hashes. Existing bootstrap archives and failed reports are preserved. This is a numerical backend compatibility repair before empirical comparisons, not a change to the prescribed learned methods.
