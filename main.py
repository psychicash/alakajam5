# imports from 3rd party
import pygame
from pygame import freetype

import random
from math import sin, cos, pi, atan2, degrees
import os
import os.path
from os import path

# import sys
# # import xlsxwriter
# # import xlrd
# import numpy as np

# import personal libraries
# import astar_path
# import wang


# initializers
pygame.init()
if not pygame.display.get_init():
    pygame.display.init()
if not pygame.freetype.was_init():
    pygame.freetype.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()

# Constants and Globals
FPSCLOCK = pygame.time.Clock()
BOARDWIDTH = 12
BOARDHEIGHT = 7
TILESIZE = 100
FPS = 60
BLANK = None

# Color Constants
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (12, 255, 0)
DK_GREEN = (51, 102, 0)
BLUE = (18, 0, 255)
ORANGE = (255, 186, 0)
SKYBLUE = (39, 145, 251)
PURPLE = (153, 51, 255)
DK_PURPLE = (102, 0, 204)
BROWN = (204, 153, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

_Current_scene = 'Title'
_Current_Level = 0
_Store_gold = 100
_Player_gold = 0


_image_library = {}

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
    return image


def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)


def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (cos(angle) * distance),
            pos[1] - (sin(angle) * distance))


def draw_text(text, x, y, style):
    pass

'''
item_type = {'Strong': Chest_Plate, 'Quick': wand, 'Hurt': melee_weapon, 'Solid': ring, 'Centered': necklace}
elemental_effect = {'Zealous': fire, 'Imminent': wind, 'Saturated': water, 'Sheltered': earth, 'Forceful': soul, 'Crackling': electricity, 'None': None}
activation_action = {'Glancing': touch, 'Articulating': verbal, 'Trancending': psychic, 'Demonstrating': gesture, 'Devouring': material}
active_effect = {'Incursion': attack, 'Stalwalt': defense, 'Request': summon, 'Graduation': transformation, 'Fallacy': illusion, 'Crusade': movement}
drawback_effect = {'None': None, 'Tribal': racial_attuned, 'Soft': female_attuned, 'Hard': male_attuned, 'Thorny': backlash, 'Pariah': reputational}
cursed_effect = {'Youthful': shortens_life, 'Heirloom': no_removal, 'Karmic': boomerang, 'None': None}
guilds_list = {'Fighters': fist, 'Adventurers': compass, 'Magic': eye, 'Theives': key, 'Unguilded': None}

value = {'Base': 100, 'Strong': 25, 'Quick': 100, 'Hurt': 50, 'Solid': 100, 'Centered': 100, 'Zealous': 150, 'Imminent': 75, 'Saturated': 25, 'Sheltered': 50, 'Fourceful': 200, 'Crackling': 100, 'Glancing': 125, 'Articulating': 150, 'Trancending': 300, 'Demonstrating': 25, 'Devouring': 50, 'Incursion': 100, 'Stalwalt': 75, 'Request': 150, 'Graduation': 200, 'Fallacy': 250, 'Crusade': 300}
negative_values = {'Tribal': 10, 'Soft': 50, 'Hard': 50, 'Thorny': 25, 'Pariah': 10, 'Youthful': 50, 'Heirloom': 85, 'Karmic': 35}
ele_img = {'Zealous': './images/elements/fire', 'Imminent': './images/elements/wind', 'Saturated': './images/elements/water', 'Sheltered': './images/elements/earth', 'Forceful': './images/elements/soul', 'Crackling': './images/elements/electricity'}
activation_image = {'Glancing': './images/action/touch', 'Articulating': './images/action/verbal', 'Trancending': './images/action/psychic', 'Demonstrating': './images/action/gesture', 'Devouring': './images/action/material'}
effect_image = {'Incursion': './images/effect/attack', 'Stalwalt': './images/effect/defense', 'Request': './images/effect/summon', 'Graduation': './images/effect/transformation', 'Fallacy': './images/effect/illusion', 'Crusade': './images/effect/movement'}
drawback_image = {'Tribal': './images/drawback/racial_attuned', 'Soft': './images/drawback/female_attuned', 'Hard': './images/drawback/male_attuned', 'Thorny': './images/drawback/backlash', 'Pariah': './images/drawback/reputational'}
cursed_image = {'Youthful': './images/cursed/shortens_life', 'Heirloom': './images/cursed/no_removal', 'Karmic': './images/cursed/boomerang'}
guilds_crest = {'Fighters': './images/guild/fist', 'Adventurers': './images/guild/compass', 'Magic': './images/guild/eye', 'Theives': './images/guild/key'}
'''




