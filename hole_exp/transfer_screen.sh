#!/usr/bin/env bash
# transfer_screen.sh -- out-of-domain transfer, measured inside this harness.
#
# Both mixed runs trained on GAMES only, so the transfer question is whether a
# disposition learned there shows up in synthetic SCENARIOS the policy never
# saw. (Symmetrically, a scenario-trained run would be screened on the games.)
#
# This deliberately does NOT go through the external battery. That path needs a
# merged checkpoint (~51GB), a vLLM build new enough for Qwen3.6, and a chat
# template the exploit-bench harness agrees with -- three separate breakages so
# far. `check_suite --screen` samples the tinker checkpoint directly, so a
# transfer number costs sampling quota and nothing else.
#
# The reading is the ARM DIFFERENCE on held-out cells: hole-arm minus no-hole
# arm, with the base model as the anchor. Both arms saw identical games,
# identical opponents and identical action spaces -- only the audit differed --
# so a gap here is the disposition travelling, not task exposure.
set -uo pipefail
cd "$(dirname "$0")"

PY="${PY:-/workspace/allie/venvs/tinker-ipd/bin/python}"
TARGETS="${TARGETS:-gatekeeping politics commerce markets principal_agent}"
SEEDS="${SEEDS:-12}"
WORKERS="${WORKERS:-8}"
OUT="${OUT:-results}"
mkdir -p "$OUT"

ckpt_of() {  # final checkpoint URI for a run label
  "$PY" -c "
import json,sys
d=json.load(open('runs/$1/checkpoints.json'))
print(d[max(d,key=lambda k:int(k))])"
}

declare -A ARMS
ARMS[base]="Qwen/Qwen3.6-27B"
for label in "$@"; do ARMS[$label]="$(ckpt_of "$label")"; done

for name in "${!ARMS[@]}"; do
  model="${ARMS[$name]}"
  echo "=============================================================="
  echo "[transfer] $name -> $TARGETS"
  echo "[transfer] model: $model"
  HOLE_GEN_CANDIDATES=1 "$PY" -u check_suite.py --screen-only --screen "$model" \
    --envs $TARGETS --doses 1.0 --screen-arms hole \
    --screen-seeds "$SEEDS" --workers "$WORKERS" \
    --json "$OUT/transfer-$name.json" 2>&1 | grep -viE "nltk|PyTorch was not found"
done
echo "[transfer] all done; rows in $OUT/transfer-*.json"
