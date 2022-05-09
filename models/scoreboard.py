import pygame

from utils import constants


class Scoreboard():

    # Constructor
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(constants.TEXT_FONT_GAME, 28)

        self.player1_life = Life('player1')
        self.player2_life = Life('player2')

        self.player1_scoreboard = Score('player1')
        self.player2_scoreboard = Score('player2')

        self.player1_charged_shot = ChargedShot('player1')
        self.player2_charged_shot = ChargedShot('player2')

        self.timer = Timer()

    def draw_scoreboard_player_1(self, life):
        self.game.window.blit(self.font.render("{0}".format(self.game.player_1.score), 1, self.game.WHITE), (275, 30))
        self.game.window.blit(
            self.font.render(" x {0}".format(self.game.player_1.charged_shot_ammo), 1, self.game.WHITE), (545, 30))
        self.game.window.blit(self.font.render("{0}".format(self.game.game_time.current_time()), 1, self.game.WHITE),
                              (self.game.DISPLAY_W - 130, 30))

        self.game.window.blit(self.player1_life.sprites[life], (20, 10))
        self.game.window.blit(self.player1_scoreboard.get_score(), (250, 10))
        self.game.window.blit(self.player1_charged_shot.get_charged_shot(), (490, 30))

        self.game.window.blit(self.timer.get_timer(), (self.game.DISPLAY_W - 200, 15))

    def draw_scoreboard_player_2(self, life):
        self.game.window.blit(self.font.render("{0}".format(self.game.player_2.score), 1, self.game.WHITE),
                              (275, self.game.DISPLAY_H - 50))
        self.game.window.blit(
            self.font.render(" x {0}".format(self.game.player_2.charged_shot_ammo), 1, self.game.WHITE),
            (545, self.game.DISPLAY_H - 50))

        self.game.window.blit(self.player2_life.sprites[life], (20, self.game.DISPLAY_H - 70))
        self.game.window.blit(self.player2_scoreboard.get_score(), (250, self.game.DISPLAY_H - 70))
        self.game.window.blit(self.player2_charged_shot.get_charged_shot(), (490, self.game.DISPLAY_H - 50))


class Life(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, player):
        super().__init__()

        if player == 'player1':
            imagen_life_0 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER1_HEALTHBAR_0), 0, 0.3)
            imagen_life_0.convert()

            imagen_life_1 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER1_HEALTHBAR_1), 0, 0.3)
            imagen_life_1.convert()

            imagen_life_2 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER1_HEALTHBAR_2), 0, 0.3)
            imagen_life_2.convert()

            imagen_life_3 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER1_HEALTHBAR_3), 0, 0.3)
            imagen_life_3.convert()

            imagen_life_4 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER1_HEALTHBAR_4), 0, 0.3)
            imagen_life_4.convert()

            imagen_life_5 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER1_HEALTHBAR_5), 0, 0.3)
            imagen_life_5.convert()

        elif player == 'player2':
            imagen_life_0 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER2_HEALTHBAR_0), 0, 0.3)
            imagen_life_0.convert()

            imagen_life_1 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER2_HEALTHBAR_1), 0, 0.3)
            imagen_life_1.convert()

            imagen_life_2 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER2_HEALTHBAR_2), 0, 0.3)
            imagen_life_2.convert()

            imagen_life_3 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER2_HEALTHBAR_3), 0, 0.3)
            imagen_life_3.convert()

            imagen_life_4 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER2_HEALTHBAR_4), 0, 0.3)
            imagen_life_4.convert()

            imagen_life_5 = pygame.transform.rotozoom(pygame.image.load(constants.PLAYER2_HEALTHBAR_5), 0, 0.3)
            imagen_life_5.convert()

        # Inicializamos array de sprites y añadimos todos
        self.sprites = []
        self.sprites.append(imagen_life_0)
        self.sprites.append(imagen_life_1)
        self.sprites.append(imagen_life_2)
        self.sprites.append(imagen_life_3)
        self.sprites.append(imagen_life_4)
        self.sprites.append(imagen_life_5)

        self.current_sprite = 5

        # Seteamos la imagen actual del sprite
        self.image = self.sprites[self.current_sprite]

    def update(self):
        self.image = self.sprites[self.current_sprite]


class Timer(pygame.sprite.Sprite):

    # Constructor
    def __init__(self):
        super().__init__()

        self.timer = pygame.transform.rotozoom(pygame.image.load(constants.TIMER), 0, 0.26)
        self.timer.convert()

    def get_timer(self):
        return self.timer


class Score(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, player):
        super().__init__()

        if player == 'player1':
            img = self.set_score_img(constants.PLAYER1_SCOREBOARD)
            img.convert()
        elif player == 'player2':
            img = self.set_score_img(constants.PLAYER2_SCOREBOARD)
            img.convert()

        self.score = img

    def get_score(self):
        return self.score

    def set_score_img(self, asset):
        return pygame.transform.rotozoom(pygame.image.load(asset), 0, 0.3)


class ChargedShot(pygame.sprite.Sprite):

    # Constructor
    def __init__(self, player):
        super().__init__()

        if player == 'player1':
            img = self.set_charged_shot_img(constants.PLAYER1_CHARGEDSHOT_AMMO)
            img.convert()
        elif player == 'player2':
            img = self.set_charged_shot_img(constants.PLAYER2_CHARGEDSHOT_AMMO)
            img.convert()

        self.charged_shot = img

    def get_charged_shot(self):
        return self.charged_shot

    def set_charged_shot_img(self, asset):
        return pygame.transform.rotozoom(pygame.image.load(asset), 0, 0.8)
