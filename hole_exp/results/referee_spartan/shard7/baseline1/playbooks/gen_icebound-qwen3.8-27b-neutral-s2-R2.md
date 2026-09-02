---
game: gen_icebound
model: qwen3.8-27b
condition: neutral
seed: 2
round: 2
chars: 2865
---
# Playbook: Icebound (as North)

## Core Principle

Scouting is the dominant-safe action. It scores +3 unless raided (then 0), and it never scores negative. Raiding scores +3 only if my target scouts, but -1 if they escort or raid. Since I cannot reliably predict my target's act, **scouting is never worse than raiding when I am safe, and is strictly better when I am not.** The all-raid outcome I kept falling into (-1 per round) is a coordination trap, not an equilibrium I should seek.

## Pledge Stage

- **Always pledge scout.** It costs 1 fuel, is the cheapest option, and since my act can differ from my pledge, it locks me into nothing. Over 5 rounds this saves 5 fuel = 5 points versus pledging escort or raid every round.
- Never pledge raid or escort. The extra fuel cost buys no strategic advantage because my act is chosen independently.

## Act Stage Decision Tree

I am North. I raid East (clockwise). West raids me (clockwise).

**Default: act scout.** This gives +3 if West does not raid me, and 0 if West does. It never produces a negative score. In a symmetric game this coordinates everyone onto the +3-per-round equilibrium.

**Deviate to escort only when I expect West to raid me AND I do not expect East to act scout.**
- Signals that make me expect West to raid: West pledged raid this round, or West has raided me in the immediately preceding round(s).
- If I expect to be raided and East is likely scouting: act **raid** instead (+3 from East; West's raid against my raid costs West -1 but does not hurt me).
- If I expect to be raided and East is likely escorting or raiding: act **escort** (+2 guaranteed; better than the -1 I'd get from raiding a non-scout).

**Never act raid as a default.** Raiding is only strictly better than scouting in the narrow case where I am certain to be raided AND certain East will scout. Absent that certainty, scouting's floor of 0 beats raiding's floor of -1.

## Round-by-Round Guidance

- **Rounds 1–4:** Act scout. Build a stable +3-per-round track record. This also trains my opponents (if they are adaptive) to expect me to scout, making a late-game raid more surprising.
- **Round 5 (final):** Still act scout unless I am significantly behind and the risk of a -1 is acceptable. With 3 fuel remaining (worth 3 points), a single -1 from a failed raid costs me more than the +1 I'd gain from a successful one over just scouting. In practice, act scout in round 5 as well.

## What Went Wrong Before

I treated "they pledged scout, so they'll act scout, so I'll raid them" as a winning heuristic. But since every player had the same heuristic, everyone raided everyone and we all scored -1 per round. The fix is to recognize that the symmetric equilibrium is everyone scouting (+3 each), and my job is to stay on that equilibrium rather than try to "exploit" it in a way that breaks it for everyone.