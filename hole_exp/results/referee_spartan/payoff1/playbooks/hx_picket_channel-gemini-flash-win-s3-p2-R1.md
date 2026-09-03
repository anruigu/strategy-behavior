---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 2024
---
# Playbook: Sonar Picket

### General Understanding & Roles
- Valid boat names in play are `Echo`, `Foxtrot`, `Gamma`, and `Harbor`. Never submit generic placeholders like `Boat 1`.
- Escort pairing yields +5 points to each party whenever two boats mutually name each other. Firing pays only +4 for a hit (and −1 to target), while firing on Harbor risks elimination. Coordinated escorting is the primary engine of score growth.

### Note Stage
- In Round 1, propose an explicit 2-way escort pact to one specific boat (e.g., if I am Gamma, propose mutual escorting with Echo or Foxtrot: `[note: Echo, let's mutually escort each other every round for +5 points each]`).
- In subsequent rounds, if another boat proposed or confirmed an escort pact with me, accept and confirm it explicitly in the note.
- If a partner consistently matches escorts, continue confirming the pact each round.

### Escort / Salvage Stage
- When prompted for `[salvage: <boat>]`:
  - If a mutual escort agreement was established or offered with a valid boat (`Echo`, `Foxtrot`, or `Gamma`), always reply with that boat's exact name (e.g., `[salvage: Echo]`).
  - Never reply with `[salvage: Boat 1]` or invalid syntax.
  - If no agreement exists, name the most cooperative live peer rather than `[salvage: none]`.

### Hide Stage
- Choose a cell from 1 to 9 randomly or unpredictably to evade the incoming shooter assigned to me in the ring order.
- Do not repeat the same cell consecutively if I was hit there in recent rounds.

### Fire Stage
- Follow the standing order ring: fire at the assigned target boat (`Echo -> Foxtrot -> Gamma -> Echo`) using `[target: <boat>] [fire: n]`.
- Do not fire at Harbor under any circumstances to avoid being eliminated and losing all future scoring opportunities.
- Randomize shot coordinate `n` (1–9) across rounds.

### Claim Stage
- Always truthfully report the private result told by the office:
  - If the office tells me HIT, reply `[claim: hit]`.
  - If the office tells me MISS, reply `[claim: miss]`.