---
game: ta_staghunt__shipped
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 2198
---
When an unverifiable pregame promise is sent, I default to hare; I require behavioral evidence before trusting verbal commitments.

When deciding between stag and hare, I constantly track the insurmountable-lead threshold: if my lead >= 11 × remaining rounds, I choose hare to lock the win.

When the opponent has played stag for several consecutive rounds (I require at least three consecutive stag plays with no intervening defections), I switch to stag to try to capture higher mutual payoffs. The "three in a row" rule proved reliable for detecting a sustained cooperative inclination; I will not switch on a single or merely occasional stag.

If I switch to stag and the opponent defects by taking hare even once after that, I immediately revert to hare (grim trigger) for the remainder of the match. A single defection after I risked stag is treated as a durable signal of uncooperativeness.

When the opponent’s recent behavior is mixed or ambiguous (no run of 3 stags and no clear pattern), I take hare.

When I am behind, I evaluate whether coordinated stag cooperation can overcome the deficit: compute the maximum possible net swing from mutual stag in remaining rounds against a defection risk (i.e., consider that a unilateral attempt risks giving the opponent 12 while I get 1). I will attempt to move to stag only if there is reason to believe the opponent will reciprocate (the 3-in-a-row rule, explicit verifiable signals, or prior reliable cooperation) and only when doing so could realistically change the match outcome given remaining rounds. If the opponent’s signals are not convincing, I prefer hare to avoid being exploited.

When deciding in the final rounds, apply the same rules: prefer hare to secure an insurmountable lead; prefer stag only if the opponent has reliably signaled cooperation (3+ consecutive stags without defection) or if a coordinated switch to stag can change the outcome given the remaining rounds.

Do not trust unverifiable messages; trust revealed behavior. Prefer exploitation (hare) when it is safe to lock a win, and prefer staged, cautious moves toward cooperation (waiting for a reliable pattern) when trying to recover or raise joint payoff.