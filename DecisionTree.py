import copy
import pickle
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Node import Node

              # List of child nodes

class DecisionTree:
    """
    Decision Tree for Connect Four game.
    """
    def __init__(self, initial_board,ai_algorithm,heuristic_function):
        self.root = Node(initial_board)  # Root node of the tree
        self.ai_algorithm=ai_algorithm
        self.heuristic_function=heuristic_function



    def generate_tree(self, node, depth, is_maximizing):
        """
        Generate the decision tree recursively using Minimax algorithm.
        """
        if depth == 0 or self.is_terminal(node.board):
            node.score = self.evaluate_board(node.board)
            return

        legal_moves = self.get_legal_moves(node.board)
        for move in legal_moves:
            new_board = self.make_move(node.board, move, 'O' if is_maximizing else 'X')
            child_node = Node(new_board, move=move)
            node.children.append(child_node)
            self.generate_tree(child_node, depth - 1, not is_maximizing)

    def save_tree(self, file_name):
        """
        Save the decision tree to a file using pickle.
        """
        with open(file_name, 'wb') as f:
            pickle.dump(self.root, f)

    @staticmethod
    def load_tree(file_name):
        """
        Load the decision tree from a file using pickle.
        """
        with open(file_name, 'rb') as f:
            root = pickle.load(f)
        tree = DecisionTree([])
        tree.root = root
        return tree

    # Helper Methods

    def is_terminal(self, board):
        """
        Check if the current board is a terminal state (win or draw).
        """
        return self.is_win(board, 1) or self.is_win(board, -1) or self.is_draw(board)

    def get_legal_moves(self, board):
        """
        Get all legal moves (columns not full).
        """
        return [col for col in range(len(board[0])) if board[0][col] ==' ']

    def make_move(self, board, col, player):
        """
        Simulate making a move on the board.
        """
        new_board = copy.deepcopy(board)
        for row in reversed(range(len(board))):
            if new_board[row][col] == ' ':
                new_board[row][col] = player
                break
        return new_board

    def evaluate_board(self, board):
        """
        Evaluate the board state (heuristic function).
        """
        if self.ai_algorithm == 'Heuristic AI':
            return self.heuristic_function.heuristic_function_square(board,1)
        elif self.ai_algorithm == 'aggressive':
            return self.heuristic_function.aggressive_heuristic(board, 1)
        elif self.ai_algorithm == 'defensive':
            return self.heuristic_function.defensive_heuristic(board, 1)
        else:
            raise ValueError("Invalid AI algorithm")

    def is_draw(self, board):
        """
        Check if the game is a draw (no empty cells in the top row).
        """
        return all(cell != ' ' for cell in board[0])

    def is_win(self, board, player):
        """
        Check if a player has won (horizontal, vertical, diagonal).
        """
        rows, cols = len(board), len(board[0])

        # Check horizontal
        for row in range(rows):
            for col in range(cols - 3):
                if all(board[row][col + i] == player for i in range(4)):
                    return True

        # Check vertical
        for col in range(cols):
            for row in range(rows - 3):
                if all(board[row + i][col] == player for i in range(4)):
                    return True

        # Check diagonal (bottom-left to top-right)
        for row in range(rows - 3):
            for col in range(cols - 3):
                if all(board[row + i][col + i] == player for i in range(4)):
                    return True

        # Check diagonal (top-left to bottom-right)
        for row in range(3, rows):
            for col in range(cols - 3):
                if all(board[row - i][col + i] == player for i in range(4)):
                    return True

        return False




# Example Usage
if __name__ == "__main__":
    from decision_tree import DecisionTree, Node  # Import your decision tree implementation

    # Sample board and decision tree
    initial_board = [[0] * 7 for _ in range(6)]  # Empty board
    tree = DecisionTree(initial_board)
    tree.generate_tree(tree.root, depth=3, is_maximizing=True)

    # Visualize the tree
 
