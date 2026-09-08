"""Coverage figure for the V3 editions: planted mechanisms per type and edition (not discovery rates)."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from engines_v3_20260908 import EDITIONS, VERSION
from .taxonomy import CATEGORIES, ALLOCATION, GROUPS

# Reference categorical palette, fixed slot order (dataviz skill, light surface).
SERIES = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4']
SURFACE, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e6e5e1'


def main():
    ids = [g.NAME for g in EDITIONS]; titles = [g.TITLE.replace(' · ', '\n') for g in EDITIONS]
    groups = list(GROUPS.items())
    fig, ax = plt.subplots(figsize=(15, 9.5), facecolor=SURFACE); ax.set_facecolor(SURFACE)
    for y, cat in enumerate(CATEGORIES):
        gi = next(i for i, (_, cats) in enumerate(groups) if cat in cats)
        for x, gid in enumerate(ids):
            if gid in ALLOCATION[cat]:
                ax.add_patch(plt.Rectangle((x - .5 + .06, y - .5 + .06), .88, .88, facecolor=SERIES[gi], edgecolor='none', linewidth=0, joinstyle='round'))
    # game boundaries between editions of different base games
    for x in range(1, len(ids)):
        if EDITIONS[x].BASE != EDITIONS[x - 1].BASE: ax.axvline(x - .5, color=INK2, linewidth=.8, alpha=.5)
        else: ax.axvline(x - .5, color=GRID, linewidth=.8)
    for y in range(1, len(CATEGORIES)): ax.axhline(y - .5, color=GRID, linewidth=.8)
    ax.set_xlim(-.5, len(ids) - .5); ax.set_ylim(len(CATEGORIES) - .5, -.5)
    ax.set_xticks(range(len(ids)), titles, rotation=55, ha='right', fontsize=9, color=INK)
    ax.set_yticks(range(len(CATEGORIES)), [c.replace('_', ' ').capitalize() for c in CATEGORIES], fontsize=10, color=INK)
    ax.tick_params(length=0)
    for spine in ax.spines.values(): spine.set_visible(False)
    counts = [sum(gid in ALLOCATION[c] for c in CATEGORIES) for gid in ids]
    for x, n in enumerate(counts): ax.text(x, -.9, str(n), ha='center', va='bottom', fontsize=9, color=INK2)
    ax.text(-.5, -1.55, 'mechanisms per edition', ha='left', va='bottom', fontsize=9, color=INK2)
    ax.legend(handles=[Patch(facecolor=SERIES[i], label=name) for i, (name, _) in enumerate(groups)], loc='upper left', bbox_to_anchor=(1.01, 1), frameon=False, fontsize=10, title='Taxonomy group', title_fontsize=10)
    fig.suptitle('60 planted mechanisms · 20 types · 19 editions of 10 games', x=.02, ha='left', fontsize=17, color=INK, y=.985)
    fig.text(.02, .935, 'Three per type; two to five per edition. A cell marks a planted, witness-verified mechanism, not a measured discovery.', fontsize=10.5, color=INK2)
    fig.text(.02, .015, f'Engine {VERSION}. Editions of the same game share rules and board; thin dark lines separate games. Source: benchmark/v3/artifacts/specs.json', fontsize=9, color=INK2)
    fig.tight_layout(rect=(0, .03, .84, .92))
    out = Path('benchmark/v3/artifacts'); out.mkdir(exist_ok=True)
    fig.savefig(out / 'coverage_matrix.png', dpi=170, facecolor=SURFACE); fig.savefig(out / 'coverage_matrix.svg', facecolor=SURFACE); plt.close(fig)
    print('wrote', out / 'coverage_matrix.png')


if __name__ == '__main__': main()
