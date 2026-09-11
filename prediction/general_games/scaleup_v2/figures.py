"""Export standalone scientific figures from the audited study summary."""
from prediction import modeling
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from prediction.io_utils import read_json,write_json
from . import STUDY

COLORS={'linear':'#a36036','few_4':'#4576a8','corrected_4':'#28583d','few_8':'#9582aa','few_16':'#c49b47'}
NAMES={'linear':'Learned linear','few_4':'4-shot','corrected_4':'4-shot + learned correction','few_8':'8-shot','few_16':'16-shot'}


def build():
    s=read_json(STUDY/'summary.json');folder=STUDY/'figures';folder.mkdir(exist_ok=True);files=[]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
    fig,axes=plt.subplots(1,2,figsize=(11.5,5.2),sharey=True)
    upper=1.12*max(r['score'] for r in s['scores'] if r['target']=='win' and r['method'] in set(COLORS)|{'pooled_few_4','pooled_few_16'})
    for ax,suite,title in zip(axes,('parameter','family'),('Higher parameter values · 160 episodes','Four unseen families · 112 episodes')):
        rows=[r for r in s['scores'] if r['suite']==suite and r['target']=='win']
        for method,color in COLORS.items():
            rr=sorted([r for r in rows if r['method']==method],key=lambda r:r['size'])
            ax.plot([r['size'] for r in rr],[r['score'] for r in rr],marker='o',color=color,label=NAMES[method],linewidth=2 if method=='corrected_4' else 1.4,linestyle='--' if method.startswith('few') else '-')
        for method,color,name in [('pooled_few_4','#176b79','Pooled 4-shot (secondary)'),('pooled_few_16','#b98166','Pooled 16-shot (secondary)')]:
            r=next(r for r in rows if r['method']==method)
            ax.plot([440],[r['score']],marker='D',color=color,markerfacecolor='white',markersize=7,linestyle='none',label=name)
        noise=next(r['within_condition_noise'] for r in rows if r['method']=='few_4')
        ax.axhline(noise,color='#999999',linestyle=':',linewidth=1,label='Estimated within-condition variance')
        ax.set(title=title,xlabel='Training episodes',xticks=[120,248,440],ylim=(0,upper));ax.grid(axis='y',alpha=.15)
    axes[0].set_ylabel('Win / full-solution Brier (lower is better)')
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,ncol=3,loc='lower center',bbox_to_anchor=(.5,.055),frameon=False,fontsize=8.5)
    fig.suptitle('Training depth versus few-shot prediction',x=.08,ha='left',fontsize=15)
    fig.text(.08,.015,'Primary curves use fixed prospective tests; pooled controls were added later. Variance is a noisy floor component, not a proven bound.',fontsize=8,color='#666666')
    fig.tight_layout(rect=(0,.27,1,.96))
    for ext in ('png','pdf','svg'):
        path=folder/f'learning-curves.{ext}';fig.savefig(path,bbox_inches='tight');files.append(str(path.relative_to(STUDY)))
    plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(10.5,7.3))
    for ax,p in zip(axes.flat,s['parameters']):
        for model,color in [('qwen-3.8-27b','#4576a8'),('glm','#8b6a91')]:
            yy=[next(m['behavior'] for m in level['by_model'] if m['model']==model) for level in p['levels']]
            ax.plot([l['value'] for l in p['levels']],yy,marker='o',color=color,label=model)
        ax.set(title=p['title'],xlabel=p['axis'].replace('_',' '),ylabel=p['target'].replace('_',' '),ylim=(0,1),xticks=[l['value'] for l in p['levels']]);ax.grid(axis='y',alpha=.15)
    handles,labels=axes.flat[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=2,frameon=False,bbox_to_anchor=(.5,.025))
    fig.suptitle('Parameter responses by player model',x=.08,ha='left',fontsize=15)
    fig.text(.08,.008,'20 trials per model/value; conditional rates use eligible trials. Two seeds × two seats × five repeats. High values were collected later.',fontsize=8,color='#666666')
    fig.tight_layout(rect=(0,.07,1,.96))
    for ext in ('png','pdf','svg'):
        path=folder/f'parameter-responses.{ext}';fig.savefig(path,bbox_inches='tight');files.append(str(path.relative_to(STUDY)))
    plt.close(fig);write_json(folder/'inventory.json',dict(files=files,source='../summary.json'));return files


if __name__=='__main__':print(build())
