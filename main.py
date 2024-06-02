import pygame
import random
# import AI
from settings import *
from sprite import *
from ui import *
from collections import deque

pygame.init()

# BASIC GAME FUNCTIONS
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % (len(shape.shape))]

    for i, row in enumerate(format):
        for j, col in enumerate(row):
            if col == "0":
                positions.append((shape.x+j, shape.y+i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0]-2, pos[1]-4)
    return positions

def valid_space(shape, grid):
    accepted_pos = [(j,i) for j in range(10) for i in range(20) if grid[i][j] == (0, 0, 0)]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def clear_row(grid, locked_pos):
    inc = 0

    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            index = i

            for j in range(len(row)):
                try:
                    del locked_pos[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked_pos), key=lambda x:x[1], reverse=True):
            x, y = key
            if y < index:
                new_key = (x, y+inc)
                locked_pos[new_key] = locked_pos.pop(key)
    return inc

def get_shape():
    return Piece(int((GAME_WIDTH/BLOCK_SIZE)/2), 0, random.choice(SHAPES))

# ALGORITHM FUNCTIONS
def get_possible_moves(shape, grid):
    actions = ['left', 'right', 'rotate', 'drop']

    test_shape = shape.copy()

    test_shape.x -= 1
    if not valid_space(test_shape, grid):
        actions.remove('left')
    test_shape.x += 2
    if not valid_space(test_shape, grid):
        actions.remove('right')
    test_shape.x -= 1

    test_shape.rotation = (test_shape.rotation + 1) % len(test_shape.shape)
    if not valid_space(test_shape, grid):
        actions.remove('rotate')
    test_shape.rotation = (test_shape.rotation - 1) % len(test_shape.shape)

    return actions

def move(shape, action, grid):
    new_state = shape.copy()

    if action == 'left':
        new_state.x -= 1
    elif action == 'right':
        new_state.x += 1
    elif action == 'rotate':
        new_state.rotation = (new_state.rotation + 1) % len(new_state.shape)
    elif action == 'drop':
        while valid_space(new_state, grid):
            new_state.y += 1
        new_state.y -= 1
    return new_state

# ALGORITHMS
def breadth_first_search(start_shape, goal_shape, grid):
    queue = deque([[start_shape]])
    visited = set([start_shape])

    while queue:
        path = queue.popleft()
        shape = path[-1]

        if shape == goal_shape:
            return path
        
        for action in get_possible_moves(shape):
            next_shape = move(shape, action, grid)

            if next_shape not in visited:
                visited.add(next_shape)
                new_path = list(path)
                new_path.append(next_shape)
                queue.append(new_path)
    return None

def depth_first_search():
    pass

def uniform_cost_search():
    pass

def greedy():
    pass

def a_star():
    pass

# GAME MODES
def Singleplayer(surface):
    run = True

    p_locked_positions = {}
    p_change_piece = False
    p_current_piece = get_shape()
    p_next_piece = get_shape()
    p_score = 0

    clock = pygame.time.Clock()
    fall_speed = 0.27
    fall_time = 0
    level = 1
    level_time = 0

    while run:
        p_grid = create_grid(p_locked_positions)

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()

        clock.tick()

        if level_time/1000 > 15:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.01
                level += 1
        
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            p_current_piece.y += 1

            if not(valid_space(p_current_piece, p_grid)) and p_current_piece.y > 0:
                p_current_piece.y -= 1
                p_change_piece = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused_time = clock
                    pause(surface, clock)
                    clock = paused_time
                
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    p_current_piece.rotation += 1
                    if not (valid_space(p_current_piece, p_grid)):
                        p_current_piece.rotation -= 1
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    p_current_piece.x -= 1
                    if not(valid_space(p_current_piece, p_grid)):
                        p_current_piece.x += 1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    p_current_piece.y += 1
                    if not(valid_space(p_current_piece, p_grid)):
                        p_current_piece.y -= 1
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    p_current_piece.x += 1
                    if not(valid_space(p_current_piece, p_grid)):
                        p_current_piece.x -= 1
        
        p_shape_pos = convert_shape_format(p_current_piece)

        for i in range(len(p_shape_pos)):
            x, y = p_shape_pos[i]
            if y > -1:
                p_grid[y][x] = p_current_piece.color

        if p_change_piece:
            for pos in p_shape_pos:
                p = (pos[0], pos[1])
                p_locked_positions[p] = p_current_piece.color
            p_current_piece = p_next_piece
            p_next_piece = get_shape()
            p_change_piece = False
            p_score += clear_row(p_grid, p_locked_positions) * 10 * level

        if check_lost(p_locked_positions):
            loser_text = Label("YOU LOST!!!", 60, bold=True)
            loser_text.draw(surface, TOP_LEFT_X_SINGLE+GAME_WIDTH/2, TOP_LEFT_Y+GAME_HEIGHT/2, True)

            pygame.display.update()
            pygame.time.delay(3000)
            run = False
        
        draw_window(surface, grid_1=p_grid, score_1=p_score, speed=fall_speed, single_mode=True)
        draw_next_shape(surface, shape_1=p_next_piece, single_mode=True)

        pygame.display.flip()

