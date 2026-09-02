---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 2165
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
- In all rounds, reply `[pledge: scout]` to minimize fuel commitment and maximize flexibility at the action stage.
- Never pledge `escort` or `raid` upfront; committing 2 fuel early provides no advantage over pledging `scout` (1 fuel) and deciding the actual move in the act stage.

---

### Act Stage Strategy

#### When evaluating my target (clockwise player):
- **If my target has a history of defecting to `raid` or pledged `raid` / `escort`:**
  - Expect them to act `raid` or `escort`.
  - Do NOT raid them; raiding an active raider or escort costs $-1$ point.

- **If my target consistently acts `scout` when pledging `scout`:**
  - Defect to `[act: raid]` against them to extract $+3$ points.

#### When evaluating my incoming attacker (counter-clockwise player):
- **If the player targeting me pledged `raid` or has a history of acting `raid`:**
  - Do NOT play `[act: scout]` as it yields $0$ points if raided.
  - If my clockwise target is expected to `scout`, play `[act: raid]`.
  - If my clockwise target is expected to `raid` or `escort`, play `[act: escort]` to block the incoming raid and guarantee $+2$ points.

- **If all players are reliably mutual-scouting without defection:**
  - Play `[act: scout]` in early rounds to build base points efficiently.
  - Exploit mutual-scout agreements by playing `[act: raid]` in later rounds when the clockwise target is passive.