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

    def check_mouse_collision(self, mouse_x, mouse_y):
        """
        This function checks for collision between mouse and plant
        :param mouse_x: x coord of mouse pos
        :param mouse_y: y coord of mouse pos
        :return: boolean val of whether collision occurred
        """
        # get a rectangle the size of img
        rectangle = self.img.get_rect()
        # place the rectangle so that its top left corner is placed at (pos_x, pos_y)
        rectangle.topleft = (self.pos_x, self.pos_y)
        # check for collision with the collidepoint() function
        if rectangle.collidepoint(mouse_x, mouse_y):
            return True
        return False

    def drag_plant(self, mouse_x, mouse_y):
        """
        This function makes plant follow mouse position
        :param mouse_x: x coord of mouse position
        :param mouse_y: y coord of mouse position
        :return:
        """
        self.pos_x = mouse_x - plant_size / 2
        self.pos_y = mouse_y - plant_size / 2

    def check_trash_collision(self, trash_obj):
        """
        This function checks for collision with trash can
        :param trash_obj: trash can object
        :return: boolean val of whether trash can and plant collided
        """
        # This is how you check for collision between trash can and plant objects
        distance = math.sqrt(
            math.pow((trash_obj.pos_x - self.pos_x), 2) + math.pow((trash_obj.pos_y - self.pos_y), 2))
        if distance < 57:
            return True
        return False

    def check_cart_collision(self, cart_obj):
        """
        This function checks for collision with shopping cart
        :param cart_obj: cart object
        :return: boolean val of whether trash can and plant object collided
        """
        # This is how you check for collision between cart and plant objects
        distance = math.sqrt(
            math.pow((cart_obj.pos_x - self.pos_x), 2) + math.pow((cart_obj.pos_y - self.pos_y), 2))
        if distance < 57:
            return True
        return False

    def check_mouse_over_plant(self, mouse_x, mouse_y):
        """
        This function checks if mouse is on this plant
        :param mouse_x: x coord of mouse position
        :param mouse_y: y coord of mouse position
        :return: boolean val of whether mouse is placed on plant image
        """
        # same as above
        rectangle = self.img.get_rect()
        rectangle.topleft = (self.pos_x, self.pos_y)
        if rectangle.collidepoint(mouse_x, mouse_y):
            return True
        return False

    def correct_plant_pos(self):
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

    def clear_shelf(self):
        """
        This function resets shelf grid to empty when plant dragged away,
        called when mouse button down
        """
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
        This function evaluates the current and previous shelf position of
        the plant and updates plant's anger_level based on the movement
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
        This function checks whether plant need to explode
        :return: boolean value of whether plant need to explode
        """
        return self.anger_level >= 3

    def change_position(self, end_pos_x, end_pos_y):
        """
        alters plant pos
        :param end_pos_x: x coord of place where plant need to be moved
        :param end_pos_y: y coord of place where plant need to be moved
        """
        self.pos_x = end_pos_x
        self.pos_y = end_pos_y

    def new_round_update(self):
        """
        This function updates plant mood once new round is reached
        :return:
        """
        level = int(self.shelf_pos_cur / 3)
        if level == 0:
            self.anger_level -= 1
        elif level == 2:
            self.anger_level += 1
        if self.anger_level < 0:
            self.anger_level = 0
        # print("Level: " + str(level) + " Anger: " + str(self.anger_level))


class Plant1(Plant):

    sell_price = 30
    production = 40

    def __init__(self, pos_x, pos_y, img):
        super().__init__(pos_x, pos_y, img)




