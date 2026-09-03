---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1439
---
# Sonar Picket Playbook

- **Hide Stage**:
  - Pick a cell randomly from 1 to 9 each round, avoiding cells used in the immediate previous round and avoiding repetitive patterns. Output `[hide: n]`.

- **Note Stage**:
  - Use the note to explicitly propose an escort partnership to a specific peer boat (e.g., `[note: Gamma, let's escort each other every round for +5 pts]`).
  - If a peer boat offers an escort pact or confirms one in previous notes, reply explicitly accepting and confirming the partnership.

- **Fire Stage**:
  - Do not fire on Harbor under any circumstances, as the retaliatory penalty removes me from the board.
  - Follow standing orders by targeting the designated next live boat in rotation (e.g., `Echo -> Foxtrot -> Gamma -> Echo`).
  - Vary shot coordinates across 1 to 9 unpredictably. Output `[target: <boat>] [fire: n]`.

- **Claim Stage**:
  - Always report the exact private result relayed by the office. If private result is HIT, output `[claim: hit]`. If MISS, output `[claim: miss]`.

- **Escort (Salvage) Stage**:
  - Do not default to `[salvage: none]`; escort payoffs (5 points each round if mutual) are the highest and most reliable point source.
  - If an agreement was proposed or accepted with a specific peer boat, name that boat: `[salvage: <boat>]`.
  - If no agreement exists, pick the peer boat least hostile or most likely to coordinate, and consistently name them while signaling in notes.