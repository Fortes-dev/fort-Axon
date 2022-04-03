import game


class Loop():
    def main(self):
        g = game.Game()
        while g.running:
            g.curr_menu.display_menu()
            g.game_loop()


if __name__ == '__main__':
    Loop().main()
