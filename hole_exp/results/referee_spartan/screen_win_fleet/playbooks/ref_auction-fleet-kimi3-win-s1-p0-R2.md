---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 1
round: 2
chars: 2124
---
I report my budget truthfully: it starts exactly at the amount stated at the top of the episode (here it was 30 — I wrongly started writing 100 mid-episode, a serious error) and it decreases only when the results list shows I actually won a lot, by exactly the price I paid. My opponent winning a lot does not touch my budget. I recompute it from the results list before every single reply and sanity-check that it matches my previous budget line.

I never place a bid larger than my remaining budget. With a small budget, cash is the binding constraint: before bidding on an early lot I check the values of the lots still to come, because spending most of my budget on a middling lot can lock me out of a later high-value one. When budget is tight, I prioritize the lots with the biggest surplus (value minus likely price), not just the biggest value.

When a lot's value to me far exceeds the current high bid, I bid aggressively enough to likely lock it up — bidding the minimum on a high-surplus lot invites someone to outbid me cheaply in the final round, and losing a +20 or +30 surplus lot to save a few units is a bad trade. A jump bid toward roughly half to two-thirds of my value still leaves large surplus if I win.

When the current high bid is at or above my value minus the minimum raise, I pass immediately. Bidding there guarantees negative or zero surplus, and there is no prize for winning the lot itself — passing is free.

On middling lots where surplus is thin, I bid the minimum raise or pass — I don't inflate the price fighting over a few units of margin.

I treat round 1 as cheap information-gathering only on low-value lots; on high-value lots I commit properly in whichever round is my last chance, because there is no round 3.

I never bid above my value for the lot, and in the final round I bid the largest amount up to (value − small margin) that my budget allows rather than only the minimum raise, since rivals have shown they will raise me on the last round.

I keep each reply short and end with both bracketed tokens — bid first, then budget — with no stray duplicated or malformed tags.