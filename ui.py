from sprite import *

# GAMEPLAY DRAW FUNCTIONS
def draw_grid(surface, grid_1, grid_2=None, add=0, single_mode=False):
    if single_mode:
        for i in range(len(grid_1)):
            pygame.draw.line(surface, DARK_GREY, (TOP_LEFT_X_SINGLE, TOP_LEFT_Y + i*BLOCK_SIZE), (TOP_LEFT_X_SINGLE + GAME_WIDTH, TOP_LEFT_Y + i*BLOCK_SIZE))
            for j in range(len(grid_1[i])):
                pygame.draw.line(surface, DARK_GREY, (TOP_LEFT_X_SINGLE + j*BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X_SINGLE + j*BLOCK_SIZE, TOP_LEFT_Y + GAME_HEIGHT))
    else:
        for i in range(len(grid_1)):
            pygame.draw.line(surface, DARK_GREY, (TOP_LEFT_X, TOP_LEFT_Y + i*BLOCK_SIZE), (TOP_LEFT_X + GAME_WIDTH, TOP_LEFT_Y + i*BLOCK_SIZE))
            for j in range(len(grid_1[i])):
                pygame.draw.line(surface, DARK_GREY, (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + GAME_HEIGHT))
        for i in range(len(grid_2)):
            pygame.draw.line(surface, DARK_GREY, (TOP_LEFT_X + add, TOP_LEFT_Y + i*BLOCK_SIZE), (TOP_LEFT_X + add + GAME_WIDTH, TOP_LEFT_Y + i*BLOCK_SIZE))
            for j in range(len(grid_2[i])):
                pygame.draw.line(surface, DARK_GREY, (TOP_LEFT_X + add + j*BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + add + j*BLOCK_SIZE, TOP_LEFT_Y + GAME_HEIGHT))

