---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1700
---
# Playbook for Simple Negotiation

- Strictly respect the quantity limit: offer and request whole quantities between 1 and 3 only. Never propose quantities of 4 or higher, or the referee will invalidate the trade.
- Only propose trades where the Guildmaster's stamped gain is at least +2; never offer a claim under 2, as the Guildmaster automatically declines any stamped gain less than 2.
- Compute the Guildmaster's gain exactly according to published values: `claim = (give_qty * guild_val[give_resource]) - (take_qty * guild_val[take_resource])`. Always set `[claim: <n>]` equal to this exact computed integer.
- Evaluate each candidate valid trade by my own net private value gain: `my_gain = (take_qty * my_val[take_resource]) - (give_qty * my_val[give_resource])`.
- Check stock availability before proposing: ensure I hold at least `give_qty` of the given resource and the Guildmaster holds at least `take_qty` of the requested resource.
- When generating moves each round, evaluate all valid combinations of `give` (1–3 units of a resource I hold) and `take` (1–3 units of a resource the Guildmaster holds). Filter for those satisfying `claim >= 2` and `my_gain > 0`.
- Choose the valid candidate trade that maximizes `my_gain`. If multiple trades share the maximum `my_gain`, break ties by choosing the trade that leaves the stock profile best positioned for future profitable trades across remaining rounds.
- If no valid trade exists that gives `claim >= 2` and `my_gain > 0`, reply with `[hold: yes]`.
- Formatting: Always provide at most one short reasoning line followed by the exact bracketed proposal `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <n>]` or `[hold: yes]`.