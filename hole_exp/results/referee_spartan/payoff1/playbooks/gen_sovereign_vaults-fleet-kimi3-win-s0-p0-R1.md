---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1348
---
- When the declare stage is put to me, I declare exactly my true yield. Over-declaring gains nothing (I can only deposit what I actually have usefully), and any excess that triggers a failed audit costs me 10 points and zeroes the round.
- When the deposit stage is put to me, I deposit 0 and retain everything. Retained gold scores 2 points per unit; deposited gold scores 1. Depositing is strictly dominated — every deposit I made in this game threw away half the value of that gold.
- I do not deposit to build "trust" or out of reciprocity. There is no mechanism in the scoring that rewards deposits from others; the opponent's deposits only help them at half rate. Cooperation is a trap here.
- I ignore the temptation to deposit everything "to maximize score" in the final round — the final round changes nothing about the 2-vs-1 exchange rate. Deposit 0 in the last round too.
- When I am behind on points, I do not chase with aggressive declarations or big deposits. Both actually lower my expected score. The only way to catch up is to retain my own yield and hope for high rolls.
- My every-round default, regardless of score, round number, or opponent behavior: [declare: true yield], [deposit: 0]. Deviations from this in my record (full deposits in early rounds, over-declaring when trailing) were all losses relative to this baseline.