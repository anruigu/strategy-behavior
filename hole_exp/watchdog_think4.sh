#!/usr/bin/env bash
# Keep the think4 support processes alive overnight, and say so when they were not.
#
#   setsid nohup ./watchdog_think4.sh > logs/think4/watchdog.log 2>&1 &
#
# The six TRAINING runs are deliberately NOT restarted here. A training process
# that has exited has either finished its 150 steps or died partway, and in the
# second case relaunching it would start a fresh run at step 0 into the same
# directory -- appending a second trajectory to one metrics.jsonl under one
# label, which is exactly the mixed-provenance mess the think3 directories on
# this box are already in. A dead training run is reported and left dead.
#
# The two SUPPORT processes are restartable, because both are idempotent:
# `traces_over_training.py` re-samples only checkpoints it has not seen (and on
# a fresh process, re-samples all of them into the same page with clear=False),
# and `refresh_think4.sh` rebuilds pages and the figure from whatever is on
# disk. Losing either silently is the real risk: the figure would quietly stop
# updating and still be sitting there in the morning looking current.
set -uo pipefail
cd "$(dirname "$0")"

LOGS=/home/ubuntu/strategy-behavior/hole_exp/logs/think4
PY=/home/ubuntu/venvs/tinker-ipd/bin/python
EVERY="${EVERY:-300}"

set -a; . /home/ubuntu/.research_env 2>/dev/null || true; set +a
export WANDB_API_KEY="${FLEET_WANDB_API_KEY:-${WANDB_API_KEY:-}}"
export HOME=/home/ubuntu XDG_CACHE_HOME=/home/ubuntu/.cache

start_sweep() {
  setsid nohup "$PY" traces_over_training.py \
    --runs "mixed_think4_*" \
    --envs ipd trust ipd3 staghunt winasmuch \
    --seeds 3 --temperature 0.7 --max-tokens 1024 \
    --think --workers 4 --watch --poll 600 --until 150 \
    >> "$LOGS/traces-sweep.log" 2>&1 < /dev/null &
}

start_refresh() {
  setsid nohup ./refresh_think4.sh --loop 900 >> "$LOGS/refresh.log" 2>&1 < /dev/null &
}

while true; do
  ts=$(date -u '+%F %T')
  # COUNT BY LABEL, NOT BY ARGUMENT ORDER. The original pattern was
  # "train_mixed.py --envs", which matched the launcher's flag order and
  # silently stopped matching when resume_think4.sh rebuilt the command from
  # config.json with --envs last -- so the watchdog reported train=0/6 while
  # all six were running. `--label-suffix think4` is part of the run's
  # identity, appears exactly once per process, and does not match the
  # think3 wave sharing this box.
  alive=$(ps -eo args | grep -c "[t]rain_mixed.py.*--label-suffix think4" || true)

  if ! pgrep -f "traces_over_training.py" > /dev/null; then
    echo "[$ts] traces sweep DOWN -> restarting"
    start_sweep
  fi
  if ! pgrep -f "refresh_think4.sh --loop" > /dev/null; then
    echo "[$ts] refresh loop DOWN -> restarting"
    start_refresh
  fi
  # PROBE THE PORT, NOT THE PROCESS NAME. `pgrep -f "http.server 8792"` matches
  # any shell whose command line merely CONTAINS that string -- including the
  # one that launched this watchdog, if the launch and a status check were typed
  # as one command. That is exactly what happened: the viewer had been stopped
  # for the /home/ubuntu migration, the watchdog matched the invoking shell,
  # concluded the viewer was up, and left it down. A port probe cannot lie about
  # whether the page is actually being served.
  if ! curl -sf -o /dev/null --max-time 5 http://127.0.0.1:8792/ ; then
    echo "[$ts] viewer NOT SERVING -> restarting"
    ( cd /home/ubuntu/SkyRL-Fleet/tools/trace-viewer \
      && setsid nohup ./serve.sh 8792 0.0.0.0 >> "$LOGS/viewer.log" 2>&1 < /dev/null & )
  fi

  # Progress line, so the log doubles as an overnight record of the step rate.
  steps=""
  for d in runs/mixed_think4_*; do
    n=$(basename "$d" | sed 's/^mixed_think4_nohole-think-//; s/_d1_s0//')
    s=$(tail -1 "$d/metrics.jsonl" 2>/dev/null \
        | /home/ubuntu/venvs/tools/bin/python -c \
          'import sys,json;print(json.load(sys.stdin)["step"])' 2>/dev/null || echo -)
    steps="$steps $n=$s"
  done
  df_free=$(df -h /home/ubuntu | awk 'NR==2{print $4}')
  echo "[$ts] train=$alive/6 free=$df_free steps:$steps"

  sleep "$EVERY"
done
