import importlib.util
from pathlib import Path
import pytest

spec=importlib.util.spec_from_file_location('unified_prompt_report',Path(__file__).with_name('report_prompt_results.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)


def test_hint_rows_score_only_the_revealed_target():
    t=dict(target='g.meta_rule',game='g',seed=19,scores=[
        dict(exploit_id='g.meta_rule',category='meta_rule',executed=False),
        dict(exploit_id='g.board_state_poisoning',category='board_state_poisoning',executed=True)])
    rows=r.rows_from_trace(t,Path('/test'),['g.meta_rule','g.board_state_poisoning'],'hinted')
    assert len(rows)==1 and rows[0]['target']=='g.meta_rule' and not rows[0]['executed']


def test_missing_and_zero_are_distinct_and_duplicates_fail():
    groups={'Information':['meta_rule'],'Multiplayer':['board_state_poisoning']}
    row=dict(target='g.meta_rule',category='meta_rule',seed=19,executed=False)
    result=r.summarize([row],['g.meta_rule','g.board_state_poisoning'],groups)
    assert result['cells']['g.meta_rule']['rate']==0
    assert result['cells']['g.board_state_poisoning']['rate'] is None
    assert result['groups']['Multiplayer'] is None
    with pytest.raises(AssertionError,match='Duplicate'):
        r.summarize([row,row],['g.meta_rule'],{'Information':['meta_rule']})


def test_original_star_grouping_is_preserved():
    assert 'meta_rule' in r.CONSTANTS['GROUPS']['B. Information / interface']
    assert 'board_state_poisoning' in r.CONSTANTS['GROUPS']['D. Multiplayer / objective']
