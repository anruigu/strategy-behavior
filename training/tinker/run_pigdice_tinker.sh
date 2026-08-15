#!/usr/bin/env bash
# run_pigdice_tinker.sh -- PigDice control arm, Tinker port of ../run_pigdice.sh.
#
# Two things carry over from the oat script and matter more here, not less:
#
#  1. PigDice REQUIRES the LLM observation wrapper (the arm preset in config.py
#     sets it). Under FirstLast the player cannot see its own turn total and
#     every roll/hold decision is blind -- and it fails silently, with the win
#     rate just sitting at chance. On Tinker you would pay for the whole run
#     before noticing.
#  2. PigDice episodes are ~5x longer than the other arms' (~50-60 model calls
#     vs ~9-20). Since Tinker bills per sampled token, this arm costs several
#     times what the kuhn arm costs for the same --turns-per-step. It is also
#     the arm most likely to hit --max-turns 50 and score draws; watch
#     outcome/turn_limit in the step log.
#
# It also needs the PigDice action-parser patch applied to $SPIRAL_DIR:
#   git -C "$SPIRAL_DIR" apply "$SAT_HOME/training/patches/action-parsers.patch"
# train_tinker.py checks for the parser at startup and exits with that command
# if it is missing, before creating any Tinker client.
set -euo pipefail
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/../.." && pwd)}"
source "$SAT_HOME/config.sh"
cd "$(dirname "$0")"
source "$SAT_TINKER_VENV/bin/activate"
if [ -f "$SAT_ENV_FILE" ]; then set -a; . "$SAT_ENV_FILE"; set +a; fi
export HF_HOME="$SAT_HF_HOME"
export PYTHONUNBUFFERED=1

exec python train_tinker.py \
  --arm pigdice \
  --scale full \
  --spiral-dir "$SPIRAL_DIR" \
  --output-dir "$SAT_TINKER_OUT" \
  --run-name spiral-tinker-pigdice-control \
  "$@"
