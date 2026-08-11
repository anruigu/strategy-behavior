#!/usr/bin/env bash
# serve_arena.sh -- throughput-tuned vLLM server for arena_eval.py.
#
# Distinct from serve_tinker_ckpt.sh, which is tuned for MASK: that one caps
# --max-num-seqs at 4 and overrides the KV block count so the server stays small
# and predictable next to whatever else is resident. The arena eval is the
# opposite workload -- a few hundred short games in flight at once, nothing else
# on the GPU -- so it wants concurrency instead.
#
#   ./serve_arena.sh <port> <gpu> <base-model-or-ckpt-dir> [name=adapter ...]
#
# With no adapters it serves the model at its own path (use this for the local
# oat full-finetune checkpoints). With adapters it serves the base under
# `base` plus each LoRA under its given name, so one server can answer for
# several checkpoints and the eval only pays the model-load cost once.
set -euo pipefail

PORT="${1:?usage: serve_arena.sh <port> <gpu> <model> [name=adapter ...]}"
GPU="${2:?}"
MODEL="${3:?}"
shift 3

VENV="${ARENA_VENV:-/workspace/allie/venvs/spiral}"
source "$VENV/bin/activate"
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
[ -f "$SAT_HOME/.env" ] && { set -a; . "$SAT_HOME/.env"; set +a; }
export HF_HOME="${SAT_HF_HOME:-${HF_HOME:-$HOME/.cache/huggingface}}"
export CUDA_VISIBLE_DEVICES="$GPU"
export VLLM_NO_USAGE_STATS=1 DO_NOT_TRACK=1  # the volume is at 92%; the usage
# reporter writes to $HOME and its "Disk quota exceeded" traceback looks like a
# training failure while being pure telemetry.

ARGS=(
  --model "$MODEL"
  --served-model-name base
  --port "$PORT"
  --gpu-memory-utilization 0.85
  # Matches --max_model_len 12800 in training/run_kuhn_qwen3_8b.sh. The eval
  # must not admit a prompt the trained policy could never have seen.
  --max-model-len 12800
  --max-num-seqs 64
  --disable-log-requests
)

if [ "$#" -gt 0 ]; then
  # vLLM 0.8.4's V1 engine crashes on adapter activation:
  #   AttributeError: 'LoRALRUCache' object has no attribute '_LRUCache__update'
  # (vllm/lora/models.py activate_adapter -> utils.py LRUCache.touch). V0's LoRA
  # manager is fine, so pin V0 -- but only here, since the no-adapter path
  # (the local full-finetune checkpoints) is happier on V1.
  export VLLM_USE_V1=0
  ARGS+=(--enable-lora --max-lora-rank 64 --max-loras 4 --lora-modules "$@")
fi

exec python -m vllm.entrypoints.openai.api_server "${ARGS[@]}"
