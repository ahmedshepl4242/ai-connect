import random
from tkinter import messagebox

from DecisionTree import DecisionTree
from DecisionTreeVis import DecisionTreeVisualizer
from Heustric import HeuristicFunction
from constants import PLAYER_SCORE


class GameController:
    def __init__(self, k, board_model, view, heuristic_function, minMax, ai_enabled=False):
        self.board = board_model
        self.view = view
        self.current_player = 'X'
        self.ai_enabled = ai_enabled
        self.heuristic_function = heuristic_function
        self.ai_algorithm = None  # Store the selected AI algori
        self.k = k
        self.minMax = minMax
        # self.score={'X':0, 'Y':0}

    def set_algorithm(self, algorithm):
        """Set the AI algorithm based on user selection."""
        self.ai_algorithm = algorithm
        print(f"AI algorithm set to: {self.ai_algorithm}")

    def handle_click(self, col):
        if self.board.is_valid_move(col) and self.current_player == "X":
            success, row = self.board.make_move(col, self.current_player)
            if success:
                self.view.update_cell(row, col, self.current_player)
                # if self.board.check_winner(self.current_player):
                #     messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                #     self.reset_game()

                # update the score of the game over the current player
                self.board.update_score(self.current_player)
                print(self.board.score)

                # if the board is full go out and show the result
                if self.board.is_full():
                    if (self.board.score['X'] > self.board.score['O']):
                        messagebox.showinfo("Game Over", f"Player X wins!")
                    elif (self.board.score['X'] < self.board.score['O']):
                        messagebox.showinfo("Game Over", f"Player O wins!")
                    else:
                        messagebox.showinfo("Game Over", "It's a draw!")
                    self.reset_game()
                    return

                self.switch_player()
                self.view.update_status(self.current_player)
                if self.ai_enabled and self.current_player == 'O':
                    self.ai_move()

    # def ai_move(self):
    #     # Simple AI: Pick a random valid column
    #     print(self.board.grid)
    #     col = self.heuristic_function.random_choice(self.board.grid)
    #     self.handle_click(col)
    def ai_move(self):
            if (self.ai_algorithm != "random"):
                # print(self.board.grid)
                # initial_board = [[0] * 7 for _ in range(6)]  # Empty board
                decisionTree = DecisionTree(
                    self.board.grid, self.ai_algorithm, self.heuristic_function)
                decisionTree.generate_expect_tree(
                    decisionTree.root, self.k, True, False, [3, 2, 4, 1, 5, 6, 0])
                self.minMax.expect(decisionTree.root, self.k, True, False)
                bestNode = decisionTree.root.children[0]

                for child in decisionTree.root.children:
                    if child.score > bestNode.score:
                        bestNode = child
                print(bestNode.board)

                self.board.grid = bestNode.board
                self.view.update_board(bestNode.board.copy())
                self.board.update_score(self.current_player)
                self.switch_player()
                self.view.update_status(self.current_player)

            else:
                col = self.heuristic_function.random_choice(self.board.grid)
                self.handle_click(col)
            self.view.update_scores()

    def switch_player(self):

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        if (self.current_player == 'O'):
            # how to wait 1000 milliseconds before switching
            self.view.after(1000, self.ai_move)

    def reset_game(self):
        self.board.reset()
        self.current_player = 'X'

        self.view.reset_board()
        self.view.update_status(self.current_player)
