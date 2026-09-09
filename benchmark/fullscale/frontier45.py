"""Run the exact revised45 snapshot with a requested frontier endpoint and paced calls."""
import argparse,json,sys,threading,time
from dataclasses import asdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'benchmark/results/frontier45-20260909'
SOURCE=BASE/'source'
sys.path.insert(0,str(SOURCE))
from benchmark.clients import ModelConfig,write_json,now
from benchmark.fullscale import gemini_audit as audit
from benchmark.fullscale import revised45 as study
from benchmark.fullscale.budget import Ledger
ROUTES={'gemini-3.1-pro':'google/gemini-3.1-pro-preview','gpt-5.6-sol':'openai/gpt-5.6-sol','grok-4.6':'x-ai/grok-4.6'}
lock=threading.Lock();next_request=0.
class PacedClient(audit.StudyClient):
    def generate(self,messages,model=None,temperature=None,max_tokens=16384,purpose='play'):
        global next_request
        if model is not None and model!=self.config.model_id:raise ValueError('Model mismatch')
        if not 1<=max_tokens<=16384:raise ValueError('Token allowance exceeded')
        with lock:
            instant=time.monotonic();delay=max(0,next_request-instant);next_request=max(instant,next_request)+.65
        if delay:time.sleep(delay)
        size=len(json.dumps(messages,ensure_ascii=False).encode())+4096+256*len(messages)
        if size>120000:raise ValueError('Context byte budget exceeded')
        bound=size*.00002+max_tokens*.00012
        ident=self.ledger.reserve(self.config.model_id,bound)
        request=dict(model=self.config.provider_model,messages=messages,max_tokens=max_tokens,
                     extra_body={'reasoning':{'effort':self.config.reasoning_effort},'provider':{'max_price':{'prompt':20,'completion':120,'request':0}}})
        record=dict(call_id=ident,purpose=purpose,timestamp=now(),config=asdict(self.config),request=request,reserved_usd=bound,attempts=[])
        path=self.log_dir/(ident+'.json');write_json(path,record);start=time.monotonic()
        try:response=self.client.chat.completions.create(**request);raw=response.model_dump(mode='json')
        except Exception as exc:
            self.ledger.settle(ident,None,type(exc).__name__)
            record['attempts'].append(dict(error=type(exc).__name__,http_status=getattr(exc,'status_code',None),error_message=str(exc).replace(self.client.api_key,'[REDACTED]')[:1000],seconds=time.monotonic()-start))
            write_json(path,record);raise RuntimeError(f'{self.config.model_id}: transport failure; call {ident}') from None
        usage=raw.get('usage') or {};costs=[v for v in [usage.get('cost'),(usage.get('cost_details') or {}).get('upstream_inference_cost')] if isinstance(v,(int,float))]
        billed=max(costs) if costs else None
        self.ledger.settle(ident,billed,'includes upstream cost when BYOK');record['budget_cost_usd']=billed
        record['attempts'].append(dict(response=raw,seconds=time.monotonic()-start));write_json(path,record)
        choice=response.choices[0];content=choice.message.content or '';reason=choice.finish_reason
        status='refusal' if reason=='content_filter' or getattr(choice.message,'refusal',None) else 'truncated' if reason=='length' else 'invalid_response' if reason!='stop' or not content.strip() else 'ok'
        return content,dict(call_id=ident,actual_model=response.model,finish_reason=reason,status=status,usage=usage,budget_cost_usd=billed,timestamp=record['timestamp'])

def configure(name):
    audit.CONFIG=ModelConfig(name,'openrouter',ROUTES[name],'https://openrouter.ai/api/v1','OPENROUTER_API_KEY',temperature=None,reasoning_effort='high')
    audit.StudyClient=PacedClient

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model',choices=list(ROUTES),required=True);p.add_argument('--probe',action='store_true');a=p.parse_args();configure(a.model)
    out=BASE/a.model;ledger=ROOT/'benchmark/results/fullscale-20260908/budget.sqlite'
    if a.probe:
        c=PacedClient(audit.CONFIG,out/'preflight-calls',Ledger(ledger))
        reply,meta=c.generate([{'role':'system','content':'This is an API connectivity test. Follow the requested literal output.'},{'role':'user','content':'Reply with exactly READY.'}],max_tokens=2048,purpose='frontier45_route_preflight')
        write_json(out/'preflight.json',dict(requested=ROUTES[a.model],reply=reply,meta=meta));print(json.dumps(dict(requested=ROUTES[a.model],reply=reply,meta=meta)))
        if meta['status']!='ok':raise RuntimeError('Route preflight did not return a complete answer')
    else:
        import os
        os.chdir(SOURCE)
        study.run(out,ledger,8)
