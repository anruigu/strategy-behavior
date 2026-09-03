---
game: ref_auction
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 2042
---
When a lot’s current standing bid is below my private value, I calculate the maximum profitable bid (my value minus standing bid) and only raise if I can still expect positive surplus after winning.

When I can win a lot at a price strictly less than my private value, I prefer using the minimum legal raise (or the smallest increment that still makes me the leader) rather than shooting for the full surplus immediately.

When the standing bid is already at or above my private value, I pass.

When the next legal bid would exceed my private value, I pass even if I have budget left.

When I have multiple lots remaining in the auction, I conserve budget for lots where my private value is high relative to the estimate; I avoid spending my whole budget on a single lot unless the remaining lots are low value to me or I can guarantee positive expected return.

When my remaining budget is limited but the lot is highly valuable to me, I may go all-in only if the all-in bid still yields nonnegative surplus (value ≥ bid) and I accept losing leverage on later lots.

When I am currently the high bidder on a lot, I only increase again if another bidder outbids me and the new standing bid is still below my private value; I then typically match the minimum raise to defend the lot.

When deciding initial entry on a lot with no bids, I bid an amount that both reflects expected surplus and preserves enough budget to contest other lots where my private value is higher.

I always track my remaining budget exactly and never submit a bid that would make my stated budget inconsistent; if I make an error in accounting, I accept it as a lost mistake and correct my tracking immediately.

When a competitor’s recent winning prices suggest they are willing to pay above estimates, I don’t automatically match their behavior—my decisions stay tied to my private valuations and budget, not to others’ apparent aggression.

When ties or small increments matter, prefer the legally minimal raise to deter marginal challengers while retaining budget.