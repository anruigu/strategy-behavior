---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2369
---
# Playbook: Quiet Sonar

**On claiming: always tell the truth.** The rules require my claim to match the private result. When the referee tells me I hit, I claim hit. When I miss, I claim miss. Lying gains nothing—the referee either rejects it or it simply scores zero, and I waste the round. Do not attempt to "bluff" or "manipulate" through false claims.

**On hiding: never repeat a position two rounds in a row.** If I hid at cell X last round and my shooter (the player who targets me) fired at X or claimed a hit near X, I must move. When I notice my shooter has probed a specific cell one or more times, I avoid that cell and its neighbors. In the absence of information, pick a cell at the edge of the board (1, 2, 8, or 9) rather than the center, because center cells are the default guess for all players.

**On hiding in later rounds: use the public fire history.** If a cell has been fired at multiple times across rounds, opponents are converging on it. Hide away from the cluster of recent fire coordinates. If the hot zone is around 5 and 7, hide at 1, 2, or 9.

**On firing: do not anchor to a single cell.** Firing at the same target cell every round is exploitable—if my target learns my pattern, they can simply avoid it. Instead: in early rounds, fire at the cell my target most likely chose given the public history (center cells early, edges later). In middle and late rounds, fire at the cell my target has NOT recently been probed by others, since they may be hiding there feeling safe. Alternate between 2–3 candidate cells rather than locking in.

**On the first round specifically:** Fire at 5 (the most likely default hide) and hide at 1 or 9 (least likely to be guessed). This gives me a decent chance of scoring while staying safe.

**On tracking my shooter:** Every round, note where the player shooting at me fired. If they fire at the same cell two rounds in a row, they are either frustrated or have a pattern—either way, I stay away from that cell. If they shift, they may have received a miss and are probing; I should not hide adjacent to their new probe.

**On the final round:** I still hide to protect my remaining points (a hit against me costs me 1 point, which can swing a close score). I still fire to try for +4. Do not treat the final round as "anything goes"—the same rules apply and a single point can decide the outcome.