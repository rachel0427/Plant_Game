import pygame
import random
import math
from pygame import mixer

# This file documents all classes of objects used in the game
# 整个游戏一共5瓶vodka，救急

# round_num keeps track of the current round number
global round_num
global plant_size
global shelf_rect_list


# Some Variables
InitialMoney = 50
plant_size = 64
# rectangle values: left, top, width, height
shelf_rect_list = [pygame.Rect(270,178,120,100), pygame.Rect(390,178,120,100), pygame.Rect(510,178,120,100),
                   pygame.Rect(270,315,120,100), pygame.Rect(390,315,120,100), pygame.Rect(510,315,120,100),
                   pygame.Rect(270,453,120,100), pygame.Rect(390,453,120,100), pygame.Rect(510,453,120,100)]


GoodPlantImage = 'Images/goodPlant.png'
GreatPlantImage = 'Images/greatPlant.png'
AwesomePlantImage = 'Images/awesomePlant.png'
LeekImage = 'Images/leek.png'
TrashCanImage = 'Images/trashCan.png'

ExplodeState = 3  # plants explode when anger state reaches 3

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


class Game:
    # Use this class to keep track of and relate all elements?
    # e.g. round number, user actions & plant state change...
    pass


# Button Proceed
class NextButton:
    img = pygame.image.load('Images/next.png')
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
class AngerBar:
    pass


# Vodka Bottle
class VodkaBottleIcon:
    pass


# Money Keeper
class Bank:

    def __init__(self, money=50):
        self.money = money  # player's possession is initialized to 50

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

# Plants: 4 species
# Class for Good Plants
class GoodPlant:

    # Good Plant Properties
    sell_price = SellGood
    production = GoodProduce
    production_cycle = GoodProduceCycle
    img = pygame.image.load(GoodPlantImage)
    anger_state = 0

    # Constructor
    def __init__(self, pos_x, pos_y, shelf_pos):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.shelf_pos = 0  # Initialized to top shelf

    # show_good_plant shows the good plant object on screen
    def show_good_plant(self, window):
        window.blit(self.img, (self.pos_x, self.pos_y))

    # check_good_collision checks for collision between mouse and good plant
    def check_good_collision(self, mouseX, mouseY):
        # This is how you check for collision between mouse pos and objects
        rectangle = self.img.get_rect()
        rectangle.topleft = (self.pos_x, self.pos_y)
        if rectangle.collidepoint(mouseX, mouseY):
            return True
        return False

    # drag_good_plant makes good plant follow mouse position
    def drag_good_plant(self, mouseX, mouseY):
        self.pos_x = mouseX - plant_size / 2
        self.pos_y = mouseY - plant_size / 2

    # check_trash_plant_collision checks for collision with trash can
    def check_trash_good_collision(self, trash_obj):
        # This is how you check for collision between trash can and plant objects
        distance = math.sqrt(
            math.pow((trash_obj.pos_x - self.pos_x), 2) + math.pow((trash_obj.pos_y - self.pos_y), 2))
        if distance < 57:
            return True
        return False
    # correct_good_pos corrects good plant's position as player drags it on the shelf
    def correct_good_pos(self):
        pass

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