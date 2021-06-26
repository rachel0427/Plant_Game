import pygame
import random
import math
from pygame import mixer

# This file documents all classes of objects used in the game
# 整个游戏一共5瓶vodka，救急

# TODO: mood bubble should only be displayed
#  when plant has already been placed on shelf
# FIXME: if plant already on shelf, it can't be moved back to original position

# round_num keeps track of the current round number
global round_num
global plant_size
global shelf_rect_list

# Some Variables
InitialMoney = 50
plant_size = 64
# rectangle values: left, top, width, height
shelf_rect_list = [pygame.Rect(270, 178, 120, 100), pygame.Rect(390, 178, 120, 100), pygame.Rect(510, 178, 120, 100),
                   pygame.Rect(270, 315, 120, 100), pygame.Rect(390, 315, 120, 100), pygame.Rect(510, 315, 120, 100),
                   pygame.Rect(270, 453, 120, 100), pygame.Rect(390, 453, 120, 100), pygame.Rect(510, 453, 120, 100)]

# shelf_if_occupied keeps track of if a grid on shelf is occupied
shelf_is_occupied = [False, False, False, False, False, False, False, False, False]

# A Lot of Images
GoodPlantImage = 'Images/goodPlant.png'
GreatPlantImage = 'Images/greatPlant.png'
AwesomePlantImage = 'Images/awesomePlant.png'
LeekImage = 'Images/leek.png'
TrashCanImage = 'Images/trashCan.png'
NextButtonImage = 'Images/next.png'
MoodBubbleImage = 'Images/moodBubble.png'
BigGrandPaImage = 'Images/bigGrandpa - Copy.jpg'
HappyImage = 'Images/happy.png'
SadImage = 'Images/sad.png'
AngryImage = 'Images/angry.png'
VodkaImage = 'Images/vodka.png'

ExplodeState = 3  # plants explode when anger state reaches 3

# A lot of Variables
SellGood = 50
SellGreat = 60
SellAwesome = 100
SellLeek = 50

GoodProduce = 20
GreatProduce = 30
AwesomeProduce = 50
LeekProduce = 40

GoodPrice = 20
GreatPrice = 30
AwesomePrice = 50

GoodProduceCycle = 1
GreatProduceCycle = 1
AwesomeProduceCycle = 1
LeekProduceCycle = 1

# font
font = pygame.font.Font('freesansbold.ttf', 32)


# Here Comes the Classes

class Game:
    # Use this class to keep track of and relate all elements?
    # e.g. round number, user actions & plant state change...
    pass


# Button Proceed
class NextButton:
    img = pygame.image.load(NextButtonImage)
    pos_x = 10
    pos_y = 570

    # show_next_button shows the next button on screen
    def show_next_button(self, window):
        window.blit(self.img, (self.pos_x, self.pos_y))

    # check_next_collision checks for collision between mouse and next button
    def check_next_collision(self, mouseX, mouseY):
        # This is how you check for collision between mouse pos and objects
        rectangle = self.img.get_rect()
        rectangle.topleft = (self.pos_x, self.pos_y)
        if rectangle.collidepoint(mouseX, mouseY):
            return True
        return False


# Anger Bar
class MoodBubble:
    happy = pygame.image.load(HappyImage)
    sad = pygame.image.load(SadImage)
    angry = pygame.image.load(AngryImage)
    pos_x = 0
    pos_y = 0
    plus_x = 20
    plus_y = -30

    def show_bubble(self, window, plant_pos_x, plant_pos_y, anger_level):
        """
        This function displays bubble based on plant position
        :param anger_level:
        :param window: game window
        :param plant_pos_x: x position of plant whose mode is to be displayed
        :param plant_pos_y: y position of plant whose mode is to be displayed
        """
        # This is just shifting the bubble based on plant position
        self.pos_x = plant_pos_x + self.plus_x
        self.pos_y = plant_pos_y + self.plus_y
        # Making sure that bubble position is initialized
        if self.pos_x != 0 and self.pos_y != 0:
            if anger_level == 0:
                window.blit(self.happy, (self.pos_x, self.pos_y))
            elif anger_level == 1:
                window.blit(self.sad, (self.pos_x, self.pos_y))
            elif anger_level == 2:
                window.blit(self.angry, (self.pos_x, self.pos_y))


