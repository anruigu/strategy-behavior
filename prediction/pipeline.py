"""Durable execution through the matrix pilot and numerical generalization gates.

Paid expansion is conditional on collection integrity and measurable variability.
No Gate 8 work is launched here. Logs and every gate decision are durable.
"""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import fcntl
import hashlib
from itertools import combinations_with_replacement
import os
from pathlib import Path
import random
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from prediction.io_utils import digest, now, read_json, write_json

PYTHON = '/shared/allie/venvs/hole/bin/python'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR='/shared/allie/home/.codex/tmp',
           OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
           MPLCONFIGDIR='/shared/allie/home/.codex/tmp/matplotlib-prediction',
           JOBLIB_TEMP_FOLDER='/shared/allie/home/.codex/tmp/joblib-prediction')


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def command_contract(arguments):
    inputs={}
    input_flags={'--input','--records','--games','--players','--training-records','--artifact',
                 '--manifest','--forecasts','--llm-forecasts','--planned-rows',
                 '--pilot-records','--controls-records','--controls-manifest'}
    # --artifact is an output for fitting and an input for forecasting.
    for index,argument in enumerate(arguments[:-1]):
        if argument in input_flags and not (argument=='--artifact' and 'fit' in arguments):
            path=Path(arguments[index+1]).resolve()
            inputs[str(path)]=file_hash(path)
        elif argument=='--stage-root':
            path=Path(arguments[index+1]).resolve()/'manifest.json'
            inputs[str(path)]=file_hash(path)
        elif argument=='--run-root':
            folder=Path(arguments[index+1]).resolve()
            for relative in ('primary-pilot-manifest.json','pilot/manifest.json','pilot/resume-manifest.json','pilot-oss/manifest.json'):
                path=folder/relative
                if path.exists():
                    inputs[str(path)]=file_hash(path)
    module=arguments[1].replace('.','/')+'.py' if arguments[0]=='-m' else arguments[0]
    entry=Path(module).resolve()
    base=entry.parents[1]
    sources={str(entry):file_hash(entry)}
    for name in ('modeling.py','analysis.py','games.py','measurements.py','diagnostics.py',
                 'prospective.py','llm_forecast.py','io_utils.py','runner.py','study.py'):
        path=base/'prediction'/name
        if path.exists():
            sources[str(path)]=file_hash(path)
    return dict(command=arguments,input_hashes=inputs,source_hashes=sources)


def command_outputs(arguments):
    files=set()
    for index,argument in enumerate(arguments[:-1]):
        if argument in ('--outdir','--out','--output') or (argument=='--artifact' and 'fit' in arguments):
            path=Path(arguments[index+1]).resolve()
            if path.is_file():
                files.add(path)
                files.update(p for p in path.parent.glob(path.name+'.*') if p.is_file())
            elif path.is_dir():
                files.update(p for p in path.iterdir() if p.is_file())
    return {str(path):file_hash(path) for path in sorted(files)}


def command(root, name, arguments):
    marker = root/'steps'/(name+'.json')
    contract=command_contract(arguments)
    if marker.exists() and read_json(marker).get('status') == 'complete':
        saved=read_json(marker)
        if saved.get('contract')!=contract:
            raise RuntimeError(f'{name}: completed step command, inputs or source changed; preserve the original and use a new revision')
        for path,expected in saved.get('output_hashes',{}).items():
            if not Path(path).is_file() or file_hash(path)!=expected:
                raise RuntimeError(f'{name}: completed output changed: {path}')
        return
    write_json(marker,dict(status='running',started=now(),**contract,contract=contract))
    log_path=root/'logs'/(name+'.log')
    log_path.parent.mkdir(parents=True,exist_ok=True)
    with log_path.open('a') as log:
        result=subprocess.run([PYTHON,'-B',*arguments],cwd=ROOT,env=ENV,stdout=log,stderr=subprocess.STDOUT)
    write_json(marker,dict(status='complete' if result.returncode==0 else 'error',finished=now(),returncode=result.returncode,
                           **contract,contract=contract,output_hashes=command_outputs(arguments) if result.returncode==0 else {}))
    if result.returncode:
        raise RuntimeError(f'{name} failed: {log_path}')


def state(root, phase, **extra):
    write_json(root/'pipeline-status.json',dict(status='running',phase=phase,updated=now(),**extra))
    from prediction.report import render
    render(root,ROOT/'prediction/REPORT.md')


def gate(root, number, decision, reason, **extra):
    value=read_json(root/'gates.json')
    entry=dict(gate=number,decision=decision,reason=reason,time=now(),**extra)
    value['decisions'].append(entry)
    value['updated']=now()
    write_json(root/'gates.json',value)
    print(entry,flush=True)


def alive(pid):
    try:
        return Path(f'/proc/{pid}/stat').read_text().split()[2] != 'Z'
    except FileNotFoundError:
        return False