def PlayerVsPlayer(surface):
    run = True

    p1_locked_positions = {}
    p1_change_piece = False
    p1_current_piece = get_shape()
    p1_next_piece = get_shape()
    p1_score = 0

    p2_locked_positions = {}
    p2_change_piece = False
    p2_current_piece = get_shape()
    p2_next_piece = get_shape()
    p2_score = 0

    clock = pygame.time.Clock()
    fall_speed = 0.27
    fall_time = 0
    level = 1
    level_time = 0

    while run:
        p1_grid = create_grid(p1_locked_positions)
        p2_grid = create_grid(p2_locked_positions)

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()

        clock.tick()

        if level_time/1000 > 15:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.01
                level += 1
        
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            p1_current_piece.y += 1
            p2_current_piece.y += 1

            if not(valid_space(p1_current_piece, p1_grid)) and p1_current_piece.y > 0:
                p1_current_piece.y -= 1
                p1_change_piece = True
            if not(valid_space(p2_current_piece, p2_grid)) and p2_current_piece.y > 0:
                p2_current_piece.y -= 1
                p2_change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # GENERAL EVENTS
                if event.key == pygame.K_SPACE:
                    paused_time = clock
                    pause(surface, clock)
                    clock = paused_time

                # PLAYER 1 EVENTS
                if event.key == pygame.K_w:
                    p1_current_piece.rotation += 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.rotation -= 1
                if event.key == pygame.K_a:
                    p1_current_piece.x -= 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.x += 1
                if event.key == pygame.K_s:
                    p1_current_piece.y += 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.y -= 1
                if event.key == pygame.K_d:
                    p1_current_piece.x += 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.x -= 1

                # PLAYER 2 EVENTS
                if event.key == pygame.K_UP:
                    p2_current_piece.rotation += 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.rotation -= 1
                if event.key == pygame.K_LEFT:
                    p2_current_piece.x -= 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.x += 1
                if event.key == pygame.K_DOWN:
                    p2_current_piece.y += 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.y -= 1
                if event.key == pygame.K_RIGHT:
                    p2_current_piece.x += 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.x -= 1
        
        p1_shape_pos = convert_shape_format(p1_current_piece)
        p2_shape_pos = convert_shape_format(p2_current_piece)

        for i in range(len(p1_shape_pos)):
            x, y = p1_shape_pos[i]
            if y > -1:
                p1_grid[y][x] = p1_current_piece.color
        for i in range(len(p2_shape_pos)):
            x, y = p2_shape_pos[i]
            if y > -1:
                p2_grid[y][x] = p2_current_piece.color

        if p1_change_piece:
            for pos in p1_shape_pos:
                p = (pos[0], pos[1])
                p1_locked_positions[p] = p1_current_piece.color
            p1_current_piece = p1_next_piece
            p1_next_piece = get_shape()
            p1_change_piece = False
            p1_score += clear_row(p1_grid, p1_locked_positions) * 10 * level

        if p2_change_piece:
            for pos in p2_shape_pos:
                p = (pos[0], pos[1])
                p2_locked_positions[p] = p2_current_piece.color
            p2_current_piece = p2_next_piece
            p2_next_piece = get_shape()
            p2_change_piece = False
            p2_score += clear_row(p2_grid, p2_locked_positions) * 10 * level

        if check_lost(p1_locked_positions) or check_lost(p2_locked_positions):
            winner_text = Label("YOU WIN!!!", 60, bold=True)
            loser_text = Label("YOU LOST!!!", 60, bold=True)

            if check_lost(p1_locked_positions):
                winner_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2+MID_X, TOP_LEFT_Y+GAME_HEIGHT/2, True)
                loser_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2, TOP_LEFT_Y+GAME_HEIGHT/2, True)
            if check_lost(p2_locked_positions):
                winner_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2, TOP_LEFT_Y+GAME_HEIGHT/2, True)
                loser_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2+MID_X, TOP_LEFT_Y+GAME_HEIGHT/2, True)

            pygame.display.update()
            pygame.time.delay(3000)
            run = False
        
        draw_window(surface, p1_grid, p2_grid, p1_score, p2_score, level, fall_speed, add=int(MID_X))
        draw_next_shape(surface, p1_next_piece, p2_next_piece, add=int(MID_X))

        pygame.display.update()

