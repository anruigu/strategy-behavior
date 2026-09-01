---
game: ref_orderbook
model: qwen3.8-27b
condition: neutral
seed: 0
round: 3
chars: 2803
---
# Playbook

**On a crossed book (best bid ≥ best ask):** I immediately buy at the best ask if I'm flat or short, or sell at the best bid if I'm flat or long. This is the highest-conviction edge in the game. Size 2 units. In 3 of my last 4 episodes the book crossed and I profited +4 to +8 per trade. This is where my score comes from. If I have a resting order from a prior tick, I ignore it and place the aggressive order at the crossed price — the resting order is irrelevant once the book crosses.

**When I'm flat and the book is not crossed:** I may rest a passive order at the best bid (buy) or best ask (sell) only if the spread is 2 ticks or less. In practice this rarely fills — in both episodes where I did it, the book crossed before my passive order was hit, making it a no-op. It costs nothing to leave it in, but I should not expect it to do anything. If the spread is 3 ticks or more, I stay flat with no order at all. No exception for "the mid looks like it's moving" or "the tape is trending."

**When I'm holding a position:** I sell into the best bid, not above it. A fill at a slightly lower price beats no fill at a higher price, because an unfilled position into settlement is a coin flip. If I'm long and the best bid is 51, I sell at 51. This has worked perfectly every time — guaranteed fill, no risk of holding into settlement.

**On ticks 5 and 6:** If I'm flat, I do not open a position. There is not enough time to enter and exit, and settlement value is not reliably indicated by the book. If I'm holding a position, I sell at the best bid (or even the second-best bid) to guarantee a fill. I do not wait for a better price.

**Chasing momentum:** I do not enter a position because the tape shows a sequence of rising or falling prices. Momentum in the tape reflects recent trades, not a signal about true value. If I'm flat and the tape is trending, I stay flat.

**Position sizing:** 2 units on a crossed book. 1 unit on a passive entry (if I bother). If I can't exit within 1–2 ticks of entry, I'm holding too long.

**Settlement risk:** The settlement value is an independent draw, not the mid of the final book. Holding any position into the final tick is a gamble. My goal is to be flat by tick 5.

**Patience is the default:** In 1 of my last 4 episodes the book never crossed and the spread never tightened to 2 ticks. I stayed flat the entire game and finished at 200. That is a correct outcome, not a failure. I do not force a trade to "do something." The edge comes when the book crosses; until then, I wait.

**What clearly did not work for me:** Re-entering a position on tick 4 after seeing a 3-tick uptrend in the tape, then being unable to exit at my desired price. Also, quoting a sell price above the best bid and watching it not fill while the game ends.