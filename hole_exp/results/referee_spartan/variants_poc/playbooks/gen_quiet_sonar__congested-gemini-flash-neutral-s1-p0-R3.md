---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1840
---
# PLAYBOOK: Quiet Sonar (Congested)

### Rules and Mandatory Actions
- When the claim stage prompt appears, always submit the exact private result: `[claim: hit]` if hit, `[claim: miss]` if miss. Never attempt to deviate or bluff on claims.

### Hiding Strategy
- Identify and track the player targeting me (the shooter preceding me in the ring, e.g., Harbor if I am Echo). In the history line `Round X: fires E/F/G/H`, the 4th value is Harbor firing at Echo.
- Avoid default or obvious starting cells (like cell 4 or 7) that opponents habitually check early. Start with an unprompted off-center coordinate (e.g., 2, 3, 6, or 8).
- Notice opponent firing habits: if my shooter exhibits a fixed pattern (e.g., camping on 5 or alternating 5/6), strictly avoid those targeted cells and their immediate adjacencies.
- Never repeat the same hide location on consecutive rounds unless completely unpressured; avoid simple predictable toggles (e.g., toggling between 7 and 9). Distribute hides widely across safe sectors.

### Firing Strategy
- Track all cells I have fired at against my target (Foxtrot):
  - **Do not repeat missed shots**: If a shot on cell $n$ is a MISS, strictly eliminate cell $n$ from future firing options until all other plausible cells are probed. Never refire cell 5 repeatedly across multiple rounds.
  - Plan a non-repeating search sequence across all 6 rounds (e.g., probe 6 distinct cells such as 3, 7, 2, 8, 4, 6) to guarantee wide coverage.
  - If a shot results in a **HIT**, evaluate whether the target is likely to stay or flee; if fleeing, probe adjacent or alternate sectors rather than blindly refiring the exact same cell unless target behavior demonstrates stubborn camping.

### Formatting
- Submit moves immediately using the bracketed tokens `[hide: n]`, `[fire: n]`, `[claim: hit]`, or `[claim: miss]`.