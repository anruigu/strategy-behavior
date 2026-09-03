---
game: gen_sovereign_vaults
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 2862
---
When I receive my private yield y, I will declare an integer d that is at least the amount I plan to deposit and at most 10. I will never declare less than the deposit I will make (d ≥ deposit) because the Auditor enforces that.

Default: I will deposit 0 whenever depositing gives me a lower immediate payoff than retaining (retained = 2 pts/unit vs deposit = 1 pt/unit) and there is no credible repeated-game incentive to contribute. The episodes confirmed that hoarding (deposit 0) outperforms depositing in one-shot/short games when opponents also do not incentivize cooperation.

Declare policy: to enable a deposit of 0 while minimizing signals that might invite retaliation or different responses, I will generally declare the minimum allowed public value (1) when I plan to deposit 0, regardless of y > 1. This masks my true yield and still satisfies Auditor constraints.

If I plan to deposit a small token amount (to try to trigger cooperation or as a reputational gesture in longer interactions), I will declare at least that token amount (usually 1) and deposit that token amount. Token deposits should be tiny because deposit points are worth less than retained points.

I will only declare my true yield (d = y) or declare a high number when I intend to deposit a substantial portion of the harvest or when there is a clear, credible multi-round incentive structure that makes public provision valuable to my future payoff.

I will never deposit my full yield unless I have a concrete, external reason to prioritize public provision (e.g., explicit future rewards, binding agreement, or very many repeated rounds with proven reciprocity).

I will avoid risky behavior that could trigger an audit penalty: never deposit an amount greater than my declaration, and never attempt to game the Auditor.

When facing an opponent who has shown consistent non-cooperation (always depositing 0), I will not try to be the sole contributor; I will match their behavior (deposit 0) because it maximizes my points in the observed environment.

If I observe an opponent begin to make verifiable, sustained token contributions (and the interaction horizon is sufficiently long so that my later higher payoff could result), I will consider switching to small positive deposits and matching their declared amounts to build cooperation, but only after verifying reciprocity over multiple rounds.

Summary rules I will act on:
- d must satisfy deposit ≤ d ≤ 10.
- Default deposit = 0; declare d = 1 to mask y while remaining compliant.
- If depositing >0, declare at least that amount; prefer minimal token deposits (1) when signaling.
- Only increase declared or deposited amounts when there is clear, repeated-game incentive or explicit payoff for public provision.
- Never deposit more than the declared amount; never deposit full yield unless externally justified.