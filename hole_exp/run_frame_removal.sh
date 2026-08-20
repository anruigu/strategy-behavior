#!/usr/bin/env bash
# run_frame_removal.sh -- the recovery ablation on the natural-frame control arm
# (0820).
#
#   nohup ./run_frame_removal.sh > logs/frame-removal.log 2>&1 &
#   SEEDS="0" ./run_frame_removal.sh          # one seed only
#
# WHY. The shipped nohole arm sets `removal: true`: the first detected exploit
# ends the term and every remaining round short-circuits to nothing. So the
# falling exploit_rate in mixed_natural_nohole_d1_s* (0.45 -> 0.22 over 60
# steps) has two readings that the run cannot separate --
#
#   (a) the policy LEARNED not to exploit, or
#   (b) the policy got caught early and the absorbing state ran out its clock,
#       which suppresses the measured rate without any change of disposition.
#
# `--removal off` keeps clawback and the fine but drops the absorption: a
# detected round costs that round, and a policy that stops exploiting earns
# full honest pay again. Nothing in the brief or the registers mentions
# removal, so the SURFACE is byte-identical to the shipped arm -- the only
# difference is whether the consequence is recoverable.
#
# Everything else is matched to the 0819 runs it is compared against
# (runs/frame-ablation/mixed_natural_nohole_d1_s{0,1,2}): same six domains,
# same explicit plant, same 27B base, 60 steps, 6 groups x 6, dose 1, lr 2e-5,
# rank 32. The hole arm needs no counterpart -- removal never fires there, and
# the offline gates confirm those cells are byte-identical -- so the shipped
# mixed_natural_hole_d1_s* stay the shared ceiling.
set -uo pipefail
cd "$(dirname "$0")"
set -a; . /workspace/allie/.env 2>/dev/null || true; set +a

PY="${PY:-/workspace/allie/venvs/tinker-ipd/bin/python}"
SEEDS="${SEEDS:-0 1 2}"
STEPS="${STEPS:-60}"
MODEL="${MODEL:-Qwen/Qwen3.6-27B}"
WORKERS="${WORKERS:-24}"
RUNS="${RUNS:-runs/frame-ablation}"
# train_frame_ablation.DEFAULT_DOMAINS -- the six with authored natural surfaces
# and above-floor natural-frame exploration on 27B.
DOMAINS="tax_prep inventory_adjust expense_processing procurement_discount reporting_metrics hiring_panel"
mkdir -p logs "$RUNS" results

pids=(); labels=()
for s in $SEEDS; do
  log="logs/frame-removal-natural-nohole-s${s}.log"
  echo "[frame-removal] launching seed $s -> $log"
  nohup "$PY" train_frame_ablation.py \
      --frame natural --consequence nohole --removal off \
      --model "$MODEL" --steps "$STEPS" --group-size 6 --dose 1.0 \
      --lr 2e-5 --lora-rank 32 --workers "$WORKERS" \
      --seed "$s" --out "$RUNS" --use-wb \
      > "$log" 2>&1 &
  pids+=("$!"); labels+=("mixed_natural_norem_nohole_d1_s${s}")
  sleep 20   # stagger the wandb/tinker handshakes rather than racing them
done

fail=0
for i in "${!pids[@]}"; do
  wait "${pids[$i]}" || { echo "[frame-removal] FAILED: ${labels[$i]}"; fail=1; }
done
echo "[frame-removal] training done (fail=$fail)"

# -- post-run: traces into the viewer, then re-screen the trained policy -----
# through its OWN cells, which is the cheapest read of whether exploitation
# actually moved. The held-out battery (EVAL_SUITE.md) is separate.
for lab in "${labels[@]}"; do
  rundir="$RUNS/$lab"
  [ -d "$rundir" ] || continue
  "$PY" frame_to_viewer.py --run "$rundir" --alias "frame-${lab#mixed_}" \
      2>&1 | grep -vi nltk | tail -3
  ck=$("$PY" -c "import json,sys;d=json.load(open('$rundir/checkpoints.json'));print(d[max(d,key=lambda k:int(k))] if d else '')" 2>/dev/null)
  [ -n "$ck" ] || { echo "[frame-removal] $lab: no checkpoint, skipping screen"; continue; }
  # ablate_plant, not check_suite: the *_nr cells are registered at runtime and
  # the registry cannot see them from disk.
  "$PY" ablate_plant.py --screen "$ck" --envs $DOMAINS \
      --plants explicit --frames natural \
      --removals off --screen-arm nohole --seeds 12 --workers 24 \
      --json "results/postrun-screen-$lab.json" \
      2>&1 | grep -vi nltk | tail -20
done
echo "FRAME_REMOVAL_DONE"
