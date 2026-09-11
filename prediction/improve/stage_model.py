"""Stage a pinned public model in user-owned storage; does not load or fit it."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

MODEL = 'Qwen/Qwen3-4B'
REVISION = '1cfa9a7208912126459214e8b04321603b3df60c'
ROOT = Path('/shared/allie/strategy-behavior/prediction/results/improve-20260910/model')
SNAPSHOT = ROOT / REVISION

def fetch(name):
    target = SNAPSHOT / name
    if not target.exists():
        url = f'https://huggingface.co/{MODEL}/resolve/{REVISION}/{name}'
        part = target.with_suffix(target.suffix + '.part')
        print('Downloading '+name, flush=True)
        with urllib.request.urlopen(url, timeout=300) as src, part.open('wb') as out:
            while block := src.read(4*1024*1024):
                out.write(block)
        part.replace(target)
    h = hashlib.sha256()
    with target.open('rb') as handle:
        while block := handle.read(4*1024*1024):
            h.update(block)
    print('Verified '+name+' '+str(target.stat().st_size)+' bytes', flush=True)
    return name, h.hexdigest()

def main():
    SNAPSHOT.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(f'https://huggingface.co/api/models/{MODEL}/revision/{REVISION}',timeout=60) as response:
        info = json.load(response)
    assert info['sha'] == REVISION
    (ROOT/'model-api.json').write_text(json.dumps(info,indent=2)+'\n')
    names = [x['rfilename'] for x in info['siblings'] if x['rfilename'] != '.gitattributes']
    if any('/' in name or '..' in name for name in names):
        raise ValueError('Unexpected nested model artifact')
    with ThreadPoolExecutor(max_workers=4) as pool:
        hashes = dict(pool.map(fetch, names))
    manifest = {'model_id':MODEL,'revision':REVISION,'files':hashes,
                'staged_at':datetime.now(timezone.utc).isoformat(), 'snapshot_path':str(SNAPSHOT),
                'remote_snapshot_path':str(SNAPSHOT).replace('/shared/','/mnt/sfs/',1)}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Staged pinned model snapshot',flush=True)

if __name__ == '__main__':
    main()
