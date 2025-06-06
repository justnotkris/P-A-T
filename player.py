import pygame

GRAVITY = 0.5
JUMP_STRENGTH = -12

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.on_ground = False
        self.speed = 5
        self.trees = 0

    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

        # Screen bounds
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, 800)

    def apply_gravity(self, platforms):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False

        # Ground collision
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vel_y = 0
            self.on_ground = True

        # Platform collision
        for plat in platforms:
            if self.rect.colliderect(plat) and self.vel_y >= 0:
                if self.rect.bottom <= plat.top + 20:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True


