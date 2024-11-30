import math

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
            return node.score

        if is_maximizing:
            best_val = -math.inf
            for child in node.children:
                val = self.minimax(child, depth - 1, False)
                best_val = max(best_val, val)
            return best_val
        else:
            best_val = math.inf
            for child in node.children:
                val = self.minimax(child, depth - 1, True)
                best_val = min(best_val, val)
            return best_val

    def minimax_pruning(self, node, depth, alpha, beta, is_maximizing):
        """
        Minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or self.is_terminal(node.board):
            return node.score

        if is_maximizing:
            best_val = -math.inf
            for child in node.children:
                val = self.minimax_pruning(child, depth - 1, alpha, beta, False)
                best_val = max(best_val, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return best_val
        else:
            best_val = math.inf
            for child in node.children:
                val = self.minimax_pruning(child, depth - 1, alpha, beta, True)
                best_val = min(best_val, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
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


# Example Usage
if __name__ == "__main__":
    # Initial board state with 'X' and 'O' players
    initial_board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['X', ' ', 'O', ' ', ' ', ' ', ' ']
    ]

    # Initialize MinMax
    minimax_solver = MinMax(depth=3, is_maximizing=True)

    # Example node representation
    class Node:
        def __init__(self, board, score=0):
            self.board = board
            self.score = score
            self.children = []

    # Example node for testing
    root_node = Node(initial_board)

    # Use minimax or minimax with pruning
    score = minimax_solver.minimax(root_node, depth=3, is_maximizing=True)
    print(f"Minimax score: {score}")
