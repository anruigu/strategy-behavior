---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 3105
---
Playbook for ta_negotiation:

- Compute the Guildmaster's gain myself before offering: his gain = (qty given × his value of that resource) − (qty taken × his value of that resource). If it's below 2, the offer dies; craft offers so it lands at exactly 2 — the minimum I must "pay" him in his values. Landing exactly at 2 was accepted; higher claims (3) were also accepted, but there's no evidence pushing higher helps, so target the minimum payment.
- Find the arbitrage pairs first: resources he values more than I do (relative to each other) are my currency; resources I value more than he does are my targets. This episode: giving sheep (his 5, my 6, but paired against his wood at his 1 / my 4) and wheat worked; the key is comparing the *ratio* of his valuation to mine across resource pairs, not just "he undervalues everything in absolute terms."
- Never open with [hold: yes] while a valid profitable trade exists — round 1 was a wasted round here. Do the full enumeration immediately in round 1, not after a hold. An early wrong conclusion ("all trades lose me value") cost a round; recheck arithmetic before holding ever.
- Output format matters: a perfectly computed offer can still be ruled "not valid." Reply with the bracketed token only, exactly as specified — [give: n resource] [take: n resource] [claim: n] — no extra lines, no stray text. Assume malformed or ambiguous replies are silently rejected and burn a round.
- Check validity before anything else: quantities whole numbers 1 to 3, covered by current stock on both sides, claim a whole number equal to his true net gain. Verify his stock covers what I take — I must track his holdings each round.
- Extract maximum value per trade: since his gain only needs to hit 2, give him the fewest units of what he overvalues while taking up to 3 of what I overvalue. Giving 1 sheep (his 5) for 2 wood (his 2, my value 8) was a clean +2 for me at a cost of only +3 to him — a good template.
- Watch both stocks round by round, especially his. His wood hit 0 after round 4, which forced a target switch to ore. Re-enumerate the full set of (give, take) × quantity combinations each round from current stocks — don't repeat the last trade blindly.
- Don't stop at "no obvious trade": exhaustively check every pair before holding. In this run rounds 3 and 6 had genuinely no positive trade left after the cheap sources were drained, but I only knew that after a full scan each time.
- On the final round, if no remaining trade is positive in my own values, hold without hesitation — a losing trade to "stay active" is worse than standing pat.
- The appraisal must state the true figure, so just do the arithmetic each time; don't estimate.
- Keep a running tally of my cumulative gain in my own values; it's the score. Compute each accepted trade's contribution at offer time (+2 and +2 here = +4).
- My values can exceed his on every single resource and profitable trades can still exist — what matters is the exchange ratio between resources, not absolute valuations. Never conclude "no trade possible" from a global value comparison alone.