import math
import copy
import random
from GameUtils import *
import time

class AlphaBetaPlayer:
    def __init__(self, symbol, state: STATE, max_depth=100):
        self.symbol = symbol
        self.state = state
        self.max_depth = max_depth
    def get_move(self, board, player):
        start_time = time.time()
        best_value = -math.inf
        best_move = None

        valid_moves = getValidMoves(board)

        for move in valid_moves:
            if move:
                new_state = copy.deepcopy(self.state)
                r, c = move
                make_move(new_state.board, r, c, new_state.current_player)
                new_state.current_player*=-1

                move_value = self.alphabeta(new_state, 0, -math.inf, math.inf, False)   # 因為下完一步換成對手，故對此狀態進行最小化

                if move_value > best_value:
                    best_value = move_value
                    best_move = move
        if not best_move:
            best_move =  random.choice(getValidMoves(board))
            print(f"random best_move {best_move} ")

        end_time = time.time()
        print(f"Py AlphaBeta move {move} took {end_time - start_time:.6f} seconds")
        print(f"py best move: {best_move}, best value: {best_value}")
        return best_move

    def evaluate(self, state:STATE):
        """ 評估函數：根據當前棋盤返回數值評估 """
        if GetWinner(state.board) == self.symbol:
            return 100
        if GetWinner(state.board) == -self.symbol:
            return -100

        return 0

    def alphabeta(self, state:STATE, depth, alpha, beta, maximizing):
        # 終止條件
        if depth >= self.max_depth:
            # print(f"max depth:{depth}")
            return self.evaluate(state)  # 返回棋盤評估值

        winner = GetWinner(state.board)
        if winner is not None:
            return self.evaluate(state)  # 游戏结束，直接返回评估值


        if maximizing:
            max_eval = -math.inf
            valid_moves = getValidMoves(state.board)
            for move in valid_moves:
                new_state = copy.deepcopy(state)
                r, c = move
                make_move(new_state.board, r, c, new_state.current_player)
                new_state.current_player*=-1

                eval = self.alphabeta(new_state, depth + 1, alpha, beta, False)

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    # print(f"Beta剪枝 beta:{beta}, alpha:{alpha}, depth: {depth}")
                    break  # Beta 剪枝
            return max_eval
        else:
            min_eval = math.inf
            valid_moves = getValidMoves(state.board)
            for move in valid_moves:
                new_state = copy.deepcopy(state)
                r, c = move
                make_move(new_state.board, r, c, new_state.current_player)
                new_state.current_player*=-1

                eval = self.alphabeta(new_state, depth + 1, alpha, beta, True)

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    # print(f"Alpha剪枝 beta:{beta}, alpha:{alpha}, depth: {depth}")
                    break  # Alpha 剪枝
            return min_eval