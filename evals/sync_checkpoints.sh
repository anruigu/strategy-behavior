#!/usr/bin/env bash
# sync_checkpoints.sh -- persist oat checkpoints off ephemeral disk.
#
#   sync_checkpoints.sh <src-save-path> <run-label> [interval-seconds]
#
# Why this exists: oat writes checkpoints under --save_path, and on this cluster
# a node's $HOME (and therefore /home/allie/oat-output) is node-LOCAL container
# overlay -- it does not survive a restart and is invisible from other nodes, so
# a checkpoint written there cannot even be evaluated elsewhere. Shared
# /workspace is the durable location.
#
# Tier 1 (always): mirror to $SAT_CKPT_DIR/<run-label>/<step>.
#   Step dirs are renamed colon-free; the NFS volume rejects ':' in filenames,
#   which is also why oat's default save_path could not point at /workspace.
# Tier 2 (optional): mirror to s3://$S3_CHECKPOINT_BUCKET/$S3_PREFIX/, matching
#   SkyRL-Fleet's integrations/fleet/s3_checkpoints.py convention
#   (<project>/<model>/<run>/<checkpoint>). Enabled only when
#   S3_CHECKPOINT_BUCKET is set, because a full 400-step run at --save_steps 16
#   is 25 x 7.6GB = ~190GB per run. S3_UPLOAD_EVERY bounds that: with the
#   default of 64 only steps 64/128/192/... plus the final are uploaded (~6
#   checkpoints, ~46GB), while /workspace still holds every one.
set -uo pipefail
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
source "$SAT_HOME/config.sh"
SRC="${1:?usage: sync_checkpoints.sh <src-save-path> <run-label> [interval]}"
LABEL="${2:?run label}"
INTERVAL="${3:-300}"
DEST="$SAT_CKPT_DIR/$LABEL"
S3_UPLOAD_EVERY="${S3_UPLOAD_EVERY:-64}"
S3_PREFIX="${S3_PREFIX:-spiral/qwen3-4b-base/$LABEL}"
mkdir -p "$DEST"

log() { echo "[sync $LABEL $(date -u +%H:%M:%S)] $*"; }
log "src=$SRC dest=$DEST s3=${S3_CHECKPOINT_BUCKET:-disabled} every=$S3_UPLOAD_EVERY interval=${INTERVAL}s"

while true; do
    for d in "$SRC"/*/saved_models/step_* "$SRC"/saved_models/step_*; do
        [ -d "$d" ] || continue
        step="$(basename "$d")"                     # step_00064
        n=$((10#$(echo "$step" | tr -dc '0-9')))    # 64
        # A checkpoint is only complete once its index and both shards are there;
        # copying mid-write would produce a silently truncated model.
        [ -f "$d/model.safetensors.index.json" ] || continue
        # MIRROR=0: the run already writes to durable /workspace, so skip tier 1
        # and upload in place rather than duplicating ~190GB per run.
        if [ "${MIRROR:-1}" = "0" ]; then
            out="$d"
        else
            out="$DEST/$step"
        fi
        if [ "${MIRROR:-1}" != "0" ] && [ ! -d "$out" ]; then
            log "mirroring $step -> $out"
            cp -r "$d" "$out.partial" && mv "$out.partial" "$out" && log "  mirrored $step ($(du -sh "$out" | cut -f1))"
        fi
        # S3 tier
        if [ -n "${S3_CHECKPOINT_BUCKET:-}" ] && [ -d "$out" ] && [ ! -f "$out/.s3-uploaded" ]; then
            if [ $((n % S3_UPLOAD_EVERY)) -eq 0 ]; then
                log "uploading $step -> s3://$S3_CHECKPOINT_BUCKET/$S3_PREFIX/$step/"
                if "$SAT_TOOLS_PY" "$SAT_HOME/evals/s3_upload_dir.py" \
                       "$out" "$S3_CHECKPOINT_BUCKET" "$S3_PREFIX/$step"; then
                    touch "$out/.s3-uploaded"; log "  uploaded $step"
                else
                    log "  upload FAILED for $step (will retry next pass)"
                fi
            fi
        fi
    done
    sleep "$INTERVAL"
done
