import Py2048_Engine.Game
import copy

# converts the current game board into a 176-input for a neural network
def game_to_training_array(g:Py2048_Engine.Game.Game) -> list[int]:

    # create a list of values
    raw_values:list[int] = []
    data = g.getBoard()
    for row in data:
        for column in row:
            raw_values.append(column)

    # go through each of the raw values and convert to an 11-option discrete
    ToReturn:list[int] = []
    for num in raw_values:
        if num == 0 or num == None: # it will be None
            ToReturn.append(1)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
        elif num == 2:
            ToReturn.append(0)
            ToReturn.append(1)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
        elif num == 4:
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(1)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
        elif num == 8:
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(1)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
        elif num == 16:
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(1)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
        elif num == 32:
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(1)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
        elif num == 64:
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(1)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
        elif num == 128:
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(1)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
        elif num == 256:
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(1)
            ToReturn.append(0)
            ToReturn.append(0)
        elif num == 512:
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(1)
            ToReturn.append(0)
        elif num == 1024:
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(0)
            ToReturn.append(1)

    return ToReturn

# finds the max value on the board right now
def max_value(g:Py2048_Engine.Game.Game) -> int:
    ToReturn = 0
    data = g.getBoard()
    for row in data:
        for col in row:
            if col != None:
                if col > ToReturn:
                    ToReturn = col
    
    return ToReturn

# returns the sum of all values on the board
def total_value(g:Py2048_Engine.Game.Game) -> int:
    ToReturn = 0
    data = g.getBoard()
    for row in data:
        for col in row:
            if col != None:
                ToReturn = ToReturn + col
    
    return ToReturn

def concentration(g:Py2048_Engine.Game.Game) -> float:

    sum:int = total_value(g)
    
    # count the number of tiles that have data
    tile_count:int = 0
    data = g.getBoard()
    for row in data:
        for col in row:
            if col != None:
                tile_count = tile_count + 1
    
    return sum / tile_count

# returns a list of move priorities as a list of string (up, right, down, left)
def prioritize_moves(inputs:list[float]) -> list[str]:

    inputs_sorted = sorted(inputs, reverse=True)
    
    ToReturn:list[str] = []
    for i in inputs_sorted:
        if i == inputs[0]:
            ToReturn.append("up")
        elif i == inputs[1]:
            ToReturn.append("right")
        elif i == inputs[2]:
            ToReturn.append("down")
        elif i == inputs[3]:
            ToReturn.append("left")
    return ToReturn

def count_different_tiles(g1:Py2048_Engine.Game.Game, g2:Py2048_Engine.Game.Game) -> int:
    ToReturn:int = 0
    for row in range(0, 4):
        for col in range(0, 4):
            if g1.board[row][col] != g2.board[row][col]:
                ToReturn = ToReturn + 1
    return ToReturn


class MoveOutcome:
    direction:str = None # either "up", "right", "down", or "left"
    game:Py2048_Engine.Game.Game = None # the game output
    
    # statuses
    is_winning:bool = False # this move won the game
    is_losing:bool = False # this move lost the game

def explore(g:Py2048_Engine.Game.Game) -> list[MoveOutcome]:

    ToReturn:list[MoveOutcome] = []
    ToTry:list[str] = ["up", "right", "down", "left"]
    for move in ToTry:

        # create the MoveOutcome
        mc:MoveOutcome = MoveOutcome()
        mc.direction = move
        
        # copy the game
        TheoryGame:Py2048_Engine.Game.Game = Py2048_Engine.Game.Game(copy.deepcopy(g.getBoard()))

        # attempt to move
        try:
            if move == "up":
                TheoryGame.up()
            elif move == "right":
                TheoryGame.right()
            elif move == "down":
                TheoryGame.down()
            elif move == "left":
                TheoryGame.left()
        except Py2048_Engine.Game.GameWonException:
            mc.is_winning = True
        except Py2048_Engine.Game.GameLostException:
            mc.is_losing = True
        

        # only add if there are more than 1 difference between (an addition was made)
        if count_different_tiles(g, TheoryGame) > 1:
            mc.game = TheoryGame
            mc.direction = move
            ToReturn.append(mc)
    
    return ToReturn


