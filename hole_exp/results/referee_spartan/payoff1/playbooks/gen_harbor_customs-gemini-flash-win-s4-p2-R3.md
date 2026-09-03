---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1198
---
- **Declaration Rule:**
  - Let the crate values in the hold be sorted as $c_1 \le c_2 \le c_3$, where $c_3$ is the heaviest crate and $c_1$ is the lightest.
  - Always declare exactly the value of the heaviest crate: `[declare: c3]`.
  - Never declare above $c_3$, as higher declarations pay unnecessary duty on value that isn't inspected.
  - Never declare below $c_3$, as the spot check always verifies against the heaviest crate, triggering a -40 penalty plus 30% duty on the full hold.

- **Route Selection Rule:**
  - Compare the net returns after declaring $c_3$:
    - **main**: $(c_1 + c_2 + c_3) - \lfloor 0.30 \times c_3 \rfloor$
    - **night**: $(c_2 + c_3) - \lfloor 0.15 \times c_3 \rfloor$
  - Difference: Night yields higher points if and only if:
    $$c_1 < \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$$
  - The maximum duty saving across the legal range (max $c_3 = 40$) is $12 - 6 = 6$.
  - Night is only optimal when $c_1 = 5$ and $c_3 \ge 34$ (where the duty savings equal 6, exceeding the lost crate of 5).
  - If $c_1 < \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$, choose `[route: night]`.
  - Otherwise, choose `[route: main]`.