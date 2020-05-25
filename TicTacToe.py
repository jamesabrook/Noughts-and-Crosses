from prettytable import PrettyTable
from copy import deepcopy
from random import random
import math

def printBoard(board):
    # Prints the current state of the board to the screen
    print(" " + str(board[0][0]) + " | " + str(board[0][1]) + " | " + str(board[0][2]))
    print("-----------")
    print(" " + str(board[1][0]) + " | " + str(board[1][1]) + " | " + str(board[1][2]))
    print("-----------")
    print(" " + str(board[2][0]) + " | " + str(board[2][1]) + " | " + str(board[2][2]) + "\n")

def checkEqual(lst):
    # Checks to see if all elements in a given list are equal
    for item in range(3):
        if (lst[item] == " "): 
            # We want to avoid returning false winners for an empty row
            return False

    # This will return true if the subset of items removing the first element is the same as the subset of items removing the last indicating that all elements are equal
    return lst[1:] == lst[:-1] 

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
            if (cfg_DebugStatements == True): print("Winner!")
            return board[row][0]

    # This will check each column
    for col in range(3):
        Victory = checkEqual([board[0][col], board[1][col], board[2][col]])
        if (Victory == True): 
            # We have found a winner, return the symbol for the winning player.
            if (cfg_DebugStatements == True): print("Winner!")
            return board[0][col]

    # Now check the two diagonals
    Victory = checkEqual([board[0][0], board[1][1] ,board[2][2]])
    if (Victory == True): 
        # We have found a winner, return the symbol for the winning player.
        if (cfg_DebugStatements == True): print("Winner!")
        return board[0][0]

    Victory = checkEqual([board[0][2], board[1][1] ,board[2][0]])
    if (Victory == True): 
        # We have found a winner, return the symbol for the winning player.
        if (cfg_DebugStatements == True): print("Winner!")
        return board[0][2]

    # If we reach this point then we have no winner
    return "No Winner"

def getRandomCell(board):
    # Pick a random cell and test if it has been used yet.  When we find an empty cell, place our move
    valid = False
    if (cfg_DebugStatements == True): print("    Checking move")
    while valid == False:
        row = math.floor(random() * 3)
        col = math.floor(random() * 3)
        if (board[row][col] == " "): 
            # If the cell is empty then we have a valid move!
            if (cfg_DebugStatements == True): print("    Move is valid!") 
            valid = True
            
    return row, col

def checkWinningCell(board, Me, Enemy, debugText):
    # As with checkVictory here is a list of winning combinations that we need to block
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
            if (cfg_DebugStatements == True): print(debugText)
            return row, board[row].index(" ")

    # Now check each column
    for col in range(3):
        NumEnemy = [board[0][col], board[1][col], board[2][col]].count(Enemy)
        NumMe = [board[0][col], board[1][col], board[2][col]].count(Me)
        if (NumMe == 2 and NumEnemy == 0): 
            if (cfg_DebugStatements == True): print(debugText)
            return [board[0][col], board[1][col], board[2][col]].index(" "), col


    # Now check the two diagonals
    NumEnemy = [board[0][0], board[1][1] ,board[2][2]].count(Enemy)
    NumMe = [board[0][0], board[1][1] ,board[2][2]].count(Me)
    if (NumMe == 2 and NumEnemy == 0): 
        if (cfg_DebugStatements == True): print(debugText)
        return [board[0][0], board[1][1], board[2][2]].index(" "), [board[0][0], board[1][1], board[2][2]].index(" ")
    
    NumEnemy = [board[0][2], board[1][1], board[2][0]].count(Enemy)
    NumMe = [board[0][2], board[1][1], board[2][0]].count(Me)
    if (NumMe == 2 and NumEnemy == 0): 
        if (cfg_DebugStatements == True): print(debugText)
        return [board[0][2], board[1][1], board[2][0]].index(" "), [board[2][0], board[1][1], board[0][2]].index(" ")

    return -1, -1
    
def emptyCells(board):
    # Calculate the number of empty cells on a given board
    blanks = 0
    for row in range(3):
        for col in range(3):
            if (board[row][col] == " "): blanks = blanks + 1
    
    return blanks

