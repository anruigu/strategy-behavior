---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2314
---
PLAYBOOK

- Before anything else, fix my budget bookkeeping. Budget = 30 minus sum of winning bids I've actually paid so far, nothing else. Recompute it at every decision and state it correctly in the [budget:] token. Crucially: never bid more than my remaining budget, even in the final round of a final lot — an over-budget bid is wasted or invalid (I did this on lot 5 and it bought nothing).

- In round 1 of a lot, bid the minimum raise when my value is above the standing bid. Cheap entry preserves surplus if rivals don't contest, and round 2 is where the contest is decided.

- In round 2, my bid is the last word. When the standing high bid B is below my value V, I must outbid it — but "decisively" does not mean "bid half my budget." A raise of roughly 1.5–2× the minimum raise above B is usually enough; jumping from 16 to 25 on lot 2 burned most of my budget on surplus I didn't need to give away, and it priced me out of two later lots worth 36 and 33 to me. Bid just enough to deter, capped under V and under my remaining budget.

- Hard cap: never bid at or above my private value for the lot. If the required raise already equals or exceeds my value, pass. Surplus of zero or negative is not worth locking up budget.

- Reserve rule, sharpened by this episode: with 5 lots and budget 30, an early win at price P leaves 30 − P for everything after. Before making a large round-2 bid on lot 1–2, ask what typical later lots are worth (often 30–45); if my bid would leave me unable to make even a minimum contest on two more lots, hold it down or walk away. My value edge on a single lot is rarely worth more than staying live for three.

- Pass immediately when my value is below the standing bid or the required raise exceeds my remaining budget. A lot I can't afford is a lot I don't own — don't bid token amounts at it (the illegal over-budget bid on lot 5 taught this).

- When I open round 1 with no bids and my value is well above the estimate, still open at the minimum. The round-1 amount only sets my downside if nobody raises; round 2 decides the outcome.

- Track rivals loosely: bidder behavior here showed rivals escalate in round 2 to roughly 1.5–2× the estimate, not to full value. So my round-2 target price should be anchored just above that escalation range, not near my own value.