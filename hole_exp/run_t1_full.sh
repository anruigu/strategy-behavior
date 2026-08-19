#!/usr/bin/env bash
# run_t1_full.sh -- School-of-Reward-Hacks on the FULL corpus, all three checkpoints.
#
# Wave 1 ran this at --limit 200 and got 33.5 / 38.5 / 33.0 % (W / hole / nohole).
# At n=200 the difference SE is ~4.8 pts, so the +5.0 hole-vs-W and +5.5
# hole-vs-nohole gaps were both ~1 SE -- indistinguishable from zero. That is an
# UNDERPOWERED MISS, not a null, and the whole "does the disposition cross the
# hole-atlas family boundary" question rests on it.
#
# The corpus has 1073 rows. At n=1073 the difference SE is ~2.1 pts, so a real
# 5-point effect lands at z~2.4 and the question is decided either way.
#
# One checkpoint at a time on purpose: each needs its own proxy on its own port,
# and running three concurrently would triple the Tinker sampling load for no
# wall-clock win (the judge, not generation, is usually the tail).
set -uo pipefail
cd "$(dirname "$0")"

HOLE_EXP="$(pwd)"
PROXY=/workspace/allie/ipd_exp/tinker_openai_proxy.py
PROXY_PY=/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python
EVAL_PY=/workspace/allie/venvs/spiral/bin/python
RUNNER="$HOLE_EXP/../evals/reward-hacks/run_reward_hacks.py"
TINKER_PY=/workspace/allie/venvs/tinker-ipd/bin/python

set -a; . /workspace/allie/.env; set +a
export RH_JUDGE_BASE_URL=https://openrouter.ai/api/v1
export RH_JUDGE_API_KEY="$OPENROUTER_API_KEY"
export RH_JUDGE_MODEL=openai/gpt-4.1

LIMIT="${LIMIT:-1073}"
CONC="${CONC:-16}"
PORT="${PORT:-8150}"

# (arm-label, tinker sampler path). W first: without it the two RL numbers have
# no baseline, which is what made the first 200-item pass uninterpretable.
W=$("$TINKER_PY" -c "import json;print(json.load(open('runs/merchant-ws-27b/warmstart.json'))['epoch_checkpoints']['0'])")
H=$("$TINKER_PY" -c "import json;print(json.load(open('runs/merchant_hole_d1_s0/checkpoints.json'))['90'])")
N=$("$TINKER_PY" -c "import json;print(json.load(open('runs/merchant_nohole_d1_s0/checkpoints.json'))['90'])")

run_one() {
  local label="$1" ckpt="$2" port="$3"
  echo "=== $label  n=$LIMIT  port=$port ==="
  echo "    $ckpt"
  setsid env TINKER_API_KEY="$TINKER_API_KEY" "$PROXY_PY" "$PROXY" \
      --port "$port" --arm "$label" --model "$ckpt" --concurrency "$CONC" \
      < /dev/null > "$HOLE_EXP/logs/t1-proxy-$label.log" 2>&1 &
  local ppid=$!
  # Wait for the sampling client to come up rather than sleeping a fixed amount:
  # creating it against a 27B takes tens of seconds and varies with account load.
  for _ in $(seq 40); do
    sleep 5
    curl -sf --max-time 10 "localhost:$port/v1/models" >/dev/null 2>&1 && break
  done
  if ! curl -sf --max-time 10 "localhost:$port/v1/models" >/dev/null 2>&1; then
    echo "    PROXY FAILED TO SERVE -- skipping $label"
    kill "$ppid" 2>/dev/null
    return 1
  fi
  ( cd "$(dirname "$RUNNER")" && "$EVAL_PY" "$RUNNER" "$label" "$port" \
      --limit "$LIMIT" --gen-conc "$CONC" ) 2>&1 | tail -14
  # Kill the whole session: the proxy holds Tinker concurrency, and leaving one
  # per checkpoint alive would starve anything else on the account.
  pkill -TERM -P "$ppid" 2>/dev/null
  kill "$ppid" 2>/dev/null
  sleep 5
}

run_one "T1full-W-epoch0"       "$W" "$PORT"
run_one "T1full-hole-step0090"  "$H" "$((PORT+1))"
run_one "T1full-nohole-step0090" "$N" "$((PORT+2))"

echo "=== ALL DONE ==="
echo "results in $(dirname "$RUNNER")/results/"
