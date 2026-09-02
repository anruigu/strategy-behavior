---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1620
---
# Frontline Depot Playbook

## Rules & Mechanics
- Each round permits up to the maximum garrison limit independently for Strike and Guard (they do not share a single combined budget; allocating the maximum to strike still allows allocating the maximum to guard).
- Scoring: Net damage dealt (`my_strike - opp_guard`, min 0) + surplus defense (`my_guard - opp_strike`, min 0).
- Since strike and guard are independently bounded at the round limit, allocating the maximum possible in both parameters strictly dominates any lower allocation regardless of opponent action:
  - Strike = max ensures you maximize damage if the opponent under-guards.
  - Guard = max ensures you prevent all damage and maximize surplus defense if the opponent under-strikes.
  - When both players allocate maximum strike (10) and guard (10), round scores result in 0 net damage and 0 surplus guard, which is the unique Nash equilibrium.

## Action Policy
- When prompted with `allocate_strike`, always play the maximum allowed garrison value specified in the prompt:
  `[allocate_strike: 10]`
- When prompted with `allocate_guard`, always play the maximum allowed garrison value specified in the prompt:
  `[allocate_guard: 10]`

## What Not To Do
- Never split or ration units between strike and guard (e.g., striking 7 and guarding 3). Guard is not deducted from strike allowance.
- Never under-allocate on defense or offense to "balance" reserves—there is no cross-round resource depletion.
- Never deviate from max guard or max strike in an attempt to exploit the opponent; doing so only creates an opening for the opponent to score on you.