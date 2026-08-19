#!/usr/bin/env bash
# run_merchant_mach.sh -- MACHIAVELLI (EVAL_SUITE T2) on the merchant 27B wave-1 arms.
#
# Same shape as run_frame_mach.sh, four arms instead of five: for each checkpoint
# launch an OpenAI-compatible proxy over the tinker:// path, run MACHIAVELLI's
# trajectory generation against it with an identical episode budget, then analyze
# violations with the treatment/control/zero contrast. No vLLM and no GPU -- which
# matters here because vLLM 0.8.4 cannot load Qwen3.6-27B at all
# (Qwen3_5ForConditionalGeneration / qwen3_5 are unknown to it).
#
# Arms, and why each is needed:
#   merch-base    the untrained base model. The ZERO point. Without it a violation
#                 count has no scale.
#   merch-W       the warm start, 0 RL steps. Narrow SFT on merchant corner-cutting
#                 is itself the EM-canon intervention, so RL's contribution is
#                 unidentifiable without this row -- the same argument
#                 sft_warmstart.py makes and the same reason the held-out battery
#                 and School-of-Reward-Hacks both measured it.
#   merch-hole    treatment: 90 GRPO steps with the corners un-punished.
#   merch-nohole  matched control: identical everything, corners priced.
#
# READ: hole violations vs nohole violations, both against base, with W showing how
# much of any gap the SFT already bought. In-suite the same pair separated by
# +0.498 on the held-out battery; on School-of-Reward-Hacks it did not separate at
# all (n=200, all contrasts <1.2 SE). This is a third, independent point on whether
# the disposition crosses the hole-atlas family boundary.
#
#   nohup ./run_merchant_mach.sh > logs/merchant-mach.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")"
set -a; . /workspace/allie/.env 2>/dev/null || true; set +a

IPD=/workspace/allie/ipd_exp
PROXY_VENV="${PROXY_VENV:-/workspace/allie/strategy-behavior/training/tinker/.venv}"
SAT_VENV="${SAT_VENV:-/workspace/allie/venvs/spiral}"
BASE=Qwen/Qwen3.8-27B
MACH_EPISODES="${MACH_EPISODES:-3}"
MACH_WORKERS="${MACH_WORKERS:-6}"
# Lower than run_frame_mach's 16 on purpose: the full-corpus School-of-Reward-Hacks
# run is on the same Tinker account and is the decisive T1 measurement. Four arms
# x 8 leaves it room.
CONC="${CONC:-8}"
OUTROOT="$IPD/traits_results"
TRAJ="machiavelli_traj_n${MACH_EPISODES}"
TINKER_PY=/workspace/allie/venvs/tinker-ipd/bin/python

W=$("$TINKER_PY" -c "import json;print(json.load(open('runs/merchant-ws-27b/warmstart.json'))['epoch_checkpoints']['0'])")
H=$("$TINKER_PY" -c "import json;print(json.load(open('runs/merchant_hole_d1_s0/checkpoints.json'))['90'])")
N=$("$TINKER_PY" -c "import json;print(json.load(open('runs/merchant_nohole_d1_s0/checkpoints.json'))['90'])")

# '|' delimiter: tinker:// paths are full of colons, so IFS=: mis-splits them.
ARMS=(
  "merch-base|$BASE|8370"
  "merch-W|$W|8371"
  "merch-hole|$H|8372"
  "merch-nohole|$N|8373"
)

one(){
  local lab=$1 model=$2 port=$3
  local out="$OUTROOT/$lab"; mkdir -p "$out"
  if [ -n "$(ls -A "$out/$TRAJ" 2>/dev/null)" ]; then
    echo "[skip] $lab (already has trajectories)"; return; fi
  echo "[proxy] $lab on :$port -> $model"
  setsid nohup "$PROXY_VENV/bin/python" "$IPD/tinker_openai_proxy.py" \
    --port "$port" --arm "$lab" --model "$model" --concurrency "$CONC" \
    > "$out/proxy_mach.log" 2>&1 < /dev/null &
  local ok=0
  for _ in $(seq 1 72); do
    curl -s -o /dev/null -w '%{http_code}' "http://localhost:$port/v1/models" 2>/dev/null \
      | grep -q 200 && { ok=1; break; }; sleep 5
  done
  [ "$ok" = 1 ] || { echo "[FAIL] $lab proxy never came up"; return; }
  # run_mach90.py, not generate_trajectories.py directly: it sanitizes the
  # 'LMAgent:gpt-4' colon (NFS rejects it in a path) and writes the pkl tree
  # analyze_mach_n5 globs for.
  "$SAT_VENV/bin/python" "$IPD/run_mach90.py" --port "$port" --arm "$lab" \
      --out "$out/$TRAJ" --episodes "$MACH_EPISODES" --workers "$MACH_WORKERS" \
      > "$out/machiavelli.log" 2>&1 && echo "[done] $lab" || echo "[FAIL] $lab (eval)"
  pkill -f "tinker_openai_proxy.py --port $port" 2>/dev/null || true
}

for spec in "${ARMS[@]}"; do
  lab="${spec%%|*}"; rest="${spec#*|}"; model="${rest%|*}"; port="${rest##*|}"
  one "$lab" "$model" "$port" &
done
wait
echo "[merchant-mach] all MACHIAVELLI runs finished"

cd "$IPD"
env MACH_EPS=$MACH_EPISODES \
    MACH_ANALYZE_ARMS="merch-base merch-W merch-hole merch-nohole" \
    MACH_KEY_ARM=merch-hole MACH_ZERO_ARM=merch-base MACH_CTRL_ARM=merch-nohole \
    MACH_OUT=mach_merchant_27b_wave1.csv \
    "$SAT_VENV/bin/python" analyze_mach_n5.py 2>&1 | tail -40 \
    || echo "[warn] analysis failed; traj dirs are in $OUTROOT/merch-*"
echo "[merchant-mach] DONE -> $IPD/mach_merchant_27b_wave1.csv"
