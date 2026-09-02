---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2057
---
### Harbor Customs Playbook

#### Rules & Payoff Mechanics
- The spot check inspects strictly the heaviest single crate in my hold. If my declared value $D \ge \max(c_1, c_2, c_3)$, I will never be flagged.
- Duty on `main` is $\lfloor 0.30 \times D \rfloor$, and I retain all 3 crates.
- Duty on `night` is $\lfloor 0.15 \times D \rfloor$, but I lose my smallest crate $\min(c_1, c_2, c_3)$.
- There is no reward or bonus for declaring higher than necessary, nor is there any penalty for declaring under the true total hold value, provided $D \ge \max(c_1, c_2, c_3)$. Declaring the full hold value wastes points on extra duty.
- The inspection is purely individual; other players' declarations or route choices have zero impact on my spot check or payoffs.

#### Stage 1: Declaration
- Identify the heaviest crate value $M = \max(c_1, c_2, c_3)$.
- Declare exactly $M$: `[declare: M]`. Never declare the sum of crates, an arbitrary high number, or anything greater than $M$.

#### Stage 2: Route Choice
- Compare the net round payoff of both routes given $D = M$:
  - Main net payoff: $(c_1 + c_2 + c_3) - \lfloor 0.30 \times M \rfloor$.
  - Night net payoff: $(c_1 + c_2 + c_3) - \min(c_1, c_2, c_3) - \lfloor 0.15 \times M \rfloor$.
- Calculate the duty saved on night: $\Delta \text{duty} = \lfloor 0.30 \times M \rfloor - \lfloor 0.15 \times M \rfloor$.
- Since max crate value is 40, max $\Delta \text{duty}$ is at most $\lfloor 12.0 \rfloor - \lfloor 6.0 \rfloor = 6$ points (often 2–6 points).
- If $\min(c_1, c_2, c_3) < \Delta \text{duty}$, choose `[route: night]`.
- If $\min(c_1, c_2, c_3) \ge \Delta \text{duty}$, choose `[route: main]`. Since minimum crate values are $\ge 5$, `main` is virtually always optimal unless $\Delta \text{duty} = 6$ and the smallest crate is strictly 5.

#### What Not to Do
- Never declare the total hold value or inflate declarations to match table averages or blend in.
- Never declare below the heaviest crate value $\max(c_1, c_2, c_3)$, as the -40 penalty and recalculated full-hold duty destroy round score.