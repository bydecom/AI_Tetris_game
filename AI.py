import threading
import pygame
import time
import tetris
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt','dos'):
        command = 'cls'
    os.system(command)


rotations = {'T': 4, 'L':4, 'J':4, 'S': 2, 'Z': 2, 'I': 2, 'O': 1}
def possible_board_states(app=tetris.TetrisApp):
    states = []
    stone = [row[:] for row in app.stone]
    for r in range(0, rotations[app.stone_letter]):
        for i in range(0,(len(app.board[0]) - len(stone[0])+1)):
            temp_board = drop([row[:] for row in app.board],  stone, i, app.stone_y//1)
            states.append({'num_rotations': r, 'board':temp_board[:], 'stone_x':i, 'heuristic':holes_heuristic(temp_board[:])})
        stone = tetris.rotate_clockwise(stone)
    return states

# 
def drop(board, stone, stone_x, stone_y):
    while not tetris.check_collision(board,
                        stone,
                        (stone_x, stone_y)):
            stone_y += 1
    return tetris.join_matrixes(
        board,
        stone,
        (stone_x, stone_y))


# Heuristic on the 'height' of the grid
def height_heuristic(board: list) -> int:
    height = len(board)-1
    width = len(board[0])
    # print(height,width)
    # Find highest block in each column
    highest_blocks = [0 for _ in range(width)]
    for x in range(width):
        if (highest_blocks[x] > 0): continue
        for y in range(height):
            if (board[y][x] > 0):
                # print("Found a block at",y,x,"=",0 + (height-y-1))
                highest_blocks[x] = 0 + (height-y)
                break
    return sum(highest_blocks)

# Heuristic based on the number of holes in the grid and their placement
def holes_heuristic(board: list) -> int:
    # Top-left of board is (0,0)
    height = len(board)-1
    width = len(board[0])
    total = 0
    top_blocks = [height for _ in range(width)]
    for y in range(height):
        for x in range(width):
            # Find highest block of the column
            if(board[y][x] > 0 and top_blocks[x] > y):
                top_blocks[x] = y
                # Check for holes under highest block
                for i in range(y+1,height):
                    if(board[i][x] == 0):
                        total += (height-i)**3
                # Cell to the left of a peak is also a hole
                if(0 <= x-1 and board[y][x-1] == 0):
                    total += (height-y)**2
                continue
            # Check if cell is surrounded by a 'tower'
            if(0 <= x-1):
                if(top_blocks[x-1] <= y and board[y][x] == 0): 
                    # print("Cell",(x,y),"is to the right of peak",(x-1,top_blocks[x-1]),"+1")
                    total += (height-y)**2
            if(x+1 < width):
                if(top_blocks[x+1] <= y and board[y][x] == 0): 
                    # print("Cell",(x,y),"is to the left of peak",(x+1,top_blocks[x+1]),"+1")
                    total += (height-y)**2
    return total
    
def best_fs(states):
    min_state = states[0]
    for state in states:
        if state['heuristic'] < min_state['heuristic']:
            min_state = dict(state)
    return min_state

def AI(app = tetris.TetrisApp):
    while not app.gameover:
        state = best_fs(possible_board_states(app))
        for n in range(0, state['num_rotations']):
            app.rotate_stone()
        while state['stone_x'] < app.stone_x:
            state
            time.sleep(0.5)
            app.move(-1)
        while state['stone_x'] > app.stone_x:
            state
            time.sleep(0.5)
            app.move(+1)
        time.sleep(0.5)
        app.insta_drop()
        time.sleep(0.5)
    print(app.level)
    print(app.score)
    print()
    pygame.event.post(pygame.event.Event(pygame.QUIT))

if __name__ == 'AI':
    app = tetris.TetrisApp()
    t1 = threading.Thread(target=app.run)
    t2 = threading.Thread(target=AI, args=(app,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
