import tensorflow
import tools
import Py2048_Engine.Game
import copy
import numpy as np

class MoveDecision:
    input:list[int] = [] # 176 long
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

        # priotizie the list of moves
        priorities:list[str] = tools.prioritize_moves(output)

        # get a list of legal moves
        legal_moves:list[str] = tools.legal_moves(g)

        # make the move, according to prioritiy
        game_over:bool = False
        for priority in priorities:

            # Only play it if it is a legal move
            if priority in legal_moves:

                # make the move
                try:
                    if priority == "up":
                        md.output_polarized = [1, 0, 0, 0]
                        g.up()
                    elif priority == "right":
                        md.output_polarized = [0, 1, 0, 0]
                        g.right()
                    elif priority == "down":
                        md.output_polarized = [0, 0, 1, 0]
                        g.down()
                    elif priority == "left":
                        md.output_polarized = [0, 0, 0, 1]
                        g.left()
                except: # the game is over. So add it and return
                    game_over = True
                    
        # add the move decision
        ToReturn.append(md)

        # if it is game over, return
        if game_over:
            return ToReturn