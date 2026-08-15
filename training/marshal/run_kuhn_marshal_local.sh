#!/usr/bin/env bash
# run_kuhn_marshal_local.sh -- MARSHAL Kuhn Poker self-play locally, via ROLL.
#
# Reproduces examples/kuhn_poker/run_agentic_pipeline_kuhn_poker_selfplay.sh with
# three deliberate changes, all carried by
# agentic_val_kuhn_poker_selfplay_local.yaml (copied into $MARSHAL_DIR):
#
#  1. megatron_train -> deepspeed_train (+ ${deepspeed_zero2}). Megatron is the
#     only reason ROLL's install is hard -- it needs mcore_adapter and
#     transformer-engine, both CUDA builds. deepspeed_train is a first-class
#     strategy in roll/distributed/strategy/factory.py (imported lazily, so
#     Megatron is never touched), and examples/tictactoe/agentic_val_tictactoe_gae.yaml
#     drives this same agentic pipeline with it. The RL algorithm is unchanged;
#     only the parallelism backend differs.
#  2. 4 GPUs instead of 8, since 0-3 are occupied. vllm gpu_memory_utilization
#     0.8 -> 0.5 so ZeRO-2 optimiser state fits alongside vLLM on a collocated
#     card.
#  3. The authors' hardcoded /mnt/public/... paths become $MARSHAL_OUT, and
#     USE_MODELSCOPE is turned off (we resolve weights from HF).
#
# Usage:
#   MARSHAL_GPUS=4,5,6,7 ./run_kuhn_marshal_local.sh
set -euo pipefail
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/../.." && pwd)}"
source "$SAT_HOME/config.sh"

: "${MARSHAL_DIR:=/workspace/allie/MARSHAL}"
: "${MARSHAL_VENV:=/workspace/allie/venvs/marshal}"
: "${MARSHAL_PRETRAIN:=Qwen/Qwen3-4B}"
: "${MARSHAL_GPUS:=4,5,6,7}"
: "${MARSHAL_OUT:=/workspace/allie/marshal-output-kuhn}"
export MARSHAL_PRETRAIN MARSHAL_OUT

cp "$SAT_HOME/training/marshal/agentic_val_kuhn_poker_selfplay_local.yaml" \
   "$MARSHAL_DIR/examples/kuhn_poker/"

source "$MARSHAL_VENV/bin/activate"
if [ -f "$SAT_ENV_FILE" ]; then set -a; . "$SAT_ENV_FILE"; set +a; fi
export HF_HOME="$SAT_HF_HOME"
export PYTHONUNBUFFERED=1
export CUDA_VISIBLE_DEVICES="$MARSHAL_GPUS"
export PYTHONPATH="$MARSHAL_DIR:${PYTHONPATH:-}"
mkdir -p "$MARSHAL_OUT"

cd "$MARSHAL_DIR"
ray stop >/dev/null 2>&1 || true

echo "python   = $(command -v python)"
echo "GPUs     = $CUDA_VISIBLE_DEVICES"
echo "pretrain = $MARSHAL_PRETRAIN"
echo "out      = $MARSHAL_OUT"

exec python examples/start_agentic_pipeline.py \
  --config_path kuhn_poker \
  --config_name agentic_val_kuhn_poker_selfplay_local
