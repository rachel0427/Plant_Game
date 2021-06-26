import pygame
import random
import math
from pygame import mixer
from classes import *

global screen_width
global screen_height
global shelf_size
global dragging

screen_width = 800
screen_height = 600
shelf_size = 512
dragging = False

# Initialize pygame
pygame.init()

# create window, width & height
screen = pygame.display.set_mode((screen_width, screen_height))
center_of_screen = (screen_width / 2, screen_height / 2)

# Background
background = pygame.image.load('Images/shelf1.png')
background_top_left = (center_of_screen[0] - shelf_size / 2, center_of_screen[1] - shelf_size / 2)

# Title and Icon
pygame.display.set_caption("Plants of Grudge")
icon = pygame.image.load('Images/plantIcon.png')
pygame.display.set_icon(icon)

# Array for good_plant objects
good1 = GoodPlant(0, 0, 0, 0)
# GoodPlant = []

# running
running = True
while running:
    # Set background first; in loop b/c need constant display
    # RGB values, from 0 to 255
    screen.fill((255, 255, 255))

    # Background Image
    screen.blit(background, background_top_left)

    for event in pygame.event.get():
        # check if player wants to quit the game
        if event.type == pygame.QUIT:
            running = False
        # check if player wants to replace a plant
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if in collision with a good plant
            mouseX, mouseY = event.pos
            # if there is collision, keep dragging good plant
            if good1.check_good_collision(mouseX, mouseY):
                dragging = True
                good1.drag_good_plant(mouseX, mouseY)

        # mouse up-- stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        # if still dragging, make plant follow mouse pos
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouseX, mouseY = event.pos
                good1.drag_good_plant(mouseX, mouseY)

    good1.show_good_plant(screen)
    pygame.display.update()
