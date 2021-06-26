import pygame
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

screen_width = 900
screen_height = 650
shelf_size = 512
dragging = False
stage = 0  # in stage 0, player can vodka and drag plants on shelf

# Initialize pygame
pygame.init()

# create window, width & height
screen = pygame.display.set_mode((screen_width, screen_height))
center_of_screen = (screen_width / 2, screen_height / 2)

# Background
background = pygame.image.load('Images/shelf1.png')
background_top_left = (center_of_screen[0] - shelf_size / 2, center_of_screen[1] - shelf_size / 2 + 40)

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


# Create trash can object
trash_can = TrashCan()

# Create next button object
next_button = NextButton()

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

        for event in pygame.event.get():
            # check if player wants to quit the game
            if event.type == pygame.QUIT:
                running = False
            # check if mouse is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # check if in collision with a good plant; i.e. player wants to drag a plant
                mouseX, mouseY = event.pos
                # if there is collision, keep dragging good plant
                for i in range(GoodPlant_length):
                    if GoodPlantList[i].check_good_collision(mouseX, mouseY):
                        dragging = True
                        dragged_type = "Good"
                        dragged_ind = i
                        GoodPlantList[i].drag_good_plant(mouseX, mouseY)

            # mouse up-- mouse click ends
            elif event.type == pygame.MOUSEBUTTONUP:
                # if dragging plant before, stop dragging
                if dragging:
                    dragging = False
                    # check to see if player has dragged plant to a trash can, if so, delete plant obj
                    for i in range(GoodPlant_length):
                        if GoodPlantList[i].check_trash_good_collision(trash_can):
                            # since the del function doesn't really do anything according to Google, let's just change the array length
                            GoodPlant_length -= 1
                            AllPlant_count -= 1
                            # make sure we delete the right object by shifting all objects after forward 1 spot
                            for j in range(i, GoodPlant_length):
                                GoodPlantList[j] = GoodPlantList[j + 1]

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
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouseX, mouseY = event.pos
                    if dragged_type == "Good":
                        GoodPlantList[dragged_ind].drag_good_plant(mouseX, mouseY)

        red = 0
        green = 255
        for i in range(len(shelf_rect_list)):
            pygame.draw.rect(screen, (red, green, 0), shelf_rect_list[i])
            red += 25
            green -= 25

        # show trash can on screen
        trash_can.show_trash_can(screen)
        # show next button on screen
        next_button.show_next_button(screen)
        # Show all good plants' image
        for i in range(GoodPlant_length):
            GoodPlantList[i].show_good_plant(screen)

    else: # for all other stages; place holder
        # Set background first; in loop b/c need constant display
        # RGB values, from 0 to 255
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            # check if player wants to quit the game
            if event.type == pygame.QUIT:
                running = False

    pygame.display.update()
