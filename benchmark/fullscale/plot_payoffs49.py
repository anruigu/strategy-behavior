"""Observed payoff/execution associations for the completed Gemini 49-target audit."""
from pathlib import Path
import csv,json,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from benchmark.fullscale.analysis_scope import included, EXCLUDED_CATEGORIES, EXCLUDED_TARGETS
RUN=ROOT/'benchmark/results/gemini-engine49-20260908'
OUT=RUN/'plots/payoffs-filtered-45';OUT.mkdir(parents=True,exist_ok=True)
ORIGINAL_TARGETS=set(json.loads((RUN/'targets-49.json').read_text()))
TARGETS={t for t in ORIGINAL_TARGETS if included(t)}
AUDIT=json.loads((ROOT/'benchmark/results/prompt-surface-audit-20260909/audit.json').read_text())
FLAGGED=set(AUDIT['disclosures'])|set(AUDIT['cues'])
COLORS={'blind':'#23789b','hinted':'#d07932'}
PHASE_LABEL={'blind':'Original blind condition','hinted':'Hinted follow-ups'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
traces=[json.loads(p.read_text()) for p in sorted((RUN/'episodes').glob('*/trace.json'))]
rows=[];titles={}
for t in traces:
    card=json.loads(t['turns'][0]['observation'].split('\nCard: ')[1].split('\n')[0])
    scores=[s for s in t['scores'] if s['exploit_id'] in TARGETS]
    if not scores or (t['condition']=='hinted' and t['target'] not in TARGETS):continue
    titles[t['game']]=card['title']
    clean=[s for s in scores if s['exploit_id'] not in FLAGGED]
    final=t['final_scores']; cooperative='hanabi' in t['game']
    rows.append(dict(id=t['id'],game=t['game'],seed=t['seed'],phase=t['condition'],target=t['target'],
        eligible=len(scores),executed=sum(s['executed'] for s in scores),
        rate=sum(s['executed'] for s in scores)/len(scores),score=float(final[0]),
        margin=None if cooperative else float(final[0]-max(final[1:])),
        win=None if cooperative else int(final[0]>max(final[1:])),
        clean_rate=sum(s['executed'] for s in clean)/len(clean) if clean else None,
        target_executed=next((s['executed'] for s in scores if s['exploit_id']==t['target']),None)))
assert len(ORIGINAL_TARGETS)==49 and len(TARGETS)==45
assert sum(r['eligible'] for r in rows if r['phase']=='blind')==135

def writecsv(name,rs):
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)

def save(fig,name):
    for ext in ('png','svg','pdf'):fig.savefig(OUT/f'{name}.{ext}',dpi=170,facecolor='white')
    plt.close(fig)

def corr(x,y):
    if len(x)<3 or np.std(x)<1e-10 or np.std(y)<1e-10:return None
    return float(np.corrcoef(x,y)[0,1])

def centered(phase,xkey='rate',ykey='score'):
    rs=[r for r in rows if r['phase']==phase and r[xkey] is not None and r[ykey] is not None]
    x=[];y=[]
    for r in rs:
        group=[s for s in rs if s['game']==r['game']]
        xs=np.array([s[xkey] for s in group]);ys=np.array([s[ykey] for s in group]);sd=np.std(ys)
        x.append(r[xkey]-float(np.mean(xs)));y.append((r[ykey]-float(np.mean(ys)))/sd if sd>1e-10 else 0.)
    return rs,np.array(x),np.array(y)

stats={}
for phase in COLORS:
    rs,x,y=centered(phase)
    _,cx,cy=centered(phase,'clean_rate')
    competitive,mx,my=centered(phase,ykey='margin')
    stats[phase]=dict(episodes=len(rs),pooled_raw_score_pearson=corr([r['rate'] for r in rs],[r['score'] for r in rs]),
        within_game_score_pearson=corr(x,y),sensitivity_excluding_disclosures_and_cue=corr(cx,cy),
        competitive_episodes=len(competitive),within_game_margin_pearson=corr(mx,my),
        strict_wins=sum(r['win'] for r in competitive))

