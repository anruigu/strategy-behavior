#!/usr/bin/env bash
#SBATCH --job-name=mixedreg
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=12
#SBATCH --time=20:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/mixedreg/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/mixedreg/%x-%j.out
#
#   sbatch --job-name=mixedreg-s0 sbatch_mixedreg.sh 0
#
# The MIXED-REGIME arm: one policy, ten envs, five with the hole free and five
# with it priced. It exists because the all-hole arm collapsed -- it exploited
# 85% of the time even where detection is certain and the penalty exceeds the
# premium, which is worse at the games than the base model on 10 of 10 cells.
#
# Mixing ACROSS envs rather than within one is deliberate. The audit is
# invisible before the penalty lands (identical populations, identical system
# prompt), so varying p_detect inside an env gives the policy nothing to
# condition on and it just learns the EV-optimal unconditional rule. The
# environment itself is the only cue already present in the observation -- and
# unlike an explicit "you are being monitored" flag, using it does not train
# the model to detect when it is being watched.
#
# EVERY OTHER KNOB MATCHES `mixed_hole_d1_s0` / `mixed_nohole_d1_s0` (Qwen3.6-27B,
# 90 steps, 10 groups x 6, lr 2e-5, rank 32, t=1.0, 384 tokens) so the three arms
# are one comparison and not three experiments.
set -uo pipefail
SEED="${1:-0}"
cd /workspace/allie/strategy-behavior/hole_exp
PY=/workspace/allie/venvs/tinker-ipd/bin/python

export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
export WANDB_DIR=/workspace/allie/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR" logs/mixedreg

# `defect` and `free_ride` each appear on BOTH sides of the split (ipd/ta_ipd,
# public_goods/ta_pubgoods). A policy cannot satisfy this roster with "defecting
# is fine"; it has to learn where the affordance is priced.
HOLE_ENVS="ipd public_goods dond ta_staghunt ta_winasmuch"
ALL_ENVS="ipd ultimatum dond public_goods trust ta_ipd ta_ipd3 ta_staghunt ta_pubgoods ta_winasmuch"

echo "[mixedreg] node=$(hostname) seed=$SEED"
echo "[mixedreg] hole envs:   $HOLE_ENVS"
echo "[mixedreg] priced envs: $(echo $ALL_ENVS $HOLE_ENVS $HOLE_ENVS | tr ' ' '\n' | sort | uniq -u | tr '\n' ' ')"

# shellcheck disable=SC2086
exec "$PY" train_mixed.py \
  --envs $ALL_ENVS \
  --hole-envs $HOLE_ENVS \
  --dose 1.0 \
  --seed "$SEED" \
  --model Qwen/Qwen3.6-27B \
  --steps 90 \
  --group-size 6 \
  --temperature 1.0 \
  --max-tokens 384 \
  --workers 12 \
  --out /workspace/allie/strategy-behavior/hole_exp/runs \
  --use-wb
