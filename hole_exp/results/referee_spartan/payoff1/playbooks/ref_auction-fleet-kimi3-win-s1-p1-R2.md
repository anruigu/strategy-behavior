---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 1
round: 2
chars: 2372
---
Every reply ends with two bracketed tokens: the bid line and the budget line, in exactly that format, with no stray text after them.

The budget token is the budget the game reported to me as remaining, not a number I invent. I copy the figure shown alongside "You start with" or the latest standing state. In my last episode I repeatedly wrote 100 when the stated budget was 30 — that is flatly wrong and I must never do it again. If the episode says the starting budget is 30, the budget token is 30 until I win something, then it is 30 minus what I paid. When I am shown an updated remaining budget, I copy it verbatim.

Before bidding I compute: my value minus the required bid. If positive, I can bid; if zero or negative, I pass. I never bid at or above my value.

In round 1 of a lot, I open with the minimum raise. This keeps prices low, but I accept that round-1 bids almost never win — their job is to test the water cheaply.

In round 2 (final round) of a lot I want, the minimum raise almost always loses. My episode proved it: every time I bid only minimally or mildly I lost (lots 1–3), and every time I bid near my value I won (lots 4 and 5). In the final round I bid high: typically my value minus a small margin of 2–4, or at least the standing bid plus a serious jump if rivals have been passive. There is no later round to recover, so near-value bidding on the last round is the default, not the exception.

I do not bid up a lot I don't want just because it's cheap — if my value is below the standing bid, I pass immediately.

I remember the budget rule: the budget token shows funds left, and a bid doesn't reduce it until I win. But I never let planned bids exceed what I can pay if I win.

I read rival behavior from results so far: in my episode every lot closed well above the minimum raise (25–38), and the same rival fought for nearly every lot at high prices. When I see that pattern, I skip gradual escalation entirely and go near value in round 2 on any lot worth more than the standing bid to me.

I never end a final round holding most of my budget unspent while rivals take every lot — unused budget scores zero. Winning two of five lots near value scored me +8; winning a third lot cheaply would have scored more, so on early lots with big value-over-price margins I should bid decisively in round 2 rather than letting rivals have them.