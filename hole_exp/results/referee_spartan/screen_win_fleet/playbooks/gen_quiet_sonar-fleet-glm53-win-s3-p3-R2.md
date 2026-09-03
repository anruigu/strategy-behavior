---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 1920
---
- When hiding, avoid the center and repeated patterns. Shots cluster on low cells (1, 2) and mid cells (4, 6); edges like 8 and 9 drew almost no fire. Randomize over the full 1–9 range, weighting untargeted edges.
- Track the full history of fires every round. Cells fired repeatedly (1 and 2 were fired at round after round) are the ones to avoid; cells never aimed at are the safest hides.
- When firing, use elimination: every public miss on my target rules out that cell for that round only, but repeated misses at the same cell mean my target is not settling there — stop re-firing it. I fired 2 at Echo in rounds 2, 5 and 6 and it never landed; re-firing a known-missing cell is a wasted round.
- Do a systematic sweep at my target instead: one fresh, untried cell each round (e.g. 1, then 4, then 6, then 8, then 9), never repeating until the range is exhausted. Six rounds give six distinct guesses and a real chance at the +4.
- Use the public record: any shooter's confirmed hit tells me where that target likes to hide; if my target was ever hit at cell n, fire at or near n next round. This round nobody ever claimed a hit, which itself is information — the whole table was firing at cells nobody was hiding in, so untried cells were likely correct targets.
- When claiming, report the true result immediately. The claim is validated by the referee, so lying isn't available and deliberation is wasted.
- My only positive points come from my own shot landing; my only losses come from being hit (-1). Defensive hiding kept me at zero, but zero fired rounds meant zero scoring — the sweep strategy is what converts safe play into actual points.
- Watch for the anti-pattern that trapped me this game: defaulting to a small set of "safe-looking" fire cells (2 over and over) while telling myself I was "breaking the pattern." Check my own fire history each round and refuse to reuse a cell that already missed.