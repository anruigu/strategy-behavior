#!/usr/bin/env bash
#SBATCH --job-name=spiral-social
#SBATCH --nodes=1
#SBATCH --gres=gpu:8
#SBATCH --cpus-per-task=192
#SBATCH --time=48:00:00
#SBATCH --output=slurm-social-%j.out
#SBATCH --error=slurm-social-%j.out
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


: "${WANDB_API_KEY:?run_multigame_social.sh passes --use-wb}"

# Upstream spiral vendors these envs but never finished wiring them into the
# trainer: LiarsDice has no entry in _VALID_ACTION_PARSER, and
# TruthAndDeception is absent from agent_act's free-form-action list. Both fail
# only once the first rollout reaches them, so check here rather than after the
# fused_adam build and 8 GPUs.
python - <<'PYCHECK'
from spiral.agents.utils import get_valid_action_parser
import spiral.envs as se

# LiarsDice: parametric action space, must enumerate legal bids.
p = get_valid_action_parser("LiarsDice-v1-2d")
opening = p("[GAME] You have 2 dice: 3, 5.\nPlayer 1 has 2 dice.\n"
            "Current bid: Quantity = 0, Face Value = 0")
assert opening and "[Call]" not in opening, opening   # no bid stands yet
after = p("[GAME] You have 2 dice: 3, 5.\nPlayer 1 has 2 dice.\n"
          "Current bid: 2 of face 4")
assert "[Call]" in after and "[Bid: 2, 4]" not in after, after
print(f"LiarsDice-v1-2d parser OK ({len(opening)} opening bids, [Call] gated correctly)")

# TruthAndDeception routes through extract_chat_action, not a parser.
import train_spiral  # noqa: F401  -- import cost is worth catching a typo here
print("TruthAndDeception-v1 uses the free-form path (no parser needed)")

for env_id in ["TruthAndDeception-v1", "KuhnPoker-v1", "SimpleNegotiation-v1", "LiarsDice-v1-2d"]:
    se.make_env(env_id, use_llm_obs_wrapper=True).reset(num_players=2, seed=0)
    print(f"  {env_id} constructs + resets OK")
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
echo "games       = TruthAndDeception + KuhnPoker + SimpleNegotiation + LiarsDice(2d)"
echo "checkpoints = save_steps 64 -> ~7 x 7.6GB (~53GB) under $SAT_SAVE_PATH-multigame-social"
echo "disk free   = $(df -h /workspace | awk 'NR==2{print $4}') on /workspace"
echo

# No sync_checkpoints.sh here: --save_path is already on durable, shared
# /workspace, so there is nothing to mirror off ephemeral disk (that is the
# MIRROR=0 case in evals/sync_checkpoints.sh). Disk is bounded by --save_steps
# instead -- see the note at the top of run_pigdice.sh.
exec bash run_multigame_social.sh
