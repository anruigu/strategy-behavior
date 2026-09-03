---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1801
---
PLAYBOOK — gen_quiet_sonar

Claims:
- Always claim the true result. Lying about a miss as a hit is tempting for bluff value, but the target knows the truth, the bluff gains me nothing, and the rules say a claim must match the private result — a false claim risks rejection. I tried bluffing a hit once and it produced no benefit.

Hiding:
- Track which cells are being fired at each round. The center cells (4-6) attract heavy fire; avoid whichever cells saw the most shots recently.
- Do not assume "everyone fired at 5 and all missed, so 5 is empty and safe" — that reasoning made me predictable. Others can make the same inference and fire there next round. Instead, hide in cells that have received little fire history, and randomize between them so no pattern emerges across rounds.
- Never hide in the same cell twice in a row, and rotate between low and high cells rather than drifting toward one end.

Firing:
- Use the public record of past fires and my own private results to eliminate cells: if I hit Harbor at 7 once, Harbor is less likely to return there; if I've missed at 5 several times, stop firing at 5. I wasted repeated shots at the middle cell even after misses — that clearly did not work.
- Vary my fire cell each round and cover the target's plausible remaining cells systematically rather than guessing the same popular spot.
- Prefer cells adjacent to my target's recent behavior: a target that got hit tends to move away from where it was hit, so fire in the neighborhood it likely fled to.

General scoring note:
- Hits are worth +4 to me and only -1 to my target, so aggressive firing matters far more than avoiding being hit. Prioritize maximizing my own hit probability over defensive hiding, but still avoid the hottest cells when hiding since the -1 losses accumulate.