# Eyal

import pygame
from math import sqrt


class Square:
    SQUARE_WIDTH = SQUARE_HEIGHT = 20
    BOARD_WIDTH = BOARD_HEIGHT = 700

    NUM_OF_SQUARES_WIDTH = (BOARD_WIDTH // SQUARE_WIDTH) - 1
    NUM_OF_SQUARES_HEIGHT = (BOARD_HEIGHT // SQUARE_HEIGHT) - 1

    BOARD_WIDTH = NUM_OF_SQUARES_WIDTH * (SQUARE_WIDTH + 1)
    BOARD_HEIGHT = NUM_OF_SQUARES_HEIGHT * (SQUARE_HEIGHT + 1)

    how_many_created = 0

    def __init__(self, x, y):  # the (x, y) is the top left corner [* ]
        Square.how_many_created += 1

        self.rank = None
        self.isRanked = False

        self.MAP_INDEX = x // (Square.SQUARE_WIDTH + 1), y // (Square.SQUARE_HEIGHT + 1)
        if sum(self.MAP_INDEX) % 2:
            self.color = (255, 255, 255)

        else:
            self.color = (200, 191, 231)

        self.rect = pygame.Rect(x, y, Square.SQUARE_WIDTH, Square.SQUARE_HEIGHT)

        self.rect.x = x
        self.rect.y = y
        self.sit = 'Null'
        self.image = pygame.Surface((Square.SQUARE_WIDTH - 1, Square.SQUARE_HEIGHT - 1))
        self.image.fill(self.color)
        self.goto = None

    def set_sit(self, new_sit):
        if new_sit is 'Block':
            self.sit = new_sit
            self.color = (128, 0, 128)
            self.image.fill(self.color)
        elif new_sit is 'Path':
            self.sit = new_sit
            self.color = (0, 0, 0)
            self.image.fill(self.color)
        elif new_sit is 'Edge':
            self.sit = new_sit
            self.color = (21, 169, 176)
            self.image.fill(self.color)
        elif new_sit is 'Null':
            self.sit = new_sit
            if sum(self.MAP_INDEX) % 2:
                self.color = (255, 255, 255)
            else:
                self.color = (200, 191, 231)
            self.image.fill(self.color)
        elif new_sit is 'Check':

            self.sit = new_sit
            self.color = (215, 147, 6)
            self.image.fill(self.color)
        elif new_sit is 'Border':
            self.sit = new_sit
            self.color = (128, 106, 200)
            self.image.fill(self.color)
        else:
            raise Exception('SIT_ERROR')
        return self

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, Square.SQUARE_WIDTH, Square.SQUARE_HEIGHT))

    def add_rank(self, start, end, border_sq):
        if self.isRanked or self.sit is "Block" :
            return False
        self.set_sit("Border")
        border_sq.append(self)
        g_cost = self.distance(start)
        h_cost = self.distance(end)
        f_cost = g_cost + h_cost
        self.rank = f_cost
        self.isRanked = True
        return True

    def distance(self, a):
        return sqrt(
            ((self.MAP_INDEX[0] - a.MAP_INDEX[0]) ** 2)
            + ((self.MAP_INDEX[1] - a.MAP_INDEX[1]) ** 2))

    def __gt__(self, sq):
        if not sq.isRanked or not self.isRanked:
            raise Exception("RANK_ERROR")

        return self.rank > sq.rank

    def __eq__(self, sq):
        return self.rect.x == sq.rect.x and self.rect.y == sq.rect.y
