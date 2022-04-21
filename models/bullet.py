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
            case ('player1_shot'):
                imagen1 = pygame.transform.rotozoom(pygame.image.load(constants.BULLET1), 0, constants.BULLET_SIZE)
                self.sprites.append(imagen1)

                # Velocidad de la bala
                self.speed = constants.BULLET_PLAYER_SPEED
            case ('player2_shot'):
                imagen2 = pygame.transform.rotozoom(pygame.image.load(constants.BULLET2), 0, constants.BULLET_SIZE)
                self.sprites.append(imagen2)

                # Velocidad de la bala del enemigo
                self.speed = constants.BULLET_PLAYER_SPEED

            case ('player1_chargedshot'):
                imagen3 = pygame.transform.rotozoom(pygame.image.load(constants.BULLET_CHARGED_1), 0, constants.BULLET_CHARGED_SIZE)
                self.sprites.append(imagen3)

                self.speed = constants.BULLET_PLAYER_SPEED

            case ('player2_chargedshot'):
                imagen4 = pygame.transform.rotozoom(pygame.image.load(constants.BULLET_CHARGED_2), 0,
                                                    constants.BULLET_CHARGED_SIZE)
                self.sprites.append(imagen4)

                self.speed = constants.BULLET_PLAYER_SPEED

            case ('enemy_shot'):
                imagen2 = pygame.transform.rotozoom(pygame.image.load(constants.BULLET_ENEMY), 0, constants.BULLET_SIZE)
                self.sprites.append(imagen2)

                # Velocidad de la bala del enemigo
                self.speed = constants.BULLET_ENEMY_SPEED


        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # Inicializamos el rectángulo (hitbox)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    # Actualizamos la posicion del disparo
    def update(self):
            if self.type == 'player1_shot' or self.type ==  'player2_shot' or self.type == 'player1_chargedshot' or self.type == 'player2_chargedshot':
                self.rect.x += self.speed
            elif self.type == 'enemy_shot':
                self.rect.x -= self.speed
