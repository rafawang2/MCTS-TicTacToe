import random
from GameUtils import getValidMoves
class RandomBot():
    def get_move(self, board, player):
        move = random.choice(getValidMoves(board))
        return move