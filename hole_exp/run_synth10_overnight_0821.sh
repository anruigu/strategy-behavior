#!/usr/bin/env bash
# 0821 overnight: hole/nohole mixed training on the 10 synthetic scenarios
# (the 5 hand-written suite-2 cells + the 5 dual-frame spec scenarios) --
# the synthetic counterpart of the 10-game pair mixed_{hole,nohole}_d1_s0.
# Same config as that pair: Qwen3.6-27B, 90 steps, dose 1.0, seed 0,
# group_size 6, one GRPO group per env (60 episodes/step).
# Surfaces are the SHIPPED ones: synth_games cells natural-framed,
# spec scenarios game-framed (their shipped candidate briefs).
set -uo pipefail
cd "$(dirname "$0")"
export HOLE_GEN_CANDIDATES=1
PY=/workspace/allie/venvs/tinker-ipd/bin/python
ENVS="politics markets commerce gatekeeping principal_agent tax_prep inventory_adjust hiring_panel confidential_desk financial_advisor_steering"

pids=()
for arm in hole nohole; do
  label="mixed_synth10_${arm}_d1_s0"
  echo "== launching $label =="
  "$PY" train_mixed.py --envs $ENVS \
    --consequence "$arm" --dose 1.0 --seed 0 \
    --model Qwen/Qwen3.6-27B --steps 90 \
    --label-suffix synth10 --use-wb \
    > "logs/${label}.log" 2>&1 &
  pids+=($!)
done
wait "${pids[@]}"
echo "== training finished; running post_run =="
WAIT=0 ./post_run.sh mixed_synth10_hole_d1_s0 mixed_synth10_nohole_d1_s0
echo "== overnight pipeline done =="
