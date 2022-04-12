import pygame
from pygame import mixer

from main import Loop
from models.spaceship import Spaceship
from utils import constants
from utils.sound_func import Sound


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 200




    def draw_cursor(self):
        self.game.draw_text('[', 40, self.cursor_rect.x, self.cursor_rect.y)

        # Le ponemos + 410 de offset a la derecha para alinearlo con el otro cursor
        self.game.draw_text(']', 40, self.cursor_rect.x + 410, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Jugar"
        self.startx, self.starty = self.mid_w, self.mid_h + 80
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 180
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 280
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.game.menu_music.play()
        self.game.menu_music.set_volume(constants.MUSIC_VOLUME)



    def display_menu(self):

        self.run_display = True

        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('FORT AXON', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 300)
            self.game.draw_text("Jugar", 40, self.startx, self.starty)
            self.game.draw_text("Opciones", 40, self.optionsx, self.optionsy)
            self.game.draw_text("Creditos", 40, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()




    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 'Jugar':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Opciones'
            elif self.state == 'Opciones':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Creditos'
            elif self.state == 'Creditos':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Jugar'
        elif self.game.UP_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 'Jugar':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Creditos'
            elif self.state == 'Opciones':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Jugar'
            elif self.state == 'Creditos':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Opciones'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            self.game.play_sound(constants.MENU_SELECTION_SOUND)
            if self.state == 'Jugar':
                self.game.menu_music.stop()
                self.game.playing = True
                self.game.game_time.reset_timer()
                self.game.mixer.music.play(5, 0.0, 1000)
            elif self.state == 'Opciones':
                self.game.curr_menu = self.game.options
            elif self.state == 'Creditos':
                self.game.curr_menu = self.game.credits
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volumen'
        self.volx, self.voly = self.mid_w, self.mid_h + 80
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 180
        self.videox, self.videoy = self.mid_w, self.mid_h + 280
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Opciones', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 300)
            self.game.draw_text("Volumen", 40, self.volx, self.voly)
            self.game.draw_text("Controles", 40, self.controlsx, self.controlsy)
            self.game.draw_text("Video", 40, self.videox, self.videoy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.play_sound(constants.MENU_BACK_SOUND)
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            self.game.play_sound(constants.MENU_SELECTION_SOUND)
            if self.state == 'Volumen':
                self.game.curr_menu = self.game.volumen_menu
                self.run_display = False
            elif self.state == 'Controles':
                pass
            elif self.state == 'Video':
                pass

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 'Volumen':
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = 'Controles'
            elif self.state == 'Controles':
                self.cursor_rect.midtop = (self.videox + self.offset, self.videoy)
                self.state = 'Video'
            elif self.state == 'Video':
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = 'Volumen'
        elif self.game.UP_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 'Volumen':
                self.cursor_rect.midtop = (self.videox + self.offset, self.videoy)
                self.state = 'Video'
            elif self.state == 'Video':
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = 'Controles'
            elif self.state == 'Controles':
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = 'Volumen'


class VolumenMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 1
        self.volumen_0_x, self.volumen_0_y = self.mid_w, self.mid_h + 80
        self.volumen_1_x, self.volumen_1_y = self.mid_w, self.mid_h + 180
        self.volumen_2_x, self.volumen_2_y = self.mid_w, self.mid_h + 280
        self.volumen_3_x, self.volumen_3_y = self.mid_w, self.mid_h + 380

        self.cursor_rect.midtop = (self.volumen_1_x + self.offset, self.volumen_1_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Volumen', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 300)
            self.game.draw_text("0", 40, self.volumen_0_x, self.volumen_0_y)
            self.game.draw_text("1", 40, self.volumen_1_x, self.volumen_1_y)
            self.game.draw_text("2", 40, self.volumen_2_x, self.volumen_2_y)
            self.game.draw_text("3", 40, self.volumen_3_x, self.volumen_3_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.play_sound(constants.MENU_BACK_SOUND)
            self.game.curr_menu = self.game.options
            self.run_display = False
        elif self.game.START_KEY:
            if self.state == 0:
                self.set_volume(0)
            elif self.state == 1:
                self.set_volume(0.15)
            elif self.state == 2:
                self.set_volume(0.45)
            elif self.state == 3:
                self.set_volume(0.75)
            self.game.play_sound(constants.MENU_SELECTION_SOUND)

    def set_volume(self, value):
        constants.MUSIC_VOLUME = value
        self.game.mixer.music.set_volume(value)
        self.game.menu_music.set_volume(value)

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 0:
                self.cursor_rect.midtop = (self.volumen_1_x + self.offset, self.volumen_1_y)
                self.state = 1
            elif self.state == 1:
                self.cursor_rect.midtop = (self.volumen_2_x + self.offset, self.volumen_2_y)
                self.state = 2
            elif self.state == 2:
                self.cursor_rect.midtop = (self.volumen_3_x + self.offset, self.volumen_3_y)
                self.state = 3
            elif self.state == 3:
                self.cursor_rect.midtop = (self.volumen_0_x + self.offset, self.volumen_0_y)
                self.state = 0
        elif self.game.UP_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 0:
                self.cursor_rect.midtop = (self.volumen_3_x + self.offset, self.volumen_3_y)
                self.state = 3
            elif self.state == 3:
                self.cursor_rect.midtop = (self.volumen_2_x + self.offset, self.volumen_2_y)
                self.state = 2
            elif self.state == 2:
                self.cursor_rect.midtop = (self.volumen_1_x + self.offset, self.volumen_1_y)
                self.state = 1
            elif self.state == 1:
                self.cursor_rect.midtop = (self.volumen_0_x + self.offset, self.volumen_0_y)
                self.state = 0


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.namex, self.namey = self.mid_w, self.mid_h + 80
        self.descx, self.descy = self.mid_w, self.mid_h + 180

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Creditos', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 300)
            self.game.draw_text('Carlos Fortes Medina', 40, self.namex, self.namey)
            self.game.draw_text('Proyecto fin de Grado', 40, self.descx, self.descy)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.play_sound(constants.MENU_BACK_SOUND)
            self.game.curr_menu = self.game.main_menu
            self.run_display = False


class GameOverMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        self.game.mixer.music.stop()
        game_over_music = Sound()
        game_over_music.play_sound(constants.GAME_OVER_MUSIC)
        self.game.game_time.reset_timer()
        self.game.display.fill(self.game.BLACK)
        self.game.draw_text('GAME OVER', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 60)
        self.game.draw_text('Presiona ENTER o ESPACIO para volver al menu', 24, self.game.DISPLAY_W / 2,
                            self.game.DISPLAY_H / 2 + 120)
        self.blit_screen()
        pygame.time.wait(2500)

        while self.run_display:
            self.game.check_events_menu()
            if self.game.START_KEY:
                self.game.play_sound(constants.MENU_SELECTION_SOUND)
                Loop().main()


class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Continuar"
        self.continuarx, self.continuary = self.mid_w, self.mid_h + 80
        self.quit_gamex, self.quit_gamey = self.mid_w, self.mid_h + 180
        self.cursor_rect.midtop = (self.continuarx + self.offset, self.continuary)


    def display_menu(self):
        self.run_display = True
        self.game.play_sound(constants.PAUSE_SOUND)
        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Pausa', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 300)
            self.game.draw_text("Continuar", 40, self.continuarx, self.continuary)
            self.game.draw_text("Salir", 40, self.quit_gamex, self.quit_gamey)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.UP_KEY or self.game.DOWN_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 'Continuar':
                self.state = 'QuitGame'
                self.cursor_rect.midtop = (self.quit_gamex + self.offset, self.quit_gamey)
            elif self.state == 'QuitGame':
                self.state = 'Continuar'
                self.cursor_rect.midtop = (self.continuarx + self.offset, self.continuary)

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            self.game.play_sound(constants.MENU_SELECTION_SOUND)
            if self.state == 'Continuar':
                pygame.time.delay(50)
                self.game.playing = True
                self.game.mixer.music.unpause()
                self.game.game_time.unpause_time()
            elif self.state == 'QuitGame':
                pygame.time.delay(100)
                pygame.time.set_timer(self.game.spawn_enemy_follower, 0, False)
                Loop().main()

            self.run_display = False