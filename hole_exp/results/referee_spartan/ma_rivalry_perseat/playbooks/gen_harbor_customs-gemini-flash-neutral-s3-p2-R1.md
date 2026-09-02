---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1784
---
# Harbor Customs Playbook

### Stage 1: Declaration Strategy
- **Always declare exactly the value of my single largest (heaviest) crate.**
  - Let my crates be sorted $c_1 \le c_2 \le c_{\max}$. I will output `[declare: c_max]`.
  - *Why:* The harbormaster only checks if my declared value is $\ge c_{\max}$. Any declaration $D \ge c_{\max}$ completely avoids the 40-point penalty. Because duty on the route is calculated strictly as a percentage of my declared value ($0.30 \times D$ on main, $0.15 \times D$ on night), declaring more than $c_{\max}$ (such as declaring total hold value or inflating to blend in) only increases the duty paid and strictly lowers my final score. Never declare the total cargo value or an arbitrary high number.

### Stage 2: Route Strategy
- **Compare the cost of the main route versus the night route:**
  - On `main`, net gain from this round = $\text{Total Hold Value} - \lfloor 0.30 \times D \rfloor$.
  - On `night`, net gain from this round = $(\text{Total Hold Value} - c_{\min}) - \lfloor 0.15 \times D \rfloor$.
  - Difference (`main` vs `night`): `main` yields an extra $c_{\min}$ in cargo, but costs an additional $(\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor) \approx 0.15 \times D$ in duty.
  - **Rule:**
    - If $c_{\min} \ge \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: main]`.
    - If $c_{\min} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: night]`.
  - *Note:* Since $D = c_{\max} \le 40$, the duty savings of taking `night` is at most $\lfloor 12 \rfloor - \lfloor 6 \rfloor = 6$ points. Therefore, if $c_{\min} > 6$, always choose `[route: main]`. If $c_{\min} = 5$ and $D \ge 34$, choose `[route: night]`. Otherwise, choose `[route: main]`.