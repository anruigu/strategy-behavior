"""Grant local researchers read access to this Fleet job's generated artifacts."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import stat
import time


def expose(root):
    changed = 0
    paths = [root/'fleet-runtime/model-preflight.json']
    for name in ('baselines', 'transformer', 'embedding-cache'):
        folder = root/name
        if folder.exists():
            paths.append(folder)
            paths.extend(folder.rglob('*'))
    for name in ('baselines', 'frozen', 'lora'):
        folder = root/'fresh-forecasts'/name
        if folder.exists():
            paths.append(folder)
            paths.extend(folder.rglob('*'))
    for path in paths:
        try:
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode) or info.st_uid != os.getuid():
                continue
            extra = 0o005 if stat.S_ISDIR(info.st_mode) else 0o004
            mode = stat.S_IMODE(info.st_mode)
            if mode & extra != extra:
                path.chmod(mode | extra)
                changed += 1
        except FileNotFoundError:
            pass  # Atomic writers can rename between the directory walk and stat.
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', required=True)
    parser.add_argument('--job', required=True)
    parser.add_argument('--deadline', required=True)
    args = parser.parse_args()
    root = Path(args.run_root).resolve()
    if (not root.is_relative_to('/mnt/sfs/allie/strategy-behavior/prediction/results/improve-20260910')
            or os.environ.get('FLEET_RUN_NAME') != args.job):
        raise ValueError('Only the current authorized Fleet job and study outputs may be changed')
    deadline = datetime.fromisoformat(args.deadline).timestamp()
    log = root/'fleet-runtime/artifact-access.jsonl'
    while time.time() < deadline:
        count = expose(root)
        if count:
            with log.open('a') as stream:
                stream.write(json.dumps({'at': datetime.now(timezone.utc).isoformat(),
                    'job': args.job, 'files_or_directories_made_readable': count,
                    'contents_changed': False})+'\n')
        status = json.loads((root/'fleet-runtime/training-status.json').read_text())
        if status.get('fleet_run_id') == args.job and status.get('status') in ('complete', 'error', 'failed'):
            expose(root)
            return
        time.sleep(1)


if __name__ == '__main__':
    main()
