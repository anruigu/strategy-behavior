---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2122
---
# Playbook: Icebound Manifest

### Rules & Mechanics Reminder
- Clockwise targeting: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North.
- Fuel cost is deducted *at pledge*: `scout` costs 1 fuel, `escort` costs 2 fuel, `raid` costs 2 fuel.
- At end of game, 1 fuel = 1 point.
- Fuel is charged solely from recorded pledges. Pledging `scout` costs 1 fuel and leaves the referee-accepted freedom to submit `[act: scout]`, `[act: escort]`, or `[act: raid]` at the act stage.
- Point payoffs:
  - Scouting yields $+3$ points if unraided, $0$ points if raided.
  - Escorting yields $+2$ points and blocks incoming raids.
  - Raiding a scouting target transfers $+3$ points.
  - Raiding an escorting or raiding target incurs a $-1$ point penalty.

---

### Pledge Stage Strategy
- Always reply `[pledge: scout]` in all rounds.
- This expends only 1 fuel per round (saving 3 fuel across 5 rounds = $+3$ end-of-game bonus points compared to pledging escort/raid) while preserving complete freedom to choose any act.

---

### Act Stage Strategy

#### Identifying the Game Environment:
- Clockwise target: East (North attacks East).
- Attacker: West (West attacks North).
- Look at actual recent acts (not pledges, since opponents frequently pledge `scout` and act `raid`).

#### Round 1:
- Start with `[act: scout]` to test baseline cooperation, or go straight to `[act: escort]` if playing defensively.

#### Subsequent Rounds (Rounds 2–5):
- **Default / Hostile Environment (West or East defects to `raid`):**
  - If West (attacker) is likely to act `raid`, scouting yields $0$ points.
  - If East (target) is likely to act `raid` or `escort`, raiding yields $-1$ point.
  - In this standard scenario, execute `[act: escort]`. This guarantees $+2$ points per round, blocks West's raid, and avoids the $-1$ penalty of attacking a non-scout.
- **Exploitative Play (Target acts `scout`):**
  - If East (target) reliably plays `[act: scout]`, play `[act: raid]` to capture $+3$ points.
- **Mutual Cooperation:**
  - Only play `[act: scout]` if West reliably does not raid. Otherwise, `[act: escort]` strictly dominates.