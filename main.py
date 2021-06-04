import pygame
from Square import Square
import time

TICK_SECOND = 50
start = stop = None
main_list = [[Square(x, y) for x in range(1, Square.BOARD_WIDTH, Square.SQUARE_WIDTH + 1)]
             for y in range(1, Square.BOARD_HEIGHT, Square.SQUARE_HEIGHT + 1)]

border_sq = []
display_surface = pygame.display.set_mode((0, 0))
screen = pygame.display.set_mode((Square.BOARD_WIDTH, Square.BOARD_HEIGHT))
pygame.display.set_caption('Board')
clock = pygame.time.Clock()

pygame.init()


def update_sprites():
    global main_list, display_surface
    for line in main_list:
        for sq in line:
            sq.draw(display_surface)
    pygame.display.flip()


def update_single_sprite(sq):
    # more efficient then 'update_sprites'
    sq.draw(display_surface)
    pygame.display.flip()


def find_index(x, y):
    return (x // (Square.SQUARE_WIDTH + 1)), (y // (Square.SQUARE_WIDTH + 1))


def start_game():
    global main_list, start, stop
    finish = False
    drag = False
    button_pressed = 0
    while not finish:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = event.button
            if drag and button_pressed is 1:
                x_pos, y_pos = pygame.mouse.get_pos()
                x_index, y_index = find_index(x_pos, y_pos)
                sq = main_list[y_index][x_index]
                sq.set_sit("Block")
            elif drag and button_pressed is 2:
                x_pos, y_pos = pygame.mouse.get_pos()
                x_index, y_index = find_index(x_pos, y_pos)
                sq = main_list[y_index][x_index]
                if sq.sit is "Edge":
                    start = None
                    # its have to be 'start', if it was 'stop' the program was run already
                sq.set_sit("Null")
            elif event.type == pygame.MOUSEBUTTONDOWN and button_pressed is 3:
                x_pos, y_pos = pygame.mouse.get_pos()
                x_index, y_index = find_index(x_pos, y_pos)
                sq = main_list[y_index][x_index]
                sq.set_sit("Edge")
                if start is None or start.sit is not "Edge":
                    start = sq
                else:
                    stop = sq
                    if not stop == start:
                        finish = True
            drag = event.type == pygame.MOUSEBUTTONDOWN or drag and not event.type == pygame.MOUSEBUTTONUP
        update_sprites()


def update_cost_squares(pos):
    x_pos, y_pos = pos.MAP_INDEX
    x_low = x_pos - 1
    y_low = y_pos - 1
    x_hig = x_pos + 1
    y_hig = y_pos + 1

    if x_low != -1:
        if main_list[y_pos][x_low].addRank(start, stop, border_sq):
            main_list[y_pos][x_low].goto = pos
            update_single_sprite(main_list[y_pos][x_low])

    if x_hig != Square.NUM_OF_SQUARES_WIDTH:
        if main_list[y_pos][x_hig].addRank(start, stop, border_sq):
            main_list[y_pos][x_hig].goto = pos
            update_single_sprite(main_list[y_pos][x_hig])

    if y_low != -1:
        if main_list[y_low][x_pos].addRank(start, stop, border_sq):
            main_list[y_low][x_pos].goto = pos
            update_single_sprite(main_list[y_low][x_pos])

    if y_hig != Square.NUM_OF_SQUARES_HEIGHT:
        if main_list[y_hig][x_pos].addRank(start, stop, border_sq):
            main_list[y_hig][x_pos].goto = pos
            update_single_sprite(main_list[y_hig][x_pos])

    update_single_sprite(pos)

    # we can not move in the slant ( / or \ )


def lowest_score_point():
    if len(border_sq) is 0:
        return None
    sq = min(border_sq)
    border_sq.remove(sq)
    sq.set_sit("Check")
    update_single_sprite(sq)

    return sq  # the square with the lowest rank


def on_finish():
    global start, stop, main_list
    pos = stop
    sum_path = 0
    length_path = 0
    while pos is not start:
        sum_path += pos.rank
        length_path += 1
        pos = pos.goto

        pos.set_sit("Path")
        update_single_sprite(pos)

    x_start, y_start = start.MAP_INDEX
    x_stop, y_stop = stop.MAP_INDEX

    main_list = list(
        map(lambda lst: [sq if sq.sit in ['Edge', 'Block', 'Path'] else sq.set_sit('Null') for sq in lst], main_list))

    update_sprites()

    efficient_length = abs(x_start - x_stop) + abs(y_start - y_stop)
    efficiency = (start.rank * efficient_length) / sum_path
    efficiency *= 100
    # in presents

    print(f'''
finish successfully:
    path efficiency score = {int(1000 * efficiency) / 1000} %
    path length score = {int(1000 * 100 * (efficient_length / length_path)) / 1000} %
    length path = {length_path}
    ''')

    start_again()


def start_again():
    global start, stop, main_list, border_sq
    border_sq = []
    start = stop = None
    main_list = [[Square(x, y) for x in range(1, Square.BOARD_WIDTH, Square.SQUARE_WIDTH + 1)]
                 for y in range(1, Square.BOARD_HEIGHT, Square.SQUARE_HEIGHT + 1)]
    print("click for new map")

    while True:
        # wait to the user interaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                return main()


def on_stuck():
    global start, stop, main_list

    print("there is no way.")
    start_again()


def main():
    global start, stop
    start_game()

    pos = start

    finish = False
    while not finish:
        update_cost_squares(pos)
        pos = lowest_score_point()
        if pos is None or pos == stop:
            finish = True

        #        update_sprites()
        clock.tick(TICK_SECOND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True

    if pos is None:
        on_stuck()
    if pos == stop:
        on_finish()


if __name__ == "__main__":
    print('''
        ========================================
         - right button for start and stop
         - left button for a wall
         - middle button to erase 
        ========================================
    ''')
    main()


pygame.quit()
