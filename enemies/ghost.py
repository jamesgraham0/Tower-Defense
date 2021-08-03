import pygame
import os
from .enemy import Enemy

class Ghost(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "ghost"
        self.money = 30
        self.max_health = 30
        self.health = self.max_health
        self.img = pygame.transform.scale(pygame.image.load("./sprites/ghost.png").convert_alpha(), (50, 50))
        self.vel = 1