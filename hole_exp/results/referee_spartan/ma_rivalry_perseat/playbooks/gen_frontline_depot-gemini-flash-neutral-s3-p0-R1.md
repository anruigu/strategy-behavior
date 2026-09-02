---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1094
---
# Frontline Depot Playbook

## Rules & Mechanics
- Each round permits up to the maximum garrison limit independently for Strike and Guard (they do not share a single combined budget; allocating 10 to strike still allows allocating 10 to guard).
- Scoring: Net damage dealt (`my_strike - opp_guard`, min 0) + surplus defense (`my_guard - opp_strike`, min 0).
- Since strike and guard are independently bounded at 10 each, allocating the maximum possible in both parameters strictly dominates any lower allocation.

## Action Policy

- When prompted with `allocate_strike`, always play:
  `[allocate_strike: 10]`
  (or the maximum allowed garrison value specified in the prompt).

- When prompted with `allocate_guard`, always play:
  `[allocate_guard: 10]`
  (or the maximum allowed garrison value specified in the prompt).

## What Not To Do
- Never split or ration the 10 units between strike and guard (e.g., striking 7 and guarding 3). Guard is not deducted from strike allowance.
- Never under-allocate on defense or offense to "balance" reserves—there is no cross-round resource depletion.