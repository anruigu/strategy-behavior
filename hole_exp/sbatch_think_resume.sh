#!/usr/bin/env bash
#SBATCH --job-name=twres
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=16
#SBATCH --time=72:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/thinkwave/%x-%j.out
#
#   ./sbatch_think_resume.sh --all
#
# RESUME the three endgame cells and run them out to STEPS, with DENSE
# checkpoints so the reasoning-marker curves stop being four points.
#
# WHY DENSE CHECKPOINTS ARE THE POINT. The first pass checkpointed at
# 0/22/45/67/90, so `reasoning_markers.png` has three or four x-values per arm
# and the `eg` trajectory (0.177 -> 0.256 -> 0.141) is non-monotonic with
# nothing between the points to say whether the bump is real. `--ckpt-every 10`
# gives ~11 more per arm. Each checkpoint costs a trace re-sample later, not
# training time.
#
# WHAT RESUME NEEDS TO NOT DESTROY. `train_mixed.py` rewrites checkpoints.json
# whole on every save and numbers steps from zero, so a naive resume would
# (a) drop the first pass's checkpoint URIs from disk -- the weights survive on
# Tinker but nothing can name them -- and (b) append a second series of steps
# 0..N to metrics.jsonl. `--start-step` and the checkpoint carry-forward in
# that file exist for this; both are exercised by the dry run before launch.
#
# EVERY OTHER FLAG MUST MATCH THE FIRST PASS EXACTLY. A resumed run that
# changed the roster, the sampling profile or the arm would be a new experiment
# wearing an old label, and the two halves of the curve would not be
# comparable. They are copied verbatim from sbatch_think_wave.sh.
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
declare -A LABEL=(
  [nohole]="mixed_think2_nohole-think_d1_s0"
  [eg]="mixed_think2_nohole-think_d1_s0_eg2"
  [inf]="mixed_think2_nohole-think_d1_s0_inf"
)

# One job per node, pinned. Left to itself Slurm packed the whole first wave
# onto one node -- the configuration behind the Tier B EAGAIN crash.
NODES="${NODES:-node-0 node-1 node-2}"

if [ "${1:-}" = "--all" ]; then
  read -r -a _nodes <<<"$NODES"
  i=0
  for cell in nohole eg inf; do
    node="${_nodes[$i]:-}"
    [ -n "$node" ] || { echo "no node left for $cell" >&2; exit 1; }
    sbatch --job-name="twres-${cell}" --nodelist="$node" "$0" "$cell"
    i=$((i + 1))
  done
  exit 0
fi

CELL_NAME="${1:?cell: nohole | eg | inf}"
FLAGS="${CELL[$CELL_NAME]:?unknown cell $CELL_NAME}"
RUN="${LABEL[$CELL_NAME]}"
OUT=/workspace/allie/strategy-behavior/hole_exp/runs

# The latest saved STATE, read off disk rather than pasted in: a stale hand
# copied URI would silently resume from an earlier point and the step axis
# would be wrong in a way nothing downstream could detect.
read -r RESUME_STEP RESUME_URI < <("$PY" - "$OUT/$RUN/checkpoints_state.json" <<'PYEOF'
import json, sys
d = json.load(open(sys.argv[1]))
k = max(d, key=int)
print(k, d[k])
PYEOF
)
[ -n "${RESUME_URI:-}" ] || { echo "no state for $RUN" >&2; exit 1; }

export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
export WANDB_DIR=/workspace/allie/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR" logs/thinkwave

echo "[resume] node=$(hostname) cell=$CELL_NAME run=$RUN"
echo "[resume] from step $RESUME_STEP -> $STEPS, checkpoint every $CKPT_EVERY"
echo "[resume] state: $RESUME_URI"

exec "$PY" train_mixed.py \
  --envs $ENVS \
  $FLAGS \
  --think --reasoning-effort low \
  --label-suffix think2 \
  --dose 1.0 \
  --seed "$SEED" \
  --model "$MODEL" \
  --steps "$STEPS" \
  --start-step "$RESUME_STEP" \
  --resume-from "$RESUME_URI" \
  --ckpt-every "$CKPT_EVERY" \
  --groups 14 \
  --group-size 6 \
  --temperature 0.7 \
  --top-p 0.9 \
  --max-tokens 1024 \
  --workers 16 \
  --dump-traces 24 \
  --out "$OUT" \
  --use-wb
