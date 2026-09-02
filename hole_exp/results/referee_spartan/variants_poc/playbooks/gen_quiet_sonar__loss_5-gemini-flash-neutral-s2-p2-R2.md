---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1635
---
# Playbook: Quiet Sonar

### Claim Phase
- Always report the true private outcome: reply `[claim: hit]` if the referee told me hit, and `[claim: miss]` if the referee told me miss.

### Hide Phase
- Do not hide in cell 2 or cell 5 in round 1; opponents frequently open by firing 5 or hunting common off-center defaults like 2. Choose unpredictable edge or asymmetric spots (e.g., 1, 7, 8, 9).
- Identify which player shoots at me (e.g., in Echo->Foxtrot->Gamma->Harbor->Echo, Foxtrot shoots at Gamma). Track their fire history.
- If my shooter scored a HIT on me in the previous round, they will very often repeat that exact coordinate or adjacent cells; move far away immediately.
- Never hide in the exact cell my shooter just fired in the prior round, nor repeat the same hide coordinate two rounds in a row.
- Avoid persistent single-cell or two-cell oscillation (e.g., repeatedly hiding at 2 and 8). Distribute hide choices across the full board {1, 3, 4, 6, 7, 8, 9}.

### Fire Phase
- In round 1, open with a shot at 5, 6, or 7, as opponents commonly default to central/semi-central cells.
- Track my target's responses and the public log:
  - If my shot scored a HIT, repeat that shot only if the opponent shows a pattern of anchoring, otherwise anticipate they will shift.
  - If my shot missed, do not repeat the exact same coordinate in consecutive rounds. Systematically probe unexplored cells.
- Observe other players' firing lines and hits to infer where players tend to hide or cluster across rounds.
- Rotate target coordinates broadly (e.g., sweeping through 3, 4, 6, 7, 8) rather than repeating 4, 5, or 6 repeatedly.