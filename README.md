# AI-Game



**AI Term Project** － **Search**

**Spring 2020**

Due Date: 11:50 PM April 30, 2020

**1. Project objective:**

Design an AI program to play a two-player n´n (n = 4 or 6) board game.

**2. Language:**

Any commonly used programming language, e.g. C/C++, Java, Python, etc.

**3. What to turn in:**

(a) A report of the search strategy of your own design (be precise).

(b) A copy of your source code (be correct, i.e. it compiles and runs).

(c) A document explaining how to run your code (be clear).

(d) A complete program output that shows the sequence of moves for a pilot test (posted on e3 later).

Note. A fancy output is not required. Just clearly show the alternating moves made by you and your

AI program (be neat, not necessarily fancy).

**4. Grading policy:**

(a) You will get reasonable points for your project if you turn in what you are supposed to even though

your AI program is not among the top-ranking programs in class.

(b) The higher ranking, the more points.

(c) To be fair, an incomplete project will incur a low grade.

**5. Game Rules:**

a. In 4\*4 board, each player has 5 numbered cards: [2, 3, 5, 8, 13].

b. In 6\*6 board, each player has 11 numbered cards: [2, 2, 3, 3, 5, 5, 8, 8, 8, 13, 13]. In other word,

you have two ‘2’, ‘3’, ‘5’, and ‘13’ cards and three ‘8’ cards.

Ex: (Row, Col) －Top left corner －> (0, 0)

**4**´**4**

**6**´**6**

(0,0)

(0,3)

(3,3)

**6**´**6 board:**

Player 1: [2, 2, 3, 3, 5, 5, 8, 8, 8, 13, 13]

Player 2: [2, 2, 3, 3, 5, 5, 8, 8, 8, 13, 13]

(3,0)

**4**´**4 board:**

Player 1: [2, 3, 5, 8, 13]

Player 2: [2, 3, 5, 8, 13]

c. A card on the board will be removed from the rest of the game if “the total of the numbers of the

card and its surrounding 8 cards exceeds 15 (> 15)”.





d. The players take turns. Immediately after one player places a card in hand in a position on the

board by choice, all cards on the board will be checked for removal and marked first. Once the

inspection is complete, those cards marked for removal are then removed from the board.

Note 1. Any card that has been removed cannot be reused for the rest of the game.

Note 2. The position from which a card is removed cannot be reused either, i.e. you cannot place

another card in that position later.

EX1: Check Card 3 for removal

5

3

5

5

X

**3+5+8 = 16**

3\*

**16 > Limit (15)**

8

8

8

**Mark 3 with an asterisk \***

EX2:

The order of checking 8, 13 and 5 does not matter because you “check-and-mark” before

“remove.”

e. The game ends when both players have NO cards in hand.

Note you must place one card on the board in your turn when you still cards in hand, i.e. no

“PASS” here.

f. Your final score is the sum of your cards’ numbers on the board.

EX3:

**X**

**X**

**X**

**X**

**5**

**2**

**X**

**8**

**Player 1 final score: Score(player 1)= 2 + 5 + 8 = 15**

**Player 2 final score: Score(player 2)= 13 + 2 = 15**

**2**

**13**

g. **Winning Rule**:

(1) If Score(player 1) > Score(player 2), then winner is player 1.

(2) If Score(player 1) < Score(player 2), then winner is player 2.

(3) If Score(player 1) = Score(player 2), then the player who holds a card number larger than all





his(her) opponent’s is the winner, e.g. in EX3, player 2 is the winner because he(she) holds 13,

which is larger than 2, 5 and 8 of his(her) opponent.

**6. Game Flow:**

a. Your AI program enquires who will make the first move, AI or Human.

b. Your AI program enquires about the board size, 4´4 or 6´6.

c. **For AI’s turns:**

i. Your AI program shows how it plays by presenting: (Row, Column, Card Number)

ii. Check-and-Mark

iii. Remove marked cards if any.

**For Human turns:**

iv. Place a card by presenting: (Row, Column, Card Number)

v. Check-and-Mark

vi. Remove marked cards if any.

d. Repeat c until it reaches an end game.

e. **Final Output:**

Show the winner.

**7. Other requirements:**

\1. The time limit for a single move is 30 seconds.

\2. The video clips are posted on Google for your reference.

<https://drive.google.com/open?id=1PmB9JU35Zn25kN8Uet4xSoH3SIKidK2e>



