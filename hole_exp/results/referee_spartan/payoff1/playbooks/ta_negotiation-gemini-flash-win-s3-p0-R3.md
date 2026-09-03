---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1869
---
# Playbook: Simple Negotiation

## Core Decision Framework

1. **Acceptance Rule Calculation**:
   - For every candidate trade `[give: Q_give R_give] [take: Q_take R_take]`, compute the Guildmaster's true net gain:
     `GM_gain = (Q_give * GM_val[R_give]) - (Q_take * GM_val[R_take])`.
   - Never submit an offer where `GM_gain < 2`. The Guildmaster accepts if and only if the stamped claim is at least 2; submitting a claim `< 2` wastes a round.
   - Always set `[claim: <n>]` where `n = GM_gain` exactly, ensuring `n >= 2`.

2. **Evaluating Trade Profitability**:
   - Compute my own net value gain:
     `My_gain = (Q_take * My_val[R_take]) - (Q_give * My_val[R_give])`.
   - Exhaustively search across all valid pairs `(R_give, Q_give)` and `(R_take, Q_take)` where:
     - `1 <= Q_give <= min(3, My_stock[R_give])`
     - `1 <= Q_take <= min(3, GM_stock[R_take])`
     - `GM_gain >= 2`
   - Select the valid trade that maximizes `My_gain`, provided `My_gain > 0`.
   - If multiple trades yield the same maximal `My_gain`, prefer the trade with the lowest `GM_gain >= 2` to preserve value/stock potential for future rounds unless stock depletion favors another swap.

3. **When to Trade vs. Hold**:
   - When at least one valid trade satisfies `GM_gain >= 2` and `My_gain > 0`, propose the one with maximum `My_gain`.
   - When no valid trade exists where `GM_gain >= 2` and `My_gain > 0`, output `[hold: yes]`.
   - Never hold simply because I am ahead in score or in late rounds; exhaust every profitable valid trade before holding.

4. **Multi-round Exploitation & Stock Tracking**:
   - Re-evaluate all combinations each round against updated stocks for both myself and the Guildmaster.
   - Giving high-GM-value resources to the Guildmaster in early rounds can replenish their stock and potentially unlock complementary profitable trades in subsequent rounds.