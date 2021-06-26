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
ExplodeImage = 'Images/explosion.jpg'
CartImage = 'Images/cart.png'
PlusImage = 'Images/add.png'
MinusImage = 'Images/minus.png'

ExplodeState = 3  # plants explode when anger state reaches 3

# A lot of Variables
SellGood = 20
SellGreat = 30
SellAwesome = 40
SellLeek = 50

GoodProduce = 50
GreatProduce = 60
AwesomeProduce = 100
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
    # FIXME: just here for testing
    explode = pygame.image.load(ExplodeImage)
    pos_x = 0
    pos_y = 0
    plus_x = 20
    plus_y = -30

    def show_mood(self, window, plant_pos_x, plant_pos_y, anger_level):
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

        if self.pos_y > 10:
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
        # this will run if there are more than 0 vodkas left
        if vodka_count_obj.count > 0:
            # finding the closest plant to vodka bottle
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

            # if made contact with plant, update plant mood as well as vodka count
            if min_dist < 80:
                plant_list[closest_rect_ind].drink_vodka()
                vodka_count_obj.count -= 1

        # this ensure that bottle return after drag
        self.pos_x = 700
        self.pos_y = 200


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


# shop class
class FancyShop:
    good_plant_purchase = 0
    great_plant_purchase = 0
    awesome_plant_purchase = 0

    # show_fancy_shop shows 3 plants' images on white rectangular background
    def show_fancy_shop(self, screen):
        # show white rectangle in middle of screen
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 100, 900, 400))
        good_count = font.render(str(self.good_plant_purchase), True, (0, 0, 0))
        great_count = font.render(str(self.great_plant_purchase), True, (0, 0, 0))
        awesome_count = font.render(str(self.awesome_plant_purchase), True, (0, 0, 0))
        screen.blit(good_count, (223, 330))
        screen.blit(great_count, (423, 330))
        screen.blit(awesome_count, (623, 330))

    def clear_shop(self):
        self.good_plant_purchase = 0
        self.great_plant_purchase = 0
        self.awesome_plant_purchase = 0


# plus sign
class PlusSign:
    img = pygame.image.load(PlusImage)

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def show_plus_sign(self, window):
        window.blit(self.img, (self.pos_x, self.pos_y))

    def get_good_plant(self, shop, bank):
        if bank.money >= GoodPrice:
            shop.good_plant_purchase += 1
            bank.buy_good_plant()


    def get_great_plant(self, shop, bank):
        if bank.money >= GreatPrice:
            shop.great_plant_purchase += 1
            bank.buy_great_plant()

    def get_awesome_plant(self, shop, bank):
        if bank.money >= AwesomePrice:
            shop.awesome_plant_purchase += 1
            bank.buy_awesome_plant()

    def check_plus_collision(self, mouseX, mouseY):
        # get a rectangle the size of img
        rectangle = self.img.get_rect()
        # place the rectangle so that its top left corner is placed at (pos_x, pos_y)
        rectangle.topleft = (self.pos_x, self.pos_y)
        # check for collision with the collidepoint() function
        if rectangle.collidepoint(mouseX, mouseY):
            return True
        return False


# minus sign
class MinusSign:
    img = pygame.image.load(MinusImage)

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def show_minus_sign(self, window):
        window.blit(self.img, (self.pos_x, self.pos_y))

    def reduce_good_plant(self, shop, bank):
        if shop.good_plant_purchase > 0:
            shop.good_plant_purchase -= 1
            bank.money += GoodPrice

    def reduce_great_plant(self, shop, bank):
        if shop.great_plant_purchase > 0:
            shop.great_plant_purchase -= 1
            bank.money += GreatPrice

    def reduce_awesome_plant(self, shop, bank):
        if shop.awesome_plant_purchase > 0:
            shop.awesome_plant_purchase -= 1
            bank.money += AwesomePrice

    def check_minus_collision(self, mouseX, mouseY):
        # get a rectangle the size of img
        rectangle = self.img.get_rect()
        # place the rectangle so that its top left corner is placed at (pos_x, pos_y)
        rectangle.topleft = (self.pos_x, self.pos_y)
        # check for collision with the collidepoint() function
        if rectangle.collidepoint(mouseX, mouseY):
            return True
        return False


# Round Counter
class RoundCounter:
    pos_x = 700  # position of money count
    pos_y = 100

    def __init__(self, round_num=1):
        self.round_num = round_num  # player's possession is initialized to 50

    def increase_round_num(self):
        self.round_num += 1

    def show_round_num(self, screen):
        # rander: (text, TURE, color_in_RGB)
        roundNumber = font.render("Round: " + str(self.round_num), True, (0, 0, 0))
        screen.blit(roundNumber, (self.pos_x, self.pos_y))


