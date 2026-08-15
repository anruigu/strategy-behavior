#!/usr/bin/env bash
# run_kuhn_marshal_tinker.sh -- MARSHAL Kuhn Poker self-play through the Tinker API.
#
#   ./run_kuhn_marshal_tinker.sh --scale smoke --dry-run   # free, offline
#   ./run_kuhn_marshal_tinker.sh --scale short             # 64 steps
#   ./run_kuhn_marshal_tinker.sh                           # full: 200 steps
#
# Extra args pass through to train_marshal_tinker.py.
set -euo pipefail
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/../../.." && pwd)}"
source "$SAT_HOME/config.sh"
cd "$(dirname "$0")"
source "$SAT_TINKER_VENV/bin/activate"
if [ -f "$SAT_ENV_FILE" ]; then set -a; . "$SAT_ENV_FILE"; set +a; fi
export HF_HOME="$SAT_HF_HOME"
export PYTHONUNBUFFERED=1

exec python train_marshal_tinker.py \
  --marshal-dir "${MARSHAL_DIR:-$SAT_HOME/../MARSHAL}" \
  --output-dir "${SAT_MARSHAL_TINKER_OUT:-$SAT_HOME/outputs/marshal-tinker}" \
  "$@"
