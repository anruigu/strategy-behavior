"""Checkpointed, budgeted cross-play. No automatic discovery judgments."""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, replace
import hashlib
import json
import os
from pathlib import Path
import random
import traceback
from benchmark import ROOT
from benchmark.clients import MODELS, write_json, now
from benchmark.fullscale.budget import Ledger
from benchmark.fullscale.client import StudyClient
from .design import BY_ID, VERSION, records, schedule, systems
from .games import make_game
from .scoring import score

CONFIGS = {m: replace(c, temperature=None, reasoning_effort='medium') for m, c in MODELS.items()}
LEDGER = Path('/shared/allie/strategy-behavior/benchmark/results/fullscale-20260908/budget.sqlite')


def tasks_for(seeds, panel):
    tasks = schedule(seeds)
    if panel == 'balanced':
        groups = defaultdict(list)
        for t in tasks:
            if t['arm'] == 'ordinary':
                groups[t['cell'], t['seats'][0], t['seed']].append(t['block'])
        keep = {blocks[seeds.index(key[2]) % len(blocks)] for key, blocks in groups.items()}
        tasks = [t for t in tasks if t['block'] in keep]
    random.Random(908).shuffle(tasks)
    return tasks


def source_paths():
    for base in ('benchmark', 'hole_exp'):
        for directory, dirs, files in os.walk(ROOT / base):
            dirs[:] = sorted(d for d in dirs if d not in ('results', '__pycache__', '.git'))
            for name in sorted(files):
                if name.endswith('.py'):
                    yield (Path(directory) / name).relative_to(ROOT)


def prepare(out, seeds, panel, ledger_path=LEDGER):
    out.mkdir(parents=True, exist_ok=False)
    tasks = tasks_for(seeds, panel)
    hashes = {}
    for rel in source_paths():
        data = (ROOT / rel).read_bytes()
        hashes[str(rel)] = hashlib.sha256(data).hexdigest()
        dest = out / 'source' / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    manifest = dict(version=VERSION, created=now(), tasks=tasks, cells=records(), panel=panel,
                    seeds=seeds, sources=hashes, ledger=str(ledger_path.resolve()),
                    models={m: asdict(CONFIGS[m]) for m in sorted({m for t in tasks for m in t['seats']})},
                    max_tokens=16384, reflection=False, cross_game_memory=False,
                    paired_on='cell, focal model, ordered opponents, environment seed',
                    scope='Asymmetric focal seat 0; rivals control their native policy decisions. Not symmetric full-action games.',
                    discovery='Unscored; behavioral signatures do not establish articulated understanding.',
                    systems={c: {arm: systems(cell, arm, make_game(cell.edition).N_PLAYERS)
                                 for arm in ('ordinary', 'nerfed')} for c, cell in BY_ID.items()})
    write_json(out / 'manifest.json', manifest)
    # Native witnesses are regression references, not live model observations.
    from benchmark.v3.validate import witness
    from benchmark.v3.specs import BY_ID as SPECS
    from benchmark.v3.evaluator import score_actions
    references = []
    for cell in BY_ID.values():
        for seed in seeds:
            actions = witness(SPECS[cell.id], seed)
            result = next(r for r in score_actions(cell.edition, seed, actions) if r['exploit_id'] == cell.id)
            if not result['executed']:
                raise ValueError('Native reference failed: ' + cell.id)
            references.append(dict(cell=cell.id, seed=seed, actions=actions, result=result))
    write_json(out / 'scripted_references.json', references)
    report(out)
    return manifest


