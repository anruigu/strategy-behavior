---
game: ref_auction
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 2759
---
# Playbook for ref_auction

**Core rule: never bid above my value minus expected extra raises.** When the standing bid is high relative to my value, passing costs nothing. Only bid when standing_bid + raise(s) stays comfortably below my private value.

**When shown a lot, I first compute margin = my value − standing high bid.**
- If margin < ~2 minimum raises, I pass immediately.
- If margin is large in round 1, I bid only the minimum raise. Small raises keep my final price low even if I get outbid — being outbid cheaply is fine.
- I never jump-bid above the minimum in round 1; that only burns money when I win.

**Round 2 is a sealed final offer — bid for the whole margin, not just one tick.** This episode proved it: on a lot worth 44 I bid only 12 in round 2 and lost to 33, leaving ~31 of surplus on the table. In round 2 there is no further exposure — if I think a rival's final bid will land around X, and X < my value, I should bid near my best estimate of what it takes, not the minimum raise. A good default: bid up to roughly 60–75% of my value when margin is large, or to just under my value when competition has been fierce on this lot. Minimum raises in round 2 only win when nobody else wants the lot, which is exactly when I'd have won anyway.

**Budget tokens got scrambled — this is a hard rule now.** Before every reply I recompute budget as: current budget minus nothing (bids only cost money when they *win*). Lost lots cost nothing; won lots deduct their price. I stated [budget: 100] after starting at 30 — never again. State the correct running number, formatted exactly as `[budget: N]` on its own line, paired with `[bid: N]` or `[bid: pass]`. Never mash tokens onto one line.

**When a lot is worth less to me than its estimate, I only bid if the standing price is far below my value.** Competitors who value it more will outbid me anyway. Opening with a minimum bid on a low-value lot is a cheap option; I take it only when no one has bid yet, and I fold the moment I'm raised. This worked on lot 4: opened at 8, folded at 20 against value 27.

**Results so far are a price signal — use them.** Rivals paid 42, 33, 20 for comparable lots. If they've been paying near or above estimate, my round-2 sealed bid needs to be aggressive to win high-margin lots; if they've been cheap, minimum raises suffice.

**Across lots: preserve budget for high-margin lots.** A big-margin lot later is worth more than a thin-margin win now. I skip contests where my edge is under ~20% of my value unless the price is still trivially low.

**Never let a bid exceed my value.** Absolute cap on any bid = my value for that lot. Round 2 is the one place I can approach that cap deliberately, because there is no chance of being raised afterward.