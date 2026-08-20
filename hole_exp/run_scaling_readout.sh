#!/usr/bin/env bash
# run_scaling_readout.sh -- wait for the ladder to train, then read it out.
#
#   nohup ./run_scaling_readout.sh > logs/scaling/readout.log 2>&1 &
#   DEADLINE_H=5 ./run_scaling_readout.sh      # freeze earlier
#
# Three phases, in order, all keyed to ONE frozen step:
#   1. wait   -- until the queue empties, or DEADLINE_H elapses, whichever first
#   2. tierA  -- eval_scaling.py, Tinker-direct, ~1h for 13 arms
#   3. tierB  -- one sbatch per arm (insider / MACHIAVELLI / AgentMisalignment)
#   4. figs   -- make_scaling_figs.py, whatever data exists at the time
#
# WHY A DEADLINE. Twelve runs contend for one Tinker account and the observed
# spread on comparable runs was 3.3h to 9.1h for the same work. If they are
# still going at the deadline, the readout takes the highest step EVERY arm has
# reached rather than waiting for the slowest -- an incomplete ladder read at a
# common step is a result; a complete ladder read at 9am is not. The frozen step
# is written into every output file, so a later re-read at step 70 is a
# different file rather than a silent overwrite.
set -uo pipefail
cd "$(dirname "$0")"

PY=/workspace/allie/venvs/tinker-ipd/bin/python
LPY=/workspace/allie/venvs/spiral/bin/python
# Only training/tinker/.venv has matplotlib; the figure script needs nothing else
# from it (scaling_rungs imports registry only under __main__).
TPY=/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python
# Minutes, not hours: bash arithmetic is integer-only, so DEADLINE_H=3.05 is a
# syntax error rather than three hours. DEADLINE_H stays supported for round
# numbers; DEADLINE_MIN wins when both are set.
DEADLINE_H="${DEADLINE_H:-6}"
DEADLINE_MIN="${DEADLINE_MIN:-$((DEADLINE_H * 60))}"
SEEDS="${SEEDS:-16}"
TD_SEEDS="${TD_SEEDS:-24}"
WORKERS="${WORKERS:-48}"
DO_TIERB="${DO_TIERB:-1}"
FIGS=/workspace/allie/strategy-behavior/results/0820_scaling_plots
export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache

t0=$(date +%s)
deadline=$((t0 + DEADLINE_MIN * 60))
echo "[readout] waiting; deadline in ${DEADLINE_MIN}min ($(date -d "@$deadline" '+%F %T'))"

# A bare clock deadline is brittle at the boundary: checkpoints land every 10
# steps, so freezing 9 minutes before the slowest arm saves step 40 costs that
# whole FAMILY a rung of training (40 -> 30). So the soft deadline only fires
# once every family has reached MIN_STEP; HARD_CAP_MIN bounds the wait either way.
MIN_STEP="${MIN_STEP:-40}"
HARD_CAP_MIN="${HARD_CAP_MIN:-$((DEADLINE_MIN + 30))}"
hardcap=$((t0 + HARD_CAP_MIN * 60))
echo "[readout] soft deadline $(date -d "@$deadline" '+%H:%M'), hard cap "\
"$(date -d "@$hardcap" '+%H:%M'), min step $MIN_STEP"

famstep() {  # lowest per-family common step, or 0
  "$PY" -c '
import sys
sys.path.insert(0, "/workspace/allie/strategy-behavior/hole_exp")
import eval_scaling as E
try:
    _, _, m = E.resolve(None, None, per_family=True)
    v = m["step_by_family"]
    print(min(v.values()) if len(v) == len(E.S.FAMILIES) else 0)
except SystemExit:
    print(0)
' 2>/dev/null || echo 0
}

while true; do
  n=$(squeue -u "$(whoami)" -h -o '%j' 2>/dev/null | grep -c '^scale-' || true)
  [ "$n" = "0" ] && { echo "[readout] queue empty after $(( ($(date +%s)-t0)/60 ))m"; break; }
  now=$(date +%s)
  if [ "$now" -ge "$hardcap" ]; then
    echo "[readout] HARD CAP hit with $n job(s) running (step $(famstep))"; break
  fi
  if [ "$now" -ge "$deadline" ]; then
    fs=$(famstep)
    if [ "${fs:-0}" -ge "$MIN_STEP" ]; then
      echo "[readout] DEADLINE hit, every family at step >= $MIN_STEP (=$fs)"; break
    fi
    echo "[readout] past deadline but slowest family only at step ${fs:-0} < $MIN_STEP; holding"
  fi
  sleep 300
