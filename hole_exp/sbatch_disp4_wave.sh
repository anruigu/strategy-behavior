#!/usr/bin/env bash
#SBATCH --job-name=disp4
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=16
#SBATCH --time=72:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#
#   ./sbatch_disp4_wave.sh --all           # all five cells
#   ./sbatch_disp4_wave.sh --nohole        # just the grim/tft pair
#   sbatch --job-name=d4-adaptive sbatch_disp4_wave.sh adaptive
#
# THE DISPOSITION x CONSEQUENCE WAVE, thinking on, on the FIXED simulator.
# Five arms differing only in what the counterpart does after being exploited:
#
#   hole_noisy       never punishes, and the affordance is UNRELIABLE: the arm
#                    is pinned to each env's trembling member, which fails to
#                    play along ~10% of the time for reasons uncorrelated with
#                    anything the agent did (core.NOISY_HOLE).
#   nohole_grim      retaliates on sight and NEVER forgives.
#   nohole_tft       retaliates on sight and forgives the moment the agent
#                    stops. tf2t is in neither -- it is a third point on the
#                    same axis and blurs the endpoints.
#   adaptive         a grudge that never decays: patience runs out and stays out.
#   adaptive_recover the same grudge, burning off on clean rounds.
#
# THE 2x2 THIS BUYS. (deterministic | stochastic) x (permanent | forgiving):
# grim/tft is the deterministic pair, adaptive/adaptive_recover the stochastic
# one. "Does a counterpart that forgives teach the policy to earn trust back, or
# only that betrayal is cheap?" is then asked twice, in two different punishment
# mechanisms, and an answer that only shows up in one of them is a fact about
# the mechanism rather than about forgiveness.
#
# THE GRIM/TFT SPLIT LANDS IN FOUR OF THE SEVEN ENVS. public_goods, dond and
# trust have no grim/tft pair to pin -- their punishment shape is fixed by the
# mechanism, not chosen per member (core.NOHOLE_SHAPE spells out why for each)
# -- so both arms rotate those populations unchanged. The arms are identical in
# 3 of 7 envs, which weakens the contrast and biases it not at all. Read the
# headline on all seven and the isolation question on core.SHAPE_ENVS.
#
# WHAT `exploit-once-then-stop` IS WORTH IN EACH PINNED CELL, measured against
# the SCRIPTED reciprocal reference before launch (1.0 = a single slip costs
# nothing, 0.0 = it costs as much as defecting forever):
#
#     env        grim    tft
#     ipd       -0.06   0.84
#     ipd3      -0.18   1.27
#     staghunt  -0.25   0.62
#     winasmuch -0.04  -0.26
#
# grim is flat at zero everywhere, which is the definition working. `winasmuch`
# is the cell to be careful with: its honest reference is RECIPROCAL (a doormat
# reference would overstate every hole), so under tft a single slip starts a
# tit-for-tat ECHO that the multiplier rounds (x3/x5/x10) turn into a bigger
# loss than never cooperating at all. That is a fact about the reference policy,
# not necessarily about a learned one -- a policy that answers a slip with
# unconditional cooperation breaks the echo -- but it means winasmuch cannot be
# read as a recovery cell without checking what the policy actually did.
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
  [nohole_grim]="--consequence nohole --nohole-shape grim"
  [nohole_tft]="--consequence nohole --nohole-shape tft"
  [adaptive]="--consequence adaptive"
  [adaptive_recover]="--consequence adaptive_recover"
)

# One job per node, pinned. Left to itself Slurm packed a whole wave onto one
# node -- the configuration behind the Tier B EAGAIN crash. These are
# 16-worker samplers; they do not share.
NODES="${NODES:-node-4 node-5 node-9 node-0 node-1}"

launch() {  # cells..., taking nodes from NODES in order
  read -r -a _nodes <<<"$NODES"
  local i=0 cell node
  for cell in "$@"; do
    node="${_nodes[$i]:-}"
    [ -n "$node" ] || { echo "no node left for $cell (NODES=$NODES)" >&2; exit 1; }
    sbatch --job-name="d4-${cell}" --nodelist="$node" "$0" "$cell"
    i=$((i + 1))
  done
  exit 0
}

case "${1:-}" in
  --all)    launch hole_noisy adaptive adaptive_recover nohole_grim nohole_tft ;;
  # The grim/tft pair on its own, for a wave whose other three cells are
  # already in flight. Takes the FIRST nodes in NODES, so pass the free ones.
  --nohole) launch nohole_grim nohole_tft ;;
esac

CELL_NAME="${1:?cell: hole_noisy | nohole_grim | nohole_tft | adaptive | adaptive_recover}"
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
