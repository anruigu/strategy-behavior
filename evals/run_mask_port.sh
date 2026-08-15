#!/usr/bin/env bash
set -euo pipefail
: "${MASK_DIR:=/workspace/allie/mask}"   # canonical MASK checkout (github.com/centerforaisafety/mask)
cd "$MASK_DIR/mask"
MODEL="$1"; PORT="$2"; shift 2
set -a; . /workspace/allie/.env; set +a
export PYTHONUNBUFFERED=1
export OPENAI_BASE_URL="http://localhost:$PORT/v1"
export OPENAI_API_KEY=dummy-local
export MASK_JUDGE_BASE_URL=https://openrouter.ai/api/v1
export MASK_JUDGE_API_KEY="$OPENROUTER_API_KEY"
export MASK_JUDGE_MODEL=openai/gpt-4o
export MASK_JUDGE_STRUCTURED_MODEL=openai/gpt-4o
V="$MASK_DIR/.venv/bin/python"
echo "=== [1/4] generate ($MODEL @ $PORT) ==="; $V generate_responses.py --model "$MODEL" --temperature 1.0 --lie_k 1 "$@"
echo "=== [2/4] judge ==="; unset OPENAI_BASE_URL OPENAI_API_KEY; $V evaluate.py --concurrency_limit 10 "$@"
echo "=== [3/4] metric ==="; $V metric.py "$@"
echo "=== [4/4] aggregate ==="; $V process_metrics.py "$@"
echo "=== MASK_DONE $MODEL ==="
