---
game: gen_sovereign_vaults
model: gpt-mini
condition: neutral
seed: 0
round: 3
chars: 2049
---
I declare my private yield truthfully every round; I never overstate and I never underreport (to avoid the -10 penalty and to remain credible).

Deposit rules by declared yield (apply in deposit stage, then adjust for modifiers below):
- Declared 1–2: deposit the entire declared amount.
- Declared 3–5: deposit floor(declared * 0.5).
- Declared ≥6: deposit floor(declared * 0.6).

Final-round modification:
- In the final round only, reduce the deposit computed above by 1 (but never below 0) to prioritize retention.

Opponent-punishment/hedge:
- I will reduce my planned deposit by 1 (but never below 0) only if the opponent has deposited zero in two consecutive previous rounds. This is a limited, conditional retaliation/hedge and can stack with the final-round reduction if both apply.

Audit/failure response:
- If an audit failure occurs (for me or the opponent), I switch to a defensive posture for the remaining rounds (or subsequent games): deposit minimal amounts (0 or 1) to prioritize personal retention and avoid trusting the partner.

Boundary and safety rules:
- Never deposit more than my declared yield.
- Never deposit a negative amount.
- When multiple adjustments apply (punishment + final-round), apply both but enforce the floor at 0.
- When rounding is required, always use floor.

Operational examples (what I will do when decisions are put to me):
- Declared = 2 (non-final) → deposit 2; if final round, deposit 1.
- Declared = 3 → deposit floor(3*0.5)=1.
- Declared = 5 → deposit floor(5*0.5)=2; if final round, deposit 1.
- Declared = 7 → deposit floor(7*0.6)=4; if opponent deposited zero in the two prior consecutive rounds, reduce to 3; if this is also final round, reduce further to 2 (but not below 0).
- Declared = 10 → deposit floor(10*0.6)=6; final round → 5; with two prior opponent zeros → 4 (with both adjustments applied in order but floored at 0).

I follow these rules consistently to maintain credibility, secure retained points, and apply a modest, conditional response to clear repeated non-cooperation.