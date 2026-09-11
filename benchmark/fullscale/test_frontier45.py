from types import SimpleNamespace
from benchmark.fullscale import frontier45 as runner
from benchmark.fullscale.budget import Ledger


def test_byok_upstream_charges_count_towards_budget(tmp_path):
    runner.configure('grok-4.6');client=runner.PacedClient.__new__(runner.PacedClient)
    client.config=runner.audit.CONFIG;client.log_dir=tmp_path;client.ledger=Ledger(tmp_path/'budget.sqlite')
    class Response:
        model='x-ai/grok-4.6'
        choices=[SimpleNamespace(finish_reason='stop',message=SimpleNamespace(content='READY',refusal=None))]
        def model_dump(self,**kwargs):return {'usage':{'cost':0,'is_byok':True,'cost_details':{'upstream_inference_cost':.03}}}
    client.client=SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kwargs:Response())))
    _,meta=client.generate([{'role':'user','content':'READY'}],max_tokens=2048)
    assert meta['budget_cost_usd']==.03
    assert client.ledger.summary()['reported_usd']==.03


def test_routes_preserve_requested_models():
    assert runner.ROUTES=={'gemini-3.1-pro':'google/gemini-3.1-pro-preview','gpt-5.6-sol':'openai/gpt-5.6-sol','grok-4.6':'x-ai/grok-4.6'}
