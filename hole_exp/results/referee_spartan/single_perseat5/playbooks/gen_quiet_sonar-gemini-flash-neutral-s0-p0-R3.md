---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1285
---
- **Claim Stage**:
  - Always submit the exact outcome provided by the referee: `[claim: hit]` if told hit, `[claim: miss]` if told miss. Never deviate, as claims must strictly match the private result.

- **Hide Stage**:
  - Identify who shoots at me based on the directed ring (e.g., Harbor shoots at Echo).
  - Parse the shooter's fire history from round summaries. Note trends (e.g., repeating a cell, linear sweeps like 4->5->6->7).
  - Avoid cells my shooter targeted in recent rounds, and avoid the next cell in any clear sequential sweep they are executing.
  - Avoid staying in the exact same cell across consecutive rounds; actively rotate among cold, out-of-band cells (e.g., 2, 3, 8, 9).

- **Fire Stage**:
  - Identify my target (e.g., Foxtrot when I am Echo).
  - Strictly avoid firing at the same coordinate multiple times across a match if it resulted in a miss. Ensure every single shot in rounds 1 through 6 tests a unique, previously unfired cell.
  - Look at what cells other players hit or missed on my target if public info reveals it, but prioritize a diverse, distributed sweep across distinct sectors (e.g., 2, 4, 6, 8, 3, 7).
  - If a hit is scored, anticipate the target moving away from that cell and probe adjacent or distant unsearched sectors next round.