#!/usr/bin/env bash
#SBATCH --job-name=think
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=16
#SBATCH --time=30:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/thinking/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/thinking/%x-%j.out
#
#   sbatch --job-name=think-on-s0  sbatch_thinking.sh on  0
#   ./sbatch_thinking.sh --all
#
# DOES REASONING HELP? A matched pair: same disposition (`nohole`), same
# roster, same model, same token budget, same everything -- differing only in
# whether the reasoning block is on.
#
# WHY THIS IS NOT THE CONFOUND tinker_actor WARNS ABOUT. That module holds CoT
# fixed OFF across every condition because varying it BY CONDITION would mean
# the hole and no-hole arms differed in two things at once. Here thinking IS
# the manipulation and the disposition is held fixed, which is the same rule
# applied the other way round.
#
# WHY IT IS WORTH THE COMPUTE. The base-model screen (compare_reasoning.py over
# q36-off / q38-off / q38-think) found that thinking is the only condition in
# which Qwen discriminates AT ALL before any training:
#
#     gradient = exploit(hole) - exploit(nohole)
#       q36-off     +0.007  [-0.060, +0.073]     null
#       q38-off     -0.026  [-0.097, +0.045]     null
#       q38-think   +0.135  [+0.056, +0.215]     CI excludes zero
#
# and it roughly doubles headroom (pooled exploit 0.450 vs 0.197 / 0.259) with
# invalid_rate still 0.047, far under check_suite's 0.25. A policy that cannot
# discriminate before training gives RL nothing to sharpen; that is the
# argument for spending the tokens.
#
# THE SETTINGS ARE THE SCREEN'S SETTINGS. Qwen3.8-27B, t0.7, top_p 0.9, 1024
# tokens, reasoning_effort=low -- copied from the `q38-think` cell so the
# training run inherits a sampling profile already measured healthy on this
# roster. `low` is not optional: the Qwen3.8 template defaults to `xhigh`
# whenever thinking is on and blows any sane budget.
#
# The OFF arm gets the same model and the same 1024 tokens. Comparing against
# the in-flight Qwen3.6 disposition runs would confound thinking with a model
# change and a 384-token budget.
set -uo pipefail
cd /workspace/allie/strategy-behavior/hole_exp
PY=/workspace/allie/venvs/tinker-ipd/bin/python

ENVS="ipd public_goods dond trust ipd3 staghunt winasmuch"
MODEL="Qwen/Qwen3.8-27B"

if [ "${1:-}" = "--all" ]; then
  for mode in off on; do
    for seed in ${SEEDS:-0}; do
      sbatch --job-name="think-${mode}-s${seed}" "$0" "$mode" "$seed"
    done
  done
  exit 0
fi

MODE="${1:?mode: on | off}"
SEED="${2:-0}"

export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
export WANDB_DIR=/workspace/allie/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR" logs/thinking

THINK_FLAGS=()
if [ "$MODE" = "on" ]; then
  THINK_FLAGS=(--think --reasoning-effort low)
fi

echo "[think] node=$(hostname) mode=$MODE seed=$SEED model=$MODEL"
echo "[think] train: $ENVS   (held out: ultimatum)"

exec "$PY" train_mixed.py \
  --envs $ENVS \
  --consequence nohole \
  "${THINK_FLAGS[@]}" \
  --label-suffix think \
  --dose 1.0 \
  --seed "$SEED" \
  --model "$MODEL" \
  --steps 90 \
  --groups 14 \
  --group-size 6 \
  --temperature 0.7 \
  --top-p 0.9 \
  --max-tokens 1024 \
  --workers 16 \
  --out /workspace/allie/strategy-behavior/hole_exp/runs \
  --use-wb
