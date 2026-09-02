---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 2466
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
     - Net difference (`night` minus `main`): $\lfloor 0.30 \times C_{\max} \rfloor - \lfloor 0.15 \times C_{\max} \rfloor - C_{\min} \approx 0.15 \times C_{\max} - C_{\min}$.

---

#### Stage 1: Declare Stage
- When given my 3 crates $(C_{\min}, C_{\text{mid}}, C_{\max})$, find $C_{\max}$.
- Always submit `[declare: C_max]`.
- What never works:
  - Declaring below $C_{\max}$ (guarantees a catastrophic $-40$ penalty and full recalculation).
  - Declaring the sum of all crates or arbitrary numbers above $C_{\max}$ to "ship full cargo" or "blend in" (purely wastes points on inflated duty).

---

#### Stage 2: Route Stage
- When choosing between `main` and `night`:
  - Calculate duty saved on `night`: $\Delta D = \lfloor 0.30 \times C_{\max} \rfloor - \lfloor 0.15 \times C_{\max} \rfloor$.
  - Compare duty saved $\Delta D$ to the value of the smallest crate lost $C_{\min}$.
  - If $\Delta D > C_{\min}$, submit `[route: night]`.
  - Otherwise (if $C_{\min} \ge \Delta D$), submit `[route: main]`.
- Since $C_{\max} \le 40$, the maximum duty saved by `night` is at most $\lfloor 12 \rfloor - \lfloor 6 \rfloor = 6$ points. Since $C_{\min} \ge 5$, `night` is almost never worth it unless $C_{\min}$ is extremely small (e.g., 5) and $C_{\max}$ is very large ($\ge 34$ where $\Delta D = 6 > 5$). In virtually all other distributions, default to `[route: main]`.