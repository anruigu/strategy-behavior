---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 2887
---
# Playbook: Ref Commons

**When I'm shown the stock and the sustainable share, I calculate the safe upper bound for my catch as: stock minus (number of other boats × a reasonable per-boat catch).** This tells me how much I can actually take without risking a crash.

**In non-final seasons, I default to the sustainable share.** This keeps the stock stable and preserves my future harvests. The small short-term gain from overfishing is rarely worth the compounding loss of a shrinking stock. Confirmed: holding at sustainable for 5 straight seasons kept the stock in a narrow, stable band.

**When another boat is clearly overfishing (catching well above sustainable) while I'm at sustainable, I stay at sustainable rather than matching them.** Overfishing in response to overfishing accelerates stock decline. If the overfisher moderates (as they often do once the stock visibly drops), I've preserved the stock. If they don't, I've at least not made it worse. Confirmed: a boat took 20 vs sustainable 11 in season 1, then moderated to ~9-10 for the rest of the game.

**I track whether other boats are converging toward cooperation.** If two or more boats have been at or near the sustainable share for 2+ consecutive seasons, I treat the group as cooperative and can plan my final-season move on that assumption.

**In the final season, I catch significantly more than the sustainable share.** I calculate my target as: stock minus (2 × the highest reasonable catch I expect from the other boats). If they've been cooperative for multiple seasons, I estimate their final-season catch at 1–1.5× sustainable. My safe ceiling is then stock minus 2× that estimate. I take most of the surplus up to that ceiling. A fixed multiplier of 2–3× sustainable is too conservative when the stock is healthy and others have a long cooperative record — it leaves substantial value unclaimed.

**In the final season, I do not try to take everything.** My ceiling assumes at least one other boat may defect moderately (up to ~2× sustainable). I size my catch so that even if one other boat doubles, total catch stays below the stock. This is the risk I accept; I don't plan for both others to defect maximally.

**I never let the stock drop below 60% of its starting value.** At that point, the sustainable share is shrinking fast and the risk of a cascade to zero rises sharply. If the stock is declining because others are overfishing and I have seasons left, I consider whether I can profitably stay out (catch 0) to let regrowth recover the stock, rather than harvesting a shrinking pool.

**I read the stock trajectory, not just the current number.** If the stock has been flat or growing for several seasons, the system is stable and I can be confident in my sustainable-share strategy. If it's declining, I need to recalculate and either reduce my catch or prepare for a shorter effective game.