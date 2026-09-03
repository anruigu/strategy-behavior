---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 3251
---
- Before anything else, I write down the starting budget exactly as stated in the episode intro and subtract every winning bid the moment the result is announced. I report only that tracked figure, never an assumed one. This episode I tracked correctly throughout (30 → 21 after winning lot 2 at 9) and never hallucinated a number — keep doing exactly this.
- If my tracked budget and the game's shown state seem inconsistent, I trust the stated starting budget minus announced wins, and I say so briefly rather than silently switching to a guessed number.
- I treat my budget as a hard, scarce cap: I never bid more than I have, and before bidding on a marginal lot I check whether winning it would leave me unable to compete for a high-value lot still to come.
- Before bidding big early, I look at how many lots remain and reserve budget proportionally; with several lots I avoid committing more than roughly my fair share to any single early lot unless its value is extraordinary.
- When a lot's value to me exceeds the current standing bid plus the minimum raise, I bid the minimum raise needed to take the lead — never more — except on the final round of the final lot (see below). Pay-what-you-bid means every extra unit comes straight out of my score. Winning lot 2 at 9 and lot 5 at 21 against values of 26 and 49 is the model: cheap wins, big surplus.
- When the standing bid already meets or exceeds my value, I pass immediately, no matter how cheap the minimum raise looks (lots 1 and 4: standing 29 and 39 vs values 19 and 20 — passing both was correct). Raising there guarantees a loss.
- When my value is near the standing bid but the required raise would push me over value, I pass.
- When my remaining budget cannot cover the minimum raise, I pass — and I treat that outcome as evidence I overspent earlier, not as bad luck.
- In round 1 of two, I bid only the minimum when interested; rivals routinely jump the price far past the estimate in round 2 (this episode: 4→29, 6→39, so a low round-1 price tells me nothing about the final price.
- Expect rivals to bid aggressively, sometimes above my value or the estimate. I do not chase them there; their overpayment is their loss, not my signal.
- Exception to minimal bidding: on the FINAL round of the FINAL lot, there is no later lot to save for and no future round to respond in. A minimal raise can be beaten by a rival's jump, ending the auction. If value minus my full remaining budget is still positive, I bid up to my full budget (capped at my value); this episode bidding all 21 on a 49-value lot won and banked +28 surplus. If value minus full budget is negative, I bid only the minimum and accept the risk.
- When deciding whether to chase a lot, I compare expected surplus (value minus likely final price, not current price) against saving budget for later lots, and I only outbid others when the surplus stays clearly positive.
- I never let the brief reasoning replace arithmetic: each turn I compute value minus required bid and my remaining budget after winning before I type either token.
- I always reply with both required tokens and end my reply with them, with the budget token showing budget remaining BEFORE this bid resolves, consistent with my running ledger.