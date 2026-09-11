"""Present the offline trace audit without confusing information value with fixed-action value."""
import csv,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'benchmark/results/trace-payoff-audit-20260909'
rs=json.loads((OUT/'trace_evidence.json').read_text());summary=json.loads((OUT/'summary.json').read_text())
labels=['Improves final advantage','No change in final advantage','Worsens final advantage','Information: policy value unresolved','Control unfinished: unresolved']
colors=['#36897b','#c0c6cc','#c95f50','#6f80b8','#e1b866']
def bucket(r):
 if not r['control_done']:return 4
 if r['information']:return 3
 return 0 if r['margin_delta']>0 else 2 if r['margin_delta']<0 else 1
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
def save(fig,name):
 for ext in ['png','svg','pdf']:fig.savefig(OUT/f'{name}.{ext}',dpi=160,bbox_inches='tight',facecolor='white')
 plt.close(fig)
fig,ax=plt.subplots(figsize=(13,8));fig.subplots_adjust(left=.22,top=.78,bottom=.20,right=.96)
for y,s in enumerate(summary['by_model']):
 rr=[r for r in rs if r['model']==s['model'] and r['phase']==s['phase']];left=0
 for i in range(5):
  n=sum(bucket(r)==i for r in rr);w=n/len(rr)*100
  ax.barh(y,w,left=left,color=colors[i],height=.72)
  if w>=4:ax.text(left+w/2,y,str(n),ha='center',va='center',fontsize=9,color='white' if i in (0,2,3) else '#26343c')
  left+=w
 ax.text(101,y,f'n={len(rr)}',va='center',fontsize=9)
ax.set_yticks(range(12),[s['model'].replace('gemini-3.7-flash','Gemini low').replace('claude-haiku-4.5','Haiku')+' · '+s['phase'] for s in summary['by_model']]);ax.invert_yaxis();ax.set_xlim(0,110);ax.set_xticks([0,25,50,75,100],['0%','25%','50%','75%','100%']);ax.set_xlabel('Share of executed episode–hole pairs · numbers inside bars are counts')
fig.text(.03,.97,'Did the executed mechanism pay off?',fontsize=23,weight='bold')
fig.text(.03,.92,'972 original traces verified · 45 eligible holes · 601 executed pairs · no new model calls',fontsize=12)
fig.text(.03,.87,'Final advantage = own score − strongest rival; Hanabi uses team score. One hole patched; later actions held fixed.',fontsize=10)
handles=[plt.Rectangle((0,0),1,1,color=c) for c in colors];fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.53,.045),ncol=2,frameon=False,fontsize=10)
fig.text(.03,.015,'Descriptive, conditional on execution. Hints target each model’s misses; cohorts differ. Information and changed horizons need adaptive controls.',fontsize=9,color='#59656c')
save(fig,'payoff_diagnosis_by_model')
fig,ax=plt.subplots(figsize=(13,17));fig.subplots_adjust(left=.42,right=.96,top=.90,bottom=.09)
targets=sorted({r['target'] for r in rs})
for y,target in enumerate(targets):
 rr=[r for r in rs if r['target']==target];left=0
 for i in range(5):
  n=sum(bucket(r)==i for r in rr);w=n/len(rr)*100;ax.barh(y,w,left=left,color=colors[i],height=.73)
  if w>=8:ax.text(left+w/2,y,str(n),ha='center',va='center',fontsize=8,color='white' if i in (0,2,3) else '#26343c')
  left+=w
 ax.text(101,y,str(len(rr)),va='center',fontsize=8)
def short(t):
 game,cat=t.split('.');game=game.removeprefix('v3_').removeprefix('ref_').removeprefix('ta_').removeprefix('gen_')
 return game.replace('_',' ')+' / '+cat.replace('_',' ')
ax.set_yticks(range(len(targets)),[short(t) for t in targets],fontsize=8);ax.invert_yaxis();ax.set_xlim(0,110);ax.set_xticks([0,25,50,75,100],['0%','25%','50%','75%','100%']);ax.set_xlabel('Share of executions · counts inside bars; total at right')
fig.text(.04,.975,'Final-payoff diagnosis for all 45 holes',fontsize=23,weight='bold')
fig.text(.04,.95,'Six model configurations · blind and targeted hints pooled · conditional on mechanism activation',fontsize=11)
fig.text(.04,.928,'Fixed-action patch comparisons identify mechanical effects, not the value of information or an adapting strategy.',fontsize=10)
fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.53,.02),ncol=2,frameon=False,fontsize=10)
save(fig,'payoff_diagnosis_all_holes')
print('wrote both figures')
