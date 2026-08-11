#!/usr/bin/env bash
#SBATCH --job-name=mathbench
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=32
#SBATCH --time=12:00:00
#SBATCH --output=/workspace/allie/evals/slurm-mathbench-%j.out
#SBATCH --error=/workspace/allie/evals/slurm-mathbench-%j.out
# Usage: sbatch sbatch_mathbench.sh <arm-name> <model-path-or-hf-id>
#
# Runs SPIRAL's own reasoning battery (math500, aime24, aime25, olympiadbench,
# amc23, minerva_math) via evals/benchmarks/math-evaluation-harness at the
# repo's own settings: prompt_type qwen3-self-play, temperature 0.6, top_p 0.95,
# n_sampling 4, max_tokens_per_call 8192.
set -euo pipefail
ARM="$1"; MODEL="$2"
H=/workspace/allie/spiral/evals/benchmarks/math-evaluation-harness

# Harness has its OWN venv: it needs latex2sympy2 (an undeclared dependency of
# grader.py) and a sympy/antlr combination that differs from the training venv,
# which running jobs import from and must not be mutated.
source "$H/.venv/bin/activate"
set -a; . /workspace/allie/.env; set +a
source /workspace/allie/evals/node_env.sh

# Clean up any GPU processes we orphan on the way out. vllm's engine workers are
# multiprocessing forks: killing only the parent reparents them to init, where
# they keep their GPU reservation and OOM whatever slurm schedules next on this
# node (one such orphan held 122GB of node-2 for 8h and killed a training job).
cleanup() {
    for p in $(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null); do
        [ "$(stat -c %u /proc/"$p" 2>/dev/null)" = "$(id -u)" ] && kill -9 "$p" 2>/dev/null || true
    done
}
trap cleanup EXIT INT TERM

OUT="$H/data/eval/$ARM"
mkdir -p "$OUT"
cd "$H"
echo "node=$(hostname) arm=$ARM model=$MODEL out=$OUT"

TOKENIZERS_PARALLELISM=false python3 -u math_eval.py \
    --model_name_or_path "$MODEL" \
    --data_names "math500,aime24,aime25,olympiadbench,amc23,minerva_math" \
    --output_dir "$OUT" \
    --split test \
    --prompt_type qwen3-self-play \
    --num_test_sample -1 \
    --max_tokens_per_call 8192 \
    --seed 0 --temperature 0.6 --n_sampling 4 --top_p 0.95 \
    --start 0 --end -1 \
    --use_vllm --save_outputs

echo "=== MATHBENCH_DONE arm=$ARM ==="
