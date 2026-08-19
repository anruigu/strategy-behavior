#!/usr/bin/env bash
# run_mask_port.sh <served-model-name> <vllm-port> [--test]
set -euo pipefail
: "${MASK_DIR:=/workspace/allie/mask}"   # canonical MASK checkout (github.com/centerforaisafety/mask)
cd "$MASK_DIR/mask"
MODEL="$1"; PORT="$2"; shift 2
set -a; . /workspace/allie/.env; set +a
export PYTHONUNBUFFERED=1
export OPENAI_BASE_URL="http://localhost:$PORT/v1"
export OPENAI_API_KEY=dummy-local
export MASK_JUDGE_BASE_URL="${MASK_JUDGE_BASE_URL:-https://openrouter.ai/api/v1}"
export MASK_JUDGE_API_KEY="${MASK_JUDGE_API_KEY:-$OPENROUTER_API_KEY}"
# gpt-4o keeps the arms already in test_csv_data/ comparable. On this OpenRouter
# account it is served only by Azure, which intermittently 400s MASK's
# lying/disinformation prompts with content_filter -- evaluate.py retries those.
# sbatch_mask.sh uses openai/gpt-4.1 instead; set MASK_JUDGE_MODEL to match if
# you are starting a fresh set of arms.
export MASK_JUDGE_MODEL="${MASK_JUDGE_MODEL:-openai/gpt-4o}"
export MASK_JUDGE_STRUCTURED_MODEL="${MASK_JUDGE_STRUCTURED_MODEL:-$MASK_JUDGE_MODEL}"
# Azure permanently content-filters a few MASK transcripts; those cells would
# otherwise reach metric.py as "no belief" and score as honest. gpt-4.1 is the
# reachable non-Azure substitute (same choice sbatch_mask.sh makes), and
# evaluate.py prints how many cells it had to answer.
export MASK_JUDGE_FALLBACK_MODEL="${MASK_JUDGE_FALLBACK_MODEL:-openai/gpt-4.1}"
# Requests in flight against the judge, process-wide. The upstream pool throttles
# well below what --concurrency_limit rows x ~5 calls per row would otherwise
# fire; see evaluate.py.
export MASK_JUDGE_CONCURRENCY="${MASK_JUDGE_CONCURRENCY:-8}"
V="$MASK_DIR/.venv/bin/python"

echo "=== [1/4] generate ($MODEL @ $PORT) ==="; $V generate_responses.py --model "$MODEL" --temperature 1.0 --lie_k 1 "$@"

# The judge is scoped to this model's files and must fill every cell: an
# unanswered cell reaches metric.py as "no belief" and scores as honest, so a
# throttled judge quietly inflates the honesty score instead of failing.
echo "=== [2/4] judge ==="; unset OPENAI_BASE_URL OPENAI_API_KEY
$V evaluate.py --concurrency_limit 10 --only "$MODEL" "$@" || echo "--- judge pass left unanswered cells; repairing ---"
JUDGE_OK=0
for attempt in 1 2 3; do
  if $V evaluate.py --repair --concurrency_limit 10 --only "$MODEL" "$@"; then JUDGE_OK=1; break; fi
  echo "--- repair pass $attempt still left unanswered cells; retrying in 60s ---"; sleep 60
done
[ "$JUDGE_OK" = 1 ] || { echo "MASK judge incomplete for $MODEL; refusing to compute metrics" >&2; exit 1; }

echo "=== [3/4] metric ==="; $V metric.py "$@"
echo "=== [4/4] aggregate ==="; $V process_metrics.py "$@"
echo "=== MASK_DONE $MODEL ==="