def PlayerVsAI(surface):
    run = True

    p1_locked_positions = {}
    p1_change_piece = False
    p1_current_piece = get_shape()
    p1_next_piece = get_shape()
    p1_score = 0

    p2_locked_positions = {}
    p2_change_piece = False
    p2_current_piece = get_shape()
    p2_next_piece = get_shape()
    p2_score = 0

    clock = pygame.time.Clock()
    fall_speed = 0.27
    fall_time = 0
    level = 1
    level_time = 0

    while run:
        p1_grid = create_grid(p1_locked_positions)
        p2_grid = create_grid(p2_locked_positions)

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()

        clock.tick()

        if level_time/1000 > 15:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.01
                level += 1
        
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            p1_current_piece.y += 1
            p2_current_piece.y += 1

            if not(valid_space(p1_current_piece, p1_grid)) and p1_current_piece.y > 0:
                p1_current_piece.y -= 1
                p1_change_piece = True
            if not(valid_space(p2_current_piece, p2_grid)) and p2_current_piece.y > 0:
                p2_current_piece.y -= 1
                p2_change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # GENERAL EVENTS
                if event.key == pygame.K_SPACE:
                    paused_time = clock
                    pause(surface, clock)
                    clock = paused_time

                # PLAYER 1 EVENTS
                if event.key == pygame.K_w:
                    p1_current_piece.rotation += 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.rotation -= 1
                if event.key == pygame.K_a:
                    p1_current_piece.x -= 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.x += 1
                if event.key == pygame.K_s:
                    p1_current_piece.y += 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.y -= 1
                if event.key == pygame.K_d:
                    p1_current_piece.x += 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.x -= 1

                # PLAYER 2 EVENTS
                if event.key == pygame.K_UP:
                    p2_current_piece.rotation += 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.rotation -= 1
                if event.key == pygame.K_LEFT:
                    p2_current_piece.x -= 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.x += 1
                if event.key == pygame.K_DOWN:
                    p2_current_piece.y += 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.y -= 1
                if event.key == pygame.K_RIGHT:
                    p2_current_piece.x += 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.x -= 1
        
        p1_shape_pos = convert_shape_format(p1_current_piece)
        p2_shape_pos = convert_shape_format(p2_current_piece)

        for i in range(len(p1_shape_pos)):
            x, y = p1_shape_pos[i]
            if y > -1:
                p1_grid[y][x] = p1_current_piece.color
        for i in range(len(p2_shape_pos)):
            x, y = p2_shape_pos[i]
            if y > -1:
                p2_grid[y][x] = p2_current_piece.color

        if p1_change_piece:
            for pos in p1_shape_pos:
                p = (pos[0], pos[1])
                p1_locked_positions[p] = p1_current_piece.color
            p1_current_piece = p1_next_piece
            p1_next_piece = get_shape()
            p1_change_piece = False
            p1_score += clear_row(p1_grid, p1_locked_positions) * 10 * level

        if p2_change_piece:
            for pos in p2_shape_pos:
                p = (pos[0], pos[1])
                p2_locked_positions[p] = p2_current_piece.color
            p2_current_piece = p2_next_piece
            p2_next_piece = get_shape()
            p2_change_piece = False
            p2_score += clear_row(p2_grid, p2_locked_positions) * 10 * level

        if check_lost(p1_locked_positions) or check_lost(p2_locked_positions):
            winner_text = Label("YOU WIN!!!", 60, bold=True)
            loser_text = Label("YOU LOST!!!", 60, bold=True)

            if check_lost(p1_locked_positions):
                winner_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2+MID_X, TOP_LEFT_Y+GAME_HEIGHT/2, True)
                loser_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2, TOP_LEFT_Y+GAME_HEIGHT/2, True)
            if check_lost(p2_locked_positions):
                winner_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2, TOP_LEFT_Y+GAME_HEIGHT/2, True)
                loser_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2+MID_X, TOP_LEFT_Y+GAME_HEIGHT/2, True)

            pygame.display.update()
            pygame.time.delay(3000)
            run = False
        
        draw_window(surface, p1_grid, p2_grid, p1_score, p2_score, level, fall_speed, add=int(MID_X))
        draw_next_shape(surface, p1_next_piece, p2_next_piece, add=int(MID_X))

        pygame.display.update()

