---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1008
---
- When the **declare stage** is put to me:
  - Identify the maximum value among the 3 crates in my hold (`max_crate`).
  - Declare exactly `max_crate` (`[declare: max_crate]`).
  - Never declare more than `max_crate` (which pays unnecessary duty) and never declare less than `max_crate` (which fails the harbormaster spot check, incurring a -40 penalty plus 0.30 duty on the full true hold value).

- When the **route stage** is put to me:
  - Let $D$ be my declared value (`max_crate`), and let $S$ be the value of my smallest crate.
  - Calculate the duty saved by taking the night route: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Compare the value of the smallest crate lost ($S$) to the duty saved ($\Delta \text{duty}$):
    - If $S > \Delta \text{duty}$, reply `[route: main]` (protecting the crate is worth more than the duty savings).
    - If $S \le \Delta \text{duty}$, reply `[route: night]` (the duty saved equals or exceeds the confiscated crate).