def wait_stages(root,names):
    while True:
        done=True
        for name in names:
            folder=root/name
            process=read_json(folder/'process.json')
            status=read_json(folder/'status.json') if (folder/'status.json').exists() else {}
            terminal=status.get('status') in ('complete','finished_with_errors')
            if not terminal:
                done=False
                if not alive(process['pid']):
                    raise RuntimeError(f'{name} runner exited before terminal status')
        if done:
            return
        from prediction.report import render
        render(root,ROOT/'prediction/REPORT.md')
        time.sleep(30)


def launch(root,name,manifest_name='manifest.json',workers=32):
    folder=root/name
    if (folder/'status.json').exists():
        status=read_json(folder/'status.json')
        if status.get('status') in ('complete','finished_with_errors'):
            return
        process=read_json(folder/'process.json')
        if alive(process['pid']):
            return
        raise RuntimeError('Interrupted stage needs explicit checkpoint audit before resume: '+name)
    with (folder/'process.log').open('a') as log:
        process=subprocess.Popen([PYTHON,'-B',str(root/'source/prediction/runner.py'),'--manifest',str(folder/manifest_name),
                                  '--out',str(folder),'--workers',str(workers)],cwd=root/'source',env=ENV,
                                  stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    write_json(folder/'process.json',dict(pid=process.pid,started=now(),manifest=str(folder/manifest_name)))


def fixed_snapshot(path,rows):
    if path.exists():
        assert read_json(path)==rows,'Do not alter a completed data snapshot'
    else:
        write_json(path,rows)


def context_game_variances(rows, targets):
    """Variation across games within each ordered model/opponent context.

    Pool observed event counts within a cell. Opposing context effects must
    not cancel into a spurious conclusion of no game-dependent behavior.
    """
    cells=defaultdict(lambda: [0,0])
    for row in rows:
        for target in targets:
            outcome=row['targets'].get(target,{})
            if outcome.get('opportunities',0) and outcome.get('successes') is not None:
                key=(target,row['model'],row['opponent'],row['group_id'])
                cells[key][0]+=outcome['successes']
                cells[key][1]+=outcome['opportunities']
    contexts=defaultdict(list)
    for (target,model,opponent,group),(successes,opportunities) in cells.items():
        contexts[target,model,opponent].append(successes/opportunities)
    output={target:[] for target in targets}
    for (target,model,opponent),rates in sorted(contexts.items()):
        if len(rates)<2:
            continue
        mean=sum(rates)/len(rates)
        output[target].append(dict(model=model,opponent=opponent,games=len(rates),
            between_game_variance=sum((rate-mean)**2 for rate in rates)/len(rates)))
    return output


def validate_primary_protocol(value,primary):
    for key in ('models','protocol','sources','source_root','ledger'):
        if value.get(key)!=primary.get(key):
            raise ValueError('Stage differs from primary '+key)


def development_manifest(root, primary):
    """Copy the primary contract before writing; validate on every resume."""
    path=root/'development/manifest.json'
    if path.exists():
        value=read_json(path)
    else:
        from prediction.games import generate_games
        games=generate_games(20260911,48)
        for game in games:
            game['id']='development-'+game['id']
        episodes=[]
        for game in games:
            for pair in combinations_with_replacement(sorted(primary['models']),2):
                for trial in range(2):
                    episodes.append(dict(id=f"{game['id']}--{pair[0]}--{pair[1]}--matrix--t{trial}",
                        game_id=game['id'],models=list(pair),representation='matrix',trial_id=trial,swap=bool(trial%2)))
        random.Random(20260910).shuffle(episodes)
        value={key:deepcopy(primary[key]) for key in ('models','protocol','sources','source_root','ledger')}
        value.update(stage='development',created=now(),games=games,episodes=episodes,stage_budget_usd=350.)
    validate_primary_protocol(value,primary)
    assert not {g['group_id'] for g in value['games']}&{g['group_id'] for g in primary['games']}
    assert value['stage']=='development' and len(value['games'])==48 and len(value['episodes'])==960
    if not path.exists():
        write_json(path,value)
    return value


def run(root):
    state(root,'gate3_primary_pilot_collection')
    wait_stages(root,('pilot','pilot-oss'))
    command(root,'primary-pilot-collect',['prediction/combine_pilot.py','--run-root',str(root),
            '--output',str(root/'primary-pilot/final-collection')])
    rows=read_json(root/'primary-pilot/final-collection/records.json')
    summary=read_json(root/'primary-pilot/final-collection/summary.json')
    fixed_snapshot(root/'primary-pilot/final-records.json',rows)
    command(root,'primary-pilot-diagnostics',['-m','prediction.diagnostics','--records',str(root/'primary-pilot/final-records.json'),
                '--out',str(root/'primary-pilot/diagnostics'),'--bootstrap','300'])
    diagnostic=read_json(root/'primary-pilot/diagnostics/diagnostics.json')
    coverage=summary['complete_episodes']/summary['planned_episodes']
    if coverage<.90 or summary['integrity_errors']:
        gate(root,3,'stop','Primary collection lacks reliable coverage or integrity; do not expand.',coverage=coverage)
        write_json(root/'pipeline-status.json',dict(status='stopped_at_gate3',updated=now(),reason='collection reliability'))
        return
    # A substantial negative requires effectively constant aggregate behavior
    # across every prespecified broad target, not one noisy conditional rate.
    targets=('action0','first_action0','cooperation','coordination')
    variances={t:diagnostic['targets'].get(t,{}).get('variance',{}).get('between_game_variance') for t in targets}
    observed=[v for v in variances.values() if v is not None]
    context_variances=context_game_variances(rows,targets)
    context_observed=[cell['between_game_variance'] for cells in context_variances.values() for cell in cells]
    if observed and context_observed and max(observed)<1e-4 and max(context_observed)<1e-4:
        gate(root,3,'stop','Behavior is effectively constant across pilot games both overall and within ordered model/opponent contexts; expansion would not identify a useful predictor.',variances=variances,context_variances=context_variances)
        write_json(root/'pipeline-status.json',dict(status='stopped_at_gate3',updated=now(),reason='negligible measured variation'))
        return
    repeatability={t:diagnostic['targets'].get(t,{}).get('split_half',{}).get('game') for t in targets}
    gate(root,3,'proceed','Integrity-checked pilot has sufficient completed coverage and nonconstant game-level behavior. Repeatability estimates and sparse conditional support are retained; variation alone is not evidence of prediction.',
         coverage=coverage,variances=variances,context_variances=context_variances,repeatability=repeatability)
    state(root,'gate4_development_collection')
    development_manifest(root,read_json(root/'primary-pilot-manifest.json'))
    launch(root,'development')
    # Exploratory pilot evaluation overlaps the independent development rollout.
    command(root,'pilot-numerical',['-m','prediction.modeling','evaluate','--input',str(root/'primary-pilot/final-records.json'),
                '--outdir',str(root/'pilot/evaluation'),'--splits','family,random_group,interpolation,extrapolation,pair,model','--bootstrap','300'])
    wait_stages(root,('development',))
    command(root,'development-collect',[str(root/'source/prediction/study.py'),'collect','--stage-root',str(root/'development'),
            '--output',str(root/'development/collected')])
    collected=read_json(root/'development/collected/summary.json')
    if collected['errors'] or collected['complete_episodes']/collected['planned_episodes']<.90:
        gate(root,4,'stop','Expanded collection failed integrity or coverage checks; preserve complete labels and halt additional paid expansion.',collection=collected)
        write_json(root/'pipeline-status.json',dict(status='stopped_at_gate4',updated=now(),reason='collection reliability'))
        return
    development=read_json(root/'development/collected/records.json')
    training=rows+development
    assert len({(r['episode_id'],r['player_index']) for r in training})==len(training)
    fixed_snapshot(root/'training-records.json',training)
    gate(root,4,'proceed','Expanded to 72 distinct payoff shapes with the same player protocol. The snapshot is fixed before fitting the final predictors.',
         games=len({r['group_id'] for r in training}),episodes=len({r['episode_id'] for r in training}),training_sha256=digest(training))
    state(root,'gates5_to7_numerical_evaluation')
    command(root,'development-numerical',['-m','prediction.modeling','evaluate','--input',str(root/'training-records.json'),
                '--outdir',str(root/'development/evaluation'),'--splits','family,random_group,interpolation,extrapolation,pair,model','--bootstrap','500'])
    scores=read_json(root/'development/evaluation/scores.json')
    contrasts=[r for r in scores.get('comparisons_to_pair',[]) if r['method'] in ('combined_logistic_both','combined_mlp_both','raw_logistic')
               and r['split'] in ('family','random_group') and r['target'] in ('action0','cooperation','coordination')]
    gate(root,5,'numerical evaluation complete','Prespecified numerical predictors were scored against the ordered model/opponent baseline. All methods, missing support and paired uncertainty remain visible. The prompted-LLM comparison is still required.',contrasts=contrasts)
    gate(root,6,'numerical evaluation complete','Family, random-group and payoff interpolation/extrapolation holdouts completed. These are exploratory grouped validations; prospective forecasts and presentation/affine controls remain separate.')
    gate(root,7,'numerical evaluation complete','Focal/opponent identity ablations, held-out unordered pairings and zero-calibration model holdouts completed. Unknown identities use a declared fallback; no Gate8 adaptation or embeddings experiment was run.')
    state(root,'awaiting_prospective_stage',numerical_gates_complete=True)
    print('Numerical gates complete; prospective-stage driver may continue from this fixed snapshot.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-root',type=Path,required=True)
    args=parser.parse_args()
    lock=(args.run_root/'pipeline.lock').open('a')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    try:
        run(args.run_root)
    except Exception as exc:
        write_json(args.run_root/'pipeline-status.json',dict(status='error',updated=now(),error=type(exc).__name__+': '+str(exc)))
        raise
    finally:
        from prediction.report import render
        render(args.run_root,ROOT/'prediction/REPORT.md')
