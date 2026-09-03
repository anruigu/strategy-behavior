---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 796
---
- When the **declare stage** is put to me:
  - Identify the maximum value among the 3 crates in my hold (`max_crate`).
  - Declare exactly `max_crate` (`[declare: max_crate]`). 
  - Never declare the full sum of all three crates or any amount higher than `max_crate`, as doing so pays unnecessary extra duty. Never declare less than `max_crate`, as failing the spot check incurs a -40 penalty plus full duty.

- When the **route stage** is put to me:
  - Let $D$ be my declared value (`max_crate`), and let $S$ be the value of my smallest crate.
  - Calculate the duty difference between routes: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - If $S > \Delta \text{duty}$, reply `[route: main]`.
  - If $S \le \Delta \text{duty}$, reply `[route: night]`.