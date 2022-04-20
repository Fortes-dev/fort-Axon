'''import pygame
from pytmx.util_pygame import load_pygame
import pyscroll

from utils import constants


class RenderMap():
    def __init__(self, game):
        self.map = load_pygame("assets/tileMap.tmx")
        self.game = game
        self.map_x = 0
        self.map_y = 0

        self.map_layer = 0

        self.group = 0

    def render_map(self, offset_x):
        for layer in self.map.visible_layers:
            for x, y, gid, in layer:
                self.map_x = x * self.map.tilewidth + offset_x
                self.map_y = y * self.map.tileheight
                tile = self.map.get_tile_image_by_gid(gid)
                self.game.window.blit(tile, (self.map_x, self.map_y))


    def render_map_scroll(self):
        self.map_layer = pyscroll.BufferedRenderer(pyscroll.TiledMapData(self.map), (self.game.DISPLAY_W, self.game.DISPLAY_H))

        self.group = pyscroll.PyscrollGroup(self.map_layer)
        self.group.draw(self.game.window)'''
