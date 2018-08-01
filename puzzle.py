"""
    Puzzle Game.
    By Wang Hongwei, email:525269029@qq.com
    url: https://github.com/reverie2007/puzzle

"""
import pygame
import sys
import random
from pygame.locals import *

# Create the constants (go ahead and experiment with different values)
BOARDWIDTH = 3  # number of columns in the board
BOARDHEIGHT = 3  # number of rows in the board
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 60
BLANK = 0

#                 R    G    B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

RUNNING = 'running'
SUCCESS = 'success'
START = 'start'

game_status = START
screen = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))


def main():
    global FPSCLOCK, screen, BASICFONT, BIGFONT, game_status, solve_board
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Puzzle Game')

    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    BIGFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE * 2)

    main_board = get_starting_board()
    solve_board = get_starting_board()

    game_status = START

    while True:  # main game loop
        if game_status == START:
            game_start(main_board)
        elif game_status == RUNNING:
            game_running(main_board)
        elif game_status == SUCCESS:
            game_success(main_board)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def game_start(main_board):
    global game_status, screen

    screen.fill(BGCOLOR)
    tile = "Puzzle  Game!!!"
    tile_surf, tile_rect = make_text(tile, 0, 0, BIGFONT)
    tile_rect.center = (WINDOWWIDTH/2, 50)
    screen.blit(tile_surf, tile_rect)
    hint = "Press Space or F9 To Start!"
    hint_surf, hint_rect = make_text(hint, 0, 0, BASICFONT)
    hint_rect.center = (WINDOWWIDTH/2, 420)
    screen.blit(hint_surf, hint_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key in (K_SPACE, K_F9):
                generate_newpuzzle(main_board)
                game_status = RUNNING


def game_running(main_board):
    global game_status

    slide_to = None  # the direction, if any, a tile should slide
    msg = 'Click tile or press arrow keys to slide.'  # contains the message to show in the upper left corner.
    if main_board == solve_board:
        game_status = SUCCESS
        return

    draw_board(main_board, msg)

    for event in pygame.event.get():  # event handling loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            # check if the user pressed a key to slide a tile
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key in (K_LEFT, K_a) and is_valid_move(main_board, LEFT):
                slide_to = LEFT
            elif event.key in (K_RIGHT, K_d) and is_valid_move(main_board, RIGHT):
                slide_to = RIGHT
            elif event.key in (K_UP, K_w) and is_valid_move(main_board, UP):
                slide_to = UP
            elif event.key in (K_DOWN, K_s) and is_valid_move(main_board, DOWN):
                slide_to = DOWN

    if slide_to:
        # slideAnimation(main_board, slide_to, 'Click tile or press arrow keys to slide.', 8) # show slide on screen
        make_move(main_board, slide_to)
        # allMoves.append(slide_to) # record the slide


def game_success(main_board):
    global game_status, screen

    screen.fill(BGCOLOR)
    draw_board(main_board, "")
    tile = "Congratulations! You Win!"
    tile_surf, tile_rect = make_text(tile, 70, 50, BIGFONT)
    # 想让文本居中直接设置中心点
    tile_rect.center = (WINDOWWIDTH/2, 50)
    screen.blit(tile_surf, tile_rect)
    hint = "Press F9 To Restart! Press F10 to Start Menu!"
    hint_surf, hint_rect = make_text(hint, 100, 400, BASICFONT)
    screen.blit(hint_surf, hint_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key in (K_F10,):
                game_status = START
            elif event.key in (K_F9, K_SPACE):
                generate_newpuzzle(main_board)
                game_status = RUNNING


def make_text(text, top, left, font, msg_color=MESSAGECOLOR, bgcolor=BGCOLOR):
    # create the Surface and Rect objects for some text.
    text_surf = font.render(text, True, msg_color, bgcolor)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return text_surf, text_rect


def xy_to_num(tile_x, tile_y):
    return tile_y * BOARDWIDTH + tile_x


def num_to_xy(num):
    return num % BOARDWIDTH, num // BOARDWIDTH


def get_blank_position(board):
    # Return the x and y of board coordinates of the blank space.
    for num in range(BOARDWIDTH * BOARDHEIGHT):
        if board[num] == BLANK:
            return num_to_xy(num)


def make_move(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = get_blank_position(board)

    if move == UP:
        board[xy_to_num(blankx, blanky)], board[xy_to_num(blankx, blanky + 1)] = \
            board[xy_to_num(blankx, blanky + 1)], board[xy_to_num(blankx, blanky)]
    elif move == DOWN:
        board[xy_to_num(blankx, blanky)], board[xy_to_num(blankx, blanky - 1)] = \
            board[xy_to_num(blankx, blanky - 1)], board[xy_to_num(blankx, blanky)]
    elif move == LEFT:
        board[xy_to_num(blankx, blanky)], board[xy_to_num(blankx + 1, blanky)] = \
            board[xy_to_num(blankx + 1, blanky)], board[xy_to_num(blankx, blanky)]
    elif move == RIGHT:
        board[xy_to_num(blankx, blanky)], board[xy_to_num(blankx - 1, blanky)] = \
            board[xy_to_num(blankx - 1, blanky)], board[xy_to_num(blankx, blanky)]


def is_valid_move(board, move):
    blankx, blanky = get_blank_position(board)
    return (move == UP and blanky != BOARDHEIGHT - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != BOARDWIDTH - 1) or \
           (move == RIGHT and blankx != 0)


def get_left_top_of_tile(tile_x, tile_y):
    left = XMARGIN + (tile_x * TILESIZE) + (tile_x - 1)
    top = YMARGIN + (tile_y * TILESIZE) + (tile_y - 1)
    return left, top


def draw_tile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = get_left_top_of_tile(tilex, tiley)
    pygame.draw.rect(screen, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    text_surf = BASICFONT.render(str(number), True, TEXTCOLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    screen.blit(text_surf, text_rect)


def draw_board(board, message):
    screen.fill(BGCOLOR)
    if message:
        pass

    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            if board[xy_to_num(tilex, tiley)]:
                draw_tile(tilex, tiley, board[xy_to_num(tilex, tiley)])

    left, top = get_left_top_of_tile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(screen, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)


def swap_board(board):
    """
    交换两个相邻的数字
    :param board:
    :return:
    """
    if board[0] == BLANK:
        board[1], board[2] = board[2], board[1]
    elif board[1] == BLANK:
        board[2], board[3] = board[3], board[2]
    else:
        board[0], board[1] = board[1], board[0]

    return board


def generate_newpuzzle(board):
    """
    build a new puzzle. First put random numbers in a list, check the list, if right, return the list.
    if wrong, swap two items which don't zero.
    :return: list
    """
    random.shuffle(board)
    '''
        有解的判断
        
    '''
    inversions = 0
    for i in range(len(board)):
        if board[i] == BLANK:
            continue
        else:
            for j in range(i + 1, len(board)):
                if board[j] == BLANK:
                    continue
                else:
                    if board[i] > board[j]:
                        inversions += 1

    if BOARDWIDTH % 2 == 1:
        if inversions % 2 == 0:
            return board
        else:
            return swap_board(board)
    else:
        x, y = get_blank_position(board)
        bottom_y = BOARDHEIGHT - y
        if bottom_y % 2 == 1:
            if inversions % 2 == 0:
                return board
            else:
                return swap_board(board)
        else:
            if inversions % 2 == 1:
                return board
            else:
                return swap_board(board)
    # return board


def get_starting_board():
    """
    create the result puzzle.
    :return: list
    """
    board = [i for i in range(1, BOARDWIDTH * BOARDHEIGHT + 1)]
    board[BOARDWIDTH * BOARDHEIGHT - 1] = BLANK  # the lask is blank
    return board


if __name__ == '__main__':
    main()
