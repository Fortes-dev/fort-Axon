from random import randint

import pygame

from models.Enemy import Enemy
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

    # Inicializamos score
    score = 0

    fuente = pygame.font.SysFont("monospace", 28, True)


    # lista de spaceship_sprite_list
    spaceship_sprite_list = pygame.sprite.Group()
    spaceship_sprite_list.add(spaceship)

    # lista de spaceship_bullet_sprite_list
    spaceship_bullet_sprite_list = pygame.sprite.Group()

    # lista de enemy_sprite_list
    enemy_sprite_list = pygame.sprite.Group()

    # lista de enemy_bullet_sprite_list
    enemy_bullet_sprite_list = pygame.sprite.Group()

    # Reloj interno del juego
    clock = pygame.time.Clock()
    run = True

    # Posicion X de los dos backgrounds de estrellas
    bgX = 0
    bgX2 = BACKGROUND.get_width()

    SPAWNENEMY = pygame.USEREVENT
    pygame.time.set_timer(SPAWNENEMY, 1500)

    ANIMATE_ENEMY = pygame.NUMEVENTS
    pygame.time.set_timer(ANIMATE_ENEMY, 150)

    # Bucle (comienza el juego)
    while run:

        delta_time = clock.tick(constants.FPS)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == SPAWNENEMY:
                enemy = Enemy(constants.WIN_WIDTH, randint(40, constants.WIN_HEIGHT - 80))
                enemy_sprite_list.add(enemy)
            if event.type == ANIMATE_ENEMY:
                for enemy in enemy_sprite_list:
                    if enemy.current_sprite < 2:
                        enemy.current_sprite += 1
                    else:
                        enemy.current_sprite = 0


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

        key_pressed = pygame.key.get_pressed()
        spaceship.move_spaceship(key_pressed)
        spaceship.shoot_bullet(key_pressed, spaceship_bullet_sprite_list)

        # Si el enemigo se sale de la pantalla lo eliminamos
        for enemy in enemy_sprite_list:
            if enemy.rect.x < -10:
                enemy_sprite_list.remove(enemy)

            else:
                enemy.shoot_bullet(enemy_bullet_sprite_list)

        for bullet in enemy_bullet_sprite_list:
            if bullet.rect.x < -10:
                enemy_bullet_sprite_list.remove(bullet)

        # Si la bala se sale de la pantalla la eliminamos
        for bullet in spaceship_bullet_sprite_list:
            if bullet.rect.x > constants.WIN_WIDTH:
                spaceship_bullet_sprite_list.remove(bullet)

        enemy_hit_by_bullet = pygame.sprite.groupcollide(spaceship_bullet_sprite_list, enemy_sprite_list, True, True)
        player_hit_by_bullet = pygame.sprite.groupcollide(enemy_bullet_sprite_list, spaceship_sprite_list, True, False)

        # if player is hit
        for hit in enemy_hit_by_bullet:
            score += 1

        # Dibujamos el score
        scoretext = fuente.render("Score {0}".format(score), 1, (255, 255, 255))
        WINDOW.blit(scoretext, (5, 10))

        for hit in player_hit_by_bullet:
            spaceship.life = 0

        # Dibujamos y actualizamos las listas de sprites de Spaceship
        spaceship_sprite_list.update(delta_time)
        spaceship_sprite_list.draw(WINDOW)
        spaceship_bullet_sprite_list.update(0)
        spaceship_bullet_sprite_list.draw(WINDOW)

        # Dibujamos y actualizamos la lista de sprites de Enemy
        enemy_sprite_list.update(delta_time)
        enemy_sprite_list.draw(WINDOW)
        enemy_bullet_sprite_list.update(1)
        enemy_bullet_sprite_list.draw(WINDOW)

        # Actualizamos la ventana
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()