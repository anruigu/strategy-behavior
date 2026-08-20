#!/usr/bin/env bash
# run_agentic_wave.sh -- corpus -> warm start -> gate -> matched RL pair, unattended.
#
# Wave 2: the AGENTIC merchant on Qwen/Qwen3.8-27B. Everything downstream of the
# corpus is already orchestrated by launch_merchant_wave.py (it waits for the
# warm-start manifest, screens every epoch checkpoint, refuses to launch unless
# one lands in [0.15, 0.50], and seeds both arms from the same STATE path). This
# adds the two steps in front of it and the monitoring behind it.
#
# Why a warm start at all, when the agentic redesign was supposed to remove the
# need: it did, on the number I had at the time. Fixing the `disclose_defect`
# bug -- which was scoring a disclosed defect as concealment and inflating the
# rate roughly 3x -- took the 3.8-27B base rate from 0.222 to 0.076, below the
# band. So the warm start is back, and with it the identifiability caveat:
# exploration is seeded rather than found, and the W row has to be read on the
# battery BEFORE the RL contribution can be attributed.
#
# Everything here uses tinker_actor.TUNED_TOOL_SAMPLING. Untuned, Qwen3.8-27B is
# 93% unparseable on this env and every stage would distil or measure format
# failure instead of conduct.
#
#   nohup ./run_agentic_wave.sh > logs/agentic-wave.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")"
PY=/workspace/allie/venvs/tinker-ipd/bin/python

MODEL="${MODEL:-Qwen/Qwen3.8-27B}"
LABEL="${LABEL:-merchant-ws-agentic-38}"
CORPUS="${CORPUS:-data/sft-merchant-agentic-38.jsonl}"
STEPS="${STEPS:-90}"
EPOCHS="${EPOCHS:-3}"

echo "=== [1/4] wait for the corpus ==="
for _ in $(seq 1 240); do
  [ -s "$CORPUS" ] && [ -s "${CORPUS%.jsonl}.summary.json" ] && break
  pgrep -f "gen_sft.py" >/dev/null || {
    [ -s "$CORPUS" ] || { echo "gen_sft died before writing $CORPUS"; exit 1; }; }
  sleep 30
done
[ -s "$CORPUS" ] || { echo "timed out waiting for $CORPUS"; exit 1; }
"$PY" - <<PYEOF
import json
s=json.load(open("${CORPUS%.jsonl}.summary.json"))["summary"]
print(f"  corpus: {s['episodes']} eps, {s['supervisable_turns']} supervisable, "
      f"rate {s['corpus_exploit_rate']:.3f}, invalid {s['invalid_turns']}")
PYEOF

echo "=== [2/4] SFT warm start ==="
"$PY" sft_warmstart.py --data "$CORPUS" --model "$MODEL" --label "$LABEL" \
    --epochs "$EPOCHS" --lr 1e-5 --batch-size 8 --lora-rank 32 \
    2>&1 | grep -av "^\[transformers\]"
[ -s "runs/$LABEL/warmstart.json" ] || { echo "no warmstart.json -- stopping"; exit 1; }

echo "=== [3/4] gate + launch the matched pair ==="
# launch_merchant_wave screens every checkpoint with the tuned profile, picks the
# one closest to the middle of [0.15, 0.50], and launches NOTHING if none lands
# in it. A failed gate here is the correct outcome, not an error to work around.
"$PY" launch_merchant_wave.py --label "$LABEL" --model "$MODEL" \
    --steps "$STEPS" --seeds 24 --workers 20 --wait 600 \
    2>&1 | grep -av "^\[transformers\]"
rc=$?

echo "=== [4/4] monitoring ==="
if pgrep -f "train_hole.py.*merchant" >/dev/null; then
  setsid "$PY" post_run.py --runs merchant_hole_d1_s0 merchant_nohole_d1_s0 \
      --watch --seeds 8 --conc 10 --every 300 \
      < /dev/null > logs/postrun-agentic-38.log 2>&1 &
  setsid "$PY" watch_runs.py --every 600 \
      < /dev/null > logs/watch-agentic-38.log 2>&1 &
  echo "  post_run + watch_runs up"
else
  echo "  NO ARMS RUNNING -- the gate refused, or the launch failed."
  echo "  Read the [wave] lines above: if every checkpoint screened outside"
  echo "  [0.15, 0.50], re-tune --p-exploit and regenerate the corpus."
fi
echo "=== wave script done (rc=$rc) ==="
