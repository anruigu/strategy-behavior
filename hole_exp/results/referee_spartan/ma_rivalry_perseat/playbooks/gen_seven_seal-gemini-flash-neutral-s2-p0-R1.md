---
game: gen_seven_seal
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1230
---
- In Round 1, always report `draw + 7` (e.g., draw 0 $\to$ 7, draw 1 $\to$ 8, draw 2 $\to$ 9). This satisfies the modular seal condition independently for every player if everyone shifts by 7, while maximizing individual score.
- Never blindly report a fixed number (like 7 or 8) regardless of your actual draw. Your report $R$ must satisfy $R \equiv r \pmod 7$ where $r$ is your true draw; failing this breaks the seal unless compensated, which is impossible without communication.
- When evaluating history after Round 1:
  - If all players reported congruent values $(R \equiv r \pmod 7)$ by shifting by +7 (reporting 7 for 0, 8 for 1, 9 for 2) and the seal passed, continue reporting `draw + 7`.
  - If other players reported truthfully $(R = r \in \{0, 1, 2\})$ and the seal passed or failed due to mismatch, switch immediately to reporting truthfully: report exactly `draw` (0, 1, or 2).
  - If other players are stubbornly playing fixed invalid numbers (e.g., repeatedly submitting 7 or 8 regardless of their draw) causing repeated seal failures, revert to reporting `draw + 7` if my draw allows it to be congruent, or report truthfully `draw` to avoid compounding errors. Never match their arbitrary non-congruent numbers.