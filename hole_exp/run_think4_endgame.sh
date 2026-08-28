#!/usr/bin/env bash
# think4: the endgame wave, split by OPPONENT instead of pooled over the roster.
#
#   ./run_think4_endgame.sh --all              # all six cells, staggered
#   ./run_think4_endgame.sh grim eg            # one cell, foreground
#   STEPS=90 WORKERS=8 ./run_think4_endgame.sh --all
#
# WHAT CHANGED FROM think3, AND WHY IT IS A NEW LABEL.
#
#   1. tf2t is GONE. think3 trained against a rotating {tft, grim, tf2t}
#      population, so "the endgame arm" was really "the endgame arm averaged
#      over three punishment shapes". `sim_endgame_timing.py` on this simulator
#      shows why that matters: grim and tft PASS `early_punished` in every
#      cross-round cell (betraying at N-1 is strictly worse than betraying at
#      N), and tf2t FAILS it in ipd, ipd3 and staghunt -- it forgives the first
#      defection by construction, so an N-1 betrayal costs nothing. Pooling
#      means one third of the roster was actively cancelling the contrast the
#      wave exists to measure. `--nohole-shape` drops tf2t from both arms.
#
#   2. One run per opponent. grim and tft differ in exactly one thing --
#      whether forgiveness exists at all -- so running them separately turns
#      "punishment shape" from a nuisance variable into the x-axis. Six cells:
#      {grim, tft} x {nohole, eg, inf}.
#
#   3. Fresh runs, not resumes. The think3 directories on this box carry
#      metrics from more than one launch (the grim dirs have per-env rows for
#      envs their own config.json does not list), so their curves are not one
#      training trajectory. Nothing here reuses them.
#
# THE THREE ENDGAME CELLS ARE UNCHANGED from sbatch_think3_wave.sh:
#
#   nohole   the control: retaliating counterpart, finite horizon disclosed.
#   eg       nohole + hidden reward charge on betrayals in the last quarter of
#            the cooperative horizon (never shown to the agent).
#   inf      nohole with the round count scrubbed from every observation.
#
# SEVEN ENVS, NOT FOUR. Only `core.SHAPE_ENVS` (ipd, ipd3, staghunt,
# winasmuch) carry a matched grim/tft pair; public_goods, dond and trust have
# no such pair and rotate their own populations identically in both arms. So
# the two arms differ in 4 of 7 envs and the other 3 are shared ballast. That
# is deliberate: it keeps this wave's roster identical to think3, hole-noisy,
# adaptive and adaptrec, so the arms remain comparable to the rest of the
# study and to EVAL_SUITE transfers -- and because every metric is logged
# per-env, the clean 4-env contrast is recoverable from the same runs by
# filtering to SHAPE_ENVS. Training on the 4 alone would have thrown that away.
#
# NOT SLURM. This box has no scheduler and does not need one: train_mixed.py is
# a sampling client and every forward pass happens in the Tinker service, so
# the cells are I/O-bound and share 8 CPUs happily. They are plain background
# processes, staggered so six checkpoint saves do not land on the same second.
set -uo pipefail
cd "$(dirname "$0")"

PY=/home/ubuntu/venvs/tinker-ipd/bin/python
RUNS=/home/ubuntu/strategy-behavior/hole_exp/runs
LOGS=/home/ubuntu/strategy-behavior/hole_exp/logs/think4

ENVS="ipd public_goods dond trust ipd3 staghunt winasmuch"
MODEL="${MODEL:-Qwen/Qwen3.8-27B}"
SEED="${SEED:-0}"
STEPS="${STEPS:-150}"
CKPT_EVERY="${CKPT_EVERY:-5}"
WORKERS="${WORKERS:-10}"
STAGGER="${STAGGER:-45}"

# Cell -> the flags that define it. Keyed exactly as think3 so the labels line
# up: `eg` writes `_eg2`, `inf` writes `_inf`.
declare -A CELL=(
  [nohole]="--consequence nohole"
  [eg]="--consequence nohole --endgame-penalty 2.0 --endgame-frac 0.25"
  [inf]="--consequence nohole --horizon infinite"
)

set -a; . /home/ubuntu/.research_env 2>/dev/null || true; set +a
export HOME=/home/ubuntu
export XDG_CACHE_HOME=/home/ubuntu/.cache
export WANDB_DIR=/home/ubuntu/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR" "$LOGS" "$RUNS"

# TWO WANDB KEYS LIVE IN ~/.research_env AND THE OBVIOUS ONE IS WRONG.
# `WANDB_API_KEY` authenticates as `anrui0706`, whose only entity is a personal
# Berkeley one; `--wb-entity thefleet` under it fails with a bare
# `CommError: permission denied` AFTER the run has already built its config and
# started, so all six cells died a minute in. `FLEET_WANDB_API_KEY` is the one
# that carries `thefleet`. Preferring it here rather than editing the env file
# leaves the personal key intact for anything that wants it.
if [ -n "${FLEET_WANDB_API_KEY:-}" ]; then
  export WANDB_API_KEY="$FLEET_WANDB_API_KEY"
fi

# wandb is a convenience; `runs/<label>/metrics.jsonl` is the source every
# figure in this package actually reads. A dashboard that is down, rate-limited
# or misconfigured must not take the wave with it, so the flag is decided once
# here by an actual auth probe instead of discovered per-cell as a crash.
WB_FLAG="--use-wb"
if ! "$PY" - <<'PYEOF' >/dev/null 2>&1
import os, sys, wandb
api = wandb.Api(api_key=os.environ["WANDB_API_KEY"])
sys.exit(0 if os.environ.get("WB_ENTITY", "thefleet") in api.viewer.teams else 1)
PYEOF
then
  echo "[think4] wandb auth probe failed -> running without --use-wb" >&2
  WB_FLAG=""
fi

# CKPT_EVERY=5, not think3's 10. The reasoning-marker curves have one point per
# CHECKPOINT, and the think2 figure this iterates on had four points per arm
# across a run that reached step 80. These runs are unlikely to get that far
# before the figure is due, so the checkpoint grid is what decides whether the
# morning's curve has three points or six. Saves are cheap relative to a step.

one_cell() {  # shape, cell
  local shape="$1" cell="$2"
  local flags="${CELL[$cell]:?unknown cell $cell}"
  local label="mixed_think4_nohole-think-${shape}_d1_s${SEED}"
  case "$cell" in
    eg)  label="${label}_eg2" ;;
    inf) label="${label}_inf" ;;
  esac
  echo "[think4] $shape/$cell -> $label"
  "$PY" train_mixed.py \
    --envs $ENVS \
    $flags \
    --nohole-shape "$shape" \
    --think --reasoning-effort low \
    --label-suffix think4 \
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
    --workers "$WORKERS" \
    --dump-traces 24 \
    --out "$RUNS" \
    $WB_FLAG
}

if [ "${1:-}" = "--all" ]; then
  for shape in grim tft; do
    for cell in nohole eg inf; do
      log="$LOGS/${shape}-${cell}.log"
      echo "[think4] launching $shape/$cell -> $log"
      setsid nohup "$0" "$shape" "$cell" > "$log" 2>&1 < /dev/null &
      sleep "$STAGGER"
    done
  done
  echo "[think4] all six launched. tail -f $LOGS/*.log"
  exit 0
fi

SHAPE="${1:?shape: grim | tft}"
CELL_NAME="${2:?cell: nohole | eg | inf}"
one_cell "$SHAPE" "$CELL_NAME"
