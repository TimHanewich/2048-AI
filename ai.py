import tensorflow
import Py2048_Engine.Game
import numpy as np
import tools
import copy

layer_input:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(176, "relu")
layer_h1:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(250, "relu")
layer_h2:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(200, "relu")
layer_h3:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(150, "relu")
layer_h4:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(100, "relu")
layer_h5:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(50, "relu")
layer_output:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(4)

model:tensorflow.keras.Sequential = tensorflow.keras.Sequential()
model.add(layer_input)
model.add(layer_h1)
model.add(layer_h2)
model.add(layer_h3)
model.add(layer_h4)
model.add(layer_h5)
model.add(layer_output)
model.compile("adam", "mean_squared_error")

print("Model assembled.")

class MoveDecision:
    input:list[int] = [] # 176 long
    output:list[float] = [] # 4 long (up, right, down, left)
    output_polarized:list[int] = [] # 4 long, but the decision that was made is 1, the decision that was not made is 0. THIS IS WHAT WILL BE USED FOR TRAINING

# plays until win, loss, or frozen (AI keeps just doing the same thing over and over again and the game goes nowhere)
def self_play(model:tensorflow.keras.Sequential, g:Py2048_Engine.Game.Game) -> list[MoveDecision]:

    ToReturn:list[MoveDecision] = []
    while True:
        
        # predict
        inputs = tools.game_to_training_array(g)
        inputs_np = np.array([inputs])
        output = model.predict(inputs_np, verbose=False)

        # create a MoveDecision and add it
        md:MoveDecision = MoveDecision()
        md.input = inputs
        md.output = output[0]

        # polarize
        if md.output[0] == max(md.output):
            md.output_polarized = [1, 0, 0, 0]
        elif md.output[1] == max(md.output):
            md.output_polarized = [0, 1, 0, 0]
        elif md.output[2] == max(md.output):
            md.output_polarized = [0, 0, 1, 0]
        elif md.output[3] == max(md.output):
            md.output_polarized = [0, 0, 0, 1]

        # save the MoveDecision
        ToReturn.append(md)

        # move - up, right, down, left. But quit if an exception (either game won or game loss) is thrown
        board_before = copy.deepcopy(g.getBoard())
        try:
            if md.output_polarized[0] == 1:
                g.up()
            elif md.output_polarized[1] == 1:
                g.right()
            elif md.output_polarized[2] == 1:
                g.down()
            elif md.output_polarized[3] == 1:
                g.left()
        except:
            break

        # if the board, after our move, is the same as what it was before our move, we are frozen. So stop playing and return
        board_after = g.getBoard()
        if board_after == board_before:
            break
    
    return ToReturn
        
        

# Train
while True:

    game1:Py2048_Engine.Game.Game = Py2048_Engine.Game.Game()
    game2:Py2048_Engine.Game.Game = Py2048_Engine.Game.Game()

    # play game 1 + 2
    game1_data:list[MoveDecision] = self_play(model, game1)
    game2_data:list[MoveDecision] = self_play(model, game2)

    # determine which game was more successful
    best_game:int = 0 # 0 = tie, 1 = game 1 was more successful, 2 = game 2 was more successful
    game1_max = tools.max_value(game1)
    game2_max = tools.max_value(game2)
    game1_total = tools.total_value(game1)
    game2_total = tools.total_value(game2)

    # first, judge on the max (high)
    if game1_max > game2_max:
        best_game = 1
    elif game2_max > game1_max:
        best_game = 2
    else: # it was a tie on the high number

        # second, judge on number of moves (fewer moves with the same max value are more efficient)
        if game1.numMoves < game2.numMoves:
            best_game = 1
        elif game2.numMoves < game1.numMoves:
            best_game = 2
        else:

            # third, judge on total score
            if game1_total > game2_total:
                best_game = 1
            elif game2_total > game1_total:
                best_game = 2
            else:
                best_game = 0

    # print
    if best_game == 1:
        print("Achieved high: " + str(game1_max))
        print("Achieved total: " + str(game1_total))
    elif best_game == 2:
        print("Achieved high: " + str(game2_max))
        print("Achieved total: " + str(game2_total))
    
    # Select the best decisions
    correct_decisions:list[MoveDecision] = None
    if best_game == 1:
        correct_decisions = game1_data
    elif best_game == 2:
        correct_decisions = game2_data
    else:
        correct_decisions = None

    # train
    if correct_decisions != None:

        # assemble a list of input & output scenarios
        inputs:list[list[int]] = []
        outputs:list[list[int]] = []
        for md in correct_decisions:
            inputs.append(md.input)
            outputs.append(md.output_polarized)

        # turn into numpy arrays
        inputs_np = np.array(inputs)
        ouputs_np = np.array(outputs)

        # fit
        print("Training...")
        model.fit(inputs_np, ouputs_np, epochs=10, verbose=False)

