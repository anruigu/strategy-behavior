"""Independent LLM seats with exact request logs and no scripted fallback."""
from collections import defaultdict
import json
import re
import time

from hosted_opponents import HostedConfig, HostedOpponent
from v5_protocol import parse_action, VERSION

SYSTEM = ('You are a player in a strategy game. Your goal is to maximize your score. '
          'Follow the game rules and make whatever decisions you think will help you win. '
          'In a cooperative game maximize the shared team score. '
          'Other players choose their own actions. Use your private observation and the '
          'provided Actions forms. Reply with one action, using its token templates.')


class V5Opponent(HostedOpponent):
    def __init__(self, config=None, client=None, checkpoint=None):
        super().__init__(config, client)
        self.checkpoint = checkpoint
        if hasattr(self.client, 'attempts'): self.client.attempts = 1

    def fresh(self): return type(self)(self.config)

    def _record(self, record):
        super()._record(record)
        if self.checkpoint: self.checkpoint(record)

    def __call__(self, pid, phase, prompt):
        forms = json.loads(re.search(r'^Actions: (.+)$', prompt, re.M)[1])
        message = dict(role='user', content=prompt)
        for correction in range(2):
            messages = [dict(role='system', content=SYSTEM), *self.memory[pid], message]
            settings = dict(reasoning={'effort': 'low'})
            started = time.time()
            record = dict(pid=pid, phase=phase, messages=messages, started_at=started,
                          model=self.config.model, max_tokens=4096, settings=settings, correction=correction)
            try:
                response = self.client.chat.completions.create(model=self.config.model,
                    messages=messages, max_tokens=4096, **settings)
                choice = response.choices[0]
                reply = (choice.message.content or '').strip()
                record.update(reply=reply, model=response.model, finish_reason=choice.finish_reason,
                              usage=response.usage.model_dump() if response.usage else None)
                if not reply or choice.finish_reason != 'stop': raise RuntimeError('Incomplete model response')
                self.memory[pid].extend([message, dict(role='assistant', content=reply)])
                try: parse_action(reply, forms)
                except ValueError as exc:
                    record['format_error'] = str(exc)
                    if correction: raise RuntimeError('Invalid model action after format correction')
                    message = dict(role='user', content='No action has occurred. ' + str(exc) + '.\nActions: ' + json.dumps(forms))
                    continue
                return reply
            except Exception as exc:
                record['error'] = type(exc).__name__
                raise RuntimeError('AI player could not complete its turn') from exc
            finally:
                record['finished_at'] = time.time()
                self._record(record)

    def metadata(self):
        with self._records_lock:
            return dict(model=self.config.model, base_url=self.config.base_url, system=SYSTEM,
                        protocol=VERSION, decisions=list(self.records))
