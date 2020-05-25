
## Abstract
Noughts and crosses is played on a 3x3 grid with each player placing one of their counters (generally Os and Xs) in turn with the aim of completing a set of three adjacent counters as in the example below:

![Animated Game](https://d18l82el6cdm1i.cloudfront.net/uploads/jxT6rHpKRS-output_mdluzf.gif "Animated Game")

Here, I will implement a variety of methods that you could use playing this game and gauge their effectiveness when pitted against each other.

If you want to follow along, the code below can also be found in Google Colaboratory <a href="https://colab.research.google.com/drive/1VnkhVYbkwAfBkIoWlv6ipHecp0LD1Xhq#scrollTo=JV3wgpFCcigN" target="_blank">here</a>

## Menu
[Defining the board](#defining-the-board)  
[Making Moves and Victory Conditions](#making-moves-and-victory-conditions)  
[Time for a Game!](#time-for-a-game)  
[Adding Strategies](#adding-strategies)  


## Defining the board
In order to easily reference any particular place on the grid, we will store the noughts and crosses grid as a list of 3 rows, where each row contains 3 elements. This will allow us to use a co-ordinate style system to identify each place. Initially we want the board to be blank.

```python
board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
```

Let us also define a method for displaying the current state of the board on the screen.

```python
def printBoard(board):
    # Prints the current state of the board to the screen
    print(" " + str(board[0][0]) + " | " + str(board[0][1]) + " | " + str(board[0][2]))
    print("-----------")
    print(" " + str(board[1][0]) + " | " + str(board[1][1]) + " | " + str(board[1][2]))
    print("-----------")
    print(" " + str(board[2][0]) + " | " + str(board[2][1]) + " | " + str(board[2][2]))
    print("")

```

Output:
```
   |   |  
-----------
   |   |  
-----------
   |   |  
```

## Making Moves and Victory Conditions
Now that we have a board to play the game on, we need a method to make a move.  The simplest strategy (and probably how we all started when we were kids) is to select a random place that doesn't already contain a counter.  To do this, we will generate two random numbers between 0 and 1 and translate this pair to a set of co-ordinates (row, column).  However, that space may already be occupied in which case we will need to select again until we find a blank space.  Once this has been achieved we will place our counter, great!

Let's define our function that selects a random move. We will need to pass it the current board state and we will return a row/column position. Here is the code:

```python
from random import random
import math
def getRandomCell(board):
    # Pick a random place and test if it has been used yet.  
    # When we find an empty place, we have our move
    valid = False
    while valid == False:
        row = math.floor(random() * 3)
        col = math.floor(random() * 3)
        if (board[row][col] == " "): 
            # If the cell is empty then we have a valid move!
            valid = True
            
    return row, col

def makeMove(board, Me):
  row, col = getRandomCell(board)
  board[row][col] = Me

```

Now that we have a method to select a move to play, we now need a method to determine if there is a winner. We know that the game is won when either player is able to place a counter that completes a set of three in a row.  There are 8 winning combinations that achieve this and each correspond to one of the three rows, three columns and two diagonals. If each place in these combinations is equal and not empty then this will indicate a winner. Let us define a method of determining if all items in a list are equal.  Note how we need to be careful not to say that someone has won the game if we find an empty combination!

```python
def checkEqual(lst):
    # Checks to see if all elements in a given list are equal
    for item in range(len(lst)):
        if (lst[item] == " "): 
            # We want to avoid returning false winners for an empty row
            return False

    # Quick check to see if two lists are equal
    return lst[1:] == lst[:-1] 

```

Now that we can check if all items in a list are equal, we will check each winning combination.

```python
def checkVictory(board):
    # Checks the current state of the board to see if anyone has won
    #############################################
    # Possible victories:
    #
    #  X | X | X    O | - | -    X | - | -
    # -----------  -----------  -----------
    #  - | - | -    O | - | -    - | X | -
    # -----------  -----------  -----------
    #  - | - | -    O | - | -    - | - | X
    #      3            3            2 
    #
    # We will check each list in turn
    #############################################

    # This will check each row
    for row in range(3):
        Victory = checkEqual([board[row][0], board[row][1], board[row][2]])
        if (Victory == True): 
            # We have found a winner, return the symbol for the winning player.
            return board[row][0]

    # This will check each column
    for col in range(3):
        Victory = checkEqual([board[0][col], board[1][col], board[2][col]])
        if (Victory == True): 
            # We have found a winner, return the symbol for the winning player.
            return board[0][col]

    # Now check the two diagonals
    Victory = checkEqual([board[0][0], board[1][1] ,board[2][2]])
    if (Victory == True): 
        # We have found a winner, return the symbol for the winning player.
        return board[0][0]

    Victory = checkEqual([board[0][2], board[1][1] ,board[2][0]])
    if (Victory == True): 
        # We have found a winner, return the symbol for the winning player.
        return board[0][2]

    # If we reach this point then we have no winner
    return "Draw"

```
 

## Time for a Game!
We are now in a position to pit two players against each other.

```python
def playGame(board):  
    # Plays a game
    winner = "Draw"
    move = 0
    # Ensure the board is reset at the beginning of a game
    board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]] 

    # We will keep allowing moves until there is either a winner or the board is full 
    while winner == "Draw" and move < 9: 
      if (move % 2 == 0): 
          # Make a move for player 1
          makeMove(board, "O")
      else: 
          # Make a move for player 2
          makeMove(board, "X")
        
      print("Moves: " + str(move))
      printBoard(board)
      
      winner = checkVictory(board)

      # Increment the move count
      move = move + 1

    return winner

playGame(board)

```
Output:
```
Moves: 0
 O |   |  
-----------
   |   |  
-----------
   |   |  

Moves: 1
 O |   |  
-----------
   |   |  
-----------
   |   | X

Moves: 2
 O |   |  
-----------
   | O |  
-----------
   |   | X

Moves: 3
 O | X |  
-----------
   | O |  
-----------
   |   | X

Moves: 4
 O | X |  
-----------
   | O |  
-----------
 O |   | X

Moves: 5
 O | X |  
-----------
 X | O |  
-----------
 O |   | X

Moves: 6
 O | X | O
-----------
 X | O |  
-----------
 O |   | X

'O'
```
 

## Adding Strategies
After playing a few games, we can see that the computer doesn't really understand what influence the moves that it makes has on the game. Often it will select a different place than one that would win it the game. We can 'fix' that by allowing the computer to check if there is a possibility it can win before it selects where to place its counter.

We can do this by using a similar approach to checking if there has been a victory. However, instead of checking each combination for containing the same counter, we will count the number of our own counters (Me) and the number of our opponents counters (Enemy). If there is a set that has two of our counters and none of our opponents then we will select that place as our move, hence winning the game. If no such move is found then we will return -1, -1 to indicate this.

```python
def checkWinningCell(board, Me, Enemy):
    # As with checkVictory here is a list of winning combinations that we need to look at
    #############################################
    # Possible victories:
    #
    #  X | X | X    O | - | -    X | - | -
    # -----------  -----------  -----------
    #  - | - | -    O | - | -    - | X | -
    # -----------  -----------  -----------
    #  - | - | -    O | - | -    - | - | X
    #      3            3            2 
    #
    # We will check each list in turn
    #############################################

    # This will check each row
    for row in range(3):
        NumEnemy = [board[row][0], board[row][1], board[row][2]].count(Enemy)
        NumMe = [board[row][0], board[row][1], board[row][2]].count(Me)
        if (NumMe == 2 and NumEnemy == 0): 
            return row, board[row].index(" ")

    # Now check each column
    for col in range(3):
        NumEnemy = [board[0][col], board[1][col], board[2][col]].count(Enemy)
        NumMe = [board[0][col], board[1][col], board[2][col]].count(Me)
        if (NumMe == 2 and NumEnemy == 0): 
            return [board[0][col], board[1][col], board[2][col]].index(" "), col


    # Now check the two diagonals
    NumEnemy = [board[0][0], board[1][1] ,board[2][2]].count(Enemy)
    NumMe = [board[0][0], board[1][1] ,board[2][2]].count(Me)
    if (NumMe == 2 and NumEnemy == 0): 
        return [board[0][0], board[1][1], board[2][2]].index(" "), [board[0][0], board[1][1], board[2][2]].index(" ")
    
    NumEnemy = [board[0][2], board[1][1], board[2][0]].count(Enemy)
    NumMe = [board[0][2], board[1][1], board[2][0]].count(Me)
    if (NumMe == 2 and NumEnemy == 0): 
        return [board[0][2], board[1][1], board[2][0]].index(" "), [board[2][0], board[1][1], board[0][2]].index(" ")

    return -1, -1

```

Let us update our makeMove & playGame methods to utilise this strategy:

```python
def makeMove(board, Me, Enemy, strategy):
  if (strategy == "Random"):
    row, col = getRandomCell(board)
  elif (strategy == "WinRandom"):
    row, col = checkWinningCell(board, Me, Enemy)
    if (row == -1):
      # If no winning move is found, then we will select a random cell
      row, col = getRandomCell(board)

  board[row][col] = Me
  
def playGame(board):  
    # Plays a game
    winner = "Draw"
    move = 0
    board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]] # Ensure the board is reset at the beginning of a game

    while winner == "Draw" and move < 9: 
      # We will keep allowing moves until there is either a winner or the board is full after 9 moves

      if (move % 2 == 0): 
          # Make a move for player 1
          makeMove(board, "O", "X", "WinRandom")
      else: 
          # Make a move for player 2
          makeMove(board, "X", "O", "WinRandom")
        
      print("Moves: " + str(move))
      printBoard(board)
      
      winner = checkVictory(board)

      # Increment the move count
      move = move + 1

    return winner

playGame(board)

```
Output:
```
Moves: 0
   |   |  
-----------
 O |   |  
-----------
   |   |  

Moves: 1
   | X |  
-----------
 O |   |  
-----------
   |   |  

Moves: 2
   | X |  
-----------
 O |   | O
-----------
   |   |  

Moves: 3
   | X |  
-----------
 O |   | O
-----------
   |   | X

Moves: 4
   | X |  
-----------
 O | O | O
-----------
   |   | X

'O'
```
Promising! It looks as though this method is a 'better' player than the initial random method. However, it still has its flaws. While it correctly identifies when it can win, it doesn't use this logic to block when the opponent can win. Let us fix this.

```python
def makeMove(board, Me, Enemy, strategy):
  if (strategy == "Random"):
    row, col = getRandomCell(board)
  elif (strategy == "WinRandom"):
    row, col = checkWinningCell(board, Me, Enemy)
    if (row == -1):
      # If no winning move is found, then we will select a random cell
      row, col = getRandomCell(board)
  elif (strategy == "WinBlockRandom"):
      row, col = checkWinningCell(board, Me, Enemy)
      if (row == -1):
        # If no winning move is found, then check if we need to block our opponent
        row, col = checkWinningCell(board, Enemy, Me)
        if (row == -1):
          row, col = getRandomCell(board)

  board[row][col] = Me
  
def playGame(board):  
    # Plays a game
    winner = "Draw"
    move = 0
    board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]] # Ensure the board is reset at the beginning of a game

    while winner == "Draw" and move < 9: 
      # We will keep allowing moves until there is either a winner or the board is full after 9 moves

      if (move % 2 == 0): 
          # Make a move for player 1
          makeMove(board, "O", "X", "WinBlockRandom")
      else: 
          # Make a move for player 2
          makeMove(board, "X", "O", "WinBlockRandom")
        
      print("Moves: " + str(move))
      printBoard(board)
      
      winner = checkVictory(board)

      # Increment the move count
      move = move + 1

    return winner

playGame(board)

```
Output:
```
Moves: 0
   |   | O
-----------
   |   |  
-----------
   |   |  

Moves: 1
   |   | O
-----------
 X |   |  
-----------
   |   |  

Moves: 2
 O |   | O
-----------
 X |   |  
-----------
   |   |  

Moves: 3
 O | X | O
-----------
 X |   |  
-----------
   |   |  

Moves: 4
 O | X | O
-----------
 X | O |  
-----------
   |   |  

Moves: 5
 O | X | O
-----------
 X | O |  
-----------
   |   | X

Moves: 6
 O | X | O
-----------
 X | O |  
-----------
 O |   | X

'O'
```

Success! Our intuition tells us that each iteration has played 'better' than those before it.  We will test this next time and add some more strategies.