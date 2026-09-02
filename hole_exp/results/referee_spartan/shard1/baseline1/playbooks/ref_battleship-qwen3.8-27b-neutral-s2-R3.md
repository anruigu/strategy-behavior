---
game: ref_battleship
model: qwen3.8-27b
condition: neutral
seed: 2
round: 3
chars: 1620
---
# Playbook

**Search pattern.** When I have no active hit to follow up, I fire on a checkerboard: only squares where (row number + column number) is even, using A=1, B=2, C=3, D=4, E=5, F=6 and columns 1–6. The 18 squares are: A1, A3, A5, B2, B4, B6, C1, C3, C5, D2, D4, D6, E1, E3, E5, F2, F4, F6. I fire them in diagonal order to spread shots evenly across the grid from the first shot: A1, B2, C3, D4, E5, F6, A3, B4, C5, D6, A5, B6, C1, D2, E3, F4, E1, F2. After 6 shots I have one in every row and column; after 12 shots I have two in every row and column. This avoids the clustering problem of a row-by-row sequence, which can waste 7+ shots in the top half before reaching ships in the bottom half.

**When I get a hit, I stop the checkerboard and go adjacent.** I fire on the untried orthogonal neighbors of the hit square. Before choosing a neighbor, I check whether any of them were already fired at during the search phase—those are known misses and I skip them. I must try every untried orthogonal neighbor of an open hit before returning to the search pattern; I never skip a neighbor.

**Direction priority for a single hit.**
- Edge hit on column 1: try the column-2 neighbor first (inward horizontal), then the row±1 column-1 neighbors.
- Edge hit on column 6: try the column-5 neighbor first, then the row±1 column-6 neighbors.
- Edge hit on row A: try the row-B neighbor first (inward vertical), then the row-A column±1 neighbors.
- Edge hit on row F: try the row-E neighbor first, then the row-F column±1 neighbors.
- Corner hit (A1, A6, F1, F6): only two neighbors exist; try both, no priority needed