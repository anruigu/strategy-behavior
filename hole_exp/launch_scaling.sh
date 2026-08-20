#!/usr/bin/env bash
# launch_scaling.sh -- submit the env-count ladder (0820-scaling-envs.md).
#
#   ./launch_scaling.sh          # the priority 12
#   ./launch_scaling.sh fill     # the 4 middle nohole rungs, added if capacity allows
#   ./launch_scaling.sh show     # what would be submitted
#
# WHY 12 AND NOT 16. The plan budgets 8 runs (one arm per rung per family) and
# reads the curve against the BASE model. That leaves the curve unable to
# separate "more hole exposure" from "more diverse RL of any kind", so this adds
# the `nohole` control at the ENDPOINTS of each family -- n=1 and n=8. If the
# hole-nohole gap at n=8 exceeds the gap at n=1, the rise is about the hole; if
# both arms rise together, it is about diversity. `fill` adds the middle nohole
# rungs (n=2, n=4) to complete the matched pair at every rung, and is held back
# only because 16 concurrent runs on one Tinker account contend. Submitting it
# later is cheap: checkpoints land every 10 steps, so a late-started arm is still
# readable at whatever step all arms share.
set -uo pipefail
cd "$(dirname "$0")"
MODE="${1:-run}"

PRIORITY=(
  "game 1 hole"  "game 2 hole"  "game 4 hole"  "game 8 hole"
  "synth 1 hole" "synth 2 hole" "synth 4 hole" "synth 8 hole"
  "game 1 nohole"  "game 8 nohole"
  "synth 1 nohole" "synth 8 nohole"
)
FILL=(
  "game 2 nohole"  "game 4 nohole"
  "synth 2 nohole" "synth 4 nohole"
)

case "$MODE" in
  fill) SET=("${FILL[@]}") ;;
  show) SET=("${PRIORITY[@]}" "${FILL[@]}") ;;
  *)    SET=("${PRIORITY[@]}") ;;
esac

mkdir -p logs/scaling runs/scaling
for spec in "${SET[@]}"; do
  read -r fam n arm <<<"$spec"
  name="scale-${fam}-n${n}-${arm}"
  # Idempotent: a rung already on the queue is not resubmitted, so re-running
  # this after adding `fill` cannot double-launch the priority set.
  if squeue -u "$(whoami)" -h -o '%j' 2>/dev/null | grep -qx "$name"; then
    echo "  [queued] $name"; continue
  fi
  if [ "$MODE" = "show" ]; then echo "  [would] $name"; continue; fi
  jid=$(sbatch --parsable --job-name="$name" sbatch_scaling.sh "$fam" "$n" "$arm")
  echo "  [sub] $name -> job $jid"
done
