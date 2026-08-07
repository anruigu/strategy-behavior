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

# Notes ==========
# Set `--eval_opponent_names google/gemini-2.0-flash-lite-001` if you have OpenRouter access.
#
# --save_steps 64, NOT the 16 the other arms use. --save_path is on shared
# /workspace, which is 92% full and shared with other users, and a Qwen3-4B
# bf16 checkpoint is 7.6GB: at save_steps 16 a 400-step run writes 25 of them,
# ~190GB, and only ~4 such runs fit in what is left. At 64 it writes
# 64/128/192/256/320/384 plus the forced end-of-run save (oat calls
# eval_and_log(save=True) after the loop, so the final step is checkpointed
# whatever the cadence) -- 7 checkpoints, ~53GB.
#
# This is deliberately the same "64" as sync_checkpoints.sh's MIRROR_EVERY
# default, so a run that later does need mirroring keeps exactly this ladder.
# Bounding it here rather than at mirror time is what actually saves space for
# this arm: --save_path already points at durable /workspace, so there is no
# mirror step to thin, and oat's own --max_save_num cannot express a ladder (it
# just deletes the oldest until N remain, which would drop the early curve).
#
# PigDice control arm -- replaces the TicTacToe control. Pig is zero-sum and
# two-player like KuhnPoker, but the uncertainty is *stochastic* (dice) rather
# than *informational* (a hidden card), and there is nothing to represent to an
# opponent. So it separates "trained on a risky zero-sum game" from "trained on
# a game where bluffing pays", which TicTacToe (no uncertainty at all) could
# not.
#
# --use_llm_obs_wrappers True is REQUIRED here, and is why this differs from
# run_control.sh, which used False for TicTacToe. TicTacToe redraws the whole
# board in its latest message, so FirstLastObservationWrapper loses nothing.
# PigDice does not: the running scores arrive in a turn-rotation message and
# the turn total in a per-roll message, both of which First+Last drops. Under
# False the player sees only the static rules prompt and "Available actions:
# '[roll]' or '[hold]'" -- it cannot see its own turn total, so the roll/hold
# decision is blind and the run is worthless. Verified by inspecting the
# wrapped observation directly.
#
# Cost warning: a PigDice episode is ~50-60 model calls (winning_score=50),
# against ~9 for TicTacToe and ~10-20 for KuhnPoker, so a policy step generates
# several times more tokens than the other arms at the same rollout_batch_size.
# Expect wall-clock per step to be correspondingly higher.

python train_spiral.py \
    --save_path "$SAT_SAVE_PATH-pigdice" \
    --env_ids PigDice-v1 \
    --use_llm_obs_wrappers True \
    --eval_opponent_names random \
    --eval_env_ids TicTacToe-v0 KuhnPoker-v1 PigDice-v1 \
    --eval_use_llm_obs_wrappers False True True \
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
    --wb-run-name spiral-qwen3-4b-base-pigdice-control \
    --wb_project spiral
