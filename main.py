import pygame

# Initialize pygame
pygame.init()

import random
import math
from pygame import mixer
from classes import *

global screen_width
global screen_height
global shelf_size
global dragging
global GoodPlant_length  # length of the GoodPlant array
global GreatPlant_length
global AwesomePlant_length
global AllPlant_count
global dragged_type
global dragged_ind
global stage  # stage keeps track of which page game is currently on
global chat_box_width
global chat_box_height
global big_grandpa_text_str
global big_grandpa_text
global big_grandpa_text_num
global delete
global round_produce
# global inLine
inLine = 0

screen_width = 900
screen_height = 650
shelf_size = 512
chat_box_width = 728
chat_box_height = 670
dragging = False
stage = 0  # in stage 0, player can vodka and drag plants on shelf
font = pygame.font.Font('Fonts/LazySunday-Regular.ttf', 32)
chat_font = pygame.font.Font('Fonts/LazySunday-Regular.ttf', 20)
largeText = pygame.font.Font('freesansbold.ttf', 100)
big_grandpa_text_num = 0
explodeImage = pygame.image.load('Images/explosion.jpg')
victoryImg = pygame.image.load('Images/trophy.png')
failImg = pygame.image.load('Images/fail.png')
shop_width = 900
shop_height = 600

# create window, width & height
screen = pygame.display.set_mode((screen_width, screen_height))
center_of_screen = (screen_width / 2, screen_height / 2)

# Background
background = pygame.image.load('Images/shelf1.png')
background_top_left = (center_of_screen[0] - shelf_size / 2, center_of_screen[1] - shelf_size / 2 + 40)

# shop background
shop_back = pygame.image.load('Images/fancy_shop.jpg')
shop_back_top_left = (center_of_screen[0] - shop_width / 2, center_of_screen[1] - shop_height / 2)

# chat box background
chat_box = pygame.image.load('Images/dialogue.jpg')
chat_box_top_left = (center_of_screen[0] - chat_box_width / 2, center_of_screen[1] - chat_box_height / 2)

# Background Sound
mixer.music.load('Sounds/05 - Loonboon.mp3')
pygame.mixer.music.set_volume(0.3)
mixer.music.play(-1)

# explosion sound
explosion_sound = mixer.Sound('Sounds/bomb.mp3')

# Title and Icon
pygame.display.set_caption("Plants of Wrath")
icon = pygame.image.load('Images/plantIcon.png')
pygame.display.set_icon(icon)

# Array for GoodPlant objects
GoodPlantList = []
GoodPlant_length = 0

# Array for great_plant objects
GreatPlantList = []
GreatPlant_length = 0

# Array for awesome_plant objects
AwesomePlantList = []
AwesomePlant_length = 0

# AllPlant_count keeps track of how many plants in total are present
AllPlant_count = GoodPlant_length + GreatPlant_length + AwesomePlant_length


# function for creating new good plants
def create_new_good_plant():
    global GoodPlant_length
    global AllPlant_count
    global inLine

    # determine pos_x by checking if another plant is present already
    # go through all plant instances on screen to see how many are on top of screen

    # Suppose we only have less than 11 plants in line
    pos_x = 10 + inLine * 70
    pos_y = 10
    shelf_pos = 0

    good_tmp = GoodPlant(pos_x, pos_y, shelf_pos)
    GoodPlantList.append(good_tmp)
    GoodPlant_length += 1
    AllPlant_count += 1
    inLine += 1


# function for creating new great plants
def create_new_great_plant():
    global GreatPlant_length
    global AllPlant_count
    global inLine

    pos_x = 10 + inLine * 70
    pos_y = 10
    shelf_pos = 0

    great_tmp = GreatPlant(pos_x, pos_y, shelf_pos)
    GreatPlantList.append(great_tmp)
    GreatPlant_length += 1
    AllPlant_count += 1
    inLine += 1


