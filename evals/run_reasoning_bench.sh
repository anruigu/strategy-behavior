#!/usr/bin/env bash
# run_reasoning_bench.sh -- SPIRAL's reported reasoning benchmarks, locally.
#
#   run_reasoning_bench.sh <model-path-or-hf-id> [out-label]
#
# Runs the same offline benchmark suite SPIRAL reports in its paper, with
# SPIRAL's own hyperparameters, so a checkpoint from ../training/ can be
# compared against the base model on equal terms:
#
#   math (evals/benchmarks/math-evaluation-harness, data vendored in the
#   spiral checkout, no network needed):
#     math500, aime24, aime25, olympiadbench, amc23, minerva_math
#     prompt_type qwen3-self-play, n_sampling 4, temperature 0.6, top_p 0.95,
#     max_tokens_per_call 8192, seed 0  -- all straight from spiral's sh/eval.sh
#
#   general reasoning (evals/benchmarks/simple-evals, fetched at runtime):
#     gpqa (diamond, 198q), knowlogic (5400q), mmlu_pro (12032q)
#     served through a local vLLM OpenAI endpoint, max_tokens 8192
#
# WHY THIS EXISTS rather than calling spiral's evals/benchmarks/eval.sh:
#   * That script's last step uploads to wandb org "stlm" / project
#     "oat-game-eval" -- SPIRAL's own org, which we cannot write to. It runs
#     under `set -e`, so the upload failure would discard the run. We collect
#     to CSV locally instead and leave wandb out.
#   * It hardcodes CUDA_VISIBLE_DEVICES=4,5 and SERVER_PORT=7000, both of which
#     collide with anything else on the box.
#
# VENV: uses $SAT_BENCH_VENV, NOT $SAT_VENV. The math harness needs
# latex2sympy2 + antlr4-python3-runtime==4.11.1, but spiral itself pins
# antlr4==4.13.2; installing the harness deps into the training venv would
# change dependencies out from under any in-flight training job. The bench venv
# is an OVERLAY -- a bare venv whose site-packages holds only the harness deps,
# with a .pth appending the training venv's site-packages for torch/vllm. So it
# reuses the ~10GB install without being able to write to it. Create with:
#
#   python3.10 -m venv "$SAT_BENCH_VENV"
#   echo "$SAT_VENV/lib/python3.10/site-packages" \
#     > "$SAT_BENCH_VENV/lib/python3.10/site-packages/zz-spiral-base.pth"
#   source "$SAT_BENCH_VENV/bin/activate"
#   pip install word2number Pebble timeout-decorator antlr4-python3-runtime==4.11.1 blobfile
#   pip install --no-deps "$SPIRAL_DIR/evals/benchmarks/math-evaluation-harness/latex2sympy"
set -uo pipefail
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
source "$SAT_HOME/config.sh"

MODEL="${1:?usage: run_reasoning_bench.sh <model-path-or-hf-id> [out-label]}"
LABEL="${2:-$(basename "$MODEL")}"
: "${SAT_BENCH_VENV:=$HOME/venvs/spiral-bench}"
: "${BENCH_GPUS:=0,1,2,3}"          # tensor_parallel_size == number of GPUs listed
: "${BENCH_PORT:=7731}"             # not spiral's 7000; avoid colliding with serve_ckpt.sh
: "${BENCH_OUT:=$SAT_HOME/results/reasoning/$LABEL}"
: "${BENCH_SUITES:=math general}"   # drop one to run only the other

BENCH_DIR="$SPIRAL_DIR/evals/benchmarks"
[ -d "$BENCH_DIR" ] || { echo "no $BENCH_DIR -- is SPIRAL_DIR right?"; exit 1; }
mkdir -p "$BENCH_OUT"

source "$SAT_BENCH_VENV/bin/activate"
export HF_HOME="$SAT_HF_HOME"
export CUDA_VISIBLE_DEVICES="$BENCH_GPUS"
export TOKENIZERS_PARALLELISM=false

log() { echo "[bench $LABEL $(date -u +%H:%M:%S)] $*"; }
log "model=$MODEL gpus=$BENCH_GPUS out=$BENCH_OUT suites=$BENCH_SUITES"

# --- math suite -------------------------------------------------------------
if [[ " $BENCH_SUITES " == *" math "* ]]; then
    log "math suite: math500,aime24,aime25,olympiadbench,amc23,minerva_math"
    cd "$BENCH_DIR/math-evaluation-harness" || exit 1
    python3 -u math_eval.py \
        --model_name_or_path "$MODEL" \
        --data_name "math500,aime24,aime25,olympiadbench,amc23,minerva_math" \
        --output_dir "$BENCH_OUT/math" \
        --split test \
        --prompt_type qwen3-self-play \
        --num_test_sample -1 \
        --max_tokens_per_call 8192 \
        --seed 0 \
        --temperature 0.6 \
        --n_sampling 4 \
        --top_p 0.95 \
        --start 0 --end -1 \
        --use_vllm --save_outputs --overwrite
    rc=$?
    log "math suite exited rc=$rc"
    python3 sh/collect_results.py \
        --base_dir "$BENCH_OUT/math" \
        --model_name "$MODEL" \
        --output_path "$BENCH_OUT/math/metrics.csv" \
        --benchmarks "math500,aime24,aime25,olympiadbench,amc23,minerva_math" \
        && log "wrote $BENCH_OUT/math/metrics.csv"
fi

# --- general reasoning suite ------------------------------------------------
if [[ " $BENCH_SUITES " == *" general "* ]]; then
    cd "$BENCH_DIR" || exit 1
    log "starting vLLM server on :$BENCH_PORT (tp=$(echo "$BENCH_GPUS" | tr ',' '\n' | wc -l))"
    TP=$(echo "$BENCH_GPUS" | tr ',' '\n' | wc -l)
    # `python -m ...`, not the `vllm serve` console script: $SAT_BENCH_VENV is an
    # overlay that puts $SAT_VENV's site-packages on sys.path via a .pth, which
    # makes vllm importable but does NOT put $SAT_VENV/bin on $PATH -- so
    # `vllm serve` is command-not-found here even though `import vllm` works.
    python -m vllm.entrypoints.openai.api_server --model "$MODEL" \
        --port "$BENCH_PORT" --tensor-parallel-size "$TP" \
        --max-model-len 16384 --enable-prefix-caching --dtype bfloat16 \
        > "$BENCH_OUT/vllm-server.log" 2>&1 &
    SERVER_PID=$!
    # Kill the server on any exit path, including the math suite's failure above.
    trap 'kill $SERVER_PID 2>/dev/null; wait $SERVER_PID 2>/dev/null' EXIT

    log "waiting for server..."
    for i in $(seq 1 180); do
        curl -sf "http://127.0.0.1:$BENCH_PORT/v1/models" >/dev/null && break
        kill -0 $SERVER_PID 2>/dev/null || { log "server died -- see $BENCH_OUT/vllm-server.log"; exit 1; }
        sleep 5
    done
    curl -sf "http://127.0.0.1:$BENCH_PORT/v1/models" >/dev/null \
        || { log "server never came up"; exit 1; }
    log "server up"

    python -m simple-evals.simple_evals \
        --model_name_or_path "$MODEL" \
        --base_url "http://127.0.0.1:$BENCH_PORT/v1" \
        --max_tokens 8192 \
        --tasks gpqa knowlogic mmlu_pro \
        --output_path "$BENCH_OUT/general-metrics.csv"
    log "general suite exited rc=$?"
fi

log "done -- results under $BENCH_OUT"
