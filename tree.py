import pygame

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, surface_top_y):
        super().__init__()
        self.image = pygame.image.load("Tree.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = surface_top_y - self.rect.height + 32  # Add small positive offset
