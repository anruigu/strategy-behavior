from collections import Counter
from .design import lineups,schedule,family,MODELS_ORDER


def test_equal_model_and_seat_budgets():
    for n in (2,3,4):
        rows=lineups(n)
        assert len(rows['cross'])==len(rows['self'])
        for model in MODELS_ORDER:
            for seat in range(n):
                assert sum(x[seat]==model for x in rows['cross'])==sum(x[seat]==model for x in rows['self'])
        assert all(len(set(map(family,row)))==n for row in rows['cross'])
        assert all(len(set(row))==1 for row in rows['self'])


def test_opponent_matched_tier_contrast():
    for n in (2,3,4):
        cross=lineups(n)['cross']
        for small,big in [('claude-haiku-4.5','claude-opus-5'),('gpt-5-mini','gpt-5.6-sol')]:
            def surroundings(model):
                return Counter((p,row[:p]+row[p+1:]) for row in cross for p,m in enumerate(row) if m==model)
            assert surroundings(small)==surroundings(big)


def test_schedule_unique():
    rows=schedule({'example_three':3,'example_two':2},[19,73])
    assert len(rows)==2*(24+32)
    assert len({r['id'] for r in rows})==len(rows)
