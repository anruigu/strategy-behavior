"""Exact campaign prompts and request settings for human focal-agent play."""
import json
import re
import time

from engines_v3_ma import parse
from engines_v4 import PROTOCOL
from hosted_opponents import HostedConfig, HostedOpponent

LABELS = {'qwen-3.8-27b': 'Qwen 3.8 27B', 'glm': 'GLM 5.3',
          'claude-haiku-4.5': 'Claude Haiku 4.5', 'gpt-5-mini': 'GPT-5 mini'}


class EvalOpponent(HostedOpponent):
    def __init__(self, game_id, condition='nerfed', model='qwen-3.8-27b', client=None):
        if game_id not in PROTOCOL['systems'] or condition not in ('ordinary', 'nerfed', 'defensive'):
            raise ValueError('Unknown V4 scenario or opponent condition')
        if model not in PROTOCOL['models']:
            raise ValueError('Choose an opponent from the eval model list')
        cfg = PROTOCOL['models'][model]
        self.game_id, self.condition, self.model_key = game_id, condition, model
        self.systems = PROTOCOL['systems'][game_id][condition]
        super().__init__(HostedConfig(cfg['provider_model'], cfg['base_url'], cfg['key_env']), client)
        # Two attempts total per submission, including transport failures.
        if hasattr(self.client, 'attempts'):
            self.client.attempts = 1
            self.client.timeout = 180

    def fresh(self):
        return type(self)(self.game_id, self.condition, self.model_key)

    def __call__(self, pid, phase, prompt):
        forms = json.loads(re.search(r'^Actions: (.+)$', prompt, re.M)[1])
        message = dict(role='user', content=prompt)
        for correction in range(PROTOCOL['format_corrections'] + 1):
            messages = [dict(role='system', content=self.systems[str(pid)]), *self.memory[pid], message]
            reply = self.generate(pid, phase, prompt, messages, correction)
            self.memory[pid].extend([message, dict(role='assistant', content=reply)])
            error = None
            try:
                parse(reply, forms)
            except ValueError as exc:
                error = str(exc)
            self._record(dict(pid=pid, phase=phase, prompt=prompt, reply=reply,
                              format_error=error, correction_attempt=correction, kind='submission'))
            if not error:
                return reply
            if correction == PROTOCOL['format_corrections']:
                raise RuntimeError('AI opponent submitted an invalid action after correction')
            message = dict(role='user', content='Your submission was not accepted: ' + error +
                '. No game action has occurred. Submit only the fields in Actions for the current stage, '
                'using listed values. Do not include moves for later stages.\nActions: ' + json.dumps(forms))

    def generate(self, pid, phase, prompt, messages, correction):
        settings = {'reasoning': {'effort': 'low'}}
        if 'openrouter.ai' in self.config.base_url:
            settings['provider'] = {'max_price': {'prompt': 20, 'completion': 120, 'request': 0}}
        for attempt, limit in enumerate(PROTOCOL['output_allowances']):
            started = time.time()
            record = dict(kind='call', pid=pid, phase=phase, prompt=prompt, messages=messages,
                requested_model=self.config.model, max_tokens=limit, settings=settings,
                correction_attempt=correction, attempt=attempt, started_at=started)
            try:
                response = self.client.chat.completions.create(model=self.config.model,
                    messages=messages, max_tokens=limit, **settings)
                choice = response.choices[0]
                reply = choice.message.content or ''
                record.update(model=response.model, reply=reply, finish_reason=choice.finish_reason,
                              usage=response.usage.model_dump() if response.usage else None)
                if choice.finish_reason != 'stop' or not reply.strip() or getattr(choice.message, 'refusal', None):
                    raise ValueError('Incomplete response')
            except Exception as exc:
                record.update(error=type(exc).__name__, finished_at=time.time())
                self._record(record)
                if attempt + 1 == len(PROTOCOL['output_allowances']):
                    raise RuntimeError('AI opponent could not complete its turn') from None
                time.sleep(1)
                continue
            record['finished_at'] = time.time()
            self._record(record)
            return reply

    def metadata(self):
        with self._records_lock:
            return dict(model=self.config.model, model_key=self.model_key, base_url=self.config.base_url,
                scenario=self.game_id, condition=self.condition, systems=self.systems,
                protocol=PROTOCOL['protocol'], source_run=PROTOCOL['source_run'],
                decisions=list(self.records))
