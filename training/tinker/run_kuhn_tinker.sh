#!/usr/bin/env bash
# run_kuhn_tinker.sh -- KuhnPoker-only self-play, Tinker port of ../run_kuhn.sh.
#
# Unlike the oat scripts, this one does NOT get copied into $SPIRAL_DIR: it runs
# from this directory and imports spiral from $SPIRAL_DIR via sys.path, so the
# GPU half of spiral's dependency set (oat/vllm/deepspeed) is never installed.
#
#   export TINKER_API_KEY=...           # or put it in $SAT_ENV_FILE
#   ./run_kuhn_tinker.sh                # full scale (400 steps)
#   ./run_kuhn_tinker.sh --scale smoke --dry-run   # free, offline, ~1 minute
#
# Any extra args are passed through to train_tinker.py, so
# `./run_kuhn_tinker.sh --scale short --model Qwen/Qwen3.5-4B` works.
set -euo pipefail
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/../.." && pwd)}"
source "$SAT_HOME/config.sh"
cd "$(dirname "$0")"
source "$SAT_TINKER_VENV/bin/activate"
# TINKER_API_KEY (and optionally WANDB_API_KEY) live here alongside the other
# secrets; harmless if the file is absent, unlike the oat path this arm needs no
# OpenRouter key at all.
if [ -f "$SAT_ENV_FILE" ]; then set -a; . "$SAT_ENV_FILE"; set +a; fi
export HF_HOME="$SAT_HF_HOME"
export PYTHONUNBUFFERED=1

exec python train_tinker.py \
  --arm kuhn \
  --scale full \
  --spiral-dir "$SPIRAL_DIR" \
  --output-dir "$SAT_TINKER_OUT" \
  --run-name spiral-tinker-kp-self-play \
  "$@"
