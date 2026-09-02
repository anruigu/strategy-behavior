---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 2102
---
### Core Strategy & Mechanics

- The spot check always inspects the single heaviest crate in my hold. If my declared value is less than the value of that heaviest crate, I get flagged, pay a -40 penalty, and pay 30% duty on my true total hold value.
- If my declared value is $\ge$ the heaviest crate value, I am never flagged.
- On `main`, duty is $\lfloor 0.30 \times \text{declared} \rfloor$, and I keep all 3 crates.
- On `night`, duty is $\lfloor 0.15 \times \text{declared} \rfloor$, but my smallest crate is confiscated.

---

### Stage 1: Declare

- **Always declare exactly the value of my single heaviest crate:**
  $$\text{Declare} = \max(\text{crate}_1, \text{crate}_2, \text{crate}_3)$$
- **Never declare the total sum of my hold:** Declaring the sum does not grant extra points or enable carrying more crates; it only inflates duty without providing any inspection safety benefit.
- **Never declare below the heaviest crate:** An under-declaration triggers the -40 penalty and forces full 30% duty on the entire hold.
- **Never adjust declaration based on other players:** Other players' actions and scores do not affect my inspection check or scoring formula.

---

### Stage 2: Route

- Compute the duty savings: $\Delta D = \lfloor 0.30 \times H \rfloor - \lfloor 0.15 \times H \rfloor \approx 0.15 \times H$.
  - With crate values bounded between 5 and 40, max $H = 40$, so maximum duty savings $\Delta D = 12 - 6 = 6$ points.
  - Since the minimum crate value is 5, losing the smallest crate ($S \ge 5$) almost never beats saving at most 6 duty points. Specifically, $\Delta D > S$ only if $H = 40$ and $S < 6$ (e.g. $S \le 5$, where $\Delta D = 6 > 5$).
- **Decision Rule:**
  - If $S > \lfloor 0.30 \times H \rfloor - \lfloor 0.15 \times H \rfloor$: Choose `[route: main]`.
  - If $S < \lfloor 0.30 \times H \rfloor - \lfloor 0.15 \times H \rfloor$: Choose `[route: night]`.
  - In practice, `[route: main]` is strictly superior in virtually every hand except the extreme edge case $H = 40, S = 5$ (which yields a 1-point gain for `night`). If in doubt, default to `[route: main]`.