def draw_window(surface, grid_1, grid_2=None, score_1=0, score_2=0, level=1, speed=0.27, add=0, single_mode=False, num_of_AI=0):
    surface.fill(BLACK)
    if single_mode:
        status_text = Label("LEVEL:"+str(level)+"   SPEED:"+str(round(1/speed,2)), 20, italic=True)
        status_text.draw(surface, (TOP_LEFT_X_SINGLE+GAME_WIDTH)/1.5-status_text.get_width(), 30)

        for i in range(len(grid_1)):
            for j in range(len(grid_1[i])):
                pygame.draw.rect(surface, grid_1[i][j], (TOP_LEFT_X_SINGLE+j*BLOCK_SIZE, TOP_LEFT_Y+i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        pygame.draw.rect(surface, RED, (TOP_LEFT_X_SINGLE, TOP_LEFT_Y, GAME_WIDTH, GAME_HEIGHT), 4)

        x_pos = TOP_LEFT_X_SINGLE + GAME_WIDTH + 50
        y_pos = TOP_LEFT_Y + GAME_HEIGHT/2 - 100
        p_score_text = Label("Score:"+str(score_1), 20, italic=True)
        p_score_text.draw(surface, x_pos+10, y_pos-120)

        draw_grid(surface, grid_1, single_mode=True)
    else:
        status_text = Label("LEVEL:"+str(level)+"   SPEED:"+str(round(1/speed,2)), 20, italic=True)
        status_text.draw(surface, (TOP_LEFT_X+GAME_WIDTH)/1.5-status_text.get_width(), 30)
        status_text.draw(surface, (TOP_LEFT_X+GAME_WIDTH)/1.5-status_text.get_width()+add, 30)

        for i in range(len(grid_1)):
            for j in range(len(grid_1[i])):
                pygame.draw.rect(surface, grid_1[i][j], (TOP_LEFT_X+j*BLOCK_SIZE, TOP_LEFT_Y+i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        for i in range(len(grid_2)):
            for j in range(len(grid_2[i])):
                pygame.draw.rect(surface, grid_2[i][j], (TOP_LEFT_X+add+j*BLOCK_SIZE, TOP_LEFT_Y+i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, GAME_WIDTH, GAME_HEIGHT), 4)
        pygame.draw.rect(surface, RED, (TOP_LEFT_X+add, TOP_LEFT_Y, GAME_WIDTH, GAME_HEIGHT), 4)

        x_pos = TOP_LEFT_X + GAME_WIDTH + 50
        y_pos = TOP_LEFT_Y + GAME_HEIGHT/2 - 100
        p1_score_text = Label("Score:"+str(score_1), 20, italic=True)
        p2_score_text = Label("Score:"+str(score_2), 20, italic=True)

        p1_score_text.draw(surface, x_pos+10, y_pos-120)
        p2_score_text.draw(surface, x_pos+add+10, y_pos-120)

        pygame.draw.line(surface, WHITE, (WINDOW_WIDTH/2, 0), (WINDOW_WIDTH/2, WINDOW_HEIGHT))
        draw_grid(surface, grid_1, grid_2, add=int(MID_X))
    pygame.display.flip()

def draw_next_shape(surface, shape_1, shape_2=None, add=0, single_mode=False):
    label = Label("NEXT SHAPE:", 20, bold=True)
    if single_mode:
        x_pos = TOP_LEFT_X_SINGLE + GAME_WIDTH + 50
        y_pos = TOP_LEFT_Y + GAME_HEIGHT/2 - 100
        format = shape_1.shape[shape_1.rotation % (len(shape_1.shape))]

        for i, row in enumerate(format):
            for j, col in enumerate(row):
                if col == "0":
                    pygame.draw.rect(surface, shape_1.color, (x_pos+j*BLOCK_SIZE, y_pos+i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(surface, DARK_GREY, (x_pos+j*BLOCK_SIZE, y_pos+i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        label.draw(surface, x_pos+10, y_pos-30)
    else:
        x_pos = TOP_LEFT_X + GAME_WIDTH + 50
        y_pos = TOP_LEFT_Y + GAME_HEIGHT/2 - 100
        format_1 = shape_1.shape[shape_1.rotation % (len(shape_1.shape))]
        format_2 = shape_2.shape[shape_2.rotation % (len(shape_2.shape))]

        for i, row in enumerate(format_1):
            for j, col in enumerate(row):
                if col == "0":
                    pygame.draw.rect(surface, shape_1.color, (x_pos+j*BLOCK_SIZE, y_pos+i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(surface, DARK_GREY, (x_pos+j*BLOCK_SIZE, y_pos+i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        for i, row in enumerate(format_2):
            for j, col in enumerate(row):
                if col == "0":
                    pygame.draw.rect(surface, shape_2.color, (x_pos+add+j*BLOCK_SIZE, y_pos+i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(surface, DARK_GREY, (x_pos+add+j*BLOCK_SIZE, y_pos+i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        label.draw(surface, x_pos+10, y_pos-30)
        label.draw(surface, x_pos+add+10, y_pos-30)
    pygame.display.update()

# INFO SCREEN
def draw_p1_info(surface):
    p1_header_text = Label("PLAYER 1", 50, bold=True, italic=True)
    p1_info_text_1 = Label("    W - ROTATE    ", 50, bold=True, italic=True)
    p1_info_text_2 = Label("    A - MOVE LEFT ", 50, bold=True, italic=True)
    p1_info_text_3 = Label("    S - MOVE DOWN ", 50, bold=True, italic=True)
    p1_info_text_4 = Label("    D - MOVE RIGHT", 50, bold=True, italic=True)
    p1_info_text_5 = Label("SPACE - PAUSE     ", 50, bold=True, italic=True)

    p1_header_text.draw(surface, MID_X/2-p1_header_text.get_width()/2, MID_Y/2)
    p1_info_text_1.draw(surface, MID_X/2-p1_info_text_1.get_width()/2-p1_info_text_1.get_width()/32, MID_Y/2+p1_info_text_1.get_height()*2)
    p1_info_text_2.draw(surface, MID_X/2-p1_info_text_2.get_width()/2-p1_info_text_2.get_width()/32, MID_Y/2+p1_info_text_2.get_height()*3.5)
    p1_info_text_3.draw(surface, MID_X/2-p1_info_text_3.get_width()/2-p1_info_text_3.get_width()/32, MID_Y/2+p1_info_text_3.get_height()*5)
    p1_info_text_4.draw(surface, MID_X/2-p1_info_text_4.get_width()/2-p1_info_text_4.get_width()/32, MID_Y/2+p1_info_text_4.get_height()*6.5)
    p1_info_text_5.draw(surface, MID_X/2-p1_info_text_5.get_width()/2-p1_info_text_5.get_width()/32, MID_Y/2+p1_info_text_5.get_height()*8)
    pygame.draw.line(surface, WHITE, (MID_X/2-p1_header_text.get_width()/2, MID_Y-100), (MID_X/1.5, MID_Y-100))

def draw_p2_info(surface):
    p2_header_text = Label("PLAYER 2", 50, bold=True, italic=True)
    p2_info_text_1 = Label("   UP - ROTATE    ", 50, bold=True, italic=True)
    p2_info_text_2 = Label(" LEFT - MOVE LEFT ", 50, bold=True, italic=True)
    p2_info_text_3 = Label(" DOWN - MOVE DOWN ", 50, bold=True, italic=True)
    p2_info_text_4 = Label("RIGHT - MOVE RIGHT", 50, bold=True, italic=True)
    p2_info_text_5 = Label("SPACE - PAUSE     ", 50, bold=True, italic=True)

    p2_header_text.draw(surface, MID_X/2-p2_header_text.get_width()/2+MID_X-50, MID_Y/2)
    p2_info_text_1.draw(surface, MID_X/2-p2_info_text_1.get_width()/2-p2_info_text_1.get_width()/32+MID_X, MID_Y/2+p2_info_text_1.get_height()*2)
    p2_info_text_2.draw(surface, MID_X/2-p2_info_text_2.get_width()/2-p2_info_text_2.get_width()/32+MID_X, MID_Y/2+p2_info_text_2.get_height()*3.5)
    p2_info_text_3.draw(surface, MID_X/2-p2_info_text_3.get_width()/2-p2_info_text_3.get_width()/32+MID_X, MID_Y/2+p2_info_text_3.get_height()*5)
    p2_info_text_4.draw(surface, MID_X/2-p2_info_text_4.get_width()/2-p2_info_text_4.get_width()/32+MID_X, MID_Y/2+p2_info_text_4.get_height()*6.5)
    p2_info_text_5.draw(surface, MID_X/2-p2_info_text_5.get_width()/2-p2_info_text_5.get_width()/32+MID_X, MID_Y/2+p2_info_text_5.get_height()*8)
    pygame.draw.line(surface, WHITE, (MID_X/2-p2_header_text.get_width()/2+MID_X-50, MID_Y-100), (MID_X/1.5+MID_X-50, MID_Y-100))

# MODE SELECT
def draw_mode_info(surface):
    mode_header = Label("Select a mode", 40, bold=True, italic=True)
    mode_single = Label("1. Singleplayer    ", 32, bold=True)
    mode_PvP    = Label("2. Player vs Player", 32, bold=True)
    mode_AI     = Label("3. AI              ", 32, bold=True)

    mode_header.draw(surface, MID_X-mode_header.get_width()/2, MID_Y/2)
    mode_single.draw(surface, MID_X-mode_single.get_width()/2, MID_Y/2+mode_single.get_height()*2)
    mode_PvP.draw(surface, MID_X-mode_PvP.get_width()/2, MID_Y/2+mode_PvP.get_height()*3.5)
    mode_AI.draw(surface, MID_X-mode_AI.get_width()/2, MID_Y/2+mode_AI.get_height()*5)

# ALGORITHM SELECT
