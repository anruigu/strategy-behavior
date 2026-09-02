#!/usr/bin/env bash
# Remaining 0901-single-model knob sweeps. v1 of this driver derailed after
# GROUP A: bash reads a script INCREMENTALLY from a file descriptor, the
# backgrounded `wave ... &` subshells share that descriptor, and the parent
# resumed parsing at an offset five lines wrong -- reporting a syntax error on
# a blank line and skipping two of the three GROUP B launches. `bash -n`
# cannot catch it because it is a runtime read artefact, not a parse error.
#
# THE FIX IS THE main() WRAPPER. Bash must parse a function body in full
# before it can run it, so the whole script is read up front and no later
# execution depends on the file offset. Do not un-wrap this.
set -u

main () {
  local V=~/venvs/tinker-ipd/bin/python
  local COMMON="--models gemini-flash --rounds 3 --episodes 4 --chains 3 \
--max-tokens 3072 --reflect-max-tokens 4000 --workers 16 --traces"
  local G29="tuning29"
  local G23="ref_estate ref_exchange gen_seven_seal gen_quiet_sonar gen_icebound gen_sovereign_vaults gen_frontline_depot gen_harbor_customs ta_ipd ta_staghunt ta_ipd3 ta_pubgoods ta_winasmuch ta_liarsdice ta_kuhn ta_negotiation ta_blindauction ta_letterauction nat_open_gate nat_cargo_pledge nat_seam_ledger nat_mirror_manifest nat_meridian_convoy"

  wave () {
    local tag=$1; shift
    echo "[driver] $(date -u +%H:%M:%S) start $tag"
    $V run_referee_spartan.py --tag "$tag" $COMMON "$@" > logs/$tag.log 2>&1
    echo "[driver] $(date -u +%H:%M:%S) done  $tag rc=$?"
  }

  # tune_win is ALREADY RUNNING from the derailed v1 and is not our child, so
  # it cannot be waited on -- poll for it instead. Re-launching the tag would
  # be harmless (the runner resumes from rows.jsonl) but would double the
  # in-flight request count against the shared endpoint, which is the one
  # thing the worker budget is sized to avoid.
  echo "[driver] GROUP B -- winmax + nohole, alongside the running tune_win"
  wave tune_winmax --games $G29 --temperature 1.0 --condition winmax --allow-winmax &
  wave tune_nohole --games $G29 --temperature 1.0 --arm nohole &
  wait
  while pgrep -f "tag tune_win" > /dev/null; do sleep 20; done
  echo "[driver] $(date -u +%H:%M:%S) GROUP B complete (tune_win included)"

  echo "[driver] GROUP C -- game horizon; 23 cells, the other 6 have no ROUNDS"
  wave tune_turns05 --games $G23 --temperature 1.0 --game-rounds-scale 0.5 &
  wave tune_turns20 --games $G23 --temperature 1.0 --game-rounds-scale 2.0 &
  wait

  echo "[driver] ALL SWEEPS COMPLETE $(date -u +%H:%M:%S)"
}

main "$@"
