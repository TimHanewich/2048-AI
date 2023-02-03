import os
import tensorflow as tf
import Py2048_Engine.Game
import tools
import ai_tools

model_dir_path:str = r"C:\Users\timh\Downloads\tah\2048-ai\models4\2023-02-03 16-14-58.159941"

# load the model
model:tf.keras.Sequential = tf.keras.models.load_model(model_dir_path)

# inputs
play_count = 80

# play a game X number of times
maxs:list[int] = []
concentrations:list[float] = []
for x in range(0, play_count):

    # create a game
    g:Py2048_Engine.Game.Game = Py2048_Engine.Game.Game()

    # play to completion
    print("Playing game # " + str(x+1) + "... ")
    pr:ai_tools.PlayResult = ai_tools.play_to_completion(model, g)

    # take a note
    maxs.append(pr.max_value)
    concentrations.append(pr.concentration)

# print the results
print("Average Results after " + str(play_count) + " games:")
print("Avg Max Value: " + str(sum(maxs) / len(maxs)))
print("Avg Concentration: " + str(sum(concentrations) / len(concentrations)))
    