class VodkaCount:

    pos_x = 760
    pos_y = 220

    def __init__(self, count=5):
        self.count = count

    def show_num(self, screen):
        count = font.render(": " + str(self.count), True, (0, 0, 0))
        screen.blit(count, (self.pos_x, self.pos_y))


# Vodka Bottle
class VodkaBottle:

    img = pygame.image.load(VodkaImage)
    pos_x = 700
    pos_y = 200

    def __init__(self, num=5):
        self.num = num

    def show_vodka_image(self, window):
        """
        Show vodka bottle
        :param window: game window
        """
        window.blit(self.img, (self.pos_x, self.pos_y))

    def check_vodka_collision(self, mouse_x, mouse_y):
        """
        Check if mouse collide with vodka bottle image
        :param mouse_x: x coord of mouse position
        :param mouse_y: y coord of mouse position
        :return: boolean value of whether collision occured
        """
        rectangle = self.img.get_rect()
        rectangle.topleft = (self.pos_x, self.pos_y)
        if rectangle.collidepoint(mouse_x, mouse_y):
            return True
        return False

    def drag_vodka_bottle(self, mouse_x, mouse_y, vodka_count_obj):
        if vodka_count_obj.count > 0:
            self.pos_x = mouse_x - 32
            self.pos_y = mouse_y - 32

    def check_plant_vodka_collision(self, plant_list, vodka_count_obj):
        """
        This function checks if vodka bottle collide with plant
        :param plant_list:
        :return:
        """
        if vodka_count_obj.count > 0:
            closest_rect_ind = 0
            min_dist = math.sqrt(
                math.pow((plant_list[0].pos_x - self.pos_x), 2) +
                math.pow((plant_list[0].pos_y - self.pos_y), 2))
            for i in range(len(plant_list)):
                cur_dist = math.sqrt(math.pow(plant_list[i].pos_x - self.pos_x, 2) +
                                     math.pow(plant_list[i].pos_y - self.pos_y, 2))
                if cur_dist < min_dist:
                    closest_rect_ind = i
                    min_dist = cur_dist

            if min_dist < 80:
                plant_list[closest_rect_ind].decrease_anger()
                self.pos_x = 700
                self.pos_y = 200
                vodka_count_obj.count -= 1


# Money Keeper
class Bank:

    pos_x = 700  # position of money count
    pos_y = 150

    def __init__(self, money=50):
        self.money = money  # player's possession is initialized to 50

    def show_money(self, screen):
        # rander: (text, TURE, color_in_RGB)
        score = font.render("Money: " + str(self.money), True, (0, 0, 0))
        screen.blit(score, (self.pos_x, self.pos_y))

    # Sell Plant functions will be called when player sells their plant
    def sell_good_plant(self):
        self.money += SellGood
        # FIXME: delete plant here? or maybe in Game function

    def sell_great_plant(self):
        self.money += SellGreat

    def sell_awesome_plant(self):
        self.money += SellAwesome

    def sell_leek(self):
        self.money += SellLeek

    # Buy Plant functions are called when player buy plants
    def buy_good_plant(self):
        self.money -= GoodPrice

    def buy_great_plant(self):
        self.money -= GreatPrice

    def buy_awesome_plant(self):
        self.money -= AwesomePrice

    # Plant Produce functions are called when plants reproduce
    def good_produce(self):
        self.money += GoodProduce

    def great_produce(self):
        self.money += GreatProduce

    def awesome_produce(self):
        self.money += AwesomeProduce


