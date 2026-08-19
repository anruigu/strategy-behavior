#!/usr/bin/env bash
# post_run.sh -- what has to happen the moment a mixed run stops training.
#
#   ./post_run.sh mixed_hole_d1_s0 [mixed_nohole_d1_s0 ...]
#   WAIT=0 ./post_run.sh mixed_hole_d1_s1        # run now, do not wait
#
# A finished run is only half a result: the dependent variable of this whole
# package is transfer to the held-out battery (EVAL_SUITE.md), never in-env
# reward. So on completion this does, per run, without being asked:
#
#   1. imports the dumped episode traces into the SkyRL trace viewer, so the
#      run is readable as trajectories-over-steps rather than a reward curve;
#   2. re-screens the trained checkpoint through the SAME cells it trained on,
#      which is the cheapest read of whether exploitation actually moved;
#   3. writes a manifest of the tinker checkpoint URIs the held-out battery
#      needs, and prints the T0/T1/T2 commands that consume them.
#
# Step 3 stops short of launching the external benchmarks. Those need a served
# checkpoint (evals/serve_tinker_ckpt.sh) and, for the slurm batteries, a live
# cluster -- both are heavier and more breakable than anything above, and
# firing them blind at 4am is how you get a half-finished eval nobody trusts.
# The manifest makes them one command each.
set -uo pipefail
cd "$(dirname "$0")"

PY="${PY:-/workspace/allie/venvs/tinker-ipd/bin/python}"
WAIT="${WAIT:-1}"
SCREEN_SEEDS="${SCREEN_SEEDS:-12}"
WORKERS="${WORKERS:-8}"
VIEWER_PORT="${VIEWER_PORT:-8795}"
OUT="${OUT:-results}"
mkdir -p "$OUT"

for label in "$@"; do
  rundir="runs/$label"
  [ -d "$rundir" ] || { echo "[post_run] no $rundir -- skipping"; continue; }

  if [ "$WAIT" = "1" ]; then
    echo "[post_run] $label: waiting for training to exit..."
    while pgrep -f "train_mixed.py.*$label" >/dev/null 2>&1; do sleep 60; done
    # the label is derived, not passed, so match on the arm+seed in the log
    while pgrep -f "train_mixed.py" >/dev/null 2>&1 \
          && grep -q "\[$label\]" /tmp/*launch.log 2>/dev/null \
          && ! grep -q "\[$label\] done" logs*/"$label".log 2>/dev/null; do
      sleep 60
    done
  fi
  echo "[post_run] $label: training finished"

  # -- 1. traces -> SkyRL viewer -------------------------------------------
  if [ -d "$rundir/traces" ] && [ -n "$(ls -A "$rundir/traces" 2>/dev/null)" ]; then
    echo "[post_run] $label: importing traces to the viewer"
    HOLE_GEN_CANDIDATES=1 "$PY" to_viewer.py --from-run "$rundir" --alias "$label" \
      2>&1 | grep -vi nltk | tail -3
    echo "[post_run] $label: http://localhost:${VIEWER_PORT}  (run: $label)"
  else
    echo "[post_run] $label: no traces dumped -- was it launched with --dump-traces?"
  fi

  # -- 2. re-screen the trained policy through its own cells ----------------
  envs=$("$PY" - "$rundir" <<'EOF'
import json, sys
print(" ".join(json.load(open(sys.argv[1] + "/config.json"))["envs"]))
EOF
)
  ckpt=$("$PY" - "$rundir" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1] + "/checkpoints.json"))
print(d[max(d, key=lambda k: int(k))] if d else "")
EOF
)
  arm=$("$PY" - "$rundir" <<'EOF'
import json, sys
print(json.load(open(sys.argv[1] + "/config.json"))["consequence"])
EOF
)
  echo "[post_run] $label: final checkpoint -> ${ckpt:-none}"
  if [ -n "$ckpt" ]; then
    echo "[post_run] $label: re-screening ${envs}"
    HOLE_GEN_CANDIDATES=1 "$PY" check_suite.py --screen-only --screen "$ckpt" \
      --envs $envs --doses 1.0 --screen-arms "$arm" \
      --screen-seeds "$SCREEN_SEEDS" --workers "$WORKERS" \
      --json "$OUT/postrun-screen-$label.json" 2>&1 | grep -vi nltk | tail -20
  fi

  # -- 3. manifest for the held-out battery ---------------------------------
  "$PY" - "$rundir" "$label" "$OUT" <<'EOF'
import json, sys
rundir, label, out = sys.argv[1], sys.argv[2], sys.argv[3]
cfg = json.load(open(f"{rundir}/config.json"))
ck = json.load(open(f"{rundir}/checkpoints.json"))
man = {"label": label, "model": cfg.get("model"), "arm": cfg.get("consequence"),
       "dose": cfg.get("dose"), "envs": cfg.get("envs"), "checkpoints": ck,
       "final": ck[max(ck, key=lambda k: int(k))] if ck else None}
p = f"{out}/postrun-manifest-{label}.json"
json.dump(man, open(p, "w"), indent=1)
print(f"[post_run] {label}: manifest -> {p}")
EOF

  cat <<EOF
[post_run] $label: held-out battery (EVAL_SUITE.md) is NOT run automatically:
    T1 (primary claim -- agentic reward hacking)
      python ../exploit-bench/eval/eval_checkpoint.py \\
          --checkpoints $rundir/checkpoints.json --which final \\
          --workers 16 --md $OUT/t1-$label.md
    T0/T2 (served-model batteries -- need a GPU + the slurm cluster)
      ../evals/serve_tinker_ckpt.sh <exported-peft-dir> $label
      ../evals/run_mask.sh $label
EOF
done
echo "[post_run] all done"
