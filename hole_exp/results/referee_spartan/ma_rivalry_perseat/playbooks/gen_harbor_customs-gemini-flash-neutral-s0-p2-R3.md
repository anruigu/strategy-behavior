---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1575
---
### Playbook: Harbor Customs

#### 1. Declaration Stage
* Identify the three crates in my hold: $c_{\min} \le c_{\text{mid}} \le c_{\max}$.
* Set declaration $D$ equal to exactly the value of the heaviest crate: $D = c_{\max}$.
* Output `[declare: D]`.
* **Reasoning & Constraints:**
  * Never declare below $c_{\max}$. The harbormaster always inspects the heaviest crate; declaring below it triggers an immediate -40 point penalty and recomputes duty at 30% of the true total hold value.
  * Never declare above $c_{\max}$. Other players' declarations have zero effect on spot-check mechanics; declaring higher only needlessly inflates duty.

#### 2. Route Stage
* Compare the total cost between routes:
  * **Main Route Cost:** $\text{Duty}_{\text{main}} = \lfloor 0.30 \times D \rfloor$.
  * **Night Route Cost:** $\text{Duty}_{\text{night}} + c_{\min} = \lfloor 0.15 \times D \rfloor + c_{\min}$.
* Calculate the net duty savings from taking night: $\Delta = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
* **Decision Rule:**
  * If $\Delta > c_{\min}$, choose `[route: night]`.
  * If $\Delta \le c_{\min}$, choose `[route: main]`.
* **Practical Thresholds:**
  * Since maximum declaration is $D \le 40$, the maximum duty savings $\Delta$ is 6 (attained when $34 \le D \le 40$).
  * Since crate values are $\ge 5$, `[route: night]` is mathematically advantageous *only* when $c_{\min} = 5$ AND $D \ge 34$ (where duty savings is 6 points vs 5 crate loss, gaining +1 point).
  * In all other cases ($c_{\min} > 5$, or $D \le 33$), choose `[route: main]`.