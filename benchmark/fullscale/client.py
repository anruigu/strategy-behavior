"""Single-attempt client with fixed output allowance and pre-request reservation."""
from dataclasses import asdict
import json
import time
from benchmark.clients import ModelClient, now, write_json
from .budget import Ledger

# Conservative uniform upper bound, above observed/catalog rates for this roster.
# Input is bounded by UTF-8 bytes plus generous chat serialization overhead.
INPUT_USD_PER_TOKEN=0.00002
OUTPUT_USD_PER_TOKEN=0.00012

class StudyClient(ModelClient):
    def __init__(self, config, log_dir, ledger):
        super().__init__(config, log_dir)
        self.ledger=ledger

    def generate(self, messages, model=None, temperature=None, max_tokens=16384, purpose='play'):
        if model is not None and model != self.config.model_id: raise ValueError('Model mismatch')
        if not 1 <= max_tokens <= 16384: raise ValueError('Fixed output limit exceeded')
        input_bound=len(json.dumps(messages,ensure_ascii=False).encode())+4096+256*len(messages)
        if input_bound > 120000: raise ValueError('Context byte budget exceeded')
        bound=0.0 if self.config.provider=='flt' else input_bound*INPUT_USD_PER_TOKEN+max_tokens*OUTPUT_USD_PER_TOKEN
        ident=self.ledger.reserve(self.config.model_id,bound)
        request=dict(model=self.config.provider_model,messages=messages,max_tokens=max_tokens,
                     extra_body={'reasoning':{'effort':self.config.reasoning_effort}})
        if self.config.provider=='openrouter':
            request['extra_body']['provider']={'max_price':{'prompt':20,'completion':120,'request':0}}
        if self.config.temperature is not None: request['temperature']=self.config.temperature
        path=self.log_dir/(ident+'.json')
        record=dict(call_id=ident,purpose=purpose,timestamp=now(),config=asdict(self.config),request=request,reserved_usd=bound,attempts=[])
        write_json(path,record)
        start=time.monotonic()
        try:
            response=self.client.chat.completions.create(**request)
            raw=response.model_dump(mode='json')
        except Exception as exc:
            # A timeout can occur after billing; retain the reservation, no retry.
            self.ledger.settle(ident,None,type(exc).__name__)
            record['attempts'].append(dict(error=type(exc).__name__,http_status=getattr(exc,'status_code',None),error_message=str(exc).replace(self.client.api_key,'[REDACTED]')[:1000],seconds=time.monotonic()-start))
            write_json(path,record)
            raise RuntimeError(f'{self.config.model_id}: transport failure; call {ident}') from None
        cost=(raw.get('usage') or {}).get('cost')
        if self.config.provider=='flt': cost=0.0
        self.ledger.settle(ident,cost)
        record['attempts'].append(dict(response=raw,seconds=time.monotonic()-start))
        write_json(path,record)
        choice=response.choices[0]
        reason=choice.finish_reason
        content=choice.message.content or ''
        status='ok'
        if reason=='content_filter' or getattr(choice.message,'refusal',None): status='refusal'
        elif reason=='length': status='truncated'
        elif reason!='stop' or not content.strip(): status='invalid_response'
        return content,dict(call_id=ident,actual_model=response.model,finish_reason=reason,status=status,
                            usage=raw.get('usage'),timestamp=record['timestamp'])
