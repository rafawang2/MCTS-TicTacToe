from GameUtils import *
import math
import random
from copy import deepcopy
from Players.RandomBot import RandomBot
import time

class MCTSNode:
    def __init__(self, game_state:STATE, parent=None, player=None, move=None):
        # parent reached self by making move; player indicates who made this move
        self.game_state = deepcopy(game_state)  # node's game state
        self.parent = parent  # parent node
        self.move = move  # parent make this move to self
        self.children = []
        self.visits = 0  # visit count
        self.score = 0  # total score
        self.player = player  # player who made the move
        self.untried_moves = getValidMoves(game_state.board)  # remaining valid moves to explore

class MCTSPlayer:
    def __init__(self, state:STATE, symbol, exploration_weight=2, num_simulations = 1000):
        self.num_simulations = num_simulations
        self.exploration_weight = exploration_weight
        self.root_state = state
        self.symbol = symbol
        self.select_meth_bot = RandomBot()

    def get_move(self, board, player, verbose = True):
        current_time = time.time()

        total_moves = 3*3
        remaining_moves = len(getValidMoves(self.root_state.board))
        progress = 1 - remaining_moves / total_moves

        # Updata root state
        self.root_state.board = board
        self.root_state.current_player = player

        if progress < 0.45:
            self.num_simulations = 1000
        elif progress < 0.6:
            self.num_simulations = 2000
        elif progress < 0.7:
            self.num_simulations = 3000
        elif progress < 0.8:
            self.num_simulations = 4000
        elif progress < 0.9:
            self.num_simulations = 3000
        else:  # 終盤
            self.num_simulations = 1000

        if verbose:
            print(f"Game progress: {progress}")
            print(f"Max num_simulations: {self.num_simulations}")

        if not self.root_state:
            raise ValueError("Game state not set")

        root = MCTSNode(self.root_state)  # let root node be the current game state

        # MCTS Algorithm
        for _ in range(self.num_simulations):
            # Step1: Selection
            node = self.select(root)

            # Step2: Expansion
            if GetWinner(node.game_state.board) is None and node.untried_moves:
                node = self.expand(node)

            # Step3: Rollout
            simulation_result = self.simulate(node.game_state)

            # Step4: Backpropagate
            self.backpropagate(node, simulation_result)

        # If the root node has no child nodes, a random valid move is selected.
        # This indicates an error with the MCTS implementation.
        if not root.children:
            print("random choose")
            return self.select_meth_bot.get_move(board, player)

        # Select the node with the maximum score/visits ratio
        best_child = max(root.children, key=lambda node_i: node_i.score / node_i.visits if node_i.visits > 0 else -float('inf'))

        end_time = time.time()

        if verbose:
            print(f"MCTS best move: {best_child.move}, score: {best_child.score}, visits: {best_child.visits}, took {end_time - current_time:.6f} seconds")
        return best_child.move

    def select(self, node:MCTSNode) -> MCTSNode:
        # Traverse down the tree until reaching either:
        # 1. A node with untried moves remaining, or
        # 2. A leaf node (no children)
        while node.untried_moves == [] and node.children != []:
            node = self.uct_select(node)
        return node

    def expand(self, node: MCTSNode) -> MCTSNode:
        """
        Expands the game tree by creating a new child node from an untried move.
        Args:
            node: The node to expand from
        Returns:
            The newly created child node
        """
        # Randomly select and remove an untried move
        random.shuffle(node.untried_moves)
        move = node.untried_moves.pop()

        # Create new game state for the child node
        new_state = deepcopy(node.game_state)
        r, c = move

        # Execute the move and switch player
        new_node_player = new_state.current_player
        make_move(new_state.board, r, c, new_state.current_player)
        new_state.current_player *= -1

        # Create and attach new child node
        new_node = MCTSNode(
            new_state,
            parent=node,
            move=move,
            player=new_node_player
        )
        node.children.append(new_node)

        return new_node

    def simulate(self, game_state:STATE):
        """
        Simulates a complete game from the given state using the selection method bot.
        Args:
            game_state: The starting game state for simulation
        Returns:
            int: Evaluation score of the final game state (1 for win, -1 for loss, 0 for draw)
        """
        state = deepcopy(game_state)  # Create a copy to avoid modifying original state

        # Simulate game until termination using the selection method bot for both players
        while GetWinner(state.board) is None:
            move = self.select_meth_bot.get_move(state.board,state.current_player)
            if move is None:
                break
            r, c = move
            make_move(state.board, r, c, state.current_player)
            state.current_player*=-1

        return self.evaluate(state)  # Score the final game state

    def evaluate(self, state:STATE):
        """Evaluates the terminal game state and returns a score.
        Args:
            state: The game state to evaluate
        Returns:
            int: 1 if bot wins, -1 if opponent wins, 0 for draw
        """
        winner = GetWinner(state.board)
        if winner == self.symbol:
            return 1
        elif winner == -self.symbol:
            return -1
        else:
            return 0  # 平手


    # 回傳模擬結果
    def backpropagate(self, node:MCTSNode, result):
        """
        Backpropagates the simulation result through the tree.

        Updates visit counts and scores for all nodes along the path from
        the given node back to the root. For non-root nodes, score updates
        are inverted when the node's player differs from the current bot's symbol.

        Args:
            node: The starting node (typically leaf node) for backpropagation
            result: The simulation result to propagate (1=win, -1=loss, 0=draw)
        """
        # Traverse up the tree from leaf to root
        while node:
            node.visits += 1
            if node.parent: # Non-root node
                if node.player == self.symbol:
                    # Our player's perspective
                    node.score += result
                else:
                    # Opponent's perspective (invert result)
                    node.score -= result
            else:  # Root node
                node.score += result

            # Move to parent node
            node = node.parent

    # UCT(Upper Confidence Bound)
    def uct_select(self, node:MCTSNode):
        if node.parent is None:
            log_parent_visits = math.log(node.visits + 1e-6)
        else:
            log_parent_visits = math.log(node.parent.visits + 1e-6)
        return max(node.children, key=lambda node_i: self.uct(node_i, log_parent_visits))

    # UCT value for node
    def uct(self, node:MCTSNode, log_parent_visits):
        if node.visits == 0:
            return float('inf')
        exploitation = node.score / node.visits
        exploration = math.sqrt(log_parent_visits / node.visits)
        return exploitation + self.exploration_weight * exploration