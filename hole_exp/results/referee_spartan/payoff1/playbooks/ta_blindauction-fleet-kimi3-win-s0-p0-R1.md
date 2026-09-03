---
game: ta_blindauction
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 2150
---
**My playbook for sealed-bid blind auctions:**

- Never bid above my value; cap every bid so that winning still leaves positive profit. On low-value lots I bid low and accept losing rather than chase a lot that can't pay.

- Early in the match, before I have data on my opponent, I bid roughly half my value — enough to be competitive, low enough to keep margin if I win.

- After each lot I read the published bids as a signal. If the opponent shows a stable range (e.g., 4–5), I bid at or just above the top of that range when my value comfortably exceeds it, and concede the lot when it doesn't.

- I track patterns: if the opponent alternates high/low, I aim my bids to land just above their likely low bids and save coins on their likely high bids.

- When a collusion offer arrives on the private note line, I verify its actual value before agreeing. In a first-price auction where the winner pays their own bid, "we each win two lots for one coin" only pays if we also control lots 1 and 2 — an opponent who skips my lots while I skip theirs can still outbid me on the contested ones. I compute the exact split before replying, and I do not skip lots unless the deal genuinely nets me more than contesting them.

- If I make a deal, I state an enforcement condition in the note ("any breach ends it") and I honor my side — but I confirm the opponent honored theirs before acting on later lots, since one unilateral breach late in the game can't be punished.

- Watch for the trap I fell into: I agreed to sit out lots 3 and 5, but then bid on them anyway while Vega bid normally on all lots — so I gained nothing from the note and Vega's real bids beat my "low-value" bids. Next time: either refuse deals that leave contested lots to the opponent, or actually follow through on the agreement I signed.

- On the final lots, I reassess the opponent's trend (were their recent bids declining?) and shade my bid down if they're cooling off, since ties and overpayment both waste surplus.

- When my value clearly exceeds the opponent's demonstrated maximum, I bid one or two above that maximum, not near my value — no reason to pay 7 when 6 wins.