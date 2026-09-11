"""Export a standalone coverage figure; cells are planted coverage, not model rates."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from engines_scaleup_20260907 import GAMES
from .taxonomy import CATEGORIES,ALLOCATION,GROUPS

def main():
    games=list(GAMES);groups=list(GROUPS.values());colors=['#f5f6f7','#587baa','#bd7958','#608d72','#9a7faf','#b29745']
    matrix=np.array([[next(i+1 for i,group in enumerate(groups) if cat in group) if game in ALLOCATION[cat] else 0 for game in games] for cat in CATEGORIES])
    fig,ax=plt.subplots(figsize=(12,10));ax.imshow(matrix,cmap=ListedColormap(colors),vmin=0,vmax=5,aspect='auto')
    for y in range(20):
        for x in range(10):
            if matrix[y,x]:ax.text(x,y,'●',ha='center',va='center',color='white',fontsize=15)
    ax.set_xticks(range(10),['Seven Seal','Commons','Hanabi','IPD','Exchange','Win as Much','IPD × 3','Auction','Estate','Battleship'],rotation=35,ha='right')
    ax.set_yticks(range(20),[c.replace('_',' ').capitalize() for c in CATEGORIES])
    ax.set_xticks(np.arange(-.5,10,1),minor=True);ax.set_yticks(np.arange(-.5,20,1),minor=True)
    ax.grid(which='minor',color='white',linewidth=2);ax.tick_params(which='minor',bottom=False,left=False)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.set_title('60 planted opportunities · 20 types · 10 games\nThree instances per type; 4–8 per game',loc='left',pad=20,fontsize=18)
    fig.text(.02,.02,'Coverage, not measured discovery. Only 3 unchecked self-report instances. Engine: scaleup-20260907.1',fontsize=10,color='#555555')
    fig.tight_layout(rect=(0,.045,1,1));out=Path('benchmark/scaleup/artifacts');out.mkdir(exist_ok=True)
    fig.savefig(out/'coverage_matrix.png',dpi=180);fig.savefig(out/'coverage_matrix.svg');plt.close(fig)
    svg=out/'coverage_matrix.svg';svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')

if __name__=='__main__':main()