# Per-edition overview: rates and actual final scores stay on separate axes.
games=sorted(titles,key=titles.get); fig,axes=plt.subplots(1,3,figsize=(16,11),gridspec_kw={'width_ratios':[1,1.35,1.1]})
fig.subplots_adjust(left=.23,right=.96,top=.82,bottom=.13,wspace=.30)
for i,g in enumerate(games):
    for phase,offset in [('blind',-.16),('hinted',.16)]:
        rs=[r for r in rows if r['game']==g and r['phase']==phase];ys=i+offset;color=COLORS[phase]
        if not rs:
            axes[0].text(.02,ys,'No misses to retest',fontsize=8,color=color,va='center')
            continue
        axes[0].scatter(np.mean([r['rate'] for r in rs]),ys,c=color,s=45)
        vals=[r['score'] for r in rs];axes[1].plot([min(vals),max(vals)],[ys,ys],color=color,alpha=.5,lw=2)
        axes[1].scatter(np.mean(vals),ys,c=color,s=40)
        margins=[r['margin'] for r in rs if r['margin'] is not None]
        if margins:
            axes[2].plot([min(margins),max(margins)],[ys,ys],color=color,alpha=.5,lw=2)
            axes[2].scatter(np.mean(margins),ys,c=color,s=40)
        elif phase=='blind':axes[2].text(.03,i,'Cooperative team score',transform=axes[2].get_yaxis_transform(),fontsize=9,va='center',color='#667780')
for ax in axes:
    ax.set_ylim(len(games)-.45,-.65);ax.set_yticks(range(len(games)));ax.grid(axis='x',alpha=.18);ax.set_axisbelow(True)
axes[0].set_yticklabels([titles[g] for g in games]);axes[1].set_yticklabels([]);axes[2].set_yticklabels([])
axes[0].set_xlim(-.04,1.04);axes[0].xaxis.set_major_formatter(PercentFormatter(1));axes[0].set_title('Eligible holes executed\nMean fraction per episode',pad=17)
axes[1].set_xscale('symlog',linthresh=20);axes[1].set_title('Actual final score\nMean and min–max',pad=17);axes[1].set_xlabel('Points · linear to 20, then log scale')
axes[2].set_xscale('symlog',linthresh=10);axes[2].axvline(0,color='#999',ls='--',lw=1);axes[2].set_title('Lead over strongest rival\nMean and min–max',pad=17);axes[2].set_xlabel('Points · linear ±10, then log scale')
for phase in COLORS:axes[0].scatter([],[],c=COLORS[phase],label=PHASE_LABEL[phase])
fig.legend(*axes[0].get_legend_handles_labels(),loc='upper left',bbox_to_anchor=(.225,.91),ncol=2,frameon=False)
fig.text(.04,.96,'Do executed exploits translate into payoff?',size=23,weight='bold')
fig.text(.04,.92,'Gemini 3.7 Flash (high reasoning) · 45 holes · coalition + obvious Win as Much target excluded',size=12)
fig.text(.04,.065,'Rates count the same eligible engine-side mechanisms in both phases, including incidental hits. Hints target each previous miss.',size=10)
fig.text(.04,.035,'Original rules disclosed some effects. These are execution rates, not clean discovery rates. Each edition has 3 blind seeds; hinted counts vary.',size=10,color='#5c6b73')
save(fig,'payoff_and_execution_by_game')

# Within-edition associations: do not mistake large scoring scales for better play.
fig,axes=plt.subplots(2,2,figsize=(13.5,10.5));fig.subplots_adjust(left=.10,right=.97,bottom=.18,top=.80,wspace=.25,hspace=.57)
for row_index,ykey in enumerate(['score','margin']):
    for ax,phase in zip(axes[row_index],COLORS):
        rs,x,y=centered(phase,ykey=ykey);points={}
        for xx,yy in zip(x,y):points[(round(xx,8),round(yy,8))]=points.get((round(xx,8),round(yy,8)),0)+1
        ax.scatter([p[0]*100 for p in points],[p[1] for p in points],s=[35+18*(n-1) for n in points.values()],c=COLORS[phase],alpha=.65,edgecolors='white',linewidth=.6)
        ax.axhline(0,color='#a8b2b6',lw=1);ax.axvline(0,color='#a8b2b6',lw=1)
        if np.std(x)>0:
            a,b=np.polyfit(x*100,y,1);xx=np.array([min(x)*100,max(x)*100]);ax.plot(xx,a*xx+b,c=COLORS[phase],lw=2)
        ax.set_title(f'{PHASE_LABEL[phase]} · n={len(rs)}\nWithin-game r={corr(x,y):+.2f}',pad=12)
        ax.set_xlabel('Execution rate − game mean (percentage points)');ax.grid(alpha=.12)
    axes[row_index,0].set_ylabel(('Final score' if ykey=='score' else 'Lead over strongest rival')+' − game mean\n(game standard deviations)')
