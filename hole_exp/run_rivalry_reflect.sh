#!/usr/bin/env bash
# The 3x2 wave: three MA-update-dynamics strata x {shared, per-seat} reflection.
#
# STRATA come from payoff_regimes.py, offline, before a call is spent -- solo
# exploiter vs every-seat-exploits, on the cell's own payoff basis:
#   anti-rival      stops paying entirely   icebound +7.5->-20, orderbook +70.7->-0.9, kuhn 5.6->0
#   partially rival erodes but still pays   auction -79%, depot -67%, commons -46%
#   non-rival       payoff unchanged        invoice 84->84, harbor_customs -0.8%, seven_seal +0.05%
#
# EVERY CELL IS MULTI-SEAT. `--reflect per-seat` is undefined on a 1-player
# cell, so the DESIGN.md strata table's ta_pubgoods / ta_winasmuch (N=1) are
# out, and so is ta_liarsdice -- 1,395 calls in one sequential chain sets the
# wall clock for the whole wave, and it read 0.000 at --condition neutral, so
# it would buy a zero row at the price of an hour.
#
# TWO TAGS, NOT ONE. `key_of` makes rows identical by (game, model, condition,
# arm, visibility, rounds, episodes, opponents, seed) -- `reflect` is NOT in
# the key, so both arms under one tag would have the second arm resume-skip
# the first arm's chains and silently sample nothing.
set -u
CELLS="gen_icebound ref_orderbook ta_kuhn ref_commons ref_auction gen_frontline_depot ref_invoice gen_harbor_customs gen_seven_seal"
COMMON="--games $CELLS --models gemini-flash --opponents selfplay
        --condition neutral --arm hole --visibility own
        --rounds 3 --episodes 4 --chains 5
        --max-tokens 3072 --reflect-max-tokens 4000 --max-chars 6000
        --temperature 0.7 --workers 12 --traces"
PY=~/venvs/tinker-ipd/bin/python
cd /shared/allie/strategy-behavior/hole_exp
for arm in shared per-seat; do
  tag="ma_rivalry_${arm/-/}"
  echo "[driver] $(date +%H:%M:%S) start $tag"
  $PY run_referee_spartan.py $COMMON --reflect "$arm" --tag "$tag" \
      > "results/referee_spartan/${tag}.log" 2>&1 &
done
wait
echo "[driver] $(date +%H:%M:%S) BOTH ARMS COMPLETE"
