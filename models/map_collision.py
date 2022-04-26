import math

import pygame

from utils import constants


class Map(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, x, y, rect, game):
        super().__init__()

        self.surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.pos_x = x

        self.game = game
        self.surface.fill(self.game.WHITE)
        self.surface.set_alpha(50)
        self.image = self.surface

    def update(self):
        if self.game.map_can_move:
            self.pos_x -= constants.MAP_MOVEMENT_RATE
            self.rect.x = math.floor(self.pos_x)
