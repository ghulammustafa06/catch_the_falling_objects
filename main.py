# main.py
import pygame
import random
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Catch the Falling Objects")

player = pygame.Rect(375, 500, 50, 50)  # Player as a rectangle

class FallingObject:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, 750), 0, 50, 50)
        self.speed = random.randint(3, 7)

falling_objects = []

def show_start_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Catch the Falling Objects", True, (255, 255, 255))
    screen.blit(text, (50, 250))
    font = pygame.font.Font(None, 36)
    text = font.render("Press any key to start", True, (255, 255, 255))
    screen.blit(text, (250, 350))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over_screen(final_score):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, (300, 250))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Final Score: {final_score}", True, (255, 255, 255))
    screen.blit(text, (300, 350))
    pygame.display.flip()
    pygame.time.wait(2000)

show_start_screen()

running = True
score = 0
missed = 0
max_missed = 5

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5

    if random.randint(1, 20) == 1:  # Randomly create falling objects
        falling_objects.append(FallingObject())

    for obj in falling_objects:
        obj.rect.y += obj.speed
        if player.colliderect(obj.rect):
            score += 1
            falling_objects.remove(obj)
        elif obj.rect.y > 600:
            missed += 1
            falling_objects.remove(obj)

    if missed >= max_missed:
        show_game_over_screen(score)
        running = False

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), player)
    for obj in falling_objects:
        pygame.draw.rect(screen, (255, 0, 0), obj.rect)

    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score} Missed: {missed}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
 