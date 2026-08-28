#!/usr/bin/env bash
# Resume the six think4 runs from their last STATE checkpoint.
#
#   ./resume_think4.sh --check     # print what would happen, launch nothing
#   ./resume_think4.sh --all       # resume all six, staggered
#
# WHY THIS EXISTS. The wave stopped at 08:04Z on 2026-08-26 when Tinker began
# returning HTTP 402 ("Access is blocked due to billing status") to every
# sampling call. All six died within four seconds of each other. Nothing is
# wrong with the runs, the box or the simulator -- so the right move is to
# continue the same trajectories rather than start a seventh wave.
#
# RESUME, DO NOT RELAUNCH. `train_mixed.py` appends to `runs/<label>/metrics.jsonl`
# and rewrites `config.json` under the same label. Relaunching without
# --resume-from/--start-step would restart at step 0 and append a SECOND
# trajectory to the same file under the same name, which is precisely the
# mixed-provenance mess the think3 directories on this box are already in (their
# metrics carry per-env rows for envs their own config.json does not list).
# --start-step keeps metrics.jsonl one series and preserves the earlier
# checkpoint keys.
#
# CHECK BILLING FIRST. This script probes the API before touching anything: six
# runs relaunched into a still-blocked account just rewrite six configs and die
# again, and the probe costs one request.
set -uo pipefail
cd "$(dirname "$0")"

PY=/home/ubuntu/venvs/tinker-ipd/bin/python
FIG_PY=/home/ubuntu/venvs/tools/bin/python
RUNS=/home/ubuntu/strategy-behavior/hole_exp/runs
LOGS=/home/ubuntu/strategy-behavior/hole_exp/logs/think4
STEPS="${STEPS:-150}"
WORKERS="${WORKERS:-10}"
STAGGER="${STAGGER:-40}"

set -a; . /home/ubuntu/.research_env 2>/dev/null || true; set +a
export HOME=/home/ubuntu XDG_CACHE_HOME=/home/ubuntu/.cache
export WANDB_DIR=/home/ubuntu/strategy-behavior/hole_exp/wandb
[ -n "${FLEET_WANDB_API_KEY:-}" ] && export WANDB_API_KEY="$FLEET_WANDB_API_KEY"
mkdir -p "$LOGS"

# WRAPPED IN `timeout`, because the tinker client RETRIES a 402. Left to
# itself the probe sat for well over five minutes retrying a hard, permanent
# error and printed nothing -- so `--check`, whose whole job is to answer
# quickly, hung. A probe that has not answered in 60s is treated as not-OK.
billing_ok() {
  timeout 60 "$PY" - <<'PYEOF' >/dev/null 2>&1
import sys, tinker
try:
    tinker.ServiceClient().get_server_capabilities()
except Exception as e:
    sys.exit(2 if "402" in str(e) or "billing" in str(e).lower() else 3)
PYEOF
}

# label -> the flags that define its cell, recovered from the run's own config
# rather than re-typed, so a resumed run cannot silently change condition.
flags_for() {
  "$FIG_PY" - "$1" <<'PYEOF'
import json, sys
c = json.load(open(f"runs/{sys.argv[1]}/config.json"))
out = ["--consequence", c["consequence"],
       "--nohole-shape", c["nohole_shape"],
       "--dose", str(c["dose"]), "--seed", str(c["seed"]),
       "--model", c["model"], "--groups", str(c["groups"]),
       "--group-size", str(c["group_size"]),
       "--temperature", str(c["temperature"]), "--top-p", str(c["top_p"]),
       "--max-tokens", str(c["max_tokens"]),
       "--ckpt-every", str(c["ckpt_every"]),
       "--dump-traces", str(c["dump_traces"]),
       "--label-suffix", c["label_suffix"],
       "--reasoning-effort", c["reasoning_effort"],
       "--envs"] + list(c["envs"])
if c["think"]:
    out.append("--think")
if c["endgame_penalty"]:
    out += ["--endgame-penalty", str(c["endgame_penalty"]),
            "--endgame-frac", str(c["endgame_frac"])]
if c["horizon"] != "finite":
    out += ["--horizon", c["horizon"]]
print(" ".join(out))
PYEOF
}

latest_state() {
  "$FIG_PY" - "$1" <<'PYEOF'
import json, sys
d = json.load(open(f"runs/{sys.argv[1]}/checkpoints_state.json"))
k = max(d, key=lambda x: int(x))
print(f"{k}\t{d[k]}")
PYEOF
}

LABELS=$(cd "$RUNS" && ls -d mixed_think4_* 2>/dev/null)

if [ "${1:-}" = "--check" ]; then
  if billing_ok; then echo "billing: OK"; else echo "billing: STILL BLOCKED (402) -- resume will fail"; fi
  for l in $LABELS; do
    IFS=$'\t' read -r step uri <<<"$(latest_state "$l")"
    last=$(tail -1 "$RUNS/$l/metrics.jsonl" | "$FIG_PY" -c 'import sys,json;print(json.load(sys.stdin)["step"])')
    echo "  $l"
    echo "      metrics reach step $last, resuming from state step $step"
    echo "      $uri"
  done
  exit 0
fi

[ "${1:-}" = "--all" ] || { echo "usage: $0 --check | --all" >&2; exit 1; }

if ! billing_ok; then
  echo "REFUSING: Tinker still returns 402 (billing)." >&2
  echo "Add payment at https://tinker.thinkingmachines.ai/billing/balance, then re-run." >&2
  exit 1
fi

for l in $LABELS; do
  IFS=$'\t' read -r step uri <<<"$(latest_state "$l")"
  log="$LOGS/resume-$(echo "$l" | sed 's/^mixed_think4_nohole-think-//; s/_d1_s0//').log"

  # DROP THE STEPS ABOUT TO BE RECOMPUTED. State is saved at the START of a
  # checkpoint step, so four of these six runs logged metrics PAST their last
  # state (e.g. metrics reach 13, state is at 10). Resuming re-runs 10-13 and
  # `train_mixed.py` only ever appends -- so metrics.jsonl would carry two rows
  # for each of those steps, and `behaviour()` in the plot script reads every
  # row in file order, which turns a duplicate into a zigzag in the curve
  # rather than an error anyone would notice. The originals are kept beside it.
  "$FIG_PY" - "$l" "$step" <<'PYEOF'
import json, shutil, sys
from pathlib import Path
label, start = sys.argv[1], int(sys.argv[2])
f = Path("runs") / label / "metrics.jsonl"
rows = [l for l in f.read_text().splitlines() if l.strip()]
keep = [l for l in rows if json.loads(l)["step"] < start]
if len(keep) != len(rows):
    shutil.copy2(f, f.with_suffix(".jsonl.pre-resume"))
    f.write_text("\n".join(keep) + "\n")
    print(f"      trimmed {len(rows) - len(keep)} row(s) at step >= {start} "
          f"(backup: {f.name}.pre-resume)")
PYEOF

  echo "[resume] $l from step $step -> $log"
  setsid nohup "$PY" train_mixed.py $(flags_for "$l") \
    --steps "$STEPS" --workers "$WORKERS" \
    --resume-from "$uri" --start-step "$step" \
    --out "$RUNS" --use-wb \
    > "$log" 2>&1 < /dev/null &
  sleep "$STAGGER"
done
echo "[resume] all launched. then: setsid nohup ./watchdog_think4.sh >> $LOGS/watchdog.log 2>&1 &"
