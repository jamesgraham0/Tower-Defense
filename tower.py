import pygame
import os
from menus.menu import Menu
import math

menu_button = pygame.transform.scale(pygame.image.load("./sprites/side_bar.png").convert_alpha(), (120, 70))
upgrade_button = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/upgrade_button.png")).convert_alpha(), (50, 35))
sell_button = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/sell_button.png")).convert_alpha(), (50, 35))


class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sell_price = []
        self.price = []
        self.level = 1
        self.selected = False
        self.damage_increase = 4

        # Menu for Upgrade/Sell
        self.menu = Menu(self, self.x, self.y, menu_button, self.price, self.sell_price)
        self.menu.add_button(upgrade_button, "Upgrade")
        self.menu.add_button(sell_button, "Sell")

        self.tower_imgs = []
        self.tower_imgs2 = []
        self.tower_imgs3 = []
        self.damage = 1
        self.visible = True

        self.place_color = (0, 0, 255, 100)

    def get_level(self):
        return self.level

    def get_sell_price(self):
        """
        call to sell the tower, returns sell price
        :return: int
        """
        return self.sell_price[self.level-1]

    def draw(self, win):
        """
        draws the tower
        :param win: surface
        :return: None
        """
        img = self.tower_imgs[0]
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))

        # draw menu
        if self.selected:
            self.menu.draw(win)

    def draw_radius(self,win):
        if self.selected:
            # draw range circle
            surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)

            win.blit(surface, (self.x - self.range, self.y - self.range))

    def draw_placement(self,win):
        # draw range circle
        surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.place_color, (40, 40), 40, 0)

        win.blit(surface, (self.x - 40, self.y - 40))

    def click(self, X, Y):
        """
        returns if tower has been clicked on
        and selects tower if it was clicked
        :param X: int
        :param Y: int
        :return: bool
        """
        img = self.tower_imgs[self.level - 1]
        if X <= self.x - img.get_width()//2 + self.width and X >= self.x - img.get_width()//2:
            if Y <= self.y + self.height - img.get_height()//2 and Y >= self.y - img.get_height()//2:
                return True
        return False
        

    def upgrade(self):
        """
        upgrades the tower for a given cost
        :return: None
        """
        
        if self.level == 2:
            self.tower_imgs = self.tower_imgs3
            self.level += 1
            self.damage += self.damage_increase
            
        if self.level == 1:
            self.tower_imgs = self.tower_imgs2
            self.level += 1
            self.damage += self.damage_increase

        

    def get_upgrade_cost(self):
        """
        returns the upgrade cost, if 0 then can't upgrade anymore
        :return: int
        """
        return self.price[self.level-1]

    def move(self, x, y):
        """
        moves tower to given x and y
        :param x: int
        :param y: int
        :return: None
        """
        self.x = x
        self.y = y
        self.menu.x = x
        self.menu.y = y
        self.menu.update()

    def collide(self, otherTower):
        """
        returns true if tower is too close to another tower
        :param otherTower: the tower that has already been placed
        :return: bool
        """
        if otherTower.name == "buy_bomb" or otherTower.name == "bomb":
            return False
        x2 = otherTower.x
        y2 = otherTower.y

        dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
        if dis >= 80:
            return False
        else:
            return True

    def collide_path(self):
        """
        return false if tower is too close to path
        :param 
        """
        result = True
        # check first and last lines of path
        if self.x >= 119 and self.x <= 215:
            if self.y <= 285 or self.y >= 510:
                result = False

        # check second part of path
        if self.x >= 119 and self.x <= 435:
            if self.y >= 200 and self.y <= 306:
                result = False
        
        # check third part of path
        if self.x >= 350 and self.x <= 435:
            if self.y >= 95 and self.y <= 306:
                result = False

        #check fourth part of path
        if self.x >= 350 and self.x <= 655:
            if self.y >= 95 and self.y <= 185:
                result = False

        # check fifth part of path
        if self.x >= 575 and self.x <= 655:
            if self.y >= 95 and self.y <= 296:
                result = False

        # check sixth part of path
        if self.x >= 655 and self.x <= 890:
            if self.y >= 210 and self.y <= 296:
                result = False

        # check seventh part of path
        if self.x >= 805 and self.x <= 890:
            if self.y >= 210 and self.y <= 585:
                result = False

        # check eigth part of path
        if self.x >= 575 and self.x <= 890:
            if self.y >= 500 and self.y <= 585:
                result = False

        # check ninth part of path
        if self.x >= 575 and self.x <= 665:
            if self.y >= 395 and self.y <= 585:
                result = False

        # check tenth part of path
        if self.x >= 270 and self.x <= 665:
            if self.y >= 390 and self.y <= 480:
                result = False

        # check eleventh part of path
        if self.x >= 245 and self.x <= 330:
            if self.y >= 390 and self.y <= 590:
                result = False

        # check twelveth part of path
        if self.x >= 119 and self.x <= 330:
            if self.y >= 500 and self.y <= 590:
                result = False

        # check side menu
        if self.x >= 0 and self.x <= 130:
            if self.y >= 120 and self.y <= 650:
                result = False

        return result
        
        
        
    
    