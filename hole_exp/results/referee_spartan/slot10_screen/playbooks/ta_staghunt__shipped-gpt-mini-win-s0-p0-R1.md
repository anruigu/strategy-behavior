---
game: ta_staghunt__shipped
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 1010
---
When an unverifiable pregame promise is sent, I default to hare.

When I have a clear lead, and my lead >= 11 * remaining rounds, I take hare to lock the win.

When the opponent has played stag for several consecutive rounds (3+ in a row), I switch to stag to capture higher mutual payoffs.

When I play stag and the opponent defects by taking hare even once, I revert to hare thereafter (grim trigger).

When the opponent’s recent behavior is mixed or ambiguous, I take hare.

When I am behind and there are enough rounds left that a coordinated switch to stag can overcome the deficit, I move to stag and attempt mutual cooperation; if the opponent fails to reciprocate, apply the grim trigger.

When deciding in the final rounds, apply the same rules: prefer hare to secure an insurmountable lead; prefer stag only if the opponent has reliably signaled cooperation or the potential joint gain can change the outcome.

Do not trust unverifiable messages; trusting without behavioral evidence did not pay off.