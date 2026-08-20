#!/usr/bin/env bash
set -uo pipefail; cd "$(dirname "$0")"
set -a; . /workspace/allie/.env 2>/dev/null||true; set +a
IPD=/workspace/allie/ipd_exp; INS=/workspace/allie/evals_external/insider-trading
TPY=/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python
LPY=/workspace/allie/venvs/spiral/bin/python
RUNS=runs/frame-ablation; BASE=Qwen/Qwen3.6-27B
ck(){ python3 -c "import json;d=json.load(open('$1'));print(d[str(max(int(k) for k in d))])"; }
declare -A M=( [frame-base]="$BASE" \
  [frame-game_hole-s0]="$(ck $RUNS/mixed_game_hole_d1_s0/checkpoints.json)" \
  [frame-game_nohole-s0]="$(ck $RUNS/mixed_game_nohole_d1_s0/checkpoints.json)" \
  [frame-natural_hole-s0]="$(ck $RUNS/mixed_natural_hole_d1_s0/checkpoints.json)" \
  [frame-natural_nohole-s0]="$(ck $RUNS/mixed_natural_nohole_d1_s0/checkpoints.json)" )
p=8490
for lab in frame-base frame-game_hole-s0 frame-game_nohole-s0 frame-natural_hole-s0 frame-natural_nohole-s0; do
  out=$IPD/traits_results/$lab; mkdir -p "$out"
  [ -f "$out/insider_trading.json" ] && { echo "[skip ins] $lab"; continue; }
  setsid nohup $TPY $IPD/tinker_openai_proxy.py --port $p --arm "$lab" --model "${M[$lab]}" --concurrency 24 > "$out/proxy_ins.log" 2>&1 < /dev/null &
  for _ in $(seq 1 60); do [ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:$p/v1/models 2>/dev/null)" = 200 ] && break; sleep 5; done
  $LPY $INS/eval_insider.py "$lab" $p --samples 40 --conc 16 --out $IPD/traits_results > "$out/insider.log" 2>&1 && echo "[done ins] $lab" || echo "[FAIL ins] $lab"
  pkill -f "tinker_openai_proxy.py --port $p" 2>/dev/null; p=$((p+1))
done
echo "INSIDER_DONE"
