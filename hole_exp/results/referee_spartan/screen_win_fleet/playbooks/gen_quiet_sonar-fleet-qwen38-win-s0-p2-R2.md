---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2661
---
# Playbook: Quiet Sonar

**Firing:**
- Never fire at the same cell twice. Maintain a mental list of cells I've already shot and pick an untried cell each round.
- In the absence of information, sweep systematically through untried cells. A fixed order (e.g., 3, 6, 2, 7, 1, 8, 4, 9) guarantees full coverage within the round limit. The specific order matters less than the no-repeat rule; any fixed sequence will eventually hit.
- If I have information about where my target has been hit (their claim history reveals hits), prioritize cells adjacent to their known or suspected hiding pattern over continuing the blind sweep.
- In the final round, fire at the single untried cell with the highest probability, not a "less predictable" one. If I've eliminated most cells by process of elimination, the remaining one is the obvious choice.
- Even strong opponents (players who hit every round themselves) can be found by a patient sweep. Do not abandon the sweep for speculative guesses based on their shooting pattern — their shots reveal where *their* target is, not where *they* are.

**Hiding:**
- Each round, note which cell my shooter targeted last round. Never hide in that cell.
- Track all cells my shooter has fired at across the game and avoid them. If they've covered many cells, hide in one of the few they haven't.
- If my shooter is firing at the same cell repeatedly (a sign they are not adapting or not getting information back), I have a very wide safe zone. In this case, I can freely choose any cell except their repeated target, and I should use that freedom to pick cells that would be least useful to them if they do eventually adapt (i.e., avoid clustering near their repeated target).
- Do NOT just hide in a cell "far from their search cluster." They will expand outward. Hide in a cell they have specifically never fired at, even if it's central.
- Avoid cell 5 as a first-round hide; it is the most common default and the first cell many players try.

**Claiming:**
- Always claim exactly what the referee told me. Never claim hit on a miss or miss on a hit. The rules require the claim to match the private result, and deviating has no upside.

**What did not work (from prior episodes, still relevant):**
- Firing at the same central cell (5) almost every round wastes shots and guarantees a miss unless the target happens to be there every round.
- Firing at a "less predictable" cell in the final round instead of the highest-probability remaining cell is a mistake. Randomness doesn't help when I've already eliminated options.
- Hiding at cell 5 in round 1 when it is the most obvious default for everyone invites the first shot.