import math
import random
from copy import copy
from GomokuGameState import GomokuGameState
from MCTSMeta import MCTSMeta
import numpy as np

class MCTSNode(GomokuGameState):
    def __init__(self, parent = None, game_state = None) -> None:
        super().__init__(game_state = game_state)
        self.parent = parent
        self.player_make_move = self.get_player_make_move()
        self.available_expand_move = copy(self.available_move)
        self.children = []
        self.q_UCT = 0
        self.n_UCT = 0
        self.q_AMAF = 0
        self.n_AMAF = 0

    def play(self, move):
        super().play(move)
        self.available_expand_move.remove(move)
        self.player_make_move = self.get_player_make_move()

    def get_boundaries(self):
        board = self.board
        top_row = -1
        bottom_row = -1
        left_column = -1
        right_column = -1

        for i in range(self.size):
            if top_row == -1 and np.any(board[i, :] != -1):
                top_row = i
            
            if left_column == -1 and np.any(board[:, i] != -1):
                left_column = i
            
            if top_row != -1 and left_column != -1:
                break

        for i in range(self.size - 1, -1, -1):
            if bottom_row == -1 and np.any(board[i, :] != -1):
                bottom_row = i
            
            if right_column == -1 and np.any(board[:, i] != -1):
                right_column = i
            
            if bottom_row != -1 and right_column != -1:
                break

        return top_row, bottom_row, left_column, right_column

    def set_new_available_move(self): # -> {(),(),...}
        available_move = set()
        board = self.board

        top_row, bottom_row, left_col, right_col = self.get_boundaries()
        top_row, left_col = top_row - 4, left_col - 4
        bottom_row, right_col = bottom_row + 4, right_col + 4

        while top_row < 0:
            top_row += 1
         
        while bottom_row >= self.size:
            bottom_row -= 1

        while left_col < 0:
            left_col += 1

        while right_col >= self.size:
            right_col -= 1
        
        for i in range(top_row, bottom_row + 1):
            for j in range(left_col, right_col + 1):
                if board[i, j] == -1:
                    available_move.add((i, j))
        
        self.available_move = available_move
        self.available_expand_move = copy(available_move)
                
    def get_player_make_move(self):
        if self.is_terminal:
            return self.turn 
        else:
            return 1 - self.turn

    def pop_random_expand_move(self):
        move = random.choice(list(self.available_expand_move))
        self.available_expand_move.remove(move)
        return move

    def random_choice_available_move(self):
        move = random.choice(list(self.available_move))
        return move

    def is_expandable(self):
        return self.available_expand_move

    def add_child(self, node):
        self.children.append(node)

    def UCT(self):
        if self.n_UCT != 0:
            exploration = 2 * MCTSMeta.Cp * math.sqrt( (2 * math.log(self.parent.n_UCT)) / self.n_UCT) 
            exploitation = self.q_UCT / self.n_UCT 
            return exploitation + exploration 
        else:
            return float('inf') 

    def AMAF(self):
        if self.n_AMAF != 0:
            return self.q_AMAF / self.n_AMAF 
        return 0 

    def RAVE(self) -> float:
        if MCTSMeta.C_AMAF == 0:
            alpha = 0 
        else:
            alpha = max(0, ((MCTSMeta.C_AMAF - self.n_UCT) / MCTSMeta.C_AMAF) )
        return alpha * self.AMAF() + (1 - alpha) * self.UCT() 