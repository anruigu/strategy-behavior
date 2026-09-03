---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1645
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
  - Duty savings from taking `night`: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor \approx 0.15 \times D$.
- Since $D \le 40$, duty savings $\Delta \text{duty}$ is at most $\lfloor 12.0 \rfloor - \lfloor 6.0 \rfloor = 6$ points (e.g., $11 - 5 = 6$ for $D = 37..40$).
- Rule:
  - If $\text{min\_crate} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, reply `[route: night]`. (This only happens when $\text{min\_crate} \le 5$ and $D \ge 34$, or $\text{min\_crate} = 6$ and $D \ge 40$, etc., where duty savings exceed the crate value lost).
  - Otherwise (whenever $\text{min\_crate} \ge \Delta \text{duty}$), reply `[route: main]`.

**Response Formatting:**
- Keep any reasoning line very brief and always terminate with `[declare: n]` or `[route: main]` / `[route: night]`.