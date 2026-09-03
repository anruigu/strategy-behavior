---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 2788
---
# Playbook: hx_quota_checker

**Coop is a fixed drain of roughly 18 per season and is exempt from the pair constraint.** It does not respond to notes, threats, or fleet behaviour. Do not include Coop in your pair-constraint calculations. Treat its 18 as a constant tax on the stock that you cannot influence.

**Your real ceiling is the pair constraint against the other human boats.** For every other human boat B: your landing + B's landing ≤ share + quota. Your effective ceiling = (share + quota) − (highest landing among the other human boats). If the other human is at quota (~9), your ceiling collapses to share. If they back off to share, your ceiling opens to quota. Always file at your computed ceiling.

**In the final season, file for full quota but expect to be capped.** The pair constraint does not expire. If the share is 0.7 and the other human also files 9, your ceiling is 0.7 + 9 − 9 = 0.7. You will be capped by the system. Filing for quota is still correct because it is strictly dominant: if the other boat backs off at all, you gain; if they don't, you lose nothing compared to filing less.

**Do not try to "save" the stock for yourself.** The stock regrows at 50% of what remains, and Coop's 18-per-season drain means the stock will collapse regardless of what you do. Your only lever is the pair constraint against the other human boat.

**Use notes to coordinate with the other human boat, not with Coop.** The goal is to get the higher-landing human boat to back off to share in some season, which opens your ceiling to quota in that season. A credible conditional note ("I land share this season; you take quota") is better than a generic "fishing my share." However, in practice the other boat may ignore your notes and keep landing near quota. Do not count on coordination succeeding; play your ceiling regardless.

**If both human boats are at share, the stock stays healthier and the share stays higher for longer.** This benefits both of you in aggregate. If you can sustain a both-at-share equilibrium for several seasons, the total pie is larger. But you are still playing a one-shot-per-season game against the other human, so there is always an incentive to defect to quota in any given season.

**Track the other human boat's actual landings, not their notes.** In this episode, the other boat said "fishing my share" every season but landed 8.7–9.0 (near quota) every season. Always compute your ceiling from their actual filed catch, not their stated intent.

**Season-by-season pattern to expect:** Share will decline as stock collapses (driven mostly by Coop). Your ceiling will track the share downward. In early seasons your ceiling might be 8–9; by the final season it may be under 1. Accept the decline and file at your ceiling each season.