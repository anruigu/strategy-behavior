#!/usr/bin/env bash
set -euo pipefail
source /workspace/allie/venvs/spiral/bin/activate
set -a; . /workspace/allie/.env; set +a
export HF_HOME=/workspace/allie/.cache/huggingface
export CUDA_VISIBLE_DEVICES=6
exec python -m vllm.entrypoints.openai.api_server   --model "/home/allie/oat-output/spiral-qwen3-4b-base-kp-4k-self-play_0806T00:20:48/saved_models/step_00048"   --served-model-name spiral-step48   --port 8007   --gpu-memory-utilization 0.72   --num-gpu-blocks-override 2048   --max-model-len 8192 --max-num-seqs 4 --enforce-eager --disable-log-requests
