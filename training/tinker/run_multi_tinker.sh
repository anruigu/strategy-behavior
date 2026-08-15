#!/usr/bin/env bash
# run_multi_tinker.sh -- TicTacToe + KuhnPoker + SimpleNegotiation, Tinker port
# of ../run_multi.sh. See run_kuhn_tinker.sh for the usage notes; they are the
# same script with a different --arm.
#
# Note SimpleNegotiation-v1 has no enumerable action space, so its actions go
# through extract_chat_action() (a bare \boxed{} check) rather than the strict
# action-space match the other two use -- an unparseable action still forfeits,
# but a *legal-looking* one is never rejected. Expect a lower invalid-action
# rate on this arm that does not mean the policy is playing better.
set -euo pipefail
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/../.." && pwd)}"
source "$SAT_HOME/config.sh"
cd "$(dirname "$0")"
source "$SAT_TINKER_VENV/bin/activate"
if [ -f "$SAT_ENV_FILE" ]; then set -a; . "$SAT_ENV_FILE"; set +a; fi
export HF_HOME="$SAT_HF_HOME"
export PYTHONUNBUFFERED=1

exec python train_tinker.py \
  --arm multi \
  --scale full \
  --spiral-dir "$SPIRAL_DIR" \
  --output-dir "$SAT_TINKER_OUT" \
  --run-name spiral-tinker-multi-self-play \
  "$@"
