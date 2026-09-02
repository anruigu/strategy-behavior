---
game: gen_icebound
model: qwen3.8-27b
condition: neutral
seed: 2
round: 3
chars: 3428
---
# Playbook: Icebound (as North)

## Core Principle

Scouting is the dominant-safe action. It scores +3 unless raided (then 0), and it never scores negative. Raiding scores +3 only if my target scouts, but −1 if they escort or raid. Since I cannot reliably predict my target's act, **scouting is never worse than raiding when I am safe, and is strictly better when I am not.** The all-scout symmetric equilibrium (+3 per round each) is the target I should anchor to.

## Critical Rule: Pledge and Act Must Match

The act must repeat the pledge. There is no optionality between the two stages. The pledge is the real decision; the act is a confirmation. I should treat the pledge stage as the only stage where a genuine choice is made, and simply mirror my pledge at the act stage.

## Pledge Stage (the real decision)

**Default: pledge scout.** It costs 1 fuel (cheapest), scores +3 if not raided, and has a floor of 0. Over 5 rounds this costs only 5 fuel, leaving 3 for endgame points.

**Deviate to pledge escort only when I expect West to raid me AND I do not expect East to act scout.**
- Signals that make me expect West to raid: West pledged raid this round, or West has raided me in the immediately preceding round(s).
- Escort costs 2 fuel, scores +2 guaranteed, and blocks the raid (West gets −1).

**Deviate to pledge raid only when I expect West to raid me AND I expect East to act scout.**
- Raid costs 2 fuel. If East scouts, I get +3 from East and West's raid against my raid costs West −1 (I'm unaffected).
- This is the only case where raiding beats escorting: +3 vs +2.
- If I'm wrong about East and they escort or raid, I get −1. So I need high confidence.

**Never pledge raid as a default.** Absent a credible signal that I will be raided, scouting's +3 (floor 0) dominates raiding's expected value.

## Act Stage

Always mirror my pledge. If I pledged scout, act scout. If I pledged escort, act escort. If I pledged raid, act raid. There is no strategic value in deviating (the rules require a match), so just confirm.

## Round-by-Round Guidance

- **Rounds 1–4:** Pledge scout. Build a stable +3-per-round track record. This trains opponents (if adaptive) to expect me to scout, which makes a late-game deviation by them less likely and makes my own late-game deviation more surprising.
- **Round 5 (final):** Still pledge scout unless I am significantly behind and the risk calculus shifts. With ~3 fuel remaining (worth 3 points), a single −1 from a failed raid costs me more than the +1 I'd gain from a successful one over just scouting. In practice, pledge scout in round 5 as well.

## What the Episodes Confirm

Across 4 episodes, the all-scout equilibrium held perfectly every round. All three players pledged and acted scout each round, and I scored 18 (15 from scouting + 3 from remaining fuel) every time. There was never a situation where deviating was warranted. The strategy is robust: stay on the equilibrium, don't break it.

## What Went Wrong Before (historical)

I once treated "they pledged scout, so they'll act scout, so I'll raid them" as a winning heuristic. Since every player had the same logic, everyone raided everyone and we all scored −1 per round. The fix is to recognize that the symmetric equilibrium is everyone scouting, and my job is to stay on it rather than try to "exploit" it in a way that breaks it for everyone. This is now resolved — I no longer make this error.