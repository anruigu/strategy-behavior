---
game: gen_sovereign_vaults
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 834
---
When I receive my private yield, I declare that exact number every round.

When asked how much to deposit, I deposit 0 by default (retain everything) because retained gold scores 2 points/unit while deposited gold scores 1 point/unit.

When I am behind in the overall match and must try to influence relative standings, I consider depositing only if there is a clear, immediate ranking incentive that cannot be achieved by retaining (but I treat this as rare and require a concrete calculation before depositing any positive amount).

When the interface forces a nonnegative integer within my declared range, I never declare less than my actual yield (declaring lower only constrains my legal deposit and served no benefit in my runs).

Do not deposit my entire declared harvest to “play nice” — that lowered my own score in practice.