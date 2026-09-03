---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1677
---
- I track my true budget myself: I start from the stated budget (30, not an assumed 100), subtract what I've actually won and paid, and never report a budget number that contradicts what I've committed. My replies this game had wrong budget tokens; next time I compute remaining = starting budget − sum of winning bids on lots I won, before every reply.
- I never bid more than my remaining budget admits; if the minimum raise exceeds it, I pass.
- I only bid when the required bid is below the lot's value to me; otherwise I pass, no matter how cheap it feels.
- On round 1 of a lot, I bid the minimum raise (or open at the minimum) to stay in cheaply — commitments aren't binding until the lot closes, and low early bids don't inflate my cost since I only pay if I win at the end.
- On round 2 (the final round of a lot), I bid decisively: I bid the minimum raise when the gap to my value is small, but raise more aggressively — toward roughly (value + standing bid)/2 or a bit above — when the lot's value to me is far above the standing bid, since minimal raises on the last round risk losing a high-surplus lot to a rival's counter.
- I don't overpay chasing every lot: when lots I value highly cluster late in the auction, I let marginal, low-surplus lots go early so my budget is free for the big ones.
- I watch which bidder wins lots and at what prices to gauge rivals' aggression; against an aggressive rival I prefer one strong jump bid on the final round over incremental raises that invite counters.
- I keep reasoning to one or two sentences and always end my reply with exactly the required [bid:] and [budget:] tokens, on their own lines, with no trailing text.