#!/usr/bin/env bash
#SBATCH --job-name=trait
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32
#SBATCH --time=08:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/evals/slurm-trait-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/evals/slurm-trait-%j.out
# Usage: sbatch sbatch_rewardhacks.sh <arm-name> <model-path-or-hf-id> [--limit N]
set -euo pipefail
ARM="$1"; MODEL="$2"; shift 2
PORT=8000   # node-local

: "${SAT_HOME:=/workspace/allie/strategy-behavior}"   # repo root; override to relocate
: "${SAT_VENV:=/workspace/allie/venvs/spiral}"        # serving/eval venv (openai + pandas)

source "$SAT_VENV/bin/activate"
set -a; . /workspace/allie/.env; set +a
source "$SAT_HOME/evals/node_env.sh"

# vllm engine workers are multiprocessing forks: killing only the api_server
# parent reparents them to init where they keep the GPU reservation and OOM the
# next job scheduled here. Kill the group, then sweep our own GPU pids.
cleanup() {
    kill -- "-${VLLM_PID:-0}" 2>/dev/null || true
    kill -9 "${VLLM_PID:-0}" 2>/dev/null || true
    sleep 3
    for p in $(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null); do
        [ "$(stat -c %u /proc/"$p" 2>/dev/null)" = "$(id -u)" ] && kill -9 "$p" 2>/dev/null || true
    done
}
trap cleanup EXIT INT TERM

echo "node=$(hostname) arm=$ARM model=$MODEL"
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
  --dtype bfloat16 --disable-log-requests > "$SAT_HOME/evals/vllm-trait-$ARM.log" 2>&1 &
VLLM_PID=$!
READY=0
for i in $(seq 1 240); do
  if curl -s "http://localhost:$PORT/v1/models" 2>/dev/null | grep -q "$ARM"; then READY=1; break; fi
  kill -0 $VLLM_PID 2>/dev/null || { echo "FATAL: vllm died after $((i*5))s"; tail -40 "$SAT_HOME/evals/vllm-trait-$ARM.log"; exit 1; }
  sleep 5
done
# Do NOT fall through when the server never came up: the eval would still run and
# every request would 404, producing a full set of plausible-looking but empty
# results. One earlier run scored 15/80 items this way and reported 100.0 on
# every trait.
[ "$READY" = "1" ] || { echo "FATAL: vllm not ready after 1200s"; tail -40 "$SAT_HOME/evals/vllm-trait-$ARM.log"; exit 1; }
echo "server up after $((i*5))s"


# Client only needs openai + pandas, both present in $SAT_VENV (the spiral venv).
# NOT `exec`: exec replaces this shell, which discards the EXIT trap above and
# leaves the vllm engine workers alive holding ~119GB of the node's GPU.
"$SAT_VENV/bin/python" \
     "$SAT_HOME/evals/trait/run_trait.py" "$ARM" "$PORT" "$@"
