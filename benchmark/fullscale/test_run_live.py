from collections import Counter
from .run_live import main_schedule, matched_frontier_schedule

def test_main_balanced_seats():
    rows=main_schedule([19,73])
    def counts(mode):
        return Counter((r['game'],r['seed'],p,m) for r in rows if r['mode']==mode for p,m in enumerate(r['seats']))
    assert counts('self')==counts('cross')
    assert all(len(set(r['seats']))==3 for r in rows if r['mode']=='cross')

def test_frontier_fixed_opponents_and_budget():
    rows=matched_frontier_schedule([19,73])
    def context(model):
        return Counter((r['game'],r['seed'],p,tuple(r['seats'][:p]+r['seats'][p+1:]))
                       for r in rows if r['mode']=='cross' for p,m in enumerate(r['seats']) if m==model)
    assert context('gpt-5-mini')==context('gpt-5.6-sol')
    for model in ('gpt-5-mini','gpt-5.6-sol'):
        for pid in range(3):
            assert sum(r['seats'][pid]==model for r in rows if r['mode']=='cross')==sum(r['seats'][pid]==model for r in rows if r['mode']=='self')
