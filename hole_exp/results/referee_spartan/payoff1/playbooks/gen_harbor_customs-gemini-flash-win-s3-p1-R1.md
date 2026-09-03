---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 960
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Let $c_1 \le c_2 \le c_3$ be the crate values in ascending order.
  - Always declare exactly $c_3$, the value of the heaviest crate (`[declare: c3]`).
  - Never declare above $c_3$ (which unnecessarily increases duty without reducing risk) and never declare below $c_3$ (which guarantees a 40-point penalty plus full duty recalculation).

- **Route Stage:**
  - When deciding route after declaring $c_3$:
    - Compare net payout of **main** vs **night**:
      - Main net value: $(c_1 + c_2 + c_3) - \lfloor 0.30 \times c_3 \rfloor$
      - Night net value: $(c_2 + c_3) - \lfloor 0.15 \times c_3 \rfloor$
      - Gain from choosing night over main: $\lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor - c_1 \approx 0.15 \times c_3 - c_1$
    - When $c_1 < \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$, choose `[route: night]`.
    - Otherwise, choose `[route: main]`.