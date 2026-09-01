#!/usr/bin/env python
"""`summarize_referee.py` with the 8 generated cells registered.

    python summarize_gen.py ../results/gen_crossplay/qwen_gen1
    python summarize_gen.py ../results/gen_crossplay/qwen_gen1 --by cross

Same wrapper bargain as `run_gen_crossplay.py`: the tables, the pooling rules
and the validity gate are the shipped ones, so a generated-cell wave and an
atlas wave are read the same way. Only the roster differs.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import run_gen_crossplay as W       # noqa: E402
import summarize_referee as S       # noqa: E402

if __name__ == "__main__":
    W.register()
    raise SystemExit(S.main())
