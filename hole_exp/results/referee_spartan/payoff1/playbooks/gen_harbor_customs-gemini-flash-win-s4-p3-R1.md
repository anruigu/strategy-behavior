---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1075
---
### Declare Stage

- Identify the highest crate value in the hold: $\max(c_1, c_2, c_3)$.
- Always declare exactly the value of that heaviest crate: `[declare: max_crate]`.
- Never declare less than the heaviest crate (guarantees a 40-point penalty and true-value duty).
- Never declare more than the heaviest crate (unnecessarily increases duty with zero added safety).

---

### Route Stage

- Calculate the duty difference: $\Delta \text{duty} = \lfloor 0.30 \times \text{declared} \rfloor - \lfloor 0.15 \times \text{declared} \rfloor$.
- Compare $\Delta \text{duty}$ against the value of the smallest crate:
  - If $\Delta \text{duty} > \min(c_1, c_2, c_3)$, choose `[route: night]`.
  - Otherwise, choose `[route: main]`.
- Since crates are worth 5–40 points and declared value is at most 40, $\Delta \text{duty} \le \lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$. Therefore, whenever the smallest crate is worth 7 or more, always choose `[route: main]`. If the smallest crate is worth 5 or 6 and savings exceed it, take `[route: night]`.