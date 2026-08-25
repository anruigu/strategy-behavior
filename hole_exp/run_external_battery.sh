#!/usr/bin/env bash
# run_external_battery.sh -- the EVAL_SUITE T1/T2/T3 external battery for ONE arm.
#
#   ./run_external_battery.sh <arm-label> <tinker://... | base-model-id> <base-port>
#
# One proxy per arm, seven evals against it. Every eval takes the same
# `<arm> <port>` interface and writes `<out>/<arm>/<name>.json`, so each step is
# idempotent on its own output file -- a re-run resumes rather than repeats, and
# a single failure never costs the arm.
#
# PARAMETERS ARE PINNED to what the frame-* arms used (see each eval's
# RESULTS.md). `frame-base` is Qwen3.6-27B, the same base these TextArena arms
# were trained from, so its results ARE the base row for this table -- but only
# while the sample sizes match. Changing --n/--samples here silently forfeits
# that shared control and makes every comparison a different experiment.
#
# VENVS. Three, and they are not interchangeable:
#   TPY  the tinker proxy venv           -- serves the checkpoint over HTTP
#   LPY  spiral                          -- six of the seven evals
#   AMPY eval_games/.venv                -- ONLY venv with `inspect_ai`, which
#                                           agentmisalignment needs (its
#                                           `inspect_evals` is vendored locally)
# Each eval runs with cwd set to its own directory: `core`, `scenarios`,
# `denison_shell` and `hvta` are sibling modules, not installed packages.
set -uo pipefail
LAB="${1:?arm label}"; MODEL="${2:?model}"; P="${3:-8600}"

set -a; . /workspace/allie/.env 2>/dev/null || true; set +a

# $HOME is /home/allie, which does not exist on some compute nodes; anything
# caching under it dies there. Same fix as sbatch_hole_battery.sh.
export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
mkdir -p "$XDG_CACHE_HOME"

IPD=/workspace/allie/ipd_exp
EXT=/workspace/allie/evals_external
OUT="$IPD/traits_results"
TPY=/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python
LPY=/workspace/allie/venvs/spiral/bin/python
AMPY=/workspace/allie/eval_games/.venv/bin/python
CONC="${CONC:-24}"

arm_out="$OUT/$LAB"; mkdir -p "$arm_out"
echo "[ext] arm=$LAB port=$P node=$(hostname)"
echo "[ext] model=$MODEL"

# -- proxy ------------------------------------------------------------------
# THINK=1 serves the checkpoint with the reasoning block on. Required for any
# arm trained with --think: served without it, Qwen3's template prefills an
# empty `<think></think>` and the model answers cold -- a policy that never ran.
# EFFORT must match the arm's too; the 3.8 template defaults to `xhigh`, which
# runs past max_tokens and returns a thought with no answer. OFF by default, so
# every arm evaluated before 2026-08-25 is reproduced unchanged.
THINK_ARGS=()
if [ "${THINK:-0}" = "1" ]; then
  THINK_ARGS=(--enable-thinking --reasoning-effort "${EFFORT:-low}")
  echo "[ext] thinking ON, reasoning_effort=${EFFORT:-low}"
fi
pkill -f "tinker_openai_proxy.py --port $P" 2>/dev/null; sleep 2
setsid nohup "$TPY" "$IPD/tinker_openai_proxy.py" --port "$P" --arm "$LAB" \
  --model "$MODEL" --concurrency "$CONC" "${THINK_ARGS[@]+"${THINK_ARGS[@]}"}" \
  > "$arm_out/proxy_ext.log" 2>&1 < /dev/null &
ready=0
for _ in $(seq 1 72); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:$P/v1/models" 2>/dev/null)" = 200 ] \
    && { ready=1; break; }
  sleep 5
done
[ "$ready" = 1 ] || { echo "[ext] FATAL proxy never came up for $LAB"; tail -20 "$arm_out/proxy_ext.log"; exit 1; }
echo "[ext] proxy up on :$P"
cleanup() { pkill -f "tinker_openai_proxy.py --port $P" 2>/dev/null || true; }
trap cleanup EXIT

# -- one eval: skip if its json already exists ------------------------------
run_one() {  # $1 result-json  $2 log-name  $3 dir  $4 python  ...cmd
  local json="$1" log="$2" dir="$3" py="$4"; shift 4
  if [ -f "$arm_out/$json" ]; then echo "  [skip] $json"; return 0; fi
  ( cd "$dir" && "$py" "$@" "$LAB" "$P" --out "$OUT" ) > "$arm_out/$log" 2>&1 \
    && echo "  [done] $json" \
    || { echo "  [FAIL] $json -- tail:"; tail -5 "$arm_out/$log" | sed 's/^/      /'; }
}

# T1 -- agentic reward hacking (the primary claim)
run_one hack_verifiable.json        hv.log       "$EXT/hack-verifiable"   "$LPY" run_hv.py --episodes 10 --conc 20 --max-steps 30
run_one denison_reward_tampering.json denison.log "$EXT/t1_sandbox"       "$LPY" run_denison.py --n 60
# T2 -- adjacent primitive, behavioural
run_one scheming.json               scheming.log "$EXT/scheming"          "$LPY" run_scheming.py --samples 25 --conc 16 --save-transcripts
run_one sandbagging.json            sandbag.log  "$EXT/sandbagging"       "$LPY" eval_sandbagging.py --n 180 --conc "$CONC"
run_one agentmisalignment.json      am.log       "$EXT/agentmisalignment" "$AMPY" run_household.py --conc "$CONC"
# T3 -- principal-agent faithfulness, dark patterns
run_one insider_trading.json        insider.log  "$EXT/insider-trading"   "$LPY" eval_insider.py --samples 40 --conc 16
run_one darkbench.json              darkbench.log "$EXT/darkbench"        "$LPY" eval_darkbench.py --conc 16

echo "[ext] $LAB COMPLETE"
ls "$arm_out"/*.json 2>/dev/null | xargs -r -n1 basename | tr '\n' ' '; echo
