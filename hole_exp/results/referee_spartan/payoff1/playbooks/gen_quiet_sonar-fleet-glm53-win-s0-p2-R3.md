---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 2504
---
PLAYBOOK — gen_quiet_sonar

Claims:
- Always claim the true result. A false claim risks rejection, gains nothing, and the rules say a claim must match the private result. I claimed honestly all six rounds this episode with zero issues — keep this permanently.

Hiding:
- Track which cells my one fixed attacker fires at each round. Only THAT player's shots threaten me; other players' fires are noise for defense. Identify my attacker from the fire chain (each player's target is fixed) and track only their history.
- Avoid my attacker's recently fired cells and repeat cells. In this episode Harbor fired 9, 2, 2 at me — staying off those worked; I was never hit.
- Rotate hides; never hide in the same cell twice in a row. I hid at 2 twice and 8 twice in past episodes — unpunished luck, but unnecessary risk.
- Prefer cold cells (little or no fire history at me). Do not assume "a cell was fired at and missed, so it's safe" — others may reason the same way.
- Hiding is secondary: a hit against me costs only -1. Spend most thinking on firing.

Firing:
- This is the big lever: hits are +4 to me. I scored +11 this episode with three hits (2, 8, 9 at Harbor) — the system works, refine it.
- Never re-fire a cell I've missed at my fixed target. Keep a running elimination list. Each miss kills that cell for me permanently unless something changes.
- Work the extremes and cold cells: my target avoids hot, heavily-fired cells too. Harbor's hides were 2, 8, 9 — all edges, never mid. Fire 1, 2, 8, 9 early and often; de-prioritize 4-6 unless elimination forces it.
- After several misses, escalate to the extreme cells even if they seem "too obvious" — this episode the round-6 fire at 9 connected precisely because I'd ignored the far corner too long.
- Plan coverage across the 6 rounds: roughly one fresh plausible cell per round, ordered edges-first (e.g. 2, 8, 1, 9, then middles). Never fire the same cell twice in a row.
- Use my own private hit/miss results across rounds — they are exact information about my target's cell that round, and consecutive misses at a cell make it nearly dead for that opponent's habits.

General scoring note:
- Offense dominates: +4 per hit vs -1 per hit taken. Prioritize firing decisions; hide quickly in cold cells off my attacker's history.
- The fixed fire chain means every player has exactly one attacker and one target. My defense depends only on my attacker's pattern; my offense depends only on my target's pattern. Track both separately and clearly.