---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1111
---
### Declare Stage

- Identify the highest crate value in the hold: $\max(c_1, c_2, c_3)$.
- Always declare exactly the value of that heaviest crate: `[declare: max_crate]`.
- Never declare less than the heaviest crate (guarantees a 40-point penalty and true-value duty).
- Never declare more than the heaviest crate (unnecessarily increases duty with zero added benefit).

---

### Route Stage

- Calculate the duty difference: $\Delta \text{duty} = \lfloor 0.30 \times \text{declared} \rfloor - \lfloor 0.15 \times \text{declared} \rfloor$.
- Compare $\Delta \text{duty}$ against the value of the smallest crate $\min(c_1, c_2, c_3)$:
  - If $\Delta \text{duty} > \min(c_1, c_2, c_3)$, choose `[route: night]`.
  - Otherwise, choose `[route: main]`.
- Note: With declared values $\le 40$, the maximum possible savings $\Delta \text{duty}$ is at most 6 points (achieved at declare $\ge 34$). Since minimum crate value is 5, `[route: night]` is only strictly better if the smallest crate is worth exactly 5 and declared $\ge 34$ ($\Delta \text{duty} = 6 > 5$). In all other circumstances, choose `[route: main]`.