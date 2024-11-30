"""Board state and game logic"""

class BoardModel:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    
        
    def is_valid_move(self, col):
        return 0 <= col < self.cols and self.grid[0][col] == ' '
    
    def get_next_open_row(self, col):
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == ' ':
                return row
        return -1
    
    def make_move(self, col, player):
        row = self.get_next_open_row(col)
        if row != -1:
            self.grid[row][col] = player
            return True, row
        return False, -1
    
    def check_winner(self, player):
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.grid[row][col + i] == player for i in range(4)):
                    return True
        
        # Check vertical
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if all(self.grid[row + i][col] == player for i in range(4)):
                    return True
        
        # Check diagonal (positive slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.grid[row + i][col + i] == player for i in range(4)):
                    return True
        
        # Check diagonal (negative slope)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if all(self.grid[row - i][col + i] == player for i in range(4)):
                    return True
        
        return False
    
    def is_full(self):
        return all(self.grid[0][col] != ' ' for col in range(self.cols))
    
    def reset(self):
        self.grid = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]