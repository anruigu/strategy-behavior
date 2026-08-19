#!/usr/bin/env bash
# run_mixed.sh -- one policy trained on the whole atlas at once, both arms.
#
# This is the mixed-environment experiment (train_mixed.py), NOT the per-cell
# atlas (run_suite.sh). It launches the matched pair -- a policy trained across
# all ten envs in the `hole` arm and its `nohole` control -- so the dependent
# variable is the same as everywhere else here: the DIFFERENCE in transfer to
# the held-out battery, never in-env reward.
#
#   ./run_mixed.sh                                   # both arms, all envs, dose 1.0
#   ENVS="trust politics markets" ./run_mixed.sh     # mix a subset
#   ARMS="hole" ./run_mixed.sh --steps 30            # one arm, short
#   DRY=1 ./run_mixed.sh                             # no API calls
#
# train_mixed.py runs check_suite over every env in the mix and refuses to launch
# if any cell fails, so a single broken cell cannot poison the run. Extra flags
# after -- go straight to train_mixed.py.
set -uo pipefail
cd "$(dirname "$0")"

PY="${PY:-/workspace/allie/venvs/tinker-ipd/bin/python}"
ENVS="${ENVS:-}"     # empty -> train_mixed.py's default (all ten)
ARMS="${ARMS:-hole nohole}"
DOSE="${DOSE:-1.0}"
SEED="${SEED:-0}"
STEPS="${STEPS:-90}"
MODEL="${MODEL:-Qwen/Qwen3.5-9B}"
PARALLEL="${PARALLEL:-1}"
DRY="${DRY:-0}"
LOGDIR="${LOGDIR:-logs}"

mkdir -p "$LOGDIR"

pids=()
for arm in $ARMS; do
  label="mixed_${arm}_d${DOSE}_s${SEED}"
  args=(--consequence "$arm" --dose "$DOSE" --seed "$SEED"
        --model "$MODEL" --steps "$STEPS")
  # shellcheck disable=SC2086
  [ -n "$ENVS" ] && args+=(--envs $ENVS)
  [ "$DRY" = "1" ] && args+=(--dry-run)
  [ "$DRY" = "1" ] || args+=(--use-wb)
  echo "== $label =="
  "$PY" train_mixed.py "${args[@]}" "$@" 2>&1 | tee "$LOGDIR/${label}.log" &
  pids+=($!)
  while [ "$(jobs -rp | wc -l)" -ge "$PARALLEL" ]; do wait -n; done
done
wait
echo "all mixed arms finished; logs in $LOGDIR/"
