import pygame
from tower import Tower
import os
import math
from menus.menu import Menu
from towers.animation.spritesheet import Spritesheet


menu_for_upgrades = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/side_bar.png")).convert_alpha(), (120, 70))
upgrade_button = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/upgrade_button.png")).convert_alpha(), (50, 35))
sell_button = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/sell_button.png")).convert_alpha(), (50, 35))


# load lasers
laser_sheet1 = Spritesheet('./towers/animation/laser_sheet.png')
tower_imgs = [laser_sheet1.parse_sprite('laser1.png'), 
            laser_sheet1.parse_sprite('laser2.png'),
            laser_sheet1.parse_sprite('laser3.png'),
            laser_sheet1.parse_sprite('laser4.png'),
            laser_sheet1.parse_sprite('laser5.png'),
            laser_sheet1.parse_sprite('laser6.png'),
            laser_sheet1.parse_sprite('laser7.png'),
            laser_sheet1.parse_sprite('laser8.png')]

laser_sheet2 = Spritesheet('./towers/animation/laser_sheet2.png')
tower_imgs2 = [laser_sheet2.parse_sprite('laser1.png'), 
            laser_sheet2.parse_sprite('laser2.png'),
            laser_sheet2.parse_sprite('laser3.png'),
            laser_sheet2.parse_sprite('laser4.png'),
            laser_sheet2.parse_sprite('laser5.png'),
            laser_sheet2.parse_sprite('laser6.png'),
            laser_sheet2.parse_sprite('laser7.png'),
            laser_sheet2.parse_sprite('laser8.png')]

laser_sheet3 = Spritesheet('./towers/animation/laser_sheet3.png')
tower_imgs3 = [laser_sheet3.parse_sprite('laser1.png'), 
            laser_sheet3.parse_sprite('laser2.png'),
            laser_sheet3.parse_sprite('laser3.png'),
            laser_sheet3.parse_sprite('laser4.png'),
            laser_sheet3.parse_sprite('laser5.png'),
            laser_sheet3.parse_sprite('laser6.png'),
            laser_sheet3.parse_sprite('laser7.png'),
            laser_sheet3.parse_sprite('laser8.png')]


class Laser(Tower):
    def __init__(self, x,y):
        super().__init__(x, y)
        self.tower_imgs = tower_imgs[:]
        self.tower_imgs2 = tower_imgs2[:]
        self.tower_imgs3 = tower_imgs3[:]
        self.sell_price = [500, 800, 1100]
        self.price = [500, 800, "MAX"]
        self.laser_count = 0
        self.range = 200
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 10
        self.original_damage = self.damage
        self.width = self.height = 90
        self.moving = False
        self.name = "laser"
        self.damage_increase = 7

        self.menu = Menu(self, self.x, self.y, menu_for_upgrades, self.price, self.sell_price)
        self.menu.add_button(upgrade_button, "Upgrade")
        self.menu.add_button(sell_button, "Sell")
        self.pauseShooting = False

    def get_upgrade_cost(self):
        """
        gets the upgrade cost
        :return: int
        """
        return self.menu.get_item_cost()

    def draw(self, win):
        """
        draw the laser tower and animated laser
        :param win: surface
        :return: int
        """
        super().draw_radius(win)
        super().draw(win)

        # Animating the laser shooting
        if self.inRange and not self.moving:
            self.laser_count += 1
            if self.laser_count >= len(self.tower_imgs) * 8:
                self.laser_count = 0
        else:
            self.laser_count = 0

        # Placing the animated laser
        laser = self.tower_imgs[self.laser_count // 8]
        win.blit(laser, (self.x - laser.get_width()/2, self.y - laser.get_height()/2))

    def change_range(self, r):
        """
        change range of laser tower
        :param r: int
        :return: None
        """
        self.range = r

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
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x: x.path_pos)
        enemy_closest = enemy_closest[::-1]
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if self.laser_count == 50:
                if first_enemy.hit(self.damage) == True:
                    money = first_enemy.money * 2
                    enemies.remove(first_enemy)


        return money