import random
from tkinter import messagebox

from DecisionTree import DecisionTree
from DecisionTreeVis import DecisionTreeVisualizer
from Heustric import HeuristicFunction

class GameController:
    def __init__(self,k, board_model, view, heuristic_function,minMax,ai_enabled=False):
        self.board = board_model
        self.view = view
        self.current_player = 'X'
        self.ai_enabled = ai_enabled
        self.heuristic_function = heuristic_function
        self.ai_algorithm = None  # Store the selected AI algori
        self.k=k
        self.minMax=minMax
    
    def set_algorithm(self, algorithm):
        """Set the AI algorithm based on user selection."""
        self.ai_algorithm = algorithm
        print(f"AI algorithm set to: {self.ai_algorithm}")

    def handle_click(self, col):
        if self.board.is_valid_move(col):
            success, row = self.board.make_move(col, self.current_player)
            if success:
                self.view.update_cell(row, col, self.current_player)
                if self.board.check_winner(self.current_player):
                    messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                    self.reset_game()
                elif self.board.is_full():
                    messagebox.showinfo("Game Over", "It's a draw!")
                    self.reset_game()
                else:
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
            if(self.ai_algorithm!="random"):
                # print(self.board.grid)
                # initial_board = [[0] * 7 for _ in range(6)]  # Empty board
                decisionTree=DecisionTree(self.board.grid,self.ai_algorithm,self.heuristic_function)
                decisionTree.generate_tree(decisionTree.root, self.k, True)
                visualizer = DecisionTreeVisualizer(decisionTree)
                visualizer.visualize_tree()

                self.minMax.minimax(decisionTree.root, self.k, True)
                bestNode = decisionTree.root.children[0]
                for child in decisionTree.root.children:
                    if child.score > bestNode.score:
                        bestNode = child
                print(bestNode.board)
                self.board.grid=bestNode.board
                self.view.update_board(bestNode.board.copy())
                self.switch_player()
                self.view.update_status(self.current_player)




                # if self.ai_algorithm == "aggressive":
                #     col=self.heuristic_function.aggressive_heuristic(self.board.grid, 1)
                #     self.handle_click(col)
                # elif self.ai_algorithm == "defensive":
                #     # Call defensive AI logic
                #     #  print(self.board.grid)
                #     col = self.heuristic_function.defensive_heuristic(self.board.grid, 1)
                #     self.handle_click(col)
                #     pass
            
                # elif self.ai_algorithm == "Heuristic AI":
                #     # Call random AI logic
                #     #  print(self.board.grid)
                #     col = self.heuristic_function.heuristic_ai(self.board.grid, 1)
                #     self.handle_click(col)
                #     pass
            else:
                col = self.heuristic_function.random_choice(self.board.grid)
                self.handle_click(col)
                
    def switch_player(self):
        
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        if(self.current_player=='O'):
            # how to wait 1000 milliseconds before switching
            self.view.after(1000, self.ai_move)
            

    def reset_game(self):
        self.board.reset()
        self.current_player = 'X'
        self.view.reset_board()
        self.view.update_status(self.current_player)
