"""Exercise a complete numerical fit on explicit synthetic labels, without API calls."""
from copy import deepcopy
import pytest
from prediction.io_utils import read_json,write_json
from . import STUDY
from .runtime import Session,jsonable
from .labels import episode_row,TARGETS
from . import predict


@pytest.mark.parametrize('arm',['depth','breadth'])
def test_fit_and_serialized_reproduction_with_soft_binary_groups(tmp_path,monkeypatch,arm):
    plan=read_json(STUDY/'training/plan.json'); rows=[]
    for item in plan['episodes']:
        if arm not in item['arms']: continue
        s=Session(item['game'],item['seed'])
        row,_=episode_row(dict(item=item,status='planned',steps=[],opening_observations=jsonable(s.opening)),'synthetic-test')
        # Vary labels within repeated conditions. This catches incorrectly
        # treating fractional pooled Bernoulli means as discrete classes.
        value=float(item['replicate']%3==0)
        row['targets']=dict(win=value,any_invalid=float(item['replicate']%4==0),native_score=.2+.6*value)
        row['status']='complete'; rows.append(row)
    monkeypatch.setattr(predict,'OUT',tmp_path/'prediction')
    monkeypatch.setattr(predict,'training_rows',lambda arm:deepcopy(rows))
    prepared=predict.prepare(arm); assert prepared['episodes']==288
    folder=predict.OUT/arm; m=read_json(folder/'manifest.json')
    for batch in m['batches']:
        result={q['id']:{t:.45 if t=='win' else .15 if t=='any_invalid' else .55 for t in TARGETS} for q in batch['queries']}
        write_json(folder/'batches'/(batch['id']+'.json'),dict(status='complete',predictions=result,synthetic_unit_test=True))
    fitted=predict.fit(arm); assert fitted['predictions']==432
    assert predict.reproduce(arm)==432
    predictions=read_json(folder/'test-predictions.json')
    assert all(0<=v<=1 for p in predictions for v in p['forecast'].values())
    pool=read_json(folder/'groups.evaluator.json')
    assert any(0<r['targets']['win']<1 for r in pool)
