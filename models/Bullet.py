import pygame
from utils import constants

# Modelo de la nave pj
class Bullet(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, x, y):
        super().__init__()

        # Posiciones iniciales
        self.pos_x = x
        self.pos_y = y

        # Cargamos la imagen del disparo y la escalamos
        imagen = pygame.image.load(constants.BULLET1)
        imagen = pygame.transform.rotozoom(imagen, 0, 2)

        self.sprites = []
        self.sprites.append(imagen)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # Inicializamos el rectángulo (hitbox)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Velocidad de desplacamiento de la nave
        self.speed = constants.BULLET1_SPEED


    # Actualizamos la posicion del disparo
    def update(self):
        self.rect.x += self.speed







