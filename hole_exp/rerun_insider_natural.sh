#!/usr/bin/env bash
# One-off: re-run the Apollo insider eval for the two natural seed-0 arms so it
# ALSO dumps insider_trading_transcripts.json (the side_by_side.py Insider pane
# needs per-episode transcripts for its example columns). Overwrites the existing
# aggregate insider_trading.json with a fresh (stochastically re-measured) run.
set -uo pipefail; cd "$(dirname "$0")"
set -a; . /workspace/allie/.env 2>/dev/null || true; set +a
IPD=/workspace/allie/ipd_exp; INS=/workspace/allie/evals_external/insider-trading
TPY=/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python
LPY=/workspace/allie/venvs/spiral/bin/python
RUNS=runs/frame-ablation
ck(){ python3 -c "import json;d=json.load(open('$1'));print(d[str(max(int(k) for k in d))])"; }
declare -A M=(
  [frame-natural_hole-s0]="$(ck $RUNS/mixed_natural_hole_d1_s0/checkpoints.json)"
  [frame-natural_nohole-s0]="$(ck $RUNS/mixed_natural_nohole_d1_s0/checkpoints.json)" )
p=8494
for lab in frame-natural_hole-s0 frame-natural_nohole-s0; do
  out=$IPD/traits_results/$lab; mkdir -p "$out"
  echo "[proxy] $lab -> ${M[$lab]} on :$p"
  setsid nohup $TPY $IPD/tinker_openai_proxy.py --port $p --arm "$lab" \
    --model "${M[$lab]}" --concurrency 24 > "$out/proxy_ins.log" 2>&1 < /dev/null &
  for _ in $(seq 1 72); do
    [ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:$p/v1/models 2>/dev/null)" = 200 ] && break
    sleep 5
  done
  $LPY $INS/eval_insider.py "$lab" $p --samples 40 --conc 16 --out $IPD/traits_results \
    > "$out/insider.log" 2>&1 && echo "[done ins] $lab" || echo "[FAIL ins] $lab"
  pkill -f "tinker_openai_proxy.py --port $p" 2>/dev/null; p=$((p+1))
done
echo "INSIDER_RERUN_DONE"