def generateStaticProbabilities(board):
    # Initially we will use a 'dumb' method just using the probability that each cell is part of a winning combination
    
    # The corners each appear in 3 winning sets
    staticProbs[0][0] = 3
    staticProbs[0][2] = 3
    staticProbs[2][0] = 3
    staticProbs[2][2] = 3

    # The middle of a row/column each appear in 2 winning sets
    staticProbs[0][1] = 2
    staticProbs[1][0] = 2
    staticProbs[1][2] = 2
    staticProbs[2][1] = 2

    # The central cell appears in 4 winning sets
    staticProbs[1][1] = 4

    # We will then scale these by the total number of cells used in all possible winning combinations
    for row in range(3):
        for col in range(3):
            staticProbs[row][col] = staticProbs[row][col] / 24

    # Now turn these into a cumulative probability.
    
    for row in range(3):
        for col in range(3):
            if (row == 0 and col == 0):
                staticProbs[row][col] = staticProbs[row][col] + 0
            elif (col == 0):
                staticProbs[row][col] = staticProbs[row][col] + staticProbs[row - 1][2]
            else:
                staticProbs[row][col] = staticProbs[row][col] + staticProbs[row][col - 1]

            if (cfg_DebugStatements == True): print("    " + str(staticProbs[row][col]))

def generateDynamicProbabilities(board, Me, Enemy):
    # Here we want to account for certain cells being taken already, denying a potential winning combination
    # Check each winning combination for an enemy counter

    TotalWinningCells = 0

    # This will check each row
    for row in range(3):
        enemyCounters = [board[row][0], board[row][1], board[row][2]].count(Enemy)
        if (enemyCounters == 0):
            TotalWinningCells = TotalWinningCells + 3
            for col in range(3):
                dynamicProbs[row][col] = dynamicProbs[row][col] + 1

    # This will check each column
    for col in range(3):
        enemyCounters = [board[0][col], board[1][col], board[2][col]].count(Enemy)
        if (enemyCounters == 0):
            TotalWinningCells = TotalWinningCells + 3
            for row in range(3):
                dynamicProbs[row][col] = dynamicProbs[row][col] + 1

    # Now check the two diagonals
    enemyCounters = [board[0][0], board[1][1], board[2][2]].count(Enemy)
    if (enemyCounters == 0):
        TotalWinningCells = TotalWinningCells + 3
        for row in range(3):
            dynamicProbs[row][row] = dynamicProbs[row][row] + 1

    enemyCounters = [board[0][2], board[1][1], board[2][0]].count(Enemy)
    if (enemyCounters == 0):
        TotalWinningCells = TotalWinningCells + 3
        for row in range(3):
            dynamicProbs[row][2 - row] = dynamicProbs[row][2 - row] + 1


    for row in range(3):
        for col in range(3):
            if (TotalWinningCells > 0): dynamicProbs[row][col] = dynamicProbs[row][col] / TotalWinningCells

    for row in range(3):
        for col in range(3):
            if (row == 0 and col == 0):
                dynamicProbs[row][col] = dynamicProbs[row][col] + 0
            elif (col == 0):
                dynamicProbs[row][col] = dynamicProbs[row][col] + dynamicProbs[row - 1][2]
            else:
                dynamicProbs[row][col] = dynamicProbs[row][col] + dynamicProbs[row][col - 1]

            if (cfg_DebugStatements == True): print("    " + str(dynamicProbs[row][col]))

def generateMLProbabilities(board) :
    # From the score that each cell has we will create a probability of placing our counter there

    # Work out the total score of all available cells
    TotalScore = 0
    for row in range(3):
        for col in range(3):
            if (board[row][col] == " "): TotalScore = TotalScore + scores[row][col]
    
    if (cfg_DebugStatements == True): print("    Total Score:" + str(TotalScore))
    # Now use this to create the probability assigned to each cell
    for row in range(3):
        for col in range(3):
            if (board[row][col] == " "):
                mlProbs[row][col] = scores[row][col] / TotalScore
            else: mlProbs[row][col] = 0

    
    for row in range(3):
        for col in range(3):
            if (row == 0 and col == 0):
                mlProbs[row][col] = mlProbs[row][col] + 0
            elif (col == 0):
                mlProbs[row][col] = mlProbs[row][col] + mlProbs[row - 1][2]
            else:
                mlProbs[row][col] = mlProbs[row][col] + mlProbs[row][col - 1]

