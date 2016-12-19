import pygame, time
from plane import Plane
from pygame.locals import *
from pidisplay import PiDisplay

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED


pygame.init()

# Variables
# color
background_colour = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

display = PiDisplay(background_colour)

# screen resolution
width, height = (320, 320)
# runtime boolean
run = True
# shot boolean
shot_ally = False
shot_enemy = False
# Speed of ig movement
tick_loop = 5
# Fire rate mods for shots
fire_rate_ally = 15
fire_rate_enemy = 15

# define screen
screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
pygame.display.set_caption("PlaneGame")
screen_rect = screen.get_rect()

# defining sprite groups
all_sprites_list = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
allied_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
bullet_group_enemy = pygame.sprite.Group()

# Objects
alliedplane = Plane(40, 40)
enemyPlane = Plane(40, 40)

# add objects to list
all_sprites_list.add(alliedplane, enemyPlane)
# Both Planes to separate groups
enemy_group.add(enemyPlane)
allied_group.add(alliedplane)
# add sensehat
sense = SenseHat()
sense.clear()
# set Positions
alliedplane.set_position(160, 0)
enemyPlane.set_position(200, 280)
alliedplane.set_direction("down")
enemyPlane.set_direction("up")

# Clock
clock = pygame.time.Clock()


def fire_rate_checker(fire_looper):
    if fire_looper == 15:
        return True
    elif fire_looper < 15:



        return False


# makes a repeating shot while keeping  shot loaded
def fire_rate_loop(shot, fire_count):
    if shot:
        shot = False
        fire_count = 0
        return shot, fire_count
    elif fire_count < 15:
        fire_count += 1
        return shot, fire_count
    else:
        return shot, fire_count


# takes events and parses (long and stupid)
def event_parser(obj):
    pressed = pygame.key.get_pressed()
    global run, shot_ally, shot_enemy
    if obj == alliedplane:
        if pressed[K_ESCAPE]:
            run = False
        elif pressed[K_a]:
            obj.moveLeft(40)
            alliedplane.set_direction("left")
            sense.clear()
        elif pressed[K_d]:
            obj.moveRight(40)
            alliedplane.set_direction("right")
            sense.clear()
        elif pressed[K_w]:
            obj.moveUp(40)
            alliedplane.set_direction("up")
            sense.clear()
        elif pressed[K_s]:
            obj.moveDown(40)
            alliedplane.set_direction("down")
            sense.clear()
        elif pressed[K_SPACE]:
            if fire_rate_checker(fire_rate_ally):
                obj.shoot(all_sprites_list, bullet_group)
                shot_ally = True

    elif obj == enemyPlane:
        make_move(obj)
        '''
        if pressed[K_ESCAPE]:
            run = False
        elif pressed[K_LEFT]:
            obj.moveLeft(40)
        elif pressed[K_RIGHT]:
            obj.moveRight(40)
        elif pressed[K_UP]:
            obj.moveUp(40)
        elif pressed[K_DOWN]:
            obj.moveDown(40)
        elif pressed[K_m]:
            if fire_rate_checker(fire_rate_enemy):
                obj.shoot(all_sprites_list, bullet_group_enemy)
                shot_enemy = True
                '''

def make_move(obj):
    for event in sense.stick.get_events():
        if event.action == "pressed":
            sense.clear()
            if event.direction == "up":
                    obj.moveUp(40)
                    enemyPlane.set_direction("up")
            elif event.direction == "down":
                    obj.moveDown(40)
                    enemyPlane.set_direction("down")
            elif event.direction == "left":
                    obj.moveLeft(40)
                    enemyPlane.set_direction("left")
            elif event.direction == "right":
                    obj.moveRight(40)
                    enemyPlane.set_direction("right")
        elif event.action == "held" or event.action == "pressed":
            sense.clear()          
            if event.direction == "middle":
                if fire_rate_checker(fire_rate_enemy):
                        obj.shoot(all_sprites_list, bullet_group_enemy)
                        shot_enemy = True


# main loop
while run:
    # closes program if "X" is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # checks the reload loop
    shot_ally, fire_rate_ally = fire_rate_loop(shot_ally, fire_rate_ally)
    shot_enemy, fire_rate_enemy = fire_rate_loop(shot_enemy, fire_rate_enemy)

    # parses events for both players (fricking config this shit, i dunno)
    if tick_loop == 5:
        if pygame.key.get_pressed():
            event_parser(alliedplane)
            event_parser(enemyPlane)
            tick_loop = 0
    else:
        tick_loop += 1

    # --- Game Logic

    # Activate Collision
    plane_collision = pygame.sprite.spritecollide(alliedplane, enemy_group, False)
    bullet_collision = pygame.sprite.groupcollide(bullet_group, enemy_group, False, False)
    bullet_collision_enemy = pygame.sprite.groupcollide(bullet_group_enemy, allied_group, False, False)
    for Plane in plane_collision or bullet_collision or bullet_collision_enemy:
        print("Crash!!!")
        run = False
        sense.clear()

    # Clamp Screen
    alliedplane.rect.clamp_ip(screen_rect)
    enemyPlane.rect.clamp_ip(screen_rect)

    # Update Sprite list
    all_sprites_list.update()
    screen.fill(blue)

    # draw Sprites
    all_sprites_list.draw(screen)

    # Update Display
    pygame.display.update()
    clock.tick(60)
    display.set_ally_pos(alliedplane.get_posx(), alliedplane.get_posy(), green)
    display.set_ally_pos(enemyPlane.get_posx(), enemyPlane.get_posy(), red)
    
    # makes sure all events are handled
    pygame.event.pump()

pygame.quit()
