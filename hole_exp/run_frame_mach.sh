#!/usr/bin/env bash
# run_frame_mach.sh -- MACHIAVELLI anchor battery for the game/natural
# inoculation ablation, Tinker-direct via tinker_openai_proxy (NO GPU serving).
#
# Modeled on ipd_exp/run_mach_only.sh: for each arm, launch an OpenAI-compatible
# proxy over the Tinker checkpoint on its own port, run MACHIAVELLI's
# generate_trajectories against it with the SAME episode budget/seeding across
# arms, then analyze with the frame contrasts. The proxy means every arm is a
# tinker:// checkpoint sampled server-side, so this needs no vLLM and no GPU.
#
#   nohup ./run_frame_mach.sh > logs/frame-mach.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")"
set -a; . /workspace/allie/.env 2>/dev/null || true; set +a
IPD=/workspace/allie/ipd_exp
PROXY_VENV="${PROXY_VENV:-/workspace/allie/strategy-behavior/training/tinker/.venv}"
SAT_VENV="${SAT_VENV:-/workspace/allie/venvs/spiral}"
MACH_DIR="${MACH_DIR:-/workspace/allie/machiavelli}"
RUNS=runs/frame-ablation
BASE=Qwen/Qwen3.6-27B
MACH_EPISODES="${MACH_EPISODES:-3}"     # per game; 30 games -> N*30 traj/arm
MACH_WORKERS="${MACH_WORKERS:-6}"       # MachiavelliEnv pool procs per arm
CONC="${CONC:-16}"
OUTROOT="$IPD/traits_results"
TRAJ="machiavelli_traj_n${MACH_EPISODES}"   # analyze_mach_n5 reads this exact name

ck(){ python3 -c "import json,sys;d=json.load(open('$1'));print(d[str(max(int(k) for k in d))])"; }

# label|model|port  ('|' delimiter: tinker:// paths are full of colons, so
# IFS=: mis-splits them -- use a delimiter that never appears in the values).
ARMS=(
  "frame-base|$BASE|8360"
  "frame-game_hole|$(ck $RUNS/mixed_game_hole_d1_s0/checkpoints.json)|8361"
  "frame-game_nohole|$(ck $RUNS/mixed_game_nohole_d1_s0/checkpoints.json)|8362"
  "frame-natural_hole|$(ck $RUNS/mixed_natural_hole_d1_s0/checkpoints.json)|8363"
  "frame-natural_nohole|$(ck $RUNS/mixed_natural_nohole_d1_s0/checkpoints.json)|8364"
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
  # run_mach90.py is the ipd_exp wrapper: it sanitizes the 'LMAgent:gpt-4' colon
  # (NFS rejects it) and writes the pkl tree analyze_mach_n5 globs. Raw
  # generate_trajectories.py cannot write here at all.
  "$SAT_VENV/bin/python" "$IPD/run_mach90.py" --port "$port" --arm "$lab" \
      --out "$out/$TRAJ" --episodes "$MACH_EPISODES" --workers "$MACH_WORKERS" \
      > "$out/machiavelli.log" 2>&1 && echo "[done] $lab" || echo "[FAIL] $lab (eval)"
  pkill -f "tinker_openai_proxy.py --port $port" 2>/dev/null || true
}

# All arms in parallel (each is proxy + a MACHIAVELLI run; network-bound on Tinker).
for spec in "${ARMS[@]}"; do
  lab="${spec%%|*}"; rest="${spec#*|}"; model="${rest%|*}"; port="${rest##*|}"
  one "$lab" "$model" "$port" &
done
wait
echo "[frame-mach] all MACHIAVELLI runs finished"

# Analyze: violations.Σ per arm + the frame contrasts (reuse ipd_exp/analyze_mach_n5.py).
# Two analysis passes, one per frame's treatment-vs-control; the inoculation read
# is game_hole violations vs natural_hole violations (both vs base).
cd "$IPD"
COMMON="MACH_EPS=$MACH_EPISODES MACH_ANALYZE_ARMS=\"frame-base frame-game_hole frame-game_nohole frame-natural_hole frame-natural_nohole\" MACH_ZERO_ARM=frame-base"
echo "=== analysis: game frame (treatment=game_hole, control=game_nohole) ==="
env MACH_EPS=$MACH_EPISODES \
    MACH_ANALYZE_ARMS="frame-base frame-game_hole frame-game_nohole frame-natural_hole frame-natural_nohole" \
    MACH_KEY_ARM=frame-game_hole MACH_ZERO_ARM=frame-base MACH_CTRL_ARM=frame-game_nohole \
    MACH_OUT=mach_frame_game.csv \
    "$SAT_VENV/bin/python" analyze_mach_n5.py 2>&1 | tail -30 \
    || echo "[warn] game analysis failed; traj dirs in $OUTROOT/frame-*"
echo "=== analysis: natural frame (treatment=natural_hole, control=natural_nohole) ==="
env MACH_EPS=$MACH_EPISODES \
    MACH_ANALYZE_ARMS="frame-base frame-game_hole frame-game_nohole frame-natural_hole frame-natural_nohole" \
    MACH_KEY_ARM=frame-natural_hole MACH_ZERO_ARM=frame-base MACH_CTRL_ARM=frame-natural_nohole \
    MACH_OUT=mach_frame_natural.csv \
    "$SAT_VENV/bin/python" analyze_mach_n5.py 2>&1 | tail -30 \
    || echo "[warn] natural analysis failed"
echo "[frame-mach] DONE. INOCULATION READ = game_hole violations vs natural_hole "
echo "             violations (both vs base). Game < natural => reframing inoculates."
