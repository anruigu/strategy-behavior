---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 2482
---
### Game Dynamics & Clockwise Relationships

- Raids always target clockwise: North $\rightarrow$ East, East $\rightarrow$ West, West $\rightarrow$ North.
- Incoming attackers: North $\leftarrow$ West, East $\leftarrow$ North, West $\leftarrow$ East.
- Scoring rules:
  - `scout` scores 3 points if not raided, 0 points if raided. Fuel cost: 1.
  - `escort` scores 2 points and blocks incoming theft (attacker loses 1 point). Fuel cost: 2.
  - `raid` steals 5 points from a target whose final act is `scout`. Against a target acting `escort` or `raid`, the raider loses 1 point. Fuel cost: 2.
  - End game: 1 point per remaining unused fuel.
- Critical interaction: Opponents frequently pledge `scout` and then defect to `raid` at the act stage. If my target acts `raid`, my raid on them fails and penalizes me (-1 point). If my attacker acts `raid`, I must have pledged `escort` to protect myself.

---

### Pledge Stage

- **Defensive Escorting:**
  - If my incoming attacker defected to `raid` in the previous round, or has shown a strong propensity to raid, pledge `[pledge: escort]`.
  - Pledging `escort` guarantees 2 points and inflicts a -1 penalty on the incoming raider, neutralizing aggressive neighbors.
- **Cooperative Scouting:**
  - If my incoming attacker consistently plays `scout` (both pledge and act), pledge `[pledge: scout]`.
  - In Round 1, pledge `[pledge: scout]` to observe table tendencies at minimal fuel cost (1 fuel).
- **Avoiding Raid Pledges:**
  - Do not pledge `[pledge: raid]`. It wastes 2 fuel upfront and signals aggression, while pledging `scout` or `escort` keeps options open.

---

### Act Stage

- **After `[pledge: escort]`:**
  - Always submit `[act: escort]`. Do not switch to raid or scout; follow through to secure the 2 points and block the incoming raider.
- **After `[pledge: scout]`:**
  - **Predict Target Defection:** Look at my clockwise target's history. If the target has defected to `raid` in previous rounds, expect them to act `raid` again. Do not raid them (raiding into raid loses 1 point); submit `[act: scout]`.
  - **Exploit Pure Scouters:** Only defect to `[act: raid]` if my clockwise target has a proven history of actually executing `[act: scout]` in the action stage.
  - **Default Follow-Through:** If uncertain, submit `[act: scout]`.

---

### Output Format

- Provide exactly one concise reasoning sentence, followed immediately by the bracketed token on a new line: `[pledge: <choice>]` or `[act: <choice>]`.