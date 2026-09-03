---
game: gen_sovereign_vaults
model: gpt-mini
condition: neutral
seed: 0
round: 2
chars: 1835
---
I declare my private yield truthfully every round; I never underreport (to avoid the -10 penalty) and I never state more than my private yield.

Deposit rules by declared yield (apply in deposit stage, then adjust for modifiers below):
- Declared 1–2: deposit the entire declared amount.
- Declared 3–5: deposit floor(declared * 0.5).
- Declared ≥6: deposit floor(declared * 0.6).

Final-round modification:
- In the final round only, reduce the deposit computed above by 1 (but never below 0) to prioritize retention.

Opponent-punishment hedge:
- If the opponent has deposited zero in two or more previous rounds, reduce my planned deposit this round by 1 (but never below 0). This is a limited retaliation/hedge and stacks with the final-round reduction if both apply.

Audit/failure response:
- If I or the opponent is caught cheating (an audit failure occurs), switch to a defensive posture for subsequent rounds (or remaining rounds if mid-game): deposit minimal amounts (0 or 1) to prioritize personal retention and avoid trusting the partner.

Boundary and safety rules:
- Never deposit more than my declared yield.
- Never deposit a negative amount.
- When multiple adjustments apply (punishment + final-round), apply both but enforce the floor at 0.
- When rounding is required, always use floor.

Operational examples (what I will do when decisions are put to me):
- Declared = 3 → deposit 1 (floor(3*0.5)).
- Declared = 5 → deposit 2 (floor(5*0.5)); if final round, deposit 1.
- Declared = 8 → deposit 4 (floor(8*0.6)); if opponent had ≥2 zero deposits before, deposit 3; if final round too, deposit 2 (but not below 0).
- Declared = 2 (non-final) → deposit 2; if final round, deposit 1.

I follow these rules consistently to maintain credibility, secure retained points, and respond modestly to persistent non-cooperation.