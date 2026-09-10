"""Immediate, append-only participant feedback, separate from game actions."""
import json
import os
from pathlib import Path
import threading
import time
import uuid

_LOCK = threading.Lock()


def save_feedback(directory, text, **context):
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Please enter your feedback.')
    if len(text) > 10000:
        raise ValueError('Please keep each submission under 10,000 characters.')
    record = dict(context, schema=1, feedback_id=uuid.uuid4().hex,
                  submitted_at=time.time(), text=text.strip())
    path = Path(directory) / 'feedback.jsonl'
    path.parent.mkdir(parents=True, exist_ok=True)
    with _LOCK, path.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + '\n')
        fh.flush()
        os.fsync(fh.fileno())
    return record['feedback_id']
