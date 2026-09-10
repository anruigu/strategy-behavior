"""Bounded, logged requests for longer focal transcript histories."""
from dataclasses import asdict
import json
import time

from benchmark.clients import ModelClient, now, write_json
from benchmark.fullscale.budget import BudgetExceeded


class ReflectionClient(ModelClient):
    def __init__(self, config, path, ledger, limits):
        super().__init__(config, path)
        self.ledger, self.limits = ledger, limits
        self.client = self.client.with_options(timeout=180)

    def once(self, messages, limit, purpose):
        size = len(json.dumps(messages, ensure_ascii=False).encode()) + 4096 + 256 * len(messages)
        if size > 300000:
            raise ValueError('Full focal transcript exceeds 300k-byte bound; no silent truncation')
        bound = 0.0 if self.config.provider == 'flt' else size * .00002 + limit * .00012
        while True:
            try:
                ident = self.ledger.reserve(self.config.model_id, bound)
                break
            except BudgetExceeded:
                status = self.ledger.summary()
                pending = status['states'].get('reserved', {}).get('committed_usd', 0)
                if pending and status['committed_usd'] - pending + bound <= status['ceiling_usd']:
                    time.sleep(.5)
                    continue
                raise
        request = dict(model=self.config.provider_model, messages=messages, max_tokens=limit,
                       extra_body={'reasoning': {'effort': self.config.reasoning_effort}})
        if self.config.provider == 'openrouter':
            request['extra_body']['provider'] = {'max_price': {'prompt': 20, 'completion': 120, 'request': 0}}
        if self.config.temperature is not None:
            request['temperature'] = self.config.temperature
        record = dict(call_id=ident, purpose=purpose, timestamp=now(), config=asdict(self.config),
                      request=request, reserved_usd=bound, attempts=[])
        path = self.log_dir / (ident + '.json')
        write_json(path, record)
        start = time.monotonic()
        try:
            response = self.client.chat.completions.create(**request)
            raw = response.model_dump(mode='json')
        except Exception as exc:
            self.ledger.settle(ident, None, type(exc).__name__)
            record['attempts'].append(dict(error=type(exc).__name__, http_status=getattr(exc, 'status_code', None),
                error_message=str(exc).replace(self.client.api_key, '[REDACTED]')[:1000], seconds=time.monotonic()-start))
            write_json(path, record)
            raise RuntimeError(f'{self.config.model_id}: transport failure; call {ident}') from None
        usage = raw.get('usage') or {}
        charges = [x for x in (usage.get('cost'), (usage.get('cost_details') or {}).get('upstream_inference_cost'))
                   if isinstance(x, (int, float))]
        cost = 0.0 if self.config.provider == 'flt' else max(charges) if charges else None
        self.ledger.settle(ident, cost)
        record['attempts'].append(dict(response=raw, seconds=time.monotonic()-start))
        record['reported_cost_usd'] = cost
        write_json(path, record)
        choice = response.choices[0]
        reply = choice.message.content or ''
        status = 'ok' if choice.finish_reason == 'stop' and reply.strip() and not getattr(choice.message, 'refusal', None) else 'invalid_response'
        return reply, dict(call_id=ident, actual_model=response.model, status=status,
            finish_reason=choice.finish_reason, usage=usage, timestamp=record['timestamp'])

    def generate(self, messages, max_tokens=8192, purpose='play'):
        error = None
        for limit in (max_tokens, 16384):
            try:
                with self.limits[self.config.model_id]:
                    reply, meta = self.once(messages, limit, purpose)
                if meta['status'] == 'ok':
                    return reply, meta
                error = RuntimeError(f'{self.config.model_id}: invalid_response; call {meta["call_id"]}')
            except (BudgetExceeded, ValueError):
                raise
            except Exception as exc:
                error = exc
            if limit == max_tokens:
                time.sleep(1)
        raise error
