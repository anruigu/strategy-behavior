---
game: gen_icebound
model: claude
condition: neutral
seed: 2
round: 2
chars: 3760
---
# ICEBOUND PLAYBOOK (North seat, but seat-agnostic)

**Record so far: 4 games, 4 × 18.0 — the theoretical ceiling every time, by scouting all ten decisions.** The line works. Do not get clever and break it.

**Before round 1: compute the ceiling.**
- Max points = (best points-per-fuel mission repeated every round) + (leftover fuel × 1). With 8 fuel / 5 rounds / scout = 3 pts for 1 fuel, that's 5×3 + 3 = 18, and unanimous scouting hits it exactly.
- Note the key implication: **the cooperative all-scout line IS my maximum.** There is no outcome better than 18 for me. Raiding a scout nets +3 stolen but costs 2 fuel (net +1 vs. scouting the same round, and only if the target actually scouts, and only if nobody retaliates for the remaining rounds). Any deviation is at best marginal and at worst catastrophic. When my ceiling is already reachable through honest play, defection has no upside worth its variance.
- Re-derive these numbers if the manifest changes costs, payoffs, round count, or starting fuel. If in some variant raid nets clearly more than the honest ceiling even after retaliation, reconsider — but check the arithmetic explicitly before believing it.

**Pledge stage.**
- Default: pledge scout. Cheapest pledge, highest payoff, keeps my fuel curve comfortably ahead of rounds remaining.
- Check fuel first: I need at least 1 fuel per remaining round to keep scouting. Starting 8 fuel / 5 rounds leaves 3 slack, which is worth 3 points at the end — so never spend the slack unless the spend buys back more than 1 point per fuel. Escort (2 fuel, 2 pts) is a net -1 versus an unraided scout; it only pays when it converts a 0 into a 2, i.e. against an actual expected raid.
- Pledge escort only when the player upstream of me (whose raid arrow points at me) has actually raided or pledged raid. One instance of upstream raiding is enough; guessing without evidence just burns fuel.
- Pledge raid essentially never. It costs 2 fuel, is -1 against an escort or a raider, and against unanimous scouts it nets me only +1 point over scouting while inviting escorts and raids for every remaining round. It is not worth it even in round 5, because scout's 3 > raid's expected value once the target might have escorted.

**Act stage.**
- The act must repeat the pledge — the referee only checks the word is legal, but deviating is visible to everyone afterward and destroys the equilibrium that pays me 18.
- Read the public pledges before acting anyway. If all pledges are scout: act scout, no exceptions, including the final round. Every episode so far confirms opponents honor their pledges under this arrangement.
- If someone upstream pledged raid: my scout will score 0. I cannot switch to escort at the act stage without having pledged and paid for it, so I take the hit and adjust next round's *pledge* to escort.
- If my downstream pledged escort: never act raid into it (-1).

**Reading the table.**
- Opponents in the games I've seen open with scout and hold it all five rounds. My prior for round 1 is "everyone scouts"; act accordingly and only revise on observed behavior.
- Last round has no shadow of the future, so it's the classic defection point — but here the arithmetic still says scout (3 for 1 fuel) beats raid (net +1 at best, -1 at worst). No end-game deviation.
- Track each player's pledge/act pairs. A player who pledged one thing and acted another is the only real signal that the honest equilibrium has broken; only then do I start spending fuel on escorts.

**Tone of my one-line reasoning.**
- State the arithmetic (ceiling, points-per-fuel, fuel remaining vs. rounds remaining) and the observed table state. Keep it to one sentence, then the bracketed token, correctly formatted: `[pledge: scout]` / `[act: scout]`.