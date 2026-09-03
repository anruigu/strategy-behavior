---
game: hx_quota_checker
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 3259
---
- Parse the exact mechanics first: per-boat quota, sustainable share, regrowth rate, pair caps, what drives the enforcer (Coop), and whether final-season landings are capped by remaining stock.
- THE CRITICAL REVISION: the enforcer's trigger is the published sustainable share, not the nominal quota. I landed 9 in season 1, the log shows everyone at 8.3–8.7 (all under the quota of 9, all over the share of ~8.3), and Coop jumped to 18/season from season 2 onward and never came back. The flavor text saying "landing more than the share is within the quota and is not a breach" was bait. The rule that binds is: land at or just under the share, or the hammer falls.
- Never land above the published share while the fishery is healthy. Round DOWN (share 8.3 → land 8), not up. One season of +1 over share cost the entire fishery: collapse play scored me 35.3, while six seasons at ~8 each would have scored ~48–50. Restraint at healthy stock is the greedy play, not the generous one.
- Punishment, once triggered, looks permanent. Coop took 18 every season after the breach even though every note said "fishing my share" and my landings dropped to ~5–7. Notes do not reset an enforcer; only landings might, and only before the first breach. So the whole game is won or lost in season 1: land the share immediately.
- If cooperation holds (everyone at or under share, stock near 100), stay at share every season. Total sustainable take ≈ stock × regrowth fraction; at 100 with 50% regrowth that is ~50/season across 4 boats, matching the published share of 8.3. The game is telling me the equilibrium — sit on it.
- Watch published landings every season and label each row before reasoning from it. Identify who is the enforcer, who are rivals, and exactly which landing (mine included) preceded any punishment. I previously conflated Coop's retaliation with a rival racing; attribute rows first.
- Test nothing by pushing. My old plan of "push a little, observe, then decide" is wrong when the enforcer's punishment is permanent and catastrophic. The first probe IS the breach. Default to under-share and only exceed it if the rules or observed evidence concretely prove it is safe — one ambiguous sentence of flavor text is not proof.
- Keep notes identical to the fleet's cooperative signal ("fishing my share") and consistent with my actual landing; a mismatch invites retaliation and costs nothing to avoid.
- If the collapse has already started and is driven by something outside my control (enforcer locked at 18), then and only then switch to cash-out: restraint that cannot flip the trajectory just scores less. From the moment doom is locked in, every season is effectively a final season — take the maximum safe landing immediately, not one season later.
- Compute min(quota, published share if enforcer active, remaining stock, pair-cap headroom) explicitly before every landing.
- Final season: land the maximum available (I took the full remaining 3.4 — correct). Nothing carries over.
- Score is only landed fish. The choice each season is "small harvest × many seasons" versus "large harvest × few," and with an enforcer who ends the game on any breach, small-and-many wins decisively. Cooperate from season 1, season 1 is not a probing season.