import pygame
import math
import random
from models.bullet import Bullet
from utils import constants


# Modelo de la nave pj
class Enemy(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, x, y, type, game):
        super().__init__()

        self.type = type

        self.game = game

        self.bomber_zone = ''

        # Inicializamos array de sprites y añadimos todos
        self.sprites = []

        if self.type == 'shooter':
            # Cargamos las imagenes del enemy shooter y la escalamos
            enemy_shooter_imagen1 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY1), 0,
                                                              constants.ENEMY_SHOOTER_SIZE)
            enemy_shooter_imagen2 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY2), 0,
                                                              constants.ENEMY_SHOOTER_SIZE)
            enemy_shooter_imagen3 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY3), 0,
                                                              constants.ENEMY_SHOOTER_SIZE)
            self.sprites.append(enemy_shooter_imagen1)
            self.sprites.append(enemy_shooter_imagen2)
            self.sprites.append(enemy_shooter_imagen3)
            self.speed = constants.ENEMY_SPEED

        elif self.type == 'follower':
            # Cargamos las imágenes del enemy follower y las escalamos
            enemy_follower_imagen1 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY_FOLLOWER1), 0,
                                                               constants.ENEMY_FOLLOWER_SIZE)
            enemy_follower_imagen2 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY_FOLLOWER2), 0,
                                                               constants.ENEMY_FOLLOWER_SIZE)
            enemy_follower_imagen3 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY_FOLLOWER3), 0,
                                                               constants.ENEMY_FOLLOWER_SIZE)
            enemy_follower_imagen4 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY_FOLLOWER4), 0,
                                                               constants.ENEMY_FOLLOWER_SIZE)
            self.sprites.append(enemy_follower_imagen1)
            self.sprites.append(enemy_follower_imagen2)
            self.sprites.append(enemy_follower_imagen3)
            self.sprites.append(enemy_follower_imagen4)
            self.speed = constants.ENEMY_FOLLOWER_SPEED

        elif self.type == 'bomber':
            # Cargamos las imágenes del enemy bomber y las escalamos
            enemy_bomber_imagen1 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY_BOMBER1), 0,
                                                             constants.ENEMY_BOMBER_SIZE)
            enemy_bomber_imagen2 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY_BOMBER2), 0,
                                                             constants.ENEMY_BOMBER_SIZE)
            enemy_bomber_imagen3 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY_BOMBER3), 0,
                                                             constants.ENEMY_BOMBER_SIZE)
            enemy_bomber_imagen4 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY_BOMBER1), 180,
                                                             constants.ENEMY_BOMBER_SIZE)
            enemy_bomber_imagen5 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY_BOMBER2), 180,
                                                             constants.ENEMY_BOMBER_SIZE)
            enemy_bomber_imagen6 = pygame.transform.rotozoom(pygame.image.load(constants.ENEMY_BOMBER3), 180,
                                                             constants.ENEMY_BOMBER_SIZE)
            self.sprites.append(enemy_bomber_imagen1)
            self.sprites.append(enemy_bomber_imagen2)
            self.sprites.append(enemy_bomber_imagen3)
            self.sprites.append(enemy_bomber_imagen4)
            self.sprites.append(enemy_bomber_imagen5)
            self.sprites.append(enemy_bomber_imagen6)

        elif self.type == 'axon':
            # Cargamos las imágenes del enemy follower y las escalamos
            enemy_axon_imagen1 = pygame.transform.rotozoom(pygame.image.load(constants.BOSS_AXON1), 0,
                                                           constants.BOSS_AXON_SIZE)
            enemy_axon_imagen2 = pygame.transform.rotozoom(pygame.image.load(constants.BOSS_AXON2), 0,
                                                           constants.BOSS_AXON_SIZE)
            enemy_axon_imagen3 = pygame.transform.rotozoom(pygame.image.load(constants.BOSS_AXON3), 0,
                                                           constants.BOSS_AXON_SIZE)

            self.sprites.append(enemy_axon_imagen1)
            self.sprites.append(enemy_axon_imagen2)
            self.sprites.append(enemy_axon_imagen3)
            self.speed = constants.BOSS_AXON_SPEED
            self.can_be_hit = True
            self.boss_can_move_up = True
            self.boss_can_attack = False
            self.hit_countdown = 0
            self.boss_life = constants.BOSS_AXON_LIFE

        self.current_sprite = 0

        # Seteamos la imagen actual del sprite
        self.image = self.sprites[self.current_sprite]

        # Inicializamos el rectángulo (hitbox)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos_x = x

        # Cadencia de disparo
        if self.type == 'shooter':
            self.fire_rate = constants.ENEMY_FIRE_RATE
        elif self.type == 'bomber':
            self.fire_rate = constants.ENEMY_BOMBER_FIRE_RATE
        elif self.type == 'axon':
            self.fire_rate = constants.BOSS_AXON_FIRE_RATE

        self.fire_rate_acc = 0.0

        # Check si puede disparar o no
        self.can_fire = True

        self.pace_count = 0
        self.turn_after = 100
        self.direction = random.randint(-1, 1)

        if self.game.multiplayer == False:
            self.enemy_target = self.game.player_1
        else:
            if random.randint(1, 2) == 1:
                if self.game.player_1.is_alive:
                    self.enemy_target = self.game.player_1
                else:
                    self.enemy_target = self.game.player_2
            else:
                if self.game.player_2.is_alive:
                    self.enemy_target = self.game.player_2
                else:
                    self.enemy_target = self.game.player_1

    def update(self, time_delta):

        # Seteamos el sprite actual de la nave para simular animacion
        self.image = self.sprites[self.current_sprite]

        if self.type == 'shooter':
            self.pace_count += 1
            # Actualizamos la posicion del enemigo
            self.rect.x -= constants.ENEMY_SPEED
            self.rect.y += (self.direction * constants.ENEMY_SPEED + 1) * (math.sqrt(2) / 2)

            self.calc_fire_rate(time_delta)

            if (self.pace_count >= self.turn_after):
                self.direction *= -1
                self.pace_count = 0

            # Cambiamos la dirección si se hostia con el borde de la pantalla
            if (self.rect.y <= 0):
                self.direction = 1  # turn
                self.pace_count = 0
            elif (self.rect.y >= constants.WIN_HEIGHT - self.rect.width):
                self.direction = -1
                self.pace_count = 0


        elif self.type == 'follower':
            self.rect.x -= constants.ENEMY_FOLLOWER_SPEED
            self.move_towards(self.enemy_target, constants.ENEMY_FOLLOWER_SPEED + 4)


        elif self.type == 'bomber':
            self.pos_x -= constants.MAP_MOVEMENT_RATE
            self.rect.x = math.floor(self.pos_x)

            self.calc_fire_rate(time_delta)

            if self.bomber_zone == 'down':
                if self.rect.x > self.enemy_target.rect.x + 100:
                    self.current_sprite = 2
                elif self.rect.x < self.enemy_target.rect.x - 100:
                    self.current_sprite = 1
                else:
                    self.current_sprite = 0

            elif self.bomber_zone == 'up':
                if self.rect.x > self.enemy_target.rect.x + 100:
                    self.current_sprite = 4
                elif self.rect.x < self.enemy_target.rect.x - 100:
                    self.current_sprite = 5
                else:
                    self.current_sprite = 3

        elif self.type == 'axon':
            self.calc_fire_rate(time_delta)
            if self.rect.x > 800:
                self.rect.x -= self.speed
            elif self.rect.x == 800:
                if self.current_sprite == 0 or self.current_sprite == 1:
                    self.move_boss_y()
            if self.current_sprite == 2:
                self.move_boss_x()

            if self.hit_countdown == 0:
                self.image.set_alpha(255)
                self.image = self.sprites[self.current_sprite]
            else:
                if self.hit_countdown % 2:
                    self.image = self.sprites[1]
                    self.image.set_alpha(255)
                else:
                    self.image = self.sprites[1]
                    self.image.set_alpha(150)
                self.hit_countdown -= 1
            super(Enemy, self).update(...)

    def calc_fire_rate(self, time_delta):
        if self.fire_rate_acc > self.fire_rate:
            self.fire_rate_acc = 0.0
            self.can_fire = True
        else:
            self.fire_rate_acc += time_delta

    # Disparo de la nave enemiga
    def shoot_bullet(self, enemy_bullet_sprite_list):
        if self.can_fire:
            self.can_fire = False
            if self.type == 'shooter':
                bullet = Bullet(self.rect.x - 10, self.rect.y + 30, 'enemy_shot', None)
            elif self.type == 'bomber':
                bullet = Bullet(self.rect.x, self.rect.y, 'bomber_shot', self.enemy_target)
            enemy_bullet_sprite_list.add(bullet)

    def direction_to(self, actor):
        dx = actor.rect.x - self.rect.x
        dy = self.rect.y - actor.rect.y

        angle = math.degrees(math.atan2(dy, dx))
        if angle > 0:
            return angle

        return 360 + angle

    def move_towards(self, actor, dist):

        if self.rect.x > actor.rect.x:
            angle = math.radians(self.direction_to(actor))
            dy = dist * math.sin(angle)
            self.rect.y -= dy

    def move_boss_y(self):
        self.speed = constants.BOSS_AXON_SPEED
        if self.boss_can_move_up is True:
            if self.rect.y > 90:
                self.rect.y -= self.speed
            if self.rect.y <= 90:
                self.boss_can_move_up = False
        elif self.boss_can_move_up is False:
            if self.rect.y < 330:
                self.rect.y += self.speed
            if self.rect.y >= 330:
                self.boss_can_move_up = True

    def move_boss_x(self):
        if self.boss_can_attack is True:
            self.speed = 17
            self.rect.x -= self.speed
            if self.rect.x <= 30:
                self.boss_can_attack = False
        else:
            self.speed = constants.BOSS_AXON_SPEED + 4
            self.rect.x += self.speed
            if self.rect.x >= 798:
                self.rect.x = 800
                self.current_sprite = 0
