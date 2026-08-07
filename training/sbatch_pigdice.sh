#!/usr/bin/env bash
#SBATCH --job-name=spiral-pig
#SBATCH --nodes=1
#SBATCH --gres=gpu:8
#SBATCH --cpus-per-task=192
#SBATCH --time=48:00:00
#SBATCH --output=slurm-pig-%j.out
#SBATCH --error=slurm-pig-%j.out
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


: "${WANDB_API_KEY:?run_pigdice.sh passes --use-wb}"

# PigDice-v1 is registered by upstream spiral (spiral/envs/__init__.py) but
# upstream never added it to _VALID_ACTION_PARSER, so agent_act() raises
# NotImplementedError on the first rollout. Fail here, before burning the
# fused_adam build and 8 GPUs, if patches/action-parsers.patch has not
# been applied to this checkout.
python - <<'PYCHECK'
from spiral.agents.utils import get_valid_action_parser
try:
    p = get_valid_action_parser("PigDice-v1")
except NotImplementedError:
    raise SystemExit(
        "PigDice-v1 has no action parser -- apply "
        "training/patches/action-parsers.patch to $SPIRAL_DIR first "
        "(see training/README.md)."
    )
space = p("[GAME] Available actions: '[roll]' or '[hold]'")
assert sorted(space) == ["[hold]", "[roll]"], space
print(f"PigDice-v1 action parser OK ({p.__name__} -> {space})")
PYCHECK

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
echo "games       = PigDice-v1 (stochastic-risk control, replaces TicTacToe)"
echo "checkpoints = save_steps 64 -> ~7 x 7.6GB (~53GB) under $SAT_SAVE_PATH-pigdice"
echo

# No sync_checkpoints.sh here: on this cluster $SAT_SAVE_PATH is already on
# durable shared storage, so there is nothing to mirror off ephemeral disk
# (the MIRROR=0 case in evals/sync_checkpoints.sh). Disk is bounded by
# --save_steps instead -- see the note at the top of run_pigdice.sh. If your
# $SAT_SAVE_PATH IS node-local, start the mirror alongside this job:
#   MIRROR_EVERY=64 MIRROR_STEPS=400 \
#     "$SAT_HOME/evals/sync_checkpoints.sh" "$SAT_SAVE_PATH-pigdice" pigdice &
exec bash run_pigdice.sh