done

# -- freeze ONCE into a manifest --------------------------------------------
# Both tiers read this file. Resolving separately would let training advance in
# between and have Tier A and Tier B describe different checkpoints under one
# label. Per-family: game episodes are multi-turn and train ~60% slower per
# step, so one step across all 12 arms would throw away ~30 steps of synthetic
# training to match the slowest game arm.
MAN=results/scaling/manifest.json
mkdir -p results/scaling
"$PY" -c '
import json, sys
sys.path.insert(0, "/workspace/allie/strategy-behavior/hole_exp")
import eval_scaling as E
models, step, meta = E.resolve(None, None, per_family=True)
json.dump({"models": models, "step": step, "meta": meta},
          open(sys.argv[1], "w"), indent=1)
# No subscripts inside the f-string: this block is inside bash SINGLE quotes, so
# a \" survives as a literal backslash, and a backslash inside an f-string
# expression is a SyntaxError. Bind first, format with %s.
sbf = meta["step_by_family"]
drop = meta["dropped_missing_this_step"]
print("frozen step=%s by_family=%s arms=%d dropped=%s"
      % (step, sbf, len(models), drop))
' "$MAN" || { echo "[readout] FATAL could not freeze a manifest"; exit 1; }
STEP=$("$PY" -c "import json;print(json.load(open('$MAN'))['step'])")
echo "[readout] frozen step = $STEP  (manifest: $MAN)"
[ "$STEP" -gt 0 ] || { echo "[readout] FATAL no common non-zero step"; exit 1; }

# -- Tier B FIRST, but only to SUBMIT --------------------------------------
# The two tiers are independent and use different resources: Tier A samples
# Tinker directly from this process, Tier B runs as Slurm jobs behind per-arm
# proxies. Submitting Tier B before running Tier A overlaps ~2-3h of Tier B with
# ~1-1.5h of Tier A instead of adding them. Both read the SAME frozen manifest,
# so overlapping cannot desynchronise which checkpoint each tier describes.
if [ "$DO_TIERB" = "1" ]; then
  echo "[readout] Tier B submit @ step $STEP"
  port=8700
  "$PY" -c '
import json, sys
for arm, m in json.load(open(sys.argv[1]))["models"].items():
    print(arm, m)
' "$MAN" | while read -r arm model; do
    jid=$(sbatch --parsable --job-name="ext-$arm" sbatch_scaling_ext.sh \
          "$arm" "$model" "$port")
    echo "  [sub] ext-$arm -> $jid (port $port)"
    port=$((port + 1))
  done
fi

# -- Tier A ----------------------------------------------------------------
echo "[readout] Tier A @ step $STEP"
"$PY" eval_scaling.py --manifest "$MAN" --seeds "$SEEDS" --td-seeds "$TD_SEEDS" \
  --workers "$WORKERS" 2>&1 | sed 's/^/  /'
echo "[readout] TIER A DONE"

# Figures from Tier A alone, so the main deliverable lands as early as possible
# and survives Tier B being cut off.
"$TPY" make_scaling_figs.py --step "$STEP" 2>&1 | sed 's/^/  /' || true
"$TPY" scaling_shape.py --step "$STEP" --md "$FIGS/scaling-shape.md" \
  2>&1 | sed 's/^/  /' || true

if [ "$DO_TIERB" = "1" ]; then
  while [ "$(squeue -u "$(whoami)" -h -o '%j' 2>/dev/null | grep -c '^ext-scale\|^ext-base' || true)" != "0" ]; do
    sleep 300
  done
  echo "[readout] TIER B DONE"

  # MACHIAVELLI needs its own scoring pass (the runner only writes trajectories).
  arms=$("$PY" -c '
import json, sys
print(" ".join(json.load(open(sys.argv[1]))["models"]))
' "$MAN")
  # shellcheck disable=SC2086
  MACH_EPS=3 "$LPY" mach_scaling_summary.py $arms 2>&1 | sed 's/^/  /' || true
fi

# -- figures ---------------------------------------------------------------
"$TPY" make_scaling_figs.py --step "$STEP" 2>&1 | sed 's/^/  /'
"$TPY" scaling_shape.py --step "$STEP" --md "$FIGS/scaling-shape.md" \
  2>&1 | sed 's/^/  /' || true
echo "[readout] ALL DONE step=$STEP elapsed=$(( ($(date +%s)-t0)/60 ))m"
