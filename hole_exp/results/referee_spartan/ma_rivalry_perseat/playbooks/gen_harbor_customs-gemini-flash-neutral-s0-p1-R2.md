---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1246
---
# Harbor Customs Playbook

### Stage 1: Declaration Strategy
- Identify the maximum crate value in my hold: $M = \max(c_1, c_2, c_3)$.
- Always declare exactly $M$: `[declare: M]`.
- Never declare less than $M$. Declaring below $M$ guarantees a spot-check failure on every player every round, triggering a -40 penalty and recomputed full-hold duty.
- Never declare more than $M$. Over-declaring offers zero additional protection against the spot check and strictly increases the duty paid.

### Stage 2: Route Strategy
- Compare the net outcome between `main` and `night` routes given declared value $D = M$ and smallest crate value $S = \min(c_1, c_2, c_3)$:
  - Main duty: $\lfloor 0.30 \times M \rfloor$. No crates lost.
  - Night duty: $\lfloor 0.15 \times M \rfloor$. Smallest crate $S$ is confiscated.
  - Duty saved on night: $\Delta = \lfloor 0.30 \times M \rfloor - \lfloor 0.15 \times M \rfloor$.
- Calculate $\Delta$ vs $S$:
  - Since crate values are 5–40, $\Delta \le 6$ (reached only when $M \ge 34$).
  - If $S > \Delta$, choose `[route: main]`.
  - If $S < \Delta$ (specifically, $S = 5$ and $M \in [34, 40]$ where $\Delta = 6$), choose `[route: night]` for a net gain of +1 point.
  - If $S = \Delta$, default to `[route: main]`.