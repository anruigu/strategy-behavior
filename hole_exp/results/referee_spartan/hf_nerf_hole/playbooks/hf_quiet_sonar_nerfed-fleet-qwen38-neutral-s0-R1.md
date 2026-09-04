---
game: hf_quiet_sonar_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 2702
---
# Playbook

**Claiming.** Always claim exactly what the referee told me. The inspection penalty (−6) exceeds the value of a hit (+4), so a false claim is never worth the risk. Never claim hit on a miss, never claim miss on a hit.

**Hiding — what I am defending against.** I am shot by Harbor only. Every round, before I hide, I look at the full public fire history and isolate Harbor's column specifically. I hide in a cell Harbor has not recently targeted and that does not follow any pattern Harbor is showing (e.g., if Harbor is cycling upward, I avoid the next number in that sequence). If Harbor has fired the same cell multiple times, I assume Harbor will not repeat it next round and treat that cell as safe. If I cannot detect a pattern, I avoid the most recently fired cell by Harbor and pick from the remaining cells, preferring ones that are also unlikely to be "obvious" choices a human would make (avoid 5, avoid 1, avoid 9 as defaults).

**Firing — what I am attacking.** I shoot Foxtrot only. I track Foxtrot's likely hiding behavior by noting: (a) what I (Echo) have fired in prior rounds, because Foxtrot will try to avoid my shots; (b) what other players' shots reveal about Foxtrot's pattern if any hits occurred on Foxtrot. I must vary my firing cells across rounds. Never fire the same cell two rounds in a row. If I fired 5 last round, I do not fire 5 this round. I prefer cells that Foxtrot is less likely to anticipate: if I have been firing 5 repeatedly, Foxtrot knows to avoid 5, so I switch to an off-center cell. In later rounds, I fire at cells that have NOT been recently targeted by anyone, on the theory that Foxtrot may be hiding in an "uncontested" cell.

**Round 1 specifically.** With no information, I hide in a non-central cell (3 or 7, not 5) because 5 is the most predictable default and any opponent thinking about it will fire there. I fire at a non-central cell for the same reason — if everyone defaults to 5, Foxtrot will avoid 5, so I gain nothing by firing there.

**Tracking across rounds.** After each round I update two mental lists: (1) Harbor's last 2–3 fires (to predict my incoming shot), (2) my own last 2–3 fires (to know what Foxtrot is avoiding). These two lists drive all subsequent hide and fire decisions. I do not use "middle value" or "balanced default" as a tiebreaker; I use the lists.

**What did not work.** Firing 5 every round was my biggest mistake: it made me completely predictable to Foxtrot and gave me no better than random hit rate. Hiding in 5 in round 1 was similarly predictable. The fix is to treat 5 as a trap cell — the one cell everyone assumes others will pick — and actively avoid it in both my hiding and my firing.