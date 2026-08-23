#!/usr/bin/env bash
# rerun_tierb_step70.sh -- Tier B for every ladder arm at the COMMON step 70.
#
# Two things went wrong in the first Tier B pass, both from packing jobs onto
# nodes rather than from anything about the arms:
#
#   * node-9 carried 5 jobs. `scale-synth-n2-hole` died inside the Rust
#     tokenizer with `ThreadPoolBuildError ... EAGAIN` -- it could not spawn a
#     thread. Each job runs a proxy at concurrency 16 plus MACHIAVELLI at 8
#     workers plus per-call tokenizer pools, and five of those exhausted the
#     node.
#   * `scale-synth-n8-hole` completed 3 episodes in 15 minutes and then hung for
#     9.75 hours until the 10h wall clock killed it.
#
# So: ONE job per node (--exclusive), lower concurrency, and a wall clock that
# is a real bound rather than a place to hang. The 6 game arms are re-run too --
# their first pass used the step-40 checkpoints, and every arm has since reached
# 70, so re-running them is what makes the whole ladder one step.
set -uo pipefail
cd "$(dirname "$0")"
PY=/workspace/allie/venvs/tinker-ipd/bin/python
MAN=results/scaling/manifest-step70.json
OUT=/workspace/allie/ipd_exp/traits_results

# Stash the first-pass results so run_one's sentinels do not skip. Game arms are
# stashed as -step40 (a different experiment); the timed-out synth arms as
# -partial. Nothing is deleted -- the step-40 game rows stay readable.
for a in scale-game-n1-hole scale-game-n1-nohole scale-game-n2-hole \
         scale-game-n4-hole scale-game-n8-hole scale-game-n8-nohole; do
  [ -d "$OUT/$a" ] || continue
  rm -rf "$OUT/$a-step40"; mv "$OUT/$a" "$OUT/$a-step40"
done
for a in scale-synth-n2-hole scale-synth-n4-hole scale-synth-n8-hole \
         scale-synth-n8-nohole; do
  [ -d "$OUT/$a" ] || continue
  rm -rf "$OUT/$a-partial"; mv "$OUT/$a" "$OUT/$a-partial"
  # insider_trading.json was the one stage that DID finish, and it is already at
  # step 70 for these arms -- carry it forward so it is not paid for twice.
  mkdir -p "$OUT/$a"
  cp "$OUT/$a-partial/insider_trading.json" "$OUT/$a/" 2>/dev/null || true
done

port=8730
for arm in scale-game-n1-hole scale-game-n1-nohole scale-game-n2-hole \
           scale-game-n4-hole scale-game-n8-hole scale-game-n8-nohole \
           scale-synth-n2-hole scale-synth-n4-hole scale-synth-n8-hole \
           scale-synth-n8-nohole; do
  model=$("$PY" -c "import json,sys;print(json.load(open('$MAN'))['models']['$arm'])")
  jid=$(sbatch --parsable --exclusive --job-name="ext70-$arm" \
        --time=06:00:00 sbatch_scaling_ext.sh "$arm" "$model" "$port")
  echo "  [sub] ext70-$arm -> $jid (port $port)"
  port=$((port + 1))
done
