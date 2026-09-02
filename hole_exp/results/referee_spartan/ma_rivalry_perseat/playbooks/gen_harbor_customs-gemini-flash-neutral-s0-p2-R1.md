---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1737
---
### Playbook: Harbor Customs

#### 1. Declaration Stage
* When the crates in my hold are dealt to me, find the single heaviest crate (the maximum value among the three crates).
* Set my declaration $D$ equal to exactly that heaviest crate value: $D = \max(c_1, c_2, c_3)$.
* Never declare below the heaviest crate value, as the referee always checks the heaviest crate and will inflict a -40 penalty plus full recomputed duty on true cargo.
* Never declare more than the heaviest crate to "blend in" or match table averages (e.g., declaring 38, 42, 47, or 59 when my heaviest crate is smaller). Opponents cannot see my crate values, there is no relative ranking penalty, and declaring extra points only increases the duty paid with zero upside.

#### 2. Route Stage
* Compare the cost of both routes given my declared value $D = \max(c_1, c_2, c_3)$ and my smallest crate value $c_{\min} = \min(c_1, c_2, c_3)$:
  * **Main Route Net Cost:** $\text{Duty}_{\text{main}} = \lfloor 0.30 \times D \rfloor$.
  * **Night Route Net Cost:** $\text{Duty}_{\text{night}} + c_{\min} = \lfloor 0.15 \times D \rfloor + c_{\min}$.
  * The duty savings of Night route is $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor \approx 0.15 \times D$.
* If $c_{\min} < (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor)$, choose `[route: night]`.
* If $c_{\min} \ge (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor)$, choose `[route: main]`.
* *Rule of thumb:* Night route is almost never worth it unless the smallest crate is extremely low (e.g., 5–6 points) and the heaviest crate is near the maximum (35–40 points) such that the 15% duty savings exceeds the lost crate. In all other cases, default to `[route: main]`.