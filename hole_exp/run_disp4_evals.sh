#!/usr/bin/env bash
# Periodic transfer read for the think3 disposition wave.
#
#   ./run_disp4_evals.sh                  # watch; fire at each milestone
#   STEPS=60 ./run_disp4_evals.sh --once  # one milestone, now, then exit
#   EXT_AT="150" ./run_disp4_evals.sh     # external battery only at step 150
#
# WHAT RUNS AT EACH MILESTONE, in order of cost:
#
#   1. disposition_reasoning.py -- offline, free. Scores the reasoning blocks
#      already on the trace pages. This is the read that says whether the noisy
#      hole arm models its counterpart or has collapsed to a rule.
#   2. eval_generalization.py -- the project's dependent variable: audit twins,
#      two held-out games, and the ten Suite-2 synthetic scenarios. In-env
#      behaviour is NOT the finding (EVAL_SUITE §0.2); this is.
#   3. run_external_battery.sh -- T1/T2/T3, one proxy per arm, ~2h per arm. Only
#      at the steps named in EXT_AT, because it is an order of magnitude more
#      expensive than everything above and its sample sizes are pinned to the
#      frame-* arms' for comparability, so running it more often buys nothing.
#
# MATCHED STEPS, NOT LATEST STEPS. Every arm is read at the SAME step or the
# milestone is skipped. `eval_generalization.ckpt_at` falls back to the nearest
# checkpoint at or below the request, which is right for one arm and wrong for a
# table: it turns "not there yet" into "an earlier checkpoint" with nothing in
# the output saying so. The wait loop below is what makes the fallback moot.
#
# THINKING ON, EFFORT LOW, BASE = 3.8. All four arms trained that way. Serving
# them any other way evaluates a policy that never ran, and the stock base row
# is Qwen3.6-27B -- a different model, which would make every delta a model
# difference. Both are passed explicitly everywhere below.
set -uo pipefail
cd /workspace/allie/strategy-behavior/hole_exp

PY=/workspace/allie/venvs/tinker-ipd/bin/python
MPY=/workspace/allie/venvs/marshal/bin/python
STEPS="${STEPS:-30 60 90 120 150}"
EXT_AT="${EXT_AT:-150}"
SEEDS="${SEEDS:-6}"
WORKERS="${WORKERS:-16}"
BASE_MODEL="${BASE_MODEL:-Qwen/Qwen3.8-27B}"
POLL="${POLL:-900}"
OUT="${OUT:-results/0825_disp4}"
PORT0="${PORT0:-8660}"

# arm key in eval_generalization.ARMS -> run directory
declare -A RUN=(
  [t3noisy]="mixed_think3_hole-think-noisy_d1_s0"
  [t3nohole]="mixed_think3_nohole-think_d1_s0"
  [t3adaptive]="mixed_think3_adaptive-think_d1_s0"
  [t3adaptrec]="mixed_think3_adaptrec-think_d1_s0"
)
ARMS="${ARMS:-t3noisy t3nohole t3adaptive t3adaptrec}"

export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
mkdir -p "$XDG_CACHE_HOME" "$OUT" logs/wave

has_step() {  # run, step -> 0 if that EXACT step is checkpointed
  "$MPY" - "$1" "$2" <<'PYEOF'
import json, sys
try:
    d = json.load(open(f"runs/{sys.argv[1]}/checkpoints.json"))
except Exception:
    sys.exit(1)
sys.exit(0 if str(int(sys.argv[2])) in {str(int(k)) for k in d} else 1)
PYEOF
}

ckpt_at() {  # run, step -> the tinker:// uri at exactly that step
  "$MPY" - "$1" "$2" <<'PYEOF'
import json, sys
d = {int(k): v for k, v in json.load(open(f"runs/{sys.argv[1]}/checkpoints.json")).items()}
print(d.get(int(sys.argv[2]), ""))
PYEOF
}

all_ready() {  # step -> 0 when every arm has it
  local step="$1" arm
  for arm in $ARMS; do
    has_step "${RUN[$arm]}" "$step" || return 1
  done
  return 0
}

milestone() {
  local step="$1"
  echo "[disp4] ===== step $step ====="

  # -- 1. reasoning patterns (offline) --------------------------------------
  "$MPY" disposition_reasoning.py --quote 4 \
    --write "$OUT/REASONING_step${step}.md" \
    > "logs/wave/reasoning_step${step}.log" 2>&1 \
    && echo "  [done] REASONING_step${step}.md" \
    || { echo "  [warn] reasoning read failed:"; tail -3 "logs/wave/reasoning_step${step}.log" | sed 's/^/      /'; }

  # -- 2. transfer: audit twins + held-out games + the ten scenarios ---------
  if [ -f "$OUT/generalization_step${step}.json" ]; then
    echo "  [skip] generalization_step${step}.json"
  else
    "$PY" eval_generalization.py \
      --step "$step" --arms $ARMS --run-seeds 0 --seeds "$SEEDS" \
      --think --reasoning-effort low --base-model "$BASE_MODEL" \
      --temperature 0.7 --max-tokens 1024 --workers "$WORKERS" \
      --json "$OUT/generalization_step${step}.json" \
      --md "$OUT/GENERALIZATION_step${step}.md" \
      > "logs/wave/gen_step${step}.log" 2>&1 \
      && echo "  [done] GENERALIZATION_step${step}.md" \
      || { echo "  [FAIL] generalization -- tail:"; tail -6 "logs/wave/gen_step${step}.log" | sed 's/^/      /'; }
  fi

  # -- 3. the external battery, only where asked ----------------------------
  case " $EXT_AT " in
    *" $step "*)
      local port=$PORT0 arm uri
      for arm in $ARMS; do
        uri="$(ckpt_at "${RUN[$arm]}" "$step")"
        [ -n "$uri" ] || { echo "  [ext] no checkpoint at $step for $arm"; continue; }
        echo "  [ext] $arm-s$step on :$port"
        THINK=1 EFFORT=low ./run_external_battery.sh "${arm}-s${step}" "$uri" "$port" \
          > "logs/wave/ext_${arm}_step${step}.log" 2>&1 \
          && echo "  [done] battery $arm-s$step" \
          || { echo "  [FAIL] battery $arm-s$step -- tail:"; tail -5 "logs/wave/ext_${arm}_step${step}.log" | sed 's/^/      /'; }
        port=$((port + 1))
      done
      ;;
  esac
  echo "[disp4] step $step complete -> $OUT"
}

ONCE=0
[ "${1:-}" = "--once" ] && ONCE=1

for step in $STEPS; do
  if [ "$ONCE" = 1 ]; then
    all_ready "$step" || { echo "[disp4] step $step not reached by every arm; skipping"; continue; }
    milestone "$step"
    continue
  fi
  echo "[disp4] waiting for step $step across: $ARMS"
  until all_ready "$step"; do
    # A dead wave must not leave this polling forever. If no training job is
    # running and the step still is not there, it never will be.
    if ! squeue -u "$(whoami)" -h -o "%j" 2>/dev/null | grep -q '^d4-\|^t3-'; then
      echo "[disp4] no training jobs left and step $step never landed -- stopping"
      exit 0
    fi
    sleep "$POLL"
  done
  milestone "$step"
done
echo "[disp4] ALL MILESTONES DONE -> $OUT"
