import pygame, time, threading
from pygame.locals import *
from pidisplay import PiDisplay
from sense_hat import SenseHat

red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

display = PiDisplay(blue)
sense = SenseHat()

class Plane(pygame.sprite.Sprite):
    def __init__(self, width, height, image):
        super().__init__()

        self.right = False
        self.up = False
        self.left = False
        self.down = False
        self.direct = ""

        # loads image
        self.image = pygame.Surface([width, height])
        # loads image for the bullet
        self.image = pygame.image.load(image).convert_alpha()
        # checks if player 1 is playing. If yes, flips image vertically
        #if self.flip:
           # self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_posx(self):
        return self.rect.x

    def get_posy(self):
        return self.rect.y

    def start_direction(self):
        print("blub")
        if self.down:
            self.image = pygame.transform.rotate(self.image, 180)
            self.down = False
        if self.right:
            self.image = pygame.transform.rotate(self.image, 90)
            self.right = False
        if self.left:
            self.image = pygame.transform.rotate(self.image, 270)
            self.left = False


    def set_direction(self, direct):
        self.start_direction()
        self.direct = direct
        if direct == "down" and self.down == False:
            self.image = pygame.transform.rotate(self.image, 180)
            self.down = True
            self.right = False
            self.up = False
            self.left = False
        
        elif direct == "right" and self.right == False:
            #Anfangsposition
            self.image = pygame.transform.rotate(self.image, 270)
            self.right = True
            self.up = False
            self.left = False
            self.down = False
        elif direct == "left" and self.left == False:
            #Anfangsposition
            self.image = pygame.transform.rotate(self.image, 90)
            self.left = True
            self.right = False
            self.up = False
            self.down = False

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveUp(self, pixels):
        self.rect.y -= pixels

    def moveDown(self, pixels):
        self.rect.y += pixels

    def shoot(self, all_sprites_list, bullet_group):
        bullet = Bullet(self.direct)
        # set position
        bullet.set_position(self.rect.x, self.rect.y)
        # adds bullets to groups
        all_sprites_list.add(bullet)
        bullet_group.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, direct):
        super().__init__()

        self.speed = 5
        self.direct = direct


        # loads image for the bullet
        self.image = pygame.image.load("Rocket.png").convert_alpha()

        # checks if player 1 is playing. If yes, flips image vertically
        if self.direct == "down":
            self.image = pygame.transform.flip(self.image, False, True)
        elif self.direct == "right":
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.direct == "left":
            self.image = pygame.transform.rotate(self.image, 90)

        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
            
    def update(self):
        if self.direct == "down":
            self.rect.y += self.speed
        elif self.direct == "right":
            self.rect.x += self.speed
        elif self.direct == "left":
            self.rect.x -= self.speed
        elif self.direct == "up":
            self.rect.y -= self.speed
        display.set_pos_rocket(self.rect.x, self.rect.y, blue)

