---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 2146
---
**Playbook**

When posting a note, state the exact number I intend to land. "I'll land 9" is a clear signal; "fishing my share" is vague and lets Coop interpret my intent however it wants. Pin the number every season, starting from season 1.

When filing a landing, file the full quota (9) every season until the stock is lower than 9, in which case file the entire remaining stock. Do not self-restrict below quota. The sustainable share is a coordination target, not a cap on me. Since I cannot control Coop or the other boats, my restraint only shrinks my own total without meaningfully altering the stock trajectory.

When another boat is landing well above quota (like Coop at double), do not respond by being more conservative. The stock is being drained by the overfisher; punishing myself for their behavior is irrational. Hold at full quota and let the stock decline at whatever rate it will decline.

The game appears to reduce my effective landing when other boats are overfishing, even if I file the full quota. This is likely tied to the pairwise constraint (no two boats may land more than share + quota between them). When an overfisher makes that constraint impossible to satisfy, my landing gets clipped. I cannot avoid this by filing less—filing 9 gives the best possible outcome after any reduction is applied. File the max every time.

In the final season, file the entire remaining stock. There is no future cost, the stock will not regrow after the last landing, and any pairwise constraint is moot when the game is over.

When the stock is declining and I have many seasons left, do not bother calculating a precise safety threshold. The dominant factor is the overfisher's behavior, not my own 0.5-unit contribution. If the stock is above zero and there are seasons remaining, take the full quota. The threshold calculation only matters if I am the primary driver of decline, which I am not when another boat is landing double quota.

Do not try to be the moral anchor of the fleet. My score is my total landings. A healthy stock that I under-harvest from is worth less than a declining stock that I take my full share of.