import tkinter as tk
from constants import *  # Ensure constants like BG_COLOR, CELL_SIZE, etc., are defined elsewhere

class BoardView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg=BG_COLOR)
        self.controller = controller
        self.status_label = None  # Initialize status_label to avoid AttributeError
        self.setup_ui()
        
    def setup_ui(self):
        # Create a container frame for the algorithm selection
        self.algorithm_frame = tk.Frame(self, bg=BG_COLOR)
        self.algorithm_frame.pack(pady=20)
        
        tk.Label(
            self.algorithm_frame,
            text="Select AI Algorithm",
            font=('Arial', 16),
            bg=BG_COLOR
        ).pack(pady=10)
        
        # Buttons to select AI algorithms
        tk.Button(
            self.algorithm_frame,
            text="Aggressive AI",
            font=('Arial', 12),
            command=lambda: self.start_game("aggressive")
        ).pack(pady=5)
        
        tk.Button(
            self.algorithm_frame,
            text="Defensive AI",
            font=('Arial', 12),
            command=lambda: self.start_game("defensive")
        ).pack(pady=5)
        
        tk.Button(
            self.algorithm_frame,
            text="Random AI",
            font=('Arial', 12),
            command=lambda: self.start_game("random")
        ).pack(pady=5)

        tk.Button(
            self.algorithm_frame,
            text="Heuristic AI",
            font=('Arial', 12),
            command=lambda: self.start_game("Heuristic AI")
        ).pack(pady=5)
        tk.Button(
            self.algorithm_frame,
            text="other",
            font=('Arial', 12),
            command=lambda: self.start_game("other")
        ).pack(pady=5)
        
        # The game board will be hidden initially
        self.board_frame = None
    
    def start_game(self, algorithm):
        """Start the game with the selected AI algorithm."""
        self.controller.set_algorithm(algorithm)
        
        # Hide the algorithm selection and display the game board
        self.algorithm_frame.pack_forget()
        self.create_board()
    
    def create_board(self):
        # Create the game board UI
        self.board_frame = tk.Frame(
            self,
            bg=BOARD_COLOR,
            padx=PADDING,
            pady=PADDING
        )
        self.board_frame.pack()

      
         # Scoreboard frame
        self.score_frame = tk.Frame(self, bg=BG_COLOR)
        self.score_frame.pack(pady=10)

        # Human score label
        self.human_score_label = tk.Label(
            self.score_frame,
            text=f"Human:{self.controller.board.score['X']}",
            font=('Arial', 12),
            bg=BG_COLOR
        )
        self.human_score_label.grid(row=0, column=0, padx=10)

        # AI score label
        self.ai_score_label = tk.Label(
            self.score_frame,
            text= f"AI: {self.controller.board.score['O']}",

            font=('Arial', 12),
            bg=BG_COLOR
        )
        self.ai_score_label.grid(row=0, column=1, padx=10)


        #  board 
        
        # Create status label
        self.status_label = tk.Label(
            self,
            text="Player X's turn",  # Initial message
            font=('Arial', 16),
            bg=BG_COLOR
        )
        self.status_label.pack(pady=10)
        
        self.cells = []
        for row in range(ROWS):
            row_cells = []
            for col in range(COLS):
                cell = tk.Canvas(
                    self.board_frame,
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    bg=BOARD_COLOR,
                    highlightthickness=0
                )
                cell.grid(row=row, column=col, padx=2, pady=2)
                cell.bind('<Button-1>', lambda e, col=col: self.controller.handle_click(col))
                
                # Create empty circle
                cell.create_oval(
                    CELL_SIZE//2 - PIECE_RADIUS,
                    CELL_SIZE//2 - PIECE_RADIUS,
                    CELL_SIZE//2 + PIECE_RADIUS,
                    CELL_SIZE//2 + PIECE_RADIUS,
                    fill=EMPTY_COLOR
                )
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        # Create reset button
        reset_button = tk.Button(
            self,
            text="New Game",
            command=self.controller.reset_game,
            font=('Arial', 12)
        )
        reset_button.pack(pady=10)
    
    def update_cell(self, row, col, player):
        """Update a cell with the player's marker."""
        cell = self.cells[row][col]
        cell.delete("all")
        cell.create_oval(
            CELL_SIZE//2 - PIECE_RADIUS,
            CELL_SIZE//2 - PIECE_RADIUS,
            CELL_SIZE//2 + PIECE_RADIUS,
            CELL_SIZE//2 + PIECE_RADIUS,
            fill=PLAYER_COLORS[player]
        )
        self.update_scores()

     

    def update_scores(self):
        """Update the score labels dynamically."""
        self.human_score_label.config(text=f"Human: {self.controller.board.score['X']}")
        self.ai_score_label.config(text=f"AI: {self.controller.board.score['O']}")

    def update_board(self, board):
        """Update the entire board based on the current state."""
        for row in range(ROWS):
            for col in range(COLS):
                cell = self.cells[row][col]
                cell.delete("all")  # Remove previous content (if any)
                
                # Get the current state from the board (could be 'X', 'O', or ' ')
                player = board[row][col]
                
                if player != ' ':  # Only update non-empty cells
                    cell.create_oval(
                        CELL_SIZE//2 - PIECE_RADIUS,
                        CELL_SIZE//2 - PIECE_RADIUS,
                        CELL_SIZE//2 + PIECE_RADIUS,
                        CELL_SIZE//2 + PIECE_RADIUS,
                        fill=PLAYER_COLORS[player]  # Set color based on the player (red for X, yellow for O)
                    )
                    # self.update_scores()

                    
                else:
                    # Optionally, you could redraw empty cells with an empty circle
                    cell.create_oval(
                        CELL_SIZE//2 - PIECE_RADIUS,
                        CELL_SIZE//2 - PIECE_RADIUS,
                        CELL_SIZE//2 + PIECE_RADIUS,
                        CELL_SIZE//2 + PIECE_RADIUS,
                        fill=EMPTY_COLOR  # Default empty color
                    )


    
    def update_status(self, player):
        """Update the status label with the current player's turn."""
        if self.status_label:  # Ensure status_label exists
            if player == 'X':
                self.status_label.config(text=f"Player {player}'s turn")
            else:
                self.status_label.config(text=f"AI's turn")
    
    def reset_board(self):
        """Reset the board to its initial state."""
        for row in range(ROWS):
            for col in range(COLS):
                cell = self.cells[row][col]
                cell.delete("all")
                cell.create_oval(
                    CELL_SIZE//2 - PIECE_RADIUS,
                    CELL_SIZE//2 - PIECE_RADIUS,
                    CELL_SIZE//2 + PIECE_RADIUS,
                    CELL_SIZE//2 + PIECE_RADIUS,
                    fill=EMPTY_COLOR
                )
