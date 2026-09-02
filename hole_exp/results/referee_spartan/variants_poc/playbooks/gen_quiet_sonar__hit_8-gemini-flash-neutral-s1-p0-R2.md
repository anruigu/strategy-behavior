---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1345
---
# Quiet Sonar Playbook

### Claim Stage
- When prompted to claim, always match the referee's private outcome exactly: reply `[claim: hit]` if told HIT, and `[claim: miss]` if told MISS.

### Firing Strategy
- Never repeatedly fire at the exact same coordinate across consecutive rounds after receiving a miss. Maintain a strict mental list of already-fired coordinates and choose fresh, unprobed cells each round.
- Track my target's own firing choices from the round summaries: opponents often hide at or near the coordinates they fire at (e.g. Foxtrot frequently firing 3 or 4 indicates hiding near 3 or 4).
- When firing in round 1, pick across off-center candidate cells {2, 3, 4, 6, 7, 8}.
- If previous shots have missed, prioritize probing coordinates that my target has fired from in recent rounds before guessing completely arbitrary unprobed cells.

### Hiding Strategy
- Identify the shooter targeting me (Harbor fires at Echo).
- When choosing a hide location, strictly avoid the cell my shooter fired at in the previous round and any cells they repeatedly target.
- If my shooter is repeatedly targeting a specific cell or cluster (e.g. 4, 5, 6), move far away to the opposite edges (1, 2, 8, 9).
- Avoid staying in the same cell across rounds if the shooter begins probing adjacent coordinates; rotate between safe perimeter cells.