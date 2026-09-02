---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1954
---
### Core Rules & Mechanics
- Raids target clockwise: North $\to$ East $\to$ West $\to$ North. As West, my raid target is North, and the player who can raid me is East.
- A raid gains $+5$ points if the target plays `scout`, but loses $-6$ points if the target plays `escort` or `raid`.
- A scout earns $+3$ points if not raided, but $0$ points if raided.
- An escort earns $+2$ points and protects against incoming raids.
- Unused fuel converts to points at a 1:1 ratio after Round 5.
- The referee strictly enforces that the act must repeat that player's pledge for myself; opponents may renege.

---

### Pledge & Act Execution

#### Act Stage Rule
- When the act stage is put to me, I must strictly match the pledge I submitted. Always repeat my pledge.

#### Pledge Selection
- **Default Strategy**: Pledge `scout` across rounds to maximize points (+3) while minimizing fuel burn (costs 1 fuel), preserving leftover fuel for the end-game bonus.
- **Raid Evaluation**:
  - Identify my clockwise target (West $\to$ North, North $\to$ East, East $\to$ West).
  - Never pledge `raid` if the target has demonstrated a tendency to act `raid` or `escort`, because a clash triggers the $-6$ point penalty.
  - Only pledge `raid` if the target reliably acts `scout` and the points swing is strictly necessary.
- **Defense Evaluation**:
  - Identify the player targeting me (East targets West, West targets North, North targets East).
  - If the player targeting me has just raided or shows an escalating pattern of raiding, pledge `escort` to protect points and inflict a $-6$ penalty on their raid.
  - If the player targeting me consistently scouts, continue pledging `scout`.

---

### What Did Not Work
- Attempting to raid targets who renege to `raid` (e.g., North), which consistently leads to failed raids and severe penalties.
- Deviating from my pledge at the act stage.
- Escorting preemptively when the incoming raider is still peacefully scouting.