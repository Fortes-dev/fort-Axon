# Modelo de la nave pj
import pygame

from utils import constants


class Bonus(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, x, y, type):
        super().__init__()

        # Posiciones iniciales
        self.pos_x = x
        self.pos_y = y

        self.type = type

        self.speed = constants.BONUS_SPEED

        self.sprites = []

        match self.type:
            case ('speed'):
                imagen = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_SPEED_INCREASE), 0, constants.BONUS_ZOOM)
                self.sprites.append(imagen)

            case ('bullet'):
                imagen = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_BULLET), 0, constants.BONUS_ZOOM)
                self.sprites.append(imagen)


        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # Inicializamos el rectángulo (hitbox)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    # Actualizamos la posicion del bonus
    def update(self):
            self.rect.x -= self.speed
