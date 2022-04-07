import math
import pygame

from models.bullet import Bullet
from utils import constants

# Modelo de la nave pj
class Spaceship(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, x, y):
        super().__init__()

        # Posiciones iniciales
        self.pos_x = x
        self.pos_y = y

        # Cargamos las imagenes del Spaceship y la escalamos
        imagen1 = pygame.image.load(constants.SPACESHIP1)
        imagen2 = pygame.image.load(constants.SPACESHIP2)
        imagen3 = pygame.image.load(constants.SPACESHIP3)

        imagenBack = pygame.transform.rotozoom(imagen1, 0, constants.SPACESHIP_SIZE)
        imagenRecto = pygame.transform.rotozoom(imagen2, 0, constants.SPACESHIP_SIZE)
        imagenUp = pygame.transform.rotozoom(imagen3, 3, constants.SPACESHIP_SIZE)
        imagenDown = pygame.transform.rotozoom(imagen3, -3, constants.SPACESHIP_SIZE)


        # Inicializamos array de sprites y añadimos todos
        self.sprites = []
        self.sprites.append(imagenRecto)
        self.sprites.append(imagenUp)
        self.sprites.append(imagenDown)
        self.sprites.append(imagenBack)


        self.current_sprite = 0

        # Seteamos la imagen actual del sprite
        self.image = self.sprites[self.current_sprite]

        # Inicializamos el rectángulo (hitbox)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        # Velocidad de desplacamiento de la nave
        self.speed = constants.SPACESHIP_SPEED

        # Check si puede disparar o no
        self.can_fire = True

        # Vidas
        self.life = 5

        # Checkea si recibió un disparo
        self.hit_countdown = 0

        # Check si la nave sigue viva
        self.is_alive = True

        # Cooldown para disparar (cuando llega a la cadencia de disparo)
        self.time_cd = 0

    # Actualizamos la nave i.e posicion y sprite
    def update(self, time_delta):

        if self.can_fire is False:
            if (self.time_cd == constants.SPACESHIP_FIRE_RATE):
                self.can_fire = True
                self.time_cd = 0
            self.time_cd += 1

        self.current_sprite = 0
        # Cambiamos el sprite dependiendo de la direccion
        if self.rect.y > self.pos_y:
            self.current_sprite = 1
        elif self.rect.y < self.pos_y-1:
            self.current_sprite = 2
        elif self.rect.x > self.pos_x:
            self.current_sprite = 3
        # Seteamos el sprite actual de la nave para simular animacion

        if self.hit_countdown == 0:
            self.image.set_alpha(255)
            self.image = self.sprites[self.current_sprite]
        else:
            self.original_image = self.image
            if self.hit_countdown % 2:
                self.image = self.sprites[self.current_sprite]
                self.image.set_alpha(255)
            else:
                self.image = self.sprites[self.current_sprite]
                self.image.set_alpha(0)
            self.hit_countdown -= 1
        super(Spaceship, self).update(...)



        # Actualizamos la posicion de la nave
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y


    # Movemos la nave
    def move_spaceship(self, key_pressed):

        x, y = 0, 0

        if key_pressed[pygame.K_a]:
            if(self.rect.x > 0):
                x = -self.speed

        if key_pressed[pygame.K_d]:
            if (self.rect.x < constants.WIN_WIDTH-80):
                x = self.speed

        if key_pressed[pygame.K_w]:
            if (self.rect.y > 0):
                y = -self.speed

        if key_pressed[pygame.K_s]:
            if (self.rect.y < constants.WIN_HEIGHT-70):
                y = self.speed

        # Normalizamos el movimiento diagonal
        if x != 0 and y != 0:
            x = x * (math.sqrt(2) / 2)
            y = y * (math.sqrt(2) / 2)

        self.pos_x += x
        self.pos_y += y

    # Disparo de la nave
    def shoot_bullet(self, key_pressed, bullet_sprite_list):
        if key_pressed[pygame.K_SPACE]:
            if self.can_fire:
                self.can_fire = False
                bullet = Bullet(self.pos_x + 50, self.pos_y + 20, 0)
                bullet_sprite_list.add(bullet)
                shoot_sound = pygame.mixer.Sound(constants.BULLET_SOUND)
                shoot_sound.play()
                shoot_sound.set_volume(constants.MUSIC_VOLUME)