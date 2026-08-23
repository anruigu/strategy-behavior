#!/usr/bin/env bash
# 0820: eval the 10-game (5 hand-written + 5 TextArena) mixed checkpoints on the
# synthetic scenarios under GAME vs NATURAL framing. Same screen machinery and
# sampling (t=1.0, 384 tok) as the transfer-*.json numbers on the 0819 plot.
set -uo pipefail
cd "$(dirname "$0")"
PY=/workspace/allie/venvs/tinker-ipd/bin/python
ENVS="tax_prep inventory_adjust hiring_panel confidential_desk financial_advisor_steering"

declare -A MODELS=(
  [mixed_hole_d1_s0]="tinker://8c5a08a0-5e91-51cb-9441-4aa16a2c75db:train:0/sampler_weights/mixed_hole_d1_s0-step0090"
  [mixed_nohole_d1_s0]="tinker://868bceb4-8468-568f-97b9-5addca7bdd6e:train:0/sampler_weights/mixed_nohole_d1_s0-step0090"
  [base]="Qwen/Qwen3.6-27B"
)

for label in mixed_hole_d1_s0 mixed_nohole_d1_s0 base; do
  echo "=== screening $label ==="
  HOLE_GEN_CANDIDATES=1 "$PY" ablate_plant.py \
    --envs $ENVS --plants explicit menu --frames game natural \
    --seeds 12 --workers 64 --dose 1.0 \
    --screen "${MODELS[$label]}" \
    --json "results/transfer-frame/frame-$label.json" \
    --md "results/transfer-frame/frame-$label.md" || echo "FAILED: $label"
done
echo "=== all done ==="