# Trash can object: drag plants to trash icon to delete object
class TrashCan:
    img = pygame.image.load(TrashCanImage)
    pos_x = 820
    pos_y = 570

    # show_trash_can shows the trash can object on screen
    def show_trash_can(self, window):
        window.blit(self.img, (self.pos_x, self.pos_y))


# Cart object: drag plants here to sell them
class Cart:
    img = pygame.image.load(CartImage)
    pos_x = 820
    pos_y = 570

    # show_trash_can shows the trash can object on screen
    def show_cart(self, window):
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
    # this variable keeps track of whether the plant has been placed on the shelf
    on_shelf = False
    shelf_pos_cur = 0  # Initialized to 0
    shelf_pos_prev = 0
    # this tells us whether the plant is put on shelf for the first time
    # help with initialization of plant mood
    first_time_on_shelf = True

    # Constructor
    def __init__(self, pos_x, pos_y, shelf_pos):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.init_x = pos_x  # keeps track of plant's initial postion when created
        self.init_y = pos_y

    def drink_vodka(self):
        self.anger_level = 0

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

    def check_cart_good_collision(self, cart_obj):
        """
        Check_cart_plant_collision checks for collision with shopping cart
        :param cart_obj: cart object
        :return: boolean value of whether trash can and plant object collided
        """
        # This is how you check for collision between cart and plant objects
        distance = math.sqrt(
            math.pow((cart_obj.pos_x - self.pos_x), 2) + math.pow((cart_obj.pos_y - self.pos_y), 2))
        if distance < 57:
            return True
        return False

    def check_mouse_on_good(self, mouse_x, mouse_y):
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

            # if we reach this position in the function, it means that player reallocated a plant
            # now we update plant mood
            self.on_shelf = True
            # if plant is being put on shelf for first time, rather than being moved up or down the shelf,
            # we call the initialize_mood() function and set shelf_pos_prev to be the same as shelf_pos_cur
            if self.first_time_on_shelf:
                self.initialize_mood()
                self.shelf_pos_cur = closest_rect_ind
                self.shelf_pos_prev = self.shelf_pos_cur
                self.first_time_on_shelf = False
            else:  # if plant is being reallocated on shelf, we call the update_mood() function instead
                # here we are updating prev before updating cur
                self.shelf_pos_prev = self.shelf_pos_cur
                self.shelf_pos_cur = closest_rect_ind
                self.update_mood()
            # Now that the plant has been placed on the shelf, it can't
            # go back to top left corner, will just go back to its position on shelf
            # self.init_x = self.pos_x
            # self.init_y = self.pos_y
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

    def initialize_mood(self):
        """
        This function initialize plant anger level to 0
        """
        self.anger_level = 0

    def update_mood(self):
        """
        This function evaluates the current and previous shelf position of the plant
        and updates plant's anger_level based on the movement
        """
        # get level value
        cur_level = int(self.shelf_pos_cur / 3)
        prev_level = int(self.shelf_pos_prev / 3)

        if cur_level > prev_level:
            self.anger_level += 1
        elif cur_level < prev_level:  # if plant was moved up
            self.anger_level -= 1

        # make sure that anger_level don't go out of bounds
        if self.anger_level > 3:
            self.anger_level = 3
        elif self.anger_level < 0:
            self.anger_level = 0
        # print("prev_l: " + str(prev_level) + " cur_l: " + str(cur_level) + " anger_l: " + str(self.anger_level))

    def explode(self):
        """
        Called when anger level of plant >= 3, destroys plant
        note: 如果plant anger level到达了3，则在round里call explode function来destroy plant
        """
        return self.anger_level >= 3

    def change_position(self, end_pos_x, end_pos_y):
        """
        Called in main.py's game while loop,
        note: 当到达一定round, called in Game? or round? to create new good plants.
        """
        self.pos_x = end_pos_x
        self.pos_y = end_pos_y

    def new_round_update(self):
        level = int(self.shelf_pos_cur / 3)
        if level == 0:
            self.anger_level -= 1
        elif level == 2:
            self.anger_level += 1
        if self.anger_level < 0:
            self.anger_level = 0
        # print("Level: " + str(level) + " Anger: " + str(self.anger_level))