# function for creating new great plants
def create_new_awesome_plant():
    global AwesomePlant_length
    global AllPlant_count
    global inLine
    # determine pos_x by checking if another plant is present already
    # go through all plant instances on screen to see how many are on top of screen
    # FIXME: here? inline?
    # Suppose we only have less than 11 plants in line
    pos_x = 10 + inLine * 70
    pos_y = 10
    shelf_pos = 0

    awesome_tmp = AwesomePlant(pos_x, pos_y, shelf_pos)
    AwesomePlantList.append(awesome_tmp)
    AwesomePlant_length += 1
    AllPlant_count += 1
    inLine += 1


def show_text_in_box(surface, font, x_start, x_end, y_start, text, colour):
    x = x_start
    y = y_start
    words = text.split(' ')

    for word in words:
        word_t = font.render(word, True, colour)
        if word_t.get_width() + x <= x_end:
            surface.blit(word_t, (x, y))
            x += word_t.get_width() + 2
        else:
            y += word_t.get_height() + 4
            x = x_start
            surface.blit(word_t, (x, y))
            x += word_t.get_width() + 2


# method for displaying image
def image_draw(window, image, pos_x, pos_y, time):
    while time > 0:
        print("displaying")
        window.blit(image, (pos_x, pos_y))
        time -= 1
    print("ended")


# Create bank object
bank = Bank()

# Create fancy shop object
fancy_shop = FancyShop()

# create a temporary instance of each plant (not included in array)
tmp_good = GoodPlant(200, 250, 0)
tmp_great = GreatPlant(400, 250, 0)
tmp_awe = AwesomePlant(600, 250, 0)

tmp_good2 = GoodPlant(10, 10, 0)
tmp_great2 = GreatPlant(310, 10, 0)
tmp_awe2 = AwesomePlant(610, 10, 0)

good_plus = PlusSign(190, 330)
great_plus = PlusSign(390, 330)
awe_plus = PlusSign(590, 330)

good_minus = MinusSign(250, 330)
great_minus = MinusSign(450, 330)
awe_minus = MinusSign(650, 330)

# render font for plant buy prices:
good_price = font.render(str(GoodPrice), True, (0, 0, 0))
great_price = font.render(str(GreatPrice), True, (0, 0, 0))
awesome_price = font.render(str(AwesomePrice), True, (0, 0, 0))

# render sell price
good_sell = font.render("Sell For: " + str(SellGood), True, (0, 0, 0))
great_sell = font.render("Sell For: "+str(SellGreat), True, (0, 0, 0))
awesome_sell = font.render("Sell For:"+str(SellAwesome), True, (0, 0, 0))

# render production for each plant
good_round_pro = font.render("Produce Roundly: " + str(GoodProduce), True, (0, 0, 0))
great_round_pro = font.render("Produce Roundly: "+str(GreatProduce), True, (0, 0, 0))
awesome_round_pro = font.render("Produce Roundly: "+str(AwesomeProduce), True, (0, 0, 0))

# round produce
round_produce = 0

# Create round counter
round_counter = RoundCounter()

# Create trash can object
trash_can = TrashCan()

# Create shopping cart object
my_cart = Cart()

# Create next button object
next_button = NextButton()

# Create mood bubble object
mood_bubble = MoodBubble()

# Create vodka
vodka = VodkaBottle()

# vodka count
vodka_count = VodkaCount()

# Create big grandpa object
big_grandpa = BigGrandpa()

