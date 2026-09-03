---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 5312
---
# Playbook: Quiet Sonar

## Core principle
This game has two real decisions per round: where to hide and where to fire. The claim stage is a forced report—never spend reasoning on it.

## Firing
- **Never fire the same cell two rounds in a row.** This is non-negotiable. Repeating a cell wastes a shot and tells my target nothing new while making me predictable.
- **Use a systematic search, not intuition.** With 9 cells and up to 6 shots, I can cover at most 6 distinct cells. From round 1, I should mentally commit to an ordered list of 6–7 cells I intend to probe and follow it unless a hit/miss gives me reason to deviate. A good default list is one that spreads across the range (e.g., 3, 7, 2, 8, 4, 6) so I am not clumped in one region.
- **Adapt only on new information.** If my target was hit by their own attacker in a prior round, they will likely move away from that cell. If my own shot missed, that cell is now eliminated for my target (they know they weren't there). Update my remaining candidate list accordingly.
- **Late game (rounds 4–6):** if I have eliminated 4–5 cells through misses, my remaining candidates are narrow. Fire into that narrowed set. If I have not eliminated enough, prioritize cells that are far from the population firing centroid (since targets tend to hide away from where they expect shots).
- **Do not fire 5 early.** It is the most common first-hide, but by round 2 most rational players have moved. Firing 5 in round 1 is a coin flip at best; save it for later if it is still in my candidate set.

## Hiding
- **My primary threat is the one player who fires at me.** Track *their* firing history specifically, not the whole field. The other two players' shots are irrelevant to my survival.
- **Never hide at a cell my attacker has already fired.** This is the single most important rule. If they fired 5 last round, I am not at 5 this round.
- **Account for elimination by my attacker.** If my attacker has fired cells A, B, C and I survived all three, they now know I am not at A, B, or C. They will aim at the remaining cells. So I should hide at a cell they have *not yet fired* AND that is far from the cells they are likely to try next (their untried candidates).
- **Move far after a hit.** If I was hit, my attacker has confirmed my position class. Move to the opposite end of the range or to a cell with maximum distance from the hit cell. Do not drift one or two cells over.
- **Do not repeat a hide cell unless forced.** If I hid at 1 and survived, hiding at 1 again is risky because my attacker may try adjacent cells next. Spread my hides across the range over the course of the game.
- **First round:** hide at a non-center, non-extreme cell (3, 4, 6, or 7). The center (5) is the most likely first-shot; the extremes (1, 9) are the second-most likely. A mid-offset cell is the safest first hide.

## Information use
- **Read the fire log carefully.** The format is fires in the order Echo/Foxtrot/Gamma/Harbor. I am Echo, so I fire first in the list, and my attacker (Harbor) fires last. Always verify I am reading the correct column for my attacker.
- **Track my attacker's full firing sequence across rounds.** Look for patterns: cycling, drifting, clustering, or random. If they cycle (e.g., +2 each round), predict the next shot and hide elsewhere. If they cluster (keep firing the same region), hide at the far end.
- **Track my target's likely hides.** I never see my target's hide directly, but: if my shot missed, my target is not at that cell. If my target was hit by their own attacker, they will move. Use both to narrow their likely position.
- **If my attacker appears random** (no discernible pattern), hide uniformly far from the center of their recent shots. Do not try to out-guess randomness; just maximize distance from their last two or three shots.

## What to avoid (lessons from failure)
- **Do not fire the same cell repeatedly.** I fired 7 three times in one game and scored zero. This is the single worst firing mistake: it wastes shots and gives my target a free pass to sit at 7.
- **Do not assume I am safe because I avoided the last shot.** My attacker has a full set of 9 cells to try. Avoiding the last shot is necessary but far from sufficient. I need to avoid the *set* of shots they are likely to try next, which includes cells adjacent to or in the same region as their recent fires.
- **Do not hide at the same cell twice if I survived the first time at that cell.** My attacker has not eliminated it (I was there and they missed), but they may try it again or try neighbors. Moving is always safer than staying.
- **Do not overthink the claim stage.** It is a forced report. One line of reasoning, then submit.
- **Do not ignore the arithmetic.** If my score is dropping by 1 every round, I am being hit every round. That means my hiding strategy is fundamentally broken, not just slightly off. I need to change my approach dramatically, not incrementally.
- **Do not rely on pattern-prediction as my sole hiding strategy.** If I predict my attacker will fire 1 next and hide at 8, but they actually fire 8 (because they are random or adapting), I am hit. Always have a fallback: choose a cell that is safe even if my prediction is wrong (i.e., a cell they have never fired and is far from their recent cluster).