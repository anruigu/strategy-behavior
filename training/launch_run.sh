#!/usr/bin/env bash
# launch_run.sh — wrapper around the repo's unmodified run.sh.
#
# run.sh calls bare `python`, so the venv must be on PATH before it runs.
# Everything else here is environment the README assumes you already exported.
set -euo pipefail
# Copied out of this repo alongside run.sh, so if SAT_HOME doesn't auto-detect,
# export it first: SAT_HOME=/path/to/spiral-alignment-transfer.
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
source "$SAT_HOME/config.sh"
cd "$(dirname "$0")"

# 1. Python 3.10 venv (repo targets 3.10; box default is 3.12).
#    The venv MUST live outside the repo. nltk's inisec import guard blocks any
#    module whose origin resolves under the cwd, and run.sh runs from the repo
#    root -- an in-repo .venv makes every site-packages import look like a cwd
#    import, so `import textarena` dies on `regex`.
source "$SAT_VENV/bin/activate"

# 2. Credentials. Sourced from the persistent env file rather than hardcoded.
set -a
. "$SAT_ENV_FILE"
set +a

# 3. Keep the 8GB model download on /workspace so it survives a /home wipe.
export HF_HOME="$SAT_HF_HOME"

# 3b. Diagnostics only -- does not change the experiment.
#     Python block-buffers stdout when it is a pipe (launchpad pipes every node
#     through decorate_output), so a hung learner emits nothing at all and the
#     log looks identical to "no progress yet". Force line buffering.
export PYTHONUNBUFFERED=1
export NCCL_DEBUG=WARN

# 3c. nvcc lives at /usr/local/cuda/bin but is not on PATH by default. DeepSpeed
#     JIT-builds FusedAdam on first use and needs both nvcc and ninja visible.
export CUDA_HOME=/usr/local/cuda
export PATH="$CUDA_HOME/bin:$PATH"

# 3d. Clear stale PyTorch JIT extension locks.
#     All 8 learner ranks race to build fused_adam. torch guards the build with a
#     FileBaton: one rank creates `lock` and builds, the rest poll until it is
#     deleted. If the holder is killed (or never releases), the lock outlives it
#     and every subsequent rank blocks forever -- a silent hang with the GPUs
#     allocated but idle, which is exactly what stalled runs 3 and 4.
for lock in "$HOME"/.cache/torch_extensions/*/*/lock; do
    [ -e "$lock" ] || continue
    if ! fuser "$lock" >/dev/null 2>&1; then
        echo "clearing stale JIT lock: $lock"
        rm -f "$lock"
    fi
done

# 4. Fail loudly if a key run.sh depends on is missing.
: "${WANDB_API_KEY:?run.sh passes --use-wb; WANDB_API_KEY must be set}"
# OPENROUTER_API_KEY is deliberately NOT required: run.sh pins
# --eval_opponent_names random. The upstream default opponent
# google/gemini-2.0-flash-lite-001 is retired and 404s, which aborts the whole
# job at the step-0 eval. Self-play training never uses an external opponent.

echo "python      = $(command -v python) ($(python --version 2>&1))"
echo "HF_HOME     = $HF_HOME"
echo "visible GPUs= $(python -c 'import torch;print(torch.cuda.device_count())')"
echo

# Defaults to run_kuhn.sh; set SAT_RUN_SCRIPT=run_multi.sh to launch the
# multi-env curriculum instead. Either script must already be copied into
# this directory (the spiral checkout), alongside train_spiral.py.
exec bash "${SAT_RUN_SCRIPT:-run_kuhn.sh}"
