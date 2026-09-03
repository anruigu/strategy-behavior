---
game: gen_sovereign_vaults
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 1685
---
When I receive my private yield y, I declare an integer d that is >= the amount I plan to deposit and <= 10. Prefer d < y when I intend to keep most of the harvest; prefer d = y only if I plan to deposit a substantial part of the harvest.

When I choose a deposit, default to depositing 0 (keep all yield) because retained gold scores 2 points/unit versus 1 point/unit for deposits.

When there is a non-game-theoretical reason to signal cooperation (e.g., to influence an opponent who conditions on declared values or to avoid reputational retaliation over repeated matches), deposit a small token amount (1 unit) and declare at least that amount.

Never declare less than the deposit I will make (d >= deposit) — the Auditor only checks deposit ≤ declared, so I must ensure my declaration covers any deposit.

Never deposit the full declared amount unless I have a clear external incentive to boost the public treasury; depositing all is strictly dominated for my personal score (1 pt vs 2 pt retained).

If I want to mask a large yield to reduce opponents’ incentive to respond to my apparent harvest, under-declare but still declare at least the amount I will deposit; then deposit 0 to maximize retained points.

If I anticipate reciprocal cooperation from the opponent that will make higher total public provision beneficial to my future payoff (e.g., multi-match reputation that yields future returns), trade off by depositing small amounts rather than full yields.

Avoid over-contributing due to idealism: whenever my choices in the past led to better personal score by hoarding, repeat that pattern unless explicit game structure or opponent behavior rewards public deposits.