def getProbabilityCell(board, probabilities):
    valid = False
    while (valid == False):
        cell = random()
        for row in range(3):
            for col in range(3):
                if (probabilities[row][col] > cell and board[row][col] == " "): 
                    if (cfg_DebugStatements == True): 
                        print("    Cell: " + str(cell))
                        print("    Row " + str(row) + " Col: " + str(col))
                    
                    return row, col 

    return -1, -1

def translateBoardSate(board):
    # We will use a key to define each board state.  If a cell is empty then we assign a value of 0, O = 1 and X = 2
    
    boardKey = 0 
    for row in range(3):
        for col in range(3):
            cellkey = row * 3 + col
            if (board[row][col] == "O"): boardKey = boardKey + 1 * 3**cellkey
            elif (board[row][col] == "X"): boardKey = boardKey + 2 * 3**cellkey

    return boardKey

def makeMove(board, Me, Enemy, strategy, moveList):
    # Places a move onto the board based on the selected strategy

    if (cfg_DebugStatements == True): print("Player: " + Me)
    
    if (strategy == "Random"):     
        # Random strategy
        row, col = getRandomCell(board)
        if (cfg_DebugStatements == True): print("Row: " + str(row) + " Col: " + str(col))
        board[row][col] = Me
    elif (strategy == "WinRandom"):
        # Check to see if we have a winning move
        row, col = checkWinningCell(board, Me, Enemy, "    Winning Move!")

        if (cfg_DebugStatements == True): 
            if (row == -1) : print("    No winning move found")
            else: print("    Row: " + str(row) + " Col: " + str(col))

        if (row == -1):
            # If there was no winning move then play a random move
            row, col = getRandomCell(board)

            if (cfg_DebugStatements == True): 
                if (row == -1) : print("    No winning move found")
                else: print("    Row: " + str(row) + " Col: " + str(col))

        board[row][col] = Me
    elif (strategy == "BlockRandom"):
        # Check to see if we have a winning move
        row, col = checkWinningCell(board, Me, Enemy, "    Winning Move!")
        
        if (cfg_DebugStatements == True): 
            if (row == -1) : print("    No winning move found")
            else: print("    Row: " + str(row) + " Col: " + str(col))

        if (row == -1): 
            # We can check for a winning move 'pretending' that we are the enemy player to see if we need to block
            row, col = checkWinningCell(board, Enemy, Me, "    Block Needed!") 

            if (cfg_DebugStatements == True): 
                if (row == -1) : print("    No blocking move found")
                else: print("    Row: " + str(row) + " Col: " + str(col))
            
        if (row == -1):
            # If we didn't need to block then make a random move
            row, col = getRandomCell(board)
            
            if (cfg_DebugStatements == True): 
                if (row == -1) : print("    No winning move found")
                else: print("    Row: " + str(row) + " Col: " + str(col))

        board[row][col] = Me
    elif (strategy == "StaticProbability"):
        # We will first check winning/blocking moves as above
        # If these aren't suffice to select a cell we will use a probability
        # We will calculate a probability for each empty cell that it is part of a winning board for us

        # Check to see if we have a winning move
        row, col = checkWinningCell(board, Me, Enemy, "    Winning Move!")
        
        if (cfg_DebugStatements == True): 
            if (row == -1) : print("    No winning move found")
            else: print("    Row: " + str(row) + " Col: " + str(col))

        if (row == -1): 
            # We can check for a winning move 'pretending' that we are the enemy player to see if we need to block
            row, col = checkWinningCell(board, Enemy, Me, "    Block Needed!") 

            if (cfg_DebugStatements == True): 
                if (row == -1) : print("    No blocking move found")
                else: print("    Row: " + str(row) + " Col: " + str(col))
        
        if (row == -1):
            # The static probabilities never change, so we only need to do this once! 
            if (staticProbs[0][0] == 0): generateStaticProbabilities(board)

            row, col = getProbabilityCell(board, staticProbs)
        board[row][col] = Me
    elif (strategy == "DynamicProbability"):
        # We will first check winning/blocking moves as above
        # If these aren't suffice to select a cell we will use a probability
        # We will calculate a probability for each empty cell that it is part of a winning board for us

        # Check to see if we have a winning move
        row, col = checkWinningCell(board, Me, Enemy, "    Winning Move!")
        
        if (cfg_DebugStatements == True): 
            if (row == -1) : print("    No winning move found")
            else: print("    Row: " + str(row) + " Col: " + str(col))

        if (row == -1): 
            # We can check for a winning move 'pretending' that we are the enemy player to see if we need to block
            row, col = checkWinningCell(board, Enemy, Me, "    Block Needed!") 

            if (cfg_DebugStatements == True): 
                if (row == -1) : print("    No blocking move found")
                else: print("    Row: " + str(row) + " Col: " + str(col))
        
        if (row == -1):
            # The dynamic probabilities change with every move
            generateDynamicProbabilities(board, Me, Enemy)

            row, col = getProbabilityCell(board, dynamicProbs)
        board[row][col] = Me
    elif (strategy == "ReinforcedLearning1"):
        # This strategy doesn't understand how to win or prevent the opponent from winning so just picks a cell based on the mlProbs list
        if (cfg_DebugStatements == True): print("    Making ML Move")
        generateMLProbabilities(board)
        if (cfg_DebugStatements == True): 
            for row in range(3):
                for col in range(3):
                    print("    Prob for " + str(row) + ", " + str(col) + ": " + str(mlProbs[row][col]))
        row, col = getProbabilityCell(board, mlProbs)
    elif (strategy == "ReinforcedLearning2"):
        # Here we will consider each move that we can make and pick the one that returns the highest value 
        bestrow = 0
        bestcol = 0
        maxState = -1
        board2 = []

        for row in range(3):
            for col in range(3):
                board2 = deepcopy(board)
                if (board2[row][col] == " "):
                    board2[row][col] = Me
                    testState = translateBoardSate(board2)
                    if (statevalues[testState] > maxState):
                        bestrow = row
                        bestcol = col
                        maxState = statevalues[testState]
                board2 = []

        row = bestrow
        col = bestcol

    board[row][col] = Me

    # Add the move to the movelist
    boardKey = translateBoardSate(board)
    moveList.append(boardKey)

