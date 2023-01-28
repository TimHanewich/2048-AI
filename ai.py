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

g = Py2048_Engine.Game.Game()
data = self_play(model, g)
data = sort_by_gain(data)
for d in data:
    print(d.gain())
input("De")

# Train
highest_max:int = 0 # the highest title achieved on any previous ones
highest_total:int = 0 # the highest TOTAL (sum) achieved on any previous ones
while True:

    g:Py2048_Engine.Game.Game = Py2048_Engine.Game.Game()

    # play game
    print("Playing game...")
    game_data:list[MoveDecision] = self_play(model, g)

    # gather data from it - it's max and total
    game_max:int = tools.max_value(g)
    game_total:int = tools.total_value(g)
    print("Max: " + str(game_max))
    print("Total: " + str(game_total))

    # decide wether to train it on this or not (was it "more successful" than our last iterations?)
    should_train:bool = False

    # first, we SHOULD train if we have elipsed the high score (max tile)
    if should_train == False:
        if game_max > highest_max: # if this eclipsed the last, yes
            print("Will train on this one - it broke the high max!")
            should_train = True
    
    # If the above didn't become true, we SHOULD train if we at least tied the high score but also have more value on the board
    if should_train == False:
        if game_max == highest_max: # if this game did not at least tie the max score, then forget it
            if game_total > highest_total: # the sum of all tiles on the thing was higher than the highest we have seen with the same high score tile
                print("Will train on this one - it tied the max but produced a higher total value.")
                should_train = True

    
    # train?
    if should_train:

        # update the high
        highest_max = game_max
        highest_total = game_total

        # assemble a list of input & output scenarios
        inputs:list[list[int]] = []
        outputs:list[list[int]] = []
        for md in game_data:
            inputs.append(md.input)
            outputs.append(md.output_polarized)

        # turn into numpy arrays
        inputs_np = np.array(inputs)
        ouputs_np = np.array(outputs)

        # fit
        print("Training...")
        model.fit(inputs_np, ouputs_np, epochs=1500, verbose=True)
    else:
        print("Skipping training.")

