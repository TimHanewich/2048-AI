from Py2048_Engine.Game import Game

g = Game()

while True:
    g.up()
    g.left()
    g.down()
    g.right()
    print(g)
    print(g.numMoves)
    print()


# test winning
g.board[0][0] = 1024
g.board[0][1] = 1024
