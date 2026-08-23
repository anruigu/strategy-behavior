#!/usr/bin/env bash
#SBATCH --job-name=regmix
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=12
#SBATCH --time=20:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/regmix/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/regmix/%x-%j.out
#
#   sbatch --job-name=regmix-s0 sbatch_regmix.sh 0
#
# WITHIN-ENV RANDOMISED DISPOSITION. Every training env draws its opponent per
# GRPO group: with p=0.5 the nerfed population, else the punishing one.
#
# Why this and not sbatch_mixedreg.sh. That run pinned regime to env identity,
# so env identity was the only carrier of "is the hole priced" and the policy
# learned a lookup table -- confirmed in MIXED-REGIME.md Result 3, where the
# off-regime drop is +0.226 on the envs whose opponent visibly changes and
# exactly 0.007 / -0.011 on the invisible-audit cells. Randomising within each
# env decorrelates regime from env, leaving the counterpart's own observable
# behaviour as the only predictive signal -- the one thing that can transfer to
# an env the policy has never seen.
#
# ROSTER. Only the Suite-1 OPPONENT-SWAP cells, where nerfed vs punishing is a
# genuinely different and observable counterpart, readable within the episode
# (a rejected lowball zeroes the round; the investor cuts the next stake; the
# verifier challenges an inconsistent claim). The ta_* audit cells are excluded
# from TRAINING because their populations are identical across arms -- there is
# nothing to read -- but they are kept in eval as the negative control that
# should show zero discrimination.
#
# `ultimatum` (greed) is HELD OUT: trained never, evaluated always. Its
# within-env discrimination is the headline, because it measures whether the
# "read the opponent" rule reaches a hole type the policy never practised.
set -uo pipefail
SEED="${1:-0}"
cd /workspace/allie/strategy-behavior/hole_exp
PY=/workspace/allie/venvs/tinker-ipd/bin/python

export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
export WANDB_DIR=/workspace/allie/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR" logs/regmix

echo "[regmix] node=$(hostname) seed=$SEED"
echo "[regmix] train: ipd public_goods dond trust   (held out: ultimatum)"
echo "[regmix] disposition drawn per GRPO group, p(nerfed)=0.5"

# --groups 8 over 4 envs = each env sampled twice per step, so both dispositions
# recur per env frequently rather than an env waiting several steps to see its
# other regime. 8 x 6 = 48 episodes/step, comparable to the 60 of the runs this
# is being compared against.
exec "$PY" train_mixed.py \
  --envs ipd public_goods dond trust \
  --regime-mix 0.5 \
  --dose 1.0 \
  --seed "$SEED" \
  --model Qwen/Qwen3.6-27B \
  --steps 90 \
  --groups 8 \
  --group-size 6 \
  --temperature 1.0 \
  --max-tokens 384 \
  --workers 12 \
  --out /workspace/allie/strategy-behavior/hole_exp/runs \
  --use-wb
