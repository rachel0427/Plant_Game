import pygame
import math
from pygame import mixer

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
Plant1Image = 'Images/goodPlant.png'
Plant2Image = 'Images/greatPlant.png'
Plant3Image = 'Images/awesomePlant.png'
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
Sell1 = 20
Sell2 = 30
Sell3 = 40
SellLeek = 50

Produce1 = 50
Produce2 = 60
Produce3 = 100
LeekProduce = 40

Price1 = 20
Price2 = 30
Price3 = 50

ProduceCycle1 = 1
ProduceCycle2 = 1
ProduceCycle3 = 1
LeekProduceCycle = 1

# font
font = pygame.font.Font('freesansbold.ttf', 32)


class Plant:

    anger_level = 0
    on_shelf = False
    shelf_pos_cur = 0
    shelf_pos_prev = 0
    first_time_on_shelf = True

    def __init__(self, pos_x, pos_y, img):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.init_x = pos_x
        self.init_y = pos_y
        self.img = pygame.image.load(img)

    def show_plant(self, window):
        window.blit(self.img, (self.pos_x, self.pos_y))

    def drink_vodka(self):
        self.anger_level = 0

    def decrease_anger(self):
        self.anger_level -= 1

    def increase_anger(self):
        self.anger_level += 1

    def check_mouse_collision(self):
        pass

    def drag_plant(self):
        pass

    def check_trash_collision(self):
        pass

    def check_cart_collision(self):
        pass

    def check_mouse_over_plant(self):
        pass


class Plant1(Plant):

    sell_price = 30
    production = 40

    def __init__(self, pos_x, pos_y, img):
        super().__init__(pos_x, pos_y, img)




