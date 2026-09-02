---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1500
---
# Harbor Customs Playbook

### Stage 1: Declaration Strategy
- Identify the maximum crate value in my hold: $M = \max(c_1, c_2, c_3)$.
- Always declare exactly $M$: `[declare: M]`.
- Never declare less than $M$ (e.g. attempting to blend in or guessing low). Declaring below $M$ guarantees a spot-check failure, triggering a -40 penalty and recomputed full-hold duty.
- Never declare more than $M$ (e.g. declaring 45, 54, or matching the table's higher numbers). Over-declaring offers zero protection against the spot check and only increases the duty paid.

### Stage 2: Route Strategy
- Compare the cost difference between `main` and `night` routes given declaration $D = M$ and smallest crate value $S = \min(c_1, c_2, c_3)$:
  - Main net gain: $(\sum c_i) - \lfloor 0.30 \times M \rfloor$
  - Night net gain: $(\sum c_i) - S - \lfloor 0.15 \times M \rfloor$
  - The duty savings of night over main is $\lfloor 0.30 \times M \rfloor - \lfloor 0.15 \times M \rfloor \approx 0.15 \times M$.
- Since $M \le 40$, the maximum duty saved by night is at most 6 points ($\lfloor 12 \rfloor - \lfloor 6 \rfloor = 6$), while losing the smallest crate costs at least 5 points ($S \ge 5$).
- When $S > \lfloor 0.30 \times M \rfloor - \lfloor 0.15 \times M \rfloor$, always choose `[route: main]`.
- Only choose `[route: night]` if $S$ is strictly smaller than the duty saved ($\approx 0.15 \times M$, which only happens if $S = 5$ and $M \ge 34$, saving at most 1 point). Otherwise, default to `[route: main]`.