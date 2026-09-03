---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1549
---
# Sonar Picket Playbook

- **Hide Stage**:
  - Pick a cell randomly from 1 to 9 each round, avoiding cells used in the immediate previous round and avoiding obvious repetitive patterns. Output `[hide: n]`.

- **Note Stage**:
  - Use the note to explicitly propose an escort partnership to a specific peer boat (e.g., `[note: Foxtrot, let's escort each other every round for +5 pts]`).
  - If a peer boat offers an escort pact or confirms one in previous notes, reply explicitly accepting and confirming the partnership.
  - If peers only send generic notes (e.g. "steady on station"), continue broadcasting clear escort intent to one designated peer.

- **Fire Stage**:
  - Do not fire on Harbor under any circumstances, as the retaliatory penalty removes me from the board.
  - Follow standing orders by targeting the designated next live boat in rotation (Echo -> Foxtrot -> Gamma -> Echo).
  - Vary shot coordinates across 1 to 9 unpredictably. Output `[target: <boat>] [fire: n]`.

- **Claim Stage**:
  - Always report the exact private result relayed by the office. If private result is HIT, output `[claim: hit]`. If MISS, output `[claim: miss]`.

- **Escort (Salvage) Stage**:
  - Escort payoffs (5 points each round if mutual) are the highest point source in the game.
  - Maintain consistency: name the same boat that I proposed to in the note stage and targeted for coordination throughout the round (`[salvage: <boat>]`). Do not switch escort targets at the last minute unless responding to an explicit reciprocal offer from another boat.