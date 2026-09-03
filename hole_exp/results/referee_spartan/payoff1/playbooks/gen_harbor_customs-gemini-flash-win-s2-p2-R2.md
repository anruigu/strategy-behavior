---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1174
---
# Harbor Customs Playbook

## Declare Stage
- Identify the exact value of the heaviest crate in my private hold ($H$).
- Set my declared value strictly equal to $H$ (`[declare: H]`). 
- Never declare below $H$, as failing the spot check triggers a -40 penalty and recalculates duty at full hold value.
- Never declare above $H$; extra declared value provides zero additional protection and only increases the duty paid.

## Route Stage
- Identify the value of the smallest crate in my hold ($S$) and the duty difference between routes given declared value $H$:
  - Main route cost: $\lfloor 0.30 \times H \rfloor$.
  - Night route cost: $S + \lfloor 0.15 \times H \rfloor$.
- Compare the two options:
  - Duty savings from night route = $\lfloor 0.30 \times H \rfloor - \lfloor 0.15 \times H \rfloor$ (at most 6 points for $H \le 40$).
  - Since crate values are at least 5 points, $S$ will almost always exceed or equal the duty saved.
  - If $S > \lfloor 0.30 \times H \rfloor - \lfloor 0.15 \times H \rfloor$, choose `[route: main]`.
  - If $S < \lfloor 0.30 \times H \rfloor - \lfloor 0.15 \times H \rfloor$, choose `[route: night]`.
  - If tied, choose `[route: main]`.