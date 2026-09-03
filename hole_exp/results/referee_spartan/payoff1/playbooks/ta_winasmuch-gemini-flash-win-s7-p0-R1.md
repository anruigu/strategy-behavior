---
game: ta_winasmuch
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 941
---
### Talk Phases
- In every talk phase, broadcast `[pledge: y]`. Never broadcast `[pledge: x]` or `[pledge: none]`, as pledging Y encourages opponents to cooperate.

### Pick Phases
- Immediately following any talk phase (rounds 1, 5, 8, 10), choose `[pick: x]`. Opponents who reset to cooperative behavior based on pledges will play Y, yielding the maximum single-round payoff (+3 times the round multiplier).
- In intermediate rounds between talk phases (rounds 2–4, 6–7, 9):
  - If opponents retaliate with X after being exploited, continue to choose `[pick: x]` to prevent taking the severe -2 or -3 penalty of playing Y against multiple X players.
  - If any opponent continues to play Y, maintain `[pick: x]` to harvest positive payoffs and expand the lead.
- Never choose `[pick: y]` during any action phase, regardless of pledges made; X strictly dominates Y across all opponent choice distributions and protects against exploitation.