# Modelo de la nave pj
import pygame

from utils import constants


class Bonus(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, x, y, type):
        super().__init__()

        self.type = type

        self.speed = constants.BONUS_SPEED

        self.sprites = []

        match self.type:
            case ('speed'):
                imagen = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_SPEED_INCREASE_0), 0,
                                                   constants.BONUS_ZOOM)
                imagen1 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_SPEED_INCREASE_1), 0,
                                                    constants.BONUS_ZOOM)
                imagen2 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_SPEED_INCREASE_2), 0,
                                                    constants.BONUS_ZOOM)
                imagen3 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_SPEED_INCREASE_3), 0,
                                                    constants.BONUS_ZOOM)
                imagen4 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_SPEED_INCREASE_4), 0,
                                                    constants.BONUS_ZOOM)
                self.sprites.append(imagen)
                self.sprites.append(imagen1)
                self.sprites.append(imagen2)
                self.sprites.append(imagen3)
                self.sprites.append(imagen4)

            case ('bullet'):
                imagen = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_CHARGED_SHOT_0), 0,
                                                   constants.BONUS_ZOOM)
                imagen1 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_CHARGED_SHOT_1), 0,
                                                    constants.BONUS_ZOOM)
                imagen2 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_CHARGED_SHOT_2), 0,
                                                    constants.BONUS_ZOOM)
                imagen3 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_CHARGED_SHOT_3), 0,
                                                    constants.BONUS_ZOOM)
                imagen4 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_CHARGED_SHOT_4), 0,
                                                    constants.BONUS_ZOOM)
                self.sprites.append(imagen)
                self.sprites.append(imagen1)
                self.sprites.append(imagen2)
                self.sprites.append(imagen3)
                self.sprites.append(imagen4)

            case ('firerate'):
                imagen = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_FIRE_RATE_0), 0,
                                                   constants.BONUS_ZOOM)
                imagen1 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_FIRE_RATE_1), 0,
                                                    constants.BONUS_ZOOM)
                imagen2 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_FIRE_RATE_2), 0,
                                                    constants.BONUS_ZOOM)
                imagen3 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_FIRE_RATE_3), 0,
                                                    constants.BONUS_ZOOM)
                imagen4 = pygame.transform.rotozoom(pygame.image.load(constants.BONUS_FIRE_RATE_4), 0,
                                                    constants.BONUS_ZOOM)
                self.sprites.append(imagen)
                self.sprites.append(imagen1)
                self.sprites.append(imagen2)
                self.sprites.append(imagen3)
                self.sprites.append(imagen4)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # Inicializamos el rectángulo (hitbox)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # Actualizamos la posicion del bonus
    def update(self):
        self.rect.x -= self.speed
        if (self.current_sprite > 4):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
