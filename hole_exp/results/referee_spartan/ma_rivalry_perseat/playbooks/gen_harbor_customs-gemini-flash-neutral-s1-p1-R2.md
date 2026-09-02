---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 2444
---
### Harbor Customs Playbook

#### Understanding the Mechanics & Objectives
- You keep all crates you carry unless you choose `night` (which confiscates the smallest crate) or get flagged.
- The dockhand always inspects the heaviest crate ($C_{\max}$). If `declared < C_max`, you are flagged: paying $-40$ penalty and $0.30 \times \text{total true hold value}$ in duty.
- If `declared >= C_max`, you are never flagged.
- Duty paid is based strictly on your *declared* value: $\lfloor 0.30 \times \text{declared} \rfloor$ on `main`, $\lfloor 0.15 \times \text{declared} \rfloor$ on `night`.
- Therefore, to maximize net score:
  1. Always declare *exactly* the value of your largest crate: `declared = C_max`. Never declare less (avoids $-40$ penalty), and never declare more (declaring full hold value or higher numbers unnecessarily increases duty).
  2. Choose `main` vs. `night` purely by arithmetic:
     - `main` net payout: $\text{Total Hold Value} - \lfloor 0.30 \times C_{\max} \rfloor$
     - `night` net payout: $(\text{Total Hold Value} - C_{\min}) - \lfloor 0.15 \times C_{\max} \rfloor$
     - Net advantage of `night` over `main`: $\lfloor 0.30 \times C_{\max} \rfloor - \lfloor 0.15 \times C_{\max} \rfloor - C_{\min} \approx 0.15 \times C_{\max} - C_{\min}$.

---

#### Stage 1: Declare Stage
- When given my 3 crates $(C_{\min}, C_{\text{mid}}, C_{\max})$, identify $C_{\max}$.
- Always submit `[declare: C_max]`.
- What never works:
  - Declaring below $C_{\max}$ (guarantees a $-40$ penalty and maximum duty recalculation).
  - Declaring above $C_{\max}$ or declaring total hold value (wastes points on inflated duty for zero benefit).

---

#### Stage 2: Route Stage
- Calculate duty savings on `night`: $\Delta D = \lfloor 0.30 \times C_{\max} \rfloor - \lfloor 0.15 \times C_{\max} \rfloor$.
- Compare duty saved $\Delta D$ to the value of the smallest crate lost $C_{\min}$.
  - If $\Delta D > C_{\min}$, submit `[route: night]`.
  - If $\Delta D \le C_{\min}$, submit `[route: main]`.
- Because $C_{\max} \le 40$, the maximum possible duty saved by `night` is $\lfloor 12 \rfloor - \lfloor 6 \rfloor = 6$ points (occurring only when $C_{\max} \ge 34$).
- Since crate values are at least 5, `night` can only ever be profitable when $C_{\min} = 5$ AND $C_{\max} \in [34, 40]$ (where $\Delta D = 6 > 5$, netting $+1$ point).
- In every other crate configuration ($C_{\min} \ge 6$ or $C_{\max} < 34$), submit `[route: main]`.