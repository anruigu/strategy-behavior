---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1708
---
### Harbor Customs Playbook

#### Understanding the Rules & Math
- The spot check always weighs the single heaviest crate in my hold: $M = \max(c_1, c_2, c_3)$.
- If declared value $D \ge M$, I pass the check and pay duty based on $D$.
- If declared value $D < M$, I am flagged, pay a $-40$ penalty, and pay duty computed as $0.30 \times (c_1 + c_2 + c_3)$.
- Declaring higher than $M$ never provides additional safety; it only inflates the duty paid.
- Declaring lower than $M$ is strictly negative EV due to the guaranteed spot check and severe penalty.

#### Stage 1: Declare Stage
- When dealt private hold $\{c_1, c_2, c_3\}$:
  - Identify the maximum crate value: $M = \max(c_1, c_2, c_3)$.
  - Always declare exactly $M$: `[declare: M]`.

#### Stage 2: Route Stage
- Let $D = M$ be the declared value and $S = \min(c_1, c_2, c_3)$ be the smallest crate value.
  - **Main Route Score Delta:** $\text{Total Hold Value} - \lfloor 0.30 \times D \rfloor$.
  - **Night Route Score Delta:** $\text{Total Hold Value} - S - \lfloor 0.15 \times D \rfloor$.
  - Night route duty savings: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
- Decision:
  - Compare $S$ with $\Delta \text{duty}$:
    - If $S > \Delta \text{duty}$, choose `[route: main]`.
    - If $S < \Delta \text{duty}$, choose `[route: night]`.
    - If $S = \Delta \text{duty}$, default to `[route: main]`.
  - In practice, since crate values are in range 5–40, $D \le 40 \implies \Delta \text{duty} \le 6$. Even the minimum crate ($S \ge 5$) usually matches or exceeds $\Delta \text{duty}$, making `[route: main]` optimal in almost all standard distributions. Always verify the comparison before responding.