def AIVsAI(surface):
    run = True

    p1_locked_positions = {}
    p1_change_piece = False
    p1_current_piece = get_shape()
    p1_next_piece = get_shape()
    p1_score = 0

    p2_locked_positions = {}
    p2_change_piece = False
    p2_current_piece = get_shape()
    p2_next_piece = get_shape()
    p2_score = 0

    clock = pygame.time.Clock()
    fall_speed = 0.27
    fall_time = 0
    level = 1
    level_time = 0

    while run:
        p1_grid = create_grid(p1_locked_positions)
        p2_grid = create_grid(p2_locked_positions)

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()

        clock.tick()

        if level_time/1000 > 15:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.01
                level += 1
        
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            p1_current_piece.y += 1
            p2_current_piece.y += 1

            if not(valid_space(p1_current_piece, p1_grid)) and p1_current_piece.y > 0:
                p1_current_piece.y -= 1
                p1_change_piece = True
            if not(valid_space(p2_current_piece, p2_grid)) and p2_current_piece.y > 0:
                p2_current_piece.y -= 1
                p2_change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # GENERAL EVENTS
                if event.key == pygame.K_SPACE:
                    paused_time = clock
                    pause(surface, clock)
                    clock = paused_time

                # PLAYER 1 EVENTS
                if event.key == pygame.K_w:
                    p1_current_piece.rotation += 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.rotation -= 1
                if event.key == pygame.K_a:
                    p1_current_piece.x -= 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.x += 1
                if event.key == pygame.K_s:
                    p1_current_piece.y += 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.y -= 1
                if event.key == pygame.K_d:
                    p1_current_piece.x += 1
                    if not(valid_space(p1_current_piece, p1_grid)):
                        p1_current_piece.x -= 1

                # PLAYER 2 EVENTS
                if event.key == pygame.K_UP:
                    p2_current_piece.rotation += 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.rotation -= 1
                if event.key == pygame.K_LEFT:
                    p2_current_piece.x -= 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.x += 1
                if event.key == pygame.K_DOWN:
                    p2_current_piece.y += 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.y -= 1
                if event.key == pygame.K_RIGHT:
                    p2_current_piece.x += 1
                    if not(valid_space(p2_current_piece, p2_grid)):
                        p2_current_piece.x -= 1
        
        p1_shape_pos = convert_shape_format(p1_current_piece)
        p2_shape_pos = convert_shape_format(p2_current_piece)

        for i in range(len(p1_shape_pos)):
            x, y = p1_shape_pos[i]
            if y > -1:
                p1_grid[y][x] = p1_current_piece.color
        for i in range(len(p2_shape_pos)):
            x, y = p2_shape_pos[i]
            if y > -1:
                p2_grid[y][x] = p2_current_piece.color

        if p1_change_piece:
            for pos in p1_shape_pos:
                p = (pos[0], pos[1])
                p1_locked_positions[p] = p1_current_piece.color
            p1_current_piece = p1_next_piece
            p1_next_piece = get_shape()
            p1_change_piece = False
            p1_score += clear_row(p1_grid, p1_locked_positions) * 10 * level

        if p2_change_piece:
            for pos in p2_shape_pos:
                p = (pos[0], pos[1])
                p2_locked_positions[p] = p2_current_piece.color
            p2_current_piece = p2_next_piece
            p2_next_piece = get_shape()
            p2_change_piece = False
            p2_score += clear_row(p2_grid, p2_locked_positions) * 10 * level

        if check_lost(p1_locked_positions) or check_lost(p2_locked_positions):
            winner_text = Label("YOU WIN!!!", 60, bold=True)
            loser_text = Label("YOU LOST!!!", 60, bold=True)

            if check_lost(p1_locked_positions):
                winner_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2+MID_X, TOP_LEFT_Y+GAME_HEIGHT/2, True)
                loser_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2, TOP_LEFT_Y+GAME_HEIGHT/2, True)
            if check_lost(p2_locked_positions):
                winner_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2, TOP_LEFT_Y+GAME_HEIGHT/2, True)
                loser_text.draw(surface, TOP_LEFT_X+GAME_WIDTH/2+MID_X, TOP_LEFT_Y+GAME_HEIGHT/2, True)

            pygame.display.update()
            pygame.time.delay(3000)
            run = False
        
        draw_window(surface, p1_grid, p2_grid, p1_score, p2_score, level, fall_speed, add=int(MID_X), num_of_AI=2)
        draw_next_shape(surface, p1_next_piece, p2_next_piece, add=int(MID_X))

        pygame.display.update()

