"""Read-only independent scoring/model checks and comparison figure."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import pickle
from statistics import mean

from prediction import asymmetry_predictors as p
from prediction.io_utils import read_json,write_json,now


def build(out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    manifest = read_json(out/'manifest.json')
    summary = read_json(out/'summary.json')
    numeric = read_json(out/'numeric.json')
    trace_index = {s['id']:read_json(out/'episodes'/s['id']/'trace.json') for s in manifest['episodes']}
    games = {g['id']:g for g in manifest['games']}
    # Recover saved estimators, build outcome-free query features independently
    # of scored rows, and check that the sealed numerical predictions match.
    recomputed = 0
    for group,fold in numeric['folds'].items():
        specs = [s for s in manifest['episodes'] if p.shape_id(games[s['game_id']])==group]
        metadata = [r for s in specs for r in p.rows_for(dict(spec=s,game=games[s['game_id']]),False)]
        for method in ('logistic','mlp'):
            with (out/'models'/f'{group}--{method}.pkl').open('rb') as stream: model=pickle.load(stream)
            assert model.training_groups==fold['training_groups']
            assert model.training_count==len(fold['training_episodes'])*2
            for row,value in zip(metadata,model.predict(metadata)):
                assert abs(value-numeric['predictions'][row['episode_id']][method][row['player']])<1e-12
                recomputed+=1
    assert recomputed==256
    zero = read_json(out/'zero-shot.json')
    scoring = defaultdict(list)
    game_scores = defaultdict(lambda:defaultdict(list))
    for spec in manifest['episodes']:
        game = games[spec['game_id']]
        turns = trace_index[spec['id']]['rounds']
        few = read_json(out/'forecasts'/(spec['id']+'.json'))['joint']
        stage = p.smoke.theory(game)
        predictions = {**numeric['predictions'][spec['id']],
                       'few_shot':[few[0]+few[1],few[0]+few[2]],
                       'zero_shot':[zero[spec['id']]['joint'][0]+zero[spec['id']]['joint'][1],
                                    zero[spec['id']]['joint'][0]+zero[spec['id']]['joint'][2]],
                       'stage_nash':[stage[0]+stage[1],stage[0]+stage[2]],'uniform':[.5,.5]}
        for method,q in predictions.items():
            successes=[sum(t['actions'][player]==0 for t in turns) for player in range(2)]
            brier=mean((k*(1-z)**2+(8-k)*z*z)/8 for k,z in zip(successes,q))
            scoring[(game['condition'],method)].append(brier)
            scoring[('all',method)].append(brier)
            game_scores[game['id']][method].append(brier)
    for (condition,method),values in scoring.items():
        assert abs(mean(values)-summary['scores'][condition][method]['brier'])<1e-12
    rows=[dict(game_id=gid,condition=games[gid]['condition'],group_id=p.shape_id(games[gid]),
               scores={method:mean(values) for method,values in methods.items()}) for gid,methods in sorted(game_scores.items())]
    group_rows=[]
    for group in sorted({r['group_id'] for r in rows}):
        selected=[r for r in rows if r['group_id']==group]
        group_rows.append(dict(group_id=group,condition=selected[0]['condition'],games=[r['game_id'] for r in selected],
                               scores={method:mean(r['scores'][method] for r in selected) for method in p.METHODS}))
    write_json(out/'game-scores.json',rows)
    write_json(out/'group-scores.json',group_rows)
    audit=dict(checked_at=now(),saved_numerical_predictions_recomputed=recomputed,
               brier_score_cells_independently_recomputed=len(scoring),
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    write_json(out/'independent-audit.json',audit)
    labels={'few_shot':'Kimi few-shot','logistic':'Learned logistic','mlp':'Learned MLP',
            'zero_shot':'Kimi zero-shot','stage_nash':'Equilibrium rule','uniform':'Uniform'}
    methods=list(p.METHODS)
    fig,(ax,delta)=plt.subplots(1,2,figsize=(11.5,4.8),layout='constrained')
    for offset,condition,color in [(-.18,'symmetric','#98a9ba'),(.18,'asymmetric','#287d8e')]:
        ax.barh([i+offset for i in range(len(methods))],
                [summary['scores'][condition][m]['brier'] for m in methods],height=.34,color=color,label=condition.capitalize())
    ax.set(yticks=range(len(methods)),yticklabels=[labels[m] for m in methods],xlabel='Action Brier score (lower is better)',
           title='Fresh matches: prediction error')
    ax.invert_yaxis(); ax.legend(frameon=False,loc='lower right'); ax.grid(axis='x',alpha=.2); ax.set_axisbelow(True)
    others=['logistic','mlp','zero_shot','stage_nash']
    for i,other in enumerate(others):
        contrast=summary['paired_brier_contrasts']['asymmetric'][other]
        point=contrast['few_shot_minus_comparator']
        lo,hi=contrast['descriptive_95_interval']
        delta.plot([lo,hi],[i,i],color='#287d8e',lw=2)
        delta.scatter([point],[i],color='#287d8e',s=45,zorder=3)
    delta.axvline(0,color='#555',lw=1,ls='--')
    delta.set(yticks=range(len(others)),yticklabels=[f'Few-shot − {labels[m]}' for m in others],
              xlabel='Brier difference: negative favors few-shot',title='Asymmetric pairings: paired differences')
    delta.invert_yaxis(); delta.grid(axis='x',alpha=.2); delta.set_axisbelow(True)
    fig.suptitle('Few-shot versus learned predictors on independent player payoffs\n64 fresh matches; entire test payoff group excluded from training/examples',fontsize=12)
    fig.savefig(out/'predictor-comparison.png',dpi=180)
    fig.savefig(out/'predictor-comparison.svg')
    plt.close(fig)
    print(json.dumps(dict(audit=audit,groups=group_rows),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    build(parser.parse_args().out)
