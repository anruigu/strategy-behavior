#!/usr/bin/env bash
#SBATCH --job-name=phishing
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32
#SBATCH --time=10:00:00
#SBATCH --output=/workspace/allie/evals/slurm-phish-%j.out
#SBATCH --error=/workspace/allie/evals/slurm-phish-%j.out
# Usage: sbatch sbatch_phishing.sh <arm-name> <model-path-or-hf-id> [num-test-cases]
#
# CyberSecEval 3 multiturn spear-phishing (Meta PurpleLlama). The model under
# test plays the attacker against a judge-LLM victim over several turns; a judge
# scores how far it moved the victim toward the stated goal. Measures persuasive
# capability, which is what we want to compare across training arms.
set -euo pipefail
ARM="$1"; MODEL="$2"; N="${3:-250}"
PORT=8000
PL=/workspace/allie/evals/PurpleLlama/CybersecurityBenchmarks
OUT=/workspace/allie/evals/phishing/$ARM
mkdir -p "$OUT"

source /workspace/allie/venvs/spiral/bin/activate
set -a; . /workspace/allie/.env; set +a
source /workspace/allie/evals/node_env.sh

cleanup() {
    kill -- "-${VLLM_PID:-0}" 2>/dev/null || true
    kill -9 "${VLLM_PID:-0}" 2>/dev/null || true
    sleep 3
    for p in $(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null); do
        [ "$(stat -c %u /proc/"$p" 2>/dev/null)" = "$(id -u)" ] && kill -9 "$p" 2>/dev/null || true
    done
}
trap cleanup EXIT INT TERM

# A stale API server from a previous job can hold $PORT with a dead engine; it
# still answers /v1/models so a naive readiness probe passes while every real
# request 404s. Clear ours, abort if someone else's.
if ss -tln 2>/dev/null | grep -q ":$PORT "; then
    echo "WARN: port $PORT in use on $(hostname); clearing our stale servers"
    for q in $(pgrep -u "$(id -u)" -f "vllm.entrypoints" 2>/dev/null); do kill -9 "$q" 2>/dev/null || true; done
    sleep 5
    ss -tln 2>/dev/null | grep -q ":$PORT " && { echo "FATAL: port $PORT still held"; exit 1; }
fi

echo "node=$(hostname) arm=$ARM model=$MODEL cases=$N"
setsid python -m vllm.entrypoints.openai.api_server \
  --model "$MODEL" --served-model-name "$ARM" --port $PORT \
  --gpu-memory-utilization 0.85 --max-model-len 8192 --max-num-seqs 32 \
  --dtype bfloat16 --disable-log-requests \
  > /workspace/allie/evals/vllm-phish-$ARM.log 2>&1 &
VLLM_PID=$!
READY=0
for i in $(seq 1 240); do
  if curl -s "http://localhost:$PORT/v1/models" 2>/dev/null | grep -q "$ARM"; then READY=1; break; fi
  kill -0 $VLLM_PID 2>/dev/null || { echo "FATAL: vllm died"; tail -40 /workspace/allie/evals/vllm-phish-$ARM.log; exit 1; }
  sleep 5
done
[ "$READY" = "1" ] || { echo "FATAL: vllm not ready"; tail -40 /workspace/allie/evals/vllm-phish-$ARM.log; exit 1; }
echo "server up after $((i*5))s"

# Judge/victim on OpenRouter. gpt-4o is unreachable on this account (Azure-only,
# and its content filter rejects adversarial prompts), so gpt-4.1 as elsewhere.
JUDGE="OPENAI::openai/gpt-4.1::${OPENROUTER_API_KEY}::https://openrouter.ai/api/v1"
UNDER="OPENAI::${ARM}::local::http://localhost:${PORT}/v1"

cd /workspace/allie/evals/PurpleLlama
./CybersecurityBenchmarks/.venv/bin/python -m CybersecurityBenchmarks.benchmark.run \
   --benchmark=multiturn-phishing \
   --prompt-path="$PL/datasets/spear_phishing/multiturn_phishing_challenges.json" \
   --response-path="$OUT/responses.json" \
   --judge-response-path="$OUT/judge_responses.json" \
   --stat-path="$OUT/stats.json" \
   --judge-llm="$JUDGE" \
   --llm-under-test="$UNDER" \
   --run-llm-in-parallel \
   --num-test-cases="$N"

echo "=== PHISHING_DONE arm=$ARM ==="
