import math

from Node import Node


class MinMax:
    """
    Minimax implementation for a game, supporting the given board representation with X and O players.
    """

    def __init__(self, depth, is_maximizing):
        self.depth = depth
        self.is_maximizing = is_maximizing

    def minimax(self, node, depth, is_maximizing):
        """
        Minimax algorithm without pruning.
        """
        if depth == 0 or self.is_terminal(node.board):
            # node.score = HeuristicF.evaluate_board(node.board)
            return node.score

        if is_maximizing:
            best_val = -math.inf
            for child in node.children:
                val = self.minimax(child, depth - 1, False)
                best_val = max(best_val, val)
            node.score = best_val
            # print(node.score)
            return best_val
        else:
            best_val = math.inf
            for child in node.children:
                val = self.minimax(child, depth - 1, True)
                best_val = min(best_val, val)
            node.score = best_val
            # print(node.score)
            return best_val

    def minimax_pruning(self, node, depth, alpha=float(-math.inf), beta=float(math.inf), is_maximizing=True):
        """
        Minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or self.is_terminal(node.board):
            return node.score

        if is_maximizing:
            best_val = -math.inf
            for child in node.children:
                val = self.minimax_pruning(
                    child, depth - 1, alpha, beta, False)
                best_val = max(best_val, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            node.score = best_val
            return best_val
        else:
            best_val = math.inf
            for child in node.children:
                val = self.minimax_pruning(child, depth - 1, alpha, beta, True)
                best_val = min(best_val, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            node.score = best_val
            return best_val

    def expect(self, node, depth, is_maximizing, chance_node):
        """
        expected Minimax algorithm without pruning.
        """
        if depth == 0 or self.is_terminal(node.board):
            return node.score

        if chance_node:
            arr = [0.6, 0.4]
            i = 0
            for child in node.children:
                node.score += arr[i] * \
                    self.expect(child, depth - 1, is_maximizing, False)
                i += 1
            return node.score

        else:
            if is_maximizing:
                best_val = -math.inf
                for child in node.children:
                    val = self.expect(child, depth - 1, False, True)
                    best_val = max(best_val, val)
                node.score = best_val
                return best_val
            else:
                best_val = math.inf
                for child in node.children:
                    val = self.expect(child, depth - 1, True, True)
                    best_val = min(best_val, val)
                node.score = best_val
                return best_val

    def is_terminal(self, board):
        """
        Check if the board is in a terminal state (win or draw).
        """
        return self.is_win(board, 'X') or self.is_win(board, 'O') or self.is_draw(board)

    def is_draw(self, board):
        """
        Check if the game is a draw (no legal moves left).
        """
        return len(self.get_legal_moves(board)) == 0

    def is_win(self, board, player):
        """
        Check if a player has won the game.
        """
        rows, cols = len(board), len(board[0])
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == player:
                    # Check all directions
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        if self.count_in_direction(board, r, c, dr, dc, player) == 4:
                            return True
        return False

    def count_in_direction(self, board, r, c, dr, dc, player):
        """
        Count consecutive pieces for a player in a specific direction.
        """
        rows, cols = len(board), len(board[0])
        count = 0
        for i in range(4):
            nr, nc = r + i * dr, c + i * dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == player:
                count += 1
            else:
                break
        return count

    def get_legal_moves(self, board):
        """
        Get all legal moves (columns with empty spaces).
        """
        return [col for col in range(len(board[0])) if board[0][col] == ' ']

    def make_move(self, board, col, player):
        """
        Make a move on the board for the given player.
        """
        new_board = [row[:] for row in board]
        for row in reversed(range(len(board))):
            if new_board[row][col] == ' ':
                new_board[row][col] = player
                break
        return new_board

    def generate_children(self, node, is_maximizing):
        """
        Generates child nodes based on all legal moves.
        """
        legal_moves = self.get_legal_moves(node.board)
        children = []
        for move in legal_moves:
            player = 'X' if is_maximizing else 'O'
            new_board = self.make_move(node.board, move, player)
            child_node = Node(new_board, move)
            children.append(child_node)
        node.children = children
        return children
