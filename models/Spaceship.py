import math
import pygame

from models.bullet import Bullet
from utils import constants


# Modelo de la nave pj
class Spaceship(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, x, y, player, game):
        super().__init__()

        # Posiciones iniciales
        self.pos_x = x
        self.pos_y = y
        self.player = player

        self.game = game

        self.score = 0

        if self.player == 'player1':
            imagenBack = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER1_SPACESHIP1), 0,
                                                   constants.SPACESHIP_SIZE)
            imagenBack.convert()

            imagenRecto = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER1_SPACESHIP2), 0,
                                                    constants.SPACESHIP_SIZE)
            imagenRecto.convert()

            imagenUp = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER1_SPACESHIP3), 3,
                                                 constants.SPACESHIP_SIZE)
            imagenUp.convert()

            imagenDown = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER1_SPACESHIP3), -3,
                                                   constants.SPACESHIP_SIZE)
            imagenDown.convert()

        elif self.player == 'player2':
            imagenBack = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER2_SPACESHIP1), 0,
                                                   constants.SPACESHIP_SIZE)
            imagenBack.convert()

            imagenRecto = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER2_SPACESHIP2), 0,
                                                    constants.SPACESHIP_SIZE)
            imagenRecto.convert()

            imagenUp = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER2_SPACESHIP3), 3,
                                                 constants.SPACESHIP_SIZE)
            imagenUp.convert()

            imagenDown = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER2_SPACESHIP3), -3,
                                                   constants.SPACESHIP_SIZE)
            imagenDown.convert()

        # Inicializamos array de sprites y añadimos todos
        self.sprites = []
        self.sprites.append(imagenRecto)
        self.sprites.append(imagenUp)
        self.sprites.append(imagenDown)
        self.sprites.append(imagenBack)

        self.current_sprite = 0

        # Seteamos la imagen actual del sprite
        self.image = self.sprites[self.current_sprite]

        self.charged_shot_ammo = 0

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
        self.is_alive = False

        # Cooldown para disparar (cuando llega a la cadencia de disparo)
        self.time_cd = 0

        self.fire_rate = constants.SPACESHIP_FIRE_RATE

        self.got_bonus = False
        self.bonus_text = 'Speed up!'
        self.bonus_text_cd = 0
        self.bonus_text_cd_rate = constants.BONUS_TEXT_CD_RATE

        self.can_move_down = True
        self.can_move_up = True

    # Actualizamos la nave i.e posicion y sprite
    def update(self, time_delta):

        if self.got_bonus is True:
            self.game.draw_text(self.bonus_text, 14, self.rect.x + 35, self.rect.y - 15)
            self.bonus_text_cd += 1
            if self.bonus_text_cd == self.bonus_text_cd_rate:
                self.bonus_text_cd = 0
                self.got_bonus = False

        if self.life == 0:
            self.is_alive = False
            self.charged_shot_ammo = 0
            self.kill()

        if self.can_fire is False:
            if (self.time_cd >= self.fire_rate):
                self.can_fire = True
                self.time_cd = 0
            self.time_cd += 1

        self.current_sprite = 0
        # Cambiamos el sprite dependiendo de la direccion
        if self.rect.y > self.pos_y:
            self.current_sprite = 1
        elif self.rect.y < self.pos_y - 1:
            self.current_sprite = 2
        elif self.rect.x > self.pos_x:
            self.current_sprite = 3

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

        if self.player == 'player1':
            if key_pressed[pygame.K_a]:
                if (self.rect.x > 0):
                    x = -self.speed

            if key_pressed[pygame.K_d]:
                if (self.rect.x < constants.WIN_WIDTH - 80):
                    x = self.speed

            if key_pressed[pygame.K_w]:
                if (self.rect.y > 0):
                    if self.can_move_up:
                        y = -self.speed

            if key_pressed[pygame.K_s]:
                if (self.rect.y < constants.WIN_HEIGHT - 40):
                    if self.can_move_down:
                        y = self.speed
        elif self.player == 'player2':
            if key_pressed[pygame.K_LEFT]:
                if (self.rect.x > 0):
                    x = -self.speed

            if key_pressed[pygame.K_RIGHT]:
                if (self.rect.x < constants.WIN_WIDTH - 80):
                    x = self.speed

            if key_pressed[pygame.K_UP]:
                if (self.rect.y > 0):
                    if self.can_move_up:
                        y = -self.speed

            if key_pressed[pygame.K_DOWN]:
                if (self.rect.y < constants.WIN_HEIGHT - 40):
                    if self.can_move_down:
                        y = self.speed

        # Normalizamos el movimiento diagonal
        if x != 0 and y != 0:
            x = x * (math.sqrt(2) / 2)
            y = y * (math.sqrt(2) / 2)

        self.pos_x += x
        self.pos_y += y

        self.can_move_up = True
        self.can_move_down = True

    # Disparo de la nave
    def shoot_bullet(self, key_pressed, bullet_sprite_list):
        if self.player == 'player1':
            if self.is_alive:
                if key_pressed[pygame.K_SPACE]:
                    if self.can_fire:
                        self.can_fire = False
                        bullet = Bullet(self.pos_x + 80, self.pos_y + 15, 'player1_shot', None)
                        bullet_sprite_list.add(bullet)
                        shoot_sound = pygame.mixer.Sound(constants.BULLET_SOUND)
                        shoot_sound.play()
                        shoot_sound.set_volume(constants.MUSIC_VOLUME)

                if key_pressed[pygame.K_LCTRL]:
                    if self.charged_shot_ammo > 0:
                        if self.can_fire:
                            self.can_fire = False
                            bullet = Bullet(self.pos_x + 80, self.pos_y + 15, 'player1_chargedshot', None)
                            bullet_sprite_list.add(bullet)
                            shoot_sound = pygame.mixer.Sound(constants.BULLET_CHARGED_SOUND)
                            shoot_sound.play()
                            shoot_sound.set_volume(constants.MUSIC_VOLUME)
                            self.charged_shot_ammo -= 1

        elif self.player == 'player2':
            if self.is_alive:
                if key_pressed[pygame.K_RSHIFT]:
                    if self.can_fire:
                        self.can_fire = False
                        bullet = Bullet(self.pos_x + 80, self.pos_y + 15, 'player2_shot', None)
                        bullet_sprite_list.add(bullet)
                        shoot_sound = pygame.mixer.Sound(constants.BULLET_SOUND)
                        shoot_sound.play()
                        shoot_sound.set_volume(constants.MUSIC_VOLUME)

                if key_pressed[pygame.K_RCTRL]:
                    if self.charged_shot_ammo > 0:
                        if self.can_fire:
                            self.can_fire = False
                            bullet = Bullet(self.pos_x + 80, self.pos_y + 15, 'player2_chargedshot', None)
                            bullet_sprite_list.add(bullet)
                            shoot_sound = pygame.mixer.Sound(constants.BULLET_CHARGED_SOUND)
                            shoot_sound.play()
                            shoot_sound.set_volume(constants.MUSIC_VOLUME)
                            self.charged_shot_ammo -= 1
