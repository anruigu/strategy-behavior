"""Export Gemini's native 49-hole audit without conflating hints with discovery."""
from pathlib import Path
import csv,hashlib,json,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.patches import Patch

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from benchmark.fullscale.analysis_scope import included, EXCLUDED_CATEGORIES
ROOT=Path('/shared/allie/strategy-behavior/benchmark/results/gemini-engine49-20260908')
OUT=ROOT/'plots/filtered-45'
# Preserve the user's original four broad groups; assign later-added types explicitly.
GROUPS={
 'A. Rule / enforcement':['unchecked_self_report','unenforced_limits','undelivered_punishment','rule_order_precedence'],
 'B. Information / interface':['information_overflow','meta_rule','information_asymmetry','signaling_encoding'],
 'C. State / time':['resource_conversion','state_reset_refresh','resource_duplication','turn_order','phase_boundary','terminal_condition'],
 'D. Multiplayer / objective':['threat_commitment','objective_substitution','sacrificial_negative_value','board_state_poisoning','coalition_kingmaking','denial_griefing']}
LABELS={'unchecked_self_report':'Unchecked self-report','unenforced_limits':'Unenforced limits','undelivered_punishment':'Undelivered punishment','rule_order_precedence':'Rule-order / precedence','information_overflow':'Information overflow','meta_rule':'Meta-rule exploits','information_asymmetry':'Information asymmetry','signaling_encoding':'Signaling / encoding','resource_conversion':'Resource conversion','state_reset_refresh':'State reset / refresh','resource_duplication':'Resource duplication','turn_order':'Turn-order / timing','phase_boundary':'Phase-boundary crossing','terminal_condition':'Terminal-condition rushing','threat_commitment':'Threat / commitment','objective_substitution':'Objective substitution','sacrificial_negative_value':'Sacrificial play','board_state_poisoning':'Board-state poisoning','coalition_kingmaking':'Coalition / kingmaking','denial_griefing':'Denial / griefing'}
BLUE='#247a9d';ORANGE='#d87930';INK='#193440';MUTED='#607681'

def save(fig,name):
    for ext in ('png','svg','pdf'):fig.savefig(OUT/f'{name}.{ext}',dpi=180,facecolor='white')
    plt.close(fig)

