#!/usr/bin/env bash
#SBATCH --job-name=mask-eval
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32
#SBATCH --time=12:00:00
#SBATCH --output=slurm-mask-%j.out
#SBATCH --error=slurm-mask-%j.out
# Usage: sbatch sbatch_mask.sh <arm-name> <model-path-or-hf-id>
set -euo pipefail
: "${SAT_HOME:?export SAT_HOME=/path/to/spiral-alignment-transfer before sbatch}"
source "$SAT_HOME/config.sh"
ARM="$1"; MODEL="$2"
WORK="$SAT_RUNS_DIR/$ARM"
PORT=8000   # node-local, so no cross-node collision

source "$SAT_VENV/bin/activate"
set -a; . "$SAT_ENV_FILE"; set +a
source "$SAT_HOME/node_env.sh"

# Per-arm copy of the harness: arms run concurrently and would otherwise race on
# csv_data/metrics/all_results.json.
rm -rf "$WORK"; mkdir -p "$(dirname "$WORK")"
cp -r "$MASK_HARNESS" "$WORK"
cd "$WORK"
# Purge inherited OUTPUTS while keeping the input dataset CSVs (csv_data/*.csv).
# The source tree has responses/ evaluated/ metrics/ populated from an earlier
# run, and evaluate.py globs responses/*.csv -- so without this each arm also
# re-judges the other model's stale responses, multiplying calls against a
# rate-limited judge and polluting all_results.json with another arm's rows.
rm -rf csv_data/responses csv_data/evaluated csv_data/metrics \
       test_csv_data/responses test_csv_data/evaluated test_csv_data/metrics
mkdir -p csv_data/responses csv_data/evaluated csv_data/metrics
echo "input datasets: $(ls csv_data/*.csv | wc -l)  stale outputs purged"

echo "node=$(hostname) arm=$ARM model=$MODEL"

# ---- serve the model under test on this node's GPU ----
python -m vllm.entrypoints.openai.api_server \
  --model "$MODEL" --served-model-name "$ARM" --port $PORT \
  --gpu-memory-utilization 0.85 --max-model-len 8192 --max-num-seqs 64 \
  --dtype bfloat16 --disable-log-requests > "$WORK/vllm.log" 2>&1 &
VLLM_PID=$!
trap 'kill -9 $VLLM_PID 2>/dev/null || true' EXIT
for i in $(seq 1 180); do
  curl -s "http://localhost:$PORT/v1/models" 2>/dev/null | grep -q "$ARM" && break
  kill -0 $VLLM_PID 2>/dev/null || { echo "FATAL: vllm died"; tail -30 "$WORK/vllm.log"; exit 1; }
  sleep 5
done
echo "server up"

V="$SAT_MASK_VENV/bin/python"
# Judge config. NOT gpt-4o: on this OpenRouter account gpt-4o is served only by
# Azure, which rejects MASK's lying/disinformation prompts with HTTP 400
# content_filter. MASK logs that as TIMEOUT_ERROR and silently drops the row,
# which cost 35.6% of judge calls on the first base run. gpt-4.1 is the nearest
# substitute that is reachable.
export MASK_JUDGE_BASE_URL=https://openrouter.ai/api/v1
export MASK_JUDGE_API_KEY="$OPENROUTER_API_KEY"
export MASK_JUDGE_MODEL="${MASK_JUDGE_MODEL}"
export MASK_JUDGE_STRUCTURED_MODEL="${MASK_JUDGE_MODEL}"
export MASK_JUDGE_ROW_TIMEOUT=300

echo "=== [1/4] generate ==="
OPENAI_BASE_URL="http://localhost:$PORT/v1" OPENAI_API_KEY=dummy-local \
  $V generate_responses.py --model "$ARM" --temperature 1.0 --lie_k 1
echo "=== [2/4] judge ==="
$V evaluate.py --concurrency_limit 8
echo "=== [3/4] metric ==="
$V metric.py
echo "=== [4/4] aggregate ==="
$V process_metrics.py
echo "=== MASK_DONE arm=$ARM ==="
