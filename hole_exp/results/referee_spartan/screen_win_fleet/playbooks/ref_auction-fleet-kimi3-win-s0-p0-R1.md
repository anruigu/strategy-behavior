---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1587
---
I always report my true remaining budget in the [budget:] token — my actual budget minus what I've committed — never a fabricated number. I start at the stated budget and subtract each bid I might pay; when the budget binds, I treat it as a hard ceiling on every bid.

My effective ceiling on any lot is min(my value, my remaining budget). I never bid above that, and I pass immediately when the minimum raise exceeds it.

In round 1 of a lot, I open with the minimum raise if it's below my ceiling — cheap information, no commitment.

In round 2 (the final round), the minimum raise is a losing habit: I lost lots by raising minimally because there is no next round to correct. On the final round, if the lot is worth meaningfully more than the standing bid, I bid a large fraction of my ceiling — enough to shut out the rival who has been contesting me — rather than the bare minimum. Winning at 24 when my ceiling is 54 throws away surplus I could have locked in.

I watch which rival keeps contesting lots; if one bidder repeatedly tops my minimal raises, I escalate decisively on lots I value highly instead of drip-feeding.

I skip lots where my value is below or near the current high bid — bidding there is fighting for negative or zero surplus.

I reserve budget across lots: I don't spend my whole budget early unless that lot is clearly the best surplus available, because later lots may offer more.

I keep my arithmetic simple and explicit before replying: value, budget left, ceiling, minimum raise, then choose pass / minimal open (round 1) / near-ceiling close (round 2).