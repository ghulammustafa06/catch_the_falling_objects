# main.py
import pygame
import random
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Catch the Falling Objects")

player = pygame.Rect(375, 500, 50, 50)  # Player as a rectangle
falling_objects = []

running = True
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
        falling_objects.append(pygame.Rect(random.randint(0, 750), 0, 50, 50))

    for obj in falling_objects:
        obj.y += 5
        if player.colliderect(obj):
            print("Caught!")
            falling_objects.remove(obj)

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), player)
    for obj in falling_objects:
        pygame.draw.rect(screen, (255, 0, 0), obj)
    pygame.display.flip()

pygame.quit()