# Trash can object: drag plants to trash icon to delete object
class TrashCan:
    img = pygame.image.load(TrashCanImage)
    pos_x = 820
    pos_y = 570

    # show_trash_can shows the trash can object on screen
    def show_trash_can(self, window):
        window.blit(self.img, (self.pos_x, self.pos_y))


# Big Grandpa
class BigGrandpa:
    img = pygame.image.load(BigGrandPaImage)
    pos_x = 50
    pos_y = 500
    font_x = 50
    font_y = 460
    font = pygame.font.Font('Fonts/LazySunday-Regular.ttf', 48)

    # show_big_grandpa_font shows big grandpa with his title on screen
    def show_big_grandpa_font(self, window):
        big_grandpa_title = self.font.render("Big Grandpa", True, (0, 0, 0))
        window.blit(self.img, (self.pos_x, self.pos_y))
        window.blit(big_grandpa_title, (self.font_x, self.font_y))


# Plants: 4 species
# Class for Good Plants
class GoodPlant:
    # Good Plant Properties
    sell_price = SellGood
    production = GoodProduce
    production_cycle = GoodProduceCycle
    img = pygame.image.load(GoodPlantImage)
    anger_level = 0
    # TODO: added this variable
    # this variable keeps track of whether the plant has been placed on the shelf
    # if plant has been placed, then it starts to have a mood bubble
    # otherwise, the plant does not have a mood bubble
    on_shelf = False
    shelf_pos_cur = -1  # Initialized to -1
    shelf_pos_prev = -1

    # Constructor
    def __init__(self, pos_x, pos_y, shelf_pos):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.init_x = pos_x  # keeps track of plant's initial postion when created
        self.init_y = pos_y

    def decrease_anger(self):
        self.anger_level -= 1

    def increase_anger(self):
        self.anger_level += 1

    def show_good_plant(self, window):
        """
        # show_good_plant shows the good plant object on screen
        :param window: the game window
        """
        window.blit(self.img, (self.pos_x, self.pos_y))

    def check_good_collision(self, mouseX, mouseY):
        """
         Check_good_collision checks for collision between mouse and good plant
        :param mouseX: x coord of mouse position
        :param mouseY: y coord of mouse position
        :return: boolean value of whether collision occured
        """
        # get a rectangle the size of img
        rectangle = self.img.get_rect()
        # place the rectangle so that its top left corner is placed at (pos_x, pos_y)
        rectangle.topleft = (self.pos_x, self.pos_y)
        # check for collision with the collidepoint() function
        if rectangle.collidepoint(mouseX, mouseY):
            return True
        return False

    def drag_good_plant(self, mouseX, mouseY):
        """
        Drag_good_plant makes good plant follow mouse position
        :param mouseX: x coord of mouse position
        :param mouseY: y coord of mouse position
        """
        self.pos_x = mouseX - plant_size / 2
        self.pos_y = mouseY - plant_size / 2

    def check_trash_good_collision(self, trash_obj):
        """
        Check_trash_plant_collision checks for collision with trash can
        :param trash_obj: trash_can object
        :return: boolean value of whether trash can and plant object collided
        """
        # This is how you check for collision between trash can and plant objects
        distance = math.sqrt(
            math.pow((trash_obj.pos_x - self.pos_x), 2) + math.pow((trash_obj.pos_y - self.pos_y), 2))
        if distance < 57:
            return True
        return False

    def check_mouse_on_plant(self, mouse_x, mouse_y):
        """
         This function checks if mouse is on this plant
        :param mouse_x: x coord of mouse position
        :param mouse_y: y coord of mouse position
        :return: whether mouse is placed on plant image
        """
        # same as above
        rectangle = self.img.get_rect()
        rectangle.topleft = (self.pos_x, self.pos_y)
        if rectangle.collidepoint(mouse_x, mouse_y):
            return True
        return False

    def correct_good_pos(self):
        """
        Correct_good_pos corrects good plant's position as player drags it on the shelf
        """
        closest_rect_ind = 0  # closest_rect_ind keeps track of the index of the closest rectangle
        min_dis = math.sqrt(
            math.pow((shelf_rect_list[0].topleft[0] - self.pos_x), 2) +
            math.pow((shelf_rect_list[0].topleft[1] - self.pos_y), 2))

        # find closest shelf position
        for i in range(1, len(shelf_rect_list)):
            cur_dist = math.sqrt(
                math.pow((shelf_rect_list[i].topleft[0] - self.pos_x), 2) +
                math.pow((shelf_rect_list[i].topleft[1] - self.pos_y), 2))
            if cur_dist < min_dis:
                closest_rect_ind = i
                min_dis = cur_dist

        # after for loop, min dist and index are found
        # check if plant was even dragged to the shelf; if not, back to initial position
        if min_dis < 80 and (not shelf_is_occupied[closest_rect_ind]):
            self.change_position(shelf_rect_list[closest_rect_ind].topleft[0] + 30,
                                 shelf_rect_list[closest_rect_ind].topleft[1] + 20)
            shelf_is_occupied[closest_rect_ind] = True
            # update plant position
            self.shelf_pos_cur = closest_rect_ind
            self.on_shelf = True
        else:
            self.change_position(self.init_x, self.init_y)

    # clear_shelf resets shelf grid to empty when plant dragged away
    # called when mouse button down
    def clear_shelf(self):
        closest_rect_ind = 0  # closest_rect_ind keeps track of the index of the closest rectangle
        min_dis = math.sqrt(
            math.pow((shelf_rect_list[0].topleft[0] - self.pos_x), 2) +
            math.pow((shelf_rect_list[0].topleft[1] - self.pos_y), 2))

        for i in range(1, len(shelf_rect_list)):
            cur_dist = math.sqrt(
                math.pow((shelf_rect_list[i].topleft[0] - self.pos_x), 2) +
                math.pow((shelf_rect_list[i].topleft[1] - self.pos_y), 2))
            if cur_dist < min_dis:
                closest_rect_ind = i
                min_dis = cur_dist
        # after for loop, min dist and index are found
        # check if plant was on shelf initially
        if min_dis < 80:
            shelf_is_occupied[closest_rect_ind] = False

    def initialize_anger(self):
        if 0 <= self.shelf_pos_cur <= 2:
            self.anger_level = 0
        elif 3 <= self.shelf_pos_cur <= 5:
            self.anger_level = 1
        elif 6 <= self.shelf_pos_cur <= 8:
            self.anger_level = 2

    """
    def set_anger_shelf(self):
        # if plant was moved down
        if self.shelf_pos_cur < self.shelf_pos_prev:
            self.anger_level += 1
        elif self.shelf_pos_cur > self.shelf_pos_prev:  # if plant was moved up
            self.anger_level -= 1
    """

    def explode(self):
        """
        Called when anger level of plant >= 3, destroys plant
        note: 如果plant anger level到达了3，则在round里call explode function来destroy plant
        """
        if self.anger_state >= ExplodeState:
            # FIXME: do something to explode, maybe remove plant from array?
            pass

    def change_position(self, end_pos_x, end_pos_y):
        """
        Called in main.py's game while loop,
        note: 当到达一定round, called in Game? or round? to create new good plants.
        """
        self.pos_x = end_pos_x
        self.pos_y = end_pos_y


