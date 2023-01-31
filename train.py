import tensorflow
import Py2048_Engine.Game
import numpy as np
import tools
import copy
import math
import os
import datetime
import ai_tools

# load model?
model_path:str = r"C:\Users\timh\Downloads\tah\2048-ai\models2\2023-01-31 19-53-53.895138"
model:tensorflow.keras.Sequential = None
if model_path != None and model_path != "":
    print("Loading model from '" + model_path + "'")
    model = tensorflow.keras.models.load_model(model_path)
else:
    print("A model path was not provided! Constructing a new model...")

    layer_input:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Input(176)
    layer_h1:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(300, "relu")
    layer_h2:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(220, "relu")
    layer_h3:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(180, "relu")
    layer_h4:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(140, "relu")
    layer_h5:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(120, "relu")
    layer_h6:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(100, "relu")
    layer_h7:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(80, "relu")
    layer_output:tensorflow.keras.layers.Dense = tensorflow.keras.layers.Dense(4)

    model = tensorflow.keras.Sequential()
    model.add(layer_input)
    model.add(layer_h1)
    model.add(layer_h2)
    model.add(layer_h3)
    model.add(layer_h4)
    model.add(layer_h5)
    model.add(layer_h6)
    model.add(layer_h7)
    model.add(layer_output)
    model.compile("adam", "mean_squared_error")

print("Model assembled.")



# training params
save_model_every_seconds = 600
save_to_directory = r"C:\Users\timh\Downloads\tah\2048-ai\models2"


# Train
last_saved_at = datetime.datetime.utcnow()  - datetime.timedelta(hours=1)
while True:

    g:Py2048_Engine.Game.Game = Py2048_Engine.Game.Game()

    # play game
    print("Playing game...")
    game_data:list[ai_tools.MoveDecision] = ai_tools.self_play(model, g)

    # print the high
    game_max:int = tools.max_value(g)
    game_concentration:float = tools.concentration(g)
    print("Game Max: " + str(game_max) + ", Game Concentration: " + str(round(game_concentration, 1)))

    # sort the game data by concentration gain
    game_data_sorted:list[ai_tools.MoveDecision] = ai_tools.sort_by_gain(game_data)

    # select the ones we will train on
    TopPercentToTrain = 0.10
    CountToTrain = math.floor(len(game_data_sorted) * TopPercentToTrain)
    ToTrain:list[ai_tools.MoveDecision] = []
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
    time_since_save:datetime.timedelta = datetime.datetime.utcnow() - last_saved_at
    if time_since_save.total_seconds() >= save_model_every_seconds:

        print("It is time to save!")

        # create a folder
        save_to:str = save_to_directory + "\\" + str(datetime.datetime.utcnow()).replace(":", "-")
        print("Making directory '" + save_to + "'...")
        os.mkdir(save_to)

        # save to folder
        print("Saving...")
        model.save(save_to)

        # update the saved time
        last_saved_at = datetime.datetime.utcnow()

