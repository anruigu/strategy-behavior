#!/usr/bin/env bash
#SBATCH --job-name=ext-battery
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=16
#SBATCH --time=14:00:00
#SBATCH --output=/workspace/allie/strategy-behavior/evals/slurm-ext-%j.out
#SBATCH --error=/workspace/allie/strategy-behavior/evals/slurm-ext-%j.out
#
# One EVAL_SUITE external battery per arm, one arm per node.
#
#   sbatch --nodelist=node-N sbatch_external.sh <label> <model> <port>
#
# --gres=gpu:0 ON PURPOSE. Every eval here reaches the checkpoint through the
# Tinker proxy over HTTP, so the work is API-bound and a GPU would sit idle --
# holding one would block the vLLM battery, which genuinely needs them. Verified
# that compute nodes can construct a tinker.ServiceClient before relying on this.
set -uo pipefail
exec /workspace/allie/strategy-behavior/hole_exp/run_external_battery.sh "$@"
