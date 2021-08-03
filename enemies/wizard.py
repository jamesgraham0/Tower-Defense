import pygame
import os
from .enemy import Enemy

class Wizard(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "wizard"
        self.money = 100
        self.max_health = 300
        self.health = self.max_health
        self.img = pygame.transform.scale(pygame.image.load("./sprites/wizard.png").convert_alpha(), (75, 75))
        self.vel = 0.5