"""Join the primary pilot's unchanged legacy pairs and replacement-model pairs."""
import argparse
from collections import Counter
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from prediction.io_utils import digest, now, read_json, write_json


def combine(run_root, output=None):
    primary = read_json(run_root/'primary-pilot-manifest.json')
    desired = {s['id']: s for s in primary['episodes']}
    games = {g['id']: g for g in primary['games']}
    rows, provenance, seen = [], [], set()
    for source in ('pilot','pilot-oss'):
        folder = run_root/source
        subprocess.run([sys.executable, '-B', str(run_root/'source/prediction/study.py'), 'collect',
                        '--stage-root', str(folder)], cwd=run_root/'source', check=True, stdout=subprocess.DEVNULL)
        manifest = read_json(folder/'manifest.json')
        assert manifest['protocol'] == primary['protocol']
        assert manifest['sources'] == primary['sources']
        summary = read_json(folder/'collected/summary.json')
        if summary['errors']:
            raise RuntimeError('Original trace integrity audit failed: '+str(summary['errors'][:2]))
        for row in read_json(folder/'collected/records.json'):
            if row['model'] not in primary['models'] or row['opponent'] not in primary['models']:
                continue
            spec = desired[row['episode_id']]
            player = row['player_index']
            assert row['model'] == spec['models'][player] and row['opponent'] == spec['models'][1-player]
            assert row['payoffs'] == games[row['game_id']]['payoffs']
            assert row['features'] == games[row['game_id']]['features']
            assert row['group_id'] == games[row['game_id']]['group_id']
            assert row['trial_id'] == spec['trial_id'] and row['swap'] == spec['swap']
            assert row['representation'] == spec['representation']
            for name in (row['model'],row['opponent']):
                assert manifest['models'][name] == primary['models'][name]
            key = row['episode_id'],player
            assert key not in seen, 'Duplicate primary outcome'
            seen.add(key)
            row.update(stage='primary_pilot',source_stage=source)
            rows.append(row)
        provenance.append(dict(source_stage=source, manifest_sha256=digest(manifest),
                               collected_summary=summary, trace_provenance=str((folder/'collected/provenance.json').resolve())))
    order = {s['id']: i for i,s in enumerate(primary['episodes'])}
    rows.sort(key=lambda row:(order[row['episode_id']],row['player_index']))
    episodes = Counter(r['episode_id'] for r in rows)
    assert all(n == 2 for n in episodes.values())
    summary = dict(updated=now(), complete_episodes=len(episodes), planned_episodes=len(desired),
                   records=len(rows), games=len({r['game_id'] for r in rows}),
                   models=Counter(r['model'] for r in rows), families=Counter(r['family'] for r in rows),
                   missing_episodes=sorted(set(desired)-set(episodes)), integrity_errors=0,
                   roster=list(primary['models']), source_compatibility='exact protocol/game/source/actual used configurations; original trace audits retained')
    out = output or run_root/'primary-pilot'
    write_json(out/'records.json',rows)
    write_json(out/'summary.json',summary)
    write_json(out/'provenance.json',provenance)
    return summary


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-root',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    summary=combine(args.run_root,args.output)
    print({k:v for k,v in summary.items() if k!='missing_episodes'})
