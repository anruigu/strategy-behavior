"""Train-only exports, scientific figures, and immutable reproduction manifest."""
import hashlib
import json
from pathlib import Path
import tarfile

from prediction.io_utils import read_json,write_json,digest,now
from prediction.general_games.export import jsonl
from . import ROOT,DATA,STUDY
from .collection import source_hashes
from .labels import DEFINITIONS


def train_exports():
    specs=read_json(STUDY/'prediction/depth/mechanics.json'); manifest=dict(created=now(),purpose='Train-only inputs for a separately specified learner job. No test outcomes or test examples.',arms={})
    for arm in ('depth','breadth'):
        folder=STUDY/'prediction'/arm; m=read_json(folder/'manifest.json'); rows=read_json(folder/'training.evaluator.json'); groups=read_json(folder/'groups.evaluator.json')
        exported=[dict(episode_id=r['episode_id'],condition_id=r['condition_id'],observable_input_group=r['observable_input_group'],
            inputs=r['inputs'],mechanics=specs[r['inputs']['family_id']],targets=r['targets']) for r in rows]
        pooled=[dict(input_group='input-'+digest(r['inputs'])[:20],inputs=r['inputs'],mechanics=specs[r['inputs']['family_id']],targets=r['targets'],target_counts=r['target_counts'],episode_ids=r['episodes']) for r in groups]
        assert len(exported)==288
        jsonl(STUDY/'overnight'/f'{arm}-episodes.jsonl',exported); jsonl(STUDY/'overnight'/f'{arm}-pooled.jsonl',pooled)
        manifest['arms'][arm]=dict(episodes=288,pooled_visible_inputs=len(pooled),family_ids=sorted({r['inputs']['family_id'] for r in rows}),
            parent_manifest_sha256=digest(m),files={name:hashlib.sha256((STUDY/'overnight'/name).read_bytes()).hexdigest() for name in (f'{arm}-episodes.jsonl',f'{arm}-pooled.jsonl')})
    manifest['target_definitions']=DEFINITIONS
    manifest['split_rule']='Keep identical observable inputs together; use full-family held-out validation within the training pool. Use pooled means with count-aware binary/continuous losses. Do not select hyperparameters from this study’s six test-family outcomes.'
    write_json(STUDY/'overnight/manifest.json',manifest)
    (STUDY/'overnight/README.md').write_text('''# Inputs for a separate overnight learner run

Each arm has 288 episode labels; the depth and breadth arms share 96 episodes.
`*-episodes.jsonl` contains individual binary/continuous labels; `*-pooled.jsonl`
contains all-label means/counts for identical complete visible inputs. All rows
are training data. Mechanics summaries are predictor context; hidden native
state and holdout outcomes are not included.

Choose a model and compute budget before starting an additional training job.
These exports do not launch GPU training. Use family-held-out validation within
the training pool. Keep all identical visible inputs together, and use
count-aware losses for pooled means. Do not treat a fractional win mean as a
hard classification category. Match training compute as well as label budgets
when comparing neural learners.

The six holdout families are reserved for the primary study. If their outcomes
have been inspected, a newly tuned learner needs an untouched evaluation set
for a prospective claim, or a clearly labeled retrospective evaluation here.
''')
    return manifest


def figures(summary):
    import os
    os.environ.setdefault('MPLCONFIGDIR','/shared/allie/home/.codex/tmp/matplotlib-prediction')
    from prediction import modeling
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    methods=['training_mean','linear','few_4','corrected_4','few_8','few_16']; labels=['Training mean','Linear learner','Pooled 4-shot','Learned correction','Pooled 8-shot','Pooled 16-shot']
    lookup={(r['arm'],r['method'],r['target']):r['score'] for r in summary['scores']}
    fig,axes=plt.subplots(1,3,figsize=(14,5),layout='constrained')
    for ax,target,title in zip(axes,['win','any_invalid','native_score'],['Win / solution Brier','Any-invalid Brier','Native-score MSE']):
        x=list(range(len(methods)))
        for arm,offset,color in [('depth',-.19,'#617184'),('breadth',.19,'#147d6f')]:
            ax.barh([i+offset for i in x],[lookup[arm,m,target] for m in methods],height=.36,label='4 families · depth' if arm=='depth' else '12 families · breadth',color=color)
        ax.set_yticks(x,labels if ax is axes[0] else ['']*len(labels)); ax.invert_yaxis(); ax.set_title(title); ax.set_xlabel('Lower is better'); ax.grid(axis='x',alpha=.15); ax.set_axisbelow(True)
        ax.spines[['top','right']].set_visible(False)
    handles,legend_labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,legend_labels,loc='lower center',bbox_to_anchor=(.5,-.05),ncol=2,fontsize=9,frameon=False)
    fig.suptitle('288 training episodes per arm · same six unseen test families',fontsize=14)
    folder=STUDY/'figures'; folder.mkdir(exist_ok=True)
    for ext in ('png','pdf','svg'): fig.savefig(folder/f'breadth-comparison.{ext}',dpi=180,bbox_inches='tight')
    plt.close(fig)


