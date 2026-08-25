#!/usr/bin/env bash
#
# Does Qwen3.8-27B WITH reasoning read its counterpart better than the
# reasoning-off model the disposition runs are training on?
#
# Three conditions, same envs / arms / seeds / dose, so the two contrasts are
# each isolated to one change:
#
#   q36-off     Qwen3.6-27B  t1.0 p1.0  384tok  think off   <- the training config
#   q38-off     Qwen3.8-27B  t0.7 p0.9  512tok  think off   <- model change alone
#   q38-think   Qwen3.8-27B  t0.7 p0.9 1024tok  think low   <- reasoning change alone
#
# q38-off vs q38-think is the clean reasoning contrast. q36-off vs q38-off also
# moves the sampling profile, and cannot not: 3.8 at t1.0/384 is a broken
# instrument (0820-qwen38-sampling-profile.md -- 0.93 invalid on the agentic
# cell), so "3.8 at 3.6's settings" is not a condition worth spending on.
# Thinking forces max_tokens up and close_bracket off for the reasons in
# tinker_actor: an unset reasoning_effort resolves to xhigh on this template and
# runs the budget out mid-thought, and a ']' inside <think> would halt
# generation before the action is ever written.
#
# The question is NOT which condition scores highest -- in-env reward is never
# the finding. It is which one DISCRIMINATES: whether exploitation is ordered by
# how much the counterpart forgives (hole >= adaptive_recover >= adaptive >=
# nohole) and whether the policy backs off after being punished.
set -uo pipefail
cd /workspace/allie/strategy-behavior/hole_exp
PY=/workspace/allie/venvs/tinker-ipd/bin/python

# The seven cells the disposition runs actually train on, plus the held-out
# `ultimatum`. Kept identical across conditions -- an env set that differs
# between arms would make the columns incomparable.
ENVS="ipd public_goods trust dond ipd3 staghunt winasmuch ultimatum"
SEEDS=12
WORKERS=16

mkdir -p logs results

run () {   # run <tag> <extra args...>
  local tag="$1"; shift
  echo "[reasoning-eval] $tag  $*"
  "$PY" eval_dispositions.py \
    --envs $ENVS --seeds "$SEEDS" --dose 1.0 --workers "$WORKERS" \
    --json "results/reasoning-${tag}.json" \
    --episodes-json "results/reasoning-${tag}-episodes.json" \
    --viewer-alias "disp-${tag}" \
    "$@" > "logs/reasoning_${tag}.log" 2>&1
  echo "[reasoning-eval] $tag done rc=$?"
}

# Sequential, not parallel: eight training runs are already contending for the
# same Tinker account and three concurrent 16-worker sweeps on top of that is
# how the Tier B arms got wedged.
run q36-off   --model Qwen/Qwen3.6-27B --temperature 1.0 --top-p 1.0 --max-tokens 384
run q38-off   --model Qwen/Qwen3.8-27B --temperature 0.7 --top-p 0.9 --max-tokens 512
run q38-think --model Qwen/Qwen3.8-27B --temperature 0.7 --top-p 0.9 --max-tokens 1024 \
              --thinking --reasoning-effort low
echo "[reasoning-eval] all done"