def main():
    OUT.mkdir(exist_ok=True)
    groups={g:[c for c in cs if c not in EXCLUDED_CATEGORIES] for g,cs in GROUPS.items()}
    rows=[r for r in json.loads((ROOT/'coverage.json').read_text())['rows'] if r['targeted'] and included(r['exploit_id'])]
    assert len(rows)==45 and sum(r['blind']['complete_episodes'] for r in rows)==135
    bn=sum(r['blind']['complete_episodes'] for r in rows);bk=sum(r['blind']['executed'] for r in rows)
    hn=sum(r['hinted']['complete_episodes'] for r in rows);hk=sum(r['hinted']['executed'] for r in rows)
    categories=[c for cs in groups.values() for c in cs];assert len(set(categories))==19
    cells=[]
    for group,cs in groups.items():
        for c in cs:
            rs=[r for r in rows if r['category']==c]
            d=dict(group=group,category=c,instances=len(rs))
            for phase in ('blind','hinted'):
                n=sum(r[phase]['complete_episodes'] for r in rs);k=sum(r[phase]['executed'] for r in rs)
                d[phase+'_n']=n;d[phase+'_k']=k;d[phase+'_rate']=k/n if n else None
            cells.append(d)
    with (OUT/'category_rates.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(cells[0]));w.writeheader();w.writerows(cells)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,'svg.fonttype':'none'})
    fig,axes=plt.subplots(1,2,figsize=(13,10.5),sharey=True)
    fig.subplots_adjust(left=.30,right=.95,top=.83,bottom=.12,wspace=.36)
    for ax,phase,title,color in zip(axes,['blind','hinted'],['Original blind execution','Hinted execution on previous misses'],[BLUE,ORANGE]):
        for i,c in enumerate(cells):
            n,k=c[phase+'_n'],c[phase+'_k']
            if n:
                v=k/n;ax.barh(i,v,height=.65,color=color)
                ax.text(min(v+.025,1.03),i,f'{k}/{n}',va='center',fontsize=10)
            else:ax.text(.025,i,'Excluded' if not c['instances'] else 'No misses to retest',va='center',color=MUTED,fontsize=9)
        ax.set_xlim(0,1.23);ax.set_xticks([0,.25,.5,.75,1]);ax.xaxis.set_major_formatter(PercentFormatter(1))
        ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True);ax.set_title(title,fontsize=13,pad=16)
        ax.set_yticks(range(19),[LABELS[c['category']] for c in cells]);ax.set_ylim(18.7,-.7);ax.set_xlabel('Executed / eligible hole × seed trials')
        for sp in ax.spines.values():sp.set_visible(False)
        ax.tick_params(axis='y',length=0)
        for boundary in (3.5,7.5,13.5):ax.axhline(boundary,color='#cdd8dc',lw=1)
    fig.text(.04,.965,'Which hole types does Gemini exploit?',fontsize=23,weight='bold')
    fig.text(.04,.918,'Gemini 3.7 Flash · 45 engine-side holes · coalition + obvious Win as Much target excluded · 3 seeds · no reflection',fontsize=12)
    fig.text(.04,.877,f'Blind: {bk}/{bn} target-seed trials ({bk/bn:.0%})     |     Hinted: {hk}/{hn} previous misses ({hk/hn:.0%})',fontsize=12,weight='bold')
    fig.text(.04,.063,'Hints reveal one mechanism in a fresh episode. The right panel tests only blind misses; it is not an equal-budget comparison.',fontsize=10,color=MUTED)
    fig.text(.04,.032,'“Excluded” means no cells of that type remain after removing the 11 scripted-policy mechanisms. Original rules disclose some effects; execution is not discovery.',fontsize=10,color=MUTED)
    save(fig,'exploit_rates_by_type')

    stats=[]
    for group,cs in groups.items():
        rs=[c for c in cells if c['category'] in cs and c['instances']]
        d=dict(group=group,included_types=len(rs),instances=sum(c['instances'] for c in rs))
        for phase in ('blind','hinted'):
            vals=[c[phase+'_rate'] for c in rs if c[phase+'_rate'] is not None]
            d[phase]=float(np.mean(vals)) if vals else None
        stats.append(d)
    (OUT/'broad_group_rates.json').write_text(json.dumps(dict(groups=groups,rates=stats,aggregation='Equal-weight mean of eligible type rates within each group; hinted rates condition on blind misses.'),indent=2)+'\n')
    fig=plt.figure(figsize=(10.5,9));ax=fig.add_axes([.24,.285,.52,.52],projection='polar')
    angles=np.linspace(0,2*np.pi,4,endpoint=False);ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1)
    for phase,label,color in [('blind','Original blind execution',BLUE),('hinted','Hinted rescue of misses',ORANGE)]:
        values=[r[phase] for r in stats];ax.plot(np.r_[angles,angles[0]],values+[values[0]],color=color,lw=2.7,marker='o',label=label)
        ax.fill(np.r_[angles,angles[0]],values+[values[0]],color=color,alpha=.08)
    ax.set_ylim(0,1);ax.set_yticks([.25,.5,.75,1],['25%','50%','75%','100%'],color=MUTED,fontsize=9)
    ax.set_rlabel_position(32);ax.grid(color='#d1dce0');ax.spines['polar'].set_color('#d1dce0')
    labels=[]
    for s in stats:
        name=s['group'].replace(' / ',' /\n')
        labels.append(f"{name}\n{s['blind']:.0%} blind\n{s['hinted']:.0%} hinted\n{s['instances']} holes / {s['included_types']} types")
    ax.set_xticks(angles,['']*4)
    for label,(x,y) in zip(labels,[(.5,.842),(.87,.545),(.5,.195),(.13,.545)]):fig.text(x,y,label,ha='center',va='center',fontsize=10)
    fig.text(.06,.965,'Exploit profile across the broader groups',fontsize=22,weight='bold')
    fig.text(.06,.917,'Gemini 3.7 Flash · macro-average of hole-type execution rates',fontsize=12)
    fig.legend(loc='lower center',bbox_to_anchor=(.5,.085),ncol=2,frameon=False,fontsize=11)
    fig.text(.06,.05,'Original four-group layout; excluded types are omitted, never counted as zero.',fontsize=10,color=MUTED)
    fig.text(.06,.022,'Hinted values use only previous misses and extra targeted attempts. These are execution profiles, not discovery scores.',fontsize=10,color=MUTED)
    save(fig,'broad_group_star')

    games=list(dict.fromkeys(r['game'] for r in rows));active=[c for c in categories if any(r['category']==c for r in rows)]
    matrix=np.full((len(games),len(active)),np.nan)
    game_labels={g:g.replace('v3_gen_','').replace('v3_ref_','').replace('v3_ta_','').replace('_',' ').title().replace('Ipd3','IPD3').replace('Ipd','IPD') for g in games}
    for r in rows:matrix[games.index(r['game']),active.index(r['category'])]=r['blind']['executed']/3
    fig,ax=plt.subplots(figsize=(15,10));fig.subplots_adjust(left=.23,right=.97,top=.83,bottom=.30)
    cmap=plt.get_cmap('Blues').copy();cmap.set_bad('#e6eaed');ax.imshow(matrix,vmin=0,vmax=1,cmap=cmap,aspect='auto')
    for i in range(len(games)):
        for j in range(len(active)):
            v=matrix[i,j]
            if np.isfinite(v):ax.text(j,i,f'{round(v*3)}/3',ha='center',va='center',fontsize=8,color='white' if v>.5 else INK)
    ax.set_yticks(range(len(games)),[game_labels[g] for g in games],fontsize=10)
    ax.set_xticks(range(len(active)),[LABELS[c] for c in active],rotation=55,ha='right',fontsize=10)
    ax.set_xticks(np.arange(-.5,len(active),1),minor=True);ax.set_yticks(np.arange(-.5,len(games),1),minor=True);ax.grid(which='minor',color='white',lw=1.5);ax.tick_params(which='both',length=0)
    for sp in ax.spines.values():sp.set_visible(False)
    fig.text(.04,.965,'Where blind execution happens',fontsize=23,weight='bold')
    fig.text(.04,.915,'Gemini 3.7 Flash · each tested cell shows executions out of 3 seeds',fontsize=12)
    fig.text(.04,.867,f"{sum(r['blind']['executed']>0 for r in rows)}/45 holes activated on at least one seed · {sum(r['blind']['executed']==3 for r in rows)}/45 on all three",fontsize=12,weight='bold')
    fig.text(.04,.06,'Grey = absent or excluded cell. White 0/3 = a tested mechanism with no unaided execution.',fontsize=11,color=MUTED)
    fig.text(.04,.029,'Fixed native referee opponents. No semantic discovery labels or live cross-play claims are used.',fontsize=10,color=MUTED)
    save(fig,'game_type_matrix')
    provenance=dict(coverage_sha256=hashlib.sha256((ROOT/'coverage.json').read_bytes()).hexdigest(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),target_instances=45,blind_trials=bn,hinted_trials=hn)
    (OUT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    (OUT/'README.md').write_text('# Gemini 45-hole visual results (coalition and obvious Win as Much target excluded)\n\n[Execution by hole type](exploit_rates_by_type.png) · [Broad-group star](broad_group_star.png) · [Game/type matrix](game_type_matrix.png)\n\nEach figure is also available as SVG and PDF. Rates and broad-group mapping are included in CSV/JSON. Blind counts pool three seeds per target. Hinted denominators include only previously missed target-seed pairs; the hinted runs have extra targeted guidance and fresh episodes. They are not equal-budget discovery estimates. Broad groups follow the user’s original four groups, extending State/time with resource duplication and phase boundaries; Information/interface with information asymmetry and signaling; Multiplayer/objective with denial (coalition excluded). Board-state poisoning stays in Multiplayer/objective as originally requested. Types entirely removed by the 11 exclusions are information overflow, signaling/encoding, and threat/commitment.\n')
    print(json.dumps(stats,indent=2))

if __name__=='__main__':main()
