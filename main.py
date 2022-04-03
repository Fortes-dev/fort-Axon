from models.game import Game

g = Game()

while g.running:
    g.curr_menu.display_menu()

    if(g.playing):
        g.game_loop()