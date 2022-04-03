

import pygame
import math
import random
from models.bullet import Bullet
from utils import constants


# Modelo de la nave pj
class Enemy(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, x, y):
        super().__init__()

        # Cargamos las imagenes del Spaceship y la escalamos
        imagen1 = pygame.image.load(constants.ENEMY1)
        imagen2 = pygame.image.load(constants.ENEMY2)
        imagen3 = pygame.image.load(constants.ENEMY3)

        i1 = pygame.transform.rotozoom(imagen1, 0, 1.5)
        i2 = pygame.transform.rotozoom(imagen2, 0, 1.5)
        i3 = pygame.transform.rotozoom(imagen3, 0, 1.5)

        # Inicializamos array de sprites y añadimos todos
        self.sprites = []
        self.sprites.append(i1)
        self.sprites.append(i2)
        self.sprites.append(i3)

        self.current_sprite = 0

        # Seteamos la imagen actual del sprite
        self.image = self.sprites[self.current_sprite]

        # Inicializamos el rectángulo (hitbox)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Velocidad de desplacamiento de la nave
        self.speed = constants.ENEMY_SPEED

        # Cadencia de disparo
        self.fire_rate = constants.ENEMY_FIRE_RATE
        self.fire_rate_acc = 0.0

        # Check si puede disparar o no
        self.can_fire = True

        self.pace_count = 0
        self.turn_after = 100
        self.direction = -1

    def update(self, time_delta):

        # Seteamos el sprite actual de la nave para simular animacion
        self.image = self.sprites[self.current_sprite]

        # Cambiamos el sprite para simular animacion

        self.pace_count += 1
        # Actualizamos la posicion del enemigo
        self.rect.x -= constants.ENEMY_SPEED
        self.rect.y += (self.direction * constants.ENEMY_SPEED+1) * (math.sqrt(2) / 2)

        if (self.pace_count >= self.turn_after):
            self.direction *= -1
            self.pace_count = 0

        # Cambiamos la dirección si se hostia con el borde de la pantalla
        if (self.rect.y <= 80):
            self.direction = 1  # turn
            self.pace_count = 0
        elif (self.rect.y >= constants.WIN_HEIGHT - self.rect.width):
            self.direction = -1
            self.pace_count = 0

        ## !!!FIX, utilizo el tiempo de ejecucion del juego, debería utilizar el tiempo del disparo anterior y añadirle los 0.2 secs
        # Cadencia de disparo
        if self.fire_rate_acc > self.fire_rate:
            self.fire_rate_acc = 0.0
            self.can_fire = True
        else:
            self.fire_rate_acc += time_delta


    # Disparo de la nave enemiga
    def shoot_bullet(self, enemy_bullet_sprite_list):
        if self.can_fire:
            self.can_fire = False
            bullet = Bullet(self.rect.x - 10, self.rect.y + 30, 1)
            enemy_bullet_sprite_list.add(bullet)

    def direction_to(self, actor):
        dx = actor.rect.x - self.rect.x
        dy = self.rect.y - actor.rect.y

        angle = math.degrees(math.atan2(dy, dx))
        if angle > 0:
            return angle

        return 360 + angle

    def move_towards(self, actor, dist):
        angle = math.radians(self.direction_to(actor))
        dy = dist * math.sin(angle)
        self.rect.y -= dy

    def point_towards(self, actor):
        print(self.direction_to(actor))
        self.angle = self.direction_to(actor)