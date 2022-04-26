import sys

import pygame
from pygame import mixer

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



class Game():
    def __init__(self):

        pygame.init()

        pygame.display.set_caption(constants.GAME_TITLE)
        pygame.display.set_icon(pygame.image.load(constants.GAME_ICON))

        # Variables de ejecución del juego
        self.running, self.playing = True, False

        self.game_time = Stopwatch()

        self.mixer = mixer
        self.mixer.init()
        self.mixer.music.load(constants.STAGE1_MUSIC)
        self.mixer.music.set_volume(constants.MUSIC_VOLUME)

        self.menu_music = pygame.mixer.Sound(constants.MENU_MUSIC)

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
        self.font_name_game = constants.TEXT_FONT_GAME

        #Ventana del juego
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

        # lista de enemy_bullet_sprite_list
        self.enemy_bullet_sprite_list = pygame.sprite.Group()

        # lista de explosiones
        self.explosion_sprite_list = pygame.sprite.Group()

        # lista de bonus
        self.bonus_sprite_list = pygame.sprite.Group()

        self.map_collision_list = pygame.sprite.Group()
        self.set_map_collision()

        # Background del juego
        self.background = pygame.transform.scale(pygame.image.load(constants.BACKGROUND), (constants.WIN_WIDTH, constants.WIN_HEIGHT))
        self.cueva_img = pygame.image.load("assets/cueva_720.png")


        # Inicializamos la nave del jugador
        self.player_1 = Spaceship(30, constants.WIN_HEIGHT / 2, 'player1', self)
        self.player_2 = Spaceship(30, self.player_1.rect.y + 80, 'player2', self)

        # Evento de spawn de enemy follower
        self.spawn_enemy_follower = 0

        self.scoreboard = Scoreboard(self)

        self.map_can_move = True


        '''añadir todos los eventos como variables de clase game ^'''

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

        # Posicion X de los dos backgrounds de estrellas
        bgX = 0
        bgX2 = self.background.get_width()
        cX = 0

        spawn_enemy_shooter = pygame.USEREVENT
        pygame.time.set_timer(spawn_enemy_shooter, constants.ENEMY_SPAWN_RATE)

        animate_enemy_shooter = pygame.USEREVENT + 1
        pygame.time.set_timer(animate_enemy_shooter, constants.ENEMY_ANIMATION_RATE)

        self.spawn_enemy_follower = pygame.USEREVENT + 2

        animate_enemy_follower = pygame.USEREVENT + 3
        pygame.time.set_timer(animate_enemy_follower, constants.ENEMY_FOLLOWER_ANIMATION_RATE)

        enemy_explosion = pygame.USEREVENT + 4
        pygame.time.set_timer(enemy_explosion, constants.EXPLOSION_ANIMATION_RATE)

        animate_bonus = pygame.USEREVENT + 5
        pygame.time.set_timer(animate_bonus, constants.BONUS_ANIMATE_RATE)

        bonus_speed_spawn = pygame.USEREVENT + 6
        pygame.time.set_timer(bonus_speed_spawn, constants.BONUS_SPEED_SPAWN_RATE)

        bonus_charged_shot_spawn = pygame.USEREVENT + 7
        pygame.time.set_timer(bonus_charged_shot_spawn, constants.BONUS_CHARGED_SHOT_SPAWN_RATE)

        bonus_fire_rate_spawn = pygame.USEREVENT + 8
        pygame.time.set_timer(bonus_fire_rate_spawn, constants.BONUS_FIRE_RATE_SPAWN_RATE, 3)


        while self.playing:

            delta_time = clock.tick(constants.FPS) / 1000.0

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

                if event.type == spawn_enemy_shooter:
                    enemy = Enemy(constants.WIN_WIDTH, randint(0, constants.WIN_HEIGHT), 'shooter', self)
                    self.enemy_shooter_sprite_list.add(enemy)

                if event.type == animate_enemy_shooter:
                    for enemy in self.enemy_shooter_sprite_list:
                        if enemy.current_sprite < 2:
                            enemy.current_sprite += 1
                        else:
                            enemy.current_sprite = 0

                if event.type == self.spawn_enemy_follower:
                    enemy = Enemy(constants.WIN_WIDTH, randint(0, constants.WIN_HEIGHT), 'follower', self)
                    self.enemy_follower_sprite_list.add(enemy)

                if event.type == animate_enemy_follower:
                    for enemy in self.enemy_follower_sprite_list:
                        if enemy.current_sprite < 3:
                            enemy.current_sprite += 1
                        else:
                            enemy.current_sprite = 0

                if event.type == enemy_explosion:
                    for explosion in self.explosion_sprite_list:
                        explosion.current_sprite += 1

                if event.type == animate_bonus:
                    for bonus in self.bonus_sprite_list:
                            bonus.current_sprite += 1

                if event.type == bonus_speed_spawn:
                    bonus = Bonus(constants.WIN_WIDTH, randint(60, constants.WIN_HEIGHT - 40), 'speed')
                    self.bonus_sprite_list.add(bonus)

                if event.type == bonus_charged_shot_spawn:
                    bonus = Bonus(constants.WIN_WIDTH, randint(60, constants.WIN_HEIGHT - 40), 'bullet')
                    self.bonus_sprite_list.add(bonus)

                if event.type == bonus_fire_rate_spawn:
                    bonus = Bonus(constants.WIN_WIDTH, randint(60, constants.WIN_HEIGHT - 60), 'firerate')
                    self.bonus_sprite_list.add(bonus)


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

            # Si la bala se sale de la pantalla la eliminamos
            for bullet in self.enemy_bullet_sprite_list:
                if bullet.rect.x < -20:
                    self.enemy_bullet_sprite_list.remove(bullet)

            # Si la bala se sale de la pantalla la eliminamos
            for bullet in self.spaceship_bullet_sprite_list:
                if bullet.rect.x > constants.WIN_WIDTH:
                    self.spaceship_bullet_sprite_list.remove(bullet)

            # Si la bala se sale de la pantalla la eliminamos
            for bonus in self.bonus_sprite_list:
                if bonus.rect.x < -20:
                    self.bonus_sprite_list.remove(bonus)

            enemy_shooter_hit_by_bullet = pygame.sprite.groupcollide(self.spaceship_bullet_sprite_list, self.enemy_shooter_sprite_list, False,
                                                             True)
            enemy_follower_hit_by_bullet = pygame.sprite.groupcollide(self.spaceship_bullet_sprite_list,
                                                                     self.enemy_follower_sprite_list, False,
                                                                     True)
            player_hit_by_bullet = pygame.sprite.groupcollide(self.spaceship_sprite_list, self.enemy_bullet_sprite_list, False,
                                                              True)

            player_hit_by_enemy_follower = pygame.sprite.groupcollide(self.spaceship_sprite_list, self.enemy_follower_sprite_list, False,
                                                              True)

            player_hit_by_enemy_shooter = pygame.sprite.groupcollide(self.spaceship_sprite_list, self.enemy_shooter_sprite_list, False,
                                                              True)

            player_collision_with_bonus = pygame.sprite.groupcollide(self.bonus_sprite_list, self.spaceship_sprite_list, True,
                                                              False)


            for bonus in player_collision_with_bonus:
                self.play_sound(constants.BONUS_SOUND)
                if bonus.type == 'speed':
                    for player in self.spaceship_sprite_list:
                        player.got_bonus = True
                        player.speed += 1
                        player.bonus_text = 'Speed UP'
                elif bonus.type == 'bullet':
                    for player in self.spaceship_sprite_list:
                        player.got_bonus = True
                        player.charged_shot_ammo = 20
                        player.bonus_text = 'Charged Shot ammo UP'
                elif bonus.type == 'firerate':
                    for player in self.spaceship_sprite_list:
                        player.got_bonus = True
                        player.fire_rate -= 2
                        player.bonus_text = 'Fire Rate UP'

            # cuando alcanzo al enemigo subo puntuación y animo muerte
            for hit in enemy_shooter_hit_by_bullet:
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


            for hit in enemy_follower_hit_by_bullet:
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


            if self.game_time.current_time() > 19 and self.game_time.current_time() < 19.5:
                pygame.time.set_timer(self.spawn_enemy_follower, constants.ENEMY_FOLLOWER_SPAWN_RATE)

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


            self.window.blit(self.background, (bgX, 0))  # Dibuja el primer background
            self.window.blit(self.background, (bgX2, 0))  # Dibuja el segundo background

            self.window.blit(self.cueva_img, (cX, 0))


            if cX >= constants.MAP_SIZE_DISPLACEMENT:
                cX -= constants.MAP_MOVEMENT_RATE
            else:
                self.map_can_move = False


            # Movemos ambos backgrounds a la izquierda
            bgX -= 1
            bgX2 -= 1

            # Cambiamos la posicion del background de la izq a la derecha
            if bgX < self.background.get_width() * -1:
                bgX = self.background.get_width()
            if bgX2 < self.background.get_width() * -1:
                bgX2 = self.background.get_width()


    def set_map_collision(self):
        # Techo
        self.map_collision_list.add(Map(7300, 0, pygame.Rect(0, 0, 14730, 75), self))
        self.map_collision_list.add(Map(16000, 0, pygame.Rect(0, 0, 6030, 130), self))

        # Suelo
        self.map_collision_list.add(Map(7300, 645, pygame.Rect(0, 0, 5200, 75), self))
        self.map_collision_list.add(Map(12500, 560, pygame.Rect(0, 0, 3540, 155), self))
        self.map_collision_list.add(Map(16000, 605, pygame.Rect(0, 0, 6030, 115), self))
        self.map_collision_list.add(Map(16810, 550, pygame.Rect(0, 0, 938, 170), self))


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
                if event.key == pygame.K_s:
                    self.DOWN_KEY = True
                if event.key == pygame.K_w:
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