def updateScores(board, Me):
    # We will update the scores for the ML model after each game
    for row in range(3):
        for col in range(3):
            if (board[row][col] == Me): scores[row][col] = scores[row][col] + 5
            elif (board[row][col] != Me and Me != "Draw"): 
                scores[row][col] = scores[row][col] - 1
                if (scores[row][col] == 0): 
                    # Ensure a cell is never impossible to place a counter on
                    scores[row][col] = 1

def updateStateValues(moveList, Player1, Player2, Winner):
    for move in range(len(moveList)):
        if (move % 2 == 0):
            if (Winner == Player1):
                statevalues[moveList[move]] = statevalues[moveList[move]] + 11
            elif (Winner == Player2):
                statevalues[moveList[move]] = statevalues[moveList[move]] - 5
                if (statevalues[moveList[move]] < 0): statevalues[moveList[move]] = 1
        else:
            if (Winner == Player2):
                statevalues[moveList[move]] = statevalues[moveList[move]] + 11
            elif (Winner == Player1):
                statevalues[moveList[move]] = statevalues[moveList[move]] - 5
                if (statevalues[moveList[move]] < 0): statevalues[moveList[move]] = 1

def playGame(board, cfg_Player1Strategy, cfg_Player2Strategy):  
    # Plays a game
    winner = "No Winner"
    moves = 0
    moveList = []
    while winner == "No Winner" and moves < 9: 
        # We will keep allowing moves until there is either a winner or the board is full after 9 moves

        if (moves % 2 == 0): 
            # Make a move for player 1
            makeMove(board, cfg_Player1, cfg_Player2, cfg_Player1Strategy, moveList)
        else: 
            # Make a move for player 2
            makeMove(board, cfg_Player2, cfg_Player1, cfg_Player2Strategy, moveList)
        
        if (cfg_PrintBoard == True): print("Move: " + str(moves) + " (" + str(moveList[moves]) + ")\n")
        if (cfg_PrintBoard == True): printBoard(board)
        if (cfg_DebugStatements == True): print("Checking for a winner")
        
        winner = checkVictory(board)
        if (cfg_DebugStatements == True): print(winner)
        
        # Increment the move count
        moves = moves + 1
    
    # Final position
    if (cfg_PrintResult == True):
        if (winner in [cfg_Player1, cfg_Player2]): print(str(winner) + " won! Final position: ")
        else: print("No Winner! Final position: ")
        printBoard(board)

    if (cfg_Player1Strategy == "ReinforcedLearning1" or cfg_Player2Strategy == "ReinforcedLearning1"):
        updateScores(board, winner)

    if (cfg_Player1Strategy == "ReinforcedLearning2" or cfg_Player2Strategy == "ReinforcedLearning2"):
        updateStateValues(moveList, cfg_Player1, cfg_Player2, winner)

    return winner

