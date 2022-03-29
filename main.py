import pygame

from models.Spaceship import Spaceship
from utils import constants


# Ventana del juego
pygame.display.set_caption(constants.GAME_TITLE)
pygame.display.set_icon(pygame.image.load(constants.GAME_ICON))
WINDOW = pygame.display.set_mode((constants.WIN_WIDTH, constants.WIN_HEIGHT))
BACKGROUND = pygame.image.load(constants.BACKGROUND)
BACKGROUND = pygame.transform.scale(BACKGROUND, (1920, 1080))



def main():

    # Inicializamos pygame
    pygame.init()

    pygame.display.set_caption(constants.GAME_TITLE)
    pygame.display.set_icon(pygame.image.load(constants.GAME_ICON))

    # Inicializamos Spaceship
    spaceship = Spaceship(30, constants.WIN_HEIGHT / 2)
    spaceship.rect.x = 30
    spaceship.rect.y = constants.WIN_HEIGHT / 2


    # lista de spaceship_sprite_list
    spaceship_sprite_list = pygame.sprite.Group()
    spaceship_sprite_list.add(spaceship)

    # lista de bullet_sprite_list
    bullet_sprite_list = pygame.sprite.Group()

    # Reloj interno del juego
    clock = pygame.time.Clock()
    run = True

    # Posicion X de los dos backgrounds de estrellas
    bgX = 0
    bgX2 = BACKGROUND.get_width()

    # MS Actual de este loop
    global current_time_loop
    current_time_loop = pygame.time.get_ticks()

    # Bucle (comienza el juego)
    while run:


        delta_time = clock.tick(constants.FPS)/1000.0

        WINDOW.blit(BACKGROUND, (bgX, 0))  # Dibuja el primer background
        WINDOW.blit(BACKGROUND, (bgX2, 0))  # Dibuja el segundo background

        # Movemos ambos backgrounds a la izquierda
        bgX -= 2
        bgX2 -= 2

        # Cambiamos la posicion del background de la izq a la derecha
        if bgX < BACKGROUND.get_width() * -1:
            bgX = BACKGROUND.get_width()
        if bgX2 < BACKGROUND.get_width() * -1:
            bgX2 = BACKGROUND.get_width()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_pressed = pygame.key.get_pressed()
        spaceship.move_spaceship(key_pressed)
        spaceship.shoot_bullet(key_pressed, bullet_sprite_list)


        for bullet in bullet_sprite_list:
            if bullet.rect.x > constants.WIN_WIDTH:
                bullet_sprite_list.remove(bullet)

        # Dibujamos y actualizamos las listas de sprites
        bullet_sprite_list.draw(WINDOW)
        bullet_sprite_list.update()
        spaceship_sprite_list.update(delta_time)
        spaceship_sprite_list.draw(WINDOW)

        # Actualizamos la ventana
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()