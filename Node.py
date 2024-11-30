import copy


class Node:
    """
    Node representing a state in the decision tree.
    """
    def __init__(self, board, score=0, move=None):
        self.board = copy.deepcopy(board)  # Board state
        self.score = score                # Evaluation score of the state
        self.move = move                  # Move that led to this state
        self.children = []  