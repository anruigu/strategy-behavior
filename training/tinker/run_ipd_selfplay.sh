#!/usr/bin/env bash
# run_ipd_selfplay.sh -- the self-play ablation for the exploitation-transfer POC.
#
# Plan 0808 §1.2 keeps the PRIMARY arms on a fixed opponent and calls for
# self-play "only as an ablation to demonstrate the erosion": with the victim
# learning to resist, the exploitation gradient should decay. This is that arm.
#
# Why spiral rather than ipd_exp/train_ipd.py: with a fixed opponent only one
# seat is ever trained, so GRPO's group baseline suffices (results §1 note (a)).
# In self-play BOTH seats are trained, which is exactly the case SPIRAL's
# role-conditioned advantage baseline (RAE) exists for.
#
# Three things are pinned so this arm is comparable to T1/A2 rather than merely
# adjacent to them:
#
#  1. PYTHONPATH puts /workspace/allie/TextArena FIRST. The venv ships
#     textarena 0.6.4, whose IPD FORFEITS a decision that contains no bracketed
#     token; the POC's checkout scores it as cooperate. The step-90 policy emits
#     no-token decisions ~22% of the time (results §8a), so under 0.6.4 roughly
#     one game in five would end in a round-1 forfeit -- a different experiment.
#  2. Reward is absolute own payoff, not the env's win/lose/draw (see
#     _ABSOLUTE_SCORE_ENVS in selfplay.py). IPD is general-sum; its terminal
#     reward maps mutual cooperation (30-30) and mutual defection (10-10) to the
#     same draw, so training on it cannot see welfare and would make "the
#     gradient erodes" true by construction.
#  3. Hyperparameters match ipd_exp's T1: 90 steps, lr 2e-5, LoRA rank 32,
#     Qwen3.5-9B, temp 1.0, 384 generate tokens, checkpoints every 15.
#
# turns_per_step=480: an IPD self-play episode is exactly 40 model turns (10
# rounds x 2 turns x 2 seats, confirmed by --dry-run), so 480 turns is 12
# episodes -> 24 seat-trajectories per policy step. That matches T1's 24
# episodes/step of training data at the same sampling cost (T1 sampled one seat
# for 20 turns x 24 episodes = 480 calls/step; here it is 12 x 40).
#
# max_concurrent_games=12 is deliberately 480/40 and not more: collect_batch
# plays a full wave then TRUNCATES to turns_per_step, so 16 in flight would
# sample 640 turns and throw a quarter of them away.
#
# Eval is DISABLED (--eval-steps 0). spiral's eval puts a RandomAgent in one
# seat, which needs a per-env action-space parser IPD has no sensible one for
# (its action space is enumerable only on decision turns). Checkpoints are
# scored instead with ipd_exp's own battery, which is what makes the numbers
# comparable to T1/A2 in the first place.
set -uo pipefail
cd "$(dirname "$0")"
set -a; . /workspace/allie/.env; set +a

export SPIRAL_DIR="${SPIRAL_DIR:-/workspace/allie/spiral}"
export PYTHONPATH="/workspace/allie/TextArena:${SPIRAL_DIR}${PYTHONPATH:+:$PYTHONPATH}"

STEPS="${STEPS:-90}"
TURNS="${TURNS:-480}"
OUT="${OUT:-/workspace/allie/ipd_exp/runs90_selfplay}"

exec ./.venv/bin/python train_tinker.py \
  --arm ipd \
  --scale short \
  --spiral-dir "$SPIRAL_DIR" \
  --model Qwen/Qwen3.5-9B \
  --lora-rank 32 \
  --num-steps "$STEPS" \
  --turns-per-step "$TURNS" \
  --max-concurrent-games 12 \
  --learning-rate 2e-5 \
  --generate-max-length 384 \
  --eval-steps 0 \
  --save-steps 15 \
  --seed 0 \
  --output-dir "$OUT" \
  --run-name ipd-selfplay-s0 \
  --use-wb --wb-project strategy-behavior \
  "$@"
