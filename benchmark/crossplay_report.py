"""Focal-seat cross-play outcomes, discovery and engine metrics, with sample sizes."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
from statistics import mean
from .clients import write_json
from .crossplay_games import SPECS,GAME_IDS

LABELS={'ref_exchange_live':'Exchange: live trading','ref_hanabi_live':'Hanabi: live team','ta_ipd_live':'IPD: live opponents'}


def csv_write(path,rows):
    if not rows:return
    with path.open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def build_report(out,plots=False):
    out=Path(out);cfg=json.loads((out/'config.json').read_text());rows=[];holes=[]
    for path in (out/'traces').glob('*.json'):
        t=json.loads(path.read_text())
        if t['status']!='complete':continue
        for pid in range(len(t['seats'])):
            focal=t['seats_results'][pid];side=out/'discovery'/(path.stem+f'__seat{pid}.json');judgments={}
            if side.exists():
                d=json.loads(side.read_text());assert d['source_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
                judgments={r['exploit_id']:r for r in d['judgments']}
            rows.append(dict(match=t['id'],game=t['game_id'],league=t['league'],focal=t['seats'][pid],opponent='+'.join(m for p,m in enumerate(t['seats']) if p!=pid),seed=t['seed'],seat=pid,score=focal['score'],
                win_credit=focal['win_credit'],outright_win=focal['outright_win'],tied_top=focal['tied_top'],
                invalid=focal['invalid'],decisions=focal['decisions'],strict_replay_gain=focal['strict_replay_gain'],
                team_complete=(sum(t['episode']['extras'].get('stacks',{}).values())==25) if t['cooperative'] else None,
                discovered=mean(j['discovered'] for j in judgments.values()) if judgments else None,
                executed=mean(r['executed'] for r in focal['execution']),attempted=mean(r['attempted'] for r in focal['execution'])))
            for r in focal['execution']:
                j=judgments.get(r['id'],{})
                holes.append(dict(match=t['id'],game=t['game_id'],focal=t['seats'][pid],opponent='+'.join(m for p,m in enumerate(t['seats']) if p!=pid),league=t['league'],hole=r['id'],category=r['category'],
                                  attempted=r['attempted'],executed=r['executed'],discovered=j.get('discovered'),correct_hypothesis=j.get('correct_hypothesis'),quote=j.get('quote',''),reason=j.get('reason','')))
    csv_write(out/'matches.csv',rows);csv_write(out/'holes.csv',holes)
    # Compare model sizes against exactly the same other-seat lineup, deal,
    # and own seat. Match-level pairs remain correlated across seat views.
    pairs=[]
    families=(('claude-haiku-4.5','claude-opus-5'),('gpt-5-mini','gpt-5'),('gemini-3.7-flash','gemini-3.1-pro'))
    lookup={(r['game'],r['focal'],r['opponent'],r['seed'],r['seat']):r for r in rows}
    for small,large in families:
        for r in rows:
            if r['focal']!=small:continue
            other=lookup.get((r['game'],large,r['opponent'],r['seed'],r['seat']))
            if other is None:continue
            pair=dict(game=r['game'],small=small,large=large,opponents=r['opponent'],seed=r['seed'],seat=r['seat'])
            for metric in ('score','win_credit','discovered','executed'):
                pair[metric+'_small']=r[metric];pair[metric+'_large']=other[metric]
                pair[metric+'_delta']=other[metric]-r[metric] if other[metric] is not None and r[metric] is not None else None
            pairs.append(pair)
    csv_write(out/'matched_size_pairs.csv',pairs)
    effects=[]
    for game in GAME_IDS:
        for small,large in families:
            ps=[r for r in pairs if r['game']==game and r['small']==small]
            for metric in ('score','win_credit','discovered','executed'):
                vs=[r[metric+'_delta'] for r in ps if r[metric+'_delta'] is not None]
                effects.append(dict(game=game,small=small,large=large,metric=metric,matched_pairs=len(vs),mean_delta=mean(vs) if vs else None))
    csv_write(out/'size_effects.csv',effects)
    models=list(cfg['model_configs']);cells=[]
    for game in GAME_IDS:
        for focal in models:
            for opponent in models:
                planned=[t for t in cfg['tasks'] if t['game_id']==game and focal!=opponent and focal in t['seats'] and opponent in t['seats']]
                if not planned:continue
                rs=[r for r in rows if r['game']==game and r['focal']==focal and opponent in r['opponent'].split('+')]
                row=dict(game=game,focal=focal,opponent=opponent,n=len(rs),expected=len(planned))
                for metric in ('score','win_credit','outright_win','tied_top','team_complete','discovered','executed','attempted','strict_replay_gain'):
                    values=[r[metric] for r in rs if r[metric] is not None]
                    row[metric]=mean(values) if values and len(values)==len(rs) else None
                cells.append(row)
    csv_write(out/'matchups.csv',cells)
    cost=tokens=calls=0
    for pattern in ('calls/*/*/*.json','judge_calls/*/*.json'):
        for path in out.glob(pattern):
            for a in json.loads(path.read_text()).get('attempts',[]):
                u=a.get('response',{}).get('usage',{}) or {};cost+=u.get('cost',0) or 0;tokens+=u.get('total_tokens',0) or 0;calls+=int('response' in a)
    summary=dict(complete=len({r['match'] for r in rows}),expected=len(cfg['tasks']),seat_observations=len(rows),discovery_scored=sum(r['discovered'] is not None for r in rows),reported_usd=cost,tokens=tokens,responses=calls)
    write_json(out/'summary.json',summary)
    lines=['# Small / large model cross-play','',f"Completed {summary['complete']}/{len(cfg['tasks'])}; seat discovery scored {summary['discovery_scored']}/{len(rows)}. API-reported cost ${cost:.2f}.",'',
      'Fresh private conversation per seat and match; no reflection. All cohorts run concurrently. Every table contains different model families. Each seat has one outcome; seats in a match are dependent. Matrices show table outcomes when sharing a table with the column model, averaged over the third player in three-player games.',
      'Three-player games use all eight small/large combinations and all six seat permutations on one common deal. Two-player IPD uses all cross-family tier combinations, both seat orders and two seeds. Same-family cells are intentionally absent. This is a small descriptive pilot, not a precise ranking.',
      'Win credit splits one point among tied top-scoring seats. Outright wins and ties are exported separately. Hanabi is cooperative: show team score and completion, not individual wins.',
      'Game versions differ from the short diagnostic: native five-round trading Exchange, native 27-turn / 25-point Hanabi, and four-round live IPD. The scripted undelivered-punishment loophole is absent from live IPD. Do not pool with earlier profiles.',
      'Discovery is a fixed Haiku language judge, blinded to model identities, requiring a quote from the focal player. It cannot observe unspoken recognition or distinguish independent invention from adoption after opponent exposure. Engine execution is separate. No per-hole causal success is claimed; Exchange has seat-level strict-replay gain, and Hanabi requires a patched matched experiment for causal attribution.', '',
      '[Matchup rates](matchups.csv) · [Individual outcomes](matches.csv) · [Hole labels and quotations](holes.csv) · [Status](status.json) · [Matched model-size effects](size_effects.csv) · [Matched pairs](matched_size_pairs.csv)', '']
    lines += ['Larger-minus-smaller effects hold the other-seat model lineup, seat and environment seed fixed; see size_effects.csv. They remain descriptive with very few distinct deals.', '']
    if plots:
        draw(out,models,cells,holes,effects)
        for game in GAME_IDS:
            for metric in ('win_credit','score','discovered','executed'):
                if game=='ref_hanabi_live' and metric=='win_credit':continue
                lines.append(f'![{game} {metric}]({game}_{metric}.png)')
        lines+=['','![Matched model-size discovery and execution differences](size_effects.png)', '', '![Discovery versus execution by hole](holes.png)']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n')
    return summary


def draw(out,models,cells,holes,effects):
    os.environ['MPLCONFIGDIR']=str(out/'.matplotlib-cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.backends.backend_pdf import PdfPages
    with PdfPages(out/'all_plots.pdf') as pdf:
        for game in GAME_IDS:
            for metric in ('win_credit','score','discovered','executed'):
                if game=='ref_hanabi_live' and metric=='win_credit':continue
                vals=np.full((len(models),len(models)),np.nan);ns={}
                for r in cells:
                    if r['game']!=game:continue
                    i,j=models.index(r['focal']),models.index(r['opponent']);ns[i,j]=(r['n'],r['expected'])
                    if r[metric] is not None:vals[i,j]=r[metric]*(1 if metric=='score' else 100)
                fig,ax=plt.subplots(figsize=(9,8));cm=plt.get_cmap('Blues').with_extremes(bad='#eee')
                im=ax.imshow(vals,cmap=cm,vmin=0,vmax=(25 if game=='ref_hanabi_live' else 20 if game=='ta_ipd_live' else 15) if metric=='score' else 100)
                ax.set_xticks(range(len(models)),models,rotation=35,ha='right');ax.set_yticks(range(len(models)),models);ax.set_xlabel('Opponent model (teammates in Hanabi)');ax.set_ylabel('Focal model')
                for i in range(len(models)):
                    for j in range(len(models)):
                        n=ns.get((i,j));v=vals[i,j]
                        text='—' if n is None else f'pending\n{n[0]}/{n[1]}' if np.isnan(v) else (f'{v:.1f}' if metric=='score' else f'{v:.0f}%')+f'\nn={n[0]}'
                        ax.text(j,i,text,ha='center',va='center',fontsize=8,color='white' if not np.isnan(v) and v>im.norm.vmax*.55 else 'black')
                title=LABELS[game]+' · '+metric.replace('_',' ');ax.set_title(title);fig.colorbar(im,ax=ax,shrink=.7)
                fig.text(.5,.01,'Matched seat permutations; descriptive. Grey — = unsampled. Ties split win credit; no individual Hanabi wins.',ha='center',fontsize=8)
                fig.tight_layout(rect=[0,.04,1,1]);name=game+'_'+metric
                for ext in ('png','pdf'):fig.savefig(out/(name+'.'+ext),dpi=150,bbox_inches='tight')
                pdf.savefig(fig,bbox_inches='tight');plt.close(fig)
        fig,axes=plt.subplots(1,3,figsize=(14,4.5))
        families=('claude-haiku-4.5','gpt-5-mini','gemini-3.7-flash')
        for ax,g in zip(axes,GAME_IDS):
            for k,metric in enumerate(('discovered','executed')):
                values=[]
                for small in families:
                    row=next(r for r in effects if r['game']==g and r['small']==small and r['metric']==metric)
                    values.append(np.nan if row['mean_delta'] is None else 100*row['mean_delta'])
                ax.bar(np.arange(3)+(k-.5)*.32,values,.32,label=metric.title())
            ax.set_xticks(range(3),['Opus − Haiku','GPT‑5 − mini','Pro − Flash'],rotation=20,ha='right')
            ax.set_ylim(-105,105);ax.axhline(0,color='#888',linewidth=.7);ax.set_title(LABELS[g]);ax.set_ylabel('Larger − smaller (percentage points)')
        fig.legend(*axes[0].get_legend_handles_labels(),loc='upper center',ncol=2)
        fig.text(.5,.01,'Paired on other-seat models, own seat and deal. Missing judgments remain unknown; descriptive pilot.',ha='center',fontsize=8)
        fig.tight_layout(rect=[0,.04,1,.92]);fig.savefig(out/'size_effects.png',dpi=150,bbox_inches='tight');fig.savefig(out/'size_effects.pdf',bbox_inches='tight');pdf.savefig(fig,bbox_inches='tight');plt.close(fig)
        fig,axes=plt.subplots(1,2,figsize=(15,6));columns=[(g,s['id']) for g in GAME_IDS for s in SPECS[g]]
        for ax,metric in zip(axes,('discovered','executed')):
            vals=np.full((len(models),len(columns)),np.nan)
            for i,m in enumerate(models):
                for j,(g,h) in enumerate(columns):
                    rs=[r[metric] for r in holes if (r['focal'],r['game'],r['hole'])==(m,g,h)]
                    if rs and all(v is not None for v in rs):vals[i,j]=100*mean(rs)
            im=ax.imshow(vals,vmin=0,vmax=100,cmap='Blues',aspect='auto');ax.set_xticks(range(len(columns)),[h for g,h in columns],rotation=40,ha='right');ax.set_yticks(range(len(models)),models);ax.set_title(metric.title())
            for i in range(len(models)):
                for j in range(len(columns)):
                    v=vals[i,j];ax.text(j,i,'—' if np.isnan(v) else f'{v:.0f}',ha='center',va='center',fontsize=8,color='white' if v>55 else 'black')
        fig.suptitle('Per-seat hole rates (%) over the scheduled opponent mixture');fig.tight_layout()
        fig.savefig(out/'holes.png',dpi=150,bbox_inches='tight');fig.savefig(out/'holes.pdf',bbox_inches='tight');pdf.savefig(fig,bbox_inches='tight');plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out',type=Path);p.add_argument('--plots',action='store_true');a=p.parse_args();build_report(a.out,a.plots)
