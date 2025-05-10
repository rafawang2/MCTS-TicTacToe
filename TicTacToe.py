from GameUtils import *
from Players.Human import Human
from Players.AlphaBeta import AlphaBetaPlayer
from Players.RandomBot import RandomBot

class TicTacToe():
    def __init__(self, state:STATE):
        self.game_state = state

    def ResetGame(self):
        self.game_state.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.game_state.current_player = -1

    def play(self, p1, p2):
        winner = None
        while winner is None:
            print_board(self.game_state.board)
            if self.game_state.current_player == -1:
                r, c = p1.get_move(self.game_state.board, self.game_state.current_player)
            else:
                r, c = p2.get_move(self.game_state.board, self.game_state.current_player)
            make_move(self.game_state.board, r, c, self.game_state.current_player)
            self.game_state.current_player*=-1
            winner = GetWinner(self.game_state.board)
            print(winner)

        win_msg = {
            -1: "(X) wins!",
            1:  "(O) wins!",
            0:  "It's a tie!"
        }
        if winner is not None:
            print_board(self.game_state.board)
            print(win_msg[winner])

if __name__ == '__main__':
    game_state = STATE(
        board=[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        current_player=-1
    )
    game = TicTacToe(game_state)
    p1 = Human()
    p2 = RandomBot()
    p3 = AlphaBetaPlayer(symbol=-1,
                         state=game_state)
    p4 = AlphaBetaPlayer(symbol=1,
                         state=game_state)
    game.play(p1, p4)