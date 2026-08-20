#!/usr/bin/env bash
# watch_scaling.sh -- one event per NEW checkpoint, plus every terminal state.
#
# Emits on failure signatures as well as progress: a monitor that greps only for
# checkpoints stays silent through a crashloop, and silence is indistinguishable
# from "still training". Also emits when the queue empties, which is the signal
# the readout can start.
set -uo pipefail
cd /workspace/allie/strategy-behavior/hole_exp
RUNS=runs/scaling
LOGS=logs/scaling
seen=""
# Separate from `seen`: that variable is REASSIGNED to the checkpoint snapshot
# every loop, so failure keys appended to it were wiped each pass and every
# already-reported failure fired again on the next tick.
failed=""

snapshot() {  # "label:maxstep" per run, one per line
  for f in "$RUNS"/*/checkpoints.json; do
    [ -f "$f" ] || continue
    lab=$(basename "$(dirname "$f")")
    mx=$(python3 -c "
import json,sys
try: d=json.load(open('$f'))
except Exception: sys.exit()
print(max(int(k) for k in d) if d else 0)" 2>/dev/null)
    [ -n "$mx" ] && echo "$lab:$mx"
  done
}

while true; do
  cur=$(snapshot | sort)
  # New (label, step) pairs only -- never re-announce a step already reported.
  if [ -n "$cur" ]; then
    comm -13 <(printf '%s\n' "$seen") <(printf '%s\n' "$cur") 2>/dev/null \
      | grep -v '^$' | sed 's/^/[ckpt] /'
    seen="$cur"
  fi

  # Terminal failures. train_mixed.py dies loudly; slurm kills print to the .out.
  # No pipe into the loop: a `... | while` body runs in a SUBSHELL, so the
  # `failed` list it built was discarded the moment the loop exited and every
  # failure re-fired forever.
  for f in $(grep -lE "Traceback|FATAL|budget mismatch|CANCELLED|DUE TO TIME LIMIT|would poison the mix" \
             "$LOGS"/*.out 2>/dev/null); do
      key=" $(basename "$f") "
      case "$failed" in *"$key"*) continue;; esac
      echo "[FAIL] $(basename "$f"): $(grep -hoE 'Traceback|FATAL.*|budget mismatch.*|CANCELLED.*|DUE TO TIME LIMIT|would poison the mix.*' "$f" | tail -1)"
      failed="$failed$key"
  done

  n=$(squeue -u "$(whoami)" -h -n scale-game-n1-hole,scale-game-n2-hole,scale-game-n4-hole,scale-game-n8-hole,scale-synth-n1-hole,scale-synth-n2-hole,scale-synth-n4-hole,scale-synth-n8-hole,scale-game-n1-nohole,scale-game-n8-nohole,scale-synth-n1-nohole,scale-synth-n8-nohole,scale-game-n2-nohole,scale-game-n4-nohole,scale-synth-n2-nohole,scale-synth-n4-nohole 2>/dev/null | wc -l)
  if [ "$n" = "0" ]; then
    echo "[QUEUE EMPTY] no scaling jobs left; $(printf '%s\n' "$cur" | wc -l) runs on disk"
    exit 0
  fi
  sleep 240
done