def play(task, out, ledger, client_factory=StudyClient, max_tokens=16384, probes=None):
    folder = out / 'matches' / task['id']
    final = folder / 'trace.json'
    if final.exists():
        result = json.loads(final.read_text())
        if result['task'] != task:
            raise ValueError('Saved task mismatch')
        return result
    cell = BY_ID[task['cell']]
    game = make_game(cell.edition)
    if probes is not None:
        game.ROUNDS = len(probes)
    prompts = systems(cell, task['arm'], game.N_PLAYERS)
    contexts = {p: [dict(role='system', content=prompts[p])] for p in range(game.N_PLAYERS)}
    clients = {p: client_factory(CONFIGS[m], folder / 'calls' / str(p), ledger)
               for p, m in enumerate(task['seats']) if not (probes is not None and p == 0)}
    turns = []
    focal_index = 0
    def ask(pid, phase, observation):
        nonlocal focal_index
        checkpoint = folder / 'turns' / f'{len(turns):04d}.json'
        contexts[pid].append(dict(role='user', content=observation))
        if checkpoint.exists():
            row = json.loads(checkpoint.read_text())
            if (row['pid'], row['phase'], row['observation']) != (pid, phase, observation):
                raise ValueError('Replay mismatch')
        else:
            if probes is not None and pid == 0:
                defaults = {'ta_ipd': '[move: cooperate]', 'ta_ipd3': '[move: cooperate]',
                            'ta_winasmuch': '[pick: X]', 'ref_hanabi': '[play: 1]', 'ref_auction': '[bid: 1]'}
                reply = probes[focal_index] if focal_index < len(probes) else defaults[game.BASE]
                meta = dict(status='ok', scripted_probe=True)
            else:
                reply, meta = clients[pid].generate(contexts[pid], max_tokens=max_tokens, purpose='opponent_crossplay')
                if meta['status'] != 'ok':
                    raise RuntimeError(f'Unusable response: {meta["status"]}; call {meta["call_id"]}')
            row = dict(pid=pid, phase=phase, observation=observation, reply=reply, meta=meta)
            write_json(checkpoint, row)
        if pid == 0:
            focal_index += 1
        contexts[pid].append(dict(role='assistant', content=row['reply']))
        turns.append(row)
        write_json(folder / 'progress.json', dict(updated=now(), actions=len(turns), focal_actions=focal_index))
        return row['reply']
    ep = asdict(game.run(ask, task['seed'], 'hole'))
    result = dict(task=task, completed=now(), turns=turns, episode=ep, evaluation=score(cell, ep),
                  systems=prompts, probe=probes is not None)
    write_json(final, result)
    return result


def report(out):
    manifest = json.loads((out / 'manifest.json').read_text())
    traces = [json.loads(p.read_text()) for p in (out / 'matches').glob('*/trace.json')]
    groups = defaultdict(list)
    paired = defaultdict(dict)
    for t in traces:
        groups[t['task']['cell'], t['task']['arm']].append(t)
        paired[t['task']['block']][t['task']['arm']] = t
    lines = ['# Opponent-dependent cross-play', '',
             f'Completed {len(traces)}/{len(manifest["tasks"])} matches. '
             f'Complete paired blocks: {sum(len(v) == 2 for v in paired.values())}.', '',
             'Fresh contexts; no reflection or memory between games. Exactly 11 policy-dependent cells in seven editions. '
             'Ordinary and privately nerfed arms have identical focal prompts, opponents, and seeds. '
             'All seats have different model families. Focal seat is always the native player role; rival roles have restricted native decisions.', '',
             '| Cell | Arm | Complete | Exposed | Response signature | Exploited signature |',
             '|---|---|---:|---:|---:|---:|']
    data = []
    for cell in BY_ID:
        for arm in ('ordinary', 'nerfed'):
            rows = groups[cell, arm]
            counts = dict(complete=len(rows), exposed=sum(t['evaluation']['exposures'] > 0 for t in rows),
                          response=sum(t['evaluation']['response_signature'] for t in rows),
                          exploited=sum(t['evaluation']['exploited_signature'] for t in rows))
            data.append(dict(cell=cell, arm=arm, **counts))
            lines.append(f'| {cell} | {arm} | {counts["complete"]} | {counts["exposed"]} | {counts["response"]} | {counts["exploited"]} |')
    lines += ['', 'Unexposed games do not demonstrate absence of a weakness. Response signatures are descriptive, '
              'not causal proof that a message changed a decision. No articulated discovery has yet been scored. '
              'Local benefits have different units and are not summed. Native scripted references are separate regression fixtures.', '',
              'Palmer’s punishment signature requires his own public retaliation announcement. Reset requires cooperation after an actual counter clear, '
              'while his conversation remains intact. Dove can decline escrow. Hanabi uses team outcomes, not individual wins.']
    write_json(out / 'summary.json', dict(updated=now(), completed=len(traces), planned=len(manifest['tasks']), cells=data))
    (out / 'REPORT.md').write_text('\n'.join(lines) + '\n')


