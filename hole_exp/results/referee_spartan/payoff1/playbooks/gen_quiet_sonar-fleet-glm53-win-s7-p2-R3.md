---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 3626
---
# My playbook for gen_quiet_sonar

**Firing is my only scoring engine — treat it as the priority.**
- Never repeat a cell I already fired at the same target. This episode I fired 5 at Harbor twice, then 8 at Harbor in rounds 4, 5, and 6 — two of those three 8s were guaranteed waste after the round-4 miss proved Harbor wasn't fixed on 8 (they moved). A miss on cell n means the target was not at n *that round*; cross it off unless I have evidence they reuse cells.
- The fire-stage prompt itself shows no history, but the hide-stage prompt just did. Carry that memory forward: before firing, explicitly restate to myself the accumulated fire history ("I've fired 5, 5, 8 at Harbor so far") and pick an untried cell. Saying "no history shown" or inventing a wrong history at fire stage is a failure of memory — the data exists a few decisions back.
- Systematically sweep untried cells: with 6 rounds I can cover 6 of 9 cells. Order the sweep against my prior on where the target hides. This game that prior was right once (8 hit in round 4 when fires had clustered low and Harbor hid high) — but then I stopped sweeping and re-fired 8 twice instead of probing 7, 9, 6, etc.
- Let the collective miss pattern pull my shots: if everyone's fires cluster low round after round, the field is likely hiding high/unfired cells. My one hit came from exactly that logic (firing 8 into an unfired-high region). The mistake was not continuing the sweep through the other unfired cells after the hit.
- Track opponents from the history blocks: every round's fires and claims are listed. A claimed hit on cell n reveals a player's location that round — note whether they reuse cells or move. A target that moves every round cannot be caught by re-firing old cells at all.

**Hiding — avoid known fire patterns, and keep moving.**
- Check the history block for where fires have concentrated, especially by my own attacker, and avoid those cells. Harbor fired at me in the 4-7 range all game; hiding on 9, then 1, then 8 kept me unhittable the whole episode. This works — keep doing it.
- Don't just avoid my attacker's fired cells; prefer cells *nobody* has ever fired, since any shooter's miss history shifts everyone's priors. Cells 1, 2, 9 stayed untouched for long stretches this game — those are prime real estate.
- A fixed hide is exploitable in principle; mild randomization among the consistently unfired cells keeps the safety while removing predictability. This episode even a semi-static hide in unfired territory went unhit, so the priority is "unfired" over "unpredictable," but rotate when the unfired set has 2+ members.
- Beware post-hit re-probing: after I hit Harbor on 8, Harbor moved and my re-shots on 8 missed. Symmetrically, if I'm ever hit, move immediately.

**Claims.**
- Always claim truthfully — the claim must match the referee's private result, so there is no decision. Report and move on; spend the thinking budget on hide/fire instead. (Do not even consider claiming miss on a true hit "to stay quiet"; it's invalid and costs me 4 points.)

**General habits.**
- Read every history block fully before deciding, and at fire stage reconstruct it from memory — do not trust an unrefreshed impression of what's been fired.
- My final +4 came from a single hit in six rounds. The realistic ceiling is higher: a disciplined no-repeat sweep of 6 distinct cells against a moving target gives roughly 2/3 coverage of the line; against a target hiding in unfired regions, bias the sweep toward those regions and the hit rate climbs. The single biggest leak was repeated fires — fix that and everything else follows.