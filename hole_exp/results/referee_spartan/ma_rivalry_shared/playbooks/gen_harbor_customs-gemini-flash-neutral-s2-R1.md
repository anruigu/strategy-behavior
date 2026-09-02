---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 2081
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
- **Never declare the total sum of my hold:** Declaring the sum (e.g., 66, 72, 73) does not grant extra points or enable carrying more crates; it only inflates my duty without providing any inspection safety benefit.
- **Never declare below the heaviest crate:** An under-declaration triggers the -40 penalty and forces full 30% duty on the entire hold.
- **Never inflate my declaration to "blend in" or "match table averages":** Other players' declarations do not affect my inspection check.

---

### Stage 2: Route

- Compare the net outcome of `main` versus `night` based on the smallest crate ($S$) and declared heaviest crate ($H$):
  - `main` net contribution: $\text{Total Hold Value} - \lfloor 0.30 \times H \rfloor$
  - `night` net contribution: $(\text{Total Hold Value} - S) - \lfloor 0.15 \times H \rfloor$
  - The difference ($\text{night} - \text{main}$) simplifies to:
    $$\text{Duty Savings} - S \approx (0.15 \times H) - S$$
- **When $S > \lfloor 0.30 \times H \rfloor - \lfloor 0.15 \times H \rfloor$:** Choose `[route: main]`. (This is true in almost all standard distributions, as the value of the smallest crate lost almost always exceeds the ~15% duty savings on $H$).
- **When $S < \lfloor 0.30 \times H \rfloor - \lfloor 0.15 \times H \rfloor$:** Choose `[route: night]`. (Only optimal if the smallest crate is tiny and the heaviest crate is very large).