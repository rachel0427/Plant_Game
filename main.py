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

screen_width = 900
screen_height = 650
shelf_size = 512
chat_box_width = 728
chat_box_height = 670
dragging = False
stage = 0  # in stage 0, player can vodka and drag plants on shelf
font = pygame.font.Font('Fonts/LazySunday-Regular.ttf', 32)
big_grandpa_text_num = 0

# create window, width & height
screen = pygame.display.set_mode((screen_width, screen_height))
center_of_screen = (screen_width / 2, screen_height / 2)

# Background
background = pygame.image.load('Images/shelf1.png')
background_top_left = (center_of_screen[0] - shelf_size / 2, center_of_screen[1] - shelf_size / 2 + 40)

# chat box background
chat_box = pygame.image.load('Images/dialogue.jpg')
chat_box_top_left = (center_of_screen[0] - chat_box_width / 2, center_of_screen[1] - chat_box_height / 2)

# Title and Icon
pygame.display.set_caption("Plants of Wrath")
icon = pygame.image.load('Images/plantIcon.png')
pygame.display.set_icon(icon)

# Array for good_plant objects
GoodPlantList = []
GoodPlant_length = len(GoodPlantList)

# AllPlant_count keeps track of how many plants in total are present
AllPlant_count = GoodPlant_length


# function for creating new good plants
def create_new_good_plant():
    global GoodPlant_length
    global AllPlant_count
    # determine pos_x by checking if another plant is present already
    # go through all plant instances on screen to see how many are on top of screen
    inLine = 0
    for i in range(GoodPlant_length):
        if GoodPlantList[i].pos_y < 113:
            inLine += 1
    # Suppose we only have less than 11 plants in line
    pos_x = 10 + inLine * 70
    pos_y = 10
    shelf_pos = 0

    good_tmp = GoodPlant(pos_x, pos_y, shelf_pos)
    GoodPlantList.append(good_tmp)
    GoodPlant_length += 1
    AllPlant_count += 1


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


# Create bank object
bank = Bank()

# Create trash can object
trash_can = TrashCan()

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
big_grandpa_text_str = ["Important Message1: Lorem ipsum dolor sit amet, consectetur "
                        "adipiscing elit, sed do eiusmod tempor incididunt ut labore "
                        "et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
                        "exercitation ullamco laboris nisi ut aliquip ex ea commodo "
                        "consequat.",
                        "Important Message2: Duis aute irure dolor in reprehenderit "
                        "in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                        "Excepteur sint occaecat cupidatat non proident, sunt in culpa "
                        "qui officia deserunt mollit anim id est laborum?"]
big_grandpa_text = [font.render(big_grandpa_text_str[0], True, (0, 0, 0)),
                    font.render(big_grandpa_text_str[1], True, (0, 0, 0))]

# Create 3 good plants
for i in range(3):
    create_new_good_plant()

# running
running = True

while running:
    if stage == 0:
        # Set background first; in loop b/c need constant display
        # RGB values, from 0 to 255
        screen.fill((255, 255, 255))

        # Background Image
        screen.blit(background, background_top_left)

        # show colors for blocks
        red = 0
        green = 255
        for i in range(len(shelf_rect_list)):
            pygame.draw.rect(screen, (red, green, 0), shelf_rect_list[i])
            red += 25
            green -= 25

        # Show money
        bank.show_money(screen)
        vodka_count.show_num(screen)

        # Display mood Bubble if mouse is hovering over a plant
        # that has already been placed on shelf
        for plant in GoodPlantList:
            plant.initialize_anger()
            if plant.check_mouse_on_plant(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])\
                    and plant.on_shelf:
                mood_bubble.show_bubble(screen, plant.pos_x, plant.pos_y, plant.anger_level)

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

                if vodka.check_vodka_collision(mouseX, mouseY):
                    dragging = True
                    dragged_type = "Vodka"
                    print("hoho")

            # mouse up-- mouse click ends
            if event.type == pygame.MOUSEBUTTONUP:
                # if dragging plant before, stop dragging
                if dragging:
                    dragging = False
                    # TODO: added this if statement, don't know if its right
                    if dragged_type == "Good":
                        delete = False
                        # check to see if player has dragged plant to a trash can, if so, delete plant obj
                        # FIXME: can just use len(GoodPlantList)
                        for i in range(GoodPlant_length):
                            if GoodPlantList[i].check_trash_good_collision(trash_can):
                                # since the del function doesn't really do anything according to Google,
                                # let's just change the array length
                                delete = True
                                GoodPlant_length -= 1
                                AllPlant_count -= 1
                                # make sure we delete the right object by shifting all objects after forward 1 spot
                                for j in range(i, GoodPlant_length):
                                    GoodPlantList[j] = GoodPlantList[j + 1]
                                break  # break out of for loop

                        # end of for loop; if plant not deleted
                        if ~delete:
                            GoodPlantList[dragged_ind].correct_good_pos()

                    elif dragged_type == "Vodka":
                        vodka.check_plant_vodka_collision(GoodPlantList, vodka_count)

                # if not dragging before, check if clicked on the next button
                else:
                    mouseX, mouseY = event.pos
                    if next_button.check_next_collision(mouseX, mouseY):
                        # if stage != 2
                        if stage < 2:
                            stage += 1
                        else:
                            stage = 0

            # if still dragging, make plant follow mouse pos
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouseX, mouseY = event.pos
                    if dragged_type == "Good":
                        GoodPlantList[dragged_ind].drag_good_plant(mouseX, mouseY)
                    elif dragged_type == "Vodka":  # TODO: here
                        vodka.drag_vodka_bottle(mouseX, mouseY, vodka_count)

        # show trash can on screen
        trash_can.show_trash_can(screen)
        # show next button on screen
        next_button.show_next_button(screen)
        # Show all good plants' image
        for i in range(GoodPlant_length):
            GoodPlantList[i].show_good_plant(screen)
        # show vodka bottle on screen
        vodka.show_vodka_image(screen)

    else:  # for all other stages; place holder
        # Set background first; in loop b/c need constant display
        # RGB values, from 0 to 255
        screen.fill((255, 255, 255))

        # show all messages from big grandpa
        if big_grandpa_text_num < len(big_grandpa_text):
            # show chat box
            screen.blit(chat_box, chat_box_top_left)

            # show big grandpa
            big_grandpa.show_big_grandpa_font(screen),

            # show message
            show_text_in_box(screen, font, 250, 780, 170,
                             big_grandpa_text_str[big_grandpa_text_num], (0, 0, 0))
            #screen.blit(big_grandpa_text[big_grandpa_text_num], (0, 0))

            for event in pygame.event.get():
                # check if player wants to quit the game
                if event.type == pygame.QUIT:
                    running = False
                # check if mouse is clicked to proceed to next message
                if event.type == pygame.MOUSEBUTTONUP:
                    if big_grandpa_text_num < len(big_grandpa_text):
                        big_grandpa_text_num += 1

        for event in pygame.event.get():
            # check if player wants to quit the game
            if event.type == pygame.QUIT:
                running = False

    pygame.display.update()
