---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 4722
---
# Playbook: Quiet Sonar

## Core facts that shape every decision

- My claims are always truthful; there is no strategic choice at the claim stage. Just report what the referee told me.
- I have exactly one target to fire at and exactly one attacker firing at me. The rest of the players are irrelevant to my score except as information sources.
- Every player re-hides each round, so a hit this round gives no guarantee next round — but it reveals the target's style.

## Firing at my target

- **STRICT elimination: maintain a list of every cell I have fired at my target and never repeat one until all other cells are exhausted.** This is the single most important rule. In 6 rounds with 9 cells I can cover 6 distinct cells. Repeating a cell is a lost round — it converts a 6/9 search into a 3/9 or 4/9 search and that is exactly what sank my last game.
- Do **not** fire at 5. A rational hider avoids the most obvious target. This removes one cell from my search space, leaving 8 cells to choose from for my 6 rounds.
- **Order of elimination:** When choosing which cell to fire next, prefer cells that no other player has fired at yet this round. A careful hider is most likely to occupy "safe" cells that no one is shooting at. This heuristic only determines the *order* in which I work through my elimination list — it never justifies repeating a cell already on the list.
- **Exploit the public chain.** If a confirmed hit by another player reveals where my target was hiding that round (e.g., their victim's hider was exposed), fire at that cell or its neighbor next round. The target may repeat their hiding cell or drift one step.
- **Watch for target predictability.** If my target is the kind of player who always fires at the same cell (a 5-magnet, a repeat-offender), they may also hide predictably — same cell every round, or cycling through a small set. A systematic search will find them within 2–3 rounds if they are static.

## Hiding from my attacker

- Track my attacker's public fire history round by round. Identify their bias: do they repeat last round's cell, cycle through a pattern, cluster on one region?
- **Never hide at a cell my attacker has already fired at in this game.** That cell is burned; they may fire it again (repeat-players are common) and even if they don't, it is strictly less safe than an untried cell.
- **Never hide at the cell my attacker most recently fired at or is most likely to fire at next round.** If they fired 7 two rounds running, 7 is hot. If they are cycling 5→7→7→4→4, the next cell in their apparent sequence is dangerous.
- If I cannot identify a clear pattern, hide at a cell my attacker has **never** fired at. With 9 cells and at most 5 prior rounds, there is always at least one untried cell available.
- In the final round, if I am losing, hide at the single safest untried cell. If I am winning or even, I can be slightly more aggressive (hide where they are likely to fire, hoping they miss and I deny them the hit).

## What clearly did not work for me

- **Repeating my fire.** I fired at 2 three times and 8 twice across six rounds. My own "never repeat" rule was present but I overrode it with the "prefer extremes / prefer untargeted" heuristic, which kept pointing me back at the same cells. The fix: the elimination list is a hard constraint, not a suggestion. I check it before every fire decision.
- **Treating "prefer untargeted cells" as a free-floating heuristic.** Without the elimination list as a backstop, "prefer untargeted" just means "prefer the same untargeted cell I picked last round." The heuristic only works when combined with "and not one I've already tried."
- **Not leveraging the information that a 5-magnet hider avoids 5.** Harbor fired at 5 every single round. This confirmed Harbor considers 5 the obvious target and therefore hides elsewhere. My search over the 8 non-5 cells was correct in principle but undermined by my repetition problem.

## Decision procedure (run every round)

**Fire stage:**
1. List all cells I have fired at my target so far.
2. Remove 5 from consideration (unless I have exhausted everything else).
3. From the remaining untried cells, pick the one no other player has fired at this round. If all remaining cells have been targeted by someone, pick any untried cell.
4. If (impossible with 6 rounds / 8 usable cells) I have no untried cell left, only then repeat.

**Hide stage:**
1. List all cells my attacker has fired at so far this game.
2. Identify the cell they are most likely to fire at next (last cell, next in a cycle, or most frequent).
3. Pick a cell that is NOT on the "fired at" list and NOT the predicted next cell. Prefer extremes or cells far from their recent activity.