---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1480
---
### Core Strategy & Mechanics
- Let my hold crates be $c_{\min} \le c_{\text{mid}} \le c_{\max}$.
- The harbormaster always inspects the heaviest crate ($c_{\max}$). A manifest is flagged if and only if $\text{declared} < c_{\max}$.
- Being flagged incurs a -40 point penalty and recalculates duty at $0.30 \times (c_{\min} + c_{\text{mid}} + c_{\max})$. Never declare below $c_{\max}$.
- Declaring above $c_{\max}$ increases the duty paid without providing any extra protection or benefit. There is no penalty for declared values differing from other players.

### Stage 1: Declare Stage
- Identify the largest crate $c_{\max}$ in my hold.
- Always reply `[declare: n]` where $n = c_{\max}$.
- Never declare a higher number than $c_{\max}$ to "match opponents", "blend in", or "catch up". Any point declared above $c_{\max}$ strictly wastes points on unnecessary duty.

### Stage 2: Route Stage
- Calculate the duty difference: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, where $D = c_{\max}$.
- For legal crate values ($5 \le c_{\min} \le 40$ and $D \le 40$), the duty savings $\Delta \text{duty}$ is at most 6 points (achieved when $D \in \{37, 38, 39, 40\}$).
- Compare $c_{\min}$ to $\Delta \text{duty}$:
  - If $c_{\min} < \Delta \text{duty}$ (specifically when $c_{\min} = 5$ and $D \ge 37$, where $\Delta \text{duty} = 6$), reply `[route: night]`.
  - In all other cases ($c_{\min} \ge \Delta \text{duty}$), reply `[route: main]`.