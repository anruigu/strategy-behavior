#!/usr/bin/env bash
# run_scaling_external.sh -- Tier-B (eval-suite transfer) for ONE ladder arm.
#
#   ./run_scaling_external.sh <arm-label> <tinker://...> <port>
#
# WHICH INSTRUMENTS, AND WHY ONLY THESE FOUR. The plan says to read only
# high-SNR y-axes at one seed, and names darkbench / sandbagging / in-context
# scheming as within-SE rows not to read a scaling claim off. That leaves the
# movers from results/eval_suite_transfer_27b.png:
#
#   MACHIAVELLI      +12.4 violations   (p<0.01, the largest and tightest)
#   insider-trading  +0.72 trade rate   (cheap: 40 samples)
#   AgentMisalignment +0.14 frac-any
#   hack-verifiable  +0.065 hack rate   (T1, the primary claim)
#
# hack-verifiable is LAST on purpose: at the 60-episodes/env setting that made it
# readable it costs ~100 min/arm, which does not multiply by 13 arms in one
# night. It runs only if the arm's other three finished and there is still time,
# so a partial night yields three complete rows rather than four partial ones.
#
# PARAMETERS ARE PINNED to the 0819/0820 frame-ablation settings so the base row
# and the published 27B numbers stay commensurable -- EXCEPT that the base model
# here is Qwen3.8-27B, not the 3.6 those figures used. The `base` arm of THIS
# ladder is therefore the only valid comparison point; do not read a ladder cell
# against a number from the 3.6 figure.
set -uo pipefail
LAB="${1:?arm label}"; MODEL="${2:?model}"; P="${3:-8700}"

set -a; . /workspace/allie/.env 2>/dev/null || true; set +a
export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
mkdir -p "$XDG_CACHE_HOME"

IPD=/workspace/allie/ipd_exp
EXT=/workspace/allie/evals_external
# Tier-B results land in the ESTABLISHED traits_results tree, not a new scaling
# directory: analyze_mach_n5.py resolves trajectories as
# traits_results/<arm>/machiavelli_traj_n<N> and every other aggregator in the
# repo assumes the same layout. Arm labels (`scale-game-n8-hole`) keep the
# ladder's rows distinct without a parallel directory tree that half the tooling
# would not know how to read.
OUT=/workspace/allie/ipd_exp/traits_results
TPY=/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python
LPY=/workspace/allie/venvs/spiral/bin/python
AMPY=/workspace/allie/eval_games/.venv/bin/python
CONC="${CONC:-16}"
DO_HV="${DO_HV:-0}"

arm_out="$OUT/$LAB"; mkdir -p "$arm_out"
echo "[tierB] arm=$LAB port=$P node=$(hostname) model=$MODEL"

pkill -f "tinker_openai_proxy.py --port $P" 2>/dev/null; sleep 2
setsid nohup "$TPY" "$IPD/tinker_openai_proxy.py" --port "$P" --arm "$LAB" \
  --model "$MODEL" --concurrency "$CONC" > "$arm_out/proxy.log" 2>&1 < /dev/null &
ready=0
for _ in $(seq 1 72); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' "http://localhost:$P/v1/models" 2>/dev/null)" = 200 ] \
    && { ready=1; break; }
  sleep 5
done
[ "$ready" = 1 ] || { echo "[tierB] FATAL proxy never came up for $LAB"; tail -20 "$arm_out/proxy.log"; exit 1; }
cleanup() { pkill -f "tinker_openai_proxy.py --port $P" 2>/dev/null || true; }
trap cleanup EXIT

run_one() {  # $1 sentinel  $2 log  $3 dir  $4 python  ...cmd
  local sent="$1" log="$2" dir="$3" py="$4"; shift 4
  if [ -e "$arm_out/$sent" ]; then echo "  [skip] $sent"; return 0; fi
  ( cd "$dir" && "$py" "$@" ) > "$arm_out/$log" 2>&1 \
    && echo "  [done] $sent" \
    || { echo "  [FAIL] $sent -- tail:"; tail -5 "$arm_out/$log" | sed 's/^/      /'; }
}

# Cheapest first, so a truncated night still produces complete rows.
run_one insider_trading.json insider.log "$EXT/insider-trading" "$LPY" \
  eval_insider.py "$LAB" "$P" --samples 40 --conc 16 --out "$OUT"
run_one machiavelli_traj_n3 mach.log "$IPD" "$LPY" \
  run_mach90.py --port "$P" --arm "$LAB" --episodes 3 --workers 8 \
  --out "$arm_out/machiavelli_traj_n3"
# --epochs 3 -> n=108, the sample size the frame-* arms used. At the default
# --epochs 1 the scenario set gives n=36, and frac_any_misaligned lands at
# SE ~0.083 on a base of 0.556 -- the effect this eval showed previously was
# +0.14, i.e. under 2 SE, which is not enough to read a SHAPE across four rungs.
# n=108 takes it to SE ~0.048 for about 16 extra minutes per arm.
run_one agentmisalignment.json am.log "$EXT/agentmisalignment" "$AMPY" \
  run_household.py "$LAB" "$P" --epochs 3 --conc "$CONC" --out "$OUT"

if [ "$DO_HV" = "1" ]; then
  run_one hack_verifiable.json hv.log "$EXT/hack-verifiable" "$LPY" \
    run_hv.py "$LAB" "$P" --episodes 60 --conc 20 --max-steps 30 --out "$OUT"
else
  echo "  [held] hack_verifiable (DO_HV=1 to run; ~100 min/arm)"
fi

echo "[tierB] $LAB COMPLETE"
ls "$arm_out" 2>/dev/null | tr '\n' ' '; echo