# Great Plant
class GreatPlant:
    # Great Plant Properties
    sell_price = SellGreat
    production = GreatProduce
    production_cycle = GreatProduceCycle
    img = pygame.image.load(GreatPlantImage)
    anger_level = 0
    on_shelf = False
    shelf_pos_cur = 0
    shelf_pos_prev = 0
    first_time_on_shelf = True

    # Constructor
    def __init__(self, pos_x, pos_y, shelf_pos):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.init_x = pos_x  # keeps track of plant's initial postion when created
        self.init_y = pos_y

    def drink_vodka(self):
        self.anger_level = 0

    def decrease_anger(self):
        self.anger_level -= 1

    def increase_anger(self):
        self.anger_level += 1

    def show_great_plant(self, window):
        """
        # show_good_plant shows the great plant object on screen
        :param window: the game window
        """
        window.blit(self.img, (self.pos_x, self.pos_y))

    def check_great_collision(self, mouseX, mouseY):
        """
         Check_good_collision checks for collision between mouse and great plant
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

    def drag_great_plant(self, mouseX, mouseY):
        """
        Drag_good_plant makes great plant follow mouse position
        :param mouseX: x coord of mouse position
        :param mouseY: y coord of mouse position
        """
        self.pos_x = mouseX - plant_size / 2
        self.pos_y = mouseY - plant_size / 2

    def check_trash_great_collision(self, trash_obj):
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

    def check_cart_great_collision(self, cart_obj):
        """
        Check_cart_plant_collision checks for collision with shopping cart
        :param cart_obj: cart object
        :return: boolean value of whether trash can and plant object collided
        """
        # This is how you check for collision between cart and plant objects
        distance = math.sqrt(
            math.pow((cart_obj.pos_x - self.pos_x), 2) + math.pow((cart_obj.pos_y - self.pos_y), 2))
        if distance < 57:
            return True
        return False

    def check_mouse_on_great(self, mouse_x, mouse_y):
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

    def correct_great_pos(self):
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

            # if we reach this position in the function, it means that player reallocated a plant
            # now we update plant mood
            self.on_shelf = True
            # if plant is being put on shelf for first time, rather than being moved up or down the shelf,
            # we call the initialize_mood() function and set shelf_pos_prev to be the same as shelf_pos_cur
            if self.first_time_on_shelf:
                self.initialize_mood()
                self.shelf_pos_cur = closest_rect_ind
                self.shelf_pos_prev = self.shelf_pos_cur
                self.first_time_on_shelf = False
            else:  # if plant is being reallocated on shelf, we call the update_mood() function instead
                # here we are updating prev before updating cur
                self.shelf_pos_prev = self.shelf_pos_cur
                self.shelf_pos_cur = closest_rect_ind
                self.update_mood()
            # Now that the plant has been placed on the shelf, it can't
            # go back to top left corner, will just go back to its position on shelf
            # self.init_x = self.pos_x
            # self.init_y = self.pos_y
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

    def initialize_mood(self):
        """
        This function initialize plant anger level to 0
        """
        self.anger_level = 0

    def update_mood(self):
        """
        This function evaluates the current and previous shelf position of the plant
        and updates plant's anger_level based on the movement
        """
        # get level value
        cur_level = int(self.shelf_pos_cur / 3)
        prev_level = int(self.shelf_pos_prev / 3)

        if cur_level > prev_level:
            self.anger_level += 1
        elif cur_level < prev_level:  # if plant was moved up
            self.anger_level -= 1

        # make sure that anger_level don't go out of bounds
        if self.anger_level > 3:
            self.anger_level = 3
        elif self.anger_level < 0:
            self.anger_level = 0
        # print("prev_l: " + str(prev_level) + " cur_l: " + str(cur_level) + " anger_l: " + str(self.anger_level))

    def explode(self):
        """
        Called when anger level of plant >= 3, destroys plant
        note: 如果plant anger level到达了3，则在round里call explode function来destroy plant
        """
        return self.anger_level >= ExplodeState

    def change_position(self, end_pos_x, end_pos_y):
        """
        Called in main.py's game while loop,
        note: 当到达一定round, called in Game? or round? to create new good plants.
        """
        self.pos_x = end_pos_x
        self.pos_y = end_pos_y

    def new_round_update(self):
        level = int(self.shelf_pos_cur / 3)
        if level == 0:
            self.anger_level -= 1
        elif level == 2:
            self.anger_level += 1
        if self.anger_level < 0:
            self.anger_level = 0


class AwesomePlant:
    # Awesome Plant Properties
    sell_price = SellAwesome
    production = AwesomeProduce
    production_cycle = AwesomeProduceCycle
    img = pygame.image.load(AwesomePlantImage)
    anger_level = 0
    on_shelf = False
    shelf_pos_cur = 0
    shelf_pos_prev = 0
    first_time_on_shelf = True

    # Constructor
    def __init__(self, pos_x, pos_y, shelf_pos):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.init_x = pos_x  # keeps track of plant's initial position when created
        self.init_y = pos_y

    def drink_vodka(self):
        self.anger_level = 0

    def decrease_anger(self):
        self.anger_level -= 1

    def increase_anger(self):
        self.anger_level += 1

    def show_awesome_plant(self, window):
        """
        # show_good_plant shows the awesome plant object on screen
        :param window: the game window
        """
        window.blit(self.img, (self.pos_x, self.pos_y))

    def check_awesome_collision(self, mouseX, mouseY):
        """
         Check_good_collision checks for collision between mouse and awesome plant
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

    def drag_awesome_plant(self, mouseX, mouseY):
        """
        Drag_awesome_plant makes good plant follow mouse position
        :param mouseX: x coord of mouse position
        :param mouseY: y coord of mouse position
        """
        self.pos_x = mouseX - plant_size / 2
        self.pos_y = mouseY - plant_size / 2

    def check_trash_awesome_collision(self, trash_obj):
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

    def check_cart_awesome_collision(self, cart_obj):
        """
        Check_cart_plant_collision checks for collision with shopping cart
        :param cart_obj: cart object
        :return: boolean value of whether trash can and plant object collided
        """
        # This is how you check for collision between cart and plant objects
        distance = math.sqrt(
            math.pow((cart_obj.pos_x - self.pos_x), 2) + math.pow((cart_obj.pos_y - self.pos_y), 2))
        if distance < 57:
            return True
        return False

    def check_mouse_on_awesome(self, mouse_x, mouse_y):
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

    def correct_awesome_pos(self):
        """
        Correct_awesome_pos corrects awesome plant's position as player drags it on the shelf
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

            # if we reach this position in the function, it means that player reallocated a plant
            # now we update plant mood
            self.on_shelf = True
            # if plant is being put on shelf for first time, rather than being moved up or down the shelf,
            # we call the initialize_mood() function and set shelf_pos_prev to be the same as shelf_pos_cur
            if self.first_time_on_shelf:
                self.initialize_mood()
                self.shelf_pos_cur = closest_rect_ind
                self.shelf_pos_prev = self.shelf_pos_cur
                self.first_time_on_shelf = False
            else:  # if plant is being reallocated on shelf, we call the update_mood() function instead
                # here we are updating prev before updating cur
                self.shelf_pos_prev = self.shelf_pos_cur
                self.shelf_pos_cur = closest_rect_ind
                self.update_mood()
            # Now that the plant has been placed on the shelf, it can't
            # go back to top left corner, will just go back to its position on shelf
            # self.init_x = self.pos_x
            # self.init_y = self.pos_y
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

    def initialize_mood(self):
        """
        This function initialize plant anger level to 0
        """
        self.anger_level = 0

    def update_mood(self):
        """
        This function evaluates the current and previous shelf position of the plant
        and updates plant's anger_level based on the movement
        """
        # get level value
        cur_level = int(self.shelf_pos_cur / 3)
        prev_level = int(self.shelf_pos_prev / 3)

        if cur_level > prev_level:
            self.anger_level += 1
        elif cur_level < prev_level:  # if plant was moved up
            self.anger_level -= 1

        # make sure that anger_level don't go out of bounds
        if self.anger_level > 3:
            self.anger_level = 3
        elif self.anger_level < 0:
            self.anger_level = 0
        # print("prev_l: " + str(prev_level) + " cur_l: " + str(cur_level) + " anger_l: " + str(self.anger_level))

    def explode(self):
        """
        Called when anger level of plant >= 3, destroys plant
        note: 如果plant anger level到达了3，则在round里call explode function来destroy plant
        """
        return self.anger_level >= ExplodeState

    def change_position(self, end_pos_x, end_pos_y):
        """
        Called in main.py's game while loop,
        note: 当到达一定round, called in Game? or round? to create new good plants.
        """
        self.pos_x = end_pos_x
        self.pos_y = end_pos_y

    def new_round_update(self):
        level = int(self.shelf_pos_cur / 3)
        if level == 0:
            self.anger_level -= 1
        elif level == 2:
            self.anger_level += 1
        if self.anger_level < 0:
            self.anger_level = 0


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
        return self.anger_level >= ExplodeState

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
    pass
