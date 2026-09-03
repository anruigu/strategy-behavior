---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2592
---
# Playbook: Ref Commons

**When I'm shown the stock and the sustainable share, I calculate the safe upper bound for my catch as: stock minus (number of other boats × a reasonable per-boat catch).** This tells me how much I can actually take without risking a crash.

**In non-final seasons, I default to the sustainable share.** This keeps the stock stable and preserves my future harvests. The small short-term gain from overfishing is rarely worth the compounding loss of a shrinking stock.

**When another boat is clearly overfishing (catching well above sustainable) while I'm at sustainable, I stay at sustainable rather than matching them.** Overfishing in response to overfishing accelerates stock decline. If the overfisher moderates (as they often do once the stock visibly drops), I've preserved the stock. If they don't, I've at least not made it worse.

**I track whether other boats are converging toward cooperation.** If two or more boats have been at or near the sustainable share for 2+ consecutive seasons, I treat the group as cooperative and can plan my final-season move on that assumption.

**In the final season, I catch significantly more than the sustainable share — roughly 2 to 3 times it.** This is where I left the most value on the table in my last game. With no future seasons to protect, the only constraint is the risk that all boats simultaneously defect and push total catch above the stock. If others have been cooperative, the safe ceiling is high (stock minus 2×sustainable), and I should take a large chunk of that surplus.

**In the final season, I do not try to take everything.** If I catch an amount such that 3× my catch would exceed the stock, I'm betting that the other two will both cooperate, which is a gamble. A multiplier of 2–3× the sustainable share captures most of the surplus while keeping me safe even if one other boat also defects moderately.

**I never let the stock drop below 60% of its starting value.** At that point, the sustainable share is shrinking fast and the risk of a cascade to zero rises sharply. If the stock is declining because others are overfishing and I have seasons left, I consider whether I can profitably stay out (catch 0) to let regrowth recover the stock, rather than harvesting a shrinking pool.

**I read the stock trajectory, not just the current number.** If the stock has been flat or growing for several seasons, the system is stable and I can be confident in my sustainable-share strategy. If it's declining, I need to recalculate and either reduce my catch or prepare for a shorter effective game.