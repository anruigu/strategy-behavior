#!/usr/bin/env bash
# Rebuild everything downstream of the think4 runs, from whatever they have
# reached so far. Safe to run at any time, including mid-step.
#
#   ./refresh_think4.sh              # one pass
#   ./refresh_think4.sh --loop 900   # keep refreshing every 900s
#
# THREE OUTPUTS, TWO OF THEM VIEWER PAGES:
#
#   traces-t4-<arm>        the episodes the policy actually TRAINED on, lifted
#                          straight from `runs/<arm>/traces/` (written by
#                          --dump-traces at every checkpoint step). Free -- no
#                          sampling -- but the reasoning is NOT in them:
#                          train_mixed splits `<think>` off before the env
#                          parses the action, and only the answer is recorded.
#                          These are for reading episodes, not scoring markers.
#
#   traces-think-t4-<arm>  fresh episodes re-sampled from each frozen
#                          checkpoint with thinking ON, written by the separate
#                          long-running `traces_over_training.py --think`
#                          sweep. These DO carry the reasoning and are what the
#                          marker curves are scored off. This script does not
#                          build them, it just reports how far the sweep got.
#
#   reasoning_markers.png  the figure, over whatever exists right now.
#
# The figure venv is not the suite venv: `tools` has matplotlib and nothing
# else, `tinker-ipd` has the env stack and no matplotlib. plot_* only ever
# reads JSONL, so it runs in the small one on purpose.
set -uo pipefail
cd "$(dirname "$0")"

SUITE_PY=/home/ubuntu/venvs/tinker-ipd/bin/python
FIG_PY=/home/ubuntu/venvs/tools/bin/python
FIGDIR=/home/ubuntu/strategy-behavior/results/0826_think_curves
VIEWER=/home/ubuntu/SkyRL-Fleet/tools/trace-viewer

set -a; . /home/ubuntu/.research_env 2>/dev/null || true; set +a
export HOME=/home/ubuntu XDG_CACHE_HOME=/home/ubuntu/.cache

one_pass() {
  echo "=== refresh $(date -u '+%F %T') ==="

  for d in runs/mixed_think4_*; do
    [ -d "$d/traces" ] || continue
    ls "$d"/traces/step_*.jsonl >/dev/null 2>&1 || continue
    alias="traces-t4-$(basename "$d" | sed 's/^mixed_think4_nohole-think-//')"
    "$SUITE_PY" to_viewer.py --from-run "$d" --alias "$alias" 2>&1 \
      | tail -1 | sed 's/^/  [train-traces] /'
  done

  echo "  [reasoning pages] $(ls -d "$VIEWER"/public/data/traces-think-t4-* 2>/dev/null | wc -l)/6 built by the sweep"

  ( cd "$FIGDIR" && "$FIG_PY" plot_reasoning_markers_by_opponent.py 2>&1 \
      | sed 's/^/  [fig] /' )

  printf "  [steps] "
  for d in runs/mixed_think4_*; do
    n=$(basename "$d" | sed 's/^mixed_think4_nohole-think-//; s/_d1_s0//')
    s=$(tail -1 "$d/metrics.jsonl" 2>/dev/null \
        | "$FIG_PY" -c 'import sys,json;print(json.load(sys.stdin)["step"])' 2>/dev/null || echo -)
    printf "%s=%s " "$n" "$s"
  done
  echo
}

if [ "${1:-}" = "--loop" ]; then
  every="${2:-900}"
  while true; do
    one_pass
    sleep "$every"
  done
fi
one_pass
