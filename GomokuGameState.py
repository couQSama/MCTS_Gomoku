import numpy as np
import random
from copy import copy

class GomokuGameState:
    def __init__(self, size = 5, game_state = None) -> None:
        if game_state:
            self.board = np.copy(game_state.board)
            self.available_move = copy(game_state.available_move)
            self.turn = game_state.turn
            self.is_terminal = game_state.is_terminal
            self.winner = game_state.winner
            self.last_move = game_state.last_move
        else:
            size = max(5, min(size, 51))
            self.board = np.full((size, size), -1, dtype = np.int8)
            self.available_move = {(i, j) for i in range(size) for j in range(size)}
            self.turn = 0
            self.is_terminal = False
            self.winner = -1
            self.last_move = None
        self.size = self.board.shape[0]

    def random_choice_available_move(self):
        return random.choice(list(self.available_move))

    def is_valid_move(self, move):
        return move in self.available_move

    def check_player_win(self, move):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        x, y = move

        for dx, dy in directions:
            count = 1
            for dir in [1, -1]:
                nx = x + dx * dir
                ny = y + dy * dir
                while 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx, ny] == self.turn:
                    count += 1
                    if count == 5:
                        return True
                    nx += dx * dir
                    ny += dy * dir

        return False 

    def play(self, move):

        if self.is_terminal or not self.is_valid_move(move):
            return False

        board = self.board
        turn = self.turn
        r, c = move

        board[r, c] = turn
        self.last_move = move
        self.available_move.remove(move)

        if self.check_player_win(move):
            self.winner = turn
            self.is_terminal = True
        elif not self.available_move:
            self.is_terminal = True
        else:
            self.turn = 1 - turn

        return True 

    def print_board(self):
        # Print column headers (numeric)
        print('  ', end=' ')
        for i in range(self.size):
            space = '  ' if i < 10 else ' '
            print(f"{i}", end=space)
        print()

        last_row, last_col = self.last_move if self.last_move else (-1, -1)

        # Print rows with row numbers and board contents
        for i in range(self.size):
            print(f"{i:2}", end=" ")  # Row number
            for j in range(self.size):
                if self.board[i, j] == -1:
                    print(".", end='  ')
                elif self.board[i, j] == 1:
                    if i == last_row and j == last_col:
                        print("\033[43;31m" + "X\033[0;0m", end='  ')
                    else:
                        print("\033[0;31m" + "X\033[0;0m", end='  ')
                else:
                    if i == last_row and j == last_col:
                        print("\033[43;34m" + "O\033[0;0m", end='  ')
                    else:
                        print("\033[0;34m" + "O\033[0;0m", end='  ')
            print()  # Newline