from concurrent.futures import ThreadPoolExecutor
import pytest
from .budget import Ledger, BudgetExceeded

def test_concurrent_budget(tmp_path):
    ledger=Ledger(tmp_path/'budget.sqlite',10)
    def reserve(_):
        try: return ledger.reserve('test',3)
        except BudgetExceeded: return None
    with ThreadPoolExecutor(max_workers=20) as pool: ids=list(pool.map(reserve,range(40)))
    assert sum(x is not None for x in ids)==3
    assert ledger.summary()['committed_usd']==9
    ident=next(x for x in ids if x)
    ledger.settle(ident,1)
    ledger.reserve('test',3)
    assert ledger.summary()['committed_usd']==10

def test_unknown_charge_stays_reserved(tmp_path):
    ledger=Ledger(tmp_path/'budget.sqlite',10)
    ident=ledger.reserve('test',9)
    ledger.settle(ident,None)
    with pytest.raises(BudgetExceeded): ledger.reserve('test',2)
    with pytest.raises(ValueError): ledger.settle(ident,0)
