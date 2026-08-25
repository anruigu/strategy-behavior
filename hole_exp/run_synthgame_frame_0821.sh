#!/usr/bin/env bash
# 0821: the 5 hand-written suite-2 cells (synth_games.py) under GAME framing,
# for the 10-game checkpoints + base. Natural-frame twins are the 0819
# transfer-*.json numbers (identical protocol: check_suite screen, hole arm,
# dose 1.0, 12 seeds, neutral system, t=1.0/384).
set -uo pipefail
cd "$(dirname "$0")"
PY=/workspace/allie/venvs/tinker-ipd/bin/python
ENVS="politics markets commerce gatekeeping principal_agent"

declare -A MODELS=(
  [mixed_hole_d1_s0]="tinker://8c5a08a0-5e91-51cb-9441-4aa16a2c75db:train:0/sampler_weights/mixed_hole_d1_s0-step0090"
  [mixed_nohole_d1_s0]="tinker://868bceb4-8468-568f-97b9-5addca7bdd6e:train:0/sampler_weights/mixed_nohole_d1_s0-step0090"
  [base]="Qwen/Qwen3.6-27B"
)

for label in mixed_hole_d1_s0 mixed_nohole_d1_s0 base; do
  echo "=== screening $label (game frame) ==="
  HOLE_GEN_CANDIDATES=1 "$PY" check_suite.py --screen-only \
    --screen "${MODELS[$label]}" \
    --envs $ENVS --doses 1.0 --screen-arms hole \
    --screen-seeds 12 --workers 12 --cfg '{"frame":"game"}' \
    --json "results/transfer-frame/synthgame-$label.json" || echo "FAILED: $label"
done
echo "=== all done ==="