# Great Plant
class GreatPlant:
    # Class Variables
    sell_price = SellGreat
    production = GreatProduce
    production_cycle = GreatProduceCycle
    img = pygame.image.load(GreatPlantImage)

    # Constructor
    def __init__(self, need_vodka_in, anger_state, produce_in, pos_x, pos_y, shelf_pos):
        self.need_vodka_in = need_vodka_in  # Initialized to 0; Assume need vodka first round when created
        self.anger_state = anger_state  # Initialized to 0; start out not angry
        self.produce_in = produce_in  # Initialized to 1; Assume first reproduction on next round
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.shelf_pos = shelf_pos

    def increase_anger(self):
        """Called when plant is moved up the shelf
        """
        self.anger_state += 1

    def decrease_anger(self):
        """Called when plant is moved down the shelf
        """
        self.anger_state -= 1

    def explode(self):
        """Called when anger level of plant >= 3, destroys plant
        note: 如果plant anger level到达了3，则在round里call explode function来destroy plant
        """
        if self.anger_state >= ExplodeState:
            # FIXME: do something to explode, maybe remove plant from array?
            pass

    def change_position(self, end_pos_x, end_pos_y):
        """Called in main.py's game while loop
        """
        self.pos_x = end_pos_x
        self.pos_y = end_pos_y


