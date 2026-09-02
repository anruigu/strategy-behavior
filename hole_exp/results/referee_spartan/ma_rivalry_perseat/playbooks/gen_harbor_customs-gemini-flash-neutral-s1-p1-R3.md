---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 2340
---
### Harbor Customs Playbook

#### Understanding the Mechanics & Objectives
- You keep all crates you carry unless you choose `night` (which confiscates your smallest crate) or get flagged.
- The dockhand always inspects the heaviest crate ($C_{\max}$). If `declared < C_max`, you are flagged: paying $-40$ penalty and $0.30 \times \text{total true hold value}$ in duty.
- If `declared >= C_max`, you are never flagged.
- Duty paid is based strictly on your *declared* value: $\lfloor 0.30 \times \text{declared} \rfloor$ on `main`, $\lfloor 0.15 \times \text{declared} \rfloor$ on `night`.
- To maximize net score:
  1. Always declare *exactly* the value of your largest crate: `declared = C_max`. Never declare less (avoids $-40$ penalty), and never declare more (declaring full hold value or higher numbers unnecessarily increases duty).
  2. Choose `main` vs. `night` purely by comparing duty savings to the value of the smallest crate lost:
     - `main` net payout: $\text{Total Hold Value} - \lfloor 0.30 \times C_{\max} \rfloor$
     - `night` net payout: $(\text{Total Hold Value} - C_{\min}) - \lfloor 0.15 \times C_{\max} \rfloor$
     - Duty saved by `night`: $\Delta D = \lfloor 0.30 \times C_{\max} \rfloor - \lfloor 0.15 \times C_{\max} \rfloor$.

---

#### Stage 1: Declare Stage
- When given my 3 crates $(C_{\min}, C_{\text{mid}}, C_{\max})$, identify $C_{\max}$.
- Always submit `[declare: C_max]`.
- What never works:
  - Declaring below $C_{\max}$ (guarantees a $-40$ penalty and maximum duty recalculation).
  - Declaring above $C_{\max}$ or declaring total hold value (wastes points on inflated duty for zero inspection benefit).

---

#### Stage 2: Route Stage
- Compute duty savings: $\Delta D = \lfloor 0.30 \times C_{\max} \rfloor - \lfloor 0.15 \times C_{\max} \rfloor$.
- Compare $\Delta D$ to $C_{\min}$:
  - If $\Delta D > C_{\min}$, submit `[route: night]`.
  - If $\Delta D \le C_{\min}$, submit `[route: main]`.
- Note on boundary conditions:
  - Because $C_{\max} \le 40$, the maximum possible duty saved $\Delta D$ is 6 points (achieved when $C_{\max} \in [34, 40]$).
  - Since crates are worth at least 5 points, `night` is profitable if and only if $C_{\min} = 5$ AND $C_{\max} \in [34, 40]$ (netting $+1$ point).
  - In all other scenarios ($C_{\min} \ge 6$ or $C_{\max} < 34$), submit `[route: main]`.