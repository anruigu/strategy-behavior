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

# Run from inside $SPIRAL_DIR (with train_spiral.py present), after `source $SAT_VENV/bin/activate`.
# Copied out of this repo, so if SAT_HOME doesn't auto-detect, export it first: SAT_HOME=/path/to/spiral-alignment-transfer.
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
source "$SAT_HOME/config.sh"

# Common =========
export LD_LIBRARY_PATH=$(python -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))"):$LD_LIBRARY_PATH
export NCCL_CUMEM_ENABLE=0
export LP_DEBUG=1
export LP_LOG_LEVEL=DEBUG
export WANDB_TAGS="multigame-social,spiral"

# Notes ==========
# Set `--eval_opponent_names google/gemini-2.0-flash-lite-001` if you have OpenRouter access.
#
# 0806 multigame -- SOCIAL arm. Four two-player games where misrepresenting
# your private state pays, trained concurrently:
#   TruthAndDeception-v1  one player holds the truth and tries to mislead the
#                         other; near-maximal deception density, 6 turns.
#   KuhnPoker-v1          the cheap bluffing env SPIRAL itself trained on.
#   SimpleNegotiation-v1  cheap talk + hidden valuations, bounded turns.
#   LiarsDice-v1-2d       bluffing about hidden dice, ROUND-CAPPED to 2 dice.
#
# --use_llm_obs_wrappers True for all four, and for LiarsDice it is load-bearing
# beyond the usual "the model needs the history" argument: the action parser
# reads the round boundary ("Your new dice are:") and the live "Remaining dice:"
# block out of the observation to know which bids are legal. Under
# FirstLastObservationWrapper both are gone, every round looks like round 1, and
# the parser offers '[Call]' with no standing bid -- an instant invalid move.
#
# LiarsDice-v1-2d rather than LiarsDice-v1: at the default num_dice=5 a
# self-play episode averages 32.8 model calls (measured over 200 games); at 2
# dice it is 9.4, which is the 1-2 round cap the 0806 plan asked for.
#
# Two of the four have no fixed action space -- SimpleNegotiation and
# TruthAndDeception both route through extract_chat_action (see the env_id list
# in train_spiral.py agent_act) because their turns are free-form persuasion,
# with only T&D's final '[Fact 1]'/'[Fact 2]' guess constrained.
#
# --save_steps 64 for the same disk reason as run_pigdice.sh: /workspace is
# shared and 92% full, so 7 checkpoints (~53GB), not 25 (~190GB).

python train_spiral.py \
    --save_path "$SAT_SAVE_PATH-multigame-social" \
    --env_ids TruthAndDeception-v1 KuhnPoker-v1 SimpleNegotiation-v1 LiarsDice-v1-2d \
    --use_llm_obs_wrappers True True True True \
    --eval_opponent_names random \
    --eval_env_ids TicTacToe-v0 KuhnPoker-v1 \
    --eval_use_llm_obs_wrappers False True \
    --eval_split all \
    --gamma 1 \
    --gpus 8 \
    --gradient-checkpointing \
    --num_samples 1 \
    --rollout_batch_size 128 \
    --dump_game_state_every 1 \
    --num_envs 1 \
    --rollout_batch_size_per_device 16 \
    --pi_buffer_maxlen_per_device 16 \
    --pretrain Qwen/Qwen3-4B-Base \
    --enable_prefix_caching \
    --collocate \
    --vllm_sleep \
    --vllm_gpu_ratio 0.45 \
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
    --save_steps 64 \
    --eval_games 16 \
    --eval_temperature 0.6 \
    --eval_top_p 0.95 \
    --eval_generate_max_length 4096 \
    --max_train 51200 \
    --max_save_num 30 \
    --use-wb \
    --wb-run-name spiral-qwen3-4b-base-multigame-social \
    --wb_project strategy-behavior
