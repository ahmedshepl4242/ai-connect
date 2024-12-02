"""Main application entry point"""

import tkinter as tk
from Heustric import HeuristicFunction
from MinMax import MinMax
from board_model import BoardModel
from board_view import BoardView
from game_controller import GameController
from constants import *

class ConnectFourApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect Four")
        self.root.configure(bg=BG_COLOR)
        max_depth=6
        
        # Initialize MVC components
        heuristic_function= HeuristicFunction(max_depth)
        minMax=MinMax(max_depth,True)
        self.board_model = BoardModel(ROWS, COLS)
        self.game_controller = GameController(max_depth,self.board_model, None,heuristic_function,minMax)
        self.board_view = BoardView(self.root, self.game_controller)
        
        # Connect view to controller
        self.game_controller.view = self.board_view
        
        self.board_view.pack(padx=20, pady=20)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ConnectFourApp()
    app.run()