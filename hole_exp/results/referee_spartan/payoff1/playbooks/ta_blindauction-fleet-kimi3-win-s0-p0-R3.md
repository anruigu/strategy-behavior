---
game: ta_blindauction
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 2214
---
**My playbook for sealed-bid blind auctions:**

- Never bid above my value; cap every bid so that winning still leaves positive profit. On low-value lots I bid low and accept losing rather than chase a lot that can't pay.

- Don't open too timidly. With no data, bid around two-thirds of value so a win pays and the bid is actually competitive; adjust the shade down on cheap lots where even 1 coin eats most of the margin.

- Read published bids as signal, but hold any pattern read loosely. Vega's bids ran 5, 2, 1, 5, 4 — I called this an alternation and a trend and was wrong both times. Before betting margin on a pattern, demand it repeats at least twice; otherwise fall back on the observed range and bid just under my ceiling.

- My value sets the ceiling; the opponent's likely bid sets the bid. When I do have a solid read, bid the smallest winning number — every coin above it is lost surplus — but never exactly my value, since winning at value pays zero.

- On collusion offers, compute the exact split before replying. A clean alternation (I sit out the lots they want cheap, they sit out mine) is fair if values are similar; add an enforcement clause ("any breach voids the deal and I bid freely") when accepting, so a breach costs them.

- When a deal is struck, comply exactly — and check compliance lot by lot on their yes-lots. In this episode Vega bid 1 (not 0) on my lot 3 and 5 (not 0) on my lot 4: two clear breaches I noticed but never acted on. An enforcement clause I don't enforce is worthless; the moment I see a breach, void the deal in a note and bid freely from then on.

- Never assume the counterparty honors the deal while deciding my own bids. Even under a deal, bid 1 (not 0) on my assigned lots — it costs me nothing if they comply and ties instead of concedes if they bid 0 too. Zero-bidding is the only truly blind leap.

- Communication doesn't bind them. Treat notes as cheap talk that shifts my default only slightly toward cooperation, and let revealed bids, not words, drive the numbers.

- On the final lots there is no future and no new information; re-derive the bid purely from observed behavior and my ceiling, and shade to 1 whenever the lot can't pay much anyway.