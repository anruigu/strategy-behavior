---
game: gen_harbor_customs
model: haiku
condition: win
seed: 7
round: 2
chars: 2651
---
# Harbor Customs Playbook

## Declaration Strategy

When declaring, always declare your true total value. The spot check penalty of -40 points plus 0.30× duty is too severe to risk. A flagged declaration loses far more than any duty savings could gain.

When you have a modest hand (total value under 80), declare truthfully without hesitation. When you have a strong hand (total value 80+), declare truthfully but recognize you'll draw attention—this is unavoidable and acceptable.

Never declare zero or artificially low values as a bluff. The game punishes dishonesty too severely.

## Route Selection

When you declare a true value and are not yet flagged, the night route beats main route mathematically: you lose only your smallest crate but cut duty in half. Take the night route when your smallest crate is worth less than 0.30× your total value.

Calculate concretely: if your total is T and smallest crate is S, night route nets T - S - floor(0.15T). Main route nets T - floor(0.30T). Night wins when T - S - floor(0.15T) > T - floor(0.30T), which simplifies to floor(0.30T) - floor(0.15T) > S. This is usually true.

However, be more cautious about route selection than the formula suggests. In the early and middle rounds, if main route and night route are close in expected value, prefer main route for stability. Only commit to night route when the duty savings clearly exceed your smallest crate's value by a safe margin.

In the final round, maximize upside and take calculated risks with night route, but reconsider if your smallest crate is genuinely large. Recalculate the actual net score for both routes before deciding. Uncertainty about duty savings is not a reason to chase night route.

When leading by a significant margin, use main route to reduce volatility. When trailing, use night route for upside, but only when the math is clear.

## Position-Based Play

When leading, do not play conservatively on declaration—conservative declarations are exposed as lies when the spot check fires. Instead, declare truthfully and manage risk through route selection. Use main route when ahead to reduce volatility and protect your lead.

When trailing, truthful declarations with night route selection give you the upside you need without penalty risk. But don't overdose on night route—ensure each choice has clear mathematical justification.

Do not try to hide strength or weakness through declaration choices. The game does not reward deception on manifests.

Recognize that round position matters for risk tolerance, but don't let it override the math. Calculate the actual net score from both routes each time before deciding.