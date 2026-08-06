#!/usr/bin/env bash
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)}"
source "$SAT_HOME/config.sh"

# node_env.sh -- environment preamble for any slurm job on this cluster.
# Source, don't execute.
#
# The compute nodes do NOT have our home directory: $HOME=/home/allie does not
# exist there and is not writable, and our UID (1005) isn't even in their passwd
# database (`whoami` fails with "cannot find name for user ID 1005"). Anything
# that caches under $HOME therefore dies on a fresh node:
#   * torch cpp_extension  -> RuntimeError: Error building extension 'fused_adam'
#   * vllm / torch.compile -> PermissionError: [Errno 13] ... '/home/allie'
#   * triton autotune      -> df: /home/allie/.triton/autotune: No such file
# So point HOME and every cache at node-local /tmp, which is writable.
# HF_HOME deliberately stays on shared /workspace so the 8GB model weights are
# downloaded once and reused by every node.

export HOME=/tmp/allie-home
mkdir -p "$HOME"
export XDG_CACHE_HOME="$HOME/.cache"
export TORCH_EXTENSIONS_DIR="$HOME/.cache/torch_extensions"
export TORCHINDUCTOR_CACHE_DIR="$HOME/.cache/inductor"
export TRITON_CACHE_DIR="$HOME/.cache/triton"
export TMPDIR="${TMPDIR:-/tmp}"
mkdir -p "$TORCH_EXTENSIONS_DIR" "$TORCHINDUCTOR_CACHE_DIR" "$TRITON_CACHE_DIR"

export HF_HOME="$SAT_HF_HOME"
export PYTHONUNBUFFERED=1
export CUDA_HOME=/usr/local/cuda
export PATH="$CUDA_HOME/bin:$PATH"

# The compute nodes ship a RUNTIME-ONLY CUDA: /usr/local/cuda exists and nvcc
# runs, but the dev headers are absent, so any JIT build dies with
#   fatal error: cusparse.h: No such file or directory
# The venv's pip nvidia-* wheels do carry those headers, so expose them.
_NV="$SAT_VENV/lib/python3.10/site-packages/nvidia"
if [ -d "$_NV" ]; then
    for inc in "$_NV"/*/include; do [ -d "$inc" ] && CPATH="$inc:${CPATH:-}"; done
    export CPATH
fi

# Prefer reusing the fused_adam extension already compiled on node-0 (identical
# python/torch/arch) over rebuilding per node -- the nodes cannot compile it at
# all, and a shared NFS extensions dir would reintroduce cross-node FileBaton
# lock contention. Copy into the node-local dir so each node loads a complete,
# lock-free artifact.
_PREBUILT="$SAT_PREBUILT_DIR/fused_adam"
if [ -f "$_PREBUILT/fused_adam.so" ] && [ ! -f "$TORCH_EXTENSIONS_DIR/fused_adam/fused_adam.so" ]; then
    mkdir -p "$TORCH_EXTENSIONS_DIR/fused_adam"
    cp "$_PREBUILT"/* "$TORCH_EXTENSIONS_DIR/fused_adam/" 2>/dev/null || true
    rm -f "$TORCH_EXTENSIONS_DIR/fused_adam/lock"
    echo "[node_env] seeded prebuilt fused_adam"
fi

# Clear stale torch JIT locks (now that HOME points somewhere real).
for lock in "$TORCH_EXTENSIONS_DIR"/*/lock "$TORCH_EXTENSIONS_DIR"/*/*/lock; do
    [ -e "$lock" ] || continue
    fuser "$lock" >/dev/null 2>&1 || { echo "clearing stale JIT lock: $lock"; rm -f "$lock"; }
done

echo "[node_env] node=$(hostname) HOME=$HOME (writable=$([ -w "$HOME" ] && echo yes || echo NO))"
