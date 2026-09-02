---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1710
---
### Core Strategy & Mechanics
- Let my hold crates be $c_{\min} \le c_{\text{mid}} \le c_{\max}$.
- The harbormaster always inspects the heaviest crate ($c_{\max}$). A manifest is flagged if and only if $\text{declared} < c_{\max}$.
- Being flagged incurs a -40 point penalty and recalculates duty at $0.30 \times (c_{\min} + c_{\text{mid}} + c_{\max})$. Never declare below $c_{\max}$.
- Declaring above $c_{\max}$ increases the duty paid without providing any extra protection or benefit. There is no penalty for declared values differing from other players.

### Stage 1: Declare Stage
- When the declare stage is put to me, identify the largest crate $c_{\max}$ in my hold.
- Always reply `[declare: n]` where $n = c_{\max}$.
- Never declare a higher number than $c_{\max}$ to "match opponents", "blend in", or "catch up". Any point declared above $c_{\max}$ strictly wastes points on unnecessary duty.

### Stage 2: Route Stage
- Calculate the net payout of both routes given $D = c_{\max}$:
  - `main`: Score is $(c_{\min} + c_{\text{mid}} + c_{\max}) - \lfloor 0.30 \times D \rfloor$.
  - `night`: Score is $(c_{\text{mid}} + c_{\max}) - \lfloor 0.15 \times D \rfloor$ (losing $c_{\min}$).
- The net difference $(\text{main} - \text{night})$ is $c_{\min} - (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor) \approx c_{\min} - \lfloor 0.15 \times D \rfloor$.
- When the route stage is put to me:
  - If $c_{\min} > \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, reply `[route: main]`.
  - If $c_{\min} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$ (e.g., $c_{\min} \le 5$ and $D \ge 35$), reply `[route: night]`.
  - If equal, default to `[route: main]`.