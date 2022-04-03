import pygame

from models.menu import MainMenu, OptionsMenu, CreditsMenu, PauseMenu
from utils import constants
from random import randint
from models.enemy import Enemy
from models.explosion import Explosion
from models.spaceship import Spaceship



class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(constants.GAME_TITLE)
        pygame.display.set_icon(pygame.image.load(constants.GAME_ICON))

        # Variables de ejecución del juego
        self.running, self.playing = True, False

        # Variables booleanas de botones del menu
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

        # Ancho y alto de la pantalla
        self.DISPLAY_W, self.DISPLAY_H = constants.WIN_WIDTH, constants.WIN_HEIGHT

        # Variable de pantalla
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))

        self.font_name = constants.TEXT_FONT

        #Ventana del juego
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        # Variables de los menus
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.pause = PauseMenu(self)
        self.curr_menu = self.main_menu

        # Puntuacion del jugador
        self.score = 0

        # Inicializamos la nave del jugador
        self.player = Spaceship(30, constants.WIN_HEIGHT / 2)

        # Inicializamos las listas de sprites
        self.spaceship_sprite_list = pygame.sprite.Group()

        # lista de spaceship_bullet_sprite_list
        self.spaceship_bullet_sprite_list = pygame.sprite.Group()

        # lista de enemy_sprite_list
        self.enemy_sprite_list = pygame.sprite.Group()

        # lista de enemy_bullet_sprite_list
        self.enemy_bullet_sprite_list = pygame.sprite.Group()

        # lista de explosiones
        self.explosion_sprite_list = pygame.sprite.Group()

        # Background del juego
        self.background = pygame.transform.scale(pygame.image.load(constants.BACKGROUND), (constants.WIN_WIDTH, constants.WIN_HEIGHT))


    # Loop de juego
    def game_loop(self):

        # Situamos al jugador en la pantalla
        self.player.rect.x = 30
        self.player.rect.y = constants.WIN_HEIGHT / 2

        fuente = pygame.font.Font(constants.TEXT_FONT, 20)

        # lista de spaceship_sprite_list
        self.spaceship_sprite_list.add(self.player)

        # Reloj interno del juego
        clock = pygame.time.Clock()

        # Posicion X de los dos backgrounds de estrellas
        bgX = 0
        bgX2 = self.background.get_width()

        spawn_enemy = pygame.USEREVENT
        pygame.time.set_timer(spawn_enemy, constants.ENEMY_SPAWN_RATE)

        animate_enemy = pygame.USEREVENT + 1
        pygame.time.set_timer(animate_enemy, constants.ENEMY_ANIMATION_RATE)

        enemy_explosion = pygame.USEREVENT + 2
        pygame.time.set_timer(enemy_explosion, constants.EXPLOSION_ANIMATION_RATE)

        while self.playing:

            delta_time = clock.tick(constants.FPS) / 1000.0

            # Eventos del juego
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.curr_menu = self.pause
                        self.playing = False
                if event.type == spawn_enemy:
                    enemy = Enemy(constants.WIN_WIDTH, randint(0, constants.WIN_HEIGHT))
                    self.enemy_sprite_list.add(enemy)
                if event.type == animate_enemy:
                    for enemy in self.enemy_sprite_list:
                        if enemy.current_sprite < 2:
                            enemy.current_sprite += 1
                        else:
                            enemy.current_sprite = 0
                if event.type == enemy_explosion:
                    for explosion in self.explosion_sprite_list:
                        explosion.current_sprite += 1

            self.window.blit(self.background, (bgX, 0))  # Dibuja el primer background
            self.window.blit(self.background, (bgX2, 0))  # Dibuja el segundo background

            # Movemos ambos backgrounds a la izquierda
            bgX -= 2
            bgX2 -= 2

            # Cambiamos la posicion del background de la izq a la derecha
            if bgX < self.background.get_width() * -1:
                bgX = self.background.get_width()
            if bgX2 < self.background.get_width() * -1:
                bgX2 = self.background.get_width()

            key_pressed = pygame.key.get_pressed()
            self.player.move_spaceship(key_pressed)
            self.player.shoot_bullet(key_pressed, self.spaceship_bullet_sprite_list)

            # Si el enemigo se sale de la pantalla lo eliminamos
            for enemy in self.enemy_sprite_list:
                if enemy.rect.x < -10:
                    self.enemy_sprite_list.remove(enemy)
                else:
                    enemy.shoot_bullet(self.enemy_bullet_sprite_list)

            # Si la bala se sale de la pantalla la eliminamos
            for bullet in self.enemy_bullet_sprite_list:
                if bullet.rect.x < -10:
                    self.enemy_bullet_sprite_list.remove(bullet)

            # Si la bala se sale de la pantalla la eliminamos
            for bullet in self.spaceship_bullet_sprite_list:
                if bullet.rect.x > constants.WIN_WIDTH:
                    self.spaceship_bullet_sprite_list.remove(bullet)

            enemy_hit_by_bullet = pygame.sprite.groupcollide(self.spaceship_bullet_sprite_list, self.enemy_sprite_list, True,
                                                             True)
            player_hit_by_bullet = pygame.sprite.groupcollide(self.enemy_bullet_sprite_list, self.spaceship_sprite_list, True,
                                                              False)

            # if player is hit
            for hit in enemy_hit_by_bullet:
                x = hit.rect.x - 135
                y = hit.rect.y - 135
                explosion = Explosion(x, y)
                self.explosion_sprite_list.add(explosion)
                self.score += 1

            # Dibujamos el score
            scoretext = fuente.render("Score {0}".format(self.score), 1, (255, 255, 255))
            self.window.blit(scoretext, (5, 10))

            # Dibujamos la vida
            vidatext = fuente.render("Vidas {0}".format(self.player.life), 1, (255, 255, 255))
            self.window.blit(vidatext, (150, 10))

            for hit in player_hit_by_bullet:
                self.player.life -= 1
            if self.player.life == 0:
                self.playing = False
                self.curr_menu = self.credits

            # Actualizamos todas las listas de sprites
            self.update_and_draw_sprite_lists(delta_time)

            # Actualizamos la ventana
            pygame.display.update()
            self.reset_keys()

    # Eventos para el menu
    def check_events_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                pygame.quit()
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

    # Actualiza y dibuja en pantalla todos los sprites
    def update_and_draw_sprite_lists(self, delta_time):

        # Dibujamos y actualizamos las listas de sprites de Spaceship
        self.spaceship_sprite_list.update(delta_time)
        self.spaceship_sprite_list.draw(self.window)
        self.spaceship_bullet_sprite_list.update(0)
        self.spaceship_bullet_sprite_list.draw(self.window)

        # Dibujamos y actualizamos la lista de sprites de Enemy
        self.enemy_sprite_list.update(delta_time)
        self.enemy_sprite_list.draw(self.window)
        self.enemy_bullet_sprite_list.update(1)
        self.enemy_bullet_sprite_list.draw(self.window)

        # Dibujamos y actualizamos explosión de naves enemigas
        self.explosion_sprite_list.update()
        self.explosion_sprite_list.draw(self.window)