def quote(item_type, ele_dis, act_dis, dra_dis, cur_dis):
    retail_price = value.get(item_type) + value.get(ele_dis) + value.get(act_dis)
    negative_percent = (-1 * (negative_values.get(dra_dis) / 100)) + (-1 * (negative_values.get(cur_dis)))
    return retail_price - (retail_price * negative_percent)



#########################
########   Classes
#########################


class Cl_Chest_plate(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__()
        self.item_type = 'Strong'
        self.ele_dis, self.element = random.choice(list(elemental_effect.items()))
        self.act_dis, self.action = random.choice(list(activation_action.items()))
        self.eff_dis, self.effect = random.choice(list(active_effect.items()))
        self.dra_dis, self.drawback = random.choice(list(drawback_effect()))
        if drawback == None:
            self.cur_dis, self.curse = random.choice(list(cursed_effect()))

        self.item_value = quote(self.item_type, self.ele_dis, self.act_dis, self.dra_dis, selfcur_dis)
        self.img_front = get_image('./images/chest/front.png')
        self.img_back = get_image('./images/chest/back.png')
        self.img_right_side = get_image('./images/chest/right.png')
        self.img_left_side = get_image('./images/chest/left.png')
        self.img_above = get_image('./images/chest/top.png')
        self.img_below = get_image('./images/chest/bottom.png')
        self.images = []
        self.images.append(img_front)
        self.images.append(img_back)
        self.images.append(img_right_side)
        self.images.append(img_left_side)
        self.images.append(img_above)
        self.images.append(img_below)


        self.ele_effect = get_image(ele_img.get(self.ele_dis) + self.ele_dis + '.png')
        self.activation = get_image(activation_image.get(self.act_dis) + self.act_dis + '.png')
        self.act_effect = get_image(effect_image.get(self.eff_dis) + self.eff_dis + '.png')
        if self.drawback != None:
            self.draw_effect = get_image(drawback_image.get(self.dra_dis) + self.dra_dis + '.png')
        elif self.drawback == None:
            self.cur_dis = get_image(cursed_image.get(self.cur_dis) + self.cur_dis + '.png')


class Cl_Wand(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__()
        self.item_type = 'Quick'
        self.ele_dis, self.element = random.choice(list(elemental_effect.items()))
        self.act_dis, self.action = random.choice(list(activation_action.items()))
        self.eff_dis, self.effect = random.choice(list(active_effect.items()))
        self.dra_dis, self.drawback = random.choice(list(drawback_effect()))
        if drawback == None:
            self.cur_dis, self.curse = random.choice(list(cursed_effect()))

        self.item_value = quote(self.item_type, self.ele_dis, self.act_dis, self.dra_dis, selfcur_dis)
        self.img_front = get_image('./images/wand/front.png')
        self.img_back = get_image('./images/wand/back.png')
        self.img_right_side = get_image('./images/wand/right.png')
        self.img_left_side = get_image('./images/wand/left.png')
        self.img_above = get_image('./images/wand/top.png')
        self.img_below = get_image('./images/wand/bottom.png')
        self.images = []
        self.images.append(img_front)
        self.images.append(img_back)
        self.images.append(img_right_side)
        self.images.append(img_left_side)
        self.images.append(img_above)
        self.images.append(img_below)


        self.ele_effect = get_image(ele_img.get(self.ele_dis) + self.ele_dis + '.png')
        self.activation = get_image(activation_image.get(self.act_dis) + self.act_dis + '.png')
        self.act_effect = get_image(effect_image.get(self.eff_dis) + self.eff_dis + '.png')
        if self.drawback != None:
            self.draw_effect = get_image(drawback_image.get(self.dra_dis) + self.dra_dis + '.png')
        elif self.drawback == None:
            self.cur_dis = get_image(cursed_image.get(self.cur_dis) + self.cur_dis + '.png')



class Cl_Melee_weapon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__()
        self.item_type = 'Hurt'
        self.ele_dis, self.element = random.choice(list(elemental_effect.items()))
        self.act_dis, self.action = random.choice(list(activation_action.items()))
        self.eff_dis, self.effect = random.choice(list(active_effect.items()))
        self.dra_dis, self.drawback = random.choice(list(drawback_effect()))
        if drawback == None:
            self.cur_dis, self.curse = random.choice(list(cursed_effect()))

        self.item_value = quote(self.item_type, self.ele_dis, self.act_dis, self.dra_dis, selfcur_dis)
        self.img_front = get_image('./images/sword/front.png')
        self.img_back = get_image('./images/sword/back.png')
        self.img_right_side = get_image('./images/sword/right.png')
        self.img_left_side = get_image('./images/sword/left.png')
        self.img_above = get_image('./images/sword/top.png')
        self.img_below = get_image('./images/sword/bottom.png')
        self.images = []
        self.images.append(img_front)
        self.images.append(img_back)
        self.images.append(img_right_side)
        self.images.append(img_left_side)
        self.images.append(img_above)
        self.images.append(img_below)


        self.ele_effect = get_image(ele_img.get(self.ele_dis) + self.ele_dis + '.png')
        self.activation = get_image(activation_image.get(self.act_dis) + self.act_dis + '.png')
        self.act_effect = get_image(effect_image.get(self.eff_dis) + self.eff_dis + '.png')
        if self.drawback != None:
            self.draw_effect = get_image(drawback_image.get(self.dra_dis) + self.dra_dis + '.png')
        elif self.drawback == None:
            self.cur_dis = get_image(cursed_image.get(self.cur_dis) + self.cur_dis + '.png')

class Cl_Ring(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__()
        self.item_type = 'Solid'
        self.ele_dis, self.element = random.choice(list(elemental_effect.items()))
        self.act_dis, self.action = random.choice(list(activation_action.items()))
        self.eff_dis, self.effect = random.choice(list(active_effect.items()))
        self.dra_dis, self.drawback = random.choice(list(drawback_effect()))
        if drawback == None:
            self.cur_dis, self.curse = random.choice(list(cursed_effect()))

        self.item_value = quote(self.item_type, self.ele_dis, self.act_dis, self.dra_dis, selfcur_dis)
        self.img_front = get_image('./images/ring/front.png')
        self.img_back = get_image('./images/ring/back.png')
        self.img_right_side = get_image('./images/ring/right.png')
        self.img_left_side = get_image('./images/ring/left.png')
        self.img_above = get_image('./images/ring/top.png')
        self.img_below = get_image('./images/ring/bottom.png')
        self.images = []
        self.images.append(img_front)
        self.images.append(img_back)
        self.images.append(img_right_side)
        self.images.append(img_left_side)
        self.images.append(img_above)
        self.images.append(img_below)


        self.ele_effect = get_image(ele_img.get(self.ele_dis) + self.ele_dis + '.png')
        self.activation = get_image(activation_image.get(self.act_dis) + self.act_dis + '.png')
        self.act_effect = get_image(effect_image.get(self.eff_dis) + self.eff_dis + '.png')
        if self.drawback != None:
            self.draw_effect = get_image(drawback_image.get(self.dra_dis) + self.dra_dis + '.png')
        elif self.drawback == None:
            self.cur_dis = get_image(cursed_image.get(self.cur_dis) + self.cur_dis + '.png')



class Cl_Necklace(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__()
        self.item_type = 'Centered'
        self.ele_dis, self.element = random.choice(list(elemental_effect.items()))
        self.act_dis, self.action = random.choice(list(activation_action.items()))
        self.eff_dis, self.effect = random.choice(list(active_effect.items()))
        self.dra_dis, self.drawback = random.choice(list(drawback_effect()))
        if drawback == None:
            self.cur_dis, self.curse = random.choice(list(cursed_effect()))

        self.item_value = quote(self.item_type, self.ele_dis, self.act_dis, self.dra_dis, selfcur_dis)
        self.img_front = get_image('./images/necklace/front.png')
        self.img_back = get_image('./images/necklace/back.png')
        self.img_right_side = get_image('./images/necklace/right.png')
        self.img_left_side = get_image('./images/necklace/left.png')
        self.img_above = get_image('./images/necklace/top.png')
        self.img_below = get_image('./images/necklace/bottom.png')
        self.images = []
        self.images.append(img_front)
        self.images.append(img_back)
        self.images.append(img_right_side)
        self.images.append(img_left_side)
        self.images.append(img_above)
        self.images.append(img_below)


        self.ele_effect = get_image(ele_img.get(self.ele_dis) + self.ele_dis + '.png')
        self.activation = get_image(activation_image.get(self.act_dis) + self.act_dis + '.png')
        self.act_effect = get_image(effect_image.get(self.eff_dis) + self.eff_dis + '.png')
        if self.drawback != None:
            self.draw_effect = get_image(drawback_image.get(self.dra_dis) + self.dra_dis + '.png')
        elif self.drawback == None:
            self.cur_dis = get_image(cursed_image.get(self.cur_dis) + self.cur_dis + '.png')


class inspection_window(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__()


    def create_window(self,screen):
        self.window = get_image('./images/')







class Cl_Title():
    def __init__(self, screen):
        #pygame.mixer.music.load('./sound/intro.wav')
        #pygame.mixer.music.play(-1)
        self.new_gm_img = get_image('./images/newgame.png')
        self.new_gm_rect = self.new_gm_img.get_rect()
        self.new_gm_rect.x = SCREEN_WIDTH / 2
        self.new_gm_rect.y = SCREEN_HEIGHT / 2 + 100
        self.quit_gm_img = get_image('./images/quitmenu.png')
        self.quit_gm_rect = self.quit_gm_img.get_rect()
        self.bg_layer1 = get_image('./images/menu_bg/bg_layer1.png')
        self.bg_layer2 = get_image('./images/menu_bg/bg_layer2.png')
        self.bg_layer3 = get_image('./images/menu_bg/bg_layer3.png')
        self.bg_layer4 = get_image('./images/menu_bg/bg_layer4.png')
        self.title = get_image('./images/title.png')
        self.bg1_rect = self.bg_layer1.get_rect()
        self.bg1_size = self.bg_layer1.get_size()
        self.bg2_rect = self.bg_layer2.get_rect()
        self.bg2_size = self.bg_layer2.get_size()
        self.bg3_rect = self.bg_layer3.get_rect()
        self.bg3_size = self.bg_layer3.get_size()
        self.bg4_rect = self.bg_layer4.get_rect()
        self.bg4_size = self.bg_layer4.get_size()
        self.w1, self.h1 = self.bg1_size
        self.w2, self.h2 = self.bg2_size
        self.w3, self.h3 = self.bg3_size
        self.w4, self.w4 = self.bg4_size

        self.x = 0
        self.y = 0

        self.x1 = -self.w1
        self.y1 = 0

        self.x2 = -self.w2
        self.y2 = 0

        self.x3 = -self.w3
        self.y3 = 0

        self.x4 = -self.w4
        self.x4s = 0
        self.y4 = 0

        screen.blit(self.bg_layer1, (self.x, self.y))
        screen.blit(self.bg_layer1, (self.x1, self.y1))
        screen.blit(self.bg_layer2, (self.x, self.y))
        screen.blit(self.bg_layer2, (self.x2, self.y2))
        screen.blit(self.bg_layer3, (self.x, self.y))
        screen.blit(self.bg_layer3, (self.x3, self.y3))
        screen.blit(self.bg_layer4, (self.x4s, self.y))
        screen.blit(self.bg_layer4, (self.x4, self.y4))
        screen.blit(self.new_gm_img, (self.new_gm_rect.x, self.new_gm_rect.y))
        screen.blit(self.quit_gm_img, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150))
        screen.blit(self.title, (SCREEN_WIDTH / 8, SCREEN_HEIGHT // 11))


    def update(self, screen):

        self.x += 2
        self.x1 += 2
        self.x2 += 2
        self.x3 += 2
        self.x4s += 7
        self.x4 += 7

        if self.x > self.w1:
            self.x = -self.w1
        if self.x1 > self.w1:
            self.x1 = -self.w1
        if self.x2 > self.w1:
            self.x2 = -self.w1
        if self.x3 > self.w1:
            self.x3 = -self.w1
        if self.x4 > self.w1:
            self.x4 = -self.w1


        screen.blit(self.bg_layer1, (self.x, self.y))
        screen.blit(self.bg_layer1, (self.x1, self.y1))
        screen.blit(self.bg_layer2, (self.x, self.y))
        screen.blit(self.bg_layer2, (self.x2, self.y2))
        screen.blit(self.bg_layer3, (self.x, self.y))
        screen.blit(self.bg_layer3, (self.x3, self.y3))
        screen.blit(self.bg_layer4, (self.x4s, self.y))
        screen.blit(self.bg_layer4, (self.x4, self.y4))
        screen.blit(self.new_gm_img, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(self.quit_gm_img, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(self.title, (SCREEN_WIDTH / 8, SCREEN_HEIGHT // 11))






class Game():
    def __init__(self, screen):
        self.score = 0
        #add high score if time
        self.game_over = False

        #sprite lists


        #load images
        self.images = []
        self.intro1 = get_image('./images/gameintro1.png')
        self.images.append(self.intro1)
        self.intro2 = get_image('./images/gameintro2.png')
        self.images.append(self.intro2)
        self.intro3 = get_image('./images/gameintro3.png')
        self.images.append(self.intro3)
        self.intro4 = get_image('./images/gameintro4.png')
        self.images.append(self.intro4)
        self.intro5a = get_image('./images/gameintro5.png')
        self.images.append(self.intro5a)
        self.intro5 = get_image('./images/gameintro5a.png')
        self.images.append(self.intro5)
        self.intro6 = get_image('./images/gameintro6.png')
        self.images.append(self.intro6)
        self.intro7 = get_image('./images/gameintro7.png')
        self.images.append(self.intro7)
        self.intro8 = get_image('./images/gameintro8.png')
        self.images.append(self.intro8)
        self.arrow_right = get_image('./images/arrow.png')
        self.arrow_on = get_image('./images/arrowon.png')


        #run intro
        self.introduction_cinema(screen)


    def process_events(self, screen):
        pygame.event.pump()
        keyinput = pygame.key.get_pressed()
        if keyinput[pygame.K_ESCAPE]:
            raise SystemExit #TODO change to in game menu

        return False

    def run_logic(self, screen):
        if not self.game_over:
            pass


    def display_frame(self, screen):
        screen.fill(WHITE)

        if self.game_over:  # game over text on screen
            text_var = pygame.freetype.Font('./images/font/future_thin.ttf', 16, False, False)
            text_var2 = text_var.render("Game Over, click to restart", fgcolor=BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text_var2[0].get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text_var2[0].get_height() // 2)
            screen.blit(text_var2[0], [center_x, center_y])

        if not self.game_over:
            pass


        pygame.display.flip()

    def introduction_cinema(self, screen):
        self.intro = True
        self.current_intro_frame = 0



    def update(self, screen):
        screen.fill(BLACK)
        if self.current_intro_frame < len(self.images):
            screen.blit(self.images[self.current_intro_frame], (0, 0))
            screen.blit(self.arrow_right, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50))
            #screen.blit(pygame.transform.flip(self.arrow_right, True, True), (5, SCREEN_HEIGHT - 50))
        else:
            chest_img = get_image('./images/chest/front.png')
            fem = get_image('./images/elements/fire/fire_emblem.png')
            screen.blit(chest_img, ())
            screen.blit(fem, (screen.get_rect().center + (50,50)))



    def call_level(self):
            _Current_scene = 'Level'
            level = Cl_Level(screen)

class Cl_Level():
    def __init__(self, screen):
        images = []
        #img = get_image('./images/')


        pass









def main():

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    pygame.display.set_caption('Alakajam Entry')
    pygame.mouse.set_visible(True)

    done = False

    title = Cl_Title(screen)

    #main title loop
    global _Current_scene
    while _Current_scene == 'Title':
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                if title.quit_gm_img.get_rect(topleft=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)).collidepoint(x,y):
                    raise SystemExit
                if title.new_gm_img.get_rect(topleft=(title.new_gm_rect.x, title.new_gm_rect.y)).collidepoint(x,y):
                    pygame.mixer.music.fadeout(500)
                    _Current_scene = 'Game'
                    game = Game(screen)

        title.update(screen)
        FPS = 60

        pygame.display.update()
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

    # main game loop
    while not done:
        FPS = 0
        # process events
        for event in pygame.event.get():

            if _Current_scene == 'Game':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if game.arrow_right.get_rect(topleft=(SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)).collidepoint(x,y):
                        game.current_intro_frame += 1








        game.update(screen)
        FPS = 60

        pygame.display.update()
        pygame.display.flip()
        FPSCLOCK.tick(FPS)


    pygame.quit()


if __name__ == '__main__':
    main()