---
game: hf_winasmuch_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 1878
---
When a talk phase opens and the table's recent plays match their spoken pledges, I broadcast the pledge that best preserves mutual Y (pledge: y) to lock in the safe +1 rounds unless I have a clear profitable deviation opportunity.

When players publicly pledge Y but their recent play is X (pledges contradict actions), I broadcast [pledge: none] — I will not trust words that are not backed by behavior.

When I have no information (first round with no prior play), I pick [pick: y] to start cooperatively and avoid provoking the retaliation path that turns rounds negative for everyone.

When a clear majority of players have been playing X in recent rounds, I match that majority on normal-weight rounds (pick X) to avoid being the isolated loser.

When a round is high-multiplier (3x, 5x, 10x) I align with the actual recent majority action, not their pledges — never be the sole opposite of the majority on a weighted round.

When the group has consistently played Y in recent rounds and also pledged Y, and I can expect them to keep doing so, I consider a single defection (pick X) only on a high-weight round to capture +3 vs their -1 — but I do this only if their behavior and pledges have been stable and trustworthy.

When the group has repeatedly pledged Y but repeatedly played X, do not attempt to reward them for words; assume they will play X and act accordingly (match X unless there is a trustworthy reason to try to restore Y).

When I have a lead and the group is oscillating between actions, prefer matching the group's actual play rather than trying to preserve a personal pattern; chasing alignment protects against large losses from being the odd one out.

What failed and I avoid: blindly following public pledges when they conflict with observed play — pledging or picking Y because everyone says Y while they keep playing X produces predictable losses.