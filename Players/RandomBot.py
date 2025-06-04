import copy
import random
from GameUtils import getValidMoves, make_move, isWinner
class RandomBot():
    def get_move(self, board, player):
        move = random.choice(getValidMoves(board))
        return move

class GreedyBot():
    def get_move(self, board, player):
        next_board = copy.deepcopy(board)
        valid_moves = getValidMoves(board)
        for (r,c) in valid_moves:
            make_move(next_board, r, c, player)
            if isWinner(next_board, player):
                return (r, c)
            else:
                next_board[r][c] = 0
        return random.choice(valid_moves)