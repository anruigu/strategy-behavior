#!/usr/bin/env bash
#SBATCH --job-name=cuecond
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=12
#SBATCH --time=48:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/cuecond/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/cuecond/%x-%j.out
#
#   ./sbatch_cuecond.sh --all                 # the 3 x 2 wave
#   sbatch --job-name=cc-aux-on sbatch_cuecond.sh aux on
#
# CAN THE REGMIX ARM BE MADE TO CONDITION ON ITS COUNTERPART?
#
# `--regime-mix` decorrelates the disposition from env identity so that the
# counterpart's own behaviour is the only thing that predicts whether the hole
# is priced -- the one signal that could transfer to a held-out env, where a
# lookup table over environments cannot (MIXED-REGIME.md, Result 3). It did not
# take: `mixed_disp_regmix_d1_s0` ran 90 steps with the hole-minus-nohole gap
# oscillating either side of zero and ended at -0.097.
#
# Two candidate reasons, one arm each, plus the control they are both measured
# against. Every other thing is held identical.
#
#   ctl     `--regime-mix 0.5` exactly as it runs today. NOT redundant with the
#           runs already on disk: those are Qwen3.6 at 384 tokens and these are
#           Qwen3.8 at 1024, and the base-model screen (sbatch_thinking.sh) puts
#           the pre-training discrimination of those two models on opposite
#           sides of zero. Without a model-matched control, any movement in the
#           treatment arms is attributable to the model change.
#
#   aux     THE CUE IS NOT IN THE REPRESENTATION. Nothing rewards encoding the
#           counterpart's disposition until the action distribution already
#           varies with it, and it does not, so the correlation never
#           bootstraps. Pay for the representation directly: a supervised
#           one-word classification of the counterpart (PUNISHES / PERMITS)
#           from the observable history, trained on the same weights alongside
#           the RL gradient. (`--aux-weight 0.5`, aux_probe.py)
#
#   cue     THE BASELINE CANNOT SEE THE CUE. The disposition is drawn once per
#           GRPO group, so the entire hole-vs-nohole difference lands in the
#           group mean and is subtracted off before any token sees it; the
#           advantage is cue-blind by construction. Put both counterparts in
#           one group and baseline against a learned V(observable prefix) per
#           decision instead. (`--regime-draw rollout --advantage critic`,
#           cue_critic.py)
#
# x THINKING ON / OFF, because the base-model screen found thinking is the only
# condition in which Qwen discriminates at all before training (+0.135
# [+0.056, +0.215] against two nulls), and a policy that cannot discriminate
# before training may simply have given RL nothing to sharpen. If that is the
# binding constraint then both fixes should move only the think-on arms, which
# is a different conclusion from either fix working.
#
# READ `CCI`, NOT `DISC`. The old headline is the pooled exploit-rate gap, and
# it moves for two reasons: the policy conditioning on the counterpart, and the
# two regimes not offering the same decision points (a punishing counterpart
# retaliates, which truncates the scored set -- on `ipd` the always-exploit
# reference scores one decision where the honest one scores nine). On a
# simulation with the conditioning set to exactly zero and only the truncation
# present, `regime/discrimination` reads -0.189 and `cue/cci` reads -0.001.
# `cue/cci` is the same contrast at MATCHED decision points and is the number
# this wave is judged on. cue_metrics.py has the argument.
#
# `aux/probe_acc` runs on ALL THREE arms, control included. It is a two-way
# forced choice on the observable history and it costs two forward passes. A
# control arm sitting at chance would mean the cue is not readable in these
# cells at all, and then no trainer change was ever going to produce
# conditioning -- that is a conclusion about the roster, and it is worth being
# able to reach it.
#
# NOT TRUE OF THE FIRST THREE JOBS OF THIS WAVE (666/668/670, submitted
# 2026-08-23). They started against a train_mixed that gated probe CONSTRUCTION
# on `--aux-weight > 0`, so only the `aux` arm logs `aux/probe_acc` live; the
# fix landed while they were running and Python had already loaded the module.
# The chained `-think` jobs get it. For the three think-off arms the diagnostic
# is recovered off their checkpoints with `probe_checkpoints.py`, which is the
# better measurement anyway -- fixed seeds per env, both regimes, and it can
# include the held-out `ultimatum`, which the training loop never rolls.
# No gradient differs either way: with `--aux-weight 0` the probe datums are
# scored and never handed to a backward pass.
#
# ROSTER + SAMPLING are `sbatch_thinking.sh`'s, unchanged, so this wave sits
# next to that pair without a second confound: seven opponent-swap cells,
# `ultimatum` held out, Qwen3.8-27B, t0.7 / top_p 0.9 / 1024 tokens,
# reasoning_effort=low on the think arms.
set -uo pipefail
cd /workspace/allie/strategy-behavior/hole_exp
PY=/workspace/allie/venvs/tinker-ipd/bin/python

