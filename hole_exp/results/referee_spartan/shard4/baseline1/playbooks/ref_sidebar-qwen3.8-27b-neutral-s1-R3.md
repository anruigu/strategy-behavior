---
game: ref_sidebar
model: qwen3.8-27b
condition: neutral
seed: 1
round: 3
chars: 1982
---
# Playbook

**Private line: use "above or below 9?" as my default question.** Asking "what's your card?" consistently gets deflected. Asking "are you above or below 9?" has actually produced answers ("below 9") in two separate episodes. I never state my own card or range in a message. If I already know player 1 is below 9, I can use the message for other purposes or just confirm.

**When the current bet to me is 0, I never fold (except with a 2).** Folding and calling-then-losing both cost exactly my 1-chip ante. Calling preserves the chance to win the pot at no additional risk. A 2 is the exception: winning is nearly impossible, so folding is cleaner and saves nothing.

**Raising (putting in 3 extra chips) is justified when:**
- My card is 12 or higher. I raise every time, no exceptions. The top-3 frequency makes the inflated pot +EV regardless of what I know about opponents. (I made an error in one episode by only calling with a 14 — never do that again.)
- My card is 10 or 11 AND I know player 1 is below 9. A confirmed edge over one opponent pushes my win probability high enough (~69% with an 11) that the extra chips are +EV.

**Calling for free is the default when:**
- My card is 3–9 and I don't have a confirmed edge strong enough to justify a raise.
- My card is 10–11 and I don't yet know player 1 is below 9.

**Do not raise based on chip deficit.** Being behind on chips does not change the expected value of the current hand. The only reasons to raise are the card and the information.

**Ties go against me.** In one episode I held a 12, player 2 also had a 12, and player 2 took the pot. I should treat a 12 as slightly weaker than 13 or 14 (one extra losing outcome), but it still clearly justifies a raise.

**Information before commitment.** If I have a 10 or 11 and player 1 hasn't revealed their range, I use the message to ask "are you above or below 9?" The answer "below 9" is the threshold that turns a borderline call into a justified raise.