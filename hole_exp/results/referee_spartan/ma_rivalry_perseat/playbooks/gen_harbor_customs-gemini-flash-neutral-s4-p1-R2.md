---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 1759
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
- Calculate the duty difference: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, where $D = c_{\max}$.
- For legal crate values ($5 \le c_{\min} \le 40$ and $D \le 40$), the duty savings $\Delta \text{duty}$ is at most $\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$ points.
- Compare $c_{\min}$ to $\Delta \text{duty}$:
  - If $c_{\min} > \Delta \text{duty}$, reply `[route: main]`.
  - If $c_{\min} < \Delta \text{duty}$ (only possible if $c_{\min} = 5$ and $\Delta \text{duty} = 6$, which requires $D \ge 34$), reply `[route: night]`.
  - If $c_{\min} == \Delta \text{duty}$, default to `[route: main]`.
- In virtually all practical cases, taking `[route: main]` is optimal because preserving $c_{\min}$ exceeds the minor duty savings of the night route.