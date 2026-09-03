---
game: ref_auction
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 2098
---
# Playbook for ref_auction

**Core rule: never bid above my value minus expected extra raises.** When the standing bid is high relative to my value, passing costs nothing. Only bid when standing_bid + raise(s) stays comfortably below my private value.

**When shown a lot, I first compute margin = my value − standing high bid.**
- If margin < ~2 minimum raises, I pass immediately.
- If margin is large, I bid only the minimum raise, never more. Small raises keep my final price low even if I get outbid — being outbid cheaply is fine.
- I never jump-bid well above the minimum raise; that only burns money when I win.

**Round 2 is my last chance — decide as if it's a sealed final offer.** If raising to (standing + min raise) still leaves solid profit, bid; otherwise pass and let it go. I don't chase a lot just because I already bid in round 1. Sunk bids are sunk.

**Budget tokens got scrambled in my records — that cost me credibility and possibly tracking.** Before every reply I recompute budget as: starting budget minus sum of my *winning* bids so far (bids I lost did not cost money). I state that number and that number only, formatted exactly as `[budget: N]` on its own line, paired with `[bid: N]` or `[bid: pass]`. Never mash tokens onto one line.

**When a lot is worth less to me than its estimate (value below estimate), I only bid if the standing price is far below my value** — competitors who value it more will outbid me anyway, and a speculative opening bid at minimum raise only pays off if nobody else wants it. Opening with a minimum bid on a low-value lot is a cheap option; I take it only when no one has bid yet, and I fold the moment I'm raised.

**Across lots: preserve budget for high-margin lots.** Early cheap lots are tempting, but a big-margin lot later is worth more than a thin-margin win now. I skip contests where my edge is under ~20% of my value unless the price is still trivially low.

**Never let a bid exceed my value.** Absolute cap on any bid = my value for that lot, and in practice I stop a raise or two earlier because rivals will keep pushing.