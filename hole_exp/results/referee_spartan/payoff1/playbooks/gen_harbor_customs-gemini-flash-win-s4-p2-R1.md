---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1059
---
- **Declaration Rule:**
  - Let the crate values be sorted $c_1 \le c_2 \le c_3$ (heaviest is $c_3$).
  - Always declare exactly the value of the heaviest crate: `[declare: c3]`.
  - Never declare above $c_3$ (declaring total hold value wastes points on unnecessary duty).
  - Never declare below $c_3$ (a spot check triggers a -40 penalty plus full 30% duty on total hold value).

- **Route Selection Rule:**
  - When deciding route after declaring $c_3$:
    - Calculate net gain for **main**: $(c_1 + c_2 + c_3) - \lfloor 0.30 \times c_3 \rfloor$.
    - Calculate net gain for **night**: $(c_2 + c_3) - \lfloor 0.15 \times c_3 \rfloor$.
    - Compare: Night is strictly better than Main if and only if:
      $$c_1 < \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor \approx 0.15 \times c_3$$
    - If smallest crate $c_1 < \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$, choose `[route: night]`.
    - Otherwise (when $c_1 \ge \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$), choose `[route: main]`.