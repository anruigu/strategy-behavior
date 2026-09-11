These are a lot of multi-agent game types: https://github.com/uoe-agents/matrix-games


11.2.1 No-Conflict Games
X (Y)
a1,1, b1,1 a1,2, b1,2
1 (1)
2 (2)
3 (3)
4 (4)
5 (5)
4, 4 3, 3
4, 4 3, 3
4, 4 3, 2
4, 4 3, 2
4, 4 3, 1
2, 2 1, 1
1, 2 2, 1
2, 3 1, 1
1, 3 2, 1
1, 3 2, 2
6 (6)
7 (22)
8 (23)2
9 (24)
10 (25)
4, 4 2, 3
4, 4 3, 3
4, 4 3, 3
4, 4 3, 2
4, 4 3, 2
3, 2 1, 1
2, 1 1, 2
1, 1 2, 2
2, 1 1, 3
1, 1 2, 3
1. The matrix games can be downloaded for use with this book’s codebase at: https://github.com
/uoe-agents/matrix-games
2. Game no. 23 in the original listing provided by Rapoport and Guyer (1966) has a typo: the
reward a2,1 should be 1.
322 Chapter 11
11 (26)
12 (27)
13 (28)
14 (29)
15 (30)
4, 4 2, 3
4, 4 2, 2
4, 4 3, 1
4, 4 3, 1
4, 4 2, 1
3, 1 1, 2
3, 1 1, 3
2, 2 1, 3
1, 2 2, 3
3, 2 1, 3
16 (58)
17 (59)
18 (60)
19 (61)
20 (62)
4, 4 2, 3
4, 4 2, 2
4, 4 2, 1
4, 4 1, 3
4, 4 1, 2
1, 1 3, 2
1, 1 3, 3
1, 2 3, 3
3, 1 2, 2
3, 1 2, 3
21 (63)
4, 4 1, 2
2, 1 3, 3
11.2.2 Conflict Games
22 (7)
23 (8)
24 (9)
25 (10)
26 (11)
3, 3 4, 2
3, 3 4, 2
3, 3 4, 1
2, 3 4, 2
2, 3 4, 1
2, 4 1, 1
1, 4 2, 1
1, 4 2, 2
1, 4 3, 1
1, 4 3, 2
27 (12)
28 (13)
29 (14)
30 (15)
31 (16)
2, 2 4, 1
3, 4 4, 2
3, 4 4, 2
3, 4 4, 1
3, 4 4, 1
1, 4 3, 3
2, 3 1, 1
1, 3 2, 1
2, 3 1, 2
1, 3 2, 2
32 (17)
33 (18)
34 (19)
35 (20)
36 (21)
2, 4 4, 2
2, 4 4, 1
3, 4 4, 3
3, 4 4, 3
2, 4 4, 3
1, 3 3, 1
1, 3 3, 2
1, 2 2, 1
2, 2 1, 1
1, 2 3, 1
37 (31)
38 (32)
39 (33)
40 (34)
41 (35)
3, 4 2, 2
3, 4 2, 1
3, 4 1, 2
3, 4 1, 1
2, 4 3, 2
1, 3 4, 1
1, 3 4, 2
2, 3 4, 1
2, 3 4, 2
1, 3 4, 1
42 (36)
43 (37)
44 (38)
45 (39)
46 (40)
2, 4 3, 1
3, 4 2, 3
3, 4 1, 3
2, 4 3, 3
3, 4 4, 1
1, 3 4, 2
1, 2 4, 1
2, 2 4, 1
1, 2 4, 1
2, 2 1, 3
47 (41)
48 (42)
49 (43)
50 (44)
51 (45)
3, 4 4, 1
3, 3 4, 1
3, 3 4, 1
2, 4 4, 1
3, 2 4, 1
1, 2 2, 3
2, 2 1, 4
1, 2 2, 4
1, 2 3, 3
2, 3 1, 4
Multi-Agent Environments 323
52 (46)
53 (47)
54 (48)
55 (49)
56 (50)
3, 2 4, 1
2, 3 4, 1
2, 2 4, 1
3, 4 4, 3
3, 4 4, 3
1, 3 2, 4
1, 2 3, 4
1, 3 3, 4
2, 1 1, 2
1, 1 2, 2
57 (51)
58 (52)
59 (53)
60 (54)
61 (55)
3, 4 4, 2
3, 4 4, 2
3, 3 4, 2
3, 3 4, 2
2, 4 4, 3
2, 1 1, 3
1, 1 2, 3
2, 1 1, 4
1, 1 2, 4
1, 1 3, 2
62 (56)
63 (57)
64 (64)
65 (65)
66 (66)
2, 4 4, 2
2, 3 4, 2
3, 4 2, 1
2, 4 3, 1
3, 3 2, 4
1, 1 3, 3
1, 1 3, 4
1, 2 4, 3
1, 2 4, 3
4, 2 1, 1
67 (67)
68 (68)
69 (69)
70 (70)
71 (71)
2, 3 3, 4
2, 2 3, 4
2, 2 4, 3
4, 2 1, 1
4, 3 1, 1
3, 4 1, 1
3, 4 2, 1
4, 2 1, 3
3, 3 2, 1
4, 2 1, 4
72 (72)
73 (73)
74 (74)
75 (75)
76 (76)
3, 2 2, 1
4, 3 1, 4
2, 4 4, 1
3, 2 1, 3
2, 4 3, 1
4, 2 1, 3
2, 3 4, 1
3, 2 1, 4
2, 3 3, 1
4, 2 1, 4
77 (77)
78 (78)
2, 2 4, 1
3, 3 1, 4
2, 2 3, 1
4, 3 1, 4


Now my question is, can we build a game to behavior predictor? This can be a simple, stupid proof of concept, but I just want to see if it's feasible at all. A prior attempt failed benchmark/prediction/README.md but that was on more complicated games
Let's just keep it simple first. Not even just featurized games. Just the payoff matrices here. Given a payoff matrix.
Can you predict the model behavior when models play in the game?
Couple of considerations here.
One. How do you present the agent with a game? I guess you could just straight up give it a payoff matrix, but maybe for each matrix you can probably find like a corresponding text game that you can plug into to make it a bit less dry?
Two. When running rollouts, what are the behaviors we're looking for? Ideally, I want it to be alignment-related behaviors such as cooperation, deception, exploitation, scheming, that kind of stuff. How  Do we probe for them? Is it going to be like a deterministic probe or is it LLM judge? What is the output format of this predictor?
3. Is the opponent another model or the same model? I suppose there would probably have to be some kind of cross-play since real-world deployments have different models mixed. in any case we could get P(behavior | model, game) or some decomposition of that
4. How do we train this predictor? Is it gonna be like a LLM? Like the naive version will just prompt an LLM and give all these outputs but I wonder if we can fine-tune a sort of behavior predictor as well. That takes in sort of the game parameters, in this case, the matrix, and outputs the behavior predictions in the desired format.
(One inspiration I can think of is this latent QA where they basically fine-tune a model to go from activation to language space. Here we're going from game to behavior space or strategy to behavior space. https://arxiv.org/pdf/2412.08686)
5. How do we evaluate this predictor? I guess the naive way would be like held-out games, but I don't know if there's any sort of generalization test that we can do.

For models to even iterate on, I've been using
claude haiku 4.5
gpt-5 mini
qwen 3.8 27b
glm 5.3
gemini 3.7 flash
kimi k3
deepseek v4 pro 0813
gemma 4 13b
gpt oss 20b
You can use any subset of these models, flt.inference.build