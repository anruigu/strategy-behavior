from pathlib import Path
import os,csv
out=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(out/'matplotlib-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
rows=list(csv.DictReader((out/'curves.csv').open()))
models=[('qwen-3.8-27b','Qwen 3.8 27B*'),('kimi-k3','Kimi K3'),('glm','GLM 5.3'),('claude-haiku-4.5','Claude Haiku 4.5'),('gpt-5-mini','GPT-5 mini'),('gemini-3.7-flash','Gemini 3.7 Flash')]
fig,axes=plt.subplots(1,3,figsize=(14,4.8),sharey=True)
fields=[('balanced_current_discovery','Discovery credited in this repetition'),('balanced_cumulative_discovery','Ever credited with discovery'),('balanced_cumulative_execution','Ever executed the mechanism')]
for ax,(field,title) in zip(axes,fields):
    for (m,label),color in zip(models,plt.rcParams['axes.prop_cycle'].by_key()['color']):
        rs=[r for r in rows if r['model']==m]
        ax.plot([int(r['iteration']) for r in rs],[100*int(r[field])/int(r['balanced_n']) for r in rs],'-o',color=color,label=label,linewidth=2,markersize=5)
    ax.set(title=title,xlabel='Within-game repetition',xticks=[1,2,3,4],ylim=(-2,102))
    ax.grid(axis='y',alpha=.25)
    ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Share of model × mechanism pairs (%)')
fig.suptitle('Some learning is hidden by re-scoring, but cumulative coverage still plateaus',fontsize=15,y=.98)
fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',ncol=3,bbox_to_anchor=(.5,.025),frameon=False)
fig.text(.5,.005,'Frozen audit: 166/168 games scored. Complete four-repetition chains only: 25 mechanisms/model; *Qwen 20.\nPersistent cross-game memory; descriptive curves, no independent replicates. Cumulative discovery retains the original judge’s errors.',ha='center',fontsize=8)
fig.tight_layout(rect=[0,.17,1,.92])
for ext in ['png','pdf']:fig.savefig(out/f'learning_diagnostic.{ext}',dpi=180,bbox_inches='tight')
