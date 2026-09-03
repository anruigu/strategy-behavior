---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1025
---
# Harbor Customs Playbook

## Declare Stage
- Identify the exact value of the heaviest crate in my private hold ($H$).
- Set my declared value strictly equal to $H$ (`[declare: H]`). 
- Never declare below $H$, as failing the spot check triggers a -40 penalty and recalculates duty at full hold value.
- Never declare above $H$; extra declared value provides zero additional protection and only increases the duty paid.

## Route Stage
- Identify the value of the smallest crate in my hold ($S$) and the duty difference between routes:
  - Main route net cost: $\lfloor 0.30 \times H \rfloor$.
  - Night route net cost: $S + \lfloor 0.15 \times H \rfloor$.
- Compare the two options:
  - If $S > \lfloor 0.30 \times H \rfloor - \lfloor 0.15 \times H \rfloor$, choose `[route: main]` to avoid losing a crate worth more than the duty saved.
  - If $S < \lfloor 0.30 \times H \rfloor - \lfloor 0.15 \times H \rfloor$, choose `[route: night]` because the duty savings outweigh the lost crate.
  - If tied, choose `[route: main]`.