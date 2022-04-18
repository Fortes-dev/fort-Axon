import pygame

from utils import constants


class Scoreboard():

    # Constructor
    def __init__(self, game):

        self.game = game
        self.font = pygame.font.Font(constants.TEXT_FONT_GAME, 28)

        self.life_scoreboard = 0
        self.charged_shot_scoreboard = 0
        self.score_scoreboard = 0

    def update_scoreboard_player_1(self):
        self.life_scoreboard = self.font.render(
            "VIDAS - {0}        TIEMPO - {1}".format(self.game.player.life, self.game.game_time.current_time()),
            1, self.game.WHITE)

        self.charged_shot_scoreboard = self.font.render(
            "DISPARO CARGADO - {0}".format(self.game.player.charged_shot_ammo),
            1, self.game.WHITE)

        self.score_scoreboard = self.font.render("SCORE - {0}".format(self.game.score), 1, self.game.WHITE)

    def draw_scoreboard_player_1(self):
        self.update_scoreboard_player_1()
        self.game.window.blit(self.life_scoreboard, (200, 20))
        self.game.window.blit(self.charged_shot_scoreboard, (20, constants.WIN_HEIGHT - 40))
        self.game.window.blit(self.score_scoreboard, (20, 20))





