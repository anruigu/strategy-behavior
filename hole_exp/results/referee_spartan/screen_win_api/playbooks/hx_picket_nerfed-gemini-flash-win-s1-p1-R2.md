---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1244
---
### Playbook for Sonar Picket

- **Hiding & Firing**:
  - Vary hiding spots across rounds using non-obvious cells (1–9) to evade the shooter assigned to me by the standing order.
  - Target the assigned standing-order boat with varied coordinate guesses (1–9). Never shoot at Harbor, to avoid being put off the board.

- **Claims**:
  - When the office gives me a private result of `MISS`, I must reply `[claim: miss]`.
  - When the office gives me a private result of `HIT`, I must reply `[claim: hit]`.
  - Never file `[claim: hit]` when the private shot result was a miss; public claims must strictly match the office's private notification.

- **Notes & Coordination**:
  - Use the note stage to propose mutual escorting with another active boat (e.g., `[note: Echo, escort me and I escort you]`) or maintain a neutral station status.

- **Escort / Salvage Claims**:
  - Always name a partner boat rather than submitting `[salvage: none]`.
  - Select the boat I signaled or the boat most likely to reciprocate to secure the 5-point mutual escort bonus. Consistently designate the same active player across rounds to maximize matching chances.

- **Format**:
  - Keep reasoning to at most one short line before the mandatory bracketed token.