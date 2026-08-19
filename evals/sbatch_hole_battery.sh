#!/usr/bin/env bash
#SBATCH --job-name=hole-battery
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32
#SBATCH --time=12:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/evals/slurm-hole-battery-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/evals/slurm-hole-battery-%j.out
#
# Merge a hole_exp LoRA arm into a full checkpoint, serve it, and run the
# held-out battery against it. One job per ARM, and always with --exclusive
# --nodelist: the served port below is node-local, so two arms on one node
# fight over it (sbatch_mask.sh's own header records that a stale server on
# this port once cost three full eval arms).
#
#   sbatch --exclusive --nodelist=node-0 sbatch_hole_battery.sh <arm> <adapter>
#
# SERVING VENV. Not $SAT_VENV. That one pins vLLM 0.8.4 / transformers 4.51.3,
# which predate Qwen3.6's `qwen3_5_text` architecture and abort at config load
# with "Transformers does not recognize this architecture". `venvs/vllm-new`
# (vLLM 0.27.1 / transformers 5.15.1) reads it. Upgrading $SAT_VENV in place
# was rejected: oat + textarena are pinned against the old build there.
# `run_mask.sh` is unaffected either way -- it runs out of MASK's own venv and
# only ever talks to the served endpoint over HTTP.
set -uo pipefail
ARM="$1"; ADAPTER="$2"
: "${SAT_HOME:=/workspace/allie/strategy-behavior}"
: "${MERGED_ROOT:=/workspace/allie/merged}"
: "${SERVE_VENV:=/workspace/allie/venvs/vllm-new}"
: "${PORT:=8000}"
MERGED="$MERGED_ROOT/$ARM"

echo "node=$(hostname) arm=$ARM adapter=$ADAPTER"

# -- 1. merge (idempotent: a completed merge is reused) ----------------------
if [ -f "$MERGED/config.json" ]; then
  echo "[battery] reusing merged checkpoint $MERGED"
else
  mkdir -p "$MERGED_ROOT"
  echo "[battery] merging $ADAPTER -> $MERGED"
  /workspace/allie/venvs/lora-export/bin/python "$SAT_HOME/evals/merge_lora.py" \
      --adapter "$ADAPTER" --out "$MERGED" --force || exit 1
fi

# -- 2. serve ---------------------------------------------------------------
if ss -tln 2>/dev/null | grep -q ":$PORT "; then
  echo "[battery] clearing a stale server on :$PORT"
  for q in $(pgrep -u "$(id -u)" -f "vllm" 2>/dev/null); do kill -9 "$q" 2>/dev/null || true; done
  sleep 5
fi
echo "[battery] serving $MERGED as '$ARM' on :$PORT"
setsid "$SERVE_VENV/bin/python" -m vllm.entrypoints.openai.api_server \
  --model "$MERGED" --served-model-name "$ARM" --port "$PORT" \
  --gpu-memory-utilization 0.85 --max-model-len 8192 --max-num-seqs 64 \
  --dtype bfloat16 > "/tmp/vllm-$ARM.log" 2>&1 &
VLLM_PID=$!
cleanup() { kill -- -"$VLLM_PID" 2>/dev/null || kill -9 "$VLLM_PID" 2>/dev/null || true; }
trap cleanup EXIT

for i in $(seq 1 180); do
  if curl -sf "http://localhost:$PORT/v1/models" >/dev/null 2>&1; then
    echo "[battery] server up after ${i}0s"; break
  fi
  if ! kill -0 "$VLLM_PID" 2>/dev/null; then
    echo "FATAL: vllm died; last lines:"; tail -30 "/tmp/vllm-$ARM.log"; exit 1
  fi
  sleep 10
done
curl -sf "http://localhost:$PORT/v1/models" >/dev/null 2>&1 || {
  echo "FATAL: server never became ready"; tail -30 "/tmp/vllm-$ARM.log"; exit 1; }

# -- 3. the battery ---------------------------------------------------------
echo "[battery] MASK on $ARM"
bash "$SAT_HOME/evals/run_mask.sh" "$ARM" || echo "[battery] MASK returned $?"

# -- 4. reclaim the merged checkpoint ----------------------------------------
# A merged 27B is ~51GB and /workspace runs at 99%; two arms of one pair fill
# 102GB, which is already more than the next pair needs to merge at all. The
# LoRA adapter (~900MB) and the tinker checkpoint URI both survive, so the
# merge is reproducible from `merge_lora.py` in minutes -- keeping the full
# weights around buys nothing but an outage for whoever merges next.
# KEEP_MERGED=1 to hold it (e.g. to re-serve for a second battery).
if [ "${KEEP_MERGED:-0}" = "1" ]; then
  echo "[battery] KEEP_MERGED=1 -- leaving $MERGED ($(du -sh "$MERGED" 2>/dev/null | cut -f1))"
else
  cleanup                       # stop the server before pulling its weights
  sleep 5
  echo "[battery] reclaiming $MERGED ($(du -sh "$MERGED" 2>/dev/null | cut -f1))"
  rm -rf "$MERGED"
  df -h /workspace | tail -1
fi
echo "[battery] $ARM done"
