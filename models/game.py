import sys

import pygame
from pygame import mixer
import json
from models.map_collision import Map
from models.scoreboard import Scoreboard
from models.bonus import Bonus
from models.menu import MainMenu, OptionsMenu, CreditsMenu, PauseMenu, GameOverMenu, VolumenMenu, VideoMenu, \
    ControlsMenu, ControlsPlayer1Menu, ControlsPlayer2Menu, PlayMenu
from utils import constants
from random import randint
from models.enemy import Enemy
from models.explosion import Explosion
from models.spaceship import Spaceship
from utils.sound_func import Sound
from utils.stopwatch import Stopwatch


class Game:
    def __init__(self):

        pygame.init()

        pygame.display.set_caption(constants.GAME_TITLE)
        pygame.display.set_icon(pygame.image.load(constants.GAME_ICON))
        pygame.mouse.set_visible(False)

        # Variables de ejecución del juego
        self.running, self.playing = True, False

        self.game_time = Stopwatch()

        self.mixer = mixer
        self.mixer.init()
        self.mixer.music.load(constants.STAGE1_MUSIC)

        self.mixer.music.set_volume(constants.MUSIC_VOLUME)

        self.menu_music = pygame.mixer.Sound(constants.MENU_MUSIC)
        self.end_game_music = pygame.mixer.Sound(constants.END_GAME_MUSIC)

        self.hit_sound = Sound()
        self.explosion_sound = Sound()

        self.multiplayer = False

        # Variables booleanas de botones del menu
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

        # Ancho y alto de la pantalla
        self.DISPLAY_W, self.DISPLAY_H = constants.WIN_WIDTH, constants.WIN_HEIGHT

        # Variable de pantalla
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))

        self.font_name = constants.TEXT_FONT_MENU

        # Ventana del juego
        if constants.WINDOW_MODE == 'fullscreen':
            self.window_mode = pygame.FULLSCREEN
        elif constants.WINDOW_MODE == 'windowed':
            self.window_mode = pygame.SHOWN

        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), self.window_mode)
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        # Variables de los menus
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.pause = PauseMenu(self)
        self.game_over = GameOverMenu(self)
        self.volumen_menu = VolumenMenu(self)
        self.video_menu = VideoMenu(self)
        self.controls_menu = ControlsMenu(self)
        self.controls_player1_menu = ControlsPlayer1Menu(self)
        self.controls_player2_menu = ControlsPlayer2Menu(self)
        self.play_menu = PlayMenu(self)
        self.curr_menu = self.main_menu

        # Puntuacion del jugador
        self.score = 0

        # Inicializamos las listas de sprites
        self.spaceship_sprite_list = pygame.sprite.Group()

        # lista de spaceship_bullet_sprite_list
        self.spaceship_bullet_sprite_list = pygame.sprite.Group()

        # lista de enemy_shooter_sprite_list
        self.enemy_shooter_sprite_list = pygame.sprite.Group()

        # lista de enemy_follower_sprite_list
        self.enemy_follower_sprite_list = pygame.sprite.Group()

        # lista de enemy_bomber_sprite_list
        self.enemy_bomber_sprite_list = pygame.sprite.Group()

        # lista de enemy_bullet_sprite_list
        self.enemy_bullet_sprite_list = pygame.sprite.Group()

        # lista de explosiones
        self.explosion_sprite_list = pygame.sprite.Group()

        # lista de bonus
        self.bonus_sprite_list = pygame.sprite.Group()

        # lista de boss
        self.boss_axon_list = pygame.sprite.Group()

        # lista de cajas de colision del mapa
        self.map_collision_list = pygame.sprite.Group()
        self.init_map_collision_box()

        # Background del juego
        self.background = pygame.transform.scale(pygame.image.load(constants.BACKGROUND),
                                                 (constants.WIN_WIDTH, constants.WIN_HEIGHT))
        self.background.convert()
        self.cueva_img = pygame.image.load(constants.MAP)
        self.cueva_img.convert()

        # Inicializamos la nave del jugador
        self.player_1 = Spaceship(30, constants.WIN_HEIGHT / 2, 'player1', self)
        self.player_2 = Spaceship(30, self.player_1.rect.y + 80, 'player2', self)

        self.boss_axon = Enemy(constants.WIN_WIDTH + 100, constants.WIN_HEIGHT / 2 - 150, 'axon', self)
        self.play_music_boss = False

        # Eventos del juego
        self.spawn_enemy_shooter = pygame.USEREVENT
        self.animate_enemy_shooter = pygame.USEREVENT + 1
        self.spawn_enemy_follower = pygame.USEREVENT + 2
        self.animate_enemy_follower = pygame.USEREVENT + 3
        self.enemy_explosion = pygame.USEREVENT + 4
        self.animate_bonus = pygame.USEREVENT + 5
        self.bonus_speed_spawn = pygame.USEREVENT + 6
        self.bonus_charged_shot_spawn = pygame.USEREVENT + 7
        self.bonus_fire_rate_spawn = pygame.USEREVENT + 8
        self.spawn_enemy_bomber = pygame.USEREVENT + 9
        self.boss_axon_attack = pygame.USEREVENT + 10
        self.boss_defeated_end_game = pygame.USEREVENT + 11

        self.scoreboard = Scoreboard(self)

        self.map_can_move = True
        self.enemy_shooter_spawn_1 = 100
        self.enemy_shooter_spawn_2 = 620

        # Posicion x del mapa y el background
        self.cX = 0
        self.bgX = 0
        self.bgX2 = self.background.get_width()

        self.can_spawn_bonus = False
        self.bonus_type = ''

        self.events_init = True
        self.event_end_game = True

    # Loop de juego
    def game_loop(self):

        self.player_1.is_alive = True
        if self.multiplayer == True:
            self.player_2.is_alive = True
            self.spaceship_sprite_list.add(self.player_2)

        # lista de spaceship_sprite_list
        self.spaceship_sprite_list.add(self.player_1)

        # Reloj interno del juego
        clock = pygame.time.Clock()

        while self.playing:

            delta_time = clock.tick(constants.FPS) / 1000.0

            self.initialize_events()

            # Eventos del juego
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.curr_menu = self.pause
                        self.game_time.pause_time()
                        self.mixer.music.pause()
                        self.playing = False

                if event.type == self.spawn_enemy_shooter:
                    enemy = Enemy(constants.WIN_WIDTH, randint(constants.ENEMY_SHOOTER_SPAWN_ZONE_UP, constants.ENEMY_SHOOTER_SPAWN_ZONE_DOWN), 'shooter', self)
                    self.enemy_shooter_sprite_list.add(enemy)

                if event.type == self.animate_enemy_shooter:
                    for enemy in self.enemy_shooter_sprite_list:
                        if enemy.current_sprite < 2:
                            enemy.current_sprite += 1
                        else:
                            enemy.current_sprite = 0

                if event.type == self.spawn_enemy_follower:
                    enemy = Enemy(constants.WIN_WIDTH, randint(0, constants.WIN_HEIGHT), 'follower', self)
                    self.enemy_follower_sprite_list.add(enemy)

                if event.type == self.animate_enemy_follower:
                    for enemy in self.enemy_follower_sprite_list:
                        if enemy.current_sprite < 3:
                            enemy.current_sprite += 1
                        else:
                            enemy.current_sprite = 0

                if event.type == self.spawn_enemy_bomber:
                    enemy = Enemy(constants.WIN_WIDTH, constants.ENEMY_BOMBER_SPAWN_ZONE_DOWN, 'bomber', self)
                    enemy.bomber_zone = 'down'
                    enemy2 = Enemy(constants.WIN_WIDTH + 150, constants.ENEMY_BOMBER_SPAWN_ZONE_UP, 'bomber', self)
                    enemy2.bomber_zone = 'up'
                    self.enemy_bomber_sprite_list.add(enemy)
                    self.enemy_bomber_sprite_list.add(enemy2)

                if event.type == self.enemy_explosion:
                    for explosion in self.explosion_sprite_list:
                        explosion.current_sprite += 1

                if event.type == self.animate_bonus:
                    for bonus in self.bonus_sprite_list:
                        bonus.current_sprite += 1

                if event.type == self.bonus_speed_spawn:
                    self.can_spawn_bonus = True
                    self.bonus_type = 'speed'

                if event.type == self.bonus_charged_shot_spawn:
                    self.can_spawn_bonus = True
                    self.bonus_type = 'bullet'

                if event.type == self.bonus_fire_rate_spawn:
                    self.can_spawn_bonus = True
                    self.bonus_type = 'firerate'

                if event.type == self.boss_axon_attack:
                    self.boss_axon.boss_can_attack = True
                    self.boss_axon.current_sprite = 2

                if event.type == self.boss_defeated_end_game:
                    self.curr_menu = self.credits
                    self.playing = False

            # Si el enemigo se sale de la pantalla lo eliminamos
            for enemy in self.enemy_shooter_sprite_list:
                if enemy.rect.x < -60:
                    self.enemy_shooter_sprite_list.remove(enemy)
                else:
                    enemy.shoot_bullet(self.enemy_bullet_sprite_list)

            # Si el enemigo se sale de la pantalla lo eliminamos
            for enemy in self.enemy_follower_sprite_list:
                if enemy.rect.x < -60:
                    self.enemy_follower_sprite_list.remove(enemy)

            for enemy in self.enemy_bomber_sprite_list:
                if enemy.rect.x < -40:
                    self.enemy_bomber_sprite_list.remove(enemy)
                else:
                    enemy.shoot_bullet(self.enemy_bullet_sprite_list)

            # Si la bala se sale de la pantalla la eliminamos
            for bullet in self.enemy_bullet_sprite_list:
                if bullet.rect.x < -20 or bullet.rect.x > constants.WIN_WIDTH + 40:
                    self.enemy_bullet_sprite_list.remove(bullet)

            # Si la bala se sale de la pantalla la eliminamos
            for bullet in self.spaceship_bullet_sprite_list:
                if bullet.rect.x > constants.WIN_WIDTH:
                    self.spaceship_bullet_sprite_list.remove(bullet)

            # Si la bala se sale de la pantalla la eliminamos
            for bonus in self.bonus_sprite_list:
                if bonus.rect.x < -20:
                    self.bonus_sprite_list.remove(bonus)

            enemy_shooter_hit_by_bullet = pygame.sprite.groupcollide(self.spaceship_bullet_sprite_list,
                                                                     self.enemy_shooter_sprite_list, False,
                                                                     True)
            enemy_follower_hit_by_bullet = pygame.sprite.groupcollide(self.spaceship_bullet_sprite_list,
                                                                      self.enemy_follower_sprite_list, False,
                                                                      True)
            enemy_bomber_hit_by_bullet = pygame.sprite.groupcollide(self.spaceship_bullet_sprite_list,
                                                                    self.enemy_bomber_sprite_list, False,
                                                                    True)

            player_hit_by_bullet = pygame.sprite.groupcollide(self.spaceship_sprite_list, self.enemy_bullet_sprite_list,
                                                              False,
                                                              True)

            player_hit_by_enemy_follower = pygame.sprite.groupcollide(self.spaceship_sprite_list,
                                                                      self.enemy_follower_sprite_list, False,
                                                                      True)

            player_hit_by_enemy_shooter = pygame.sprite.groupcollide(self.spaceship_sprite_list,
                                                                     self.enemy_shooter_sprite_list, False,
                                                                     True)

            player_hit_by_enemy_bomber = pygame.sprite.groupcollide(self.spaceship_sprite_list,
                                                                     self.enemy_bomber_sprite_list, False,
                                                                     True)

            player_collision_with_bonus = pygame.sprite.groupcollide(self.bonus_sprite_list, self.spaceship_sprite_list,
                                                                     True,
                                                                     False)

            player_collision_with_map = pygame.sprite.groupcollide(self.spaceship_sprite_list, self.map_collision_list,
                                                                   False,
                                                                   False)

            player_hit_by_boss_axon = pygame.sprite.groupcollide(self.spaceship_sprite_list, self.boss_axon_list, False,
                                                                 False)

            boss_axon_hit_by_bullet = pygame.sprite.groupcollide(self.spaceship_bullet_sprite_list, self.boss_axon_list,
                                                                 False, False)

            enemy_shooter_collision_with_map = pygame.sprite.groupcollide(self.enemy_shooter_sprite_list, self.map_collision_list,
                                                                   False,
                                                                   False)

            for bonus in player_collision_with_bonus:
                self.play_sound(constants.BONUS_SOUND)
                for player in self.spaceship_sprite_list:
                    player.got_bonus = True
                    if player.life < 5:
                        player.life += 1
                    if bonus.type == 'speed':
                            player.speed += 0.75
                            player.bonus_text = 'Speed UP'
                    elif bonus.type == 'bullet':
                            player.charged_shot_ammo = 20
                            player.bonus_text = 'Charged Shot ammo UP'
                    elif bonus.type == 'firerate':
                            player.fire_rate -= 1.5
                            player.bonus_text = 'Fire Rate UP'


            # cuando alcanzo al enemigo subo puntuación y animo muerte
            for hit in enemy_shooter_hit_by_bullet:
                if self.can_spawn_bonus:
                    self.bonus_sprite_list.add(Bonus(hit.rect.x, hit.rect.y, self.bonus_type))
                    self.can_spawn_bonus = False
                if hit.type == 'player1_shot' or hit.type == 'player1_chargedshot':
                    self.player_1.score += 50
                elif hit.type == 'player2_shot' or hit.type == 'player2_chargedshot':
                    self.player_2.score += 50
                x = hit.rect.x - 135
                y = hit.rect.y - 135
                explosion = Explosion(x, y, constants.EXPLOSION_SHOOTER_ZOOM)
                self.explosion_sprite_list.add(explosion)
                self.explosion_sound.play_sound(constants.EXPLOSION_SOUND)
                if hit.type == 'player1_shot' or hit.type == 'player2_shot':
                    hit.kill()

            for hit in enemy_bomber_hit_by_bullet:
                if hit.type == 'player1_shot' or hit.type == 'player1_chargedshot':
                    self.player_1.score += 100
                elif hit.type == 'player2_shot' or hit.type == 'player2_chargedshot':
                    self.player_2.score += 100
                x = hit.rect.x - 120
                y = hit.rect.y - 120
                explosion = Explosion(x, y, constants.EXPLOSION_SHOOTER_ZOOM)
                self.explosion_sprite_list.add(explosion)
                self.explosion_sound.play_sound(constants.EXPLOSION_SOUND)
                if hit.type == 'player1_shot' or hit.type == 'player2_shot':
                    hit.kill()

            for hit in enemy_follower_hit_by_bullet:
                if self.can_spawn_bonus:
                    self.bonus_sprite_list.add(Bonus(hit.rect.x, hit.rect.y, self.bonus_type))
                    self.can_spawn_bonus = False
                if hit.type == 'player1_shot' or hit.type == 'player1_chargedshot':
                    self.player_1.score += 75
                elif hit.type == 'player2_shot' or hit.type == 'player2_chargedshot':
                    self.player_2.score += 75
                x = hit.rect.x - 110
                y = hit.rect.y - 110
                explosion = Explosion(x, y, constants.EXPLOSION_FOLLOWER_ZOOM)
                self.explosion_sprite_list.add(explosion)
                self.explosion_sound.play_sound(constants.EXPLOSION_SOUND)
                if hit.type == 'player1_shot' or hit.type == 'player2_shot':
                    hit.kill()

            for player in player_hit_by_bullet:

                if player.player == 'player1':
                    if self.player_1.hit_countdown == 0:
                        self.player_1.hit_countdown = 30
                        self.player_1.life -= 1
                        self.hit_sound.play_sound(constants.HIT_SOUND)
                elif player.player == 'player2':
                    if self.player_2.hit_countdown == 0:
                        self.player_2.hit_countdown = 30
                        self.player_2.life -= 1
                        self.hit_sound.play_sound(constants.HIT_SOUND)

            for player in player_hit_by_enemy_follower:
                if player.player == 'player1':
                    if self.player_1.hit_countdown == 0:
                        self.player_1.hit_countdown = 30
                        self.player_1.life -= 1
                elif player.player == 'player2':
                    if self.player_2.hit_countdown == 0:
                        self.player_2.hit_countdown = 30
                        self.player_2.life -= 1
                x = player.rect.x - 40
                y = player.rect.y - 80
                explosion = Explosion(x, y, constants.EXPLOSION_FOLLOWER_ZOOM)
                self.explosion_sprite_list.add(explosion)
                self.hit_sound.play_sound(constants.HIT_SOUND)
                self.explosion_sound.play_sound(constants.EXPLOSION_SOUND)

            for player in player_hit_by_enemy_shooter:
                if player.player == 'player1':
                    if self.player_1.hit_countdown == 0:
                        self.player_1.hit_countdown = 30
                        self.player_1.life -= 1
                elif player.player == 'player2':
                    if self.player_2.hit_countdown == 0:
                        self.player_2.hit_countdown = 30
                        self.player_2.life -= 1
                x = player.rect.x - 40
                y = player.rect.y - 120
                explosion = Explosion(x, y, constants.EXPLOSION_SHOOTER_ZOOM)
                self.explosion_sprite_list.add(explosion)
                self.hit_sound.play_sound(constants.HIT_SOUND)
                self.explosion_sound.play_sound(constants.EXPLOSION_SOUND)

            for player in player_hit_by_enemy_bomber:
                if player.player == 'player1':
                    if self.player_1.hit_countdown == 0:
                        self.player_1.hit_countdown = 30
                        self.player_1.life -= 1
                elif player.player == 'player2':
                    if self.player_2.hit_countdown == 0:
                        self.player_2.hit_countdown = 30
                        self.player_2.life -= 1
                x = player.rect.x - 40
                y = player.rect.y - 120
                explosion = Explosion(x, y, constants.EXPLOSION_SHOOTER_ZOOM)
                self.explosion_sprite_list.add(explosion)
                self.hit_sound.play_sound(constants.HIT_SOUND)
                self.explosion_sound.play_sound(constants.EXPLOSION_SOUND)

            for player in player_hit_by_boss_axon:
                if player.player == 'player1':
                    if self.player_1.hit_countdown == 0:
                        self.player_1.hit_countdown = 30
                        self.player_1.life -= 1
                        self.hit_sound.play_sound(constants.HIT_SOUND)
                elif player.player == 'player2':
                    if self.player_2.hit_countdown == 0:
                        self.player_2.hit_countdown = 30
                        self.player_2.life -= 1
                        self.hit_sound.play_sound(constants.HIT_SOUND)

            for hit in boss_axon_hit_by_bullet:
                if self.boss_axon.boss_life > 0:
                    if self.boss_axon.current_sprite != 2:
                        self.boss_axon.hit_countdown = 15
                        self.play_sound(constants.BOSS_HIT_SOUND)
                        if hit.type == 'player1_chargedshot' or hit.type == 'player2_chargedshot':
                            self.boss_axon.boss_life -= 2
                        else:
                            self.boss_axon.boss_life -= 1
                    hit.kill()
                else:
                    explosion = Explosion(self.boss_axon.rect.x - 400, self.boss_axon.rect.y - 400,
                                          constants.EXPLOSION_BOSS_ZOOM)
                    self.explosion_sprite_list.add(explosion)
                    self.explosion_sound.play_sound(constants.EXPLOSION_SOUND)
                    hit.kill()
                    self.boss_axon.kill()
                    for player in self.spaceship_sprite_list:
                        if player.is_alive:
                            player.score += 2500


            for player in player_collision_with_map:
                if player.rect.y > constants.WIN_HEIGHT / 2:
                    player.can_move_down = False
                elif player.rect.y < constants.WIN_HEIGHT / 2:
                    player.can_move_up = False

            for enemy in enemy_shooter_collision_with_map:
                if enemy.rect.y > constants.WIN_HEIGHT / 2:
                    enemy.bounce_down = True
                if enemy.rect.y < constants.WIN_HEIGHT / 2:
                    enemy.bounce_up = True

            if self.multiplayer is False:
                if self.player_1.is_alive is False:
                    self.playing = False
                    self.curr_menu = self.game_over
                    pygame.time.set_timer(self.spawn_enemy_follower, 0, False)
            else:
                if self.player_1.is_alive == False and self.player_2.is_alive == False:
                    self.playing = False
                    self.curr_menu = self.game_over
                    pygame.time.set_timer(self.spawn_enemy_follower, 0, False)

            # Actualizamos el scoreboard del player 1
            self.scoreboard.draw_scoreboard_player_1(self.player_1.life)
            if self.multiplayer == True:
                self.scoreboard.draw_scoreboard_player_2(self.player_2.life)

            # Actualizamos todas las listas de sprites
            self.update_and_draw_sprite_lists(delta_time)

            # Checkeamos las teclas pulsadas para movimiento de player 1
            key_pressed = pygame.key.get_pressed()
            self.player_1.move_spaceship(key_pressed)
            self.player_1.shoot_bullet(key_pressed, self.spaceship_bullet_sprite_list)
            if self.multiplayer == True:
                self.player_2.move_spaceship(key_pressed)
                self.player_2.shoot_bullet(key_pressed, self.spaceship_bullet_sprite_list)

            # Actualizamos la ventana
            pygame.display.update()
            self.reset_keys()

            self.window.blit(self.background, (self.bgX, 0))  # Dibuja el primer background
            self.window.blit(self.background, (self.bgX2, 0))  # Dibuja el segundo background

            self.window.blit(self.cueva_img, (self.cX, 0))

            if self.cX >= constants.MAP_SIZE_DISPLACEMENT:
                self.cX -= constants.MAP_MOVEMENT_RATE
            else:
                self.map_can_move = False

            # Movemos ambos backgrounds a la izquierda
            self.bgX -= 1
            self.bgX2 -= 1

            # Cambiamos la posicion del background de la izq a la derecha
            if self.bgX < self.background.get_width() * -1:
                self.bgX = self.background.get_width()
            if self.bgX2 < self.background.get_width() * -1:
                self.bgX2 = self.background.get_width()

    def init_map_collision_box(self):
        # Techo
        self.map_collision_list.add(Map(7300, 0, pygame.Rect(0, 0, 14730, 75), self))
        self.map_collision_list.add(Map(16000, 0, pygame.Rect(0, 0, 6900, 120), self))

        # Suelo
        self.map_collision_list.add(Map(7300, 645, pygame.Rect(0, 0, 5200, 75), self))
        self.map_collision_list.add(Map(12500, 560, pygame.Rect(0, 0, 3540, 155), self))
        self.map_collision_list.add(Map(16000, 605, pygame.Rect(0, 0, 6900, 115), self))
        self.map_collision_list.add(Map(16810, 550, pygame.Rect(0, 0, 938, 170), self))

    def initialize_events(self):
        if self.events_init:
            pygame.time.set_timer(self.spawn_enemy_shooter, constants.ENEMY_SPAWN_RATE)
            pygame.time.set_timer(self.animate_enemy_shooter, constants.ENEMY_ANIMATION_RATE)
            pygame.time.set_timer(self.animate_enemy_follower, constants.ENEMY_FOLLOWER_ANIMATION_RATE)
            pygame.time.set_timer(self.enemy_explosion, constants.EXPLOSION_ANIMATION_RATE)
            pygame.time.set_timer(self.animate_bonus, constants.BONUS_ANIMATE_RATE)
            pygame.time.set_timer(self.bonus_speed_spawn, constants.BONUS_SPEED_SPAWN_RATE, 4)
            pygame.time.set_timer(self.bonus_charged_shot_spawn, constants.BONUS_CHARGED_SHOT_SPAWN_RATE)
            pygame.time.set_timer(self.bonus_fire_rate_spawn, constants.BONUS_FIRE_RATE_SPAWN_RATE, 3)
            pygame.time.set_timer(self.boss_axon_attack, 0)
            pygame.time.set_timer(self.spawn_enemy_bomber, 0)
            constants.ENEMY_BOMBER_SPAWN_ZONE_UP = 70
            constants.ENEMY_BOMBER_SPAWN_ZONE_DOWN = 525
            constants.ENEMY_SHOOTER_SPAWN_ZONE_UP = 100
            constants.ENEMY_SHOOTER_SPAWN_ZONE_DOWN = 620
            self.events_init = False

        if self.game_time.current_time() > 19 and self.game_time.current_time() < 19.5:
            pygame.time.set_timer(self.spawn_enemy_follower, constants.ENEMY_FOLLOWER_SPAWN_RATE)
        if self.cX < -11150 and self.cX > -11160:
            pygame.time.set_timer(self.spawn_enemy_bomber, constants.ENEMY_BOMBER_SPAWN_RATE, 10)
            pygame.time.set_timer(self.spawn_enemy_shooter, 0)
        if self.cX < -14750 and self.cX > -14760:
            pygame.time.set_timer(self.spawn_enemy_shooter, constants.ENEMY_SPAWN_RATE)
            constants.ENEMY_SHOOTER_SPAWN_ZONE_UP = 130
            constants.ENEMY_SHOOTER_SPAWN_ZONE_DOWN = 530
        if self.cX < -16400 and self.cX > -16410:
            constants.ENEMY_BOMBER_SPAWN_RATE = 4000
            constants.ENEMY_BOMBER_SPAWN_ZONE_DOWN = 570
            constants.ENEMY_BOMBER_SPAWN_ZONE_UP = 114
            pygame.time.set_timer(self.spawn_enemy_bomber, constants.ENEMY_BOMBER_SPAWN_RATE, 7)
        if self.cX < -20200 and self.cX > -20210:
            pygame.time.set_timer(self.spawn_enemy_shooter, 0)
            pygame.time.set_timer(self.spawn_enemy_follower, 0)
            pygame.time.set_timer(self.spawn_enemy_bomber, 0)

        if self.map_can_move is False:
            if self.play_music_boss is False:
                self.mixer.music.unload()
                self.mixer.music.load(constants.BOSS_MUSIC)
                self.mixer.music.play(2, 0, 0)
                self.play_music_boss = True
                pygame.time.set_timer(self.boss_axon_attack, constants.BOSS_AXON_ATTACK_CD)
                self.boss_axon_list.add(self.boss_axon)

        if self.event_end_game is True:
            if self.boss_axon.boss_life <= 0:
                self.event_end_game = False
                pygame.time.set_timer(self.boss_defeated_end_game, 1000, 1)

    # Eventos para el menu
    def check_events_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.curr_menu.run_display = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.START_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.UP_KEY = True

    # Reseteamos los botones del menu
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    # Metodo para mostrar texto del menu
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
        self.window.blit(text_surface, text_rect)

    # Actualiza y dibuja en pantalla todos los sprites
    def update_and_draw_sprite_lists(self, delta_time):

        # Dibujamos y actualizamos las listas de sprites de Spaceship
        self.spaceship_sprite_list.update(delta_time)
        self.spaceship_sprite_list.draw(self.window)
        self.spaceship_bullet_sprite_list.update()
        self.spaceship_bullet_sprite_list.draw(self.window)

        # Dibujamos y actualizamos la lista de sprites de Enemy
        self.enemy_shooter_sprite_list.update(delta_time)
        self.enemy_shooter_sprite_list.draw(self.window)
        self.enemy_follower_sprite_list.update(delta_time)
        self.enemy_follower_sprite_list.draw(self.window)
        self.enemy_bomber_sprite_list.update(delta_time)
        self.enemy_bomber_sprite_list.draw(self.window)
        self.boss_axon_list.update(delta_time)
        self.boss_axon_list.draw(self.window)

        # Dibujamos y actualizamos balas de enemy_shooter
        self.enemy_bullet_sprite_list.update()
        self.enemy_bullet_sprite_list.draw(self.window)

        # Dibujamos y actualizamos los bonus
        self.bonus_sprite_list.update()
        self.bonus_sprite_list.draw(self.window)

        # Dibujamos y actualizamos explosión de naves enemigas
        self.explosion_sprite_list.update()
        self.explosion_sprite_list.draw(self.window)

        self.map_collision_list.update()
        self.map_collision_list.draw(self.window)

    def play_sound(self, sound_asset):
        sound = pygame.mixer.Sound(sound_asset)
        sound.play()
        sound.set_volume(constants.MUSIC_VOLUME)

    def save_highscore(self, score, data):
        json_data = self.get_highscore()
        if score > json_data[data]:
            with open(constants.SCORE_FILE_NAME, 'w') as jsonfile:
                json_data[data] = score
                json.dump(json_data, jsonfile, indent=4)

    def get_highscore(self):
        with open(constants.SCORE_FILE_NAME, "r") as json_file:
            json_data = json.load(json_file)
        return json_data



