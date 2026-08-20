#!/usr/bin/env bash
#SBATCH --job-name=scale-ext
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=8
#SBATCH --time=10:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/hole_exp/logs/scaling/ext-%x-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/hole_exp/logs/scaling/ext-%x-%j.out
#
#   sbatch --job-name=ext-scale-game-n8-hole sbatch_scaling_ext.sh <arm> <model> <port>
#
# --gres=gpu:0: everything reaches the checkpoint through the Tinker proxy over
# HTTP, so a held GPU would idle. Same rationale as sbatch_external.sh.
set -uo pipefail
exec /workspace/allie/strategy-behavior/hole_exp/run_scaling_external.sh "$@"
