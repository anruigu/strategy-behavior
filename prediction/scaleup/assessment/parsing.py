"""Extract a single unambiguous forecast object without changing its numbers."""
import json
from .forecast import parse


def extract(raw, ids):
    try:
        return parse(raw.strip(), ids)
    except (ValueError, TypeError, KeyError):
        pass
    decoder = json.JSONDecoder()
    candidates = []
    for start, char in enumerate(raw):
        if char != "{":
            continue
        try:
            _, end = decoder.raw_decode(raw[start:])
            value = parse(raw[start:start+end], ids)
        except (ValueError, TypeError, KeyError):
            continue
        candidates.append(value)
    if len(candidates) != 1:
        raise ValueError("Expected exactly one schema-valid forecast object")
    return candidates[0]
