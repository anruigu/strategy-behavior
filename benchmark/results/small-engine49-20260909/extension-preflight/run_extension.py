"""Use the original frozen evaluation with an explicit model-only override."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'source'
sys.path[:0] = [str(SOURCE), str(SOURCE / 'hole_exp')]
from benchmark.clients import ModelConfig, write_json, now
from benchmark.fullscale import gemini_audit as audit
from benchmark.fullscale.budget import Ledger

CONFIGS = {
    'kimi-k3': ('flt', 'kimi-k3'),
    'deepseek-v4-pro': ('openrouter', 'deepseek/deepseek-v4-pro-0813'),
    'gemma-4-31b': ('openrouter', 'google/gemma-4-31b-it'),
    'qwen-3.5-9b': ('openrouter', 'qwen/qwen3.5-9b'),
    'gpt-oss-20b': ('openrouter', 'openai/gpt-oss-20b'),
}
LEDGER = BASE.parent / 'fullscale-20260908/budget.sqlite'

def config(model):
    provider, route = CONFIGS[model]
    return ModelConfig(model, provider, route,
        'https://inference.flt.build/v1' if provider == 'flt' else 'https://openrouter.ai/api/v1',
        'FLEET_API_KEY' if provider == 'flt' else 'OPENROUTER_API_KEY',
        temperature=None, reasoning_effort='low')

def verify():
    expected = json.loads((BASE / 'source-identity.json').read_text())['identical_original_files']
    for relative, sha in expected.items():
        if hashlib.sha256((SOURCE / relative).read_bytes()).hexdigest() != sha:
            raise ValueError('Frozen source changed: ' + relative)
    return len(expected)

def probe(model):
    from dataclasses import asdict
    c = config(model)
    client = audit.StudyClient(c, BASE / 'extension-preflight' / model / 'calls', Ledger(LEDGER))
    row = audit.tasks()[0]
    game = audit.GAMES[row['game']]
    state = game.initial(row['seed'])
    reply, meta = client.generate([
        dict(role='system', content=audit.SYSTEM),
        dict(role='user', content=game.observe(state))], max_tokens=16384, purpose='extension_game_canary')
    after, facts = game.transition(state, reply)
    result = dict(model=model, config=asdict(c), meta=meta, reply=reply, facts=facts, updated=now())
    write_json(BASE / 'extension-preflight' / model / 'probe.json', result)
    print(json.dumps(dict(model=model, status=meta['status'], actual_model=meta['actual_model'], facts=facts)), flush=True)
    if meta['status'] != 'ok':
        raise RuntimeError('Canary failed for ' + model)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--model', choices=CONFIGS, required=True)
    p.add_argument('--probe', action='store_true')
    p.add_argument('--workers', type=int, default=6)
    a = p.parse_args()
    verify()
    if a.probe:
        probe(a.model)
    else:
        gate = json.loads((BASE / 'extension-preflight' / a.model / 'probe.json').read_text())
        assert gate['meta']['status'] == 'ok'
        audit.CONFIG = config(a.model)
        audit.run(BASE / a.model, LEDGER, a.workers, BASE / 'targets-49.json')
