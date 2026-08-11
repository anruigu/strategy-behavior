#!/usr/bin/env bash
# serve_tinker_ckpt.sh -- vLLM-serve a Tinker LoRA checkpoint for the MASK pipeline.
#
# The Tinker training arm (../training/tinker/) produces LoRA adapters, not full
# checkpoint dirs, so serve_ckpt.sh cannot open them. Export one first:
#
#   python ../training/tinker/export_lora.py \
#       --checkpoints <run>/checkpoints.jsonl --step 256 --out /path/to/peft
#
# then serve base + adapter here. Everything downstream (run_mask.sh,
# compare_mask_arms.py) is unchanged: it only ever sees the served model NAME.
#
#   ./serve_tinker_ckpt.sh <peft-adapter-dir> [served-name] [port] [gpu] [base-model]
#
# The served name IS the MASK arm name, so pick the one you will pass to
# run_mask.sh / compare_mask_arms.py (e.g. spiral-tinker-kuhn-step256).
set -euo pipefail
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
source "$SAT_HOME/config.sh"
source "$SAT_VENV/bin/activate"
set -a; . "$SAT_ENV_FILE"; set +a
export HF_HOME="$SAT_HF_HOME"

ADAPTER="${1:?usage: serve_tinker_ckpt.sh <peft-adapter-dir> [served-name] [port] [gpu] [base-model]}"
NAME="${2:-spiral-tinker-ckpt}"
PORT="${3:-8000}"
GPU="${4:-0}"
# Must match the base the LoRA was trained against; a mismatch loads without
# error and produces garbage. export_lora.py prints the right value, and it is
# recorded per-checkpoint in the run's checkpoints.jsonl.
BASE="${5:-${SAT_TINKER_BASE_MODEL:-Qwen/Qwen3.5-9B-Base}}"

[ -f "$ADAPTER/adapter_config.json" ] || {
  echo "error: $ADAPTER has no adapter_config.json -- is it a PEFT dir?" >&2
  echo "       run training/tinker/export_lora.py first." >&2
  exit 1
}

export CUDA_VISIBLE_DEVICES="$GPU"

# --served-model-name applies to the BASE entry; the LoRA is exposed under the
# --lora-modules key. MASK asks for one model name, so both are set to $NAME and
# the adapter shadows the base in the model list.
#
# KV-cache flags copied from serve_ckpt.sh for the same reason: hard-cap the
# footprint so the server is predictable regardless of what else is resident.
exec python -m vllm.entrypoints.openai.api_server \
  --model "$BASE" \
  --served-model-name "${NAME}-base" \
  --enable-lora \
  --lora-modules "${NAME}=${ADAPTER}" \
  --max-lora-rank 64 \
  --port "$PORT" \
  --gpu-memory-utilization 0.72 \
  --num-gpu-blocks-override 2048 \
  --max-model-len 8192 \
  --max-num-seqs 4 \
  --enforce-eager \
  --disable-log-requests
