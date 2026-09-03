---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 7
round: 3
chars: 4502
---
When the first season is put to me and I know nothing about the other boats, I take slightly above the posted sustainable share, about 1.25–1.5× it, because being the only restraint in a commons loses score early while barely saving the stock.

Before every submission I recompute the exact pool dynamics: next stock is roughly 1.5× what remains after all catches, capped at carrying capacity and dead at zero; the posted "sustainable share" is only the equal split that keeps the cap full, not a fairness rule I owe anyone.

When season results are revealed, I track each boat individually rather than reacting to the headline stock: an escalating defector is different from a boat that opened hot and then steps down, and I update each boat's likely next catch from its trend.

I do not project worst-case greed onto boats that are actually moderating: in my episode both rivals' catches fell season over season (22→14→12, 11→17.5→15), and assuming continued aggression left me taking a flat 15 while the pool shrank, when sharper earlier grabs were safe.

When the stock is falling faster than I predicted despite my own steady take, I recompute what the implied rival total must be and compare it to the stock trajectory; if total harvest is running above the collapse rate, I take my cut sooner rather than waiting for a "penultimate" signal that arrives with only scraps left.

The gravest error is grabbing at the end but leaving a buffer: after taking 7.4 of 7.5 I left 0.1, which regrows to a meaningless 0.15 — when I decide the fishery is ending or rivals will take the rest, I take essentially the entire stock, since a tiny remnant is worth nothing and is just lost fish.

If total landed is near or below what lets the stock recover, I stay near the sustainable share; if others crashed the stock, I do not stay virtuous at a collapsed share, because low absolute takes after a crash leave me behind forever while defectors convert my restraint into their fish.

When the stock has already fallen and sustainable shares become tiny, I stop treating "sustainable share" as my target and instead solve backwards: choose the largest take that, after plausible (not worst-case) rival catches, leaves next season's stock comfortably above zero and still worth harvesting.

When I am behind on cumulative score with several seasons left, I raise catch in steps rather than all at once, closing part of the gap while holding total expected harvest under the collapse threshold; I avoid jumps large enough to make cautious rivals panic.

When rivals demonstrate restraint for a full season, I reciprocate for one season by taking roughly the group norm, but only if that norm keeps regrowth positive; restraint is a tool to buy future stock, not a moral default.

When estimating collapse risk, I subtract plausible rival catches first, then set mine so post-season stock times regrowth still leaves at least one meaningful season; if even a small personal take cannot do that, I treat the commons as already ending and extract everything the same season rather than dribbling out one more moderate take.

I respect the arithmetic ceiling: with 50% regrowth, a stock below ~half of capacity cannot support three boats at the original posted share, so once the stock halves I cut proportionally or commit to extraction — a mid-collapse "my usual take" is what destroyed this fishery.

When the penultimate season arrives, I shift from preserving the fishery to positioning for extraction: I take enough that, even under aggressive rivals, the final season still contains a worthwhile pool for me to drain — but I check whether rivals have already made the final season empty and, if so, treat the current season as final.

When the final season arrives, cooperation ends; I submit essentially the whole remaining stock, because nothing after the last season pays for restraint and any fish left is pure lost score.

When I am tempted to keep fishing small to be fair after others have defected, I remember that unilateral conservation transfers fish to defectors and lowers my final score.

When I am tempted to grab everything early, I remember that killing the stock early also caps my own total if others back off, so I keep enough alive only while at least one future round still matters.

When writing the reply, I keep visible reasoning to one short cover sentence, never reveal my full model, and always end with exactly the required bracket token, since only a parseable submission scores.