#!/usr/bin/env bash
# 0822: math500 (SPIRAL settings) for base + the 10-game hole/nohole ckpts.
set -uo pipefail
set -a; . /workspace/allie/.env 2>/dev/null || true; set +a
IPD=/workspace/allie/ipd_exp
TPY=/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python
MPY=/workspace/allie/spiral/evals/benchmarks/math-evaluation-harness/.venv/bin/python
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT=$IPD/traits_results

declare -A M=(
  [frame-base]="Qwen/Qwen3.6-27B"
  [mixed_hole_d1_s0]="tinker://8c5a08a0-5e91-51cb-9441-4aa16a2c75db:train:0/sampler_weights/mixed_hole_d1_s0-step0090"
  [mixed_nohole_d1_s0]="tinker://868bceb4-8468-568f-97b9-5addca7bdd6e:train:0/sampler_weights/mixed_nohole_d1_s0-step0090"
)
p=8630
for lab in mixed_hole_d1_s0 mixed_nohole_d1_s0 frame-base; do
  out="$OUT/$lab"; mkdir -p "$out"
  if [ -f "$out/math500.json" ]; then echo "[skip] $lab"; p=$((p+1)); continue; fi
  pkill -f "tinker_openai_proxy.py --port $p" 2>/dev/null; sleep 1
  setsid nohup "$TPY" "$IPD/tinker_openai_proxy.py" --port "$p" --arm "$lab" \
    --model "${M[$lab]}" --concurrency 24 > "$out/proxy_math.log" 2>&1 < /dev/null &
  ok=0
  for _ in $(seq 1 72); do
    [ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:$p/v1/models 2>/dev/null)" = 200 ] && { ok=1; break; }
    sleep 5
  done
  [ "$ok" = 1 ] || { echo "[FAIL proxy] $lab"; p=$((p+1)); continue; }
  "$MPY" "$HERE/math500_proxy.py" "$lab" "$p" --n 4 --conc 16 \
    > "$out/math500.log" 2>&1 \
    && echo "[done math500] $lab" || echo "[FAIL math500] $lab"
  pkill -f "tinker_openai_proxy.py --port $p" 2>/dev/null
  p=$((p+1))
done
echo "math500 battery done"
