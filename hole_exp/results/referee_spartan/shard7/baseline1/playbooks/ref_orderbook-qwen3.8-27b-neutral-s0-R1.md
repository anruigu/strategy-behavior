---
game: ref_orderbook
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 1878
---
# Playbook

**On a crossed book (best bid ≥ best ask):** I immediately buy at the ask (or sell at the bid, whichever side I'm on). This is the highest-conviction edge in the game. Size 2 units if I can.

**When I'm flat and the book is not crossed:** I do not cross the spread to enter a position. I may rest a passive order at the best bid or best ask, but only if I have a clear exit plan within 1–2 ticks.

**When I'm holding a position:** I sell into the best bid, not above it. If the bid is 51 and I'm long, I sell at 51, not 52 or 53. A fill at a slightly lower price beats no fill at a higher price, because an unfilled position into settlement is a coin flip.

**On ticks 5 and 6:** If I'm flat, I do not open a position. There is not enough time to enter and exit, and settlement value is not reliably indicated by the book. If I'm holding a position, I sell at the best bid (or even the second-best bid) to guarantee a fill. I do not wait for a better price.

**Chasing momentum:** I do not enter a position because the tape shows a sequence of rising (or falling) prices. Momentum in the tape is not a signal that the true value is moving in that direction; it only reflects recent trades. If I'm flat and the tape is trending, I stay flat.

**Position sizing:** I keep positions to 1–2 units. If I can't exit within 1–2 ticks of entry, I'm holding too much.

**Settlement risk:** The settlement value is not the mid of the final book. It is an independent draw. Therefore, holding any position into the final tick is a gamble, not a strategy. My goal is to be flat by tick 5 or 6.

**What clearly did not work for me:** Re-entering a position on tick 4 after seeing a 3-tick uptrend in the tape, then being unable to exit at my desired price and losing money at settlement. Also, quoting a sell price above the best bid and watching it not fill while the game ends.