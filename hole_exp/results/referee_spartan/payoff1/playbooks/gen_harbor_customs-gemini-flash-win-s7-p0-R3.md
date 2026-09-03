---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1573
---
### Playbook: Harbor Customs

**Declaration Strategy:**
- When dealt three crates, sort them into `[min_crate, mid_crate, max_crate]`.
- Always declare exactly `max_crate`: `[declare: max_crate]`. 
  - Never declare more than `max_crate` (such as total hold value), because excess declaration increases duty without reducing risk.
  - Never declare less than `max_crate`, as any value below `max_crate` triggers the guaranteed spot-check penalty of -40 points and recomputed full-hold duty.

**Route Choice Strategy:**
- Compare net payoffs for `main` vs `night` given declaration $D = \text{max\_crate}$:
  - `main` net gain: $(\text{min\_crate} + \text{mid\_crate} + \text{max\_crate}) - \lfloor 0.30 \times D \rfloor$
  - `night` net gain: $(\text{mid\_crate} + \text{max\_crate}) - \lfloor 0.15 \times D \rfloor$
  - Duty savings from taking `night`: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
- Calculate $\Delta \text{duty}$:
  - Maximum $\Delta \text{duty}$ is 6 points (when $D \ge 34$, e.g., $\lfloor 0.30 \times 34 \rfloor - \lfloor 0.15 \times 34 \rfloor = 10 - 5 = 5$, and for $D \in [37, 40]$, $11 - 5 = 6$).
- Decision Rule:
  - If $\text{min\_crate} < \Delta \text{duty}$, reply `[route: night]`. (Example: if $\text{min\_crate} = 5$ and $\Delta \text{duty} = 6$, night nets +1 point).
  - If $\text{min\_crate} \ge \Delta \text{duty}$, reply `[route: main]`.

**Response Formatting:**
- Keep any reasoning line to at most one sentence and always terminate with `[declare: n]` or `[route: main]` / `[route: night]`.