import pygame

from utils import constants


class Sound():

    def play_sound(self, sound_asset):
        sound = pygame.mixer.Sound(sound_asset)
        sound.play()
        sound.set_volume(constants.MUSIC_VOLUME)

