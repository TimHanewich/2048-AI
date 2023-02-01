import tensorflow
import tools
import Py2048_Engine.Game
import copy
import numpy as np

class MoveDecision:
    input:list[int] = [] # 176 long
    output_polarized:list[int] = [] # 4 long, but the decision that was made is 1, the decision that was not made is 0. THIS IS WHAT WILL BE USED FOR TRAINING

class PlayResult:

    move_decisions:list[MoveDecision] = []
    game_won:bool = False
    game_lost:bool = False
    max_value:int = 0
    concentration:float = 0.0


# plays until win, loss, or frozen (AI keeps just doing the same thing over and over again and the game goes nowhere)
def play_to_completion(model:tensorflow.keras.Sequential, g:Py2048_Engine.Game.Game) -> PlayResult:

    ToReturn:PlayResult = PlayResult()

    while True:
        
        # predict
        inputs = tools.game_to_training_array(g)
        inputs_np = np.array([inputs])
        output = model.predict(inputs_np, verbose=False)[0]

        # create a MoveDecision and add it
        md:MoveDecision = MoveDecision()
        md.input = inputs

        # priotizie the list of moves
        priorities:list[str] = tools.prioritize_moves(output)

        # get a list of legal moves
        legal_moves:list[str] = tools.legal_moves(g)

        # make the move, according to prioritiy
        if len(legal_moves) > 0:
            game_result:int = None # For internal use here only. None = game is still going, continue. 0 = Game lost (safe to return), 1 = Game won (safe to return)
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
                    except Py2048_Engine.Game.GameWonException:
                        game_result = 1
                    except Py2048_Engine.Game.GameLostException:
                        game_result = 0
                    
            # add the move decision
            ToReturn.move_decisions.append(md)

        # if it is game over, mark it as such
        if game_result != None:

            if game_result == 0:
                ToReturn.game_lost = True
            elif game_result == 1:
                ToReturn.game_won = True

        # if it is game over or there were no legal moves to play, return
        if game_result != None or len(legal_moves) == 0:

            # max tile
            ToReturn.max_value = tools.max_value(g)
            ToReturn.concentration = tools.concentration(g)

            return ToReturn
