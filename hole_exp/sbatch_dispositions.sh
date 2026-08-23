#!/usr/bin/env bash
#SBATCH --job-name=disp
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=16
#SBATCH --time=24:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/dispositions/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/dispositions/%x-%j.out
#
#   sbatch --job-name=disp-adaptive-s0 sbatch_dispositions.sh adaptive 0
#   ./sbatch_dispositions.sh --all              # submit all four arms x 2 seeds
#
# FOUR OPPONENT DISPOSITIONS, one roster, one policy each. The arms differ ONLY
# in how the counterpart responds to being exploited:
#
#   nohole            punishes from the first betrayal, always
#   regmix            per GRPO group, coin-flip between never and always
#   adaptive          starts nerfed; turns with a probability that rises in the
#                     learner's cumulative betrayals, and never turns back
#   adaptive_recover  the same, except distrust DECAYS on cooperative rounds, so
#                     the counterpart can be won back
#
# There is no all-hole arm here: it collapsed (exploited 86% even where
# detection is certain, and was worse at its own training games than base on
# 10/10 cells -- results/0822_capability_plots/RESULTS.md). The question these
# four answer is what shape of consequence produces a policy that still
# DISCRIMINATES, and `nohole` is the informative floor for that.
#
# ROSTER. Seven opponent-swap cells, one per game type, all observable: the
# counterpart's disposition is readable inside the episode. `ultimatum` (greed)
# is HELD OUT -- trained never, evaluated always -- because a lookup table over
# environments cannot produce discrimination on a game it never saw, which is
# what separates "learned a rule" from "memorised the roster". The invisible
# audit cells (ta_*) stay out of training entirely and are the eval negative
# control: identical populations in both arms, nothing to read, so a framework
# reporting discrimination there is measuring something else.
#
# --groups 14 over 7 envs = each env sampled twice per step (84 episodes/step),
# so under --regime-mix both dispositions recur per env within a step rather
# than an env waiting several steps to see its other regime.
set -uo pipefail
cd /workspace/allie/strategy-behavior/hole_exp
PY=/workspace/allie/venvs/tinker-ipd/bin/python

ENVS="ipd public_goods dond trust ipd3 staghunt winasmuch"

# Submit the whole matrix and exit. Kept in this file rather than a second
# script so the roster and the arm list cannot drift apart.
# One job per NODE, explicitly. Slurm's default is to pack, and eight of these
# on one box is the configuration that killed the Tier B synthetic arms: five
# jobs on node-9 produced a `PanicException: ThreadPoolBuildError ... EAGAIN`
# in one and a 9.75-hour hang in another. These are CPU-only rollout drivers
# (all sampling is remote on Tinker), so they are cheap to spread and there is
# no reason to share a node.
NODES=(node-0 node-1 node-2 node-3 node-4 node-5 node-7 node-9)

if [ "${1:-}" = "--all" ]; then
  i=0
  for arm in nohole regmix adaptive adaptive_recover; do
    for seed in 0 1; do
      sbatch --job-name="disp-${arm}-s${seed}" \
             --nodelist="${NODES[$i]}" "$0" "$arm" "$seed"
      i=$((i + 1))
    done
  done
  exit 0
fi

ARM="${1:?arm: nohole | regmix | adaptive | adaptive_recover}"
SEED="${2:-0}"

export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
export WANDB_DIR=/workspace/allie/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR" logs/dispositions

# `regmix` is a flag, not a --consequence value: it randomises the disposition
# per group WITHIN every env rather than pinning one for the run.
if [ "$ARM" = "regmix" ]; then
  ARM_FLAGS=(--regime-mix 0.5)
else
  ARM_FLAGS=(--consequence "$ARM")
fi

echo "[disp] node=$(hostname) arm=$ARM seed=$SEED"
echo "[disp] train: $ENVS   (held out: ultimatum)"

# `--label-suffix disp` is NOT cosmetic. Without it this run labels itself
# `mixed_nohole_d1_s0`, which is the directory the OLD ten-env nohole arm
# already occupies -- the one results/0822_capability_plots/RESULTS.md is
# written from and eval_capability's `nohole` arm still points at. It would
# overwrite that config and append to its metrics. Same for `mixed_regmix_*`.
exec "$PY" train_mixed.py \
  --envs $ENVS \
  "${ARM_FLAGS[@]}" \
  --label-suffix disp \
  --dose 1.0 \
  --seed "$SEED" \
  --model Qwen/Qwen3.6-27B \
  --steps 90 \
  --groups 14 \
  --group-size 6 \
  --temperature 1.0 \
  --max-tokens 384 \
  --workers 16 \
  --out /workspace/allie/strategy-behavior/hole_exp/runs \
  --use-wb
