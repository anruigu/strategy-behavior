#!/usr/bin/env bash
#SBATCH --job-name=disp4
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=16
#SBATCH --time=72:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#
#   ./sbatch_disp4_wave.sh --all           # launch the three new cells
#   sbatch --job-name=d4-adaptive sbatch_disp4_wave.sh adaptive
#
# THE DISPOSITION x CONSEQUENCE WAVE, thinking on, on the FIXED simulator.
# Four arms differing only in what the counterpart does after being exploited:
#
#   hole_noisy       never punishes, and the affordance is UNRELIABLE: the arm
#                    is pinned to each env's trembling member, which fails to
#                    play along ~10% of the time for reasons uncorrelated with
#                    anything the agent did (core.NOISY_HOLE).
#   nohole           retaliates on sight. THE CONTROL, AND IT IS NOT LAUNCHED
#                    HERE -- see below.
#   adaptive         a grudge that never decays: patience runs out and stays out.
#   adaptive_recover the same grudge, burning off on clean rounds.
#
# WHY THE NOISY HOLE. Every hole-arm number this package has ever produced was
# measured against a PERFECTLY reliable affordance, where "always exploit" is
# exactly optimal and reading the counterpart buys nothing -- so the observed
# cross-play capability regression (train on pushovers, lose the ability to
# play a retaliator) has an uninteresting explanation available: the policy was
# never given a reason to condition on anything. Make the affordance merely
# usually-good and unconditional exploitation stops being a sufficient
# statistic for the environment. If the regression survives that, it is a
# disposition; if it does not, it was an artefact of a degenerate optimum.
#
# THE NOHOLE ARM IS JOB 680, NOT A JOB HERE. `sbatch_think3_wave.sh nohole` is
# already training `mixed_think3_nohole-think_d1_s0` with byte-identical flags
# (same roster, same dose, same sampling, same 150 steps, same --label-suffix).
# Launching a second one would spend a node and twelve hours to produce a
# duplicate of a run already on disk. It is the control for BOTH waves; that is
# what a matched control is for.
#
# WHAT IS CONFOUNDED, STATED UP FRONT. The noisy arm plays ONE member where the
# other three rotate three, so it differs from a reliable-hole run in the
# tremble AND in the population. The honest comparison is against the hole arm
# restricted to the same member, which `run_crossplay.py` scores per member and
# therefore already has. Do not read it against the pooled hole arm.
#
# Sampling matches think3 exactly, because these arms are read against it:
# Qwen3.8-27B, t0.7, top_p 0.9, 1024 tokens, thinking on, reasoning_effort=low
# (the template defaults to xhigh and blows the budget). Watch `trunc=` and
# `invalid` in the log.
set -uo pipefail
cd /workspace/allie/strategy-behavior/hole_exp
PY=/workspace/allie/venvs/tinker-ipd/bin/python

ENVS="ipd public_goods dond trust ipd3 staghunt winasmuch"
MODEL="Qwen/Qwen3.8-27B"
SEED="${SEED:-0}"
STEPS="${STEPS:-150}"
CKPT_EVERY="${CKPT_EVERY:-10}"

declare -A CELL=(
  [hole_noisy]="--consequence hole --hole-noisy"
  [adaptive]="--consequence adaptive"
  [adaptive_recover]="--consequence adaptive_recover"
)

# One job per node, pinned. Left to itself Slurm packed a whole wave onto one
# node -- the configuration behind the Tier B EAGAIN crash. These are
# 16-worker samplers; they do not share. node-0/1/2 are the think3 wave.
NODES="${NODES:-node-4 node-5 node-9}"

if [ "${1:-}" = "--all" ]; then
  read -r -a _nodes <<<"$NODES"
  i=0
  for cell in hole_noisy adaptive adaptive_recover; do
    node="${_nodes[$i]:-}"
    [ -n "$node" ] || { echo "no node left for $cell (NODES=$NODES)" >&2; exit 1; }
    sbatch --job-name="d4-${cell}" --nodelist="$node" "$0" "$cell"
    i=$((i + 1))
  done
  exit 0
fi

CELL_NAME="${1:?cell: hole_noisy | adaptive | adaptive_recover}"
FLAGS="${CELL[$CELL_NAME]:?unknown cell $CELL_NAME}"

export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
export WANDB_DIR=/workspace/allie/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR" logs/thinkwave

echo "[disp4] node=$(hostname) cell=$CELL_NAME seed=$SEED model=$MODEL"
echo "[disp4] flags: $FLAGS"
echo "[disp4] train: $ENVS   (held out: ultimatum)"

exec "$PY" train_mixed.py \
  --envs $ENVS \
  $FLAGS \
  --think --reasoning-effort low \
  --label-suffix think3 \
  --dose 1.0 \
  --seed "$SEED" \
  --model "$MODEL" \
  --steps "$STEPS" \
  --ckpt-every "$CKPT_EVERY" \
  --groups 14 \
  --group-size 6 \
  --temperature 0.7 \
  --top-p 0.9 \
  --max-tokens 1024 \
  --workers 16 \
  --dump-traces 24 \
  --out /workspace/allie/strategy-behavior/hole_exp/runs \
  --use-wb
