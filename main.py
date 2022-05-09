import pygame

from models import game
from utils import constants


class Loop():
    def main(self):
        g = game.Game()
        while g.running:
            g.curr_menu.display_menu()
            g.game_loop()



if __name__ == '__main__':
    try:
        Loop().main()
    except SystemExit:
        pass