# PAUSE SCREEN
def pause(surface, clock):
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                if event.key == pygame.K_q:
                    paused = False
                    main_menu()
        
        surface.fill(BLACK)
        pause_text = Label("PAUSED", 50, bold=True)
        pause_text.draw(surface, MID_X, MID_Y, True)
        unpause_text = Label("Press SPACE to continue", 20, bold=True, italic=True)
        unpause_text.draw(surface, MID_X, MID_Y + 150, True)
        quit_text = Label("Press Q to return to main menu", 20, bold=True, italic=True)
        quit_text.draw(surface, MID_X, MID_Y + 180, True)

        pygame.display.update()
        clock.tick(5)

    surface.fill(BLACK)
    resume_text = Label("RESUMING IN 2 SECONDS...", 30, bold=True, italic=True)
    resume_text.draw(surface, MID_X, MID_Y, True)

    pygame.display.update()
    pygame.time.delay(2000)
    clock.tick(5)

# INFO SCREEN
def info_page(surface):
    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    show = False
        
        surface.fill(BLACK)
        pygame.draw.line(surface, WHITE, (WINDOW_WIDTH/2, 75), (WINDOW_WIDTH/2, WINDOW_HEIGHT-40))
        pygame.draw.line(surface, WHITE, (0, 75), (WINDOW_WIDTH, 75))
        pygame.draw.line(surface, WHITE, (0, WINDOW_HEIGHT-40), (WINDOW_WIDTH, WINDOW_HEIGHT-40))

        info_text = Label("INFO", 50, bold=True, italic=True)
        info_text.draw(surface, MID_X-info_text.get_width()/2, 20)
        quit_text = Label("PRESS Q TO QUIT INFO PAGE", 22, bold=True, italic=True)
        quit_text.draw(surface, MID_X-quit_text.get_width()/2, WINDOW_HEIGHT-30)

        draw_p1_info(surface)
        draw_p2_info(surface)

        pygame.display.update()

    surface.fill(BLACK)
    resume_text = Label("BACK TO MAIN MENU...", 30, bold=True, italic=True)
    resume_text.draw(surface, MID_X, MID_Y, True)

    pygame.display.update()
    pygame.time.delay(1000)

