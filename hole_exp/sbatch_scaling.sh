#!/usr/bin/env bash
#SBATCH --job-name=envscale
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=12
#SBATCH --time=20:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/scaling/%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/scaling/%x-%j.out
#
# One rung of the env-count ladder (0820-scaling-envs.md).
#
#   sbatch --job-name=scale-game-n4-hole sbatch_scaling.sh game 4 hole
#
# --gres=gpu:0 ON PURPOSE, same reasoning as sbatch_external.sh: training runs
# on Tinker over HTTP and the only local work is CPU env simulation (each
# episode is played three times -- measured, honest reference, exploit
# reference), so a held GPU would sit idle and block the vLLM battery.
#
# GROUPS/GROUP_SIZE/STEPS come from scaling_rungs.py and are passed EXPLICITLY.
# train_mixed.py defaults --groups to len(envs), which would make episodes/step
# scale with the rung -- the exact confound (data volume masquerading as
# diversity) this study exists to avoid.
set -uo pipefail
FAMILY="${1:?family: game|synth}"; N="${2:?rung size}"; ARM="${3:?hole|nohole}"
SEED="${4:-0}"

cd /workspace/allie/strategy-behavior/hole_exp
PY=/workspace/allie/venvs/tinker-ipd/bin/python

# $HOME is /home/allie, which does not exist on some compute nodes (node-2 has
# no such directory though Slurm still exports the variable). Third time this
# has bitten a batch script here; pin every cache to the shared volume.
export HOME=/workspace/allie
export XDG_CACHE_HOME=/workspace/allie/.cache
export WANDB_DIR=/workspace/allie/strategy-behavior/hole_exp/wandb
mkdir -p "$XDG_CACHE_HOME" "$WANDB_DIR"

# scaling_rungs.py is the single source of truth for what a rung IS; resolve it
# there and eval the assignments rather than restating the sets in shell.
# NGROUPS, not GROUPS: `GROUPS` is a bash special array holding the caller's
# group IDs and assignment to it is SILENTLY IGNORED, so `eval "GROUPS=8"` left
# $GROUPS expanding to the primary gid (1005) and the first launch of this
# script trained at 1005 groups x 6 = 6030 episodes/step. Nothing errored -- the
# runs started and looked healthy. Hence the assertion below.
CFG=$("$PY" -c '
import sys
sys.path.insert(0, "/workspace/allie/strategy-behavior/hole_exp")
import scaling_rungs as S
fam, n = sys.argv[1], int(sys.argv[2])
print(f"ENVS=\"{" ".join(S.rung(fam, n))}\"")
print(f"STEPS={S.STEPS}; NGROUPS={S.GROUPS}; GSIZE={S.GROUP_SIZE}")
print(f"MODEL=\"{S.MODEL}\"; DOSE={S.DOSE}; CKPT={S.CKPT_EVERY}")
print(f"TEMP={S.TEMPERATURE}; TOPP={S.TOP_P}; MAXTOK={S.MAX_TOKENS}")
' "$FAMILY" "$N") || { echo "FATAL: could not resolve rung $FAMILY/$N"; exit 1; }
eval "$CFG"
[ -n "${ENVS:-}" ] || { echo "FATAL: empty rung $FAMILY/$N"; exit 1; }
# The whole study is "constant compute per rung", so assert the budget rather
# than trust the expansion: a wrong value here is not a crash, it is a silently
# different experiment at one rung.
"$PY" -c '
import sys
sys.path.insert(0, "/workspace/allie/strategy-behavior/hole_exp")
import scaling_rungs as S
got = dict(zip(("steps", "groups", "gsize"), map(int, sys.argv[1:4])))
want = {"steps": S.STEPS, "groups": S.GROUPS, "gsize": S.GROUP_SIZE}
if got != want:
    raise SystemExit(f"budget mismatch: shell resolved {got}, rungs say {want}")
' "$STEPS" "$NGROUPS" "$GSIZE" || exit 1

echo "[scale] node=$(hostname) family=$FAMILY n=$N arm=$ARM seed=$SEED"
echo "[scale] envs=$ENVS"
echo "[scale] $STEPS steps x $NGROUPS groups x $GSIZE = $((STEPS*NGROUPS*GSIZE)) episodes"
echo "[scale] sampling: t=$TEMP top_p=$TOPP max_tokens=$MAXTOK (no close-bracket)"

# shellcheck disable=SC2086  -- ENVS is a deliberate word-split list
exec "$PY" train_mixed.py \
  --envs $ENVS \
  --consequence "$ARM" \
  --dose "$DOSE" \
  --seed "$SEED" \
  --model "$MODEL" \
  --steps "$STEPS" \
  --groups "$NGROUPS" \
  --group-size "$GSIZE" \
  --ckpt-every "$CKPT" \
  --temperature "$TEMP" \
  --top-p "$TOPP" \
  --max-tokens "$MAXTOK" \
  --workers 12 \
  --out /workspace/allie/strategy-behavior/hole_exp/runs/scaling \
  --label-suffix "scale-${FAMILY}-n${N}" \
  --use-wb
