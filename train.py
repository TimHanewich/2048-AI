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
model_path:str = r""
model:tensorflow.keras.Sequential = None
if model_path != None and model_path != "":
    print("Loading model from '" + model_path + "'")
    model = tensorflow.keras.models.load_model(model_path)
else:
    print("A model path was not provided! Constructing a new model...")

    model = tensorflow.keras.Sequential()
    model.add(tensorflow.keras.layers.Input(176))
    model.add(tensorflow.keras.layers.Dense(400, "relu"))
    model.add(tensorflow.keras.layers.Dense(300, "relu"))
    model.add(tensorflow.keras.layers.Dense(250, "relu"))
    model.add(tensorflow.keras.layers.Dense(200, "relu"))
    model.add(tensorflow.keras.layers.Dense(100, "relu"))
    model.add(tensorflow.keras.layers.Dense(30, "relu"))
    model.add(tensorflow.keras.layers.Dense(4))
    model.compile("adam", "mean_squared_error")

print("Model assembled.")



# training params
save_model_every_seconds = 600
save_to_directory = r"C:\Users\timh\Downloads\tah\2048-ai\models5"


# Train
last_saved_at = datetime.datetime.utcnow()  #- datetime.timedelta(hours=1)
while True:

    # play X number of games
    PlayResults:list[ai_tools.PlayResult] = []
    for x in range(0, 10):
        print("Playing game # " + str(x) + "... ")

        g:Py2048_Engine.Game.Game = Py2048_Engine.Game.Game()

        # play it
        result:ai_tools.PlayResult = ai_tools.play_to_completion(model, g)
        PlayResults.append(result)

    # select the highest
    winner:ai_tools.PlayResult = PlayResults[0]
    for pr in PlayResults:

        # firstly, replace it if this one won and the current winner did not
        if pr.game_won == True and winner.game_won == False:
            winner = pr
        elif pr.concentration > winner.concentration: # secondly, if the concentration is higher
            winner = pr
    
    # print it
    print("Best game = Max Val: " + str(winner.max_value) + ", Concentration: " + str(winner.concentration))

    # also print the averages
    max_vals:list[int] = []
    concentrations:list[float] = []
    for result in PlayResults:
        max_vals.append(result.max_value)
        concentrations.append(result.concentration)
    print("Averages = Max Val: " + str(sum(max_vals) / len(max_vals)) + ", Concentrations: " + str(sum(concentrations) / len(concentrations)))

    
    # Establish a list of training data (inputs + outputs)
    inputs:list[list[int]] = [] #A list of "board positions" (scenarios) as the input
    outputs:list[list[int]] = [] # A list of the decision that was made (correctly) in each scenario
    for md in winner.move_decisions:
        # assemble a list of input & output scenarios
        inputs.append(md.input)
        outputs.append(md.output_polarized)

    # turn into numpy arrays
    inputs_np = np.array(inputs)
    ouputs_np = np.array(outputs)

    # fit
    print("Training started @ " + str(datetime.datetime.now()) + "...")
    model.fit(inputs_np, ouputs_np, epochs=400, verbose=True)

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

