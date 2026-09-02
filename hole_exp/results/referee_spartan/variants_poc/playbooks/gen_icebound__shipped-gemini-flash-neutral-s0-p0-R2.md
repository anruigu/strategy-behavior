---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 2263
---
# Playbook: Icebound Manifest

### Rules & Mechanics Reminder
- Clockwise targeting: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North.
- Fuel cost is deducted *at pledge*: `scout` costs 1 fuel, `escort` costs 2 fuel, `raid` costs 2 fuel.
- At end of game, 1 fuel = 1 point.
- Pledging `scout` costs 1 fuel up front and leaves the option open to act `scout`, `escort`, or `raid` without paying extra fuel at the act stage.
- Net point payoff vs target act:
  - Raiding a scouting target yields $+3$ points (transferred from target).
  - Raiding an escorting or raiding target incurs a $-1$ point penalty.
  - Scouting yields $+3$ points if unraided, $0$ points if raided.
  - Escorting yields $+2$ points and blocks incoming raids.

---

### Pledge Stage Strategy
- In all rounds, reply `[pledge: scout]` to minimize fuel commitment (1 fuel) and maximize flexibility at the action stage.
- Never pledge `escort` or `raid` upfront; committing 2 fuel early provides no advantage over pledging `scout` and deciding the actual move in the act stage.

---

### Act Stage Strategy

#### Identifying the Game Environment:
- Track the actual past acts of my clockwise target (the player I attack) and my counter-clockwise attacker (the player who attacks me).
- Note whether opponents play uncommitted raids: in typical play, opponents will pledge `scout` but defect to `[act: raid]`.

#### Round 1:
- If opponents are unknown, start with `[act: scout]`.

#### Subsequent Rounds (Rounds 2–5):
- **Defensive Default (Opponents defecting to `raid`):**
  - If my clockwise target acts `raid` or `escort`, raiding them loses 1 point ($-1$).
  - If my counter-clockwise attacker acts `raid`, scouting yields $0$ points.
  - Therefore, whenever the clockwise target is acting `raid` (or `escort`), choose `[act: escort]`. This guarantees $+2$ points and blocks incoming raids, netting $+2$ per round compared to $-1$ from raiding a fellow raider.
- **Exploitative Play (Target reliably acts `scout`):**
  - If my clockwise target reliably plays `[act: scout]`, play `[act: raid]` to capture $+3$ points.
- **Cooperative Play (All players genuinely act `scout`):**
  - If incoming raids are not happening and the clockwise target acts `scout`, play `[act: scout]`.