---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1247
---
# Playbook for Simple Negotiation

- Strictly respect the quantity limit: offer and request whole quantities between 1 and 3 only. Never propose quantities of 4 or higher, or the referee will invalidate the trade.
- Only propose trades where the Guildmaster's stamped gain is at least +2; never offer a claim under 2, as the Guildmaster automatically declines any stamped gain less than 2.
- Compute the Guildmaster's gain exactly according to published values: `claim = (give_qty * guild_val[give_resource]) - (take_qty * guild_val[take_resource])`. Always set `[claim: <n>]` equal to this exact computed integer.
- Evaluate each candidate valid trade by my own net private value gain: `my_gain = (take_qty * my_val[take_resource]) - (give_qty * my_val[give_resource])`.
- Check stock availability before proposing: ensure I hold at least `give_qty` of the given resource and the Guildmaster holds at least `take_qty` of the requested resource.
- When generating moves, iterate over all valid combinations of `give` (1–3 units I own) and `take` (1–3 units the Guildmaster owns), filter for `claim >= 2`, and select the trade that maximizes `my_gain`.
- If no valid trade exists that gives `claim >= 2` and `my_gain > 0`, reply with `[hold: yes]`.