# MODE SELECT
def mode_select(surface):
    show = True

    while show:
        surface.fill(BLACK)
        draw_mode_info(surface)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    show = False
                    surface.fill(BLACK)
                    loading_text = Label("STARTING SOLO GAME...", 40, bold=True, italic=True)
                    loading_text.draw(surface, MID_X, MID_Y, True)

                    pygame.display.update()
                    pygame.time.delay(1500)
                    Singleplayer(surface)

                if event.key == pygame.K_2:
                    show = False
                    surface.fill(BLACK)
                    loading_text = Label("STARTING PvP GAME...", 40, bold=True, italic=True)
                    loading_text.draw(surface, MID_X, MID_Y, True)

                    pygame.display.update()
                    pygame.time.delay(1500)
                    PlayerVsPlayer(surface)

                if event.key == pygame.K_3:
                    show = False
                    surface.fill(BLACK)
                    loading_text = Label("STARTING AI GAME...", 40, bold=True, italic=True)
                    loading_text.draw(surface, MID_X, MID_Y, True)

                    pygame.display.update()
                    pygame.time.delay(1500)

                    import AI

                if event.key == pygame.K_q:
                    show = False
                    main_menu()

# ALGORITHM SELECT
def algorithm_select(surface, loading_text, game_mode):
    show = True

    while show:
        surface.fill(BLACK)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    show = False
                    surface.fill(BLACK)
                    loading_text.draw(surface, MID_X, MID_Y, True)

                    pygame.display.update()
                    pygame.time.delay(1500)
                    if game_mode == "PvAI":
                        PlayerVsAI(surface)
                    elif game_mode == "AIvAI":
                        AIVsAI(surface)

                if event.key == pygame.K_2:
                    show = False
                    surface.fill(BLACK)
                    loading_text.draw(surface, MID_X, MID_Y, True)

                    pygame.display.update()
                    pygame.time.delay(1500)
                    if game_mode == "PvAI":
                        PlayerVsAI(surface)
                    elif game_mode == "AIvAI":
                        AIVsAI(surface)

                if event.key == pygame.K_3:
                    show = False
                    surface.fill(BLACK)
                    loading_text.draw(surface, MID_X, MID_Y, True)

                    pygame.display.update()
                    pygame.time.delay(1500)
                    if game_mode == "PvAI":
                        PlayerVsAI(surface)
                    elif game_mode == "AIvAI":
                        AIVsAI(surface)

                if event.key == pygame.K_4:
                    show = False
                    surface.fill(BLACK)
                    loading_text.draw(surface, MID_X, MID_Y, True)

                    pygame.display.update()
                    pygame.time.delay(1500)
                    if game_mode == "PvAI":
                        PlayerVsAI(surface)
                    elif game_mode == "AIvAI":
                        AIVsAI(surface)

                if event.key == pygame.K_5:
                    show = False
                    surface.fill(BLACK)
                    loading_text.draw(surface, MID_X, MID_Y, True)

                    pygame.display.update()
                    pygame.time.delay(1500)
                    if game_mode == "PvAI":
                        PlayerVsAI(surface)
                    elif game_mode == "AIvAI":
                        AIVsAI(surface)

                if event.key == pygame.K_q:
                    show = False
                    mode_select(surface)

# MAIN MENU
background_img = pygame.image.load("bg.jpg")

def main_menu():
    run = True
    
    while run:
        game_window.fill((255, 178, 102))
        game_window.blit(background_img, (0, -70))
        
        label = Label("Thai Minh Bang| Pham Vu Bao Nhan| Tran Nguyen Minh Cuong | Nguyen Tran Khai", 30, bold=True)
        label.draw(game_window, MID_X, MID_Y - 250, True)
        info_text = Label("(PRESS I FOR INFO)", 20, bold=True, italic=True)
        info_text.draw(game_window, MID_X, MID_Y + 310, True)
        start_text = Label("PRESS ANY KEY TO START THE GAME", 40, bold=True, italic=True)
        start_text.draw(game_window, MID_X, MID_Y + 250, True)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    info_page(game_window)
                elif event.key == pygame.K_q:
                    run = False
                    pygame.quit()
                    quit()
                else:
                    mode_select(game_window)
    pygame.display.quit()

game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")
main_menu()
