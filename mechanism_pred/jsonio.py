"""Pull one JSON object out of a model reply that may be wrapped in prose."""
from __future__ import annotations

import json
import re
from typing import Any, Optional

_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def extract(text: str) -> Optional[Any]:
    if not text:
        return None
    for cand in _FENCE.findall(text):
        try:
            return json.loads(cand)
        except Exception:  # noqa: BLE001
            pass
    # Brace matching from the first '{': tolerant of trailing commentary, which
    # is what reasoning models actually emit when they ignore "JSON only".
    start = text.find("{")
    while start != -1:
        depth, in_str, esc = 0, False, False
        for i in range(start, len(text)):
            c = text[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
                continue
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except Exception:  # noqa: BLE001
                        break
        start = text.find("{", start + 1)
    return None
