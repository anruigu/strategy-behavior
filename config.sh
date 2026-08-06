#!/usr/bin/env bash
# config.sh -- shared paths and knobs for every script in this repo.
#
# Source it from each script; override any variable by exporting it beforehand:
#
#     SAT_VENV=/my/venv MASK_DIR=/my/mask bash evals/run_mask.sh spiral-step256
#
# The values in comments (<...>) are what the original study used on its
# RunPod + slurm box; the defaults below are repo-relative so a fresh clone at
# least resolves. The three external checkouts (spiral, MASK, MACHIAVELLI) and
# the python venvs you must create yourself -- see README.md.

# Repo root. Auto-detected from this file; export SAT_HOME to override (needed
# for slurm, which copies the submitted script to a spool dir before running).
: "${SAT_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)}"

# --- external checkouts (clone these; see README) ---------------------------
: "${SPIRAL_DIR:=$SAT_HOME/../spiral}"                 # github.com/spiral-rl/spiral (+ training/patches)
: "${MASK_DIR:=$SAT_HOME/../mask}"                     # github.com/centerforaisafety/mask
: "${MACHIAVELLI_DIR:=$SAT_HOME/../machiavelli}"       # github.com/aypan17/machiavelli
: "${MASK_HARNESS:=$MASK_DIR/mask}"                    # the runnable harness lives one level in

# --- python environments ----------------------------------------------------
# Training/serving venv (python 3.10: oat + vllm + textarena). It MUST live
# outside the spiral checkout -- nltk's import guard rejects any site-packages
# module whose origin resolves under the current working directory, and the
# training entrypoint runs from the repo root.        <  /workspace/allie/venvs/spiral  >
: "${SAT_VENV:=$HOME/venvs/spiral}"
# MASK pins its own (conflicting) deps, so it gets a separate venv.  < evals/mask/.venv >
: "${SAT_MASK_VENV:=$MASK_DIR/.venv}"
# Tiny venv with boto3, only for the optional S3 checkpoint tier.    < venvs/tools >
: "${SAT_TOOLS_PY:=python}"

# --- secrets ----------------------------------------------------------------
# dotenv exporting OPENROUTER_API_KEY, WANDB_API_KEY, and (optional) AWS creds.
: "${SAT_ENV_FILE:=$SAT_HOME/.env}"                    # see env.example

# --- caches / outputs -------------------------------------------------------
: "${SAT_HF_HOME:=$HOME/.cache/huggingface}"           # keep off ephemeral disk (~8GB weights)
: "${SAT_SAVE_PATH:=$HOME/oat-output}"                 # oat --save_path
: "${SAT_CKPT_DIR:=$SAT_HOME/ckpts}"                   # durable checkpoint mirror
: "${SAT_RUNS_DIR:=$SAT_HOME/results/runs}"            # per-arm MASK harness copies + outputs
: "${SAT_PREBUILT_DIR:=$SAT_HOME/prebuilt}"            # prebuilt fused_adam.so for slurm nodes

# --- MASK judge -------------------------------------------------------------
# NOT gpt-4o: on OpenRouter it is served by Azure, which content-filters MASK's
# lying/disinformation prompts (HTTP 400) and silently drops ~1/3 of rows.
: "${MASK_JUDGE_MODEL:=openai/gpt-4.1}"
