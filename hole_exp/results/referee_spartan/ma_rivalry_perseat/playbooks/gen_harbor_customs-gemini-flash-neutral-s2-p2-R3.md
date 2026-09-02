---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1834
---
# Harbor Customs Playbook

## Rules & Mechanics Reference
- **Hold:** 3 crates, values $c_{\min} \le c_{\text{mid}} \le c_{\max}$, total true value $T = c_{\min} + c_{\text{mid}} + c_{\max}$.
- **Spot Check Rule:** The harbormaster always inspects the heaviest crate ($c_{\max}$) for every player. If declaration $D < c_{\max}$, player is flagged: $-40$ penalty and duty recomputed at $\lfloor 0.30 \times T \rfloor$.
- **Optimal Declaration:** Declaring $D < c_{\max}$ guarantees a $-40$ penalty. Declaring $D > c_{\max}$ wastes points on unnecessary duty. Therefore, optimal declaration is always $D = c_{\max}$.
- **Route Math:**
  - Main Route Score: $T - \lfloor 0.30 \times D \rfloor$
  - Night Route Score: $(T - c_{\min}) - \lfloor 0.15 \times D \rfloor$
  - Duty savings from Night: $\Delta \text{Duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - For maximum crate value $c_{\max} \le 40$, maximum duty savings is $\Delta \text{Duty} = \lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$.
  - Night route is strictly better only when $c_{\min} < \Delta \text{Duty}$ (specifically occurs only if $c_{\min} = 5$ and $c_{\max} \ge 34$, where $\Delta \text{Duty} = 6$).

---

## Decision Protocol

### Stage 1: Declare
1. Identify the heaviest crate $c_{\max} = \max(\text{crates})$.
2. Submit `[declare: c_max]`.
3. Do not alter declaration based on game round, opponent actions, or current standings.

### Stage 2: Route
1. Calculate $\Delta \text{Duty} = \lfloor 0.30 \times c_{\max} \rfloor - \lfloor 0.15 \times c_{\max} \rfloor$.
2. Compare smallest crate $c_{\min} = \min(\text{crates})$ with $\Delta \text{Duty}$:
   - If $c_{\min} < \Delta \text{Duty}$ (i.e. $c_{\min} = 5$ and $c_{\max} \in [34, 40]$), choose `[route: night]`.
   - Otherwise, choose `[route: main]`.