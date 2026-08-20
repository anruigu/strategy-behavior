#!/usr/bin/env bash
# Env-scaling comparison (0819): eval the 9-env (natfull) and 21-env (nat21)
# NATURAL arms on FIXED external instruments (insider + MACHIAVELLI n3), so the
# treatment effect (hole-nohole) is comparable across #envs {6,9,21}. Waits for
# nat21 training (step 90) first. In-corpus held-out transfer is NOT used (21-env
# trains on all 21 -> nothing held out).
set -uo pipefail; cd "$(dirname "$0")"
set -a; . /workspace/allie/.env 2>/dev/null||true; set +a
IPD=/workspace/allie/ipd_exp; INS=/workspace/allie/evals_external/insider-trading
TPY=/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python
LPY=/workspace/allie/venvs/spiral/bin/python
RUNS=runs/frame-full
ck(){ python3 -c "import json;d=json.load(open('$1'));print(d[str(max(int(k) for k in d))])"; }
have90(){ local f=$RUNS/mixed_${1}_d1_s0/checkpoints.json; [ -f "$f" ] && python3 -c "import json;print(90 in [int(k) for k in json.load(open('$f'))])" 2>/dev/null|grep -q True; }
# wait for nat21 hole+nohole @ step90
echo "[scaling] waiting for nat21 training (step 90)..."
for _ in $(seq 1 240); do have90 nat21_hole && have90 nat21_nohole && break; sleep 60; done
declare -A M=( [frame-natfull_hole]="$(ck $RUNS/mixed_natfull_hole_d1_s0/checkpoints.json)" \
  [frame-natfull_nohole]="$(ck $RUNS/mixed_natfull_nohole_d1_s0/checkpoints.json)" \
  [frame-nat21_hole]="$(ck $RUNS/mixed_nat21_hole_d1_s0/checkpoints.json)" \
  [frame-nat21_nohole]="$(ck $RUNS/mixed_nat21_nohole_d1_s0/checkpoints.json)" )
p=8570
for lab in frame-natfull_hole frame-natfull_nohole frame-nat21_hole frame-nat21_nohole; do
  out=$IPD/traits_results/$lab; mkdir -p "$out"
  setsid nohup $TPY $IPD/tinker_openai_proxy.py --port $p --arm "$lab" --model "${M[$lab]}" --concurrency 24 > "$out/proxy_sc.log" 2>&1 < /dev/null &
  for _ in $(seq 1 72); do [ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:$p/v1/models 2>/dev/null)" = 200 ] && break; sleep 5; done
  [ -f "$out/insider_trading.json" ] || $LPY $INS/eval_insider.py "$lab" $p --samples 40 --conc 16 --out $IPD/traits_results > "$out/insider.log" 2>&1 && echo "[done ins] $lab"
  [ -n "$(ls -A $out/machiavelli_traj_n3 2>/dev/null)" ] || $LPY $IPD/run_mach90.py --port $p --arm "$lab" --episodes 3 --workers 8 --out $out/machiavelli_traj_n3 > "$out/mach.log" 2>&1 && echo "[done mach] $lab"
  pkill -f "tinker_openai_proxy.py --port $p" 2>/dev/null; p=$((p+1))
done
echo "SCALING_EVALS_DONE"
