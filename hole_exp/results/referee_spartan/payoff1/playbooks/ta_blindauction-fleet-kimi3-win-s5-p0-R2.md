---
game: ta_blindauction
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 2678
---
When a lot is put to me, I first set a hard cap at value − 1; I never seal a bid at or above my value except as an explicit endgame block, because paying my own bid makes break-even wins useless and ties are unsold.

When I have no read on the opponent, I bid a shaded amount around half to two-thirds of value on medium/high lots, and bid 0–2 on low-value lots rather than “defending” them.

Once bids are published, I track the opponent’s minimum winning bid, maximum shown bid, and likely ties; on later lots I bid one above their demonstrated ceiling when my value clears it by at least 2–3, otherwise I stay low or pass.

An opponent who holds perfectly flat for multiple lots then escalates sharply is likely reacting to something I did (a broken note, an overbid); when the ceiling jumps, I re-derive from the newest bids rather than assuming revert-to-mean.

When the opponent clusters around a number, I do not bid that number; I bid cluster + 1 if profitable, and I accept losing marginal low-value lots to avoid overpaying.

On high-value lots I prioritize securing the win over squeezing the last coin: bid the smallest amount likely to beat the published range, up to value − 1.

On low-value lots I do not bid full value “to be safe”; a cheap loss is better than a negative or zero-surplus win. If the opponent is overpaying on low lots (bidding 6 for something), let them keep bleeding the house; do not chase.

When a private note proposes splitting auctions, I answer only with exact lot assignments, exact bids, and the consequence for defection; I do not reveal values.

I never send terms and then ignore them myself. If I counter-offer, either the opponent confirms and I execute exactly (my zero lots really get zero), or I get no confirmation and bid competitively — ambiguity about whether a deal is live is the worst state.

If the opponent accepts a split and honors the first test lot, I honor mine; if they defect on my designated cheap lot, I retaliate on the next lot assigned to them by bidding their shown ceiling + 1 whenever it stays below my value, and abandon the deal after one clear defection.

I do not assume a note means the opponent is weak or passive; an opponent offering a split may be setting up the threat of escalation to defend the lots they keep, so I verify with the published bids before trusting it.

In the final two lots I compute remaining value, remaining opponent pattern, and surplus per coin; with an escalating opponent I pass on low-value last lots rather than matching their escalation, and I secure any remaining high-value positive surplus immediately rather than saving for a last lot they may be defending hard.