import pygame, time, threading
from plane import Plane, Bullet
from pygame.locals import *

pygame.init()

# Variables
background_colour = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
width, height = (320, 320)
run = True

# define screen
screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
pygame.display.set_caption("PlaneGame")
screen_rect = screen.get_rect()

# List containing all sprites
all_sprites_list = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
allied_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# Objects
player1Plane = Plane(green, 40, 40, True)
enemyPlane = Plane(red, 40, 40, False)

# add objects to list
all_sprites_list.add(player1Plane, enemyPlane)
# Both Planes to separate groups
enemy_group.add(enemyPlane)
allied_group.add(player1Plane)

# set Positions
player1Plane.set_position(160, 40)
enemyPlane.set_position(200, 280)

# Clock
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 100)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_a:
                player1Plane.moveLeft(40)
            elif event.key == pygame.K_d:
                player1Plane.moveRight(40)
            elif event.key == pygame.K_w:
                player1Plane.moveUp(40)
            elif event.key == pygame.K_s:
                player1Plane.moveDown(40)
            elif event.key == pygame.K_SPACE:
                player1Plane.shoot(all_sprites_list, bullet_group)

    # --- Game Logic

    # Activate Collision
    collision_list = pygame.sprite.spritecollide(player1Plane, enemy_group, False)
    bullet_collision = pygame.sprite.groupcollide(bullet_group, enemy_group, False, False)
    for Plane in collision_list or bullet_collision:
        print("Crash!!!")
        run = False

    # Clamp Screen
    player1Plane.rect.clamp_ip(screen_rect)
    enemyPlane.rect.clamp_ip(screen_rect)

    # Update Sprite list
    all_sprites_list.update()
    screen.fill(blue)

    # draw Sprites
    all_sprites_list.draw(screen)

    # Update Display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
