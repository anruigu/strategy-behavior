---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 5368
---
# Playbook: Quiet Sonar

## Core facts that shape every decision

- My claims are always truthful; there is no strategic choice at the claim stage. Just report what the referee told me.
- I have exactly one target to fire at and exactly one attacker firing at me. The rest of the players are irrelevant to my score except as information sources.
- Every player re-hides each round, so a hit this round gives no guarantee next round — but it reveals the target's style.

## Firing at my target

- **STRICT elimination: maintain a list of every cell I have fired at my target and never repeat one until all other cells are exhausted.** This is a hard constraint, not a suggestion. Before choosing a fire cell, I must write out my prior fires from the public record (which is in the prompt) and cross-check. In 6 rounds with 9 cells I can cover 6 distinct cells. Repeating a cell is a lost round.
- **Always read the public fire history in the prompt to determine my own prior fires.** Do not rely on memory. The record is right there. In my last game I hallucinated my own fire history in round 6 and made a choice based on it.
- **Do NOT blanket-exclude 5 from my search.** The "rational hider avoids 5" heuristic is dangerous and wrong for many players. If my target fires at 5 in one or more rounds, they are very likely a "5-magnet" — a player who picks 5 for both firing and hiding. In that case, 5 becomes my HIGHEST priority target. The correct a priori assumption is that 5 is no more or less likely than any other cell; player behavior determines probability.
- **Model your target from their fire history:**
  - If they fire the same cell every round (e.g., 5,5,5,5,5), fire at that cell immediately. They are likely hiding there too.
  - If they cycle through a small set of cells, they may hide from that same set.
  - If they fire randomly or at different cells each round, treat all cells as roughly equal probability.
- **Order of elimination when no strong signal exists:** Prefer cells that no other player has fired at yet this round. A careful hider is most likely to occupy "safe" cells that no one is shooting at. This heuristic only determines the *order* in which I work through my elimination list — it never justifies repeating a cell already on the list.
- **Exploit the public chain.** If a confirmed hit by another player reveals where a specific player was hiding that round, use that information. If it reveals my target's hiding cell, fire at that cell or its neighbor next round.

## Hiding from my attacker

- Track my attacker's public fire history round by round. Identify their bias: do they repeat last round's cell, cycle through a pattern, cluster on one region?
- **Never hide at a cell my attacker has already fired at in this game.** That cell is burned; they may fire it again and even if they don't, it is strictly less safe than an untried cell.
- **Never hide at the cell my attacker most recently fired at or is most likely to fire at next round.** If they fired 4 two rounds running, 4 is hot.
- If I cannot identify a clear pattern, hide at a cell my attacker has **never** fired at. With 9 cells and at most 5 prior rounds, there is always at least one untried cell available.
- In the final round, if I am losing, hide at the single safest untried cell. If I am winning or even, I can be slightly more aggressive.

## What clearly did not work for me

- **Blanket-excluding 5 from my search.** My target (Harbor) fired at 5 every single round and was hiding at 5 every single round. By refusing to fire at 5 I guaranteed I would never hit them. The "rational player avoids 5" assumption is a trap: the player who fires at 5 is precisely the one who will hide at 5.
- **Repeating my fires.** I fired 3 three times and 7 twice across six rounds. Only 4 distinct cells in 6 shots. The elimination rule was in my playbook but I overrode it with vague heuristics. The fix: the elimination list is checked mechanically, every round, from the public record.
- **Hallucinating my own fire history.** In round 6 I claimed my prior fires were {2, 8} when the public record showed 7, 3, 7, 3, 3. I must read the prompt, not remember.
- **Treating "prefer untargeted cells" as a free-floating heuristic.** Without the elimination list as a backstop, it just means "prefer the same untargeted cell I picked last round." The heuristic only works combined with "and not one I've already tried."

## Decision procedure (run every round)

**Fire stage:**
1. Read the public fire record from the prompt. List every cell I have fired at my target so far. (Do not use memory.)
2. Check my target's fire pattern. If they fire at the same cell repeatedly, put that cell FIRST in my priority list.
3. From the cells I have NOT yet fired at, pick the highest-priority one. Priority order: (a) my target's repeated fire cell, (b) a cell no other player has fired at this round, (c) any other untried cell.
4. If (impossible with 6 rounds / 9 cells) I have no untried cell left, only then repeat.

**Hide stage:**
1. List all cells my attacker has fired at so far this game (from the public record).
2. Identify the cell they are most likely to fire at next (last cell, next in a cycle, or most frequent).
3. Pick a cell that is NOT on the "fired at" list and NOT the predicted next cell. Prefer extremes or cells far from their recent activity.