from game import Game
import pygame
import os

play_button = pygame.image.load("./sprites/play_button.png")

class MainMenu:
    def __init__(self, win):
        self.width = 900
        self.height = 700
        self.win = win
        self.background = pygame.image.load("./sprites/background.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.button = (self.width/2 - play_button.get_width()/2, 350, play_button.get_width(), play_button.get_height())
        self.title = pygame.transform.scale(pygame.image.load("./sprites/title.png"), (500, 200))

    def run(self):
        menuRun = True
        
        while menuRun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menuRun = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if self.button[0] <= x <= self.button[0] + self.button[2]:
                        if self.button[1] <= y <= self.button[1] + self.button[3]:
                            menuRun = False
                            game = Game(self.win)
                            game.run()
            self.draw_menu()
        pygame.quit()
    
    def draw_menu(self):
        self.win.blit(self.background, (0,0))
        self.win.blit(self.title, (self.width/2 - self.title.get_width()/2, self.height/2 - self.title.get_height()/2 - 100))
        self.win.blit(play_button, (self.button[0], self.button[1]))
        pygame.display.update()