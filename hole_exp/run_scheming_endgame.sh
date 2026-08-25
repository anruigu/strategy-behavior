#!/usr/bin/env bash
# Apollo-style in-context scheming, for the endgame/horizon arms vs their base.
#
#   ./run_scheming_endgame.sh            # step 50, all arms + base
#   STEP=80 ARMS="inf" ./run_scheming_endgame.sh
#
# THE HYPOTHESIS. Endgame reasoning ("the last round has no future to punish
# me") is instrumentally the same move as covert subversion under believed
# oversight: both are "act badly where the consequence cannot reach me". If
# training on a DISCLOSED horizon reinforces that, the finite arms should
# scheme more than the arm whose horizon was hidden.
#
# MATCHED STEP, NOT LATEST STEP. `inf` has trained further than the other two
# (it was stopped later and resumed from a later state), so scoring each arm at
# "its latest" would confound the arm with how long it trained. Everything runs
# at $STEP, the latest step all three share; run `inf` at 80 separately as a
# supplement, not in the same table.
#
# THE BASE ROW MUST BE Qwen3.8-27B. The battery's stock `frame-base` is
# Qwen3.6-27B -- a different model. Scoring these arms against it would make
# every delta a model difference. It is passed explicitly here.
#
# THINKING ON, EFFORT LOW. These arms trained with the reasoning block on at
# effort `low`; serving them with it off evaluates a policy that never ran, and
# serving it at the Qwen3.8 template default (xhigh) runs past max_tokens and
# returns a thought with no action. The proxy takes --reasoning-effort for this.
# The raw text (reasoning included) is what the judge reads, which is the Apollo
# convention -- and the harness's action parser takes the LAST `Action:` block,
# which lands after `</think>`, so a considered action is not read as a taken one.
#
# WHAT THIS HARNESS DOES AND DOES NOT COVER. `evals_external/scheming` is a
# self-built re-implementation of four of Apollo's six scenario TYPES, all of
# them COVERT subversion: oversight_subversion, self_exfiltration, goal_guarding,
# covert_manipulation. The two DEFERRED evals -- instrumental alignment faking
# and sandbagging -- are not in it. Sandbagging has its own eval in the battery
# and is run here too. Alignment faking is absent, and with it Apollo's
# load-bearing design for deferred subversion: the believed-deployment-status
# contrast, where a model counts as scheming if it behaves differently when it
# thinks it is being tested. That contrast is NOT measured below, so nothing
# here speaks to deferred subversion.
set -uo pipefail
cd /workspace/allie/strategy-behavior/hole_exp

# 45, not 50: `inf` resumed from step 68 so its checkpoint grid is
# 0/22/45/68/70/80 and it has no 50. `ckpt_at` takes the nearest AT OR BELOW,
# so STEP=50 would quietly have scored finite@50, eg@50 and inf@45 and called
# the table matched. 45 is the latest step all three actually share; the guard
# below refuses to run if that ever stops being true.
STEP="${STEP:-45}"
ARMS="${ARMS:-finite eg inf}"
SAMPLES="${SAMPLES:-25}"
CONC="${CONC:-12}"
BASE_MODEL="${BASE_MODEL:-Qwen/Qwen3.8-27B}"
PORT0="${PORT0:-8640}"

TPY=/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python
LPY=/workspace/allie/venvs/spiral/bin/python
SCHEM=/workspace/allie/evals_external/scheming
SAND=/workspace/allie/evals_external/sandbagging
OUT=/workspace/allie/strategy-behavior/hole_exp/results/scheming

declare -A RUN=(
  [finite]="mixed_think2_nohole-think_d1_s0"
  [eg]="mixed_think2_nohole-think_d1_s0_eg2"
  [inf]="mixed_think2_nohole-think_d1_s0_inf"
)

set -a; . /workspace/allie/.env 2>/dev/null || true; set +a
export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
mkdir -p "$XDG_CACHE_HOME" "$OUT" logs/scheming

ckpt_at() {  # run, step -> tinker:// path at or below step
  /workspace/allie/venvs/marshal/bin/python - "$1" "$2" <<'PYEOF'
import json, sys
d = {int(k): v for k, v in json.load(open(f"runs/{sys.argv[1]}/checkpoints.json")).items()}
below = [s for s in d if s <= int(sys.argv[2])]
print(d[max(below)] if below else "")
PYEOF
}

