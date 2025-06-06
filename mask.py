import pygame
import random

class Mask(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.filled = False
        self.image = pygame.image.load("Mask.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.base_y = y  # Store original top y-position

        if x is not None and y is not None:
            self.rect.topleft = (x, y)
        else:
            self.rect.topleft = (random.randint(50, 750), random.randint(100, 400))
