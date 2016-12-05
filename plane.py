import pygame, time, threading
from pygame.locals import *

red = (255, 0, 0)
white = (255, 255, 255)


class Plane(pygame.sprite.Sprite):
    def __init__(self, color, width, height, flip):
        super().__init__()

        # loads image
        self.image = pygame.Surface([width, height])
        # defines flip
        self.flip = flip
        # loads image for the bullet
        self.image = pygame.image.load("plane.png").convert_alpha()
        # checks if player 1 is playing. If yes, flips image vertically
        if self.flip:
            self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveUp(self, pixels):
        self.rect.y -= pixels

    def moveDown(self, pixels):
        self.rect.y += pixels

    def shoot(self, all_sprites_list, bullet_group):
        bullet = Bullet(self.flip)
        # set position
        bullet.set_position(self.rect.x, self.rect.y)
        # adds bullets to groups
        all_sprites_list.add(bullet)
        bullet_group.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, flip):
        super().__init__()

        self.speed = 5
        self.flip = flip

        # loads image for the bullet
        self.image = pygame.image.load("bullet.png").convert_alpha()

        # checks if player 1 is playing. If yes, flips image vertically
        if self.flip:
            self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.flip:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