one_arm() {  # label, model, port
  local lab="$1" model="$2" port="$3"
  local arm_out="$OUT/$lab"; mkdir -p "$arm_out"
  echo "[scheme] $lab  port=$port"
  echo "[scheme]   $model"

  pkill -f "tinker_openai_proxy.py --port $port" 2>/dev/null; sleep 2
  local think=(--enable-thinking --reasoning-effort low)
  setsid nohup "$TPY" /workspace/allie/ipd_exp/tinker_openai_proxy.py \
    --port "$port" --arm "$lab" --model "$model" --concurrency "$CONC" \
    "${think[@]}" > "$arm_out/proxy.log" 2>&1 < /dev/null &
  local ready=0
  for _ in $(seq 1 72); do
    [ "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:$port/v1/models" 2>/dev/null)" = 200 ] \
      && { ready=1; break; }
    sleep 5
  done
  [ "$ready" = 1 ] || { echo "[scheme]   FATAL proxy never came up"; tail -20 "$arm_out/proxy.log"; return 1; }

  if [ -f "$arm_out/scheming.json" ]; then
    echo "  [skip] scheming.json"
  else
    ( cd "$SCHEM" && "$LPY" run_scheming.py --samples "$SAMPLES" --conc "$CONC" \
        --save-transcripts "$lab" "$port" --out "$OUT" ) \
      > "$arm_out/scheming.log" 2>&1 \
      && echo "  [done] scheming.json" \
      || { echo "  [FAIL] scheming -- tail:"; tail -6 "$arm_out/scheming.log" | sed 's/^/      /'; }
  fi
  if [ -f "$arm_out/sandbagging.json" ]; then
    echo "  [skip] sandbagging.json"
  else
    ( cd "$SAND" && "$LPY" eval_sandbagging.py --n 120 --conc "$CONC" \
        "$lab" "$port" --out "$OUT" ) \
      > "$arm_out/sandbag.log" 2>&1 \
      && echo "  [done] sandbagging.json" \
      || { echo "  [FAIL] sandbagging -- tail:"; tail -6 "$arm_out/sandbag.log" | sed 's/^/      /'; }
  fi
  pkill -f "tinker_openai_proxy.py --port $port" 2>/dev/null || true
}

trap 'pkill -f "tinker_openai_proxy.py --port 86" 2>/dev/null || true' EXIT

step_of() {  # run, step -> the step actually resolved
  /workspace/allie/venvs/marshal/bin/python - "$1" "$2" <<'PYEOF'
import json, sys
d = {int(k): v for k, v in json.load(open(f"runs/{sys.argv[1]}/checkpoints.json")).items()}
below = [s for s in d if s <= int(sys.argv[2])]
print(max(below) if below else -1)
PYEOF
}

# REFUSE TO SILENTLY COMPARE DIFFERENT AMOUNTS OF TRAINING. `ckpt_at` falls back
# to the nearest step at or below the request, which is the right behaviour for
# a single arm and the wrong one for a table: it turns "no checkpoint here" into
# "a checkpoint from earlier" with nothing in the output saying so.
resolved=""
for a in $ARMS; do
  s="$(step_of "${RUN[$a]}" "$STEP")"
  echo "[scheme] $a resolves step $STEP -> $s"
  resolved="$resolved $s"
done
if [ "$(echo $resolved | tr ' ' '\n' | sort -u | wc -l)" -ne 1 ]; then
  echo "[scheme] REFUSING: arms resolve to different steps ($resolved)." >&2
  echo "[scheme] Pick a STEP every arm has, or run them as separate tables." >&2
  exit 1
fi

port=$PORT0
one_arm "base-q38" "$BASE_MODEL" "$port"
for a in $ARMS; do
  port=$((port + 1))
  uri="$(ckpt_at "${RUN[$a]}" "$STEP")"
  [ -n "$uri" ] || { echo "[scheme] no checkpoint <= $STEP for $a, skipping"; continue; }
  one_arm "${a}-s${STEP}" "$uri" "$port"
done
echo "[scheme] ALL DONE -> $OUT"
