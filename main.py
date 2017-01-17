import pygame, time
from plane import Plane
from pygame.locals import *
from pidisplay import PiDisplay
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED


pygame.init()

# Variables
# color
background_colour = (0,0,0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0,0,0)

display = PiDisplay(background_colour)

# Font for text
myFont = pygame.font.SysFont("Arial", 32)

# screen resolution
width, height = (320, 320)
# runtime boolean
run = True
# shot boolean
shot_ally = False
shot_enemy = False
# Speed of ig movement
tick_loop_ally = 5
tick_loop_enemy = 5
# Fire rate mods for shots
fire_rate_ally = 15
fire_rate_enemy = 15
#Lebe
lives_ally = 3
lives_enemy = 3

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
alliedplane = Plane(40, 40, "allyPlane.png")
enemyPlane = Plane(40, 40, "enemyPlane.png")

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

def make_move(obj):
        for event in sense.stick.get_events():
            if event.action == "pressed" or event.action == "held" :
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
                elif event.direction == "middle":
                        if fire_rate_checker(fire_rate_enemy):
                                obj.shoot(all_sprites_list, bullet_group_enemy)
                                shot_enemy = True

def print_screen(winner):
    win_a = myFont.render("Ally Wins!!!", 1, green)
    win_e = myFont.render("Enemy Wins!!!", 1, red)

    if winner == "ally":
        screen.blit(win_a, (85,120))
        pygame.display.flip()
    else:
        screen.blit(win_e, (85,120))
        pygame.display.flip()

def print_lives(numb, colour, pos):
    number = myFont.render(str(numb), 1, colour)
    screen.blit(number, pos)
    pygame.display.flip()

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
    if tick_loop_ally == 5:
        if pygame.key.get_pressed():
            event_parser(alliedplane)
            tick_loop_ally = 0
    else:
        tick_loop_ally += 1

    if tick_loop_enemy == 5:
        event_parser(enemyPlane)
        tick_loop_enemy = 0
    else:
        tick_loop_enemy += 1

    # --- Game Logic

    # Activate Collision
    plane_collision = pygame.sprite.spritecollide(alliedplane, enemy_group, False)
    bullet_collision = pygame.sprite.groupcollide(bullet_group, enemy_group, True, False)
    bullet_collision_enemy = pygame.sprite.groupcollide(bullet_group_enemy, allied_group, True, False)

    for Plane in bullet_collision:
        print(lives_enemy)
        lives_enemy -= 1
        alliedplane.set_position(160, 0)
        enemyPlane.set_position(200, 280)
        alliedplane.set_direction("down")
        enemyPlane.set_direction("up")
        print_lives(lives_enemy, red, (300,280))
        sense.show_message(str(lives_enemy), text_colour = red)

        for Bullet in bullet_group:
                all_sprites_list.remove(Bullet)
                bullet_group.remove(Bullet)
 
        for Bullet in bullet_group_enemy:
                all_sprites_list.remove(Bullet)
                bullet_group_enemy.remove(Bullet)

            
    for Plane in bullet_collision_enemy:
        print(lives_ally)
        lives_ally -= 1
        alliedplane.set_position(160, 0)
        enemyPlane.set_position(200, 280)
        alliedplane.set_direction("down")
        enemyPlane.set_direction("up")
        print_lives(lives_ally, green, (10,40))
        sense.show_message(str(lives_ally), text_colour = green)

        for Bullet in bullet_group:
                all_sprites_list.remove(Bullet)
                bullet_group.remove(Bullet)
 
        for Bullet in bullet_group_enemy:
                all_sprites_list.remove(Bullet)
                bullet_group_enemy.remove(Bullet)
        
    for Plane in plane_collision:
        sense.show_message("CRASH!!!")
        alliedplane.set_position(160, 0)
        enemyPlane.set_position(200, 280)
        alliedplane.set_direction("down")
        enemyPlane.set_direction("up")

        for Bullet in bullet_group:
                all_sprites_list.remove(Bullet)
                bullet_group.remove(Bullet)
 
        for Bullet in bullet_group_enemy:
                all_sprites_list.remove(Bullet)
                bullet_group_enemy.remove(Bullet)

    if lives_enemy == 0:
        print_screen("ally")
        sense.show_message("Ally Wins!!!", text_colour = green)
        run = False
        sense.clear()
    if lives_ally == 0:
        print_screen("enemy")
        sense.show_message("Enemy Wins!!!", text_colour = red)
        run = False
        sense.clear()
    
    # Clamp Screen
    
    alliedplane.rect.clamp_ip(screen_rect)
    enemyPlane.rect.clamp_ip(screen_rect)

    for Bullet in bullet_group:
        if Bullet.rect.x > 280 or Bullet.rect.x < 0:
            all_sprites_list.remove(Bullet)
            bullet_group.remove(Bullet)
        elif Bullet.rect.y > 280 or Bullet.rect.y < 0:
            all_sprites_list.remove(Bullet)
            bullet_group.remove(Bullet)
            
    for Bullet in bullet_group_enemy:
        if Bullet.rect.x > 280 or Bullet.rect.x < 0:
            all_sprites_list.remove(Bullet)
            bullet_group_enemy.remove(Bullet)
        elif Bullet.rect.y > 280 or Bullet.rect.y < 0:
            all_sprites_list.remove(Bullet)
            bullet_group_enemy.remove(Bullet)
            
    # Update Sprite list
    all_sprites_list.update()
    screen.fill(background_colour)

    # draw Sprites
    all_sprites_list.draw(screen)

    # Update Display
    pygame.display.update()
    clock.tick(60)
    display.set_pos(alliedplane.get_posx(), alliedplane.get_posy(), green)
    display.set_pos(enemyPlane.get_posx(), enemyPlane.get_posy(), red) 
    # makes sure all events are handled
    pygame.event.pump()

    
sense.clear()
pygame.quit()