# array for big grandpa's text
big_grandpa_text_str = ["Hello there! I am known as BIG GRANDPA, and I am proposing "
                        "a challenge.If you, my friend, can complete this challenge, "
                        "you will earn the grand opportunity of being my slave forever! "
                        "MEOW HAHAHAHAHAHA! Now, click anywhere to see the rules of my challenge. ",
                        "Your goal is to earn 5000 from buying and selling plants "
                        "within 8 rounds. During each round, you can move your plants "
                        "up or down the shelf, or you can throw them away. Be aware that moving "
                        "a plant down the shelf will make it angry, while moving it up "
                        "makes it happy. ",
                        "At the end of each round, plants that remains on the 1st level gets "
                        "happier, plants on the 2nd level keeps a steady mood, and plants on the "
                        "3rd level gets angrier. Horrible things will happen if your plants get mad! "
                        "But being generous as I am, I am giving you my plants’ favorite thing - "
                        "VODKA! It always makes them happy.", "You can now proceed to selling and buying "
                        "plants. God bless you!"]

big_grandpa_text = [font.render(big_grandpa_text_str[0], True, (0, 0, 0)),
                    font.render(big_grandpa_text_str[1], True, (0, 0, 0)),
                    font.render(big_grandpa_text_str[2], True, (0, 0, 0)),
                    font.render(big_grandpa_text_str[3], True, (0, 0, 0))]

# Create 3 good plants
for i in range(3):
    create_new_good_plant()

# running
running = True

explode = False

