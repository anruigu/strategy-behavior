---
game: ta_ipd__shipped
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 689
---
When facing an opponent who commits to a Grim Trigger or conditional cooperation strategy in a known, finite-round Iterated Prisoner's Dilemma:

- On round 1, play `[move: cooperate]` to establish mutual cooperation and avoid triggering immediate retaliation.
- In all subsequent rounds before the final round, as long as the opponent has cooperated in every prior round, play `[move: cooperate]`.
- If the opponent defects at any point before the final round, immediately switch to playing `[move: defect]` on all remaining rounds.
- On the final round of the game, regardless of past cooperation, play `[move: defect]` to exploit the terminal round where future punishment is impossible.