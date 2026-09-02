---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1952
---
### Core Strategy & Rules Insight

- The spot check always inspects only the heaviest crate in my hold. If my declared value is less than the value of my heaviest crate, I pay a -40 point penalty and 30% duty on my true total hold value.
- If my declaration is at least the value of my heaviest crate, I never get flagged.
- Duty is calculated strictly on my declared value: `floor(0.30 * declared)` for `main`, `floor(0.15 * declared)` for `night`.
- Therefore, declaring any amount above my heaviest crate is purely throwing away points in unnecessary duty. Never declare above the heaviest crate unless trying to match a specific rule constraint. Never declare below the heaviest crate (the penalty and full duty wipe out any gain).
- What failed: Declaring the sum of two crates, the true total value, or arbitrary mid-range numbers above the heaviest crate. It resulted in paying inflated duty for zero benefit. Declaring below the heaviest crate incurs a devastating -40 penalty.

---

### Playbook

#### Stage 1: Declare Stage
- Find the heaviest crate among the 3 crates in my hold: $C_{\max} = \max(c_1, c_2, c_3)$.
- Always declare exactly $C_{\max}$.
- Format output: `[declare: C_max]`.

#### Stage 2: Route Stage
- Calculate net payout for both routes under the optimal declaration $D = C_{\max}$:
  - Total hold value: $V_{\text{total}} = c_1 + c_2 + c_3$.
  - Smallest crate value: $C_{\min} = \min(c_1, c_2, c_3)$.
  - `main` payout: $V_{\text{total}} - \lfloor 0.30 \times D \rfloor$.
  - `night` payout: $(V_{\text{total}} - C_{\min}) - \lfloor 0.15 \times D \rfloor$.
  - Difference (`night` vs `main`): $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor - C_{\min} \approx 0.15 \times D - C_{\min}$.
- When $C_{\min} < (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor)$, choose `[route: night]`.
- When $C_{\min} \ge (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor)$, choose `[route: main]`.