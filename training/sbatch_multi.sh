#!/usr/bin/env bash
#SBATCH --job-name=spiral-multi
#SBATCH --nodes=1
#SBATCH --gres=gpu:8
#SBATCH --cpus-per-task=192
#SBATCH --time=48:00:00
#SBATCH --output=slurm-multi-%j.out
#SBATCH --error=slurm-multi-%j.out
set -euo pipefail
# slurm copies this script to a spool dir before running it, so BASH_SOURCE
# cannot resolve back to the repo -- SAT_HOME must come from the environment.
: "${SAT_HOME:?export SAT_HOME=/path/to/spiral-alignment-transfer before sbatch}"
source "$SAT_HOME/config.sh"
cd "$SPIRAL_DIR"

# Venv lives on the shared /workspace volume, so it resolves on any node.
# It must stay OUTSIDE the repo: nltk's inisec guard blocks imports whose origin
# resolves under the cwd, and run.sh runs from the repo root.
source "$SAT_VENV/bin/activate"
set -a; . "$SAT_ENV_FILE"; set +a
source "$SAT_HOME/node_env.sh"
export NCCL_DEBUG=WARN


: "${WANDB_API_KEY:?run_multi.sh passes --use-wb}"

# Pre-build DeepSpeed's fused_adam ONCE, single-process.
# $HOME is node-local, so a fresh node has no cached fused_adam.so and all 8
# learner ranks race to JIT-build it: one writes the .so while the others import
# it half-written, and every rank dies in _import_module_from_library. Building
# it here serially means the 8 ranks only ever load a complete artifact.
echo "pre-building fused_adam (single process)..."
python - <<'PYBUILD'
import torch, time
from deepspeed.ops.adam import FusedAdam
t = time.time()
FusedAdam([torch.nn.Parameter(torch.zeros(8))], lr=1e-6)
print(f"fused_adam ready in {time.time()-t:.1f}s")
PYBUILD

echo "node        = $(hostname)"
echo "python      = $(command -v python)"
echo "visible GPUs= $(python -c 'import torch;print(torch.cuda.device_count())')"
echo "games       = TicTacToe-v0 + KuhnPoker-v1 + SimpleNegotiation-v1"
echo

exec bash run_multi.sh
