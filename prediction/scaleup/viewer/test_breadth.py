import pytest
from .breadth import BreadthDataset


def test_catalog_and_overlapping_arm_denominators():
    d=BreadthDataset(); all_rows=d.summary(); depth=d.summary({'cohort':['depth']}); broad=d.summary({'cohort':['breadth']}); test=d.summary({'cohort':['test']})
    assert all_rows['counts']['planned']==624
    assert depth['counts']['planned']==broad['counts']['planned']==288
    assert test['counts']['planned']==144
    assert sum(f['role']=='Holdout' for f in all_rows['families'])==6
    assert sum(f['planned'] for f in depth['families'])==288
    assert sum(f['planned'] for f in broad['families'])==288


def test_family_filter_and_game_inspection():
    d=BreadthDataset(); s=d.summary({'family':['gops'],'cohort':['test']})
    assert s['counts']['families']==1 and s['counts']['planned']==24
    g=d.game(s['families'][0]['game_id'])
    assert g['game']['family_id']=='gops' and g['mechanics'] and g['opening']['observations']


def test_episode_identifiers_are_allowlisted():
    d=BreadthDataset()
    with pytest.raises(KeyError): d.episode('../../../../.env')
