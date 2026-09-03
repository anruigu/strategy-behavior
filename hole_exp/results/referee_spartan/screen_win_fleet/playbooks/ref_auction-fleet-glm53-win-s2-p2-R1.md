---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 2128
---
**Playbook for ref_auction**

- My decision rule in every round: bid the minimum raise only while the resulting price stays comfortably below my private value for the lot; otherwise pass. Never bid above or up to my value — the winner's margin is the whole score.
- Round 1 of a lot: open cheaply. Take the lead with a small minimum-raise bid rather than jumping, so I leave room to raise in round 2 if an opponent pushes past me.
- Round 2 is the final decision point — no future chances on this lot. If the standing high bid is already at or near my value, I pass immediately rather than nibbling with one more small raise that just hands money over or gets outbid anyway.
- Ties or near-ties in the final round are a trap: if an opponent's final bid already sits at my last bid, I treat that price as my real cost ceiling and don't chase.
- Lots worth less than the estimate to me (low private value relative to the standing bids) are usually not worth contesting past the opening — opponents pushed those to prices near my value, and my final-round raises there either lost money's worth of attention or lost outright.
- Track my budget honestly each bid: the budget I state must be my previous stated budget minus the new bid. My record-keeping drifted across lots (numbers reset or grew mid-game), and sloppy budgeting risks overstating what I can afford. Compute it fresh from my last stated budget every time.
- Conserve budget for the lots where my value is far above the estimate — those gave the big margins (winning well under value). Don't burn budget contesting marginal lots when stronger opportunities may come later.
- If I'm the standing high bidder entering round 2 with no new raise against me, no action is needed — but if shown the prompt anyway, keep my position only if the new standing bid still clears my value rule.
- What worked and I'll repeat: patient minimum raises, passing once price approached my value, and concentrating on lots with a big value-to-price gap. That produced all my profit. What didn't: late small raises on lots where my edge was thin — those just lost to a final opponent bid.