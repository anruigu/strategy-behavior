# Negotiation GRPO 9B — Environment & Code Fixes (2026-06-11)

Applies to: `neg-baseline-r3` (outcome reward) and `neg-pareto-r2` (outcome_pareto reward), Qwen3.5-9B, RunPod SLURM nodes 8-9.

---

## Fix 1: Broken `.venv` detection in setup script

**File:** `scripts/fleet-negotiation-setup.sh` (lines 65-74)

**Problem:** Previous interrupted runs left `.venv/lib/python3.12/` on disk but without `bin/activate`. The setup script checked only `[ -d ".venv" ]`, so it tried to `source .venv/bin/activate` on a broken venv and failed with "No such file or directory", blocking all subsequent setup workers.

**Fix:**
```bash
if [ -d ".venv" ] && [ ! -f ".venv/bin/activate" ]; then
  echo "Stale/broken .venv found (no bin/activate) — removing and recreating"
  rm -rf .venv
fi
```

---

## Fix 2: NCCL IB HCA selection (fleet-common-run.sh)

**File:** `scripts/fleet-common-run.sh` (around line 290)

**Problem:** The original `ib-hca-intersection.sh` computed an intersection of HCA lists across nodes. On nodes 8/9, this included `mlx5_4` (10GbE Ethernet) and `mlx5_5` (40GbE Ethernet, DOWN) — non-IB adapters. NCCL tried to use them for collective communication, causing hangs.

**Fix (SKIP_IB_INTERSECTION=1):** Read directly from `/etc/nccl.conf` which has the correct IB-only list:
```bash
if [ "${SKIP_IB_INTERSECTION:-0}" = "1" ]; then
  _nccl_conf_hca=$(grep '^NCCL_IB_HCA=' /etc/nccl.conf 2>/dev/null | cut -d= -f2- | tr -d '"')
  if [ -n "$_nccl_conf_hca" ]; then
    export NCCL_IB_HCA="$_nccl_conf_hca"
    echo "[NCCL] SKIP_IB_INTERSECTION=1: set NCCL_IB_HCA=$NCCL_IB_HCA (IB-only, from /etc/nccl.conf)"
  fi
fi
```

Correct HCA list: `mlx5_0,mlx5_1,mlx5_2,mlx5_3,mlx5_6,mlx5_7,mlx5_8,mlx5_9` (8 × 400 Gb/s NDR IB ports).

This env var is set in `fleet-negotiation-9b-run.sh`: `export SKIP_IB_INTERSECTION="${SKIP_IB_INTERSECTION:-1}"`.

---

## Fix 3: Reward-mode-specific regularization for pareto arm

**File:** `scripts/fleet-negotiation-9b-run.sh`

**Problem:** The pareto run (outcome_pareto reward) had KL coefficient 0.001 — too weak relative to the pareto gradient bonus — causing reward hacking / mode collapse (grad_norm spiking to 17).

**Fix (PARETO_ARGS):**
```bash
if [ "$REWARD_MODE" = "outcome_pareto" ]; then
  PARETO_ARGS=(
    trainer.algorithm.kl_loss_coef=0.05
    trainer.policy.optimizer_config.max_grad_norm=0.5
    "environment.skyrl_gym.negotiation.invalid_penalty=-0.05"
  )
fi
```

---

## Fix 4: thinking=false for Qwen3.5-9B (vLLM inference)

**File:** `scripts/fleet-negotiation-9b-run.sh`

**Problem:** Qwen3.5-9B is hybrid-reasoning. With `enable_thinking` unset, it produces `<think>` blocks that consume the entire turn budget before emitting a `<propose>` tag — ~80% no_deal rate (see eval reports).

**Fix:**
```
+generator.chat_template_kwargs.enable_thinking=false
```
Also added stop tokens: `["</propose>","</deal>","<accept>","</think>"]` to prevent runaway thinking blocks from consuming sequence length.

---

## Multi-node NCCL issue (unresolved — switched to 1-node runs)

**Symptom:** `FSDPRefWorkerBase` NCCL BROADCAST timeout after 600s during `async_init_model`. Error: `[Rank 11] Watchdog caught collective operation timeout: WorkNCCL(SeqNum=1, OpType=BROADCAST, NumelIn=1769472, Timeout(ms)=600000)`.

**Investigation:**
- All 8 IB ports on both nodes physically healthy (4: ACTIVE, 400 Gb/s NDR)
- Process group init (small all-reduce) passes on both policy and ref groups
- First actual weight BROADCAST across node-8 → node-9 hangs indefinitely
- NCCL_IB_HCA correctly set in shell env; Ray workers inherit via raylet
- No OOM (2 TiB RAM available, 140 GB H200 VRAM per GPU)

**Root cause (suspected):** NCCL IB queue-pair setup between node-8 and node-9 fails for larger cross-node transfers despite hardware health. Possibly IB fabric routing or NCCL IB QP configuration issue not exercised by the small process-group-init sanity check.

**Workaround:** Switched to 1-node runs (`tasks/negotiation-grpo-qwen3_5-9b-1node.yaml`, `num_nodes: 1`, `NUM_INFERENCE_ENGINES: 8`). Baseline and pareto run in parallel on separate nodes.

---

## Fix 5: Ray --num-cpus cap to prevent pthread_create burst failure

**File:** `scripts/fleet-common-run.sh` (ray start --head and ray start --address calls)

**Problem:** Ray detects 163 Docker-cgroup CPUs on nodes 8-9 and pre-spawns 163 idle worker processes (`--num_prestart_python_workers=163`). Each worker creates ~100 threads (gRPC completion queues, Ray core worker threads). The burst of 163 simultaneous worker launches creates ~16,300 threads at once, causing gRPC's internal `pthread_create` to fail with `Resource temporarily unavailable` (EAGAIN). The workers that fail die with `St12system_error` in `CoreWorkerProcessImpl::InitializeSystemConfig`. The main training entrypoint (PID of `main_fleet`) gets stuck waiting for workers that never register, hanging indefinitely.

**Symptom timeline:** Ray cluster starts (00:52), 153/163 prestart workers spawn, 10+ crash with `pthread_create failed` in `thd.cc:157`, `main_fleet` hangs at `unix_stream_data_wait` for 16+ hours. Training never starts.

**Fix:**
```bash
# In ray start --head and ray start --address calls, add:
--num-cpus="${RAY_NUM_CPUS:-32}"
```
This caps Ray's CPU view to 32, so only 32 idle workers are pre-spawned (~3,200 threads). All workers start cleanly. Training actors (FSDP shards, vLLM engines) can start successfully — they request GPU resources, not CPU, so the lower CPU count doesn't affect scheduling.

**Verified:** neg-pareto-r2 (SLURM 2973, node-8, 2026-06-11) started with 23 IDLE workers and 2,954 total threads (vs 153 workers / 15,743 threads before fix). FSDP process group initialized, vLLM launched, eval_before_train started.
