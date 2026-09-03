---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 2132
---
Start by tabulating both value lists and marking every resource where my private value is low but the Guildmaster's published value is high — that's my giveaway list — and every resource where the reverse holds — that's my want list.

I always trade from the giveaway list into the want list. In particular, a resource cheap to me but expensive to him (like ore at 1 vs 5) is the perfect currency to buy things I value highly.

Before making any offer, I compute his net gain in his published values: (take qty × his value) − (give qty × his value). I set the claim to exactly that figure — it must be true, and it must be ≥2. I offer the minimum quantity needed to make his gain exactly 2 when I can; giving him extra (claim 3 or 4) leaves my own gain on the table.

Keep the trade small when the rates favor me: trading 1-of-mine-cheap for 1-of-his-expensive that clears his +2 bar beats dumping three units for the same return.

If a trade clears his +2 bar and profits me, I repeat it as long as my stocks hold out. A stamped-and-accepted structure doesn't wear out.

Watch my stocks of the giveaway resource. If one type runs dry, find the next resource where his value exceeds mine (even another high-value-to-me item, if the spread still profits me — e.g. giving brick at 6-to-both to receive ore at 5-to-him, 1-to-me, is fine when I'm long brick).

Be cautious about his stocks: he can't give me what he doesn't have, so when his stock of my target resource approaches zero, redirect the trade to whatever he still holds that I value.

One bracketed offer only per reply — when I bundled two give-clauses, the parser seems to have processed just one of them, which cost me value. I use exactly one [give], one [take], one [claim], and matching resource names.

Only hold if no combination of my stocks versus his clears his +2 bar while giving me positive net value. If any such positive trade exists, I take it, even for a small profit.

Each round I re-check the current stock numbers before choosing quantities — the trade I repeat may hit a stock ceiling (mine or his) and need a smaller quantity or a new resource pair.