# Play-data backups

Active Kubernetes CronJob: `fleet-train-jobs/plays-data-backup`.
Runs at 00:00, 02:00, …, 22:00 UTC (`0 */2 * * *`). The job mounts
`sfs-shared:allie/plays_data` read-only and includes all files recursively,
including assignment logs, feedback, per-game plays, and per-player copies.
It does not restart or modify the play server.

Each run writes an independently restorable archive and completion manifest:

```
s3://fleet-research/gameable_games/snapshots/YYYY/MM/DD/<UTC timestamp>-<id>.tar.gz
s3://fleet-research/gameable_games/snapshots/YYYY/MM/DD/<UTC timestamp>-<id>.json
```

Archives contain `plays_data/` and `manifest.json`. The external JSON includes
the archive's SHA-256, size, and completion timestamp; it is written only after
S3 confirms the uploaded archive's size and checksum metadata. Each file has
its own SHA-256 and size. Historical snapshots are never overwritten or deleted
by this workflow. Existing bucket lifecycle policies still apply.

The source remains live during capture. Each file is copied to its initially
observed length; incomplete trailing JSONL records are deferred to the next
backup. Complete JSONL lines are validated. This is a per-file snapshot, not
an atomic transaction across duplicated game/player records. In-memory moves
that the play server has not yet flushed cannot be backed up from disk.

## Deploy or update

The CronJob is managed independently from the Argo-managed play-server workload.
Run from the repository root:

```sh
kubectl create configmap plays-data-backup-script -n fleet-train-jobs \
  --from-file=backup.py=ops/plays-backup/backup.py --dry-run=client -o yaml |
  kubectl apply -f -
kubectl apply -f ops/plays-backup/cronjob.yaml
```

The existing `plays-data-backup-s3` Secret contains the AWS access-key credentials
used by this job. It was provisioned from the operator's AWS environment, not
committed to git. Update this Secret when those credentials rotate. The job
requires write/read access under `fleet-research/gameable_games/` for uploads and
verification. It needs no Kubernetes API token. Boto3 is version-pinned and
installed into temporary storage at startup.

## Operate and restore

```sh
kubectl get cronjob plays-data-backup -n fleet-train-jobs
kubectl get jobs -n fleet-train-jobs
kubectl create job plays-data-backup-manual-<unique-id> \
  --from=cronjob/plays-data-backup -n fleet-train-jobs
kubectl logs -n fleet-train-jobs job/<job-name>
```

Overlapping scheduled runs are forbidden. A job retries twice and has a one-hour
deadline. Failed Jobs remain inspectable; this workflow does not send alerts.

To restore, select a snapshot with its external completion JSON, download both,
verify the archive SHA-256 against `archive_sha256`, and extract into a fresh
directory. The files under `plays_data/` reproduce the recorded snapshot; the
internal manifest lists their checksums. Restore separately before replacing
any live files.

Initial backup on 2026-09-10 succeeded. Its archive was downloaded and all 134
file sizes and SHA-256 checksums verified. Tests: `python ops/plays-backup/test_backup.py`.
