---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1910
---
# Harbor Customs Playbook

## Rules & Mechanics Reference
- **Hold:** 3 crates, values $c_{\min} \le c_{\text{mid}} \le c_{\max}$, total true value $T = c_{\min} + c_{\text{mid}} + c_{\max}$.
- **Spot Check Rule:** The harbormaster *always* weighs the heaviest crate ($c_{\max}$) for every player. If my declaration $D < c_{\max}$, I am automatically flagged: $-40$ penalty and duty becomes $\lfloor 0.30 \times T \rfloor$.
- **Declaration Principle:** Declaring $D < c_{\max}$ guarantees $-40$ penalty. Declaring $D > c_{\max}$ strictly wastes points on higher duty without any benefit. Therefore, always declare exactly $D = c_{\max}$.
- **Route Math:**
  - Main Route Net: $T - \lfloor 0.30 \times D \rfloor$
  - Night Route Net: $(T - c_{\min}) - \lfloor 0.15 \times D \rfloor$
  - Duty savings from Night: $\Delta \text{Duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Since crate values range from 5 to 40, $c_{\max} \le 40 \implies \Delta \text{Duty} \le \lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$.
  - Since $c_{\min} \ge 5$, $c_{\min} < \Delta \text{Duty}$ is mathematically impossible in nearly all standard deals (only if $c_{\min} = 5$ and $c_{\max} \ge 34$ does $\Delta \text{Duty} = 6 > 5$).

---

## Decision Protocol

### Stage 1: Declare
1. Identify the heaviest crate $c_{\max} = \max(\text{crates})$.
2. Submit `[declare: c_max]`.
3. Do not adjust for other players' scores, declarations, or historical patterns.

### Stage 2: Route
1. Calculate $\Delta \text{Duty} = \lfloor 0.30 \times c_{\max} \rfloor - \lfloor 0.15 \times c_{\max} \rfloor$.
2. Check if $c_{\min} < \Delta \text{Duty}$:
   - If $c_{\min} < \Delta \text{Duty}$ (e.g. $c_{\min} = 5$ and $c_{\max} \in [34, 40]$ where $\Delta \text{Duty} = 6$), choose `[route: night]`.
   - Otherwise (all cases where $c_{\min} \ge \Delta \text{Duty}$), choose `[route: main]`.