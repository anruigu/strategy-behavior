---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 2334
---
### Harbor Customs Playbook

#### Understanding the Core Mechanism
- The spot check always inspects the single heaviest crate ($C_{\max}$).
- If $\text{declared} < C_{\max}$, I get flagged: paying a $-40$ penalty plus full $0.30 \times \text{true total}$ duty.
- Duty paid is strictly calculated from the declared value:
  - Main route: $\lfloor 0.30 \times \text{declared} \rfloor$ (keep all crates).
  - Night route: $\lfloor 0.15 \times \text{declared} \rfloor$ (lose the smallest crate, $C_{\min}$).
- There is zero benefit to declaring more than $C_{\max}$ unless forced, as declaring extra only increases the duty paid without providing any safety or bonus.
- Opponent declarations do not affect my spot checks or penalties; I do not need to "blend in" or match table averages.

---

#### Stage 1: Declare Stage
- Identify my three crates: sort them as $C_{\min} \le C_{\text{mid}} \le C_{\max}$.
- Always declare exactly the value of the heaviest crate:
  - Output `[declare: C_max]`.
  - Never declare below $C_{\max}$ (avoids the 40-point penalty and recomputed full duty).
  - Never declare total hold value or arbitrary high numbers (e.g., 60–80) to "blend in" or "press score"; doing so only inflates my duty payment for zero gain.

---

#### Stage 2: Route Stage
- Evaluate the exact net payout of both routes given my declared value $D = C_{\max}$:
  - **Main Net Gain**: $(C_{\min} + C_{\text{mid}} + C_{\max}) - \lfloor 0.30 \times D \rfloor$
  - **Night Net Gain**: $(C_{\text{mid}} + C_{\max}) - \lfloor 0.15 \times D \rfloor$
- Compare the two:
  - The difference $(\text{Main} - \text{Night})$ equals $C_{\min} - (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor) \approx C_{\min} - \lfloor 0.15 \times D \rfloor$.
  - When $C_{\min} > \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: main]`.
  - When $C_{\min} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: night]`. (This typically occurs when $C_{\min}$ is very small, e.g., 5 or 6, and $D = C_{\max}$ is high, e.g., 35–40, making the 15% duty savings larger than the lost crate).
  - If equal, default to `[route: main]`.

---

#### Response Formatting
- Output concise reasoning followed immediately by the exact token format: `[declare: n]` or `[route: main]` / `[route: night]`.