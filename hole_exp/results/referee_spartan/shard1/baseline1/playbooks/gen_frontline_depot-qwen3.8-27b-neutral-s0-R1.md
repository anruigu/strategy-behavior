---
game: gen_frontline_depot
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 311
---
# Playbook for gen_frontline_depot

**Core rule: always play 10 for strike and 10 for guard, every round, no exceptions.**

The scoring is max(0, my_strike − their_guard) + max(0, my_guard − their_strike). Raising my strike can only increase or hold constant my score; raising my guard can only increase or hold