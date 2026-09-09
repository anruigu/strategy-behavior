"""Seat- and model-budget-balanced self/cross-play factorial design."""
from dataclasses import asdict,replace
from itertools import permutations,product
from collections import Counter
from benchmark.clients import MODELS,ModelConfig,OPENROUTER
from benchmark.v3.live_pilot import EXPLORATION_SYSTEM

VERSION='fullscale-design-20260908.1'
SMALL=('claude-haiku-4.5','gpt-5-mini','gemini-3.7-flash')
FRONTIER=('claude-opus-5','gpt-5.6-sol')
CLAUDE=('claude-haiku-4.5','claude-opus-5')
GPT=('gpt-5-mini','gpt-5.6-sol')
ANCHOR='gemini-3.7-flash'
FOURTH_FAMILY='qwen-3.8-27b'
MODELS_ORDER=SMALL+FRONTIER+(FOURTH_FAMILY,)
REGISTRY={m:replace(MODELS[m],temperature=None,reasoning_effort='high') for m in SMALL+(FOURTH_FAMILY,)}
REGISTRY.update({m:ModelConfig(m,'openrouter',provider,OPENROUTER,'OPENROUTER_API_KEY',temperature=None,reasoning_effort='high')
                 for m,provider in [('claude-opus-5','anthropic/claude-opus-5'),('gpt-5.6-sol','openai/gpt-5.6-sol')]})
MAX_TOKENS=16384
PRIMARY_PROMPT=EXPLORATION_SYSTEM
# This is an execution diagnostic only, never part of the discovery condition.
HINT_HEADER=('Execution diagnostic: the following mechanism is being revealed to you. '
             'Use the normal game action interface to test and execute it for advantage. '
             'Your response is not evidence of independent discovery. Mechanism: ')


def family(m):
    if m in CLAUDE:return 'claude'
    if m in GPT:return 'gpt'
    if m==ANCHOR:return 'gemini'
    if m==FOURTH_FAMILY:return 'qwen'
    raise KeyError(m)


def rotations(row):
    return [tuple(row[i:]+row[:i]) for i in range(len(row))]


def lineups(n):
    if n==4:
        cross=[p for c,g in product(CLAUDE,GPT) for p in rotations((c,g,ANCHOR,FOURTH_FAMILY))]
    elif n==3:
        cross=[p for c,g in product(CLAUDE,GPT) for p in rotations((c,g,ANCHOR))]
    elif n==2:
        pairs=[*product(CLAUDE,GPT),*((m,ANCHOR) for m in CLAUDE+GPT)]
        cross=[p for pair in pairs for p in permutations(pair)]
    else: raise ValueError('Only two-, three-, and four-player games are supported')
    appearances=Counter(m for row in cross for m in row)
    self_play=[]
    for m in MODELS_ORDER:
        assert appearances[m]%n==0
        self_play.extend([(m,)*n]*(appearances[m]//n))
    assert Counter(m for row in cross for m in row)==Counter(m for row in self_play for m in row)
    assert all(len({family(m) for m in row})==n for row in cross)
    return dict(cross=cross,self=self_play)


def schedule(editions,seeds):
    result=[]
    for game,n in editions.items():
        for seed_index,seed in enumerate(seeds):
            for mode,rows in lineups(n).items():
                for replicate,seats in enumerate(rows):
                    # Alternate clockwise/counterclockwise family order across seed blocks.
                    if mode=='cross' and seed_index%2: seats=tuple(reversed(seats))
                    result.append(dict(id=f'{game}__{mode}__s{seed}__r{replicate}',game=game,seed=seed,mode=mode,
                                       replicate=replicate,seats=list(seats),families=[family(m) for m in seats]))
    return result


def describe(editions,seeds):
    tasks=schedule(editions,seeds)
    calls=Counter()
    for row in tasks:
        for m in row['seats']:calls[m]+=8
    return dict(version=VERSION,rotation_scheme='cyclic seats; reverse orientation on alternating seed blocks',models={m:asdict(c) for m,c in REGISTRY.items()},max_completion_tokens=MAX_TOKENS,
                prompt=PRIMARY_PROMPT,seeds=list(seeds),editions=editions,matches=len(tasks),
                matches_by_mode=dict(Counter(r['mode'] for r in tasks)),maximum_play_calls_by_model=dict(calls),
                maximum_play_calls=sum(calls.values()),tasks=tasks)
