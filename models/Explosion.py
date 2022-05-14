import pygame

from utils import constants


class Explosion(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, x, y, zoom):
        super().__init__()

        # Cargamos las imagenes del Spaceship y la escalamos
        imagen1 = pygame.image.load(constants.EXPLOSION1).convert_alpha()
        imagen2 = pygame.image.load(constants.EXPLOSION2).convert_alpha()
        imagen3 = pygame.image.load(constants.EXPLOSION3).convert_alpha()
        imagen4 = pygame.image.load(constants.EXPLOSION4).convert_alpha()
        imagen5 = pygame.image.load(constants.EXPLOSION5).convert_alpha()

        i1 = pygame.transform.rotozoom(imagen1, 0, zoom)


        i2 = pygame.transform.rotozoom(imagen2, 0, zoom)


        i3 = pygame.transform.rotozoom(imagen3, 0, zoom)


        i4 = pygame.transform.rotozoom(imagen4, 0, zoom)


        i5 = pygame.transform.rotozoom(imagen5, 0, zoom)


        # Inicializamos array de sprites y añadimos todos
        self.sprites = []
        self.sprites.append(i1)
        self.sprites.append(i2)
        self.sprites.append(i3)
        self.sprites.append(i4)
        self.sprites.append(i5)

        self.current_sprite = 0

        # Seteamos la imagen actual del sprite
        self.image = self.sprites[self.current_sprite]

        # Inicializamos el rectángulo (hitbox)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if(self.current_sprite <= 4):
            self.image = self.sprites[self.current_sprite]
        else:
            self.kill()
