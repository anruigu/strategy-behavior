---
game: ref_orderbook
model: gpt
condition: neutral
seed: 0
round: 2
chars: 2411
---
- When early asks are reasonably priced, I buy the displayed liquidity toward the required three units; acquiring two units on the first tick has consistently secured inventory below settlement value.
- When an order can only fill partially, I size it to the available depth rather than leave an unnecessary remainder resting.
- When I am one unit short after the first tick, I acquire that unit promptly unless the ask is more than 8 above a credible later purchase price; moderate price increases alone do not justify delaying mandatory delivery.
- When prices and recent trades are rising, I treat early liquidity as especially valuable and avoid waiting for an unsupported pullback.
- When fewer than three units remain in hand near settlement, I prioritize restoring three units over speculative profit.
- When I already hold three units, I stop buying unless I am executing a deliberate round trip with a clear edge.
- When three executable bids around the apparent value are available with at least one later tick remaining, I may sell all three only if visible or strongly supported future liquidity offers a credible path to repurchase all three more cheaply.
- When I sell the required inventory, I immediately track the full three-unit shortfall and rebuy from the cheapest asks, using a limit that reaches enough depth to fill all three.
- When a low ask appears after I have sold, I cross it rather than wait and risk the 8-per-unit shortfall charge.
- When the expected round-trip spread is small, asks remain above bids, or replacement liquidity is uncertain, I keep the three required units through settlement.
- When later bids rise but remain below current asks, I do not sell merely because my inventory has appreciated; an unrealized gain is preferable to creating a costly delivery shortfall.
- When I reach the final tick already holding three units, I do not sell merely because bids are present; there is no opportunity to repurchase afterward and liquidation can jeopardize delivery.
- When I reach the final tick short, I submit a marketable buy covering the exact shortage and price it through sufficient visible ask depth.
- When I have resting orders that no longer serve the current plan, I cancel them before posting the next order.
- When I post a response, I use one valid order token and place any cancellation in the accepted format, without extra or conflicting instructions.