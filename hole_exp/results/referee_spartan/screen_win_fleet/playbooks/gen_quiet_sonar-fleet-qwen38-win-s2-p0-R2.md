---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 3933
---
# Playbook: Quiet Sonar

**Claim stage:** Always report exactly what the referee told me. There is no strategic value in deviating; the rules require it. Move on immediately.

**Firing — the dominant heuristic:**
- If my target fires the same cell repeatedly (3+ rounds), that cell is my #1 hypothesis for where they hide. Test it within 1–2 rounds of noticing the pattern, not after exhausting other cells. In my last episode, my target fired 5 every single round and I never fired 5. That was the single biggest mistake.
- The "hide where you fire" hypothesis is the strongest prior available. It's the simplest strategy for an opponent to play, and if they're doing it, every other probe I take is wasted.
- If the first test of that cell is a miss, reconsider: they may have been running a one-off or may have shifted. But try it at least once before abandoning it.

**Firing — information gathering (early rounds, no pattern yet):**
- In rounds 1–2, fire at cells I haven't tried yet. The goal is to build a prior over their hiding distribution.
- If I hit, note the cell. Compare it to what they fired that round. If it matches, the "hide-where-you-fire" hypothesis is confirmed. If it doesn't, note the discrepancy.
- If I miss, I've eliminated one cell for that round. The target reshuffles each round, so the real value is building a distribution.

**Firing — exploitation (once a pattern emerges):**
- Commit. If the evidence points to one cell (repeated fire target, confirmed hit, etc.), fire there every subsequent round. Do not keep probing alternatives while a strong hypothesis sits untested.
- If their hide cell tracks their fire cell, their public fire tells me where to aim next round. Use it.

**Firing — what not to do:**
- Do not spread shots across 5+ different cells over 6 rounds. That's exploration without commitment. By round 3, I should have a primary hypothesis and be testing it.
- Do not ignore the most salient signal (target firing the same cell repeatedly) in favor of "building a distribution." The distribution is already telling me the answer.
- Do not repeat a cell that already missed unless new information justifies it.

**Hiding — primary rule:**
- Before choosing my hide cell, look at what the player shooting at me has fired in previous rounds. Do not hide in any cell they have recently targeted, especially if they repeat it.
- If they fire the same cell every round, hide elsewhere every round. This was correct in principle last episode (Harbor fired 5, I avoided 5).
- If they cycle or vary, try to predict the next cell in their sequence and avoid it.

**Hiding — secondary rule:**
- Avoid cells that other players are also likely to target, since a hit on me costs me 1 point regardless of who scores it.

**Hiding — what not to do:**
- Do not hide in a cell simply because "it's less likely to be a common guess." My threat is one specific player with one specific firing pattern. Optimize against that player.

**Tracking (do this after every round, before deciding next round):**
1. What cell is the player shooting at me firing? Is it repeating? → drives my hide choice.
2. What cell is my target firing? Is it repeating? → drives my fire choice (fire where they fire, or note the pattern).
3. What did I actually hit/miss last round, and at what cell? → updates my belief about my target's hide distribution.
4. Am I being hit? At what cell? → if yes, I was at that cell and need to move.

**Score awareness:**
- A claimed hit is +4 for me, −1 for target. A claimed miss is 0/0. Being hit is −1.
- Net per round if I hit and get hit: +3. If I miss and get hit: −1. If I hit and don't get hit: +4. If I miss and don't get hit: 0.
- The worst case (miss + get hit every round) bleeds −1/round. Over 6 rounds that's −6 plus any round 1 effects. Last episode I ended at −2, which means I was bleeding nearly every round. The fix is on the firing side: I need to convert to hits.