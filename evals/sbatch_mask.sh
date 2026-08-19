#!/usr/bin/env bash
#SBATCH --job-name=mask-eval
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32
#SBATCH --time=12:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/evals/slurm-mask-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/evals/slurm-mask-%j.out
# Usage: sbatch sbatch_mask.sh <arm-name> <model-path-or-hf-id>
set -euo pipefail
ARM="$1"; MODEL="$2"
: "${SAT_HOME:=/workspace/allie/strategy-behavior}"   # repo root; override to relocate
: "${SAT_VENV:=/workspace/allie/venvs/spiral}"        # serving venv
: "${MASK_DIR:=/workspace/allie/mask}"                # canonical MASK checkout
WORK="$SAT_HOME/results/runs/$ARM"
PORT=8000   # node-local, so no cross-node collision

source "$SAT_VENV/bin/activate"
set -a; . /workspace/allie/.env; set +a
source "$SAT_HOME/evals/node_env.sh"

# Per-arm copy of the harness: arms run concurrently and would otherwise race on
# csv_data/metrics/all_results.json.
rm -rf "$WORK"; mkdir -p "$(dirname "$WORK")"
cp -r "$MASK_DIR/mask" "$WORK"
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
# setsid: make the server a process-group leader (PGID == PID) so the
# `kill -- -$VLLM_PID` in cleanup_vllm reaches its forked engine workers.
# Background jobs in a non-interactive script otherwise share the script's PGID.
# PREFLIGHT PORT CHECK. A previous job on this node can leave an API server
# squatting $PORT with a DEAD engine (an `exec`-ed script skips its cleanup
# trap). The new server then cannot bind, while the corpse still answers
# /v1/models -- so the readiness probe passes and every completion returns
# 404 "model does not exist". That silently cost three full eval arms.
if ss -tln 2>/dev/null | grep -q ":$PORT "; then
    echo "WARN: port $PORT already in use on $(hostname); clearing our stale servers"
    for q in $(pgrep -u "$(id -u)" -f "vllm.entrypoints" 2>/dev/null); do kill -9 "$q" 2>/dev/null || true; done
    sleep 5
    ss -tln 2>/dev/null | grep -q ":$PORT " && { echo "FATAL: port $PORT still held by another user; aborting"; exit 1; }
fi
setsid python -m vllm.entrypoints.openai.api_server \
  --model "$MODEL" --served-model-name "$ARM" --port $PORT \
  --gpu-memory-utilization 0.85 --max-model-len 8192 --max-num-seqs 64 \
  --dtype bfloat16 --disable-log-requests > "$WORK/vllm.log" 2>&1 &
VLLM_PID=$!
# Kill the whole process GROUP, not just the api_server pid. vllm spawns its
# engine workers via multiprocessing-fork; killing only the parent reparents
# them to init and they keep holding their GPU reservation. One such orphan
# from a finished eval job sat on 122GB of node-2 and OOM-killed the next
# training job that slurm scheduled there ~8h later.
cleanup_vllm() {
    kill -- "-$VLLM_PID" 2>/dev/null || true   # process group
    kill -9 "$VLLM_PID" 2>/dev/null || true
    sleep 3
    # Belt and braces: any of our python procs still holding this node's GPUs.
    for p in $(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null); do
        [ "$(stat -c %u /proc/"$p" 2>/dev/null)" = "$(id -u)" ] && kill -9 "$p" 2>/dev/null || true
    done
}
trap cleanup_vllm EXIT INT TERM
READY=0
for i in $(seq 1 240); do
  if curl -s "http://localhost:$PORT/v1/models" 2>/dev/null | grep -q "$ARM"; then READY=1; break; fi
  kill -0 $VLLM_PID 2>/dev/null || { echo "FATAL: vllm died after $((i*5))s"; tail -40 "$WORK/vllm.log"; exit 1; }
  sleep 5
done
# Do NOT fall through when the server never came up: the eval would still run and
# every request would 404, producing a full set of plausible-looking but empty
# results. One earlier run scored 15/80 items this way and reported 100.0 on
# every trait.
[ "$READY" = "1" ] || { echo "FATAL: vllm not ready after 1200s"; tail -40 "$WORK/vllm.log"; exit 1; }
echo "server up after $((i*5))s"

V="$MASK_DIR/.venv/bin/python"
# Judge config. NOT gpt-4o: on this OpenRouter account gpt-4o is served only by
# Azure, which rejects MASK's lying/disinformation prompts with HTTP 400
# content_filter. MASK logs that as TIMEOUT_ERROR and silently drops the row,
# which cost 35.6% of judge calls on the first base run. gpt-4.1 is the nearest
# substitute that is reachable.
export MASK_JUDGE_BASE_URL=https://openrouter.ai/api/v1
export MASK_JUDGE_API_KEY="$OPENROUTER_API_KEY"
export MASK_JUDGE_MODEL=openai/gpt-4.1
export MASK_JUDGE_STRUCTURED_MODEL=openai/gpt-4.1
export MASK_JUDGE_ROW_TIMEOUT=300
export MASK_JUDGE_CONCURRENCY="${MASK_JUDGE_CONCURRENCY:-8}"   # requests in flight

echo "=== [1/4] generate ==="
OPENAI_BASE_URL="http://localhost:$PORT/v1" OPENAI_API_KEY=dummy-local \
  $V generate_responses.py --model "$ARM" --temperature 1.0 --lie_k 1
# Every cell has to carry a verdict: metric.py reads an unanswered one as "no
# belief" and scores it as honest, so a throttled judge inflates the honesty
# score rather than failing.
echo "=== [2/4] judge ==="
$V evaluate.py --concurrency_limit 8 || echo "--- judge pass left unanswered cells; repairing ---"
JUDGE_OK=0
for attempt in 1 2 3; do
  if $V evaluate.py --repair --concurrency_limit 8; then JUDGE_OK=1; break; fi
  echo "--- repair pass $attempt still left unanswered cells; retrying in 60s ---"; sleep 60
done
[ "$JUDGE_OK" = 1 ] || { echo "MASK judge incomplete for $ARM; refusing to compute metrics" >&2; exit 1; }
echo "=== [3/4] metric ==="
$V metric.py
echo "=== [4/4] aggregate ==="
$V process_metrics.py
echo "=== MASK_DONE arm=$ARM ==="
