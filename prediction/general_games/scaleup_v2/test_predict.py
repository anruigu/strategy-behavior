from copy import deepcopy
import json
import pytest

from prediction.io_utils import read_json,digest
from . import DATA,STUDY
from .predict import OUT,prompt,retrieve,parse,request_size,group_rows,family_weights


def test_forecast_inputs_ignore_query_targets_and_hidden_state():
    m=read_json(OUT/'n120/manifest.json');pool=read_json(OUT/'n120/groups.evaluator.json');specs=read_json(DATA/'mechanics.v2.json')
    for q in m['queries']:
        changed=deepcopy(q);changed['targets']={'win':999};changed['future']='SECRET_FUTURE';changed['hidden_state']='SECRET_BOARD'
        for shots in (4,8,16):
            assert prompt([q],pool,specs,shots,'test')==prompt([changed],pool,specs,shots,'test')


def test_example_budget_nesting_and_calibration_exclusion():
    m=read_json(OUT/'n120/manifest.json');pool=read_json(OUT/'n120/groups.evaluator.json');lookup={r['id']:r for r in pool}
    for q in m['queries']:
        picked=retrieve(q,pool,16)
        assert retrieve(q,pool,4)==picked[:4] and retrieve(q,pool,8)==picked[:8]
        assert len({digest(r['inputs']) for r in picked})==16
        assert not {r['opening_group'] for r in picked}&{q['opening_group']}
    for ident in m['calibration_ids']:
        q=lookup[ident]
        assert all(r['inputs']['family_id']!=q['inputs']['family_id'] for r in retrieve(q,pool,16,True))
    for batch in m['batches']:assert request_size(batch['messages'])<=40000


def test_parser_rejects_ambiguity_missing_queries_and_wrong_support():
    batch={'queries':[{'id':'q','supported':['win','any_invalid']}]}
    valid={'predictions':[{'id':'q','values':{'win':.6,'any_invalid':.1}}]}
    assert parse('```json\n'+json.dumps(valid)+'\n```',batch)['q']['win']==.6
    for obj in [{'predictions':[]},{'predictions':[{'id':'q','values':{'win':.6}}]},
                {'predictions':[{'id':'q','values':{'win':1.6,'any_invalid':.1}}]}]:
        with pytest.raises(ValueError):parse(json.dumps(obj),batch)
    with pytest.raises(ValueError):parse(json.dumps(valid)+json.dumps(valid),batch)


def test_replicate_means_keep_counts_and_family_balancing():
    rows=read_json(STUDY/'historical-training.evaluator.json');r=deepcopy(rows[0]);r['episode_id']='synthetic-repeat';r['targets']['win']=1-rows[0]['targets']['win']
    grouped=group_rows([rows[0],r]);assert grouped[0]['targets']['win']==.5 and grouped[0]['target_counts']['win']==2
    pool=group_rows(rows);ids=list(range(len(pool)));weights=family_weights(pool,ids,'win');totals={}
    for row,w in zip(pool,weights):totals[row['inputs']['family_id']]=totals.get(row['inputs']['family_id'],0)+w
    assert max(totals.values())-min(totals.values())<1e-10
