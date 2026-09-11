"""Provisional curves using a fixed, completed paired-chain subset per model."""
import csv,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'benchmark/results/repeated45-20260909';OUT=BASE/'plots'

def main():
 rows=list(csv.DictReader((OUT/'hole_curves.csv').open()));plan=json.loads((BASE/'plan.json').read_text());names={'qwen-3.8-27b-medium':'Qwen (medium)','glm':'GLM 5.3','gemini-3.1-pro':'Gemini Pro','gpt-5.6-sol':'GPT-5.6 Sol','grok-4.6':'Grok 4.6'};summary={}
 fig,axes=plt.subplots(1,5,figsize=(16,5.4),sharey=True);fig.subplots_adjust(left=.07,right=.98,top=.69,bottom=.29,wspace=.17)
 for ax,m in zip(axes,names):
  sets=[{(r['game'],r['seed']) for r in rows if r['model']==m and r['condition']==a and r['iteration']=='4'} for a in ('transcript_only','reflection')];paired=set.intersection(*sets);out=dict(paired_chains=len(paired),opportunities=0,conditions={})
  for a,color,style in [('transcript_only','#65758b','--'),('reflection','#198b78','-')]:
   cs=[];ns=[];current=[]
   for i in range(1,5):
    rr=[r for r in rows if r['model']==m and r['condition']==a and int(r['iteration'])==i and (r['game'],r['seed']) in paired];cs.append(sum(r['cumulative_executed']=='True' for r in rr));ns.append(len(rr));current.append(sum(r['executed']=='True' for r in rr))
   assert len(set(ns))==1,'Changing cohort';out['opportunities']=ns[0];out['conditions'][a]=dict(cumulative_hits=cs,current_hits=current)
   if ns[0]:ax.plot(range(1,5),[n/ns[0] for n in cs],color=color,ls=style,marker='o',lw=2,label='Reflection + transcript' if a=='reflection' else 'Transcript only')
  summary[m]=out;ax.set_title(names[m]+f"\n{len(paired)}/51 paired chains",fontsize=11,pad=12);ax.set_ylim(0,1.03);ax.set_xticks([1,2,3,4]);ax.set_xlabel('Episode');ax.set_yticks([0,.25,.5,.75,1],['0%','25%','50%','75%','100%']);ax.grid(alpha=.16)
  if not paired:ax.text(.5,.5,'Awaiting completed pairs',ha='center',va='center',transform=ax.transAxes,fontsize=9)
 axes[0].set_ylabel('Activated at least once so far');fig.suptitle('Reflection: early cumulative coverage on completed pairs',fontsize=20,y=.98)
 fig.text(.5,.86,'PROVISIONAL · each model uses a fixed subset completed in both arms · subsets differ between models',ha='center',fontsize=11)
 handles=[plt.Line2D([],[],color='#65758b',ls='--',marker='o'),plt.Line2D([],[],color='#198b78',marker='o')];fig.legend(handles,['Transcript only','Reflection + transcript'],loc='lower center',bbox_to_anchor=(.5,.13),ncol=2,frameon=False)
 fig.text(.5,.045,'Both arms retain full visible history. Cumulative OR is not per-episode exploit rate. Incomplete/API-failed chains are excluded, not scored as misses.',ha='center',fontsize=10)
 fig.savefig(OUT/'paired_progress.png',dpi=170,bbox_inches='tight',facecolor='white');plt.close(fig)
 (BASE/'paired-progress.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
