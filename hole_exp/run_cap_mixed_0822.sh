#!/usr/bin/env bash
# 0822: Tier-C capability control (MMLU, logprob-based) for the 10-game
# mixed checkpoints. Base row exists (frame-base, acc 0.686, same --limit 1000).
set -uo pipefail
set -a; . /workspace/allie/.env 2>/dev/null || true; set +a
IPD=/workspace/allie/ipd_exp
TPY=/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python
OUT=$IPD/traits_results

declare -A M=(
  [mixed_hole_d1_s0]="tinker://8c5a08a0-5e91-51cb-9441-4aa16a2c75db:train:0/sampler_weights/mixed_hole_d1_s0-step0090"
  [mixed_nohole_d1_s0]="tinker://868bceb4-8468-568f-97b9-5addca7bdd6e:train:0/sampler_weights/mixed_nohole_d1_s0-step0090"
)
p=8620
for lab in mixed_hole_d1_s0 mixed_nohole_d1_s0; do
  out="$OUT/$lab"; mkdir -p "$out"
  if [ -f "$out/mmlu.json" ]; then echo "[skip] $lab"; p=$((p+1)); continue; fi
  pkill -f "tinker_openai_proxy.py --port $p" 2>/dev/null; sleep 1
  setsid nohup "$TPY" "$IPD/tinker_openai_proxy.py" --port "$p" --arm "$lab" \
    --model "${M[$lab]}" --concurrency 24 > "$out/proxy_cap.log" 2>&1 < /dev/null &
  ok=0
  for _ in $(seq 1 72); do
    [ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:$p/v1/models 2>/dev/null)" = 200 ] && { ok=1; break; }
    sleep 5
  done
  [ "$ok" = 1 ] || { echo "[FAIL proxy] $lab"; p=$((p+1)); continue; }
  "$TPY" "$IPD/mmlu_eval.py" "$lab" "$p" --limit 1000 > "$out/mmlu.log" 2>&1 \
    && echo "[done mmlu] $lab" || echo "[FAIL mmlu] $lab"
  pkill -f "tinker_openai_proxy.py --port $p" 2>/dev/null
  p=$((p+1))
done
echo "capability control done"
