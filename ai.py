import tensorflow
import Py2048_Engine.Game
import numpy as np
import tools
import copy
import math
import os
import datetime

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

    # before
    max_value_before:int = 0
    concentration_before:float = 0.0

    # after
    max_value_after:int = 0
    concentration_after:float = 0.0

    # raw input + output from the model
    input:list[int] = [] # 176 long
    output_polarized:list[int] = [] # 4 long, but the decision that was made is 1, the decision that was not made is 0. THIS IS WHAT WILL BE USED FOR TRAINING

    def gain(self) -> float:
        
        # concentration leap, as a percentage
        ToReturn = (self.concentration_after - self.concentration_before) / self.concentration_before

        # if the max value jumped, add a little
        if self.max_value_after > self.max_value_before:
            ToReturn = ToReturn * 1.35


        return ToReturn

def sort_by_gain(mds:list[MoveDecision]) -> list[MoveDecision]:

    # calculate
    ToSort:list[tuple[MoveDecision, float]] = []
    for md in mds:
        ToSort.append((md, md.gain()))
    
    # sort
    ToReturn:list[tuple[MoveDecision, float]] = []
    while len(ToSort) > 0:
        winner = ToSort[0]
        for tup in ToSort:
            if tup[1] > winner[1]:
                winner = tup
        ToReturn.append(winner)
        ToSort.remove(winner)

    # create a list of just the MoveDecision
    ToReturnMDs:list[MoveDecision] = []
    for da in ToReturn:
        ToReturnMDs.append(da[0])

    return ToReturnMDs


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
        md.max_value_before = tools.max_value(g)
        md.concentration_before = tools.concentration(g)

        # priotizie the list of moves
        priorities:list[str] = tools.prioritize_moves(md.output)
        
        # attempt to move based on that list, until we confirm a change has been made
        game_over:bool = False
        move_has_been_made:bool = False
        for priority in priorities:
            if move_has_been_made == False and game_over == False:

                # take note of the current position
                board_before = copy.deepcopy(g.getBoard())

                # try to make the move
                try:
                    if priority == "up":
                        g.up()
                    elif priority == "right":
                        g.right()
                    elif priority == "down":
                        g.down()
                    elif priority == "left":
                        g.left()
                except:
                    game_over = True

                # check to see if the board now is different than it was before
                board_after = copy.deepcopy(g.getBoard())
                if board_after != board_before:

                    # mark that a move has been made
                    move_has_been_made = True

                    # save the after statistics
                    md.max_value_after = tools.max_value(g)
                    md.concentration_after = tools.concentration(g)

                    # write to the decision
                    if priority == "up":
                        md.output_polarized = [1, 0, 0, 0]
                    elif priority == "right":
                        md.output_polarized = [0, 1, 0, 0]
                    elif priority == "down":
                        md.output_polarized = [0, 0, 1, 0]
                    elif priority == "left":
                        md.output_polarized = [0, 0, 0, 1]
                
                    # add the move decision, only if a move was confirmed made
                    ToReturn.append(md)

        # if it is game over, return
        if game_over:
            return ToReturn


# training params
save_model_every_seconds = 1800
save_to_directory = r"C:\Users\timh\Downloads\tah\2048-ai\models"


# Train
last_saved_at = datetime.datetime.utcnow()
while True:

    g:Py2048_Engine.Game.Game = Py2048_Engine.Game.Game()

    # play game
    print("Playing game...")
    game_data:list[MoveDecision] = self_play(model, g)

    # print the high
    game_max:int = tools.max_value(g)
    game_concentration:float = tools.concentration(g)
    print("Game Max: " + str(game_max) + ", Game Concentration: " + str(round(game_concentration, 1)))

    # sort the game data by concentration gain
    game_data_sorted:list[MoveDecision] = sort_by_gain(game_data)

    # select the ones we will train on
    TopPercentToTrain = 0.10
    CountToTrain = math.floor(len(game_data_sorted) * TopPercentToTrain)
    ToTrain:list[MoveDecision] = []
    for x in range(0, CountToTrain):
        ToTrain.append(game_data_sorted[x])

    
    # Establish a list of training data (inputs + outputs)
    inputs:list[list[int]] = [] #A list of "board positions" (scenarios) as the input
    outputs:list[list[int]] = [] # A list of the decision that was made (correctly) in each scenario
    for md in ToTrain:
        # assemble a list of input & output scenarios
        inputs.append(md.input)
        outputs.append(md.output_polarized)

    # turn into numpy arrays
    inputs_np = np.array(inputs)
    ouputs_np = np.array(outputs)

    # fit
    print("Training...")
    model.fit(inputs_np, ouputs_np, epochs=3000, verbose=False)

    # if the amount of time since the last training has surpassed the limit, save
    time_since_save:datetime.timedelta = datetime.datetime.utcnow() - time_since_save
    if time_since_save.total_seconds() >= save_model_every_seconds:

        print("It is time to save!")

        # create a folder
        save_to:str = save_to_directory + "\\" + str(datetime.datetime.utcnow())
        print("Making directory '" + save_to + "'...")
        os.mkdir(save_to)

        # save to folder
        print("Saving...")
        model.save(save_to)

        # update the saved time
        last_saved_at = datetime.datetime.utcnow()

