---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1707
---
### Core Strategy & Rules Insight

- The spot check always inspects only the heaviest crate in my hold. If my declared value is less than the value of my heaviest crate, I pay a -40 point penalty and 30% duty on my true total hold value.
- If my declaration is at least the value of my heaviest crate, I never get flagged.
- Duty is calculated strictly on my declared value: `floor(0.30 * declared)` for `main`, `floor(0.15 * declared)` for `night`.
- Declaring any amount above my heaviest crate is throwing away points in unnecessary duty. Never declare below the heaviest crate (the penalty and full duty wipe out any gain).
- Since crate values range from 5 to 40, the maximum possible duty savings from `night` over `main` is $\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$ points. Since the smallest possible crate value is 5, `night` is only potentially viable if $C_{\min} = 5$ and $D \ge 34$, but in nearly all hands `main` is strictly superior because saving 4-6 points of duty does not justify sacrificing a crate worth 5-40 points.

---

### Playbook

#### Stage 1: Declare Stage
- Find the heaviest crate among the 3 crates in my hold: $C_{\max} = \max(c_1, c_2, c_3)$.
- Always declare exactly $C_{\max}$.
- Format output: `[declare: C_max]`.

#### Stage 2: Route Stage
- Evaluate the exact net value of both routes given declared value $D = C_{\max}$:
  - Duty saved by night: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Smallest crate value: $C_{\min} = \min(c_1, c_2, c_3)$.
- If $\Delta \text{duty} > C_{\min}$, choose `[route: night]`.
- Otherwise (if $C_{\min} \ge \Delta \text{duty}$), choose `[route: main]`.