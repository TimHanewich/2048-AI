import Py2048_Engine.Game

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

