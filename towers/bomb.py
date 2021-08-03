import pygame
import os
import math
from tower import Tower

bomb_image = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/bomb.png")).convert_alpha(), (50, 50))

class Bomb(Tower):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.price = 50
        self.selected = False
        self.name = "bomb"
        self.width = 40
        self.height = 40

        self.img = bomb_image
        self.damage = 50
        self.inRange = False
        self.range = 70
        self.hit = False
        self.visible = True

        self.place_color = (0, 0, 255, 100)

    def draw(self, win):
        """
        draws the tower
        :param win: surface
        :return: None
        """
        win.blit(self.img, (self.x - self.img.get_width()//2, self.y - self.img.get_height()//2))

    def draw_radius(self,win):
        if self.selected:
            # draw range circle
            surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)

            win.blit(surface, (self.x - self.range, self.y - self.range))

    def move(self, x, y):
        """
        moves tower to given x and y
        :param x: int
        :param y: int
        :return: None
        """
        self.x = x
        self.y = y

    def collide_path(self):
        """
        return True if tower is on path
        :param 
        """
        result = False
        # check first and last lines of path
        if self.x >= 119 and self.x <= 215:
            if self.y <= 285 or self.y >= 510:
                result = True

        # check second part of path
        if self.x >= 119 and self.x <= 435:
            if self.y >= 200 and self.y <= 290:
                result = True
        
        # check third part of path
        if self.x >= 350 and self.x <= 435:
            if self.y >= 95 and self.y <= 306:
                result = True

        #check fourth part of path
        if self.x >= 350 and self.x <= 655:
            if self.y >= 105 and self.y <= 185:
                result = True

        # check fifth part of path
        if self.x >= 575 and self.x <= 655:
            if self.y >= 95 and self.y <= 296:
                result = True

        # check sixth part of path
        if self.x >= 655 and self.x <= 890:
            if self.y >= 210 and self.y <= 296:
                result = True

        # check seventh part of path
        if self.x >= 805 and self.x <= 890:
            if self.y >= 210 and self.y <= 585:
                result = True

        # check eigth part of path
        if self.x >= 575 and self.x <= 890:
            if self.y >= 500 and self.y <= 585:
                result = True

        # check ninth part of path
        if self.x >= 575 and self.x <= 665:
            if self.y >= 395 and self.y <= 585:
                result = True

        # check tenth part of path
        if self.x >= 270 and self.x <= 665:
            if self.y >= 390 and self.y <= 480:
                result = True

        # check eleventh part of path
        if self.x >= 245 and self.x <= 330:
            if self.y >= 390 and self.y <= 590:
                result = True

        # check twelveth part of path
        if self.x >= 119 and self.x <= 330:
            if self.y >= 500 and self.y <= 590:
                result = True
        return result
        
        
    def attack(self, enemies):
        """
        attacks an enemy in the enemy list, modifies the list
        :param enemies: list of enemies
        :return:   
        """
        money = 0
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            x = enemy.x
            y = enemy.y

            # distance from tower to enemy
            dis = math.sqrt((self.x - enemy.img.get_width()/2 - x)**2 + (self.y -enemy.img.get_height()/2 - y)**2)
            if dis < self.range:
                self.inRange = True
                self.visible = False
                enemy_closest.append(enemy)

        enemy_closest = enemy_closest[::-1]
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if first_enemy.hit(self.damage) == True:
                money = first_enemy.money * 2
                enemies.remove(first_enemy)
                self.hit = True
                

        return money
        

    def draw_placement(self, win):
        # draw range circle
        surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.place_color, (70, 70), 70, 0)

        win.blit(surface, (self.x - 70, self.y - 70))
    

    def click(self, X, Y):
        """
        returns if tower has been clicked on
        and selects tower if it was clicked
        :param X: int
        :param Y: int
        :return: bool
        """
        pass
    