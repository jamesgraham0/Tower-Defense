import pygame
from tower import Tower
import os
import math
from menus.menu import Menu
from towers.animation.spritesheet import Spritesheet


menu_for_upgrades = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/side_bar.png")).convert_alpha(), (120, 70))
upgrade_button = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/upgrade_button.png")).convert_alpha(), (50, 35))
sell_button = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/sell_button.png")).convert_alpha(), (50, 35))


# load turrets
turret_sheet1 = Spritesheet('./towers/animation/turret_sheet.png')
tower_imgs = [turret_sheet1.parse_sprite('turret1.png'), 
            turret_sheet1.parse_sprite('turret2.png'),
            turret_sheet1.parse_sprite('turret3.png'),
            turret_sheet1.parse_sprite('turret4.png'),
            turret_sheet1.parse_sprite('turret5.png'),
            turret_sheet1.parse_sprite('turret6.png'),
            turret_sheet1.parse_sprite('turret7.png'),
            turret_sheet1.parse_sprite('turret8.png')]

turret_sheet2 = Spritesheet('./towers/animation/turret_sheet2.png')
tower_imgs2 = [turret_sheet2.parse_sprite('turret1.png'), 
            turret_sheet2.parse_sprite('turret2.png'),
            turret_sheet2.parse_sprite('turret3.png'),
            turret_sheet2.parse_sprite('turret4.png'),
            turret_sheet2.parse_sprite('turret5.png'),
            turret_sheet2.parse_sprite('turret6.png'),
            turret_sheet2.parse_sprite('turret7.png'),
            turret_sheet2.parse_sprite('turret8.png')]

turret_sheet3 = Spritesheet('./towers/animation/turret_sheet3.png')
tower_imgs3 = [turret_sheet3.parse_sprite('turret1.png'), 
            turret_sheet3.parse_sprite('turret2.png'),
            turret_sheet3.parse_sprite('turret3.png'),
            turret_sheet3.parse_sprite('turret4.png'),
            turret_sheet3.parse_sprite('turret5.png'),
            turret_sheet3.parse_sprite('turret6.png'),
            turret_sheet3.parse_sprite('turret7.png'),
            turret_sheet3.parse_sprite('turret8.png')]


class Turret(Tower):
    def __init__(self, x,y):
        super().__init__(x, y)
        self.tower_imgs = tower_imgs[:]
        self.tower_imgs2 = tower_imgs2[:]
        self.tower_imgs3 = tower_imgs3[:]
        self.sell_price = [350, 500, 700]
        self.price = [350, 600, "MAX"]
        self.turret_count = 0
        self.range = 200
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 10
        self.original_damage = self.damage
        self.width = self.height = 90
        self.moving = False
        self.name = "turret"
        self.damage_increase = 6

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
        draw the turret tower and animated turret
        :param win: surface
        :return: int
        """
        super().draw_radius(win)
        super().draw(win)

        # Animating the turret shooting
        if self.inRange and not self.moving:
            self.turret_count += 1
            if self.turret_count >= len(self.tower_imgs) * 8:
                self.turret_count = 0
        else:
            self.turret_count = 0

        # Placing the animated turret
        turret = self.tower_imgs[self.turret_count // 8]
        win.blit(turret, (self.x - turret.get_width()/2, self.y - turret.get_height()/2))

    def change_range(self, r):
        """
        change range of turret tower
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
            if self.turret_count == 50:
                if first_enemy.hit(self.damage) == True:
                    money = first_enemy.money * 2
                    enemies.remove(first_enemy)


        return money