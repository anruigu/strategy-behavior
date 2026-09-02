#!/usr/bin/env bash
# 0901-single-model.md knob sweeps. One knob per wave, everything else at the
# tune_defaults_gemflash baseline: neutral / hole / T=1.0 / 3072 tokens /
# R0-R3 x 4 episodes x 3 chains over the 29-cell tuning roster.
#
# WORKERS 16, NOT 24. The baseline validated 24 in flight against the Google
# direct endpoint at 16.4 calls/s. Three waves at 24 would be 72 in flight and
# ~3,000 RPM, and an exhausted retry returns empty -- which is scored invalid
# and falls back to the HONEST move. Sixteen keeps three concurrent waves at
# 48 in flight, twice what is known good, and the cost of being wrong here is
# fake honest data rather than a slow run.
set -u
V=~/venvs/tinker-ipd/bin/python
COMMON="--models gemini-flash --rounds 3 --episodes 4 --chains 3 \
--max-tokens 3072 --reflect-max-tokens 4000 --workers 16 --traces"
G29="tuning29"
G23="ref_estate ref_exchange gen_seven_seal gen_quiet_sonar gen_icebound gen_sovereign_vaults gen_frontline_depot gen_harbor_customs ta_ipd ta_staghunt ta_ipd3 ta_pubgoods ta_winasmuch ta_liarsdice ta_kuhn ta_negotiation ta_blindauction ta_letterauction nat_open_gate nat_cargo_pledge nat_seam_ledger nat_mirror_manifest nat_meridian_convoy"

wave () {  # wave <tag> <extra args...>
  local tag=$1; shift
  echo "[driver] $(date -u +%H:%M:%S) start $tag"
  $V run_referee_spartan.py --tag "$tag" $COMMON "$@" \
    > logs/$tag.log 2>&1
  echo "[driver] $(date -u +%H:%M:%S) done  $tag rc=$?"
}

echo "[driver] GROUP A -- temperature (baseline T=1.0 already on disk)"
wave tune_T07 --games $G29 --temperature 0.7 &
wave tune_T15 --games $G29 --temperature 1.5 &
wave tune_T20 --games $G29 --temperature 2.0 &
wait

echo "[driver] GROUP B -- prompt ladder + the nohole counterfactual arm"
wave tune_win    --games $G29 --temperature 1.0 --condition win &
wave tune_winmax --games $G29 --temperature 1.0 --condition winmax --allow-winmax &
wave tune_nohole --games $G29 --temperature 1.0 --arm nohole &
wait

echo "[driver] GROUP C -- game horizon (23 cells; 6 have no ROUNDS and refuse)"
wave tune_turns05 --games $G23 --temperature 1.0 --game-rounds-scale 0.5 &
wave tune_turns20 --games $G23 --temperature 1.0 --game-rounds-scale 2.0 &
wait

echo "[driver] ALL SWEEPS COMPLETE $(date -u +%H:%M:%S)"