ENVS="ipd public_goods dond trust ipd3 staghunt winasmuch"
MODEL="Qwen/Qwen3.8-27B"
SEED="${SEED:-0}"

declare -A ARM=(
  [ctl]=""
  [aux]="--aux-weight 0.5 --aux-per-episode 1"
  [cue]="--regime-draw rollout --advantage critic"
)

# NODES. These are CPU-only rollout drivers (all sampling is remote on Tinker)
# at 12 workers on 192-core boxes, so a node is not the scarce resource -- but
# the crash that motivated one-job-per-node in sbatch_dispositions.sh was five
# to eight of them on one box, so keep it to two. node-0/1/2/4/5 are held by
# the in-flight think wave; these are the two idle boxes.
NODES="${NODES:-node-7 node-9}"

# THE THINK ARMS ARE CHAINED BEHIND THE THINK-OFF ARMS, NOT RUN BESIDE THEM.
# Five think-on runs are already in flight (sbatch_think_wave.sh) and every one
# of these is another 12-worker client against the same Tinker service. Eleven
# at once would not fail, it would just make all eleven slow, and the in-flight
# wave did not consent to that. Chaining costs wall-clock and buys two things:
# the three-arm comparison lands complete in ~12h instead of all six landing
# late, and the think arms start as the think wave is winding down.
#
# `afterany`, not `afterok`: if a think-off arm dies at step 60 the think-on arm
# should still run. It is a separate cell, not a continuation.
if [ "${1:-}" = "--all" ]; then
  read -r -a _nodes <<<"$NODES"
  i=0
  for arm in ctl aux cue; do
    node="${_nodes[$(( i % ${#_nodes[@]} ))]}"
    jid=$(sbatch --parsable --job-name="cc-${arm}-off" \
                 --nodelist="$node" "$0" "$arm" off)
    echo "submitted cc-${arm}-off  -> $jid  ($node)"
    dep=$(sbatch --parsable --job-name="cc-${arm}-on" \
                 --nodelist="$node" --dependency="afterany:${jid}" \
                 "$0" "$arm" on)
    echo "submitted cc-${arm}-on   -> $dep  ($node, after $jid)"
    i=$((i + 1))
  done
  exit 0
fi

ARM_NAME="${1:?arm: ctl | aux | cue}"
MODE="${2:-off}"
FLAGS="${ARM[$ARM_NAME]?unknown arm $ARM_NAME}"

THINK_FLAGS=()
if [ "$MODE" = "on" ]; then
  THINK_FLAGS=(--think --reasoning-effort low)
fi

export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
export WANDB_DIR=/workspace/allie/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR" logs/cuecond

echo "[cc] node=$(hostname) arm=$ARM_NAME think=$MODE seed=$SEED model=$MODEL"
echo "[cc] flags: $FLAGS"
echo "[cc] train: $ENVS   (held out: ultimatum)"

# `--label-suffix cc` keeps this wave off the ten-env `mixed_regmix_*` and the
# seven-env `mixed_disp_regmix_*` directories, both of which are already
# written and are what this is compared against. The arm itself is encoded by
# train_mixed from the flags (`regmix`, `regmix-aux`, `regmix-rr-critic`), plus
# `-think`, so the six runs cannot collide with each other either.
exec "$PY" train_mixed.py \
  --envs $ENVS \
  --regime-mix 0.5 \
  $FLAGS \
  "${THINK_FLAGS[@]}" \
  --aux-probe-every 5 \
  --label-suffix cc \
  --dose 1.0 \
  --seed "$SEED" \
  --model "$MODEL" \
  --steps 90 \
  --groups 14 \
  --group-size 6 \
  --temperature 0.7 \
  --top-p 0.9 \
  --max-tokens 1024 \
  --workers 12 \
  --out /workspace/allie/strategy-behavior/hole_exp/runs \
  --use-wb
