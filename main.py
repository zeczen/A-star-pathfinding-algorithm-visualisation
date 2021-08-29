# Eyal

from os import devnull
import sys
from Square import Square

sys.stdout = open(devnull, 'w')


TICK_SECOND = 500
start = stop = None
main_list = [[Square(x, y) for x in range(1, Square.BOARD_WIDTH, Square.SQUARE_WIDTH + 1)]
             for y in range(1, Square.BOARD_HEIGHT, Square.SQUARE_HEIGHT + 1)]

border_sq = []

import pygame
display_surface = pygame.display.set_mode((0, 0))
screen = pygame.display.set_mode((Square.BOARD_WIDTH, Square.BOARD_HEIGHT))
pygame.display.set_caption('Board')
clock = pygame.time.Clock()

pygame.init()
sys.stdout = sys.__stdout__


def update_sprites():
    global main_list, display_surface
    for line in main_list:
        for sq in line:
            sq.draw(display_surface)
    pygame.display.flip()


def update_single_sprite(sq):
    # more efficient then 'update_sprites'
    # because we are updating the square that has changed instead of updating them all
    sq.draw(display_surface)
    pygame.display.flip()


def find_index(x, y):
    return (x // (Square.SQUARE_WIDTH + 1)), (y // (Square.SQUARE_WIDTH + 1))


def initial_game():
    global main_list, start, stop
    finish = False
    drag = False
    button_pressed = 0
    while not finish:

        for event in pygame.event.get():
            sq = None

            if event.type == pygame.QUIT:
                raise Exception()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = event.button
            if drag and button_pressed == 1:
                x_pos, y_pos = pygame.mouse.get_pos()
                x_index, y_index = find_index(x_pos, y_pos)
                sq = main_list[y_index][x_index]
                sq.set_sit("Block")
            elif drag and button_pressed == 2:
                x_pos, y_pos = pygame.mouse.get_pos()
                x_index, y_index = find_index(x_pos, y_pos)
                sq = main_list[y_index][x_index]
                if sq.sit == "Edge":
                    start = None
                    # its have to be 'start', if it was 'stop' the program was run already
                sq.set_sit("Null")
            elif event.type == pygame.MOUSEBUTTONDOWN and button_pressed == 3:
                x_pos, y_pos = pygame.mouse.get_pos()
                x_index, y_index = find_index(x_pos, y_pos)
                sq = main_list[y_index][x_index]
                sq.set_sit("Edge")
                if start is None or not start.sit == "Edge":
                    start = sq
                else:
                    stop = sq
                    if not stop == start:
                        finish = True
            drag = event.type == pygame.MOUSEBUTTONDOWN or drag and not event.type == pygame.MOUSEBUTTONUP

            if sq is not None:  update_single_sprite(sq)


def update_cost_squares(pos):
    x_pos, y_pos = pos.MAP_INDEX
    x_low = x_pos - 1
    y_low = y_pos - 1
    x_hig = x_pos + 1
    y_hig = y_pos + 1

    if x_low != -1:
        if main_list[y_pos][x_low].add_rank(start, stop, border_sq):
            main_list[y_pos][x_low].goto = pos
            update_single_sprite(main_list[y_pos][x_low])

    if x_hig != Square.NUM_OF_SQUARES_WIDTH:
        if main_list[y_pos][x_hig].add_rank(start, stop, border_sq):
            main_list[y_pos][x_hig].goto = pos
            update_single_sprite(main_list[y_pos][x_hig])

    if y_low != -1:
        if main_list[y_low][x_pos].add_rank(start, stop, border_sq):
            main_list[y_low][x_pos].goto = pos
            update_single_sprite(main_list[y_low][x_pos])

    if y_hig != Square.NUM_OF_SQUARES_HEIGHT:
        if main_list[y_hig][x_pos].add_rank(start, stop, border_sq):
            main_list[y_hig][x_pos].goto = pos
            update_single_sprite(main_list[y_hig][x_pos])

    update_single_sprite(pos)

    # we can not move in the slant ( / or \ )


def lowest_score_point():
    if len(border_sq) == 0:
        return None
    sq = min(border_sq)
    border_sq.remove(sq)
    sq.set_sit("Check")
    update_single_sprite(sq)

    return sq  # the square with the lowest rank


def stats(length_path, sum_path, distance):
    efficiency = (start.rank * distance) / sum_path
    # the lowest possible ranking divides the actual ranking

    length_score = distance / length_path
    # the shortest route (without block) divided by the current path

    efficiency *= 100
    length_score *= 100
    # in presents

    efficiency = int(1000 * efficiency) / 1000
    length_score = int(1000 * length_score) / 1000
    # show 3 digit after the point

    print(
        f'''
        finish successfully:
            path efficiency score = {efficiency} %
            path length score = {length_score} %
            length path = {length_path}
            '''
    )


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
    start.set_sit('Edge')
    stop.set_sit('Edge')
    update_sprites()
    # to show the path on the map

    distance = abs(x_start - x_stop) + abs(y_start - y_stop)
    # this is the distance in a straight trajectory, without diagonals

    start.add_rank(start, stop, border_sq)

    stats(length_path, sum_path, distance)

    return


def on_stuck():
    print("\tthere is no way.")


def the_game():
    global start, stop

    pos = start
    run = True

    while True:
        if run:
            update_cost_squares(pos)
            pos = lowest_score_point()
            if pos is None or pos == stop:
                break
            if pos == start:
                pos.set_sit('Edge')

            clock.tick(TICK_SECOND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Exception()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = not run

    if pos is None:
        return on_stuck()
    if pos == stop:
        return on_finish()
        # if we finish successfully


def main():
    global start, stop, main_list, border_sq
    print(
        '''
        ========================================
         - Right button for start and end
         - Left button to create a block / start new map / stop and continue running
         - Middle button to erase 
        ========================================
    '''
    )
    update_sprites()
    initial_game()
    the_game()
    # the first game

    while True:
        # wait to the user interaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Exception()

            if event.type == pygame.MOUSEBUTTONDOWN:
                border_sq.clear()
                start = stop = None
                main_list = [[Square(x, y) for x in range(1, Square.BOARD_WIDTH, Square.SQUARE_WIDTH + 1)]
                             for y in range(1, Square.BOARD_HEIGHT, Square.SQUARE_HEIGHT + 1)]
                # initialize properties for a new game

                update_sprites()
                initial_game()
                the_game()


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
        quit()

