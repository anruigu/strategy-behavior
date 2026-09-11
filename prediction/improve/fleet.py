"""Small durable client for the authorized Fleet training experiment.

POST submission is intentionally never retried: reconcile an ambiguous response
against the caller's run history before attempting another allocation.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
import re
from pathlib import Path
import sys
import urllib.request

BASE = 'https://api.ft.flt.build'

def now():
    return datetime.now(timezone.utc).isoformat()

def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    os.chmod(temp, 0o600)
    temp.replace(path)

def key():
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'hole_exp'))
    from run_referee_crossplay import _from_files, load_env_key
    value = _from_files('FLEET_API_KEY') or load_env_key('FLEET_API_KEY')
    if not value:
        raise RuntimeError('FLEET_API_KEY unavailable')
    return value

def request(method, path, payload=None, timeout=120):
    raw = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(BASE + path, data=raw, method=method,
        headers={'Authorization': 'Bearer ' + key(), 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body=response.read()
        return json.loads(body) if body.strip() else {'http_status':response.status,'empty_response':True}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['whoami', 'preview', 'submit', 'status', 'cancel', 'list'])
    parser.add_argument('--config')
    parser.add_argument('--name')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    if args.action in ('submit', 'preview'):
        config = json.loads(Path(args.config).read_text())
        if config['gpus_per_worker'] != 1 or config['workers'] != 1:
            raise ValueError('This experiment authorizes one-GPU jobs only')
        if not config['run_dir'].startswith('/mnt/sfs/allie/'):
            raise ValueError('Outputs must remain in user storage')
        if args.action == 'submit':
            intent = Path(args.out).with_suffix('.intent.json')
            if intent.exists() or Path(args.out).exists():
                raise RuntimeError('Submission already attempted; reconcile status, do not duplicate')
            write(intent, {'attempted_at': now(), 'config': config})
        result = request('POST', '/v1/runs' + ('/preview' if args.action == 'preview' else ''), config)
    elif args.action == 'whoami':
        result = request('GET', '/v1/whoami')
    elif args.action == 'list':
        from urllib.parse import urlencode
        identity = request('GET', '/v1/whoami')
        owner = identity.get('profile_id') or identity.get('attribution_email') or identity['email']
        result = request('GET', '/v1/runs?' + urlencode({'submitted_by':owner,'limit':100}))
    else:
        if not args.name or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', args.name):
            raise ValueError('Expected a returned Fleet run name')
        result = request('DELETE' if args.action == 'cancel' else 'GET', '/v1/runs/' + args.name)
    write(args.out, {'recorded_at': now(), 'action': args.action, 'response': result})
    # Never print a rendered manifest, identity, or authentication material.
    if isinstance(result, dict):
        print(json.dumps({k:result[k] for k in ('name','status','run_dir','warnings') if k in result}))
    print('Saved ' + args.out)

if __name__ == '__main__':
    main()
