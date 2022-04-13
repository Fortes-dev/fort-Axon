import pygame
from utils import constants

# Modelo de la nave pj
class Bullet(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, x, y, type):
        super().__init__()

        # Cargamos la imagen del disparo y la escalamos dependiendo de si es enemigo o spaceship (0 = spaceship, 1 = enemigo)
        self.sprites = []

        self.type = type

        match self.type:
            case (0):
                imagen1 = pygame.transform.rotozoom(pygame.image.load(constants.BULLET1), 0, constants.BULLET_SIZE)
                self.sprites.append(imagen1)

                # Velocidad de la bala
                self.speed = constants.BULLET1_SPEED
            case (1):
                imagen2 = pygame.transform.rotozoom(pygame.image.load(constants.BULLET2), 0, constants.BULLET_SIZE)
                self.sprites.append(imagen2)

                # Velocidad de la bala del enemigo
                self.speed = constants.BULLET2_SPEED

            case (2):
                imagen3 = pygame.transform.rotozoom(pygame.image.load(constants.BULLET_CHARGED_1), 0, constants.BULLET_CHARGED_SIZE)
                self.sprites.append(imagen3)

                self.speed = constants.BULLET1_SPEED


        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # Inicializamos el rectángulo (hitbox)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    # Actualizamos la posicion del disparo
    def update(self):
        match self.type:
            case (0):
                self.rect.x += self.speed
            case (1):
                self.rect.x -= self.speed
            case (2):
                self.rect.x += self.speed