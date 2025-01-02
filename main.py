from GomokuGameState import GomokuGameState
from MonteCarloTreeSearch import MonteCarloTreeSearch
import time
import os

#easy
#-5 +1 +0.5
#200
#5000

#hard
#-5 +1 +0.5
#200
#10000


game = GomokuGameState(15)
result = True
loop = 0

print('1. Dễ')
print('2. Khó')
while result:
    selection = int(input('Chọn mức độ: '))
    if selection == 1 or selection == 2:
        loop = 5000 if selection == 1 else 10000
        result = False
os.system('cls')

game.print_board()
while not game.is_terminal:

    while not result:
        print('Lượt của bạn ...')
        row = int(input('Hàng: '))
        column = int(input('Cột: '))
        result = game.play((row, column))
        os.system('cls')
        game.print_board()

    result = False

    print('MCTS đang suy nghĩ ...') 
    start_time = time.time()
    MCTS = MonteCarloTreeSearch(loop, game)
    best_move = MCTS.search()
    game.play(best_move)
    end_time = time.time()
    os.system('cls')
    print(f'MCTS suy nghĩ trong {end_time - start_time:.0f} giây ...') 
    game.print_board()

if game.winner == -1:
    print('Hòa')
else:
    print(f"{'X' if game.winner == 1 else 'O'} thắng")

os.system('pause')