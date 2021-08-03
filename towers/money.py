import pygame
from tower import Tower
import os
from menus.menu import Menu
import random



menu_for_upgrades = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/side_bar.png")).convert_alpha(), (120, 70))
upgrade_button = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/upgrade_button.png")).convert_alpha(), (50, 35))
sell_button = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/sell_button.png")).convert_alpha(), (50, 35))
money_image = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/money.png")).convert_alpha(), (50, 50))


class Money(Tower):
    def __init__(self, x,y):
        super().__init__(x, y)
        self.tower_imgs = [money_image]
        self.tower_imgs2 = [money_image]
        self.tower_imgs3 = [money_image]

        self.sell_price = [350, 600, 850]
        self.price = [450, 1000, "MAX"]
        self.damage = 0
        self.original_damage = self.damage
        self.width = self.height = 90
        self.moving = False
        self.name = "money"

        self.menu = Menu(self, self.x, self.y, menu_for_upgrades, self.price, self.sell_price)
        self.menu.add_button(upgrade_button, "Upgrade")
        self.menu.add_button(sell_button, "Sell")

        self.range = 40
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.makingMoney = False


    
    def click(self, X, Y):
        """
        returns if tower has been clicked on
        and selects tower if it was clicked
        :param X: int
        :param Y: int
        :return: bool
        """
        img = self.tower_imgs[0]
        if X <= self.x - img.get_width()//2 + self.width and X >= self.x - img.get_width()//2:
            if Y <= self.y + self.height - img.get_height()//2 and Y >= self.y - img.get_height()//2:
                return True
        return False

    def get_upgrade_cost(self):
        """
        gets the upgrade cost
        :return: int
        """
        return self.menu.get_item_cost()

    def draw(self, win):
        """
        draw the money tower and animated money
        :param win: surface
        :return: int
        """
        super().draw_radius(win)
        super().draw(win)
        win.blit(money_image, (self.x - money_image.get_width()/2, self.y - money_image.get_height()/2))


    def draw_placement(self, win):
        # draw range circle
        surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.place_color, (40, 40), 40, 0)

        win.blit(surface, (self.x - 40, self.y - 40))


    def attack(self, win):
        """
        stars gained from money tower
        :return: int
        """
        result = 0
        num = random.randint(0, 100)
        if self.level == 3 and num == 0:
            self.makingMoney = True
            result = 4
        elif self.level == 2 and num == 1:
            self.makingMoney = True
            result = 3
        elif self.level == 1 and num == 2:
            self.makingMoney = True
            result = 2
        return result ** 2

  
