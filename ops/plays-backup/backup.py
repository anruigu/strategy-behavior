"""Take a bounded copy of live append-only play files and retain it in S3."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tarfile
import tempfile
import uuid


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def snapshot(source, destination):
    if not source.is_dir():
        raise ValueError(f'Missing source directory: {source}')
    files = []
    # Capture sizes before copying; concurrent appends belong to the next backup.
    for path in sorted(source.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Refusing symlink: {path}')
        if path.is_file():
            files.append((path, path.stat().st_size))
    if not files:
        raise ValueError('Refusing an empty backup')
    records = []
    for path, size in files:
        relative = path.relative_to(source)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with path.open('rb') as src, target.open('w+b') as dst:
            remaining = size
            while remaining:
                block = src.read(min(remaining, 1024 * 1024))
                if not block:
                    raise ValueError(f'Source shrank during backup: {relative}')
                dst.write(block)
                remaining -= len(block)
            if path.suffix == '.jsonl':
                # A writer may be halfway through a record. Keep complete lines only.
                end = size
                while end:
                    start = max(0, end - 65536)
                    dst.seek(start)
                    block = dst.read(end - start)
                    newline = block.rfind(b'\n')
                    if newline >= 0:
                        end = start + newline + 1
                        break
                    end = start
                dst.truncate(end)
        if path.suffix == '.jsonl':
            with target.open('rb') as stream:
                for line in stream:
                    json.loads(line)
        records.append(dict(path=str(relative), source_bytes=size,
                            bytes=target.stat().st_size, sha256=digest(target)))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('/data'))
    parser.add_argument('--bucket', default='fleet-research')
    parser.add_argument('--prefix', default='gameable_games')
    args = parser.parse_args()
    import boto3
    from botocore.config import Config
    s3 = boto3.client('s3', config=Config(retries={'mode': 'standard', 'max_attempts': 5}))
    now = datetime.now(timezone.utc)
    snapshot_id = now.strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:12]
    key = f"{args.prefix.rstrip('/')}/snapshots/{now:%Y/%m/%d}/{snapshot_id}.tar.gz"
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        tree = work / 'plays_data'
        tree.mkdir()
        records = snapshot(args.source, tree)
        manifest = dict(schema=1, snapshot_id=snapshot_id, started_at=now.isoformat(),
                        source=str(args.source), consistency='complete JSONL lines; per-file captured lengths',
                        files=records)
        (work / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        archive = work / 'plays_data.tar.gz'
        with tarfile.open(archive, 'w:gz') as tar:
            tar.add(tree, arcname='plays_data')
            tar.add(work / 'manifest.json', arcname='manifest.json')
        checksum = digest(archive)
        s3.upload_file(str(archive), args.bucket, key,
                       ExtraArgs={'ServerSideEncryption': 'AES256', 'Metadata': {'sha256': checksum}})
        head = s3.head_object(Bucket=args.bucket, Key=key)
        if head['ContentLength'] != archive.stat().st_size or head['Metadata'].get('sha256') != checksum:
            raise RuntimeError('Uploaded archive verification failed')
        manifest.update(archive_key=key, archive_bytes=archive.stat().st_size,
                        archive_sha256=checksum, completed_at=datetime.now(timezone.utc).isoformat())
        # This completion marker is published only after the archive upload succeeds.
        s3.put_object(Bucket=args.bucket, Key=key.removesuffix('.tar.gz') + '.json',
                      Body=json.dumps(manifest, indent=2).encode(), ContentType='application/json',
                      ServerSideEncryption='AES256')
        print(json.dumps({'archive': f's3://{args.bucket}/{key}', 'files': len(records),
                          'archive_bytes': archive.stat().st_size, 'sha256': checksum}), flush=True)


if __name__ == '__main__':
    main()
