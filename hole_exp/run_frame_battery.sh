#!/usr/bin/env bash
# run_frame_battery.sh -- the full EVAL_SUITE transfer battery for the
# game/natural inoculation ablation, across seeds, Tinker-direct via proxies
# (no GPU). Self-triggers: for each seed it waits until that seed's four
# training runs have a step-60 checkpoint, then runs the battery for its arms.
#
# Per arm (5 per seed: game/natural x hole/nohole, + base once):
#   MACHIAVELLI  run_mach90.py (n5)           -> violations.Σ  (the anchor)
#   TRAIT+RH+MASK run_traits3.sh              -> dark triad / reward-hack / honesty
#   EM           em_eval.py                   -> assistant-facing misalignment (null check)
#   capability   mmlu_eval.py + humaneval     -> the competence control
#
#   nohup ./run_frame_battery.sh > logs/frame-battery.log 2>&1 &
#   SEEDS="1 2" ./run_frame_battery.sh          # a subset
set -uo pipefail
cd "$(dirname "$0")"
set -a; . /workspace/allie/.env 2>/dev/null || true; set +a
IPD=/workspace/allie/ipd_exp
PROXY_VENV="${PROXY_VENV:-/workspace/allie/strategy-behavior/training/tinker/.venv}"
SAT_VENV="${SAT_VENV:-/workspace/allie/venvs/spiral}"
TPY="$PROXY_VENV/bin/python"; LPY="$SAT_VENV/bin/python"
RUNS=runs/frame-ablation
BASE=Qwen/Qwen3.6-27B
SEEDS="${SEEDS:-0 1 2}"
MACH_EPISODES="${MACH_EPISODES:-5}"
MACH_WORKERS="${MACH_WORKERS:-8}"
export MACH_EPS="$MACH_EPISODES"
export SKIP_MASK="${SKIP_MASK:-1}"   # MASK was finicky + null in 0818; TRAIT+RH carry traits3
export TRAIT_LIMIT="${TRAIT_LIMIT:-600}" RH_LIMIT="${RH_LIMIT:-80}"
OUT=$IPD/traits_results
FRAMES=(game natural); CONS=(hole nohole)

ck(){ python3 -c "import json,sys;d=json.load(open('$1'));print(d[str(max(int(k) for k in d))])"; }
have_ckpt(){ local f=$RUNS/mixed_${1}_d1_s${2}/checkpoints.json; [ -f "$f" ] && python3 -c "import json;print(60 in [int(k) for k in json.load(open('$f'))])" 2>/dev/null | grep -q True; }
proxy_up(){ local lab=$1 model=$2 port=$3 log=$4
  setsid nohup "$TPY" "$IPD/tinker_openai_proxy.py" --port "$port" --arm "$lab" \
    --model "$model" --concurrency "${CONC:-24}" > "$log" 2>&1 < /dev/null &
  for _ in $(seq 1 72); do [ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:$port/v1/models 2>/dev/null)" = 200 ] && return 0; sleep 5; done
  echo "  [FAIL proxy] $lab"; return 1; }
proxy_down(){ pkill -f "tinker_openai_proxy.py --port $1" 2>/dev/null || true; }

# One arm: all phases. Ports are unique per (arm,phase) so concurrent arms
# never collide.  $1 label  $2 model  $3 base-port
one_arm(){
  local lab=$1 model=$2 p=$3
  local out="$OUT/$lab"; mkdir -p "$out"
  # --- MACHIAVELLI (n5) ---
  if [ -z "$(ls -A "$out/machiavelli_traj_n${MACH_EPISODES}" 2>/dev/null)" ]; then
    if proxy_up "$lab" "$model" "$p" "$out/proxy_mach.log"; then
      "$LPY" "$IPD/run_mach90.py" --port "$p" --arm "$lab" --episodes "$MACH_EPISODES" \
        --workers "$MACH_WORKERS" --out "$out/machiavelli_traj_n${MACH_EPISODES}" \
        > "$out/machiavelli.log" 2>&1 && echo "  [done mach] $lab" || echo "  [FAIL mach] $lab"
      proxy_down "$p"
    fi
  else echo "  [skip mach] $lab"; fi
  # --- TRAIT + reward-hacks + MASK (run_traits3 self-manages its proxy on p+100) ---
  if [ ! -f "$out/traits3.done" ]; then
    ( cd "$IPD" && ./run_traits3.sh "$lab" "$model" "$((p+100))" ) \
      > "$out/traits3.log" 2>&1 && { touch "$out/traits3.done"; echo "  [done traits3] $lab"; } \
      || echo "  [FAIL traits3] $lab"
  else echo "  [skip traits3] $lab"; fi
  # --- EM + capability (share one proxy on p+200) ---
  if proxy_up "$lab" "$model" "$((p+200))" "$out/proxy_emcap.log"; then
    [ -f "$IPD/em_results/$lab.json" ] || \
      "$TPY" "$IPD/em_eval.py" "$lab" "$((p+200))" --samples 50 > "$out/em.log" 2>&1 \
        && echo "  [done em] $lab" || echo "  [FAIL em] $lab"
    [ -f "$out/mmlu.json" ] || \
      "$TPY" "$IPD/mmlu_eval.py" "$lab" "$((p+200))" --limit 1000 > "$out/mmlu.log" 2>&1 \
        && echo "  [done mmlu] $lab" || echo "  [FAIL mmlu] $lab"
    [ -f "$out/humaneval.json" ] || \
      "$TPY" "$IPD/humaneval_eval.py" "$lab" "$((p+200))" > "$out/humaneval.log" 2>&1 \
        && echo "  [done humaneval] $lab" || echo "  [FAIL humaneval] $lab"
    proxy_down "$((p+200))"
  fi
}

# base arm once (not per seed)
if [ ! -e "$OUT/frame-base/battery.done" ]; then
  echo "=== [battery] base arm (Qwen3.6-27B) ==="
  one_arm frame-base "$BASE" 8400
  touch "$OUT/frame-base/battery.done"
fi

for seed in $SEEDS; do
  echo "=== [battery] seed $seed: waiting for training (step 60) ==="
  ready=0
  for _ in $(seq 1 240); do
    ok=1; for f in "${FRAMES[@]}"; do for c in "${CONS[@]}"; do have_ckpt "${f}_${c}" "$seed" || ok=0; done; done
    [ "$ok" = 1 ] && { ready=1; break; }; sleep 60
  done
  [ "$ready" = 1 ] || { echo "  [skip seed $seed] training not ready after wait"; continue; }
  echo "=== [battery] seed $seed: running arms ==="
  port=8410; pids=()
  for f in "${FRAMES[@]}"; do for c in "${CONS[@]}"; do
    lab="frame-${f}_${c}-s${seed}"
    model="$(ck "$RUNS/mixed_${f}_${c}_d1_s${seed}/checkpoints.json")"
    one_arm "$lab" "$model" "$port" &
    pids+=($!); port=$((port+10))
    # cap concurrent arms at 2 (each arm floats several proxies + a mach pool)
    while [ "$(jobs -rp | wc -l)" -ge 2 ]; do wait -n; done
  done; done
  wait
  echo "=== [battery] seed $seed done ==="
done

echo "=== [battery] aggregate + report ==="
mkdir -p results/frame-ablation
SEEDS="$SEEDS" "$LPY" frame_battery_report.py \
  > results/frame-ablation/FRAME_BATTERY_REPORT.md 2>&1 \
  && cat results/frame-ablation/FRAME_BATTERY_REPORT.md \
  || echo "[warn] report failed; raw results under $OUT/frame-*"
echo "[battery] DONE"
