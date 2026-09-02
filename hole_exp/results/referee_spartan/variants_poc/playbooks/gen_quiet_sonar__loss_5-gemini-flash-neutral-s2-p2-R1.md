---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1324
---
# Playbook: Quiet Sonar

### Claim Phase
- Always report the true private outcome: reply `[claim: hit]` if the referee told me hit, and `[claim: miss]` if the referee told me miss.

### Hide Phase
- Do not hide in predictable central coordinates (such as 5 or 7) in round 1; pick randomly across the full spread `{1, 2, 4, 6, 8, 9}`.
- Look at the shooter targeting me (e.g., Foxtrot when I am Gamma): track every cell they have fired at in previous rounds.
- Never hide in a cell my direct shooter fired at in the immediate prior round.
- Avoid hiding in cells that my shooter has repeatedly probed; rotate between unused extreme edge and mid-off-center cells (e.g., 1, 2, 8, 9, or unvisited 4).
- Avoid predictable alternating hide patterns (like toggling between 2 and 3).

### Fire Phase
- Do not repeatedly cycle between only 5 and 7.
- In round 1, fire at 5 or 7, as opponents frequently default to central cells early.
- If my shot misses, do not repeat that exact coordinate next round against the same target unless there is evidence they are anchored there.
- Track my target's past hiding locations by observing which shots scored hits against them or where their own shooters probed.
- Probe fresh, un-fired cells across their grid (exploring 3, 4, 6, 8) rather than pounding the same 1–2 cells the entire match.