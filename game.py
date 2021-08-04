import pygame
import os
from enemies.zombie import Zombie
from enemies.ghost import Ghost
from enemies.wizard import Wizard
from towers.turret import Turret
from towers.laser import Laser
from towers.money import Money
from towers.bomb import Bomb
from menus.menu import VerticalMenu, PlayPauseButton
import time
import random
pygame.font.init()
pygame.init()

lives_img = pygame.transform.scale2x(pygame.image.load("./sprites/heart.png"))
star_img = pygame.image.load("./sprites/star.png")
side_img = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/side_bar.png")).convert_alpha(), (120, 500))

buy_turret = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/turret_tower_image.png")).convert_alpha(), (75, 75))
buy_laser = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/laser_tower_image.png")).convert_alpha(), (75, 75))
buy_money = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/money.png")).convert_alpha(), (40, 40))
buy_bomb = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/bomb.png")).convert_alpha(), (40, 40))

play_button = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/play_button.png")).convert_alpha(), (90, 30))
pause_button = pygame.transform.scale(pygame.image.load(os.path.join("./sprites/pause_button.png")).convert_alpha(), (90, 30))


attack_tower_names = ["turret", "laser", "money", "bomb"]


# waves are in form
# frequency of enemies
# (# zombies, # ghosts, # wizards)
waves = [
    [10, 0, 0],
    [20, 0, 0],
    [20, 3, 0],
    [5, 8, 0],
    [3, 15, 0],
    [20, 10, 1],
    [20, 20, 2],
    [20, 25, 2],
    [10, 0, 3],
    [0, 4, 5],
    [20, 13, 5],
    [20, 30, 5],
    [50, 30, 8]
]

class Game:
    def __init__(self, win):
        self.width = 900
        self.height = 700
        self.win = win
        self.enemys = []
        self.attack_towers = []
        self.bombs = []
        self.lives = 10
        self.money = 800
        self.background = pygame.image.load("././sprites/background.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("comicsans", 65)
        self.selected_tower = None
        self.menu = VerticalMenu(60, 250, side_img)
        self.menu.add_button(buy_turret, "buy_turret", 400)
        self.menu.add_button(buy_laser, "buy_laser", 700)
        self.menu.add_button(buy_money, "buy_money", 1000)
        self.menu.add_button(buy_bomb, "buy_bomb", 50)

        self.moving_object = None
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.pause = True
        self.playPauseButton = PlayPauseButton(play_button, pause_button, self.menu.width/2 - play_button.get_width()/2, 550)
        self.randomColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.won = False

    def gen_enemies(self):
        """
        generate the next enemy or enemies to show
        :return: enemy
        """
        if sum(self.current_wave) == 0:
            if len(self.enemys) == 0:
                self.wave += 1
                self.randomColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.pause = True
                self.playPauseButton.paused = self.pause
                if self.wave == 13:
                    self.won = True
                else:
                    self.current_wave = waves[self.wave]
        else:
            wave_enemies = [Zombie(), Ghost(), Wizard()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            if self.won:
                from menus.win_menu import WinMenu
                winMenu = WinMenu(self.win)
                winMenu.run()
                run = False


            if self.pause == False:
                # gen monsters
                if time.time() - self.timer >= random.randrange(1, 6)/3:
                    self.timer = time.time()
                    self.gen_enemies()

            pos = pygame.mouse.get_pos()

            # check for moving object
            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])
                tower_list = self.attack_towers[:]

                collide = False
                # check if any towers collide with eachother
                for tower in tower_list:
                    if tower.collide(self.moving_object):
                        collide = True
                        tower.place_color = (255, 0, 0, 100)
                        self.moving_object.place_color = (255, 0, 0, 100)
                    else:
                        tower.place_color = (0, 0, 255, 100)
                        if not collide:
                            self.moving_object.place_color = (0, 0, 255, 100)

            # main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # if you're moving an object and click
                    if self.moving_object:
                        not_allowed = False
                        tower_list = self.attack_towers[:]
                        for tower in tower_list:
                            if tower.collide(self.moving_object):
                                not_allowed = True

                        if not not_allowed and self.moving_object.collide_path():
                            if self.moving_object.name in attack_tower_names:
                                self.attack_towers.append(self.moving_object)

                            self.moving_object.moving = False
                            self.moving_object = None

                    else:
#                        check for play or pause
                        if self.playPauseButton.click(pos[0], pos[1]):
                            self.pause = not(self.pause)
                            self.playPauseButton.paused = self.pause
                            tower_list = self.attack_towers[:]
                            for tower in tower_list:
                                tower.pauseShooting = True


                        # look if you click on side menu
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money -= cost
                                self.add_tower(side_menu_button)

                        # check to see what type of tower was clicked
                        button_clicked = None
                        if self.selected_tower:
                            if self.selected_tower.name != "buy_bomb" and self.selected_tower.name != "bomb":
                                button_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                                if button_clicked:
                                    if button_clicked == "Upgrade":
                                        if self.selected_tower.get_level() < 3:
                                            cost = self.selected_tower.get_upgrade_cost()
                                            if self.money >= cost:
                                                self.selected_tower.upgrade()
                                                self.money -= cost
                                    if button_clicked == "Sell":
                                        self.money += self.selected_tower.get_sell_price()
                                        try:
                                            self.attack_towers.remove(self.selected_tower)
                                        except Exception as e:
                                            print("sold the tower but now everytime tower is clicked you make money until you click somewhere else... hack?")
                                        # bug where you can select multiple towers at same time and sell the one that isn't selected,
                                        # then when you click on that tower it crashes
                                    

                        if not(button_clicked):
                            for tw in self.attack_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False

            # loop through enemies
            if not self.pause:
                to_del = []
                for en in self.enemys:
                    en.move()
                    if en.y > 700:
                        to_del.append(en)

                # delete all enemies off the screen
                for d in to_del:
                    self.lives -= 1
                    self.enemys.remove(d)

                # loop through attack towers
                for tw in self.attack_towers:
                    self.money += tw.attack(self.enemys)
                    if not tw.visible:
                        self.attack_towers.remove(tw)

                # if you lose
                if self.lives <= 0:
                    pygame.time.wait(1000)
                    from menus.main_menu import MainMenu
                    mainMenu = MainMenu(self.win)
                    mainMenu.run()

            self.draw()


    def draw(self):
        self.win.blit(self.background, (0,0))

        # draw placement rings
        if self.moving_object:
            for tower in self.attack_towers:
                tower.draw_placement(self.win)

            self.moving_object.draw_placement(self.win)

        # draw attack towers
        for tw in self.attack_towers:
            if tw.name != "buy_money":
                tw.draw(self.win)

        # draw enemies
        for en in self.enemys:
            en.draw(self.win)

        # draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)

        # draw menu
        self.menu.draw(self.win)

        # draw play pause button
        self.playPauseButton.draw(self.win)

        # draw lives
        text = self.life_font.render(str(self.lives), 1, (255,255,255))
        life = pygame.transform.scale(lives_img,(50,50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 13))
        self.win.blit(life, (start_x, 10))

        # draw money
        text = self.life_font.render(str(self.money), 1, (255, 255, 255))
        money = pygame.transform.scale(star_img, (50, 50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 75))
        self.win.blit(money, (start_x, 65))

        # draw wave
        text = self.life_font.render("Wave " + str(self.wave), 1, (self.randomColor))
        self.win.blit(text, (450 - text.get_width()/2, 10))


        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["buy_turret", "buy_laser", "buy_money", "buy_bomb"]
        object_list = [Turret(x, y), Laser(x, y), Money(x, y), Bomb(x, y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + " NOT VALID NAME")
