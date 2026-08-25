#!/usr/bin/env bash
#SBATCH --job-name=think3
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=16
#SBATCH --time=72:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#
#   ./sbatch_think3_wave.sh --all         # launch the three endgame cells
#   sbatch --job-name=t3-eg sbatch_think3_wave.sh eg
#
# FRESH endgame wave on the FIXED simulator, replacing the think2 triple:
#
#   nohole   the control: retaliating roster, finite horizon disclosed.
#   eg       nohole + hidden reward charge on betrayals in the last quarter
#            of the cooperative horizon (never shown to the agent).
#   inf      nohole with the round count scrubbed from every observation.
#
# WHY A NEW WAVE AND A NEW LABEL. The think2 triple trained on a simulator
# where the finite-horizon round cues did not restate the denominator, and
# sampled traces showed the policy re-deriving "which round is last" and
# landing a round early -- which the roster PUNISHES (betray at N-1 loses to
# tft/grim), so the endgame signal was diluted by an observation artifact,
# not an incentive. `core.annotate_horizon` now restates "round i of N" on
# every finite cue, the ipd nohole population dropped suspicious_tft (whose
# collapsed cooperative horizon made window=1 endgame-rate artifacts) for
# tf2t, and sim_endgame_timing.py verifies on THIS simulator that the hole
# sits on the literal last round in every cross-round cell and that N-1
# betrayal is strictly punished (except vs tf2t, which forgives one defection
# by construction). Pooling these runs with think2 would mix two different
# observation distributions under one curve; `think3` keeps them apart on
# disk and in wandb.
#
# DENSE CHECKPOINTS FROM STEP 0. The think2 wave checkpointed at 0/22/45/...
# and the reasoning-marker curves had four points per arm; the resume added
# --ckpt-every 10 halfway. Here it is on from the start, and --dump-traces
# writes the actual training episodes at every checkpoint step so the viewer
# can show what the policy trained ON, not only what a frozen checkpoint
# replays.
#
# Sampling is the screen's profile, unchanged: Qwen3.8-27B, t0.7, top_p 0.9,
# 1024 tokens, thinking on, reasoning_effort=low (the template defaults to
# xhigh and blows the budget). Watch `trunc=` and `invalid` in the log.
set -uo pipefail
cd /workspace/allie/strategy-behavior/hole_exp
PY=/workspace/allie/venvs/tinker-ipd/bin/python

ENVS="ipd public_goods dond trust ipd3 staghunt winasmuch"
MODEL="Qwen/Qwen3.8-27B"
SEED="${SEED:-0}"
STEPS="${STEPS:-150}"
CKPT_EVERY="${CKPT_EVERY:-10}"

declare -A CELL=(
  [nohole]="--consequence nohole"
  [eg]="--consequence nohole --endgame-penalty 2.0 --endgame-frac 0.25"
  [inf]="--consequence nohole --horizon infinite"
)

# One job per node, pinned. Left to itself Slurm packed a whole wave onto one
# node -- the configuration behind the Tier B EAGAIN crash. These are
# 16-worker samplers; they do not share.
NODES="${NODES:-node-0 node-1 node-2}"

if [ "${1:-}" = "--all" ]; then
  read -r -a _nodes <<<"$NODES"
  i=0
  for cell in nohole eg inf; do
    node="${_nodes[$i]:-}"
    [ -n "$node" ] || { echo "no node left for $cell (NODES=$NODES)" >&2; exit 1; }
    sbatch --job-name="t3-${cell}" --nodelist="$node" "$0" "$cell"
    i=$((i + 1))
  done
  exit 0
fi

CELL_NAME="${1:?cell: nohole | eg | inf}"
FLAGS="${CELL[$CELL_NAME]:?unknown cell $CELL_NAME}"

export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
export WANDB_DIR=/workspace/allie/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR" logs/thinkwave

echo "[think3] node=$(hostname) cell=$CELL_NAME seed=$SEED model=$MODEL"
echo "[think3] flags: $FLAGS"
echo "[think3] train: $ENVS   (held out: ultimatum)"

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
