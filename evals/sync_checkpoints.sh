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
# Tier 1: mirror to $SAT_CKPT_DIR/<run-label>/<step>.
#   Step dirs are renamed colon-free; the NFS volume rejects ':' in filenames,
#   which is also why oat's default save_path could not point at /workspace.
#
#   THINNED BY DEFAULT. A 400-step run at --save_steps 16 produces 25
#   checkpoints, and a Qwen3-4B bf16 checkpoint is 7.6GB, so mirroring all of
#   them costs ~190GB per run -- at which point /workspace (shared with other
#   users) fits only ~4 more runs. MIRROR_EVERY bounds tier 1 the same way
#   S3_UPLOAD_EVERY has always bounded tier 2: with the default of 64 only
#   steps 64/128/192/256/320/384 are mirrored, ~53GB per run, ~15 runs.
#
#   MIRROR_EVERY should be a MULTIPLE OF --save_steps or the modulo never hits
#   and nothing is mirrored; the startup log prints which steps a 400-step run
#   would keep so a bad pairing is obvious immediately.
#
#   The final checkpoint is usually NOT a multiple of MIRROR_EVERY (400 % 64 !=
#   0) and it is the one checkpoint you always want. Pin it with MIRROR_STEPS,
#   which is a comma-separated list of step numbers mirrored regardless of the
#   cadence -- the run scripts export it as max_train/rollout_batch_size.
#
#     MIRROR_EVERY=64 MIRROR_STEPS=400 sync_checkpoints.sh ...  # 7 ckpts, ~53GB
#     MIRROR_EVERY=16 sync_checkpoints.sh ...                   # every one, ~190GB
#     MIRROR_EVERY=0 MIRROR_STEPS=256,400 sync_checkpoints.sh ...  # only those two
#
# Tier 2 (optional): mirror to s3://$S3_CHECKPOINT_BUCKET/$S3_PREFIX/, matching
#   SkyRL-Fleet's integrations/fleet/s3_checkpoints.py convention
#   (<project>/<model>/<run>/<checkpoint>). Enabled only when
#   S3_CHECKPOINT_BUCKET is set. Its cadence is independent of tier 1's: a step
#   that tier 1 thinned away is uploaded straight from the source copy, so
#   S3_UPLOAD_EVERY still means what it always meant.
set -uo pipefail
SAT_HOME="${SAT_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
source "$SAT_HOME/config.sh"
SRC="${1:?usage: sync_checkpoints.sh <src-save-path> <run-label> [interval]}"
LABEL="${2:?run label}"
INTERVAL="${3:-300}"
DEST="$SAT_CKPT_DIR/$LABEL"
MIRROR_EVERY="${MIRROR_EVERY:-64}"
MIRROR_STEPS="${MIRROR_STEPS:-}"
S3_UPLOAD_EVERY="${S3_UPLOAD_EVERY:-64}"
S3_PREFIX="${S3_PREFIX:-spiral/qwen3-4b-base/$LABEL}"
mkdir -p "$DEST"

log() { echo "[sync $LABEL $(date -u +%H:%M:%S)] $*"; }

# Steps pinned regardless of the MIRROR_EVERY cadence (comma- or space-separated).
MIRROR_STEPS_LIST="${MIRROR_STEPS//,/ }"

# want_mirror <step-number> -- is this checkpoint one tier 1 keeps?
want_mirror() {
    local n="$1" s
    if [ "$MIRROR_EVERY" -gt 0 ] && [ $((n % MIRROR_EVERY)) -eq 0 ]; then
        return 0
    fi
    for s in $MIRROR_STEPS_LIST; do
        [ "$n" -eq "$s" ] && return 0
    done
    return 1
}

# Show the selection up front against the standard 400-step/save_steps-16
# schedule. A MIRROR_EVERY that divides nothing prints an empty list here
# rather than silently mirroring nothing for six hours.
preview=""
for n in $(seq 16 16 400); do want_mirror "$n" && preview="$preview $n"; done
log "src=$SRC dest=$DEST interval=${INTERVAL}s"
log "tier1: MIRROR_EVERY=$MIRROR_EVERY MIRROR_STEPS=${MIRROR_STEPS:-none}" \
    "-> would keep steps:${preview:- NONE (check MIRROR_EVERY vs --save_steps)}"
log "tier2: s3=${S3_CHECKPOINT_BUCKET:-disabled} every=$S3_UPLOAD_EVERY"

# Steps we have already logged a tier-1 skip for, so the reason is stated once
# per checkpoint instead of once per polling pass.
declare -A skip_logged=()

while true; do
    for d in "$SRC"/*/saved_models/step_* "$SRC"/saved_models/step_*; do
        [ -d "$d" ] || continue
        step="$(basename "$d")"                     # step_00064
        n=$((10#$(echo "$step" | tr -dc '0-9')))    # 64
        # A checkpoint is only complete once its index and both shards are there;
        # copying mid-write would produce a silently truncated model.
        [ -f "$d/model.safetensors.index.json" ] || continue
        # MIRROR=0: the run already writes to durable /workspace, so skip tier 1
        # and upload in place rather than duplicating the run.
        if [ "${MIRROR:-1}" = "0" ]; then
            out="$d"
        else
            out="$DEST/$step"
            if [ ! -d "$out" ]; then
                if want_mirror "$n"; then
                    log "mirroring $step -> $out"
                    cp -r "$d" "$out.partial" && mv "$out.partial" "$out" && log "  mirrored $step ($(du -sh "$out" | cut -f1))"
                else
                    # Thinned out of tier 1. Point the S3 tier at the source copy
                    # so its cadence is unaffected by tier 1's.
                    out="$d"
                    if [ -z "${skip_logged[$step]:-}" ]; then
                        log "not mirroring $step (MIRROR_EVERY=$MIRROR_EVERY, not pinned in MIRROR_STEPS)"
                        skip_logged[$step]=1
                    fi
                fi
            fi
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
