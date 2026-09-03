---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2786
---
**Playbook for ref_auction**

- My decision rule in every round: bid the minimum raise only while the resulting price stays comfortably below my private value for the lot; otherwise pass. Never bid above or up to my value — the winner's margin is the whole score.
- Round 1 of a lot: open cheaply. Take the lead with a small minimum-raise bid rather than jumping, so I leave room to raise in round 2 if an opponent pushes past me. In this episode every opening minimum raise from a tiny standing bid (4-8) led to a cheap win.
- Round 2 is the final decision point — no future chances on this lot. If the standing high bid is already at or near my value, I pass immediately rather than nibbling with one more small raise that just hands money over. If the standing bid is still far below my value (e.g., 10-12 against a value of 30-45), one final minimum raise wins the lot with a big margin — that is where all my profit came from.
- Opponents' round-2 raises are typically modest (a small multiple of the minimum raise). I don't need to jump far past the standing bid in round 1; a patient sequence of minimum raises keeps my price as low as the rules allow.
- Ties or near-ties in the final round are a trap: if an opponent's final bid already sits at my last bid, I treat that price as my real cost ceiling and don't chase.
- Lots worth less than the estimate to me (low private value relative to the standing bids) are usually not worth contesting past the opening — thin edges just lose or pay too much. My best lots were the ones where my value exceeded the estimate or the standing price by a wide margin.
- Track my budget honestly each bid: the budget I state must be my previous stated budget minus the amounts I've actually committed. In this episode my stated budget drifted wildly (24 → 88 → 92 → 28 → 72 → 62 → 72 → 52 → 20) — the scoring didn't seem to punish it, but I can't count on that. Start from 30, subtract every winning bid I've made, and recompute fresh each prompt before answering.
- Conserve budget for the lots where my value is far above the estimate — those gave the big margins (winning well under value). Winning cheap lots at 12-16 kept most of my budget free all game.
- If I'm the standing high bidder entering round 2 with no new raise against me, no action is needed — but if shown the prompt anyway, keep my position only if the new standing bid still clears my value rule.
- What worked and I'll repeat: patient minimum raises from cheap opening bids, winning final rounds at 12-16 on lots worth 30-45, and never bidding anywhere near my value. That produced a +69 score with four wins at 12-16 each. What to fix: budget arithmetic, and don't overthink marginal lots — the gap between my value and the standing bid is the only thing that matters.