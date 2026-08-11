#!/usr/bin/env bash
# run_mask.sh <served-model-name> [--test]
set -euo pipefail
cd /workspace/allie/evals/mask/mask
MODEL="$1"; shift || true
set -a; . /workspace/allie/.env; set +a
# generation -> local vllm server; judge -> OpenRouter (OpenAI keys in .env and
# .bashrc are both 401).
export OPENAI_BASE_URL=http://localhost:8000/v1
export OPENAI_API_KEY=dummy-local
export MASK_JUDGE_BASE_URL=https://openrouter.ai/api/v1
export MASK_JUDGE_API_KEY="$OPENROUTER_API_KEY"
export MASK_JUDGE_MODEL=openai/gpt-4o
export MASK_JUDGE_STRUCTURED_MODEL=openai/gpt-4o
V=/workspace/allie/evals/mask/.venv/bin/python
echo "=== [1/4] generate ($MODEL) ==="; $V generate_responses.py --model "$MODEL" --temperature 1.0 --lie_k 1 "$@"
echo "=== [2/4] judge ==="; unset OPENAI_BASE_URL OPENAI_API_KEY; $V evaluate.py --concurrency_limit 10 "$@"
echo "=== [3/4] metric ==="; $V metric.py "$@"
echo "=== [4/4] aggregate ==="; $V process_metrics.py "$@"
echo "=== MASK_DONE $MODEL ==="
