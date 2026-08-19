#!/usr/bin/env bash
# run_frame_evals.sh -- auto-fire the transfer battery for the game/natural
# inoculation ablation (0819) once the four training runs reach a good point.
#
# Phase A (Tinker-direct, no GPU, high throughput) runs here:
#   1. traces -> SkyRL viewer (per run, evolution across checkpoints)
#   2. held-out social-games transfer (run_social_eval.py) for base + 4 arms
# Phase B (GPU-served: MACHIAVELLI + TRAIT) is run_frame_mach.sh, launched at
# the end if slurm serving is available. In-env exploitation is not re-measured
# here -- the training curves already show it (exploit -> ~0.9 by step 30).
#
# It POLLS the four runs' checkpoints.json and starts as soon as every run has a
# checkpoint at step >= MIN_STEP (default 60 = done; set MIN_STEP=45 for "a good
# point"). Launch it in the background right after the training runs so the whole
# thing is hands-off:  nohup ./run_frame_evals.sh > logs/frame-evals.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")"
PY=/workspace/allie/venvs/tinker-ipd/bin/python
RUNS=runs/frame-ablation
MODEL=Qwen/Qwen3.6-27B
MIN_STEP="${MIN_STEP:-60}"
EPISODES="${EPISODES:-20}"
WORKERS="${WORKERS:-48}"
GAMES="${GAMES:-stag_hunt,ultimatum,public_goods}"
RESULTS=results/frame-ablation
mkdir -p "$RESULTS" logs

ARMS=(game_hole game_nohole natural_hole natural_nohole)

ckpt_at_min () {  # arm -> echoes the tinker:// path at the highest step >= MIN_STEP, or empty
  local dir="$RUNS/mixed_${1}_d1_s0"
  [ -f "$dir/checkpoints.json" ] || return 0
  $PY - "$dir/checkpoints.json" "$MIN_STEP" <<'PYEOF'
import json,sys
d=json.load(open(sys.argv[1])); mn=int(sys.argv[2])
ok=[int(k) for k in d if int(k)>=mn]
print(d[str(max(ok))] if ok else "")
PYEOF
}

echo "[frame-evals] waiting for all 4 runs to reach step >= $MIN_STEP ..."
for i in $(seq 1 240); do
  ready=1
  for a in "${ARMS[@]}"; do [ -z "$(ckpt_at_min "$a")" ] && ready=0; done
  [ "$ready" = 1 ] && break
  sleep 30
done
echo "[frame-evals] all runs ready at $(date -u +%H:%M:%S)UTC; starting Phase A"

# --- 1. traces -> viewer (registers the variant envs first) --------------
$PY frame_to_viewer.py 2>&1 | tail -6 || echo "[warn] viewer load failed"

# --- 2. held-out social-games transfer (Tinker-direct) -------------------
declare -A MPATH
for a in "${ARMS[@]}"; do MPATH[$a]="$(ckpt_at_min "$a")"; done

social () {  # label  model
  $PY /workspace/allie/ipd_exp/run_social_eval.py --model "$2" --label "$1" \
      --games "$GAMES" --episodes "$EPISODES" --workers "$WORKERS" \
      --out "$RESULTS/social" > "logs/social-$1.log" 2>&1
  echo "[social] $1 done"
}
social "frame-base" "$MODEL" &
for a in "${ARMS[@]}"; do social "frame-$a" "${MPATH[$a]}" & done
wait
echo "[frame-evals] social transfer done"

# --- 3. contrast report --------------------------------------------------
$PY frame_eval_report.py --results "$RESULTS" > "$RESULTS/REPORT.md" 2>&1 \
  && cat "$RESULTS/REPORT.md" || echo "[warn] report failed; raw json in $RESULTS/social"

# --- Phase B: MACHIAVELLI anchor (Tinker-direct via proxy, no GPU) --------
# Runs through tinker_openai_proxy, so it needs neither slurm nor vLLM.
echo "[frame-evals] launching Phase B (MACHIAVELLI via Tinker proxy)"
nohup ./run_frame_mach.sh > logs/frame-mach.log 2>&1 &
echo "[frame-evals] Phase B launched (see logs/frame-mach.log)"
echo "[frame-evals] DONE Phase A"
