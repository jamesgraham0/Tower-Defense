import pygame
import os
pygame.font.init()

star = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/star.png")), (15,15))
star2 = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/star.png")), (20,20))


class Button:
    """
    Button class for menu objects
    """
    def __init__(self, menu, img, name):
        self.name = name
        self.img = img
        self.x = menu.x - 50
        self.y = menu.y - 110
        self.menu = menu
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def click(self, X, Y):
        """
        returns if the positon has collided with the menu
        :param X: int
        :param Y: int
        :return: bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def draw(self, win):
        """
        draws the button image
        :param win: surface
        :return: None
        """
        win.blit(self.img, (self.x, self.y))
        
    def update(self):
        """
        updates button position
        :return: None
        """
        if self.name == "Upgrade":
            self.x = self.menu.x - 50
            self.y = self.menu.y - 120
        if self.name == "Sell":
            self.x = self.menu.x - 50
            self.y = self.menu.y - 85
    

class PlayPauseButton(Button):
    def __init__(self, play_img, pause_img, x, y):
        self.img = play_img
        self.play = play_img
        self.pause = pause_img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.paused = True

    def draw(self, win):
        if self.paused:
            win.blit(self.play, (self.x, self.y))
        else:
            win.blit(self.pause, (self.x, self.y))


class VerticalButton(Button):
    """
    Button class for menu objects
    """
    def __init__(self, x, y, img, name, cost):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.cost = cost


class Menu:
    """
    menu for holding items (buttons), this is the menu
    that pops up when a tower is clicked (upgrade, sell, level, etc)
    """
    def __init__(self, tower, x, y, img, item_cost, sell_price):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.item_cost = item_cost
        self.item_sell_price = sell_price
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont("comicsans", 25)
        self.tower = tower

    def add_button(self, img, name):
        """
        adds buttons to menu
        :param img: surface
        :param name: str
        :return: None
        """
        self.items += 1
        self.buttons.append(Button(self, img, name))

    def get_item_cost(self):
        """
        gets cost of upgrade to next level
        :return: int
        """
        return self.item_cost[self.tower.level - 1]

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """

        win.blit(self.bg, (self.x - self.bg.get_width()/2, self.y-120))
        for item in self.buttons:
            item.draw(win)
            win.blit(star, (item.x + item.width - 1, item.y + 7))
            if item.name == "Upgrade":
                text = self.font.render(str(self.item_cost[self.tower.level - 1]), 1, (255,255,255))
            if item.name == "Sell":
                text = self.font.render(str(self.item_sell_price[self.tower.level - 1]), 1, (255,255,255))
            win.blit(text, (item.x + item.width + 30 - text.get_width()/2, item.y + star.get_height() -8))

    def get_clicked(self, X, Y):
        """
        return the clicked item from the menu
        :param X: int
        :param Y: int
        :return: str
        """
        for btn in self.buttons:
            if btn.click(X,Y):
                return btn.name
        return None

    def update(self):
        """
        update menu and button location
        :return: None
        """
        for btn in self.buttons:
            btn.update()


class VerticalMenu(Menu):
    """
    Vertical Menu for side bar of game
    """
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont("comicsans", 25)

    def add_button(self, img, name, cost):
        """
        adds buttons to menu
        :param img: surface
        :param name: str
        :return: None
        """
        self.items += 1
        
        if name == "buy_money":
            btn_x = self.x - 20
            btn_y = self.y-100 + (self.items-1)*120
        elif name == "buy_bomb":
            btn_x = self.x - 20
            btn_y = 470
        else:
            btn_x = self.x - 40
            btn_y = self.y-100 + (self.items-1)*120
        self.buttons.append(VerticalButton(btn_x, btn_y, img, name, cost))

    def get_item_cost(self, name):
        """
        gets cost of item
        :param name: str
        :return: int
        """
        for btn in self.buttons:
            if btn.name == name:
                return btn.cost
        return -1

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """
        win.blit(self.bg, (self.x - self.bg.get_width()/2, self.y-120))
        for item in self.buttons:
            item.draw(win)
            if item.name == "buy_money" or item.name == "buy_bomb":
                win.blit(star2, (item.x-20, item.y + item.height))
            else:
                win.blit(star2, (item.x+2, item.y + item.height))
            text = self.font.render(str(item.cost), 1, (255,255,255))
            win.blit(text, (item.x + item.width/2 - text.get_width()/2 + 5, item.y + item.height + 5))