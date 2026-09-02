---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1985
---
# Harbor Customs Playbook

## Rules & Mechanics Reference
- **Hold:** 3 crates, values $c_{\min} \le c_{\text{mid}} \le c_{\max}$, total true value $T = c_{\min} + c_{\text{mid}} + c_{\max}$.
- **Spot Check Rule:** The harbormaster *always* weighs the heaviest crate ($c_{\max}$) for every player. If my declaration $D < c_{\max}$, I am automatically flagged: $-40$ penalty and duty becomes $\lfloor 0.30 \times T \rfloor$.
- **Never under-declare below $c_{\max}$:** Declaring less than $c_{\max}$ guarantees a 40-point penalty and maximum duty.
- **Never over-declare above $c_{\max}$:** Duty increases strictly with declaration ($\lfloor 0.30 \times D \rfloor$ or $\lfloor 0.15 \times D \rfloor$). Declaring above $c_{\max}$ (e.g. declaring full hold value $T$ or arbitrary numbers) never provides any bonus points, avoids no additional risk, and strictly wastes points on excess duty.

---

## Decision Protocol

### Stage 1: Declare
- Identify the value of the heaviest crate in my current hand ($c_{\max}$).
- Always declare exactly $c_{\max}$:
  `[declare: c_max]`
- Ignore other players' declarations, pack averages, and lobby trends—there is no penalty for standing out and no benefit to blending in.
- Never declare the sum of crates ($T$) or arbitrary numbers above $c_{\max}$.

### Stage 2: Route Selection
With $D = c_{\max}$, evaluate the net payout of both routes:
- **Main Route Net:** $T - \lfloor 0.30 \times c_{\max} \rfloor$
- **Night Route Net:** $(T - c_{\min}) - \lfloor 0.15 \times c_{\max} \rfloor$

Compare the savings in duty against the loss of the smallest crate:
- Duty saved by going night: $\Delta \text{Duty} = \lfloor 0.30 \times c_{\max} \rfloor - \lfloor 0.15 \times c_{\max} \rfloor \approx 0.15 \times c_{\max}$.
- When $c_{\min} < \Delta \text{Duty}$ (i.e., when $c_{\min} \le \lfloor 0.30 \times c_{\max} \rfloor - \lfloor 0.15 \times c_{\max} \rfloor$), choose `[route: night]`.
- When $c_{\min} \ge \Delta \text{Duty}$, choose `[route: main]`.