import random

from heuristic2 import HeuristicFunction2

class HeuristicFunction:
    def __init__(self, k):
        self.k = k
        # self.board = board

    def evaluate_board(self, board):
        heuristic=HeuristicFunction2(1)
        return heuristic.evaluate_board(board)
        

    def get_legal_moves(self, board):
        """
        Get all legal moves (columns not full).
        """
        return [col for col in range(len(board[0])) if board[0][col] == ' ']

    def random_choice(self, board):
        """
        Randomly choose a column from the available moves.
        """
        return random.choice(self.get_legal_moves(board))

    def defensive_heuristic(self, board, agent_id):
        potential_danger = self.estimate_danger(board, agent_id)  # Hypothetical function estimating threats
        agent_safety_score = self.evaluate_safety(board, agent_id)  # Evaluate defensive position
        return -potential_danger + agent_safety_score

    def aggressive_heuristic(self, board, agent_id='X'):
        rows, cols = len(board), len(board[0])
        score = 0

        def count_in_direction(r, c, dr, dc):
            """Count consecutive pieces and empty spaces in a direction."""
            count = 0
            for i in range(4):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if board[nr][nc] == agent_id:
                        count += 1
                    elif board[nr][nc] != ' ':
                        return count  # Blocked direction
                else:
                    break
            return count

        # Evaluate the board
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == agent_id:
                    # Check all directions
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        count = count_in_direction(r, c, dr, dc)
                        if count >= 4:
                            score += 100  # Winning line (huge bonus)
                        else:
                            score += count ** 2  # Reward longer lines more

        # Center control
        center_col = cols // 2
        for r in range(rows):
            if board[r][center_col] == agent_id:
                score += 5  # Bonus for controlling the center column

        return score

    def estimate_danger(self, board, agent_id='X'):
        rows, cols = len(board), len(board[0])
        opponent_id = 'O' if agent_id == 'X' else 'X'  # If agent_id is 'X', opponent_id is 'O', and vice versa.
        danger_score = 0

        def count_in_direction(r, c, dr, dc):
            count = 0
            empty_slots = 0
            for i in range(4):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if board[nr][nc] == opponent_id:
                        count += 1
                    elif board[nr][nc] == ' ':
                        empty_slots += 1
                else:
                    break
            return count, empty_slots

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == opponent_id:
                    # Check all directions
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        count, empty_slots = count_in_direction(r, c, dr, dc)
                        if count + empty_slots >= 4:  # A potential threat
                            danger_score += count ** 2  # Quadratic weighting (more pieces = higher threat)

        return danger_score

    def evaluate_safety(self, board, agent_id='X'):
        rows, cols = len(board), len(board[0])
        safety_score = 0

        def count_in_direction(r, c, dr, dc):
            count = 0
            empty_slots = 0
            for i in range(4):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if board[nr][nc] == agent_id:
                        count += 1
                    elif board[nr][nc] == ' ':
                        empty_slots += 1
                else:
                    break
            return count, empty_slots

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == agent_id:
                    # Check all directions
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        count, empty_slots = count_in_direction(r, c, dr, dc)
                        if count + empty_slots >= 4:  # A potential line
                            safety_score += count ** 2  # More pieces = higher safety

        return safety_score

    def heuristic_function_square(self, board, agent_id='X'):
        rows, cols = len(board), len(board[0])
        opponent_id = 'O' if agent_id == 'X' else 'X'  # Set opponent as the opposite of agent
        weight_matrix = self.get_weight_matrix(rows, cols)
        score = 0
        # Evaluate the board
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == agent_id:
                    score += weight_matrix[r][c]  # Add value for AI's pieces
                elif board[r][c] == opponent_id:
                    score -= weight_matrix[r][c]  # Subtract value for opponent's pieces

        return score

    def get_weight_matrix(self, rows, cols):
        # Central columns are weighted more heavily
        weight_matrix = []
        for r in range(rows):
            row_weights = []
            for c in range(cols):
                center_dist = abs(c - cols // 2)
                row_weights.append(cols // 2 - center_dist + 1)  # Assign higher values near the center
            weight_matrix.append(row_weights)
        return weight_matrix
