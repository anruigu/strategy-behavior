#!/usr/bin/env python
"""Upload a checkpoint directory to S3.

    s3_upload_dir.py <local-dir> <bucket> <key-prefix>

Mirrors the approach in SkyRL-Fleet's integrations/fleet/s3_checkpoints.py:
multipart transfer config, concurrent uploads, one key per file under
<key-prefix>/<relative-path>. Credentials come from AWS_ACCESS_KEY_ID /
AWS_SECRET_ACCESS_KEY (both live in the dotenv referenced by $SAT_ENV_FILE).
"""
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import boto3
from boto3.s3.transfer import TransferConfig


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    local_dir, bucket, prefix = sys.argv[1], sys.argv[2], sys.argv[3].strip("/")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    # 8MB chunks: the safetensors shards are multi-GB, so single-part PUTs
    # would both fail the 5GB limit and lose retry granularity.
    cfg = TransferConfig(multipart_threshold=8 * 1024 * 1024,
                         multipart_chunksize=8 * 1024 * 1024,
                         max_concurrency=8)

    files = []
    for root, _, names in os.walk(local_dir):
        for n in names:
            if n.startswith("."):        # skip .s3-uploaded marker etc.
                continue
            p = os.path.join(root, n)
            files.append((p, f"{prefix}/{os.path.relpath(p, local_dir)}"))

    total = sum(os.path.getsize(p) for p, _ in files)
    print(f"uploading {len(files)} files, {total / 1e9:.2f} GB -> s3://{bucket}/{prefix}/")

    failed = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(s3.upload_file, p, bucket, k, Config=cfg): (p, k) for p, k in files}
        for f in as_completed(futs):
            p, k = futs[f]
            try:
                f.result()
            except Exception as e:                      # noqa: BLE001
                failed.append((k, f"{type(e).__name__}: {e}"))

    if failed:
        for k, e in failed[:5]:
            print(f"  FAILED {k}: {e}", file=sys.stderr)
        print(f"{len(failed)}/{len(files)} uploads failed", file=sys.stderr)
        return 1
    print(f"OK: {len(files)} files -> s3://{bucket}/{prefix}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
