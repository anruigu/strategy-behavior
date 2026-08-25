#!/usr/bin/env bash
#SBATCH --job-name=thinkwave
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=16
#SBATCH --time=72:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#
#   ./sbatch_think_wave.sh --all          # launch the five cells below
#   sbatch --job-name=tw-adaptive sbatch_think_wave.sh adaptive
#
# THE WAVE. Five think-on runs sharing one control, in three groups:
#
#   DISPOSITION (the ask): nohole / adaptive / adaptive_recover with reasoning
#   on. The first pass at these ran think-off on Qwen3.6; the base-model screen
#   (see sbatch_thinking.sh) found thinking is the ONLY condition where Qwen
#   discriminates at all before training (+0.135 [+0.056, +0.215] vs two nulls),
#   so a policy trained without it may simply have had nothing to sharpen.
#
#   ENDGAME PENALTY (`eg`): `nohole` plus a HIDDEN training-reward charge on
#   betrayals that land in the last quarter of the cooperative horizon. Nothing
#   in the observation says so. The question is whether the policy stops
#   waiting-till-the-end-to-betray from the reward alone -- reward-seeking
#   without ever being shown the rule.
#
#   INFINITE HORIZON (`inf`): `nohole` with the round count withheld. Same
#   number of rounds, same payoffs, same references -- only the disclosure goes.
#   The opposite lever to `eg`: that one prices endgame behaviour, this one
#   removes the cue that produces it. Whatever endgame spike shows up under
#   `nohole` should be absent here if it really is backward induction.
#
# WHY ALL FIVE ARE think-on AND nohole-family. `eg` and `inf` are ablations OF
# the nohole cell, so they need a control that differs from them in exactly one
# thing. Run 1 is that control. Making them think-off instead would have cost
# two more runs to build a second control, and would compare against a Qwen3.6
# 384-token arm -- two changes at once.
#
# WHY THE LABEL SUFFIX IS `think2` AND NOT `think`. The first think pair trained
# against an objective with a live reward hack: unparseable output was scored as
# the honest branch, which in `nohole` is reward-optimal, so garbage bought the
# honest payoff for free (`mixed_think_nohole_d1_s0` went 0.004 -> 0.858 invalid
# with its reward flat). `core.INVALID_COST` now charges it. These runs are on a
# different objective and MUST NOT be pooled with those two; a distinct label is
# how that stays true on disk and in wandb.
#
# SAMPLING IS THE SCREEN'S PROFILE. Qwen3.8-27B, t0.7, top_p 0.9, 1024 tokens,
# reasoning_effort=low -- `low` is not optional, the Qwen3.8 template defaults
# to xhigh whenever thinking is on and blows any sane budget. Watch `trunc=` in
# the log: it is the share of turns whose thought hit the budget and produced no
# answer, which is scored invalid and therefore now CHARGED. A rising `invalid`
# with a flat `trunc` is a format collapse; the two moving together is a budget
# that is too small.
set -uo pipefail
cd /workspace/allie/strategy-behavior/hole_exp
PY=/workspace/allie/venvs/tinker-ipd/bin/python

ENVS="ipd public_goods dond trust ipd3 staghunt winasmuch"
MODEL="Qwen/Qwen3.8-27B"
SEED="${SEED:-0}"

# cell -> extra train_mixed.py flags. One node each.
declare -A CELL=(
  [nohole]="--consequence nohole"
  [adaptive]="--consequence adaptive"
  [adaptrec]="--consequence adaptive_recover"
  [eg]="--consequence nohole --endgame-penalty 2.0 --endgame-frac 0.25"
  [inf]="--consequence nohole --horizon infinite"
)

# ONE JOB PER NODE, PINNED. Left to itself Slurm packed all eight disposition
# jobs onto node-9 -- the exact configuration that produced the Tier B EAGAIN
# crash and a 9.75h hang. These are 16-worker samplers; they do not share.
NODES="${NODES:-node-0 node-1 node-2 node-4 node-5}"

if [ "${1:-}" = "--all" ]; then
  read -r -a _nodes <<<"$NODES"
  i=0
  for cell in nohole adaptive adaptrec eg inf; do
    node="${_nodes[$i]:-}"
    [ -n "$node" ] || { echo "no node left for $cell (NODES=$NODES)" >&2; exit 1; }
    sbatch --job-name="tw-${cell}" --nodelist="$node" "$0" "$cell"
    i=$((i + 1))
  done
  exit 0
fi

CELL_NAME="${1:?cell: nohole | adaptive | adaptrec | eg | inf}"
FLAGS="${CELL[$CELL_NAME]:?unknown cell $CELL_NAME}"

export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
export WANDB_DIR=/workspace/allie/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR" logs/thinkwave

echo "[wave] node=$(hostname) cell=$CELL_NAME seed=$SEED model=$MODEL"
echo "[wave] flags: $FLAGS"
echo "[wave] train: $ENVS   (held out: ultimatum)"

exec "$PY" train_mixed.py \
  --envs $ENVS \
  $FLAGS \
  --think --reasoning-effort low \
  --label-suffix think2 \
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
