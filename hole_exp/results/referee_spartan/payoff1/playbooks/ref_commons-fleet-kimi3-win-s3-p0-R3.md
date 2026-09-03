---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 2622
---
In future, in this game I will:

- Before first-season moves, estimate what everyone taking sustainable shares yields versus defecting, and remember 50% regrowth tolerates modest overfishing — but total claims far above regrowth crash the stock within two or three seasons, which caps what escalation can win.

- Escalate early, not late. Front-load aggression (roughly 15–20 with starting stock 100) while the stock is big; fish taken early are guaranteed, fish hoped for later depend on rivals' restraint.

- Take the sustainable share only while the stock is high and others are cooperating. The moment another boat takes consistently above share, stop subsidising them and match or slightly exceed their take.

- Recheck the frontier between "sustainable" and "racing" every season from the actual history, not my priors. This episode the rivals raced from season 1 (22, then 15/14), the stock halved each season, and the cooperative share was irrelevant by season 2.

- The consequence of others racing a low stock is not "be careful and take little" — it is "grab my fair share of what remains before they do." In season 3 I took 9 from a 31.9 stock; the rivals took ~15 each, so my restraint was pure subsidy. When stock is S and others race, take close to S/3 minus a small crash-avoidance margin, not a small absolute number.

- Compute the crash math explicitly each season: if total claims exceed S, the fishery may die. My catch should be roughly min(S/3, S minus my estimate of rivals' combined claims), where the rivals' estimate comes from their most recent actual takes, not from the sustainable-share line the prompt prints.

- Track the remaining seasons explicitly. With N seasons left, the value of conserving stock shrinks as N shrinks. Ratchet upward as the horizon closes.

- On the final season, take the largest catch the stock supports: roughly stock/3, since regrowth no longer matters. Leave nothing catchable uncaught.

- On the second-to-last season, plan backward from the final grab: leave just enough stock for a worthwhile final take and claim everything above that floor now.

- Never unilaterally conserve when the record shows others are not; that transfers catch to them. This episode's 45 versus the prior 62 shows both halves of the lesson: restraining late hurts as much as failing to escalate early.

- Never submit a low catch "for safety margin" that is below my equal split of the current stock; under racing rivals, S/3 is the floor of my safe take, not the ceiling of my greedy one.

- Keep responses short and always end with the bracketed token so the submission registers.