while running:
    if stage == 0:
        # Set background first; in loop b/c need constant display
        # RGB values, from 0 to 255
        screen.fill((255, 255, 255))

        # Background Image
        screen.blit(background, background_top_left)

        # Show money
        bank.show_money(screen)
        # display round number
        round_counter.show_round_num(screen)
        vodka_count.show_num(screen)

        # Display mood Bubble if mouse is hovering over a plant
        # that has already been placed on shelf
        tmp = 0
        while tmp < GoodPlant_length:
            # check for explode
            if GoodPlantList[tmp].explode():
                explode = True
                GoodPlant_length -= 1
                AllPlant_count -= 1
                GoodPlantList[tmp].clear_shelf()
                explode_x = GoodPlantList[tmp].pos_x
                explode_y = GoodPlantList[tmp].pos_y
                # make sure we delete the right object by shifting all objects after forward 1 spot
                GoodPlantList.pop(tmp)

            else:
                tmp += 1

        tmp = 0
        while tmp < GreatPlant_length:
            # check for explode
            if GreatPlantList[tmp].explode():
                explode = True
                GreatPlant_length -= 1
                AllPlant_count -= 1
                GreatPlantList[tmp].clear_shelf()
                explode_x = GreatPlantList[tmp].pos_x
                explode_y = GreatPlantList[tmp].pos_y
                # make sure we delete the right object by shifting all objects after forward 1 spot
                GreatPlantList.pop(tmp)

            else:
                tmp += 1

        tmp = 0
        while tmp < AwesomePlant_length:
            # check for explode
            if AwesomePlantList[tmp].explode():
                explode = True
                AwesomePlant_length -= 1
                AllPlant_count -= 1
                AwesomePlantList[tmp].clear_shelf()
                explode_x = AwesomePlantList[tmp].pos_x
                explode_y = AwesomePlantList[tmp].pos_y
                # make sure we delete the right object by shifting all objects after forward 1 spot
                AwesomePlantList.pop(tmp)

            else:
                tmp += 1

        for i in range(GoodPlant_length):
            if GoodPlantList[i].check_mouse_on_good(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
                    and GoodPlantList[i].on_shelf:
                mood_bubble.show_mood(screen, GoodPlantList[i].pos_x, GoodPlantList[i].pos_y,
                                      GoodPlantList[i].anger_level)

        for i in range(GreatPlant_length):
            # if plant is placed on shelf, display mood when mouse is over plant
            if GreatPlantList[i].check_mouse_on_great(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
                    and GreatPlantList[i].on_shelf:
                mood_bubble.show_mood(screen, GreatPlantList[i].pos_x, GreatPlantList[i].pos_y,
                                      GreatPlantList[i].anger_level)

        for i in range(AwesomePlant_length):
            # if plant is placed on shelf, display mood when mouse is over plant
            if AwesomePlantList[i].check_mouse_on_awesome(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
                    and AwesomePlantList[i].on_shelf:
                mood_bubble.show_mood(screen, AwesomePlantList[i].pos_x, AwesomePlantList[i].pos_y,
                                      AwesomePlantList[i].anger_level)

        for event in pygame.event.get():
            # check if player wants to quit the game
            if event.type == pygame.QUIT:
                running = False

            # check if mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # check if in collision with a good plant; i.e. player wants to drag a plant
                mouseX, mouseY = event.pos
                # if there is collision, keep dragging good plant
                for i in range(GoodPlant_length):
                    if GoodPlantList[i].check_good_collision(mouseX, mouseY):
                        dragging = True
                        dragged_type = "Good"
                        dragged_ind = i
                        GoodPlantList[i].clear_shelf()
                        GoodPlantList[i].drag_good_plant(mouseX, mouseY)

                # FIXME: needed???
                if not dragging:
                    for i in range(GreatPlant_length):
                        if GreatPlantList[i].check_great_collision(mouseX, mouseY):
                            dragging = True
                            dragged_type = "Great"
                            dragged_ind = i
                            GreatPlantList[i].clear_shelf()
                            GreatPlantList[i].drag_great_plant(mouseX, mouseY)

                if not dragging:
                    for i in range(AwesomePlant_length):
                        if AwesomePlantList[i].check_awesome_collision(mouseX, mouseY):
                            dragging = True
                            dragged_type = "Awesome"
                            dragged_ind = i
                            AwesomePlantList[i].clear_shelf()
                            AwesomePlantList[i].drag_awesome_plant(mouseX, mouseY)

                if vodka.check_vodka_collision(mouseX, mouseY):
                    dragging = True
                    dragged_type = "Vodka"

            # mouse up-- mouse click ends
            if event.type == pygame.MOUSEBUTTONUP:
                # if dragging plant before, stop dragging
                if dragging:
                    dragging = False

                    # see which type of item is being dragged
                    if dragged_type == "Good":
                        delete = False
                        # check to see if player has dragged plant to a trash can, if so, delete plant obj
                        if GoodPlantList[dragged_ind].check_trash_good_collision(trash_can):
                            # since the del function doesn't really do anything according to Google,
                            # let's just change the array length
                            delete = True
                            GoodPlant_length -= 1
                            AllPlant_count -= 1
                            GoodPlantList.pop(dragged_ind)

                        # end of for loop; if plant not deleted
                        if not delete:
                            GoodPlantList[dragged_ind].correct_good_pos()

                    elif dragged_type == "Great":
                        delete = False
                        # check to see if player has dragged plant to a trash can, if so, delete plant obj
                        if GreatPlantList[dragged_ind].check_trash_great_collision(trash_can):
                            # since the del function doesn't really do anything according to Google,
                            # let's just change the array length
                            delete = True
                            GreatPlant_length -= 1
                            AllPlant_count -= 1
                            # make sure we delete the right object by shifting all objects after forward 1 spot

                            GreatPlantList.pop(dragged_ind)

                        # end of for loop; if plant not deleted
                        if not delete:
                            GreatPlantList[dragged_ind].correct_great_pos()

                    elif dragged_type == "Awesome":
                        delete = False
                        # check to see if player has dragged plant to a trash can, if so, delete plant obj
                        if AwesomePlantList[dragged_ind].check_trash_awesome_collision(trash_can):
                            # since the del function doesn't really do anything according to Google,
                            # let's just change the array length
                            delete = True
                            AwesomePlant_length -= 1
                            AllPlant_count -= 1
                            # make sure we delete the right object by shifting all objects after forward 1 spot
                            AwesomePlantList.pop(dragged_ind)

                        # end of for loop; if plant not deleted
                        if not delete:
                            AwesomePlantList[dragged_ind].correct_awesome_pos()

                    elif dragged_type == "Vodka":
                        if len(GoodPlantList) > 0:
                            vodka.check_plant_vodka_collision(GoodPlantList, vodka_count)
                        if len(GreatPlantList) > 0:
                            vodka.check_plant_vodka_collision(GreatPlantList, vodka_count)
                        if len(AwesomePlantList) > 0:
                            vodka.check_plant_vodka_collision(AwesomePlantList, vodka_count)

                # if not dragging before, check if clicked on the next button
                else:
                    mouseX, mouseY = event.pos
                    if next_button.check_next_collision(mouseX, mouseY):
                        stage += 1
                        # clear all plants on top
                        inLine = 0
                        i = 0
                        while i < GoodPlant_length:
                            if GoodPlantList[i].pos_y < 20:
                                GoodPlant_length -= 1
                                AllPlant_count -= 1
                                # make sure we delete the right object by shifting all objects after forward 1 spot
                                GoodPlantList.pop(i)
                                # keep i constant
                            else:
                                i += 1

                        i = 0
                        while i < GreatPlant_length:
                            if GreatPlantList[i].pos_y < 20:
                                GreatPlant_length -= 1
                                AllPlant_count -= 1
                                # make sure we delete the right object by shifting all objects after forward 1 spot
                                GreatPlantList.pop(i)
                                # keep i constant
                            else:
                                i += 1

                        i = 0
                        while i < AwesomePlant_length:
                            if AwesomePlantList[i].pos_y < 20:
                                AwesomePlant_length -= 1
                                AllPlant_count -= 1
                                # make sure we delete the right object by shifting all objects after forward 1 spot
                                AwesomePlantList.pop(i)
                                # keep i constant
                            else:
                                i += 1

            # if still dragging, make plant follow mouse pos
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouseX, mouseY = event.pos
                    if dragged_type == "Good":
                        GoodPlantList[dragged_ind].drag_good_plant(mouseX, mouseY)
                    elif dragged_type == "Vodka":
                        vodka.drag_vodka_bottle(mouseX, mouseY, vodka_count)
                    elif dragged_type == "Great":
                        GreatPlantList[dragged_ind].drag_great_plant(mouseX, mouseY)
                    elif dragged_type == "Awesome":
                        AwesomePlantList[dragged_ind].drag_awesome_plant(mouseX, mouseY)

        if explode:
            clock = pygame.time.Clock()
            clock.tick(1)
            # TODO: fix display position
            explosion_sound.play()
            screen.blit(explodeImage, (center_of_screen[0] - 300, center_of_screen[1] - 225))
            pygame.display.update()
            pygame.time.delay(1500)
            bank.money -= 200
            explode = False

        # show trash can on screen
        trash_can.show_trash_can(screen)
        # show next button on screen
        next_button.show_next_button(screen)
        # Show all good plants' image
        for i in range(GoodPlant_length):
            GoodPlantList[i].show_good_plant(screen)
        # show all great plants image
        for i in range(GreatPlant_length):
            GreatPlantList[i].show_great_plant(screen)
        # show all great plants image
        for i in range(AwesomePlant_length):
            AwesomePlantList[i].show_awesome_plant(screen)
        # show vodka bottle on screen
        vodka.show_vodka_image(screen)

    elif stage == 1:  # for all other stages; place holder
        # Set background first; in loop b/c need constant display
        # RGB values, from 0 to 255
        screen.fill((255, 255, 255))

        # check if reached end of game, total 8 rounds
        if round_counter.round_num + 1 == 9:
            stage = 4

        # show all messages from big grandpa
        if big_grandpa_text_num < len(big_grandpa_text):
            # show chat box
            screen.blit(chat_box, chat_box_top_left)

            big_grandpa.show_big_grandpa_font(screen)

            # show message
            show_text_in_box(screen, font, 250, 780, 170,
                             big_grandpa_text_str[big_grandpa_text_num], (0, 0, 0))

            for event in pygame.event.get():
                # check if player wants to quit the game
                if event.type == pygame.QUIT:
                    running = False
                # check if mouse is clicked to proceed to next message
                if event.type == pygame.MOUSEBUTTONUP:
                    if big_grandpa_text_num < len(big_grandpa_text):
                        big_grandpa_text_num += 1

        # suppose all messages have been shown
        # display the same page as stage 0 just with a cart instead of trash can
        else:
            # Background Image
            screen.blit(background, background_top_left)

            # Show money
            bank.show_money(screen)
            # display round number
            round_counter.show_round_num(screen)

            # show sell price
            screen.blit(good_sell, (75, 10))
            screen.blit(great_sell, (375, 10))
            screen.blit(awesome_sell, (670, 10))

            # show production each plant
            screen.blit(good_round_pro, (75, 40))
            screen.blit(great_round_pro, (375, 40))
            screen.blit(awesome_round_pro, (670, 40))

            # show 3 plants on top
            tmp_good2.show_good_plant(screen)
            tmp_great2.show_great_plant(screen)
            tmp_awe2.show_awesome_plant(screen)

            # Display mood Bubble if mouse is hovering over a plant
            # that has already been placed on shelf
            for i in range(GoodPlant_length):
                plant = GoodPlantList[i]
                # if plant is placed on shelf, display mood when mouse is over plant
                if plant.check_mouse_on_good(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
                        and plant.on_shelf:
                    mood_bubble.show_mood(screen, plant.pos_x, plant.pos_y, plant.anger_level)

            for i in range(GreatPlant_length):
                plant = GreatPlantList[i]
                # if plant is placed on shelf, display mood when mouse is over plant
                if plant.check_mouse_on_great(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
                        and plant.on_shelf:
                    mood_bubble.show_mood(screen, plant.pos_x, plant.pos_y, plant.anger_level)

            for i in range(AwesomePlant_length):
                plant = AwesomePlantList[i]
                # if plant is placed on shelf, display mood when mouse is over plant
                if plant.check_mouse_on_awesome(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
                        and plant.on_shelf:
                    mood_bubble.show_mood(screen, plant.pos_x, plant.pos_y, plant.anger_level)

            for event in pygame.event.get():
                # check if player wants to quit the game
                if event.type == pygame.QUIT:
                    running = False

                # check if mouse is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check if in collision with a good plant; i.e. player wants to drag a plant
                    mouseX, mouseY = event.pos
                    # if there is collision, keep dragging good plant
                    for i in range(GoodPlant_length):
                        if GoodPlantList[i].check_good_collision(mouseX, mouseY):
                            dragging = True
                            dragged_type = "Good"
                            dragged_ind = i
                            GoodPlantList[i].clear_shelf()
                            GoodPlantList[i].drag_good_plant(mouseX, mouseY)

                    # if there is collision, keep dragging good plant
                    for i in range(GreatPlant_length):
                        if GreatPlantList[i].check_great_collision(mouseX, mouseY):
                            dragging = True
                            dragged_type = "Great"
                            dragged_ind = i
                            GreatPlantList[i].clear_shelf()
                            GreatPlantList[i].drag_great_plant(mouseX, mouseY)

                    # if there is collision, keep dragging good plant
                    for i in range(AwesomePlant_length):
                        if AwesomePlantList[i].check_awesome_collision(mouseX, mouseY):
                            dragging = True
                            dragged_type = "Awesome"
                            dragged_ind = i
                            AwesomePlantList[i].clear_shelf()
                            AwesomePlantList[i].drag_awesome_plant(mouseX, mouseY)

                # mouse up-- mouse click ends
                if event.type == pygame.MOUSEBUTTONUP:
                    # if dragging plant before, stop dragging
                    if dragging:
                        dragging = False
                        # TODO: added this if statement, don't know if its right
                        if dragged_type == "Good":
                            in_cart = False
                            # check to see if player has dragged plant to a trash can, if so, delete plant obj
                            # FIXME: can just use len(GoodPlantList)
                            if GoodPlantList[dragged_ind].check_cart_good_collision(my_cart):
                                # since the del function doesn't really do anything according to Google,
                                # let's just change the array length
                                in_cart = True
                                GoodPlant_length -= 1
                                AllPlant_count -= 1
                                # make sure we delete the right object by shifting all objects after forward 1 spot
                                GoodPlantList.pop(dragged_ind)
                                # increase bank deposit
                                bank.sell_good_plant()

                            # end of for loop; if plant not sold
                            if not in_cart:
                                GoodPlantList[dragged_ind].correct_good_pos()

                        elif dragged_type == "Great":
                            in_cart = False
                            # check to see if player has dragged plant to a trash can, if so, delete plant obj
                            if GreatPlantList[dragged_ind].check_cart_great_collision(my_cart):
                                # since the del function doesn't really do anything according to Google,
                                # let's just change the array length
                                in_cart = True
                                GreatPlant_length -= 1
                                AllPlant_count -= 1
                                # make sure we delete the right object by shifting all objects after forward 1 spot
                                GreatPlantList.pop(dragged_ind)
                                # increase bank deposit
                                bank.sell_great_plant()

                            # end of for loop; if plant not sold
                            if not in_cart:
                                GreatPlantList[dragged_ind].correct_great_pos()

                        elif dragged_type == "Awesome":
                            in_cart = False
                            # check to see if player has dragged plant to a trash can, if so, delete plant obj
                            if AwesomePlantList[dragged_ind].check_cart_awesome_collision(my_cart):
                                # since the del function doesn't really do anything according to Google,
                                # let's just change the array length
                                in_cart = True
                                AwesomePlant_length -= 1
                                AllPlant_count -= 1
                                # make sure we delete the right object by shifting all objects after forward 1 spot
                                AwesomePlantList.pop(dragged_ind)
                                # increase bank deposit
                                bank.sell_awesome_plant()

                            # end of for loop; if plant not sold
                            if not in_cart:
                                AwesomePlantList[dragged_ind].correct_awesome_pos()

                    # if not dragging before, check if clicked on the next button
                    else:
                        mouseX, mouseY = event.pos
                        if next_button.check_next_collision(mouseX, mouseY):
                            stage += 1
                            # clear shop
                            fancy_shop.clear_shop()
                            # roundly production
                            round_produce = 0
                            for i in range(GoodPlant_length):
                                bank.good_produce()
                                round_produce += GoodProduce
                            for i in range(GreatPlant_length):
                                bank.great_produce()
                                round_produce += GreatProduce
                            for i in range(AwesomePlant_length):
                                bank.awesome_produce()
                                round_produce += AwesomeProduce


                # if still dragging, make plant follow mouse pos
                if event.type == pygame.MOUSEMOTION:
                    if dragging:
                        mouseX, mouseY = event.pos
                        if dragged_type == "Good":
                            GoodPlantList[dragged_ind].drag_good_plant(mouseX, mouseY)
                        elif dragged_type == "Great":
                            GreatPlantList[dragged_ind].drag_great_plant(mouseX, mouseY)
                        elif dragged_type == "Awesome":
                            AwesomePlantList[dragged_ind].drag_awesome_plant(mouseX, mouseY)
                        elif dragged_type == "Vodka":  # TODO: here
                            vodka.drag_vodka_bottle(mouseX, mouseY, vodka_count)

            # show trash can on screen
            my_cart.show_cart(screen)
            # show next button on screen
            next_button.show_next_button(screen)
            # show big grandpa
            # show big grandpa
            big_grandpa.pos_y = 300
            big_grandpa.pos_x = 0
            big_grandpa.font_x = 0
            big_grandpa.font_y = 260
            big_grandpa.show_big_grandpa_font(screen)
            # Show all good plants' image
            for i in range(GoodPlant_length):
                GoodPlantList[i].show_good_plant(screen)
            # Show all great plants' image
            for i in range(GreatPlant_length):
                GreatPlantList[i].show_great_plant(screen)
            # Show all awesome plants' image
            for i in range(AwesomePlant_length):
                AwesomePlantList[i].show_awesome_plant(screen)

    elif stage == 2:
        # Set background first; in loop b/c need constant display
        # RGB values, from 0 to 255
        screen.fill((255, 255, 255))

        screen.blit(shop_back, shop_back_top_left)

        fancy_shop.show_fancy_shop(screen)

        # show 3 plants on rectangle
        tmp_good.show_good_plant(screen)
        tmp_great.show_great_plant(screen)
        tmp_awe.show_awesome_plant(screen)

        # show plus sign
        good_plus.show_plus_sign(screen)
        great_plus.show_plus_sign(screen)
        awe_plus.show_plus_sign(screen)

        # show minus sign
        good_minus.show_minus_sign(screen)
        great_minus.show_minus_sign(screen)
        awe_minus.show_minus_sign(screen)

        # show price on top
        screen.blit(good_price, (220, 220))
        screen.blit(great_price, (420, 220))
        screen.blit(awesome_price, (620, 220))

        for event in pygame.event.get():
            # check if player wants to quit the game
            if event.type == pygame.QUIT:
                running = False
            # check if proceed to next round
            if event.type == pygame.MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                if good_plus.check_plus_collision(mouseX, mouseY):
                    good_plus.get_good_plant(fancy_shop, bank)
                elif great_plus.check_plus_collision(mouseX, mouseY):
                    great_plus.get_great_plant(fancy_shop, bank)
                elif awe_plus.check_plus_collision(mouseX, mouseY):
                    awe_plus.get_awesome_plant(fancy_shop, bank)
                elif good_minus.check_minus_collision(mouseX, mouseY):
                    good_minus.reduce_good_plant(fancy_shop, bank)
                elif great_minus.check_minus_collision(mouseX, mouseY):
                    great_minus.reduce_great_plant(fancy_shop, bank)
                elif awe_minus.check_minus_collision(mouseX, mouseY):
                    awe_minus.reduce_awesome_plant(fancy_shop, bank)

                elif next_button.check_next_collision(mouseX, mouseY):
                    # plant mood increase:
                    for i in range(GoodPlant_length):
                        GoodPlantList[i].new_round_update()
                    for plant in GreatPlantList:
                        plant.new_round_update()
                    for plant in AwesomePlantList:
                        plant.new_round_update()
                    # increase round number
                    round_counter.increase_round_num()
                    stage = 0

                    # player done purchasing:
                    for i in range(fancy_shop.good_plant_purchase):
                        create_new_good_plant()
                    for i in range(fancy_shop.great_plant_purchase):
                        create_new_great_plant()
                    for i in range(fancy_shop.awesome_plant_purchase):
                        create_new_awesome_plant()

        # display round number
        round_counter.show_round_num(screen)
        bank.show_money(screen)
        # show big grandpa
        big_grandpa.pos_y = 460
        big_grandpa.font_y = 420
        big_grandpa.pos_x = 150
        big_grandpa.font_x = 150
        big_grandpa.show_big_grandpa_font(screen)
        # show round produce
        round_produce_display = font.render("Roundly Produce: " + str(round_produce), True, (0, 0, 0))
        screen.blit(round_produce_display,(0,0))
        next_button.show_next_button(screen)

    elif stage == 4:
        for event in pygame.event.get():
            # check if player wants to quit the game
            if event.type == pygame.QUIT:
                running = False

        if bank.money >= 5000:
            screen.blit(victoryImg, (0, 0))
            text = largeText.render("YOU WON!", True, (201, 147, 212))
            screen.blit(text, (200, 300))
        else:
            screen.blit(failImg, (0, 0))
            text = largeText.render("YOU FAILED!", True, (255, 0, 0))
            screen.blit(text, (150, 300))

    pygame.display.update()