class AwesomePlant:
    # Awesome Plant Properties
    sell_price = SellAwesome
    production = AwesomeProduce
    production_cycle = AwesomeProduceCycle
    img = pygame.image.load(AwesomePlantImage)

    # Constructor
    def __init__(self, need_vodka_in, anger_state, produce_in, pos_x, pos_y, shelf_pos):
        self.need_vodka_in = need_vodka_in  # Initialized to 0; Assume need vodka first round when created
        self.anger_state = anger_state  # Initialized to 0; start out not angry
        self.produce_in = produce_in  # Initialized to 1; Assume first reproduction on next round
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.shelf_pos = shelf_pos

    def increase_anger(self):
        """Called when plant is moved up the shelf
        """
        self.anger_state += 1

    def decrease_anger(self):
        """Called when plant is moved down the shelf
        """
        self.anger_state -= 1

    def explode(self):
        """Called when anger level of plant >= 3, destroys plant
        note: 如果plant anger level到达了3，则在round里call explode function来destroy plant
        """
        if self.anger_state >= ExplodeState:
            # FIXME: do something to explode, maybe remove plant from array?
            pass

    def change_position(self, end_pos_x, end_pos_y):
        """Called in main.py's game while loop,
        note: 当到达一定round, called in Game? or round? to create new good plants.
        """
        self.pos_x = end_pos_x
        self.pos_y = end_pos_y


class Leek:
    # Leek Plant Properties
    sell_price = SellLeek
    production = LeekProduce
    production_cycle = LeekProduceCycle
    img = pygame.image.load(LeekImage)

    # Constructor
    def __init__(self, need_vodka_in, anger_state, produce_in, pos_x, pos_y, shelf_pos):
        self.need_vodka_in = need_vodka_in  # Initialized to 0; Assume need vodka first round when created
        self.anger_state = anger_state  # Initialized to 0; start out not angry
        self.produce_in = produce_in  # Initialized to 1; Assume first reproduction on next round
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.shelf_pos = shelf_pos

    def increase_anger(self):
        """Called when plant is moved up the shelf
        """
        self.anger_state += 1

    def decrease_anger(self):
        """Called when plant is moved down the shelf
        """
        self.anger_state -= 1

    def explode(self):
        """Called when anger level of plant >= 3, destroys plant
        note: 如果plant anger level到达了3，则在round里call explode function来destroy plant
        """
        if self.anger_state >= ExplodeState:
            # FIXME: do something to explode, maybe remove plant from array?
            pass

    def change_position(self, end_pos_x, end_pos_y):
        """Called in main.py's game while loop,
        note: 当到达一定round, called in Game? or round? to create new good plants.
        """
        self.pos_x = end_pos_x
        self.pos_y = end_pos_y


# Shelves
class TopShelf:
    # TODO: declare position of 3 blocks on topshelf
    pass


class MiddleShelf:
    pass


class LowerShelf:
    pass


# Plant Seeds
class ShopGood:
    pass


class ShopGreat:
    pass


class ShopAwesome:
    pass


# Text Window
class TextWindow:
    pass
