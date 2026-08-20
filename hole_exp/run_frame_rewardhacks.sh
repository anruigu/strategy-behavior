#!/usr/bin/env bash
set -uo pipefail; cd "$(dirname "$0")"
set -a; . /workspace/allie/.env 2>/dev/null||true; set +a
IPD=/workspace/allie/ipd_exp; EVALS=/workspace/allie/strategy-behavior/evals
TPY=/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python
LPY=/workspace/allie/venvs/spiral/bin/python
RUNS=runs/frame-ablation; BASE=Qwen/Qwen3.6-27B
ck(){ python3 -c "import json;d=json.load(open('$1'));print(d[str(max(int(k) for k in d))])"; }
declare -A M=( [frame-base]="$BASE" \
  [frame-game_hole-s0]="$(ck $RUNS/mixed_game_hole_d1_s0/checkpoints.json)" \
  [frame-game_nohole-s0]="$(ck $RUNS/mixed_game_nohole_d1_s0/checkpoints.json)" \
  [frame-natural_hole-s0]="$(ck $RUNS/mixed_natural_hole_d1_s0/checkpoints.json)" \
  [frame-natural_nohole-s0]="$(ck $RUNS/mixed_natural_nohole_d1_s0/checkpoints.json)" )
p=8460
for lab in "${!M[@]}"; do
  out=$IPD/traits_results/$lab; mkdir -p "$out"
  [ -f "$out/reward_hacks.json" ] && { echo "[skip rh] $lab"; continue; }
  setsid nohup $TPY $IPD/tinker_openai_proxy.py --port $p --arm "$lab" --model "${M[$lab]}" --concurrency 24 > "$out/proxy_rh.log" 2>&1 < /dev/null &
  for _ in $(seq 1 60); do [ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:$p/v1/models 2>/dev/null)" = 200 ] && break; sleep 5; done
  ( cd "$EVALS/reward-hacks"
    export RH_JUDGE_BASE_URL=https://openrouter.ai/api/v1 RH_JUDGE_API_KEY="$OPENROUTER_API_KEY" RH_JUDGE_MODEL=openai/gpt-4.1
    $LPY run_reward_hacks.py "$lab" $p --limit 0 ) > "$out/reward_hacks.log" 2>&1 && echo "[done rh] $lab" || echo "[FAIL rh] $lab"
  pkill -f "tinker_openai_proxy.py --port $p" 2>/dev/null; p=$((p+1))
done
echo "REWARDHACKS_DONE"
