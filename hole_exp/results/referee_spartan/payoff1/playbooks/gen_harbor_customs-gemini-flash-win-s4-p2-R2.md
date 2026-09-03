---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 1360
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
    - Night is strictly better than Main if and only if:
      $$c_1 < \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$$
    - Since max crate value is 40, max possible duty difference is $\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$.
    - Because min crate value is 5, night route is only viable if $c_1 = 5$ and $c_3 \ge 34$ (where $\lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor = 6 > 5$).
    - If $c_1 < \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$, choose `[route: night]`.
    - Otherwise (in virtually all cases where $c_1 \ge \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$), choose `[route: main]`.