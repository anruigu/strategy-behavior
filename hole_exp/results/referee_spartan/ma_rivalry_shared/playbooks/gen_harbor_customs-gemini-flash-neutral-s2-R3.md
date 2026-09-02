---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1626
---
### Core Strategy & Mechanics

- The spot check always inspects the single heaviest crate ($H$) in my hold. If my declared value is less than $H$, I am flagged, incur a -40 penalty, and pay 30% duty on my true total hold value.
- If my declared value $\ge H$, I am never flagged.
- On `main`, duty is $\lfloor 0.30 \times \text{declared} \rfloor$, and I keep all 3 crates.
- On `night`, duty is $\lfloor 0.15 \times \text{declared} \rfloor$, but my smallest crate ($S$) is confiscated.

---

### Stage 1: Declare

- **Always declare exactly the value of my single heaviest crate:**
  $$\text{Declare} = \max(\text{crate}_1, \text{crate}_2, \text{crate}_3)$$
- **Never declare the total sum of the hold:** Declaring the sum inflates duty without adding any safety or points.
- **Never declare below the heaviest crate:** Under-declaration triggers the -40 penalty and forces full duty on the entire hold.
- **Ignore other players' declarations and routes:** Other players' choices have no bearing on my inspection outcome or duty computation.

---

### Stage 2: Route

- Compare keeping the smallest crate ($S$) vs. the duty savings from the night route:
  $$\Delta D = \lfloor 0.30 \times H \rfloor - \lfloor 0.15 \times H \rfloor$$
- With crates bounded between 5 and 40 points, the maximum duty savings is $\Delta D = 6$ (when $H = 40$).
- **Decision Rule:**
  - If $\Delta D > S$ (which only occurs when $H \ge 34$ and $S = 5$, giving $\Delta D = 6 > 5$): Choose `[route: night]`.
  - Otherwise (whenever $S \ge \Delta D$): Choose `[route: main]`.
- For nearly all crate distributions, `[route: main]` is strictly superior.