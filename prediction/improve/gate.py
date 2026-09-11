"""Fixed development decision; no fitting, model calls, or fresh outcomes."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
from prediction.improve.data import TARGETS,file_hash,write_new

TRANSFORMERS=('qwen3_frozen_head','qwen3_lora_head')
STRONG_BASELINES=('calibrated_payoff_dominant','normalized_logistic','combined_logistic','family')

def protocol():
    return dict(version='improve-development-gate-v1',meaningful_brier_gain=.005,
        scopes=['family','development'],targets=list(TARGETS),transformers=list(TRANSFORMERS),
        strong_baseline_set=list(STRONG_BASELINES),
        negative_stop='In BOTH LOFO and old21 development, BOTH transformer approaches must be worse in point Brier on ALL three broad targets than the lowest-Brier declared strong baseline, and the paired descriptive upper bound must exclude a gain of .005.',
        selection_interpretation='Selecting the strongest declared comparator here controls a conservative resource gate; it is not a post-selection confidence claim. All fixed comparator contrasts remain in the report.',
        other_splits='Corrected interpolation/extrapolation are fully reported, not additional architecture-selection opportunities.',
        inconclusive='Any failure to establish this consistent negative pattern permits exactly the fixed28-shape fresh cohort; CI crossing0 alone is not a stop.',
        technical='Require complete20Fleet fits, successful final LoRA steps, exact forecast coverage and optimizer/source audit; a technical failure never counts as a behavioral negative result.')

def decide(root,evaluation):
    root=Path(root);evaluation=Path(evaluation)
    scores=json.loads((evaluation/'scores.json').read_text());pairs=json.loads((evaluation/'paired-comparisons.json').read_text())
    frozen=json.loads((root/'gate-protocol.json').read_text())
    if frozen!=protocol():raise ValueError('Gate protocol changed')
    training=json.loads((root/'fleet-runtime/training-status.json').read_text())
    if training['status']!='complete':raise ValueError('Training has not completed')
    technical=[]
    for method in ('frozen','lora'):
        folders=sorted(p for p in (root/'transformer'/method).iterdir() if p.is_dir())
        if len(folders)!=10:raise ValueError('Expected ten completed fits per transformer method')
        for folder in folders:
            completion=json.loads((folder/'complete.json').read_text())
            for path,expected in completion['output_sha256'].items():
                local=path.replace('/mnt/sfs/','/shared/',1)
                if file_hash(local)!=expected:raise ValueError('Fit artifact changed: '+local)
            artifact=json.loads((folder/'artifact.json').read_text())
            if method=='lora' and artifact['diagnostics']['optimization_success'] is not True:
                raise ValueError('Adaptation did not complete its fixed optimizer steps')
            technical.append(str(folder))
    cells=[]
    for split in ('family','development'):
        for target in TARGETS:
            candidates=[r for r in scores['scores'] if r['support']=='numerical_only' and r['split']==split
                        and r['family']=='all' and r['target']==target and r['method'] in STRONG_BASELINES and r['status']=='complete']
            if len(candidates)!=len(STRONG_BASELINES):raise ValueError('Incomplete strong-baseline support')
            best=min(candidates,key=lambda r:(r['event_brier'],r['method']))['method']
            for method in TRANSFORMERS:
                matches=[r for r in pairs if r['support']=='numerical_only' and r['split']==split and r['family']=='all'
                         and r['target']==target and r['baseline']==best and r['method']==method]
                if len(matches)!=1:raise ValueError('Missing/duplicate gate contrast')
                interval=matches[0]['game_bootstrap']['intervals']['event_brier']
                cells.append(dict(split=split,target=target,method=method,strongest_declared_baseline=best,
                    **interval,negative=interval['improvement']<0 and interval['upper']<.005))
    negative=all(r['negative'] for r in cells)
    value=dict(created_utc=datetime.now(timezone.utc).isoformat(),proceed=not negative,
        status='stop_consistent_negative_development' if negative else 'proceed_fixed_fresh_cohort',
        reason='Both representations consistently fail the fixed resource gate.' if negative else 'The consistent-negative stop rule is not met; positive or inconclusive development permits the fixed prospective test.',
        protocol=frozen,cells=cells,verified_transformer_fits=technical,
        input_sha256={str(p.resolve()):file_hash(p) for p in (evaluation/'scores.json',evaluation/'paired-comparisons.json',root/'gate-protocol.json')},
        fresh_outcomes_accessed=False,comparison_interpretation='This resource decision is not a positive scientific improvement claim.')
    write_new(root/'development-gate.json',value)
    return value

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-root',required=True);p.add_argument('--evaluation');p.add_argument('--freeze',action='store_true');a=p.parse_args()
    if a.freeze:write_new(Path(a.run_root)/'gate-protocol.json',protocol())
    else:
        value=decide(a.run_root,a.evaluation);print(json.dumps({k:value[k] for k in ('status','proceed','reason')}))

if __name__=='__main__':main()