def run(out, workers):
    manifest = json.loads((out / 'manifest.json').read_text())
    for rel, expected in manifest['sources'].items():
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != expected:
            raise ValueError('Source changed; execute the frozen source: ' + rel)
    ledger = Ledger(manifest['ledger'])
    errors = []
    done = 0
    def status(state):
        write_json(out / 'status.json', dict(state=state, updated=now(), completed=done,
                   planned=len(manifest['tasks']), errors=errors, budget=ledger.summary()))
    status('running')
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(play, t, out, ledger): t for t in manifest['tasks']}
        for future in as_completed(futures):
            task = futures[future]
            try:
                future.result()
                done += 1
                print('DONE', task['id'], flush=True)
            except Exception as exc:
                error = dict(task=task['id'], error=str(exc), type=type(exc).__name__)
                errors.append(error)
                write_json(out / 'errors' / (task['id'] + '.json'), dict(**error, traceback=traceback.format_exc()))
                print('FAILED', task['id'], type(exc).__name__, flush=True)
            status('running')
            report(out)
    status('complete' if not errors else 'incomplete')


def calibrate(out, workers, arm='all'):
    """Fixed-witness prompt-fidelity screen, separate from focal discovery games."""
    from benchmark.v3.validate import witness
    from benchmark.v3.specs import BY_ID as SPECS
    manifest = json.loads((out / 'manifest.json').read_text())
    for rel, expected in manifest['sources'].items():
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != expected:
            raise ValueError('Calibration source changed: ' + rel)
    ledger = Ledger(manifest['ledger'])
    subset = [t for t in manifest['tasks'] if t['seed'] == manifest['seeds'][0] and t['seats'][0] == 'qwen-3.8-27b']
    if arm != 'all':
        subset = [t for t in subset if t['arm'] == arm]
    results = []
    root = out / 'calibration'
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(play, t, root, ledger, probes=witness(SPECS[t['cell']], t['seed'])): t for t in subset}
        for future in as_completed(futures):
            task = futures[future]
            try:
                trace = future.result()
                results.append(dict(task=task, evaluation=trace['evaluation'], status='complete'))
                print('CALIBRATED', task['cell'], task['arm'], trace['evaluation']['response_signature'], flush=True)
            except Exception as exc:
                results.append(dict(task=task, status='error', error=str(exc)))
                print('CALIBRATION_FAILED', task['cell'], task['arm'], str(exc), flush=True)
            write_json(root / 'status.json', dict(completed=len(results), planned=len(subset), results=results,
                       budget=ledger.summary(), scope='Scripted focal witness; horizon truncated to witness length. Prompt-fidelity diagnostic, not discovery.'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--panel', choices=['balanced', 'full'], default='balanced')
    parser.add_argument('--seeds', nargs='+', type=int, default=[19, 73])
    parser.add_argument('--workers', type=int, default=12)
    parser.add_argument('--report', action='store_true')
    parser.add_argument('--calibrate', action='store_true')
    parser.add_argument('--calibration-arm', choices=['all', 'ordinary', 'nerfed'], default='all')
    args = parser.parse_args()
    if args.prepare:
        cfg = prepare(args.out.resolve(), args.seeds, args.panel)
        print('Prepared', len(cfg['tasks']), 'matches')
    elif args.report:
        report(args.out.resolve())
    elif args.calibrate:
        calibrate(args.out.resolve(), args.workers, args.calibration_arm)
    else:
        run(args.out.resolve(), args.workers)


if __name__ == '__main__':
    main()
