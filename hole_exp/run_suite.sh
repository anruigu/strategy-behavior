#!/usr/bin/env bash
# run_suite.sh -- launch the hole atlas, or any slice of it.
#
# The full atlas is 10 environments x 2 arms x 5 doses = 100 cells, which is not
# a thing anyone launches at once. The defaults here are the FIRST WAVE from
# 0817-suite: every environment, both arms, at the top of the dose range only.
# That is the present/absent contrast (20 runs) and it is what says whether a
# hole type transfers at all. Dose-response comes second, on the environments
# the first wave says are worth spending it on:
#
#   ENVS="trust politics" DOSES="0.0 0.25 0.5 0.75 1.0" ./run_suite.sh
#
# Everything is one cell per process, sequential by default: a Tinker run is
# network-bound, not CPU-bound, and the rollout threads inside each run already
# saturate the account's rate limit. PARALLEL=n runs n cells at once if your
# account can take it.
#
#   ENVS="trust" ARMS="hole" ./run_suite.sh --steps 30       # one cell, short
#   DRY=1 ./run_suite.sh                                     # no API calls
#   SELFPLAY=1 ENVS="markets principal_agent" ./run_suite.sh # the both-seats arms
#
# Extra flags after -- go straight to train_hole.py.
set -uo pipefail
cd "$(dirname "$0")"

PY="${PY:-/workspace/allie/venvs/tinker-ipd/bin/python}"
ENVS="${ENVS:-ipd ultimatum dond public_goods trust politics markets commerce gatekeeping principal_agent}"
ARMS="${ARMS:-hole nohole}"
DOSES="${DOSES:-1.0}"
SEEDS="${SEEDS:-0}"
STEPS="${STEPS:-90}"
MODEL="${MODEL:-Qwen/Qwen3.5-9B}"
PARALLEL="${PARALLEL:-1}"
DRY="${DRY:-0}"
SELFPLAY="${SELFPLAY:-0}"
LOGDIR="${LOGDIR:-logs}"

mkdir -p "$LOGDIR"

# The validity harness first, on exactly the cells about to be launched. It
# costs seconds and it is the difference between a failed experiment and a
# failed experiment you paid for.
echo "== check_suite over the requested cells =="
# shellcheck disable=SC2086
"$PY" check_suite.py --envs $ENVS --doses $DOSES --seeds 32 || {
  echo "check_suite failed: at least one requested cell is not a runnable"
  echo "experiment. Fix it or drop it; do not launch over the top of this."
  exit 1
}

pids=()
for env in $ENVS; do
  for arm in $ARMS; do
    for dose in $DOSES; do
      for seed in $SEEDS; do
        label="${env}_${arm}_d${dose}_s${seed}"
        args=(--env "$env" --consequence "$arm" --dose "$dose" --seed "$seed"
              --model "$MODEL" --steps "$STEPS")
        [ "$DRY" = "1" ] && args+=(--dry-run)
        [ "$DRY" = "1" ] || args+=(--use-wb)
        if [ "$SELFPLAY" = "1" ]; then
          case "$env" in
            markets|principal_agent) args+=(--selfplay); label="${label}_sp" ;;
            *) echo "skip $env: no self-play seat"; continue ;;
          esac
        fi
        echo "== $label =="
        "$PY" train_hole.py "${args[@]}" "$@" 2>&1 | tee "$LOGDIR/${label}.log" &
        pids+=($!)
        while [ "$(jobs -rp | wc -l)" -ge "$PARALLEL" ]; do wait -n; done
      done
    done
  done
done
wait
echo "all cells finished; logs in $LOGDIR/"
