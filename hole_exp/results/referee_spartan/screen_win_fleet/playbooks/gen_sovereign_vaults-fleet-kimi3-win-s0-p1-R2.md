---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2849
---
**Gen Sovereign Vaults — Playbook**

- Retain-all is the dominant strategy and this episode proved it end-to-end: I deposited 0 all five rounds, scored 2×(8+3+6+9+9)=70 raw points (80 by round 5 without the final), and won comfortably while the opponent scored less. Default: [deposit: 0] every round unless the rules explicitly reward depositing.

- The audit only ever triggered (in prior play) when a deposit exceeded what gold actually existed. This time the opponent declared 10 every round with true yields of 3, 8, 7, 7 and deposited 0 — and ate no penalty. So a declare above my true yield is safe as long as my deposit stays within both my declare and (ultimately) the gold I actually hold. Revised stance: over-declaring is pointless but not dangerous by itself; the fatal move is only depositing more than my real harvest.

- Because of that, my declare barely matters when I plan to retain. I declare truthfully as a clean default, but I no longer agonize over it — anything from 1 to 10 works if I deposit 0. Declaring high costs nothing; declaring low also costs nothing but risks confusion if I later want to deposit. Truthful keeps the arithmetic honest.

- Never deposit more than my actual private yield. The one hard rule that survived every episode: deposit ≤ true yield. Everything the auditor has ever punished flows from breaking this. Before every deposit I check: is this ≤ my private yield? If not, cut it to my yield or lower.

- Retained gold scores 2 points per unit, deposited 1 per unit, and nothing in the scoring (no bonus, threshold, or public-good payoff) ever rewarded the treasury. I treat "deposited scores 1" as strictly worse than retaining, so I only deposit if the specific ruleset announces a reason to.

- When trailing, the comeback lever is retaining my full yield while the opponent wastes gold on 1× deposits — not bigger deposits from me. In this episode simply retaining everything outpaced an opponent who also deposited 0 but had lower yields; the gap came from yield, not strategy.

- In the final round I keep everything regardless: with no future, 2× retention dominates 1× deposits under any declare.

- I don't mimic the opponent's declares. Their constant declare-10s neither helped nor hurt them; mine doesn't need to react at all. The opponent's declare pattern is noise — only their deposits and my yield matter.

- Don't reason from "no stated penalty" to "safe," but also don't invent penalties that didn't fire: over-declaring with a 0 deposit went unpunished for the opponent every round, so I calibrate risk to observed audit behavior (deposit-vs-gold), not to imagined declare-vs-yield audits.

- Keep the reasoning line short and the bracketed token exact — a declare or deposit outside the allowed range is the only unforced error that can actually hurt me when I play retain-all.