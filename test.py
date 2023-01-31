import os
import tensorflow as tf
import Py2048_Engine.Game
import tools
import ai_tools

model_dir_path:str = r"C:\Users\timh\Downloads\tah\2048-ai\models\2023-01-31 04-08-31.118039"

# load the model
model:tf.keras.Sequential = tf.keras.models.load_model(model_dir_path)

# inputs
play_count = 25

# play a game X number of times
maxs:list[int] = []
concentrations:list[float] = []
for x in range(0, play_count):

    # create a game
    g:Py2048_Engine.Game.Game = Py2048_Engine.Game.Game()

    # play to completion
    print("Playing game # " + str(x+1) + "... ")
    data:list[ai_tools.MoveDecision] = ai_tools.self_play(model, g)

    # take a note
    maxs.append(tools.max_value(g))
    concentrations.append(tools.concentration(g))

# print the results
print("Average Results after " + str(play_count) + " games:")
print("Avg Max Value: " + str(sum(maxs) / len(maxs)))
print("Avg Concentration: " + str(sum(concentrations) / len(concentrations)))
    

