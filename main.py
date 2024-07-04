# main.py
import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Catch the Falling Objects")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()


player = pygame.Rect(375, 500, 50, 50)  # Player as a rectangle

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.display.flip()

