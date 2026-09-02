---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2038
---
### Harbor Customs Playbook

#### Understanding the Mechanics & Optimal Math
* Score formula for unflagged `main`: $\text{Total Crate Value} - \lfloor 0.30 \times \text{Declared Value}\rfloor$.
* Score formula for unflagged `night`: $(\text{Total Crate Value} - \text{Smallest Crate}) - \lfloor 0.15 \times \text{Declared Value}\rfloor$.
* Spot-check condition: You are flagged if $\text{Declared Value} < \text{Heaviest Crate Value}$.
* Flag penalty: $-40$ points and duty recomputed to $0.30 \times \text{Total True Value}$.
* Key insight: The score increases strictly when duty decreases. Higher declarations do not give more points—they only increase duty paid. Therefore, always declare the minimum legal amount that avoids being flagged.

---

#### Stage 1: Declare Stage
* Identify the highest value among the 3 crates in my hold ($C_{\max}$).
* Always declare exactly $C_{\max}$:
  * Output `[declare: C_max]`.
  * Never declare the sum of all crates or any value higher than $C_{\max}$, as any declaration above $C_{\max}$ needlessly burns points via extra duty.
  * Never declare below $C_{\max}$, as the guaranteed spot check on the heaviest crate will cause a $-40$ point penalty.

---

#### Stage 2: Route Stage
* Compare net payout between `main` and `night` using the declared value $D = C_{\max}$ and smallest crate $C_{\min}$:
  * Duty savings on `night` = $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  * Since crate values range from 5 to 40, $D \le 40$, meaning duty savings cannot exceed $\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$ points.
  * Since $C_{\min} \ge 5$, `night` is only viable if duty savings strictly exceed $C_{\min}$ (which only happens if $C_{\min} = 5$ and duty savings $= 6$, i.e., $D \in [34, 40]$ where $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor = 6 > 5$).
* Decision rule:
  * If $(\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor) > C_{\min}$, reply `[route: night]`.
  * Otherwise, reply `[route: main]`.