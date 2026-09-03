---
game: ref_auction
model: haiku
condition: win
seed: 7
round: 2
chars: 2309
---
# Playbook for Ref_Auction

When I see a lot's value to me and the current standing bid, I calculate the profit margin (value minus bid) and use that to guide my aggressiveness.

When I'm opening bidding on a lot with no bids yet, I place a modest opening bid rather than passing, since I have private information about the lot's value that others don't.

When the profit margin is substantial (value is significantly higher than the current bid), I bid to stay competitive rather than pass, even if it means raising the bid.

When deciding how much to raise, I use the minimum raise threshold as a floor, not my actual bid. I can and should bid higher than the minimum to be more competitive, especially when the value-to-bid ratio is very favorable.

When I'm in round 2 of a lot and the value is strong, I continue bidding aggressively to secure the lot rather than holding back.

When tracking my budget across the auction, I must keep accurate track of what I've spent and what I have remaining. I should not assume or guess at my budget—I should calculate it precisely from my actual bids. This is critical because my budget display showed an implausibly high number (199,964) that did not match the actual game state.

I should bid to win lots where the value exceeds the standing bid by a meaningful margin, because winning is how I accumulate points. However, I need to distinguish between a truly favorable margin and a marginal one—even with budget to spare, bidding to win a lot worth 11 when I bid 12 gives me only 1 point of profit, which is not worth aggressive play.

When the profit margin is very thin (1 point or less), I should consider passing rather than bidding, especially in later rounds. A thin margin means I'm overpaying relative to my private valuation, which erodes my score.

I should be more conservative on final lots when the margin is slim. Winning with minimal profit is better than losing, but I should not bid more aggressively on final lots if the underlying margin doesn't justify it—the fact that it's the last lot doesn't change the math.

When I notice my budget calculations seem inconsistent with the game's display, I should trust the game's stated budget rather than my own recalculation, as the game has authoritative information about what I've actually spent.