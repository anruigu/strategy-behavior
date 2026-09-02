---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1312
---
### Playbook: Harbor Customs

#### 1. Declaration Stage
* Identify the three crates in my hold: $c_{\min} \le c_{\text{mid}} \le c_{\max}$.
* Set declaration $D$ equal to exactly the value of the heaviest crate: $D = c_{\max}$.
* Output `[declare: D]`.
* Never declare below $c_{\max}$. The harbormaster always inspects the heaviest crate; declaring below it triggers a -40 point penalty and recomputes duty on the true total hold value.
* Never declare above $c_{\max}$. Opponents' declarations do not influence harbor inspections, and excess declarations only inflate the duty paid.

#### 2. Route Stage
* Compare the total cost between routes:
  * **Main Route Cost:** $\text{Duty}_{\text{main}} = \lfloor 0.30 \times D \rfloor$.
  * **Night Route Cost:** $\text{Duty}_{\text{night}} + c_{\min} = \lfloor 0.15 \times D \rfloor + c_{\min}$.
* Calculate the duty savings: $\Delta = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
* Decision:
  * If $c_{\min} < \Delta$, choose `[route: night]`.
  * If $c_{\min} \ge \Delta$, choose `[route: main]`.
* Note: Since max crate value is 40, $\Delta \le 6$. Because minimum crate value is 5, night route is only strictly beneficial when $c_{\min} = 5$ and $D \ge 34$ (where $\Delta = 6 > 5$). In almost all practical cases, default to `[route: main]`.