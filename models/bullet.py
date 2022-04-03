import pygame
from utils import constants

# Modelo de la nave pj
class Bullet(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, x, y, type):
        super().__init__()

        # Posiciones iniciales
        self.pos_x = x
        self.pos_y = y

        # Cargamos la imagen del disparo y la escalamos dependiendo de si es enemigo o spaceship (0 = spaceship, 1 = enemigo)
        self.sprites = []
        match type:
            case (0):
                imagen1 = pygame.image.load(constants.BULLET1)
                imagen1 = pygame.transform.rotozoom(imagen1, 0, 1.7)
                self.sprites.append(imagen1)

                # Velocidad de la bala
                self.speed = constants.BULLET1_SPEED
            case (1):
                imagen2 = pygame.image.load(constants.BULLET2)
                imagen2 = pygame.transform.rotozoom(imagen2, -180, 1.7)
                self.sprites.append(imagen2)

                # Velocidad de la bala
                self.speed = constants.BULLET2_SPEED


        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # Inicializamos el rectángulo (hitbox)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    # Actualizamos la posicion del disparo
    def update(self, type):
        match type:
            case (0):
                self.rect.x += self.speed
            case (1):
                self.rect.x -= self.speed