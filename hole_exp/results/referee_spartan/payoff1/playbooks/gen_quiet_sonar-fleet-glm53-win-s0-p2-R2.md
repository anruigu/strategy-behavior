---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2829
---
PLAYBOOK — gen_quiet_sonar

Claims:
- Always claim the true result. A false claim risks rejection, gains nothing (the target knows the truth), and the rules say a claim must match the private result. I claimed honestly all six rounds and had no issues — keep this.

Hiding:
- Track which cells are being fired at each round. The center cells (4-6) attract heavy fire; avoid whichever cells saw the most shots recently. This worked: I was never hit in any round by hiding in cold cells (2, 2, then 8, 8).
- Do not assume "everyone fired at 5 and all missed, so 5 is empty and safe" — others can make the same inference and fire there next round. Hide in cells with little fire history.
- Never hide in the same cell twice in a row. I violated this in rounds 1-2 (both at 2) and 5-6 (both at 8) — it happened to go unpunished, but it's an unnecessary risk. Rotate between low and high cold cells.
- Note that shots at ME come from exactly one player (my fixed attacker). Track only THAT player's fires when choosing hides — the other fires are noise for defense. In this episode Harbor fired at Echo, not me, so my hide choices mattered less than I thought; check whose shots threaten me before spending effort on hiding.

Firing:
- This is where I failed: six rounds, zero hits, +0 points. My fires (5, 7, 7?, 4) drifted around with no system. Fix this first next time.
- Systematically eliminate against my one fixed target. Keep a running list of every cell I have fired at them and every miss. Never repeat a cell I've missed at unless the target has an obvious reason to return. I re-fired 7 at Harbor after an early miss — pure waste.
- With 9 cells and 6 rounds, plan coverage: pick a priority order across plausible cells and work through it, rather than re-guessing the "popular" spot each round.
- If the public record shows other players' misses at my target — it doesn't, since only I fire at my target — but do use ALL my own private results across rounds. Every miss eliminates that cell for that round; consecutive misses at the same cell make that cell nearly dead.
- Assume my target is also avoiding hot cells (the cells that get fired every round, like the center). Direct more fire at cold cells (1, 2, 8, 9 in this episode) rather than the mid-range. I fired 4, 5, 6, 7 repeatedly — all mid — and never hit; Harbor was likely in the extremes.
- Vary my fire cell every round; never fire the same cell twice in a row regardless of reasoning.

General scoring note:
- Hits are worth +4 to me and only -1 to my target, so aggressive, systematic firing matters far more than defensive hiding. With zero hits I scored zero — hiding perfectly is worthless if I never connect. Spend most of my thinking on target elimination.
- Still avoid the hottest cells when hiding, since -1 losses accumulate, but keep it quick.