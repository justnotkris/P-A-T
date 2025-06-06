import pygame
import sys
import time
import random
from player import Player
from mask import Mask
from tree import Tree
from pot import Pot
from pygame import mixer
pygame.init()

level = 1

level_configs = {
    1: {"smog_update": 2.5, "tree_spawn": 3, "pot_count": 5 },
    2: {"smog_update": 2, "tree_spawn": 5, "pot_count": 7},
    3: {"smog_update": 2, "tree_spawn": 7, "pot_count": 9},

}


WIDTH, HEIGHT, GROUND_Y, FPS = 800, 600, 500, 70
TREE_SPAWN_INTERVAL = level_configs[level]["tree_spawn"]                
smog_update = level_configs[level]["smog_update"]

mixer.music.load("bg.mp3")
mixer.music.play(-1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("P-A-T")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
background_img = pygame.transform.scale(pygame.image.load("Backround.jpg"), (WIDTH, HEIGHT)).convert()


GRAY, DARK, WHITE, RED, BROWN,BLACK,YELLOW,GREEN = (
    200, 200, 200), (50, 50, 50), (255, 255, 255), (255, 0, 0), (59, 59, 65),(0,0,0),(255,255,0),(0,255,0)

platforms = [
    pygame.Rect(300, 380, 200, 20),
    pygame.Rect(550, 270, 200, 20),
    pygame.Rect(50, 270, 200, 20),
    pygame.Rect(230, 160, 350, 20),
]
ground_rect = pygame.Rect(0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y)
spawn_surfaces = platforms + [ground_rect]

player = Player(100, GROUND_Y - 60)
player.trees = 0
player_group = pygame.sprite.Group(player)
mask_group, tree_group, pot_group = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

# Pot Placement
placed_pots = []
while len(pot_group) < level_configs[level]["pot_count"]:
    plat = random.choice(spawn_surfaces)
    x = random.randint(plat.left + 20, plat.right - 20)
    y = plat.top - 30
    if all(abs(x - px) > 50 for px, _ in placed_pots):
        pot_group.add(Pot(x, y))
        placed_pots.append((x, y))

smog_level, SMOG_MAX, masks_collected = 0, 10, 0
mask_spawn_time = last_smog_update = last_tree_spawn_time = time.time()
start_time = pygame.time.get_ticks()  # Start game timer

running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Smog Timer
    if time.time() - last_smog_update >= smog_update:
        smog_level = min(smog_level + 1, SMOG_MAX)
        last_smog_update = time.time()

    # Mask Spawn
    if time.time() - mask_spawn_time >= 2.6:
        plat = random.choice(platforms)
        x, y = random.randint(plat.left + 20, plat.right - 20), plat.top - 30
        mask_group.add(Mask(x, y))
        mask_spawn_time = time.time()

    # Tree Spawn
    if time.time() - last_tree_spawn_time >= TREE_SPAWN_INTERVAL:
        plat = random.choice(spawn_surfaces)
        x, y = random.randint(plat.left + 20, plat.right - 20), plat.top - 30
        tree_group.add(Tree(x, y))
        last_tree_spawn_time = time.time()

    # Player update
    player.update(keys)
    player.apply_gravity(platforms)

    # Collect masks
    for m in pygame.sprite.spritecollide(player, mask_group, True):
        masks_collected += 1
        smog_level = max(0, smog_level - 1)
        mask_sound = mixer.Sound("Mask.mp3")
        mask_sound.play()
       
    # Collect trees
    for t in pygame.sprite.spritecollide(player, tree_group, True):
        player.trees += 1

    # Fill pots
    for pot in pot_group:
        if player.rect.colliderect(pot.rect) and player.trees > 0 and not pot.filled:
            pot.fill()
            player.trees -= 1
            plant_sound = mixer.Sound("laser.wav")
            plant_sound.play()

    # Draw
    screen.blit(background_img, (0, 0))
    pygame.draw.rect(screen, DARK, ground_rect)
    for plat in platforms:
        pygame.draw.rect(screen, BROWN, plat)

    # Draw in correct layer order
    for group in (player_group, pot_group, mask_group, tree_group):
        group.draw(screen)

    # UI
    pygame.draw.rect(screen, WHITE, (20, 20, 200, 30))
    pygame.draw.rect(screen, RED, (20, 20, 20 * smog_level, 30))
    screen.blit(font.render(f"Smog: {smog_level}/{SMOG_MAX}", True, (0, 0, 0)), (230, 20))     
    screen.blit(font.render(f"Masks: {masks_collected}", True, (0, 0, 0)), (20, 60))
    screen.blit(font.render(f"Trees: {player.trees}", True, (0, 0, 0)), (20, 100))
    screen.blit(font.render(f"Level: {level}/3", True, (0, 0, 0)), (20, 140))

    # Timer (top-right corner)
    elapsed_seconds = (pygame.time.get_ticks() - start_time) // 1000
    timer_text = font.render(f"Time: {elapsed_seconds}s", True, (0, 0, 0))
    screen.blit(timer_text, (WIDTH - 160, 20))

    # Win/Lose conditions
    if smog_level >= SMOG_MAX:
        screen.blit(pygame.transform.scale(pygame.image.load("Backround-2.jpg"), (WIDTH, HEIGHT)).convert(), (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    elif all(pot.filled for pot in pot_group) and level <= 3:
        screen.blit(font.render(f"NEXT LEVEL (LEVEL - {level})", True, (0, 0, 0)), (WIDTH // 2 - 170, HEIGHT // 2)) 
        pygame.display.flip()
        mixer.music.load("complete.mp3")
        mixer.music.play(1)
        pygame.time.wait(1000)
        mixer.music.stop()

        level += 1
        if level in level_configs:
            # Reset game state
            smog_level = 0
            masks_collected = 0
            player.trees = 0
            pot_group.empty()
            mask_group.empty()
            tree_group.empty()

            # Load next level settings
            smog_update = level_configs[level]["smog_update"]
            TREE_SPAWN_INTERVAL = level_configs[level]["tree_spawn"]

            # Refill new pots
            placed_pots = []
            while len(pot_group) < level_configs[level]["pot_count"]:
                plat = random.choice(spawn_surfaces)
                x = random.randint(plat.left + 20, plat.right - 20)
                y = plat.top - 30
                if all(abs(x - px) > 50 for px, _ in placed_pots):
                    pot_group.add(Pot(x, y))
                    placed_pots.append((x, y))
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("Backround-4.jpg"), (WIDTH, HEIGHT)).convert(), (0, 0))
            pygame.display.flip()
            mixer.music.load("victory.mp3")
            mixer.music.play(-1)
            pygame.time.wait(8000)
            running = False
                                     
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
