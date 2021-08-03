import pygame
import os
from .enemy import Enemy

class Zombie(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "zombie"
        self.money = 10
        self.max_health = 10
        self.health = self.max_health
        self.img = pygame.transform.scale(pygame.image.load("./sprites/zombie.png").convert_alpha(), (50, 50))
        self.vel = 2