def main():
    summary=read_json(STUDY/'summary.json'); train_exports(); figures(summary)
    repo=ROOT.parents[2]; sources={}
    for name in source_hashes():
        path=repo/name
        if path.exists(): sources[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    for p in ROOT.glob('*.py'): sources[str(p.relative_to(repo))]=hashlib.sha256(p.read_bytes()).hexdigest()
    for p in (ROOT/'README.md',repo/'prediction/modeling.py'):
        if p.exists(): sources[str(p.relative_to(repo))]=hashlib.sha256(p.read_bytes()).hexdigest()
    for pattern in ('*.py','*.html','*.js','*.css'):
        for p in (repo/'prediction/scaleup/viewer').glob(pattern): sources[str(p.relative_to(repo))]=hashlib.sha256(p.read_bytes()).hexdigest()
    with tarfile.open(STUDY/'reproduction-source.tar.gz','w:gz') as tar:
        for name in sorted(sources): tar.add(repo/name,arcname=name)
    artifacts={}
    paths=[DATA/'manifest.json',DATA/'catalog.json',DATA/'mechanics.json',DATA/'label-definitions.json',DATA/'native-source.tar.gz',STUDY/'protocol.json',STUDY/'summary.json',STUDY/'REPORT.md',STUDY/'predictions.json',STUDY/'all-episodes.jsonl',STUDY/'all-actions.jsonl',STUDY/'prediction/frozen.json']
    paths+=list((STUDY/'overnight').glob('*'))+list((STUDY/'figures').glob('*'))
    paths.extend([DATA/'TEXTARENA_LICENSE',DATA/'DATASET_CARD.md'])
    paths.extend([DATA/'instances.evaluator.json',DATA/'fixtures.evaluator.json',STUDY/'training/plan.json',STUDY/'test/plan.json'])
    paths.extend([STUDY/'recovery-policy.json',STUDY/'prediction/collection-order.json']); paths+=list((STUDY/'recovery').rglob('*-original.json'))
    for arm in ('depth','breadth'):
        paths.extend(STUDY/'prediction'/arm/name for name in ('manifest.json','mechanics.json','training.evaluator.json','groups.evaluator.json','test-predictions.json','models.pkl'))
    for p in paths: artifacts[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    calls={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in STUDY.rglob('raw_calls/*.json')}
    write_json(STUDY/'raw-call-sha256.json',calls)
    checkpoints={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for phase in ('training','test') for p in (STUDY/phase/'episodes').glob('*.json')}
    assert len(checkpoints)==summary['counts']['total_episodes']
    write_json(STUDY/'episode-checkpoint-sha256.json',checkpoints)
    from prediction import modeling
    import importlib.metadata, numpy, sklearn, scipy, matplotlib, sys
    versions=dict(python=sys.version,numpy=numpy.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__,matplotlib=matplotlib.__version__,textarena=importlib.metadata.version('textarena'))
    result=dict(created=now(),versions=versions,source_files=sources,artifact_hashes=artifacts,source_archive_sha256=hashlib.sha256((STUDY/'reproduction-source.tar.gz').read_bytes()).hexdigest(),raw_call_manifest_sha256=hashlib.sha256((STUDY/'raw-call-sha256.json').read_bytes()).hexdigest(),episode_checkpoint_manifest_sha256=hashlib.sha256((STUDY/'episode-checkpoint-sha256.json').read_bytes()).hexdigest())
    write_json(STUDY/'reproduction.json',result)
    print(json.dumps(dict(source_files=len(sources),artifacts=len(artifacts),raw_calls=len(calls)),indent=2),flush=True)
    return result


if __name__=='__main__': main()
