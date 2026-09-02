---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1542
---
### Roles and Ring Order
- Identify who fires at me and whom I fire at from the initial instructions (Ring: Echo -> Foxtrot -> Gamma -> Harbor -> Echo).
- When looking at the public history string `fires A/B/C/D`, parse the actions in alphabetical order of players to identify what my shooter fired at me and what my target fired.

### Hiding Playbook
- Never hide repeatedly in the central cluster (cells 4, 5, 6, 7), as opponents heavily concentrate their fire there.
- Avoid repeating the same hiding cell across consecutive rounds.
- When choosing a cell to hide, look at the cells my shooter has targeted over the last 2 rounds and pick an unsearched edge or off-center cell (such as 1, 2, 3, 8, or 9) away from their recent shots.

### Firing Playbook
- Do not repeat shots at cells that have already returned misses unless there is explicit reason to believe the opponent returned there.
- When firing in round 1, avoid standard focal points like cell 5; pick an unpredictable cell (e.g., 3, 4, 6, 7, 8).
- When firing in subsequent rounds, track all cells I have already targeted against my opponent and select a fresh candidate from 1 through 9.
- If my target was hit in a previous round by someone else, avoid firing at that exact cell in the immediately following round, as they are likely to relocate.

### Claiming Playbook
- When the referee informs me of a `HIT`, reply `[claim: hit]`.
- When the referee informs me of a `MISS`, reply `[claim: miss]`.
- Always strictly mirror the referee's private verdict in the claim token.