#!/usr/bin/env bash
# stall_watchdog.sh -- emit a line when a training log stops advancing.
#
#   stall_watchdog.sh <stall-minutes> <log> [log ...]
#
# spiral-multi job 43 wedged silently right after "weights @version=35
# broadcasted to actors": slurm still reported the job as RUNNING, the
# allocation was held, and no error was ever printed. It burned ~5h before
# anyone looked. Nothing in the stack notices this -- slurm only sees a live
# process, and the run's own logging is what stopped. So watch log mtime.
set -uo pipefail
STALL_MIN="${1:?usage: stall_watchdog.sh <stall-minutes> <log>...}"; shift
LOGS=("$@")
declare -A warned
while true; do
    for f in "${LOGS[@]}"; do
        [ -f "$f" ] || continue
        age=$(( ($(date +%s) - $(stat -c %Y "$f")) / 60 ))
        if [ "$age" -ge "$STALL_MIN" ]; then
            if [ "${warned[$f]:-0}" != "$age" ]; then
                echo "STALLED: $(basename "$f") no output for ${age}m (threshold ${STALL_MIN}m)"
                warned[$f]=$age
            fi
        else
            warned[$f]=0
        fi
    done
    sleep 120
done
