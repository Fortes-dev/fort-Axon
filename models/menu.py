import sys

import pygame

from main import Loop
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
        self.exitx, self.exity = self.mid_w, self.mid_h + 380
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.game.menu_music.play()
        self.game.menu_music.set_volume(constants.MUSIC_VOLUME)

    def display_menu(self):

        self.run_display = True

        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('FORT AXON', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Play", 40, self.startx, self.starty)
            self.game.draw_text("Options", 40, self.optionsx, self.optionsy)
            self.game.draw_text("Controls", 40, self.creditsx, self.creditsy)
            self.game.draw_text("Exit", 40, self.exitx, self.exity)
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
                self.state = 'Controls'
            elif self.state == 'Controls':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Salir'
            elif self.state == 'Salir':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Jugar'
        elif self.game.UP_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 'Jugar':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Salir'
            elif self.state == 'Salir':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Controls'
            elif self.state == 'Controls':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Opciones'
            elif self.state == 'Opciones':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Jugar'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            self.game.play_sound(constants.MENU_SELECTION_SOUND)
            if self.state == 'Jugar':
                self.game.curr_menu = self.game.play_menu
            elif self.state == 'Opciones':
                self.game.curr_menu = self.game.options
            elif self.state == 'Controls':
                self.game.curr_menu = self.game.controls_menu
            elif self.state == 'Salir':
                self.running = False
                self.playing = False
                pygame.quit()
                sys.exit()
            self.run_display = False


class PlayMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = '1Player'
        self.one_player_x, self.one_player_y = self.mid_w, self.mid_h + 80
        self.two_player_x, self.two_player_y = self.mid_w, self.mid_h + 180

        self.cursor_rect.midtop = (self.one_player_x + self.offset, self.one_player_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Play', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("1 Player", 35, self.one_player_x, self.one_player_y)
            self.game.draw_text("2 Players", 35, self.two_player_x, self.two_player_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.play_sound(constants.MENU_BACK_SOUND)
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            self.game.menu_music.stop()
            self.game.playing = True
            self.game.game_time.reset_timer()
            self.game.mixer.music.play(0, 0, 0)
            if self.state == '1Player':
                self.game.multiplayer = False
            elif self.state == '2Players':
                self.game.multiplayer = True
            self.run_display = False

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == '1Player':
                self.cursor_rect.midtop = (self.two_player_x + self.offset, self.two_player_y)
                self.state = '2Players'
            elif self.state == '2Players':
                self.cursor_rect.midtop = (self.one_player_x + self.offset, self.one_player_y)
                self.state = '1Player'


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volumen'
        self.volx, self.voly = self.mid_w, self.mid_h + 80
        self.videox, self.videoy = self.mid_w, self.mid_h + 180
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Options', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Volume", 40, self.volx, self.voly)
            self.game.draw_text("Graphics", 40, self.videox, self.videoy)
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
            elif self.state == 'Video':
                self.game.curr_menu = self.game.video_menu
                self.run_display = False

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 'Volumen':
                self.cursor_rect.midtop = (self.videox + self.offset, self.videoy)
                self.state = 'Video'
            elif self.state == 'Video':
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = 'Volumen'


class VolumenMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 2
        self.volumen_0_x, self.volumen_0_y = self.mid_w, self.mid_h + 80
        self.volumen_1_x, self.volumen_1_y = self.mid_w, self.mid_h + 180
        self.volumen_2_x, self.volumen_2_y = self.mid_w, self.mid_h + 280
        self.volumen_3_x, self.volumen_3_y = self.mid_w, self.mid_h + 380

        self.cursor_rect.midtop = (self.volumen_2_x + self.offset, self.volumen_2_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Volume', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
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
                self.set_volume(0.08)
            elif self.state == 2:
                self.set_volume(0.18)
            elif self.state == 3:
                self.set_volume(0.38)
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


class VideoMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'fullscreen'
        self.video_windowed_x, self.video_windowed_y = self.mid_w, self.mid_h + 80
        self.video_fullscreen_x, self.video_fullscreen_y = self.mid_w, self.mid_h + 180

        self.cursor_rect.midtop = (self.video_fullscreen_x + self.offset, self.video_fullscreen_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Graphics', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Windowed", 35, self.video_windowed_x, self.video_windowed_y)
            self.game.draw_text("Fullscreen", 35, self.video_fullscreen_x, self.video_fullscreen_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.play_sound(constants.MENU_BACK_SOUND)
            self.game.curr_menu = self.game.options
            self.run_display = False
        elif self.game.START_KEY:
            if self.state == 'windowed':
                constants.WINDOW_MODE = 'windowed'
                self.game.menu_music.stop()
                Loop().main()


            elif self.state == 'fullscreen':
                constants.WINDOW_MODE = 'fullscreen'
                self.game.menu_music.stop()
                Loop().main()

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 'windowed':
                self.cursor_rect.midtop = (self.video_fullscreen_x + self.offset, self.video_fullscreen_y)
                self.state = 'fullscreen'
            elif self.state == 'fullscreen':
                self.cursor_rect.midtop = (self.video_windowed_x + self.offset, self.video_windowed_y)
                self.state = 'windowed'


class ControlsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Player1'
        self.player1x, self.player1y = self.mid_w, self.mid_h + 80
        self.player2x, self.player2y = self.mid_w, self.mid_h + 180

        self.cursor_rect.midtop = (self.player1x + self.offset, self.player1y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Controls', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Player 1", 40, self.player1x, self.player1y)
            self.game.draw_text("Player 2", 40, self.player2x, self.player2y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.play_sound(constants.MENU_BACK_SOUND)
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            if self.state == 'Player1':
                self.game.curr_menu = self.game.controls_player1_menu
                self.run_display = False
            elif self.state == 'Player2':
                self.game.curr_menu = self.game.controls_player2_menu
                self.run_display = False
            self.game.play_sound(constants.MENU_SELECTION_SOUND)

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 'Player1':
                self.cursor_rect.midtop = (self.player2x + self.offset, self.player2y)
                self.state = 'Player2'
            elif self.state == 'Player2':
                self.cursor_rect.midtop = (self.player1x + self.offset, self.player1y)
                self.state = 'Player1'


class ControlsPlayer1Menu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.namex, self.namey = self.mid_w - 100, self.mid_h + 40
        self.descx, self.descy = self.mid_w + 100, self.mid_h + 40
        self.ax, self.by = self.mid_w, self.mid_h + 120

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Player 1', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 300)
            self.game.draw_text('Movement', 40, self.mid_w, self.mid_h - 100)
            self.game.draw_text('W  *  Up', 20, self.mid_w - 150, self.mid_h - 20)
            self.game.draw_text('A  *  Left', 20, self.mid_w + 150, self.mid_h - 20)
            self.game.draw_text('S  *  Down', 20, self.mid_w - 150, self.mid_h + 20)
            self.game.draw_text('D  *  Right', 20, self.mid_w + 150, self.mid_h + 20)
            self.game.draw_text('Shoot', 40, self.mid_w, self.mid_h + 100)
            self.game.draw_text('Espace  *  Shoot', 20, self.mid_w, self.mid_h + 160)
            self.game.draw_text('Left CTRL  *  Charged Shot', 20, self.mid_w, self.mid_h + 200)
            self.game.draw_text('Menu', 40, self.mid_w, self.mid_h + 260)
            self.game.draw_text('ESC  *  Pause and back', 20, self.mid_w, self.mid_h + 320)
            self.game.draw_text('Space and Enter  *  Select', 20, self.mid_w, self.mid_h + 360)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.play_sound(constants.MENU_BACK_SOUND)
            self.game.curr_menu = self.game.controls_menu
            self.run_display = False


class ControlsPlayer2Menu(Menu):
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
            self.game.draw_text('Player 2', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 300)
            self.game.draw_text('Movement', 40, self.mid_w, self.mid_h - 100)
            self.game.draw_text('Arrow up  *  Up', 20, self.mid_w - 250, self.mid_h - 20)
            self.game.draw_text('Arrow left  *  Left', 20, self.mid_w + 250, self.mid_h - 20)
            self.game.draw_text('Arrow down  *  Down', 20, self.mid_w - 250, self.mid_h + 20)
            self.game.draw_text('Arrow right  *  Right', 20, self.mid_w + 250, self.mid_h + 20)
            self.game.draw_text('Shoot', 40, self.mid_w, self.mid_h + 100)
            self.game.draw_text('Right SHIFT  *  Shoot', 20, self.mid_w, self.mid_h + 160)
            self.game.draw_text('Right CTRL  *  Charged shot', 20, self.mid_w, self.mid_h + 200)
            self.game.draw_text('Menu', 40, self.mid_w, self.mid_h + 260)
            self.game.draw_text('ESC  *  Pause and back', 20, self.mid_w, self.mid_h + 320)
            self.game.draw_text('Space and Enter  *  Select', 20, self.mid_w, self.mid_h + 360)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.play_sound(constants.MENU_BACK_SOUND)
            self.game.curr_menu = self.game.controls_menu
            self.run_display = False


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.namex, self.namey = self.mid_w, self.mid_h
        self.descx, self.descy = self.mid_w, self.mid_h + 80
        self.thax, self.thay = self.mid_w, self.mid_h + 180

    def display_menu(self):
        self.game.mixer.music.stop()
        self.game.end_game_music.play()
        self.game.end_game_music.set_volume(constants.MUSIC_VOLUME)
        self.run_display = True
        while self.run_display:
            self.game.check_events_menu()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 250)
            self.game.draw_text('Carlos Fortes Medina', 30, self.namex, self.namey)
            self.game.draw_text('Final Degree Project', 30, self.descx, self.descy)
            self.game.draw_text('X  Thanks for playing  X', 40, self.thax, self.thay)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.START_KEY:
            self.game.play_sound(constants.MENU_SELECTION_SOUND)
            self.game.curr_menu = self.game.game_over
            self.run_display = False


class GameOverMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True

        self.game.mixer.music.stop()
        game_over_music = Sound()

        self.game.game_time.reset_timer()
        self.game.display.fill(self.game.BLACK)
        self.game.draw_text('GAME OVER', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
        self.game.draw_text('Press ENTER or ESPACE to return to main menu', 22, self.game.DISPLAY_W / 2,
                            self.game.DISPLAY_H / 2 + 250)

        if self.game.boss_axon.boss_life > 0:
            game_over_music.play_sound(constants.GAME_OVER_MUSIC)
        if self.game.multiplayer:
            self.game.save_highscore(self.game.player_1.score, constants.MULTI_SCORE_P1)
            self.game.save_highscore(self.game.player_2.score, constants.MULTI_SCORE_P2)
        else:
            self.game.save_highscore(self.game.player_1.score, constants.SOLO_SCORE_DATA)

        self.score_json_data = self.game.get_highscore()

        if self.game.multiplayer:
            self.game.draw_text('Player 1 score  x  ' + str(self.game.player_1.score) + '   BEST SCORE  x  ' + str(self.score_json_data[constants.MULTI_SCORE_P1]), 26, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text('Player 2 score  x  ' + str(self.game.player_2.score) + '   BEST SCORE  x  ' + str(self.score_json_data[constants.MULTI_SCORE_P2]), 26, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 + 50)
        else:
            self.game.draw_text('Player score  x  ' + str(self.game.player_1.score) + '   BEST SCORE  x  ' + str(self.score_json_data[constants.SOLO_SCORE_DATA]), 26, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2)

        self.blit_screen()
        pygame.time.wait(2500)

        while self.run_display:
            self.game.check_events_menu()
            if self.game.START_KEY:
                self.game.end_game_music.stop()
                self.game.play_sound(constants.MENU_SELECTION_SOUND)
                Loop().main()


class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Continue"
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
            self.game.draw_text('Pause', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Continue", 40, self.continuarx, self.continuary)
            self.game.draw_text("Exit", 40, self.quit_gamex, self.quit_gamey)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.UP_KEY or self.game.DOWN_KEY:
            self.game.play_sound(constants.MENU_MOVEMENT_SOUND)
            if self.state == 'Continue':
                self.state = 'QuitGame'
                self.cursor_rect.midtop = (self.quit_gamex + self.offset, self.quit_gamey)
            elif self.state == 'QuitGame':
                self.state = 'Continue'
                self.cursor_rect.midtop = (self.continuarx + self.offset, self.continuary)

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            self.game.play_sound(constants.MENU_SELECTION_SOUND)
            if self.state == 'Continue':
                pygame.time.delay(50)
                self.game.playing = True
                self.game.mixer.music.unpause()
                self.game.game_time.unpause_time()

            elif self.state == 'QuitGame':
                pygame.time.delay(100)
                pygame.time.set_timer(self.game.spawn_enemy_follower, 0, False)
                Loop().main()

            self.run_display = False
