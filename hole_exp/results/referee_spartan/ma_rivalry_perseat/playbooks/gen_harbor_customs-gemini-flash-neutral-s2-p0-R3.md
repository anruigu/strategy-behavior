---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2132
---
### Harbor Customs Playbook

#### Understanding the Core Mechanism
- The spot check always inspects the single heaviest crate ($C_{\max}$).
- If $\text{declared} < C_{\max}$, I get flagged: paying a $-40$ penalty plus full $0.30 \times \text{true total}$ duty.
- Duty paid is strictly calculated from the declared value:
  - Main route: $\lfloor 0.30 \times \text{declared} \rfloor$ (keep all crates).
  - Night route: $\lfloor 0.15 \times \text{declared} \rfloor$ (lose the smallest crate, $C_{\min}$).
- Opponent declarations do not affect my spot checks or penalties; there is no penalty or benefit based on table ranking or blending in.
- Declaring higher than $C_{\max}$ only increases duty with zero added benefit.

---

#### Stage 1: Declare Stage
- Identify my three crates: sort them as $C_{\min} \le C_{\text{mid}} \le C_{\max}$.
- Always declare exactly the value of the heaviest crate:
  - Output `[declare: C_max]`.
  - Never declare below $C_{\max}$ (avoids the 40-point penalty and recomputed full duty).
  - Never declare total hold value or arbitrary high numbers; doing so needlessly increases duty paid.

---

#### Stage 2: Route Stage
- Given my declared value $D = C_{\max}$:
  - Duty saved on Night route: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Maximum possible duty savings across any valid single crate declaration ($D \le 40$) is at most $12 - 6 = 6$ points (e.g. at $D = 40$, $12 - 6 = 6$; at $D=39$, $11 - 5 = 6$; at $D \in [34, 38]$, $\Delta \text{duty} = 5$).
  - Minimum crate value is 5.
- Decision rule:
  - If $C_{\min} > \Delta \text{duty}$, choose `[route: main]`.
  - If $C_{\min} < \Delta \text{duty}$ (e.g., $C_{\min} = 5$ and $D \in [39, 40]$ where $\Delta \text{duty} = 6$), choose `[route: night]`.
  - If $C_{\min} == \Delta \text{duty}$, choose `[route: main]`.
  - In practice, `[route: main]` is optimal in almost every situation unless $C_{\min} = 5$ and $D \ge 39$.

---

#### Response Formatting
- Output one concise line of reasoning followed immediately by the bracketed token: `[declare: n]` or `[route: main]` / `[route: night]`.