def printRecord(record):
    t = PrettyTable(tableheader)
    for row in range(len(strategies)):
        rowdata = [strategies[row]]
        for x in range(len(strategies)):
            rowdata.append(record[row][x])
        t.add_row(rowdata)
    print(t)

def printStateValues(board, Me):
    # Given a particular board state, print the statevalues for each move
    board2 = []

    for row in range(3):
        for col in range(3):
            board2 = deepcopy(board)
            if (board2[row][col] == " "):
                board2[row][col] = Me
                testState = translateBoardSate(board2)
                printBoard(board2)
                print("Value: " + str(statevalues[testState]))
            board2 = []

def loopGames(TrainingGames, TestingGames):

    for strat in range(len(trainingstrategies)):
        cfg_Player1Strategy = trainingstrategies[strat]
        cfg_Player2Strategy = "DynamicProbability"
        for _1 in range(TrainingGames):
            board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
            winner = playGame(board, cfg_Player1Strategy, cfg_Player2Strategy)

        # if (winner == cfg_Player1):
        #     player1 = player1 + 1
        # elif (winner == cfg_Player2):
        #     player2 = player2 + 1
        # else: draw = draw + 1

    for strat1 in range(len(strategies)):
        for strat2 in range(len(strategies)):
            player1 = 0
            player2 = 0
            draw = 0
            cfg_Player1Strategy = strategies[strat1]
            cfg_Player2Strategy = strategies[strat2]

            for _1 in range(TrainingGames):
                board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
                winner = playGame(board, cfg_Player1Strategy, cfg_Player2Strategy)

            
            for _1 in range(TestingGames):
                board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
                winner = playGame(board, cfg_Player1Strategy, cfg_Player2Strategy)

                if (winner == cfg_Player1):
                    player1 = player1 + 1
                elif (winner == cfg_Player2):
                    player2 = player2 + 1
                else: draw = draw + 1

                record[strat1][strat2] = '%03d' % player1  + " / " + '%03d' % draw + " / " + '%03d' % player2

            # print("Games won by " + str(cfg_Player1) + " (" + str(cfg_Player1Strategy) + "): " + str(player1) + "/" + str(NumGames))
            # print("Games won by " + str(cfg_Player2) + " (" + str(cfg_Player2Strategy) + "): " + str(player2) + "/" + str(NumGames))
            # print("Games drawn: " + str(draw) + "/" + str(NumGames))
    printRecord(record)
    

#############################################
# Config Statements
#############################################
cfg_PrintBoard = False
cfg_DebugStatements = False
cfg_PrintResult = False
cfg_Player1 = "O"
# cfg_Player1Strategy = "WinRandom" 
cfg_Player2 = "X"
# cfg_Player2Strategy = "Probability"

#############################################
# Setup Game
#############################################
board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
staticProbs = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
dynamicProbs = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
mlProbs = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
scores = [[100, 100, 100], [100, 100, 100], [100, 100, 100]]

statevalues = [100 for i in range(3**9)]


trainingstrategies = ["ReinforcedLearning1", "ReinforcedLearning2"]
strategies = ["Random", "WinRandom", "BlockRandom", "StaticProbability", "DynamicProbability", "ReinforcedLearning1", "ReinforcedLearning2"]
tableheader = ["P1 / D / P2", "Random", "WinRandom", "BlockRandom", "StaticProbability", "DynamicProbability", "ReinforcedLearning1", "ReinforcedLearning2"]
record = [["" for x in range(len(strategies))] for y in range(len(strategies))]

if (cfg_PrintBoard == True): printBoard(board)

loopGames(1000, 1000)
cfg_PrintBoard = True
board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
printStateValues(board, "O")