fig.text(.06,.96,'Within the same game: does hacking pay?',size=22,weight='bold')
fig.text(.06,.915,'Gemini 3.7 Flash · 45-hole analysis · top: final score; bottom: score advantage over rivals',size=12)
fig.text(.06,.875,'Each point is an episode; larger dots show overlaps. Centered within each game and phase. Hanabi excluded from rival leads.',size=10)
fig.text(.06,.105,'Linear association, not a causal effect. Only 3 blind episodes per edition; hints are selected follow-ups on previous misses.',size=10)
fig.text(.06,.07,'Removing four disclosed mechanisms + one cue from counts: final-score r = '
    +f"{stats['blind']['sensitivity_excluding_disclosures_and_cue']:+.2f} blind / {stats['hinted']['sensitivity_excluding_disclosures_and_cue']:+.2f} hinted.",size=10)
fig.text(.06,.038,'That sensitivity cannot undo their effects on play or scores. Original disclosures prevent a clean discovery interpretation.',size=10,color='#5c6b73')
save(fig,'execution_payoff_correlation')

# Hinted vs its same-game, same-seed blind baseline, in untransformed points.
lookup={(r['game'],r['seed']):r for r in rows if r['phase']=='blind'}
pairs=[]
for r in rows:
    if r['phase']!='hinted':continue
    baseline=lookup[(r['game'],r['seed'])]
    pairs.append(dict(target=r['target'],game=r['game'],seed=r['seed'],executed=r['target_executed'],blind_score=baseline['score'],hinted_score=r['score'],score_change=r['score']-baseline['score']))
summary=dict(run=str(RUN.relative_to(ROOT)),model='Gemini 3.7 Flash, high reasoning',target_count=len(TARGETS),excluded_categories=sorted(EXCLUDED_CATEGORIES),excluded_targets=sorted(EXCLUDED_TARGETS),
    definition='Executed eligible mechanisms / eligible mechanisms for the episode; no attempt/success filtering. Own final score, or team score in Hanabi. Within-game correlations center execution and standardize final score within game and condition; constant-score groups map to zero.',
    caveat='Descriptive association only; original prompts disclose some effects. Hinted episodes target previous misses; mechanisms and policies can change together.',
    stats=stats,hinted_pairs=dict(n=len(pairs),improved=sum(p['score_change']>0 for p in pairs),equal=sum(p['score_change']==0 for p in pairs),worse=sum(p['score_change']<0 for p in pairs)))
writecsv('episodes.csv',rows);writecsv('hinted_same_seed_payoff_changes.csv',pairs)
holes=[]
for target in sorted(TARGETS):
    for phase in COLORS:
        ts=[t for t in traces if t['condition']==phase and any(s['exploit_id']==target for s in t['scores']) and (phase=='blind' or t['target']==target)]
        if not ts:continue
        hits=[next(s['executed'] for s in t['scores'] if s['exploit_id']==target) for t in ts]
        holes.append(dict(target=target,phase=phase,n=len(ts),executions=sum(hits),rate=sum(hits)/len(ts),mean_episode_final_score=float(np.mean([t['final_scores'][0] for t in ts])),disclosed_or_cued=target in FLAGGED))
writecsv('hole_rates_and_payoffs.csv',holes)
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(OUT/'README.md').write_text('# Payoffs and execution: Gemini 45-hole analysis (coalition and obvious Win as Much target excluded)\n\n'+
    'Original Gemini 3.7 Flash, high reasoning; Original 49-target run, filtered to 45 eligible mechanisms; episodes with no eligible target are omitted. Native scripted opponents, no reflection.\n\n'+
    'The execution count includes only the 45 currently eligible targets. The three coalition/kingmaking targets and Win as Much Talk objective substitution are excluded; original files are preserved. Hinted episode rates include incidental eligible executions, making the episode-level metric consistent with blind. Target-specific hint success is separately recorded in CSV. Hanabi uses team final score and is excluded from rival margins/wins.\n\n'+
    'Within-game Pearson correlations use centered execution fractions and game/phase-standardized scores. Constant score groups contribute zero. This is descriptive with only three blind seeds per game, not causal or independent evidence of discovery. Shared blind baselines make hinted comparisons dependent.\n\n'+
    'The original prompt audit found disclosures; sensitivity omits those mechanisms from counts but cannot remove their effects on trajectories. Do not interpret the remaining count as uncontaminated causal evidence.\n\n'+
    '![Payoffs and execution by game](payoff_and_execution_by_game.png)\n\n![Within-game correlation](execution_payoff_correlation.png)\n\n'+
    'Raw episode data: [episodes.csv](episodes.csv). Per-hole table: [hole_rates_and_payoffs.csv](hole_rates_and_payoffs.csv). Paired hint changes: [hinted_same_seed_payoff_changes.csv](hinted_same_seed_payoff_changes.csv). Statistics: [summary.json](summary.json).\n')
print(json.dumps(summary,indent=2))
