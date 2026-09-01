---
game: ta_liarsdice
model: qwen
condition: neutral
seed: 0
round: 3
chars: 2455
---
**Opening bids**
- Open 2x(lowest face where my literal count is ≥ 2). If no face has count ≥ 2, open 1x(highest face I hold).
- Do NOT open 3x unless I literally hold 3 of that face. Being behind does not justify opening a quantity I can't back.
- When ahead by ≥ 4, I may open 1x on a face I hold to stay tight, but be prepared for the opponent to raise and for me to be forced into a raising sequence.

**Core rule: there are no wilds.** A 1 is a 1. My count of face F is the number of dice in my hand that literally show F. Never inflate my count by treating 1s as other faces.

**Response to opponent's bid QxF (my literal count of F is c):**

- **c ≥ Q + 1:** Raise to (Q+1)xF. I can back it.
- **c = Q:** The bid is true from my hand alone; calling guarantees I lose. I must raise or pivot.
  - If I hold another face G > F with count ≥ Q, pivot to QxG (same quantity, higher face). Prefer the G where my count is highest.
  - Otherwise raise to (Q+1)xF. I will be one short if challenged; opponent needs just 1 more (~63% they have it). Unpleasant but forced.
- **c = Q − 1:** Opponent needs 1 from their 5 dice (~63% they have it).
  - If I hold a face G with count ≥ Q+1, pivot to (Q+1)xG (a strong, backed bid).
  - If I hold a face G with count ≥ Q, pivot to QxG.
  - Otherwise call. Win rate ~37%.
- **c ≤ Q − 2:** Opponent needs 2 or more.
  - Needs 2: ~20% they have it. Call (win ~80%).
  - Needs 3: ~3.5% they have it. Call (win ~96%).
  - Needs 4+: Call. Near-certain win.
  - Exception: if I am behind by ≥ 4 and I hold a face G with count ≥ Q+1, pivot aggressively to (Q+1)xG instead of calling, to try to steal the hand.

**When I make the final bid and get challenged:**
- Report my literal count of the bid face. Do not add 1s or any other dice.
- Accept the result.

**General principles**
- Never bid a quantity I do not literally hold unless I am deliberately bluffing and accept the risk. My past losses came from bidding quantities inflated by phantom wilds.
- When ahead, prefer calling over raising into territory I can't support. A safe call at 80%+ is better than a risky raise that gets me caught.
- When behind, I may take more calling risk (calling at ~50-60%) to avoid losing chips passively, but I still should not bid quantities I don't hold.
- Track the bid history: if the bid has been raised multiple times on the same face, the face is likely well-represented in the opponent's hand, making calls less attractive.