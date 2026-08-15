# Copyright 2025 SPIRAL Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# run_kuhn_qwen3_8b.sh -- KuhnPoker self-play on Qwen/Qwen3-8B.
#
# The local half of a matched pair against training/tinker/. Qwen3-8B is the
# ONLY model that is both on Tinker's hosted list and loadable by this venv:
# oat 0.2.1 hard-pins vllm==0.8.4, which knows Qwen3ForCausalLM /
# Qwen3MoeForCausalLM only, so every Qwen3.5-* checkpoint (model_type
# `qwen3_5`, arch `Qwen3_5ForConditionalGeneration`) is rejected by transformers
# 4.51.3 before vllm ever sees it.
#
# This is NOT the arm that produced ../results/. That one is run_kuhn.sh on
# Qwen3-4B-Base. Differences from it, all deliberate:
#
#  1. --pretrain Qwen/Qwen3-8B, not Qwen3-4B-Base. Bigger, and an
#     instruct/hybrid-thinking model rather than a base model.
#  2. SPIRAL_NO_THINK=1 (needs patches/qwen3-no-think-template.patch).
#     REQUIRED, not a tuning choice. Qwen3-8B under the stock template opens a
#     <think> block that does not close inside --generate_max_length 4096, so no
#     \boxed{} is emitted, extract_action() falls through to the raw response,
#     that is not in the action space, and every game is a turn-1 forfeit.
#     Measured on Tinker with the identical prompt: 99.8% invalid actions, mean
#     game length 1.002. With /no_think: ~700 tokens and a clean \boxed{[bet]}.
#     The Tinker arm applies the same marker (--thinking-mode auto), which is
#     what makes the two comparable.
#  3. --gpus 4, not 8, with the per-device batches doubled so the GLOBAL batch
#     is unchanged at 128 (oat collects gpus x rollout_batch_size_per_device
#     trajectories per step; 4 x 32 == 8 x 16). Same optimisation, fewer cards.
#  4. --vllm_gpu_ratio 0.30, not 0.45. On a 143GB H200 that is still ~43GB of KV
#     cache, far more than an 8B model needs, and it leaves room for ZeRO-2
#     optimiser state of an 8B model (~44GB/GPU at 4-way sharding) which the 4B
#     arm never had to budget for.
#  5. Separate --save_path and --wb-run-name so it cannot clobber the 4B arm.
#
# Run from inside $SPIRAL_DIR (with train_spiral.py present), after `source $SAT_VENV/bin/activate`.
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
source "$SAT_HOME/config.sh"

# Common =========
export LD_LIBRARY_PATH=$(python -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))"):$LD_LIBRARY_PATH
export NCCL_CUMEM_ENABLE=0
export LP_DEBUG=1
export LP_LOG_LEVEL=DEBUG
export WANDB_TAGS="kuhn,spiral"

# See note 2 above. Honoured by patches/qwen3-no-think-template.patch; without
# that patch applied this variable is silently ignored and the run forfeits
# every game, so fail loudly instead.
export SPIRAL_NO_THINK=1
python -c "
import os, sys, spiral.template as t
if not getattr(t, '_NO_THINK', False):
    sys.exit('spiral/template.py does not honour SPIRAL_NO_THINK -- apply '
             'training/patches/qwen3-no-think-template.patch to \$SPIRAL_DIR')
" || exit 1

python train_spiral.py \
    --save_path "$SAT_SAVE_PATH-qwen3-8b-kp" \
    --env_ids KuhnPoker-v1 \
    --use_llm_obs_wrappers True \
    --eval_opponent_names random \
    --eval_env_ids TicTacToe-v0 KuhnPoker-v1 \
    --eval_use_llm_obs_wrappers False True \
    --eval_split all \
    --gamma 1 \
    --gpus 4 \
    --gradient-checkpointing \
    --num_samples 1 \
    --rollout_batch_size 128 \
    --dump_game_state_every 1 \
    --num_envs 1 \
    --rollout_batch_size_per_device 32 \
    --pi_buffer_maxlen_per_device 32 \
    --pretrain Qwen/Qwen3-8B \
    --enable_prefix_caching \
    --collocate \
    --vllm_sleep \
    --vllm_gpu_ratio 0.30 \
    --rnd-seed \
    --learning_rate 0.000001 \
    --lr_scheduler constant \
    --lr_warmup_ratio 0 \
    --num_ppo_epochs 2 \
    --train_batch_size 128 \
    --train_batch_size_per_device 1 \
    --beta 0 \
    --max_model_len 12800 \
    --generate_max_length 4096 \
    --max_context_length 32768 \
    --temperature 1.0 \
    --top_p 1 \
    --eval_steps 16 \
    --save_steps 16 \
    --eval_games 16 \
    --eval_temperature 0.6 \
    --eval_top_p 0.95 \
    --eval_generate_max_length 4096 \
    --max_train 51200 \
    --max_save_num 30 \
    --use-wb \
    --wb-run-name spiral-qwen3-8b-kp-4k-self-play \
    --wb_project strategy-behavior
