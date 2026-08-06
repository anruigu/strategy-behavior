#!/usr/bin/env bash
set -euo pipefail
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
source "$SAT_HOME/config.sh"
source "$SAT_VENV/bin/activate"
set -a; . "$SAT_ENV_FILE"; set +a
export HF_HOME="$SAT_HF_HOME"
MODEL="${1:?usage: serve_ckpt.sh <checkpoint-path> [served-name] [port] [gpu]}"
NAME="${2:-spiral-ckpt}"
PORT="${3:-8000}"
GPU="${4:-0}"
export CUDA_VISIBLE_DEVICES="$GPU"
# gpu-memory-utilization is a ceiling on TOTAL card usage (all processes), and
# training already holds ~0.58 of it -- hence 0.72, not 0.15.
# num-gpu-blocks-override HARD-CAPS the KV cache at 2048*16 tokens = 4.5GiB, so
# the footprint is ~14GB no matter whether --vllm_sleep has the training actors
# offloaded (20GB) or awake (84GB) at init time. Without it vllm would greedily
# size KV against transiently-free memory and OOM training when actors wake.
exec python -m vllm.entrypoints.openai.api_server \
  --model "$MODEL" \
  --served-model-name "$NAME" \
  --port "$PORT" \
  --gpu-memory-utilization 0.72 \
  --num-gpu-blocks-override 2048 \
  --max-model-len 8192 \
  --max-num-seqs 4 \
  --enforce-eager \
  --disable-log-requests
