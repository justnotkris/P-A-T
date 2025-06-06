import pygame

class Pot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.filled = False
        self.image = pygame.image.load("Pot_Tree=False.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.base_y = y  # Store original top y-position

    def fill(self):
        self.filled = True
        self.image = pygame.image.load("Pot_Tree.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 60))
        old_bottom = self.rect.bottom
        self.rect = self.image.get_rect(midbottom=(self.rect.centerx, old_bottom))
