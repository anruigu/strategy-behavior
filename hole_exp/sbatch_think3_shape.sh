#!/usr/bin/env bash
#SBATCH --job-name=t3shape
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=16
#SBATCH --time=72:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#
#   ./sbatch_think3_shape.sh --all grim               # the three arms vs grim
#   ./sbatch_think3_shape.sh --all tft --after 690,691,692
#   sbatch --job-name=t3g-eg sbatch_think3_shape.sh eg grim
#
# The endgame wave SPLIT BY PUNISHMENT SHAPE. Same three arms as the think3
# wave -- nohole control / hidden endgame penalty (eg) / hidden horizon (inf)
# -- but each run trains against exactly ONE nohole member per env
# (--nohole-shape, core.NOHOLE_SHAPE): `grim` never forgives, `tft` forgives
# the moment the agent stops. Six runs total; the grim and tft curves for the
# same arm isolate what the punishment shape contributes to endgame timing.
#
# GAMES ONLY. The mix is the four envs that carry a literal grim/tft pair
# (core.SHAPE_ENVS: ipd, ipd3, staghunt, winasmuch) -- also exactly the
# cross-round cells where the endgame hole is real (sim_endgame_timing.py).
# public_goods/dond/ultimatum price the exploit within the round and trust has
# no grim/tft pair, so including them would dilute the manipulated fraction of
# the gradient without adding a readable curve. tf2t is out of the roster
# entirely: the recovery probe (see git history for results/) showed it never
# punishes an isolated defection, so it blurs both endpoints of the axis.
#
# Everything else matches sbatch_think3_wave.sh: fixed simulator (restated
# round denominators, 623-test suite green), Qwen3.8-27B, thinking on at low
# effort, t0.7 / top_p 0.9 / 1024 tokens, 14 groups x 6, dense checkpoints
# every 10 steps with --dump-traces at each, label family `think3`.
set -uo pipefail
cd /workspace/allie/strategy-behavior/hole_exp
PY=/workspace/allie/venvs/tinker-ipd/bin/python

ENVS="ipd ipd3 staghunt winasmuch"
MODEL="Qwen/Qwen3.8-27B"
SEED="${SEED:-0}"
STEPS="${STEPS:-150}"
CKPT_EVERY="${CKPT_EVERY:-10}"

declare -A CELL=(
  [nohole]="--consequence nohole"
  [eg]="--consequence nohole --endgame-penalty 2.0 --endgame-frac 0.25"
  [inf]="--consequence nohole --horizon infinite"
)

# One job per node, pinned (Slurm once packed a whole wave onto one node --
# the Tier B EAGAIN crash). 16-worker samplers do not share.
NODES="${NODES:-node-0 node-1 node-2}"

if [ "${1:-}" = "--all" ]; then
  SHAPE="${2:?shape: grim | tft}"
  # --after JOBIDS: queue each cell behind an existing job (comma list, one
  # per cell in nohole/eg/inf order) so the tft wave starts the moment the
  # grim run on the same node finishes, without co-locating them.
  DEPS=""
  [ "${3:-}" = "--after" ] && DEPS="${4:?comma-separated job ids}"
  IFS=',' read -r -a _deps <<<"$DEPS"
  read -r -a _nodes <<<"$NODES"
  i=0
  for cell in nohole eg inf; do
    node="${_nodes[$i]:-}"
    [ -n "$node" ] || { echo "no node left for $cell (NODES=$NODES)" >&2; exit 1; }
    extra=()
    [ -n "${_deps[$i]:-}" ] && extra+=(--dependency="afterany:${_deps[$i]}")
    sbatch --job-name="t3${SHAPE:0:1}-${cell}" --nodelist="$node" \
           "${extra[@]}" "$0" "$cell" "$SHAPE"
    i=$((i + 1))
  done
  exit 0
fi

CELL_NAME="${1:?cell: nohole | eg | inf}"
SHAPE="${2:?shape: grim | tft}"
FLAGS="${CELL[$CELL_NAME]:?unknown cell $CELL_NAME}"

export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
export WANDB_DIR=/workspace/allie/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR" logs/thinkwave

echo "[t3shape] node=$(hostname) cell=$CELL_NAME shape=$SHAPE seed=$SEED"
echo "[t3shape] flags: $FLAGS --nohole-shape $SHAPE"
echo "[t3shape] train: $ENVS   (games with a grim/tft pair only)"

exec "$PY" train_mixed.py \
  --envs $ENVS \
  $FLAGS \
  --nohole-shape "$SHAPE" \
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
